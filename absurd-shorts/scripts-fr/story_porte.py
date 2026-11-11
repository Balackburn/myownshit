#!/usr/bin/env python3
"""La porte (story 39, cycle 3 of the cartoon staging): this man held the door for a lady. He is still holding it. Behind her there was the whole
town. The town hall counted: four thousand passages a day. At that level it is a public service, and a public service does not close. His
replacement is in the queue. In the evening he goes home; the arm stays. The door is listed as a historic monument; the arm too. Yesterday a
technician came by: it was automatic. The lady never said thank you.
Cartoon rig with guided hands (cycle 3): the hand stays on the handle whatever the body does, and the arm stretches as far as it must.
Natural look."""
from story_kit import *
import math

st = Story('porte', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 9), ('S03', 'L02', 0), ('S04', 'L02', 5), ('S05', 'L03', 0), ('S06', 'L04', 0), ('S07', 'L05', 0), ('S08', 'L05', 5), ('S09', 'L06', 0),
         ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L08', 4), ('S13', 'L09', 0), ('S14', 'L09', 6), ('S15', 'L10', 0), ('S16', 'L10', 5), ('S17', 'L11', 0)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}
# ---- the bakery door, on the right-hand pavement of the Paris street: its front faces the road (-X)
DX, DZ, DW = 9.93, 0.0, 1.0                          # the middle of the threshold; the leaf's width
STREET = {'clear': [-30, 30], 'eiffel': False}
OPEN = 80                                           # degrees: the leaf held open
def handle(deg, slide=0.0):                          # the handle in the world (the same numbers as doorHandle in engine/props_porte.js; the door is turned -90 degrees)
    a = math.radians(deg); r = DW - 0.12
    lx = -DW / 2 + r * math.cos(a) - 0.07 * math.sin(a) + slide; lz = 0.03 + r * math.sin(a) + 0.07 * math.cos(a)
    return [round(DX - lz, 3), 1.1, round(DZ + lx, 3)]
SIGNW = 1.5                                         # a sign hardly wider than the door: close shots of him clear it (a wider one was cut in two by every tight frame)
DOOR = lambda **kw: P('door', 'shopDoor', pos=[DX, 0, DZ], ry=-90, opts={'w': DW, 'h': 2.5, 'signW': SIGNW, **kw})
PUBLIC = {'sign': 'SERVICE\nPUBLIC', 'signBg': '#2A4B9B', 'signFg': '#F4F1E8', 'signEdge': '#F4F1E8'}   # the bakery's sign once it is a public service: the same object as the plate that slams over it in S08 (two lines, a cream border)
HOLD = [9.12, 0, -1.02]                             # where he stands to hold it: beside the open leaf, facing the road
GRIP = lambda deg, w=1, **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*handle(deg), w, 0.05, [0.2, -1, 0.5]]}, **kw}
RIP = lambda a, ph, n=2: {'armL': [a, n, ph, 0, 1.5708], 'foreL': [a, n, ph - n, 0, 1.5708]}   # a ripple along the stretched arm (toon channel `wave`): a metres high, n waves on each half, moved along by ph (rising: toward the hand)

# 1: he reaches the bakery door, sees a lady coming, pulls it open with a bow; she walks in without a look
O1 = 0.42                                           # the door starts to open
LADY = [(7.4, 4.6), (8.3, 0.25), (10.6, 0.0)]       # her way: along the pavement, then in
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [9.05, 0, 0.55], -90, 'stand', 'neutral', keys=[k(0.0, toon=GRIP(0), toonDur=0), k(0.0, look=[9.0, 1.2, 0.5]), k(0.14, look='dame', expr='surprised'),
            k(0.3, expr='happy'), k(O1, to=HOLD, dur=0.24, glide=True, ease='inOut', face=-90), k(O1, toon=GRIP(OPEN, sq=[1.03, 0.96, 1.03]), toonDur=0.24, toonEase='inOut'),
            k(O1 + 0.3, toon=GRIP(OPEN, bend={'spine': [0.64, 0, 0.1, 1, None], 'neck': [0.26, 0, 0, 1, None]}, sq=[1.03, 0.96, 1.03], hands={'L': 'grip', 'R': 'open'}, reach={'L': [*handle(OPEN), 1, 0.05, [0.2, -1, 0.5]], 'R': [8.86, 1.08, -1.14, 1, 0.1]}), toonDur=0.16, toonEase='outBack'), k(O1 + 0.3, look=[7.8, 0.6, 0.3], expr='proud'),   # a bow: his back curves, his free hand comes to his stomach (it was his head alone, on a hinge)
            k(1.3, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.18), k(1.3, look=None, expr='happy'), k(1.46, toon=GRIP(OPEN, face={'gx': 0.9, 'lid': 1}), toonDur=0.04),   # he straightens: his eyes go in after her; a blink
            k(1.52, look=[7.5, 1.6, 6.0], expr='surprised'), k(1.54, toon=GRIP(OPEN, sq=[0.97, 1.05, 0.97], face={'eye': 0.2, 'brow': 0.6}), toonDur=0.08, toonEase='outBack'),   # then his head turns up the street: somebody else is coming
            k(1.72, toon=GRIP(OPEN, face={'eye': 0.3, 'brow': 0.8, 'jaw': 0.25}), toonDur=0.1)]),   # and somebody else (the next shot)
        act('dame', [LADY[0][0], 0, LADY[0][1]], 180, 'walk', 'smug', keys=[k(0.0, to=[LADY[1][0], 0, LADY[1][1]], dur=1.05, clip='walk', ease='linear'), k(1.05, to=[LADY[2][0], 0, LADY[2][1]], dur=0.55, clip='walk', ease='linear'),
            k(1.44, visible=False)])],
        props=[DOOR(swing=[[0, 0], [O1, 0], [O1 + 0.24, OPEN]])],
        cams=[cam(0.0, [4.3, 1.7, -2.3], [4.5, 1.7, -2.2], [9.7, 1.5, -0.3], [9.7, 1.5, -0.3], lens=44)])   # from the side he steps to: the open leaf is seen at an angle, a pane of glass beside him

# 2: he is still holding it: people shoot through the doorway one after the other; at each one his beard grows a notch; a cobweb between his arm and the leaf
HOLDK = lambda **kw: k(-0.05, toon=GRIP(OPEN, **kw), toonDur=0)
def rusher(i, t0, z0=0.25, x0=5.2, z1=0.0):            # somebody who dashes into the bakery
    return act(f'r{i}', [x0, 0, z0], 90, 'stand', 'neutral', keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, to=[DX + 0.6, 0, z1], dur=0.2, clip='dashOff', ease='linear', blend=0.01), k(t0 + 0.19, visible=False)])
BEARD = lambda sc=1.25, **kw: P('beard', 'beard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.03, 0.09], 'rot': [0, 0, 0]}, scale=sc, opts={'color': '#17161A'}, **kw)   # it stays from now on
JAWB = [0.0, -0.2, 0.14]                            # where the beard hangs when his jaw has dropped: under the chin, in front of the chest (at the depth of the face it was inside the chest: no beard in either take)
WEB = lambda **kw: P('web', 'spiderWeb', pos=[9.02, 1.42, -0.7], ry=-90, opts={'r': 0.3}, **kw)
B2 = [0.12, 0.42, 0.72]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(0.0, look=None)] + [x for t in B2 for x in (k(t, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.03), k(t + 0.08, toon=GRIP(OPEN, face={'gx': 1.0}), toonDur=0.1), k(t + 0.22, toon=GRIP(OPEN), toonDur=0.06))] +   # his eyes alone follow each one in
            [k(B2[1], expr='unimpressed'), k(0.9, expr='deadpan')])] + [rusher(i, t, z0=-2.1, x0=6.6) for i, t in enumerate(B2)],   # they cut across in front of him, between the camera and him: three streaks
        props=[DOOR(swing=[[0, OPEN]]), BEARD(0.01, keys=[k(B2[0] + 0.12, scale=0.5, dur=0.1, ease='outBack'), k(B2[1] + 0.12, scale=0.85, dur=0.1, ease='outBack'), k(B2[2] + 0.12, scale=1.25, dur=0.1, ease='outBack')]),
               WEB(scale=0.01, keys=[k(B2[2] + 0.05, scale=1.0, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [6.5, 1.5, -0.45], [6.65, 1.5, -0.5], [9.3, 1.38, -0.8], [9.3, 1.38, -0.8], lens=44)])   # close: the sign above the door stays out of the frame (it was cut in two)
# 3: behind her there was... first what he sees: the queue, down the pavement, out of sight; then his face, to us: eyes out, the jaw on his tie
QUEUE = lambda **kw: P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[7.7, 1.6], [7.5, 190.0]], 'gap': 0.8, 'people': True, 'seed': 9, **kw})
T3 = 0.56                                           # the cut to his face
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(-0.3, look=[7.6, 1.6, 12.0]), k(T3, look=None), k(T3, toon=GRIP(OPEN, sq=[1.1, 0.85, 1.1], scl={'head': [1.12, 0.86, 1]}, face={'lid': 1}), toonDur=0.04), k(T3 + 0.08, expr='take'),   # a squash first
            k(T3 + 0.08, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.9, 'popLen': 0.14}, sq=[1.04, 0.95, 1.04]), toonDur=0.07, toonEase='outBack'), k(T3 + 0.4, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.9, 'popLen': 0.14}), toonDur=0.1)])],   # the jaw drops, the eyes come out at us; he does not stretch up (his eyes left the frame)
        props=[DOOR(swing=[[0, OPEN]]), QUEUE(), BEARD(keys=[k(T3 + 0.08, attach='mec', joint='head', offset=JAWB, rot=[0, 0, 0])]), WEB()],
        cams=[cam(0.0, [8.7, 1.6, -1.6], [8.65, 1.62, -1.2], [7.5, 1.5, 14.0], [7.5, 1.5, 14.0], lens=44),
              cam(T3, [6.55, 1.55, -1.3], [6.7, 1.55, -1.28], [9.12, 1.53, -1.17], [9.12, 1.53, -1.17], lens=44)])   # the frame stops under the sign and left of it
