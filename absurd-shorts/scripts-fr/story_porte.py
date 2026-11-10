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
PUBLIC = {'sign': 'SERVICE PUBLIC', 'signBg': '#2A4B9B', 'signFg': '#F4F1E8'}   # the bakery's sign once it is a public service
HOLD = [9.12, 0, -1.02]                             # where he stands to hold it: beside the open leaf, facing the road
GRIP = lambda deg, w=1, **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*handle(deg), w, 0.05, [0.2, -1, 0.5]]}, **kw}

# 1: he reaches the bakery door, sees a lady coming, pulls it open with a bow; she walks in without a look
O1 = 0.42                                           # the door starts to open
LADY = [(7.4, 4.6), (8.3, 0.25), (10.6, 0.0)]       # her way: along the pavement, then in
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [9.05, 0, 0.55], -90, 'stand', 'neutral', keys=[k(0.0, toon=GRIP(0), toonDur=0), k(0.0, look=[9.0, 1.2, 0.5]), k(0.14, look='dame', expr='surprised'),
            k(0.3, expr='happy'), k(O1, to=HOLD, dur=0.24, glide=True, ease='inOut', face=-90), k(O1, toon=GRIP(OPEN, sq=[1.03, 0.96, 1.03]), toonDur=0.24, toonEase='inOut'),
            k(O1 + 0.3, toon=GRIP(OPEN, bend={'spine': [0.5, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}), toonDur=0.16, toonEase='outBack'), k(O1 + 0.3, look=[7.8, 0.6, 0.3], expr='proud'),   # a bow
            k(1.35, toon=GRIP(OPEN), toonDur=0.2), k(1.35, look='dame')]),
        act('dame', [LADY[0][0], 0, LADY[0][1]], 180, 'walk', 'smug', keys=[k(0.0, to=[LADY[1][0], 0, LADY[1][1]], dur=1.05, clip='walk', ease='linear'), k(1.05, to=[LADY[2][0], 0, LADY[2][1]], dur=0.55, clip='walk', ease='linear'),
            k(1.5, visible=False)])],
        props=[DOOR(swing=[[0, 0], [O1, 0], [O1 + 0.24, OPEN]])],
        cams=[cam(0.0, [3.7, 1.7, 0.6], [3.9, 1.7, 0.5], [9.9, 1.5, -0.35], [9.9, 1.5, -0.35], lens=44)])

# 2: he is still holding it: people shoot through the doorway one after the other; at each one his beard grows a notch; a cobweb between his arm and the leaf
HOLDK = lambda **kw: k(-0.05, toon=GRIP(OPEN, **kw), toonDur=0)
def rusher(i, t0, z0=0.25, x0=5.2):                    # somebody who dashes into the bakery
    return act(f'r{i}', [x0, 0, z0], 90, 'stand', 'neutral', keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, to=[DX + 0.6, 0, 0.0], dur=0.2, clip='dashOff', ease='linear', blend=0.01), k(t0 + 0.19, visible=False)])