# 4: ...the town: from above, the queue runs down the street out of sight; he is at the bottom of the frame, at his door
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK()])],
        props=[DOOR(swing=[[0, OPEN]]), QUEUE(), BEARD(), WEB()],
        cams=[cam(0.0, [6.8, 7.5, -8.0], [6.9, 9.0, -9.5], [8.2, 0.8, 9.0], [8.2, 0.8, 12.0], lens=44)])

# 5: the town hall counted: a clerk at the other jamb with a hand counter: one click for each who goes in; they go in faster and faster: his head follows
#    each one like a tennis match, his thumb swells
CLERK = [9.25, 0, 1.05]
R5 = [0.08, 0.34, 0.56, 0.74, 0.88, 0.99, 1.08, 1.16]   # they go in, closer and closer together
CLICK = lambda **kw: P('clicker', 'tallyClicker', on={'actor': 'agent', 'hand': 'R', 'offset': [0, -0.02, 0.03], 'rot': [0, 0, 0]}, **kw)
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[act('agent', CLERK, -90, 'stand', 'determined', keys=[k(0.0, toon={'hands': {'R': 'grip'}, 'reach': {'R': [8.95, 1.55, 1.0, 1, 0.05]}}, toonDur=0)] +
            [x for i, t in enumerate(R5) for x in (k(max(0.0, t - 0.05), look=[6.2, 1.6, 1.9]), k(t + 0.06, look=[7.4, 1.6, -0.6]))] +   # like a tennis match, between two points in front of him: his face stays on us
            [k(0.7, expr='worried'), k(0.4, toon={'hands': {'R': 'grip'}, 'reach': {'R': [8.95, 1.55, 1.0, 1, 0.05]}, 'scl': {'handR': [1.7, 1.7, 1.7]}}, toonDur=0.8, toonEase='inOut'), k(1.1, expr='scared')])] +   # the fist swells from the fourth click on
        [rusher(i, t, z0=0.58 + 0.07 * (i % 3), z1=0.3) for i, t in enumerate(R5)],   # they go in on his side of the doorway: whole in the frame
        props=[DOOR(swing=[[0, OPEN]], signHide=[[0, 9]]), CLICK(opts={'at': 0.05, 'rate': 9})],
        cams=[cam(0.0, [5.6, 1.55, 1.3], [5.75, 1.57, 1.27], [9.4, 1.36, 0.7], [9.4, 1.36, 0.7], lens=44)])   # the clerk in the right half, the doorway and those who dash in on the left; the bakery's sign put away (the frame cut it to NGERIE)
# 6: « four thousand passages a day »: he has stepped aside to the counter on the wall, which rolls up to it; he reads it out, his thumb still swollen,
#    the clicker smoking
CLERK6 = [9.25, 0, 1.75]
W6 = [st.at('S06', 'L04', i) for i in range(5)]      # « Quatre mille passages par jour »
CLK6 = lambda y, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [8.9, y, 1.45, 1, 0.05]}, 'scl': {'handR': [1.7, 1.7, 1.7]}, **kw}
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[act('agent', CLERK6, -90, 'stand', 'worried', keys=[k(0.0, toon=CLK6(1.7, face={'sweat': 1}), toonDur=0), k(0.0, look=None)] + st.talk('L04', 'S06', 'worried') +
            [x for i in (0, 1) for x in (k(W6[i], toon=CLK6(1.7, bend={'neck': [0.22, 0, 0, 1, None], 'spine': [0.08, 0, 0, 1, None]}, face={'sweat': 1, 'brow': 0.6, 'eye': 0.2}), toonDur=0.06), k(W6[i] + 0.12, toon=CLK6(1.7, face={'sweat': 1}), toonDur=0.1))] +   # a nod on « quatre », on « mille »
            [k(W6[2] - 0.02, toon=CLK6(2.0, sq=[0.97, 1.04, 0.97], face={'sweat': 1, 'browL': 0.8, 'browR': -0.3, 'gx': -0.6}), toonDur=0.14, toonEase='outBack'),   # the clicker held up, smoking: the proof
             k(W6[4], toon=CLK6(2.0, face={'sweat': 1, 'lid': 1}), toonDur=0.04), k(W6[4] + 0.1, toon=CLK6(2.0, face={'sweat': 1}), toonDur=0.05)])],   # a blink
        props=[DOOR(swing=[[0, OPEN]]), CLICK(), P('counter', 'rollCounter', pos=[9.9, 2.98, 1.75], ry=-90, scale=0.01, opts={'from': 0, 'to': 4000, 'at': 0.12, 'dur': 0.7, 'w': 1.0, 'h': 0.62}, keys=[k(0.02, scale=1.0, dur=0.14, ease='outBack')]),
               P('smoke', 'dustPuff', pos=[8.85, 1.85, 1.45], scale=0.2, opts={'period': 0.6, 'color': '#C9C9C9'}, keys=[k(W6[2] - 0.02, to=[8.85, 2.15, 1.45], dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [6.5, 2.05, 2.2], [6.7, 2.07, 2.15], [9.5, 2.2, 1.68], [9.5, 2.2, 1.68], lens=44)])
# 7: at that level it is a... the mayor marches up in his sash and points at him
MAYOR = [9.15, 0, 0.72]                             # the mayor, by the other jamb, three quarters to us
M7 = 0.42                                           # the mayor has arrived: his finger comes out
JAB7 = [M7 + 0.24, M7 + 0.48]                        # jabbed twice more
RECOIL = lambda a, L=1.0, **f: GRIP(OPEN, bend={'neck': [0, 0, -a, L, None]}, face={'gx': 0.8, **f})   # the hero's head, knocked aside on its neck by the finger
NOSE7 = [9.0, 1.96, -0.86]                          # the corner of his face on the mayor's side
SHORT7 = [8.98, 1.94, -0.56]                        # the fingertip, stopped a hand short of it
FINGER = lambda pt, **kw: {'hands': {'R': 'point'}, 'reach': {'R': [*pt, 1, 0.08]}, **kw}   # the mayor's index, guided: his arm crosses the doorway
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'unimpressed', keys=[HOLDK(face={'gx': 0.9}), k(0.0, look=None), k(0.16, toon=GRIP(OPEN, face={'gx': 0.9, 'lid': 1}), toonDur=0.04), k(0.24, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.05),   # his eyes on the mayor who marches up; a blink
            k(M7 + 0.05, expr='surprised'), k(M7 + 0.05, toon=GRIP(OPEN, sq=[0.95, 1.07, 0.95], bend={'neck': [0, 0, -0.14, 1, None]}, face={'gx': 0.8, 'eye': 0.25}), toonDur=0.08, toonEase='outBack')] +   # the finger: he draws himself up, his head back from it
            [x for i, t_ in enumerate(JAB7) for x in (k(t_, toon=RECOIL(0.42 + 0.2 * i, 1.2 + 0.15 * i, lid=1), toonDur=0.04), k(t_ + 0.07, toon=RECOIL(-0.2 - 0.08 * i, 1.08, eye=0.3), toonDur=0.07),   # each jab lands: his head goes over on a neck that stretches, further the second time,
                                                               k(t_ + 0.15, toon=RECOIL(0.1, browL=0.7, browR=-0.3), toonDur=0.07))]),   # comes back past upright, and settles (his beard goes with it)
        act('maire', [9.05, 0, 1.6], 180, 'marchPomp', 'proud', keys=[k(0.0, to=MAYOR, dur=M7, clip='marchPomp', ease='linear', face=-125), k(M7, clip='point', expr='determined', blend=0.08, look=None),   # he is in the frame at the cut, marching; his face stays three quarters to us (a look at the man turned it away)
            k(M7, toon={'sq': [1.06, 0.92, 1.06]}, toonDur=0.05), k(M7 + 0.06, toon=FINGER(SHORT7, sq=[0.96, 1.06, 0.96], face={'gx': -0.9}), toonDur=0.1, toonEase='outBack')] +   # his eyes on him; the finger stops a hand short of his face
            [x for i, t_ in enumerate(JAB7) for x in (k(t_ - 0.05, toon=FINGER(NOSE7, bend={'spine': [0.13 + 0.03 * i, 0, 0, 1, None]}, face={'gx': -0.9, 'jaw': 0.3 * i, 'brow': -0.5}), toonDur=0.05, toonEase='in'), k(t_ + 0.1, toon=FINGER(SHORT7, face={'gx': -0.9}), toonDur=0.1))])],   # then it lands, twice
        props=[DOOR(swing=[[0, OPEN]]), BEARD(), WEB()],
        cams=[cam(0.0, [3.4, 1.7, -0.05], [3.6, 1.7, -0.1], [9.6, 1.65, -0.18], [9.6, 1.65, -0.18], lens=44)])
# 8: ...public service: a blue enamel plate slams over the bakery's sign; then close on him: a doorman's cap drops onto his head: he sinks under it, only
#    his eyes go up to it
P8 = 0.1                                            # the plate
T8 = 0.36                                           # the cut to him
C8 = T8 + 0.2                                       # the cap lands
UP8 = C8 + 0.24                                     # he comes back up
SUNK = [1.45, 0.55, 1.45]
CAPOFF = [0.0, 0.5, 0.0]
CAP = lambda **kw: P('cap', 'doormanCap', on={'actor': 'mec', 'joint': 'head', 'offset': CAPOFF, 'rot': [0, 0, 0]}, **kw)   # he wears it from now on
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'surprised', keys=[HOLDK(), k(0.0, look=None), k(P8 + 0.06, toon=GRIP(OPEN, face={'gy': -0.9, 'gx': 0.5}), toonDur=0.08),
            k(T8, toon=GRIP(OPEN, face={'gy': -1.0}), toonDur=0.08),
            k(C8, toon=GRIP(OPEN, sq=SUNK, face={'gy': 0.2, 'eye': 0.2}), toonDur=0.04), k(C8 + 0.08, toon=GRIP(OPEN, sq=SUNK, face={'gy': -1.0, 'eye': 0.3, 'brow': 0.8}), toonDur=0.12),   # sunk to half his height; his eyes climb to the cap
            k(UP8, toon=GRIP(OPEN, sq=[0.9, 1.14, 0.9], face={'gy': -1.0}), toonDur=0.08, toonEase='out'), k(UP8 + 0.09, toon=GRIP(OPEN, sq=[1.03, 0.97, 1.03], face={'gy': -0.6}), toonDur=0.07), k(UP8 + 0.1, expr='deadpan'), k(UP8 + 0.17, toon=GRIP(OPEN), toonDur=0.06)])],
        props=[DOOR(swing=[[0, OPEN]], signHide=[[T8, 9]]), BEARD(), WEB(),
               P('plate', 'signBoard', pos=[DX - 0.13, 0, DZ], ry=-90, scale=0.01, opts={'text': 'SERVICE PUBLIC', 'w': SIGNW + 0.06, 'h': 0.64, 'height': 2.64, 'posts': False, 'frame': '#F4F1E8', 'bg': '#2A4B9B', 'fg': '#F4F1E8'},
                 keys=[k(P8, scale=1.0, dur=0.1, ease='outBack'), k(P8 + 0.1, squash=[1.1, 0.82, 1.0], dur=0.3), k(T8, visible=False)]),   # (put away in the close shot: a corner of it stuck into the frame)
               P('cap', 'doormanCap', pos=[9.12, 3.0, -1.02], ry=-90, keys=[k(0.0, visible=False), k(C8 - 0.17, visible=True), k(C8 - 0.17, to=[9.12, 2.3, -1.02], dur=0.17, ease='in'), k(C8, attach='mec', joint='head', offset=CAPOFF, rot=[0, 0, 0]), k(C8, squash=[1.35, 0.5, 1.35], dur=0.35)])],   # it comes down through the top of the frame: four frames of it; the plate and the cap squash where they land (prop key `squash`)
        fx=[{'type': 'shake', 'at': P8 + 0.08, 'dur': 0.12, 'amount': 0.016}, {'type': 'shake', 'at': C8, 'dur': 0.1, 'amount': 0.014}],
        cams=[cam(0.0, [5.0, 1.95, 1.0], [5.1, 1.98, 0.98], [9.9, 2.62, 0.05], [9.9, 2.64, 0.05], lens=44),   # the sign and the door, a little from the right: the whole plate inside the frame (its left end was cut), he is just out of it, his arm comes in at the bottom
              cam(T8, [6.1, 2.2, -1.2], [6.12, 2.2, -1.2], [9.12, 1.75, -1.1], [9.12, 1.75, -1.1], lens=44),   # on him, with room over his head for the cap to come down
              glide([cam(C8, [6.15, 1.9, -1.2], [6.15, 1.9, -1.2], [9.12, 1.1, -1.1], [9.12, 1.1, -1.1], lens=44)], 0.1),   # the camera goes down with him: sunk, his cap and his eyes at mid-height (they sat in the caption band)
              glide([cam(UP8 - 0.02, [6.2, 2.2, -1.2], [6.22, 2.2, -1.2], [9.12, 1.6, -1.1], [9.12, 1.6, -1.1], lens=44)], 0.14)])   # and back up with him
# 9: and a public service does not close: he tries to slip away: he tiptoes toward us, his hand still on the handle, the arm paid out behind him like
#    elastic; at the end of it his feet spin on the spot; it takes him back: he is shot against the wall and the leaf swings round on him: pressed in the
#    door like a flower in a book, seen through the glass; the leaf comes back, he peels off the wall
GO9, RUN9, FAR9 = 0.1, 0.5, [8.9, 0, -3.4]
HOLD9 = 0.9                                         # his feet give up: he stands at the end of the arm, and looks at us                     # he goes; how far he gets: sideways along the shop front, across the frame: the arm is a clothes line from his shoulder to the handle (walking toward the camera hid the arm behind him)
SNAP9 = 1.1                                         # it takes him back
SAND = [9.85, 0, -1.02]                             # between the wall and the leaf
SWING9 = [[0, OPEN], [SNAP9 + 0.02, OPEN], [SNAP9 + 0.1, 166], [SNAP9 + 0.44, 166], [SNAP9 + 0.62, OPEN]]
FLAT9 = [1.9, 1.0, 0.09]                            # pressed: nearly twice his width, no thicker than the pane
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[HOLDK(face={'gx': -0.9}), k(0.0, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.07),   # a look each way, with the eyes only (the first one is on at the cut)
            k(GO9, to=FAR9, dur=RUN9, clip='sneak', ease='out', face='keep'), k(GO9, toon=GRIP(OPEN), toonDur=0.05), k(GO9, expr='determined'),
            k(GO9 + RUN9, clip='scramble', params={'dur': 0.5, 'expr': 'scared'}, blend=0.05), k(GO9 + RUN9, toon=GRIP(OPEN, bend={'spine': [0.35, 0, 0, 1, None]}), toonDur=0.1),   # at the end of the arm: his feet spin
            k(GO9 + RUN9 + 0.05, toon=GRIP(OPEN, bend={'spine': [0.35, 0, 0, 1, None]}, wave=RIP(0.06, 0)), toonDur=0.08), k(GO9 + RUN9 + 0.13, toon=GRIP(OPEN, bend={'spine': [0.4, 0, 0, 1, None]}, wave=RIP(0.08, 2.2)), toonDur=round(HOLD9 - GO9 - RUN9 - 0.15, 3)),   # and the arm, taut, hums like a string
            k(HOLD9, clip='stand', blend=0.06), k(HOLD9, look=[4.6, 1.6, -7.0], expr='scared'),   # held: five frames, his feet still, his eyes to us:
            k(HOLD9, toon=GRIP(OPEN, bend={'spine': [0.3, 0, 0, 1, None]}, wave=RIP(0.05, 3.6), face={'eye': 0.35, 'brow': 0.9}), toonDur=0.05), k(HOLD9 + 0.08, toon=GRIP(OPEN, bend={'spine': [0.3, 0, 0, 1, None]}, wave=RIP(0.03, 5.0), face={'eye': 0.35, 'brow': 0.9, 'gy': 0.2}), toonDur=0.08),   # he knows
            k(SNAP9, to=SAND, dur=0.09, glide=True, ease='in', face='keep'), k(SNAP9, clip='blownBack', expr='take', blend=0.02), k(SNAP9 + 0.02, toon=GRIP(166), toonDur=0.08),
            k(SNAP9 + 0.09, clip='pressGlass', expr='dizzy', blend=0.02), k(SNAP9 + 0.09, toon=GRIP(166, sq=FLAT9, scl={'handR': [1.6, 1.6, 1]}, hands={'L': 'grip', 'R': 'spread'}, face={'stars': 1, 'mouth': 'o', 'mouthW': 0.6}), toonDur=0.02),   # flat between the wall and the glass, a palm spread on it
            k(SNAP9 + 0.44, toon=GRIP(OPEN, sq=FLAT9, face={'stars': 1}), toonDur=0.18, toonEase='inOut'),   # the leaf comes back, his arm goes with it; he stays on the wall, as thin as a poster,
            k(SNAP9 + 0.54, clip='poster', params={'high': 0.1, 'slideAt': 9, 'slide': 0.0, 'peelK': 0, 'stars': 1}, expr='dizzy', blend=0.05)])],   # we leave him there, flat: the cut comes on the poster (the peel that followed, 0.2 s, read as a nod of the head)
        props=[DOOR(swing=SWING9, glass=0.14, signHide=[[SNAP9 - 0.02, 9]], **PUBLIC), BEARD(), WEB(keys=[k(GO9, visible=False)]), CAP()],   # (the sign put away for the close frame at the wall: its lower line stuck into the top corner)
        fx=[{'type': 'shake', 'at': SNAP9 + 0.09, 'dur': 0.18, 'amount': 0.03}],
        cams=[cam(0.0, [4.6, 1.6, -7.0], [4.65, 1.6, -6.9], [9.2, 0.95, -2.0], [9.2, 0.95, -2.0], lens=44),   # three quarters along the shop front, tilted down: his feet spin above the caption band
              glide([cam(SNAP9 - 0.02, [6.6, 1.5, -2.2], [6.65, 1.5, -2.18], [9.9, 1.42, -1.0], [9.9, 1.42, -1.0], lens=44)], 0.1)])   # back with him to the wall: his cap and the stars inside the frame   # the camera goes back with him to the wall, under the sign