BEARD = lambda sc=1.25, **kw: P('beard', 'beard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.03, 0.09], 'rot': [0, 0, 0]}, scale=sc, opts={'color': '#17161A'}, **kw)   # it stays from now on
WEB = lambda **kw: P('web', 'spiderWeb', pos=[9.02, 1.42, -0.7], ry=-90, opts={'r': 0.3}, **kw)
B2 = [0.12, 0.42, 0.72]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(0.0, look=[5.5, 1.6, 0.3]), k(B2[0] + 0.1, look=[9.9, 1.6, 0.0]), k(B2[1], look=[5.5, 1.6, 0.3], expr='unimpressed'), k(B2[1] + 0.1, look=[9.9, 1.6, 0.0]),
            k(B2[2], look=[5.5, 1.6, 0.3]), k(B2[2] + 0.1, look=[9.9, 1.6, 0.0]), k(0.9, look=None, expr='deadpan')])] + [rusher(i, t) for i, t in enumerate(B2)],
        props=[DOOR(swing=[[0, OPEN]]), BEARD(0.01, keys=[k(B2[0] + 0.12, scale=0.5, dur=0.1, ease='outBack'), k(B2[1] + 0.12, scale=0.85, dur=0.1, ease='outBack'), k(B2[2] + 0.12, scale=1.25, dur=0.1, ease='outBack')]),
               WEB(scale=0.01, keys=[k(B2[2] + 0.05, scale=1.0, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [6.5, 1.5, -0.45], [6.65, 1.5, -0.5], [9.3, 1.38, -0.8], [9.3, 1.38, -0.8], lens=44)])   # close: the sign above the door stays out of the frame (it was cut in two)
# 3: behind her there was... first what he sees: the queue, down the pavement, out of sight; then his face, to us: eyes out, the jaw on his tie
QUEUE = lambda **kw: P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[7.7, 1.6], [7.5, 190.0]], 'gap': 0.8, 'people': True, 'seed': 9, **kw})
T3 = 0.56                                           # the cut to his face
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(-0.3, look=[7.6, 1.6, 12.0]), k(T3 + 0.06, look=None, expr='take'),
            k(T3 + 0.06, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.9, 'popLen': 0.14}, sq=[0.92, 1.14, 0.92]), toonDur=0.07, toonEase='outBack'), k(T3 + 0.4, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.9, 'popLen': 0.14}), toonDur=0.1)])],
        props=[DOOR(swing=[[0, OPEN]]), QUEUE(), BEARD(), WEB()],
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
            [x for i, t in enumerate(R5) for x in (k(max(0.0, t - 0.05), look=[6.0, 1.6, 0.5]), k(t + 0.06, look=[9.9, 1.6, 0.3]))] +
            [k(0.7, expr='worried'), k(0.7, toon={'hands': {'R': 'grip'}, 'reach': {'R': [8.95, 1.55, 1.0, 1, 0.05]}, 'scl': {'handR': [1.7, 1.7, 1.7]}}, toonDur=0.5, toonEase='in'), k(1.1, expr='scared')])] +
        [rusher(i, t, z0=0.3 + 0.1 * (i % 3)) for i, t in enumerate(R5)],
        props=[DOOR(swing=[[0, OPEN]]), CLICK(opts={'at': 0.05, 'rate': 9})],
        cams=[cam(0.0, [6.5, 1.65, 1.5], [6.65, 1.67, 1.45], [9.4, 1.55, 0.8], [9.4, 1.55, 0.8], lens=44)])
# 6: « four thousand passages a day »: he has stepped aside to the counter on the wall, which rolls up to it; he reads it out, his thumb still swollen,
#    the clicker smoking
CLERK6 = [9.25, 0, 1.75]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[act('agent', CLERK6, -90, 'stand', 'dizzy', keys=[k(0.0, toon={'hands': {'R': 'grip'}, 'reach': {'R': [8.9, 1.7, 1.45, 1, 0.05]}, 'scl': {'handR': [1.7, 1.7, 1.7]}}, toonDur=0), k(0.0, look=None)] + st.talk('L04', 'S06', 'dizzy'))],
        props=[DOOR(swing=[[0, OPEN]]), CLICK(), P('counter', 'rollCounter', pos=[9.9, 2.78, 1.75], ry=-90, scale=0.01, opts={'from': 0, 'to': 4000, 'at': 0.12, 'dur': 0.7, 'w': 1.0, 'h': 0.62}, keys=[k(0.02, scale=1.0, dur=0.14, ease='outBack')]),
               P('smoke', 'dustPuff', pos=[8.85, 1.85, 1.45], scale=0.2, opts={'period': 0.6, 'color': '#C9C9C9'})],
        cams=[cam(0.0, [6.5, 1.95, 2.2], [6.7, 1.97, 2.15], [9.5, 2.05, 1.68], [9.5, 2.05, 1.68], lens=44)])