# 10: his replacement is in the queue: far down it a man in the same cap leans out, his neck up over the heads, and waves his ticket; the camera runs
#     down the queue to him
REMP = [7.05, 0, 9.4]
N10 = 0.34                                          # his neck starts up
NECK = lambda L, bz=0.0, **kw: {'bend': {'neck': [0, bz, 0, L, 0.55], 'spine': [0, 0, -0.2, 1, None]}, **kw}
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('remp', REMP, 185, 'wave', 'happy', keys=[k(0.0, look=[8.6, 1.7, -1.0]), k(0.0, toon=NECK(1.0), toonDur=0.0),
            k(N10, toon=NECK(15.0, wave={'neck': [0.1, 1.0, 0.0, 1, 0]}, sq=[0.96, 1.06, 0.96]), toonDur=0.3, toonEase='outBack'), k(N10 + 0.3, expr='bigGrin'),   # up over the heads: three heads of neck
            k(N10 + 0.34, toon=NECK(13.5, 0.05, wave={'neck': [0.07, 1.0, 0.9, 1, 0]}), toonDur=0.16), k(N10 + 0.52, toon=NECK(14.2, -0.05, wave={'neck': [0.05, 1.0, 1.7, 1, 0]}), toonDur=0.18),   # it wobbles at the top
            k(N10 + 0.74, toon=NECK(14.0, 0.03, wave={'neck': [0.03, 1.0, 2.4, 1, 0]}), toonDur=0.2), k(N10 + 0.98, toon=NECK(14.0), toonDur=0.2)])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), QUEUE(), P('rcap', 'doormanCap', on={'actor': 'remp', 'joint': 'head', 'offset': CAPOFF, 'rot': [0, 0, 0]}),
               P('ticket', 'queueTicket', on={'actor': 'remp', 'hand': 'R', 'offset': [0, 0.02, 0.02], 'rot': [0, 3.1416, 0]}, scale=3.0, opts={'num': '2', 'sub': 'Porte'})],   # turned to us (its number read backwards)
        cams=[cam(0.0, [8.7, 1.6, -1.6], [8.68, 1.62, -1.4], [7.5, 1.5, 14.0], [7.5, 1.5, 14.0], lens=44),
              glide([cam(0.02, [8.0, 2.2, 4.8], [7.98, 2.2, 4.95], [7.1, 2.55, 9.4], [7.1, 2.55, 9.4], lens=44)], 0.36)])   # the run down the queue starts at the cut; it ends under him: his head high in the frame, his neck over the heads
# 11: in the evening he goes home: at night, seen through the pane of the open leaf, from the wall: his hand on the handle in the foreground, the arm
#     paid out from it down the pavement to him, who walks away with his shoulders down and waves good night without turning round; pigeons asleep on
#     the sleeve; warm pools under the lamps, a lit window or two
NIGHT = {**STREET, 'night': True}
W11 = [[8.95, -4.6], [8.9, -6.9]]                    # where he walks in this shot
NIGHTGRADE = dict(dark=[[0, 0.72, 0.001]], darkFloor=0.5, darkTint='#7A98F0')   # a night: half the light of the day, cold
NIGHT11 = dict(dark=[[0, 0.62, 0.001]], darkFloor=0.5, darkTint='#7A98F0')   # the street, a little lighter: he is a dark shape between two pools of lamp light
H11 = handle(OPEN)
D11 = st.dur('S11')
z11 = lambda t_: W11[0][1] + (W11[1][1] - W11[0][1]) * t_ / D11   # where he is at a time of the shot
def on_arm(f, t01):   # a point of the arm paid out behind him: f of the way from the handle to his shoulder, when he has walked t01 of his way
    sx, sz = W11[0][0] - 0.26 + (W11[1][0] - W11[0][0]) * t01, W11[0][1] + (W11[1][1] - W11[0][1]) * t01
    return [round(H11[0] + f * (sx - H11[0]), 3), round(H11[1] + f * (1.63 - H11[1]) + 0.035, 3), round(H11[2] + f * (sz - H11[2]), 3)]
PG11 = lambda i, f, ph: P(f'pg{i}', 'pigeon', pos=on_arm(f, 0), ry=-90, scale=1.0, opts={'ph': ph, 'sleep': True}, keys=[k(0.0, to=on_arm(f, 1), dur=D11, ease='linear')])   # it rides the arm as it pays out
SLOUCH = {'spine': [0.2, 0, 0, 1, None], 'neck': [0.28, 0, 0, 1, None]}   # the end of a day: shoulders down, head down
WAVE11 = lambda t_, x, y: GRIP(OPEN, bend=SLOUCH, hands={'L': 'grip', 'R': 'spread'}, reach={'L': [*handle(OPEN), 1, 0.05, [0.2, -1, 0.5]], 'R': [x, y, round(z11(t_) - 0.12, 3), 1, 0.1]})   # his other hand up over his shoulder, wherever he has got to
st.shot('S11', 'parisStreet', setOpts=NIGHT, lighting='night', actors=[act('mec', [W11[0][0], 0, W11[0][1]], 180, 'walk', 'deadpan', darkEyes=False, keys=[k(-0.05, toon=GRIP(OPEN, bend=SLOUCH), toonDur=0),
            k(0.0, to=[W11[1][0], 0, W11[1][1]], dur=D11, clip='walk', ease='linear'),
            k(0.34, toon=WAVE11(0.48, 9.32, 2.36), toonDur=0.14, toonEase='outBack'), k(0.52, toon=WAVE11(0.64, 9.02, 2.46), toonDur=0.12), k(0.68, toon=WAVE11(0.8, 9.34, 2.36), toonDur=0.12), k(0.84, toon=WAVE11(0.96, 9.04, 2.46), toonDur=0.12),   # good night: a real wave, twice each way, without turning round
            k(1.02, toon=GRIP(OPEN, bend=SLOUCH), toonDur=0.22)])],   # and the hand comes down
        props=[DOOR(swing=[[0, OPEN]], glass=0.03, inner=False, **PUBLIC), BEARD(), CAP(), PG11(1, 0.25, 0.3), PG11(2, 0.55, 1.7),
               P('lampA', 'streetLamp', pos=[7.75, 0, -2.6], inDark=True, opts={'on': True, 'light': 9, 'glow': False, 'pool': 1.9}), P('lampB', 'streetLamp', pos=[6.3, 0, -8.6], inDark=True, opts={'on': True, 'light': 9, 'glow': False, 'pool': 2.4}),   # (to the left of the leaf's upright: its post stood behind the arm and the lower pigeon)
               P('moon', 'moon', pos=[8.1, 1.2, -62.0], inDark=True, opts={'radius': 3.2})], **NIGHT11,   # a low moon at the end of the street: his raised hand is in front of it (navy on a navy sky, it was lost)   # warm pools on the pavement (no cone of light: it veiled him)
        cams=[cam(0.0, [9.5, 2.3, 2.6], [9.5, 2.3, 2.45], [8.85, 1.0, -4.0], [8.85, 1.0, -4.0], lens=44)])   # from the wall side, above head height, through the pane of the open leaf (cleared): the hand on the handle low in the frame, the arm running from it up the picture to him (from his own height it was hidden end-on behind the pigeons)