# 7: at that level it is a... the mayor marches up in his sash and points at him
MAYOR = [9.15, 0, 0.72]                             # the mayor, by the other jamb, three quarters to us
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'unimpressed', keys=[HOLDK(), k(0.0, look='maire'), k(0.75, expr='surprised'), k(0.75, toon=GRIP(OPEN, sq=[0.95, 1.07, 0.95]), toonDur=0.08, toonEase='outBack'), k(0.9, toon=GRIP(OPEN), toonDur=0.1)]),
        act('maire', [9.0, 0, 4.2], 180, 'marchPomp', 'proud', keys=[k(0.0, to=MAYOR, dur=0.6, clip='marchPomp', ease='linear', face=-150), k(0.6, clip='point', expr='determined', blend=0.08, look='mec'),
            k(0.6, toon={'sq': [1.06, 0.92, 1.06]}, toonDur=0.05), k(0.66, toon={'sq': [0.96, 1.06, 0.96], 'hands': {'R': 'point'}}, toonDur=0.1, toonEase='outBack'), k(0.8, toon={'hands': {'R': 'point'}}, toonDur=0.1)])],
        props=[DOOR(swing=[[0, OPEN]]), BEARD(), WEB()],
        cams=[cam(0.0, [3.5, 1.7, 0.0], [3.7, 1.7, -0.05], [9.6, 1.65, -0.15], [9.6, 1.65, -0.15], lens=44)])
# 8: ...public service: a blue enamel plate slams over the bakery's sign; then close on him: a doorman's cap drops onto his head: he sinks under it, only
#    his eyes go up to it
P8 = 0.1                                            # the plate
T8 = 0.42                                           # the cut to him
C8 = T8 + 0.2                                       # the cap lands
CAPOFF = [0.0, 0.5, 0.0]
CAP = lambda **kw: P('cap', 'doormanCap', on={'actor': 'mec', 'joint': 'head', 'offset': CAPOFF, 'rot': [0, 0, 0]}, **kw)   # he wears it from now on
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'surprised', keys=[HOLDK(), k(0.0, look=None), k(P8 + 0.06, toon=GRIP(OPEN, face={'gy': -0.9, 'gx': 0.5}), toonDur=0.08),
            k(T8, toon=GRIP(OPEN, face={'gy': -1.0}), toonDur=0.08),
            k(C8, toon=GRIP(OPEN, sq=[1.14, 0.8, 1.14], face={'gy': -1.0}), toonDur=0.05), k(C8 + 0.06, toon=GRIP(OPEN, sq=[0.97, 1.04, 0.97], face={'gy': -1.0}), toonDur=0.12, toonEase='outBack'),
            k(C8 + 0.24, expr='deadpan'), k(C8 + 0.24, toon=GRIP(OPEN), toonDur=0.08)])],
        props=[DOOR(swing=[[0, OPEN]]), BEARD(), WEB(),
               P('plate', 'signBoard', pos=[DX - 0.13, 0, DZ], ry=-90, scale=0.01, opts={'text': 'SERVICE PUBLIC', 'w': SIGNW + 0.06, 'h': 0.64, 'height': 2.64, 'posts': False, 'frame': '#F4F1E8', 'bg': '#2A4B9B', 'fg': '#F4F1E8'},
                 keys=[k(P8, scale=1.0, dur=0.1, ease='outBack')]),
               P('cap', 'doormanCap', pos=[9.12, 4.2, -1.02], ry=-90, keys=[k(C8 - 0.14, to=[9.12, 2.42, -1.02], dur=0.14, ease='in'), k(C8, attach='mec', joint='head', offset=CAPOFF, rot=[0, 0, 0])])],
        fx=[{'type': 'shake', 'at': P8 + 0.08, 'dur': 0.12, 'amount': 0.016}, {'type': 'shake', 'at': C8, 'dur': 0.1, 'amount': 0.014}],
        cams=[cam(0.0, [5.9, 1.9, 0.25], [6.0, 1.95, 0.25], [9.9, 2.7, 0.2], [9.9, 2.72, 0.2], lens=44),   # the sign and the door (he is just out of the frame)
              cam(T8, [7.0, 1.93, -1.5], [7.1, 1.93, -1.5], [9.12, 1.9, -1.42], [9.12, 1.9, -1.42], lens=44)])   # close on him, left of the sign