# 12: the arm stays: his bedroom at night, the window moonlit: he sleeps on his back, cap on, the arm across him and out through the window; somebody
#     uses the door: a ripple comes in along the arm, then it takes him off the bed: he ends on the wall under the window, horizontal as he lay, hanging
#     by the arm that goes out of it, his pillow behind his head, his blanket still on him; he does not wake up
WIN = [-4.7, 1.75, -0.6]                            # through the window
BED12 = [-2.6, 0.62, -1.7]                          # on the set's bed (2 m long along Z, the pillow toward -Z)
TUG = 0.5
ARM12 = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*WIN, 1, 0.05]}, **kw}
WALL12 = [-4.33, 0.16, -1.28]                       # where his hips end, against the wall: he lies along it under the window, his head to our left, his upper shoulder under the middle of the window
NIGHT12 = dict(dark=[[0, 0.6, 0.001]], darkFloor=0.55, darkTint='#7A98F0')   # the room: a little lighter than the street (the yank was lost in the dark)
ZZZ = lambda pos, at_, **kw: P('zzz' + kw.pop('n', ''), 'speechBubble', pos=pos, ry=90, scale=0.9, opts={'text': 'Zzz', 'w': 0.6, 'h': 0.32, 'tail': 'down', 'popAt': at_}, **kw)
st.shot('S12', 'chambre', setOpts={'poster': 'SERVICE\nPUBLIC', 'posterBg': '#2A4B9B', 'posterFg': '#F4F1E8', 'pane': '#86A4E6', 'paneGlow': '#5E7CC8'}, actors=[act('mec', BED12, 0, 'lieBack', 'sleepy', darkEyes=False, keys=[k(-0.05, toon=ARM12(face={'lid': 1}), toonDur=0), k(0.02, toon=ARM12(sq=[1.0, 1.0, 1.14], face={'jaw': 0.35, 'lid': 1}), toonDur=0.14, toonEase='inOut'), k(0.18, toon=ARM12(face={'lid': 1}), toonDur=0.12, toonEase='inOut'),   # a snore: the chest comes up, goes down (his lids are shut and do not shine: in a night that is only graded, the eyes that stay lit in the dark read as open)
            k(TUG - 0.3, toon=ARM12(wave=RIP(0.07, 1.5, 1.5), face={'lid': 1}), toonDur=0.05), k(TUG - 0.25, toon=ARM12(wave=RIP(0.1, 0.2, 1.5), face={'lid': 1}), toonDur=0.13),   # somebody uses the door: a ripple comes in through the window, along the arm, to him
            k(TUG - 0.12, toon=ARM12(sq=[1.03, 0.97, 1.03], wave=RIP(0.05, -0.4, 1.5), face={'lid': 1}), toonDur=0.1), k(TUG, to=WALL12, dur=0.1, glide=True, ease='in', face=90), k(TUG, toon=ARM12(sq=[0.85, 1.3, 0.85], face={'lid': 1}), toonDur=0.06),   # it takes him: three frames, stretched along the way
            k(TUG + 0.1, clip='wallBunk', expr='sleepy', blend=0.02), k(TUG + 0.1, toon=ARM12(sq=[1.3, 0.9, 0.22], face={'lid': 1}), toonDur=0.02),   # on the wall, flat, as he lay: horizontal, eyes shut
            k(TUG + 0.18, toon=ARM12(sq=[1.08, 1.0, 0.5], face={'lid': 1}), toonDur=0.12, toonEase='outBack'),
            k(TUG + 0.34, toon=ARM12(sq=[1.1, 1.02, 0.55], face={'jaw': 0.35, 'lid': 1}), toonDur=0.12, toonEase='inOut'), k(TUG + 0.48, toon=ARM12(sq=[1.08, 1.0, 0.5], face={'lid': 1}), toonDur=0.1)])],   # and he snores on
        props=[BEARD(), CAP(), ZZZ([-2.55, 1.5, -2.55], 0.0, keys=[k(TUG - 0.05, visible=False)]), ZZZ([-4.0, 1.6, 0.0], TUG + 0.3, n='2', keys=[k(0.0, visible=False), k(TUG + 0.3, visible=True)]),
               P('pillow', 'pillow', pos=[-2.6, 0.7, -2.62], rot=[0.25, 0, 0], inDark=True, keys=[k(TUG, attach='mec', joint='head', offset=[0.0, 0.26, -0.13], rot=[0, 0, 0])]),   # his pillow goes with him (it keeps its white in the night),
               P('moonwall', 'moonPatch', pos=[-4.47, 0.58, -1.1], ry=90, inDark=True, opts={'w': 2.9, 'h': 1.0, 'skew': 0.0, 'opacity': 0.3, 'bars': False})],   # a pale band of moonlight on the wall under the window, where he ends: he is a dark shape on it (a blanket hung from him made a dark block under him: he seemed to lie on a cupboard)
        fx=[{'type': 'shake', 'at': TUG + 0.1, 'dur': 0.15, 'amount': 0.025}], **NIGHT12,
        cams=[cam(0.0, [3.4, 1.9, -1.65], [3.3, 1.9, -1.65], [-4.4, 1.25, -1.65], [-4.4, 1.25, -1.65], lens=44),   # from the side of the room: he lies across the frame, the window over his feet
              glide([cam(TUG + 0.02, [2.4, 1.6, -1.0], [2.3, 1.6, -1.0], [-4.4, 1.25, -1.0], [-4.4, 1.25, -1.0], lens=44)], 0.12)])   # the camera goes to the wall with him: he fills the width of the frame, the window over him, the top of the frame free for the title card
# 13: the door is listed as a historic monument: a bronze plaque over him; a tourist comes for a selfie with him, as with the guards, and pokes his cheek:
#     his head rocks, his eyes go to the finger; nothing else moves
PLQ = 0.3                                           # the plaque: as the tourist arrives (on « monument » it had four frames before the cut to the two of them)
STOP13 = [9.0, 0, -2.6]                             # where he stops in the wide: a step short of him (beside him he stood over him)
BRONZE = lambda **kw: P('bronze', 'bronzePlaque', pos=[9.84, 2.62, -2.3], ry=-90, opts={'text': 'MONUMENT/HISTORIQUE', 'w': 1.3, 'h': 0.72}, **kw)   # over the heads
TOUR = [9.0, 0, -1.78]                              # beside him along the wall, shoulder to shoulder for the picture
CU13 = 1.04                                         # the cut to the two of them
SNAP13 = CU13 + 0.14                                # the picture is taken
POKES = [CU13 + 0.3, CU13 + 0.62]                    # a finger in his cheek, twice (three did not leave the head time to swing)
CHEEK = face_pt13 = [8.98, 2.0, -1.2]                # his cheek, on the tourist's side
PHONE13 = [8.5, 2.5, -2.1]                         # the phone, at arm's length: up and out on his far side (toward the camera, his arm filled the frame)
def rock(t_, i):   # his head under one poke: knocked over on its neck like a punch-bag (35 to 45 degrees), back past upright, a wobble that dies over eight frames; his eyes on the finger
    a = 0.62 + 0.16 * i; F = {'gx': -0.9, 'gy': 0.2}
    return [k(t_, toon=GRIP(OPEN, face=F, bend={'neck': [0, 0, a, 1.2, None]}), toonDur=0.04), k(t_ + 0.08, toon=GRIP(OPEN, face=F, bend={'neck': [0, 0, -0.55 * a, 1.08, None]}), toonDur=0.08),
            k(t_ + 0.16, toon=GRIP(OPEN, face=F, bend={'neck': [0, 0, 0.3 * a, 1.03, None]}), toonDur=0.07), k(t_ + 0.23, toon=GRIP(OPEN, face=F, bend={'neck': [0, 0, -0.12 * a, 1, None]}), toonDur=0.06), k(t_ + 0.29, toon=GRIP(OPEN, face=F), toonDur=0.05)]
TPOSE = lambda finger, **kw: {'hands': {'R': 'grip', 'L': 'point'}, 'reach': {'R': [PHONE13[0], PHONE13[1] - 0.08, PHONE13[2] - 0.03, 1, 0.05], 'L': finger}, 'bend': {'spine': [0, 0, -0.16, 1, None]}, **kw}
BACK13, IN13 = [8.9, 1.95, -1.52, 1, 0.16], [CHEEK[0], CHEEK[1], CHEEK[2] - 0.02, 1, 0.16]
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stiffStand', 'deadpan', keys=[HOLDK(), k(0.0, look=None), k(0.5, toon=GRIP(OPEN, face={'lid': 1}), toonDur=0.04), k(0.58, toon=GRIP(OPEN), toonDur=0.05), k(CU13 + 0.04, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.06)] +   # a blink; then his eyes on the man beside him
            [x for i, t_ in enumerate(POKES) for x in rock(t_, i)] + [k(POKES[1] + 0.36, toon=GRIP(OPEN, face={'gx': -0.9, 'gy': 0.2, 'browL': -0.4, 'browR': 0.6}), toonDur=0.06)]),
        act('t1', [8.6, 0, -5.2], 0, 'walk', 'happy', keys=[k(0.0, to=STOP13, dur=0.72, clip='walk', ease='out', face=-100), k(0.74, clip='stand', expr='bigGrin', blend=0.12, look=None), k(CU13, to=TOUR, dur=0.02, glide=True, ease='linear', face=-100),   # (at the cut he is shoulder to shoulder with him)
            k(0.84, toon=TPOSE(BACK13, sq=[1.05, 0.93, 1.05]), toonDur=0.12, toonEase='outBack'), k(SNAP13 + 0.06, toon=TPOSE(BACK13), toonDur=0.06)] +   # the phone up at arm's length, he leans in
            [x for t_ in POKES for x in (k(t_ - 0.05, toon=TPOSE(IN13), toonDur=0.05, toonEase='in'), k(t_ + 0.08, toon=TPOSE(BACK13), toonDur=0.08))] + [k(POKES[0] + 0.02, expr='laugh')])],   # and pokes: once, twice, three times
        props=[DOOR(swing=[[0, OPEN]], signHide=[[CU13, 9]], **PUBLIC), BEARD(1.6), CAP(), WEB(), BRONZE(scale=0.01, keys=[k(PLQ, scale=1.0, dur=0.12, ease='outBack'), k(PLQ + 0.12, squash=[1.1, 0.85, 1.0], dur=0.3), k(CU13, visible=False)]),   # (put away in the two-shot: it was cut by the frame behind them)
               P('phone', 'smartPhone', pos=[8.4, 1.2, -1.9], ry=60, scale=1.7, opts={'call': False, 'case': '#F2C230'}, keys=[k(0.0, visible=False), k(0.84, visible=True), k(0.84, to=PHONE13, dur=0.12, ease='outBack')]),
               P('pg', 'pigeon', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.62, 0.0], 'rot': [0, 1.5708, 0]}, scale=1.1, opts={'ph': 0.5, 'flaps': [[t_ + 0.02, t_ + 0.3] for t_ in POKES]})],   # it beats its wings at each poke, to stay on
        fx=[{'type': 'shake', 'at': PLQ + 0.1, 'dur': 0.1, 'amount': 0.012}, {'type': 'flash', 'at': SNAP13, 'dur': 0.12}],
        cams=[cam(0.0, [4.6, 1.8, -7.0], [4.7, 1.8, -6.85], [9.2, 1.65, -2.0], [9.2, 1.65, -2.0], lens=44),   # three quarters along the shop front, as when he tried to leave
              cam(CU13, [5.0, 1.85, -1.55], [5.1, 1.85, -1.53], [9.05, 1.8, -1.45], [9.05, 1.8, -1.45], lens=44)])   # the two of them from the hips, both heads whole (his was cut by the right edge), the pigeon and the phone inside the frame
# 14: the arm too: close on him and his arm: a small plaque is screwed on the sleeve; the pigeon comes down from his cap to sit by it
LAND14 = 0.64
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stiffStand', 'deadpan', keys=[HOLDK(), k(0.0, look=None), k(0.18, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.7}), toonDur=0.08), k(LAND14 + 0.08, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.5, 'lid': 1}), toonDur=0.04),
            k(LAND14 + 0.16, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.5}), toonDur=0.05), k(0.8, toon=GRIP(OPEN, face={'browL': 0.6, 'browR': -0.4}), toonDur=0.1)])],   # his eyes go down to the plaque; a blink when the pigeon lands; then to us
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(1.6), CAP(),   # (no cobweb in this shot: plaque, pigeon, handle and web made one tangle)
               P('bronze2', 'bronzePlaque', pos=[8.88, 1.19, -0.55], ry=-90, scale=0.01, opts={'text': 'BRAS/CLASSÉ', 'w': 0.46, 'h': 0.27}, keys=[k(0.1, scale=1.0, dur=0.1, ease='outBack'), k(0.2, squash=[1.15, 0.85, 1.0], dur=0.25)]),   # on the forearm, on our side of the sleeve (half of it was behind the sleeve), and larger
               P('pg', 'pigeon', pos=[8.95, 2.75, -0.5], ry=180, scale=1.15, opts={'ph': 0.5, 'flap': [0.0, LAND14 + 0.04]}, keys=[k(0.0, visible=False), k(0.36, visible=True), k(0.38, to=[9.07, 1.6, -0.8], dur=round(LAND14 - 0.38, 3), ease='out', arc=0.25), k(LAND14, squash=[1.2, 0.8, 1.2], dur=0.25)])],   # in profile, down onto his upper arm, beside the plaque: half a second after it
        fx=[{'type': 'shake', 'at': 0.16, 'dur': 0.08, 'amount': 0.01}],
        cams=[cam(0.0, [6.6, 2.2, -1.35], [6.7, 2.2, -1.33], [9.1, 1.55, -0.8], [9.1, 1.55, -0.8], lens=44)])   # from a little above and from his side: the forearm stands against the lit doorway
# 15: yesterday a technician came by: he sets his toolbox down by the other jamb, finds a box on the wall: one big button, AUTO: he presses it
T15 = round(st.dur('S15') - 0.3, 3)                 # he presses
TECH = [9.2, 0, 1.6]
SW = [9.88, 1.4, 2.15]                              # the box on the wall, right of the door
TOOL15 = [8.92, 1.42, 1.3, 1, 0.1, [0.2, -1, -0.4]]   # his right hand, with the screwdriver, held up at his side
HOLD15 = lambda **kw: {'hands': {'R': 'grip'}, 'reach': {'R': TOOL15}, **kw}
PRESS = lambda dx, **kw: {'hands': {'L': 'point', 'R': 'grip'}, 'reach': {'L': [SW[0] - dx, SW[1] - 0.05, SW[2], 1, 0.16, [0.3, -1, -0.2]], 'R': TOOL15}, **kw}   # his left index on the button, the arm out behind him (his face stays on us: a look at the box showed the back of his head)
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('tech', [9.0, 0, 2.95], 180, 'walk', 'neutral', keys=[k(0.0, to=TECH, dur=0.66, clip='walk', ease='out', face=-78), k(0.7, clip='stand', blend=0.1, look=None, expr='hmm'), k(0.0, toon=HOLD15(), toonDur=0.0),
            k(0.72, toon=HOLD15(face={'gx': -0.8, 'gy': -0.5}), toonDur=0.1), k(1.02, toon=HOLD15(face={'gx': 0.95, 'eye': 0.25}, sq=[0.97, 1.05, 0.97]), toonDur=0.07, toonEase='outBack'), k(1.02, expr='surprised'),   # the door, then the box that pops up behind him: with his eyes alone
            k(T15 - 0.34, expr='smug'), k(T15 - 0.34, toon=PRESS(0.32, face={'browL': 0.9, 'browR': -0.3}), toonDur=0.22, toonEase='out'),   # the arm goes back to it, one brow up: he knows
            k(T15 - 0.04, toon=PRESS(0.07, face={'browL': 0.9, 'browR': -0.3}), toonDur=0.04), k(T15 + 0.06, toon=PRESS(0.09, face={'browL': 0.9, 'lidR': 1, 'mouth': 'smirk'}), toonDur=0.06)])],   # pressed, without a look; a wink at us
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), P('box', 'toolbox', pos=[8.8, 0, 2.5], ry=-70), P('switch', 'wallSwitch', pos=SW, ry=-90, scale=0.01, opts={'at': T15, 'label': 'AUTO'}, keys=[k(0.95, scale=1.7, dur=0.12, ease='outBack')]),
               P('tool', 'screwdriver', on={'actor': 'tech', 'hand': 'R', 'offset': [0, 0.02, 0.03], 'rot': [0, 0, 0]}, scale=1.5),   # a screwdriver in his free hand,
               P('patch', 'chestPatch', on={'actor': 'tech', 'joint': 'torso', 'offset': [0.085, 0.46, 0.125], 'rot': [0, 0, 0]}, opts={'text': 'MAINTENANCE', 'w': 0.2, 'h': 0.062})],   # his trade on his chest
        cams=[cam(0.0, [6.1, 1.6, 2.55], [6.22, 1.6, 2.5], [9.8, 1.62, 1.95], [9.8, 1.62, 1.95], lens=44)])   # right of the door: its sign stays out of the frame; his helmet a fifth of the way down (it touched the top edge)