# 9: and a public service does not close: he tries to slip away: he tiptoes toward us, his hand still on the handle, the arm paid out behind him like
#    elastic; at the end of it his feet spin on the spot; it takes him back: he is shot against the wall and the leaf swings round on him: pressed in the
#    door like a flower in a book, seen through the glass; the leaf comes back, he peels off the wall
GO9, FAR9 = 0.25, [7.2, 0, -1.82]                    # he goes; how far he gets: toward the camera, a little left of its axis: the arm runs back to the door on the right of him
SNAP9 = 1.3                                         # it takes him back
SAND = [9.8, 0, -1.02]                              # between the wall and the leaf
SWING9 = [[0, OPEN], [SNAP9 + 0.02, OPEN], [SNAP9 + 0.1, 166], [SNAP9 + 0.48, 166], [SNAP9 + 0.68, OPEN]]
FLAT9 = [1.25, 1.0, 0.14]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[HOLDK(), k(0.0, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.08), k(0.12, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.08),   # a look each way, with the eyes only
            k(GO9, to=FAR9, dur=0.75, clip='sneak', ease='out', face='keep'), k(GO9, toon=GRIP(OPEN), toonDur=0.05), k(GO9, expr='determined'),
            k(GO9 + 0.75, clip='scramble', params={'dur': 0.5, 'expr': 'scared'}, blend=0.05), k(GO9 + 0.75, toon=GRIP(OPEN, bend={'spine': [0.35, 0, 0, 1, None]}), toonDur=0.1),   # at the end of the arm: his feet spin
            k(SNAP9, to=SAND, dur=0.09, glide=True, ease='in', face='keep'), k(SNAP9, clip='blownBack', expr='take', blend=0.02), k(SNAP9 + 0.02, toon=GRIP(166), toonDur=0.08),
            k(SNAP9 + 0.09, clip='pressGlass', expr='dizzy', blend=0.02), k(SNAP9 + 0.09, toon=GRIP(166, sq=FLAT9, face={'stars': 1}), toonDur=0.02),   # flat between the wall and the glass
            k(SNAP9 + 0.48, toon=GRIP(OPEN, sq=FLAT9, face={'stars': 1}), toonDur=0.2, toonEase='inOut'),   # the leaf comes back; he stays on the wall
            k(SNAP9 + 0.72, to=HOLD, dur=0.14, glide=True, ease='inOut', face='keep'), k(SNAP9 + 0.72, clip='stand', expr='deadpan', blend=0.1), k(SNAP9 + 0.72, toon=GRIP(OPEN, sq=[0.9, 1.1, 0.9]), toonDur=0.1, toonEase='outBack'),
            k(SNAP9 + 0.84, toon=GRIP(OPEN), toonDur=0.08)])],
        props=[DOOR(swing=SWING9, **PUBLIC), BEARD(), WEB(keys=[k(GO9, visible=False)]), CAP()],
        fx=[{'type': 'shake', 'at': SNAP9 + 0.09, 'dur': 0.18, 'amount': 0.03}],
        cams=[cam(0.0, [5.3, 1.9, -2.7], [5.25, 1.9, -2.72], [9.9, 1.5, 0.0], [9.9, 1.5, 0.0], lens=44),   # the whole sign in the frame; he comes to us on the left of it
              glide([cam(SNAP9 - 0.02, [6.6, 1.45, -2.2], [6.65, 1.45, -2.18], [9.9, 1.15, -1.0], [9.9, 1.15, -1.0], lens=44)], 0.1)])   # the camera goes back with him to the wall, under the sign

CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("La porte", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'dame': CITIZEN('mamie', 51, suit='#8A3A5A', glasses=False), 'agent': CITIZEN('officiel', 53, suit='#6E7A86', tie='#2F6E5C'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    **{f'r{i}': CITIZEN(['femme', 'serveur', 'lyceen', 'madame', 'sportif', 'tourist', 'fermier', 'lyceenne'][i], 60 + i) for i in range(8)}})