# 16: it was automatic: the leaf leaves his hand: it shuts by itself, slides open; his hand stays in the air, holding nothing; he lifts the fist. Close on
#     him, the fist already up under his eyes: he looks at it, at the door (a small turn of the head), at the fist: a squash, and the take, not the one of
#     S03: he shoots up off his heels, his cap stays in the air; his hand opens and his jaw runs down into the palm; the cap comes back down on his head
SHUT16 = 0.18                                        # the leaf has swung shut
SLIDE16 = [[0, 0], [0.2, 0], [0.34, 0.95], [0.6, 0.95], [0.74, 0], [0.9, 0], [1.04, 0.95]]
AIR = handle(OPEN)                                  # where the handle was: his hand stays there
FREE = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*AIR, 1, 0.05, [0.2, -1, 0.5]]}, **kw}
CU16 = 0.3                                          # the cut to his face
HAND16 = [8.82, 1.55, -0.72]                        # the empty fist, lifted in front of his chest, under his eyes (where the handle was, it sat in the caption band)
PALM16 = [8.86, 1.5, -0.98]                         # the open palm, under his chin: where his jaw lands
LIFT = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*HAND16, 1, 0.05, [0.2, -1, 0.5]]}, **kw}
CATCH = lambda **kw: {'hands': {'L': 'open'}, 'reach': {'L': [*PALM16, 1, 0.05, [0.2, -1, 0.5]]}, **kw}
TAKE16 = CU16 + 0.5
JAW16 = TAKE16 + 0.09                               # he is back on his heels: the jaw goes down into the palm
LAND16 = TAKE16 + 0.22                              # the cap comes back down on his head
WIDE16 = {'eye': 0.75, 'brow': 1.0}                 # his eyes as big as they go, on his face this time (no stalks)
JAWB16 = [0.0, -0.24, 0.14]                         # the beard, under the chin that has run down
CAM16 = [6.8, 1.8, 0.0]                             # the close camera, nearly in front of him: his face is three quarters to it before the take, full at it
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[k(-0.05, toon=FREE(), toonDur=0), k(0.0, look=None), k(0.06, toon=FREE(face={'gx': 0.9, 'gy': 0.3}), toonDur=0.06), k(0.1, expr='surprised'),   # his eyes alone go after the leaf
            k(CU16 - 0.1, toon=LIFT(face={'gx': 0.3, 'gy': 0.9}), toonDur=0.1, toonEase='outBack'),   # the fist comes up before the cut: he looks at what it holds: five frames
            k(CU16 + 0.17, toon=LIFT(bend={'neck': [0, 0.3, 0, 1, None]}, face={'gx': 1.0, 'gy': -0.1, 'browL': 0.7}), toonDur=0.06),   # the door, beside him: his eyes, and his head a little: five frames
            k(CU16 + 0.34, toon=LIFT(face={'gx': 0.3, 'gy': 0.9, 'brow': 0.4}), toonDur=0.06),   # the fist again: four frames
            k(TAKE16 - 0.07, toon=LIFT(sq=[1.12, 0.82, 1.12], scl={'head': [1.14, 0.84, 1]}, face={'lid': 1}), toonDur=0.05),   # a squash: he winds up
            k(TAKE16 - 0.02, expr='shocked', look=CAM16), k(TAKE16, toon=CATCH(sq=[0.86, 1.2, 0.86], bend={'neck': [0, 0, 0, 1.25, None]}, face={**WIDE16, 'jaw': 0.35}), toonDur=0.05, toonEase='outBack'),   # the take: up off his heels, his head to us, the hand opens
            k(JAW16, toon=CATCH(sq=[1.05, 0.95, 1.05], face={**WIDE16, 'jaw': 1.0, 'jawLen': 0.5, 'tongue': 0.6}), toonDur=0.07, toonEase='in'),   # back down: the jaw runs down into the palm
            k(LAND16, toon=CATCH(sq=[1.1, 0.9, 1.1], scl={'head': [1.08, 0.9, 1]}, face={**WIDE16, 'jaw': 1.0, 'jawLen': 0.5, 'tongue': 0.6, 'lid': 0.5}), toonDur=0.03),   # the cap lands: his head gives under it
            k(LAND16 + 0.08, toon=CATCH(face={**WIDE16, 'jaw': 1.0, 'jawLen': 0.5, 'tongue': 0.6}), toonDur=0.08, toonEase='outBack')])],
        props=[DOOR(swing=[[0, OPEN], [0.03, OPEN], [SHUT16, 0]], slide=SLIDE16, led=0.2, signHide=[[CU16, 9]], **PUBLIC), BEARD(1.25, keys=[k(JAW16, attach='mec', joint='head', offset=JAWB16, rot=[0, 0, 0])]),
               CAP(keys=[k(TAKE16 + 0.04, visible=False), k(LAND16, visible=True), k(LAND16, squash=[1.35, 0.5, 1.35], dur=0.3)]),   # his cap: it stays up there when he comes back down,
               P('capfly', 'doormanCap', pos=[9.1, 2.98, -1.0], ry=-66, keys=[k(0.0, visible=False), k(TAKE16 + 0.04, visible=True), k(LAND16 - 0.07, to=[9.1, 2.32, -1.0], dur=0.07, ease='in'), k(LAND16, visible=False)]),   # four frames in the air, then down
               BRONZE(keys=[k(CU16, visible=False)])],   # the bronze plaque would sit behind his cap in the close shot: put away
        fx=[{'type': 'shake', 'at': LAND16, 'dur': 0.1, 'amount': 0.012}],
        cams=[cam(0.0, [5.2, 1.7, -2.6], [5.3, 1.7, -2.5], [9.6, 1.55, -0.5], [9.6, 1.55, -0.5], lens=44),
              cam(CU16, CAM16, [6.9, 1.8, -0.03], [9.02, 1.66, -0.9], [9.02, 1.66, -0.9], lens=44),   # nearly in front of him: the dark window behind his head, no sign in the frame, the fist under his chin
              glide([cam(TAKE16 - 0.03, [6.2, 1.9, 0.15], [6.15, 1.9, 0.17], [9.02, 2.0, -0.9], [9.02, 2.0, -0.9], lens=44)], 0.07)])   # back and up with him at the take: the cap in the air stays inside the frame
# 17: the lady never said thank you: he shuts his jaw with the palm that caught it, his hand goes back to where the handle was; the door slides open for
#     her: she comes out with her bread, goes by under his nose and away; once she is past he raises a finger, his mouth opens; nothing; it shuts, the
#     finger wilts. Then, closer, his arm: he turns to it, lays his other hand on the forearm (held), pushes it down, out at his side over the pale door:
#     it bows like a springboard and trembles; he lets go; it stays; a sigh, eyes shut. His fingers twitch; one eye opens; it comes back up by itself,
#     past where the handle was; the door opens for nobody. A look at it, a look at us
OUT17 = 0.25                                        # she comes out
LADY17 = [(10.5, 0.0), (8.6, 0.05), (8.2, -1.6), (7.9, -6.5)]
F17 = 1.42                                          # the finger
PUSH = 2.2                                          # his other hand lands on the forearm
DOWN17 = PUSH + 0.24                                # after four frames of contact, it pushes
REL = PUSH + 0.54                                   # he lets go
TW17 = REL + 0.32                                   # the fingers twitch
RISE = TW17 + 0.16                                  # it comes back up
US17 = RISE + 0.26                                  # the look at us
LOW17 = [9.02, 0.72, -0.45]                         # the hand, pushed straight down: still out at his side, over the pale door
POLE = [0.2, -1, 0.5]
ONARM = lambda y: [9.0, round(y + 0.13, 3), -0.5, 1, 0.08, [-1, 0.3, -0.6]]   # his other hand, flat on the forearm, its elbow out toward us: a gap between that arm and his chest
EYE17 = {'gx': 0.9, 'gy': 0.5}                       # his eyes on the arm
CAMB17 = [6.4, 1.5, -1.6]                           # the closer camera, on his right: the forearm and the hand on it stand against the pale leaf
FING = lambda y, z, hand='point', **kw: FREE(hands={'L': 'grip', 'R': hand}, reach={'L': [*AIR, 1, 0.05, POLE], 'R': [8.75, y, z, 1, 0.16]}, **kw)
DOWNARM = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE]}, **kw}
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'surprised', keys=[k(-0.05, toon=CATCH(face={**WIDE16, 'jaw': 1.0, 'jawLen': 0.5, 'tongue': 0.6}), toonDur=0), k(-0.05, look=CAM16),   # still in the take: his jaw in his palm
            k(0.02, toon={'hands': {'L': 'open'}, 'reach': {'L': [PALM16[0], PALM16[1] + 0.25, PALM16[2], 1, 0.05, POLE]}, 'face': {'eye': 0.3}}, toonDur=0.08, toonEase='in'),   # the palm shuts it
            k(0.14, toon=FREE(sq=[1.03, 0.96, 1.03]), toonDur=0.16, toonEase='outBack'), k(0.2, look=None), k(0.3, look='dame'),   # and the hand goes back to where the handle was, while the door opens
            k(F17, toon=FING(2.55, -1.3, sq=[0.96, 1.07, 0.96], face={'jaw': 0.6, 'brow': 0.7}), toonDur=0.12, toonEase='outBack'), k(F17, look=[8.0, 1.6, -5.0]),   # she is past: a finger, high, over the awning's stripes; his mouth open
            k(F17 + 0.28, toon=FING(2.52, -1.3, face={'brow': 0.3}), toonDur=0.05),   # nothing: it shuts
            k(F17 + 0.34, toon=FING(2.22, -1.27, 'rest', bend={'spine': [0.06, 0, 0, 0.99, None]}, face={'brow': -0.2, 'lid': 0.4}), toonDur=0.12, toonEase='inOut'),   # the finger wilts: it curls, the hand sinks,
            k(F17 + 0.46, toon=FING(1.72, -1.2, 'rest', bend={'spine': [0.1, 0, 0, 0.97, None], 'neck': [0.16, 0, 0, 1, None]}, face={'brow': -0.3, 'lid': 0.5}), toonDur=0.12, toonEase='inOut'),   # his shoulders with it
            k(F17 + 0.58, toon=FREE(bend={'spine': [0.08, 0, 0, 0.98, None]}), toonDur=0.1), k(F17 + 0.58, expr='sad', look=None),
            k(PUSH - 0.14, to=HOLD, dur=0.12, glide=True, ease='inOut', face=-62), k(PUSH - 0.1, toon=FREE(face=EYE17), toonDur=0.06), k(PUSH - 0.1, expr='hmm'),   # he turns to his arm; his eyes on it
            k(PUSH, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*AIR, 1, 0.05, POLE], 'R': ONARM(AIR[1])}, 'face': EYE17}, toonDur=0.1, toonEase='out'),   # the other hand, across, onto the forearm: four frames of contact
            k(DOWN17, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE], 'R': ONARM(LOW17[1])}, 'bend': {'spine': [0.12, 0, -0.14, 1, None], 'foreL': [0.4, 0, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {**EYE17, 'browTilt': -10, 'mouth': 'grimace'}}, toonDur=0.16, toonEase='inOut'),   # down: the forearm bows like a springboard
            k(DOWN17 + 0.18, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE], 'R': ONARM(LOW17[1])}, 'bend': {'spine': [0.14, 0, -0.14, 1, None], 'foreL': [0.5, 0, 0, 1, None]}, 'wave': RIP(0.035, 1.2, 1), 'sq': [1.04, 0.95, 1.04], 'face': {**EYE17, 'browTilt': -10, 'mouth': 'grimace'}}, toonDur=0.1),   # it pushes back: held, trembling
            k(REL, toon=DOWNARM(face=EYE17), toonDur=0.08), k(REL + 0.06, expr='relieved', look=None),   # he lets go: it stays down
            k(REL + 0.08, toon=DOWNARM(sq=[1.03, 0.96, 1.03], bend={'spine': [0.05, 0, 0, 0.97, None]}, face={'lid': 1, 'mouth': 'smile'}), toonDur=0.14),   # a sigh, eyes shut: eight frames
            k(TW17, toon={'hands': {'L': 'spread'}, 'reach': {'L': [LOW17[0], LOW17[1] + 0.05, LOW17[2], 1, 0.05, POLE]}, 'face': {'lid': 1, 'mouth': 'smile'}}, toonDur=0.03), k(TW17 + 0.04, toon=DOWNARM(face={'lidR': 1, **EYE17, 'browL': 0.6}), toonDur=0.03),   # the fingers twitch: one eye opens, on the arm
            k(TW17 + 0.08, toon={'hands': {'L': 'spread'}, 'reach': {'L': [LOW17[0], LOW17[1] + 0.08, LOW17[2], 1, 0.05, POLE]}, 'wave': RIP(0.03, 0.4, 1), 'face': {'lidR': 1, **EYE17, 'browL': 0.8}}, toonDur=0.03), k(TW17 + 0.12, toon=DOWNARM(face={**EYE17, 'eye': 0.25, 'brow': 0.6}), toonDur=0.03), k(TW17 + 0.12, expr='surprised'),   # again: both eyes
            k(RISE, toon=FREE(reach={'L': [AIR[0], AIR[1] + 0.2, AIR[2], 1, 0.05, POLE]}, wave=RIP(0.1, 0.6, 1.5), sq=[0.96, 1.06, 0.96], face={**EYE17, 'eye': 0.25}), toonDur=0.07, toonEase='out'),   # it comes back up, past where the handle was
            k(RISE + 0.09, toon=FREE(wave=RIP(0.05, 1.5, 1.5), face={'gx': 0.9, 'gy': 0.3}), toonDur=0.08), k(RISE + 0.2, toon=FREE(face={'gx': 0.9, 'gy': 0.3}), toonDur=0.06),
            k(US17, expr='deadpan', look=[7.0, 1.6, -1.45]), k(US17, toon=FREE(), toonDur=0.08)]),   # and at us: held to the end
        act('dame', [LADY17[0][0], 0, LADY17[0][1]], -90, 'walk', 'smug', keys=[k(0.0, visible=False), k(OUT17, visible=True), k(OUT17, to=[LADY17[1][0], 0, LADY17[1][1]], dur=0.55, clip='walk', ease='linear'),
            k(OUT17 + 0.55, to=[LADY17[2][0], 0, LADY17[2][1]], dur=0.5, clip='walk', ease='linear'), k(OUT17 + 1.05, to=[LADY17[3][0], 0, LADY17[3][1]], dur=1.5, clip='walk', ease='linear')])],
        props=[DOOR(swing=[[0, 0]], slide=[[0, 0], [0.05, 0], [0.22, 0.95], [1.0, 0.95], [1.2, 0], [RISE + 0.04, 0], [RISE + 0.2, 0.95]], led=0.0, signHide=[[PUSH - 0.14, 9]], **PUBLIC),
               P('beard', 'beard', on={'actor': 'mec', 'joint': 'head', 'offset': JAWB16, 'rot': [0, 0, 0]}, scale=1.25, opts={'color': '#17161A'}, keys=[k(0.08, attach='mec', joint='head', offset=[0.0, 0.03, 0.09], rot=[0, 0, 0])]),   # (it comes back up with his jaw)
               CAP(), BRONZE(keys=[k(PUSH - 0.14, visible=False)]),
               P('bread', 'baguette', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0.1, 0], 'rot': [0, 0, 1.3]}, keys=[k(0.0, visible=False), k(OUT17, visible=True)])],
        cams=[cam(0.0, [4.75, 1.65, -1.85], [4.95, 1.65, -1.75], [9.5, 1.45, -0.45], [9.5, 1.45, -0.45], lens=44),   # a little to the right: the bronze plaque stays out of the left edge
              cam(PUSH - 0.14, CAMB17, [6.5, 1.5, -1.55], [9.05, 1.25, -0.7], [9.05, 1.25, -0.7], lens=44),   # closer for his arm: from his right, the forearm over the pale leaf (the shot was one wide of 3.7 s)
              glide([cam(US17 - 0.08, [6.9, 1.6, -1.45], [7.0, 1.6, -1.42], [9.05, 1.5, -0.78], [9.05, 1.5, -0.78], lens=44)], 0.3)])   # and in for the last look

# sound on the actions
st.cue('sfx:squeak', 'S01', O1, 0.3)
for t_ in B2: st.cue('whoosh', 'S02', t_, 0.35, 0.2, 500, 3500); st.cue('pop', 'S02', t_ + 0.12, 0.25)
st.cue('sfx:gasp', 'S03', T3 + 0.06, 0.35)
for i_, t_ in enumerate(R5): st.cue('whoosh', 'S05', t_, 0.25, 0.18, 500, 3500); st.cue('sfx:tick', 'S05', t_ + 0.06, 0.22 + 0.02 * i_)
st.cue('pop', 'S06', 0.02, 0.3); st.cue('sfx:slideUp', 'S06', 0.12, 0.3)
st.cue('sfx:stepHeavy', 'S07', 0.08, 0.3); st.cue('sfx:stepHeavy', 'S07', 0.28, 0.3); st.cue('pop', 'S07', M7 + 0.06, 0.3)
for t_ in JAB7: st.cue('pop', 'S07', t_, 0.22)
st.cue('clack', 'S08', P8 + 0.08, 0.45); st.cue('thud', 'S08', C8, 0.4); st.cue('sfx:boing', 'S08', UP8, 0.35)
st.cue('sfx:stretch', 'S09', GO9, 0.35); st.cue('sfx:zip', 'S09', SNAP9, 0.4); st.cue('sfx:splat', 'S09', SNAP9 + 0.09, 0.5); st.cue('sfx:squeak', 'S09', SNAP9 + 0.5, 0.3)
st.cue('whoosh', 'S10', 0.02, 0.3, 0.3, 400, 3000); st.cue('sfx:slideUp', 'S10', N10, 0.4); st.cue('sfx:boing', 'S10', N10 + 0.3, 0.3)
st.cue('sfx:stretch', 'S12', TUG - 0.1, 0.3); st.cue('sfx:zip', 'S12', TUG, 0.35); st.cue('thud', 'S12', TUG + 0.1, 0.5)
st.cue('clack', 'S13', PLQ + 0.1, 0.4); st.cue('sfx:click', 'S13', SNAP13, 0.45)
for t_ in POKES: st.cue('pop', 'S13', t_, 0.3)
st.cue('clack', 'S14', 0.16, 0.35); st.cue('sfx:poof', 'S14', LAND14, 0.25)
st.cue('sfx:tick', 'S15', T15, 0.45)
st.cue('sfx:slideUp', 'S16', 0.2, 0.3); st.cue('sfx:slideUp', 'S16', 0.6, 0.2); st.cue('sfx:boing', 'S16', TAKE16, 0.4); st.cue('sfx:slideDown', 'S16', JAW16, 0.3); st.cue('thud', 'S16', LAND16, 0.35)
st.cue('clack', 'S17', 0.1, 0.35); st.cue('sfx:slideUp', 'S17', 0.05, 0.3); st.cue('sfx:slideDownSlow', 'S17', F17 + 0.34, 0.25); st.cue('sfx:stretch', 'S17', DOWN17, 0.3); st.cue('sfx:squeak', 'S17', DOWN17 + 0.18, 0.25)
st.cue('sfx:tick', 'S17', TW17, 0.3); st.cue('sfx:tick', 'S17', TW17 + 0.08, 0.3); st.cue('sfx:spring', 'S17', RISE, 0.5); st.cue('sfx:slideUp', 'S17', RISE + 0.05, 0.3)

st.card('S12', 'LE BRAS RESTE')
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("La porte", rig='toon', fingers=True, cloth=True, idleShift=1.8, limbSmear=1, extra_cast={
    'dame': CITIZEN('mamie', 51, suit='#8A3A5A', glasses=False), 'agent': CITIZEN('officiel', 53, suit='#6E7A86', tie='#2F6E5C'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'remp': CITIZEN('lemec_brown', 71), 't1': CITIZEN('tourist', 73), 'tech': CITIZEN('worker', 77, glasses=False, suit='#3F74B8', cuff='#3F74B8', pants='#2C4F85', lapel='#3F74B8', hat='hardhat2', hatColor='#F2C230', bandColor='#D8F03C', bandH=0.05),   # a maintenance man: blue work jacket with two hi-vis bands, a yellow site helmet with a ridge and a front lip (the white one with a brim was a panama, the lapelled jacket a suit)
    **{f'r{i}': CITIZEN(['femme', 'proviseur', 'lyceen', 'madame', 'sportif', 'tourist', 'fermier', 'lyceenne'][i], 60 + i) for i in range(8)}})
