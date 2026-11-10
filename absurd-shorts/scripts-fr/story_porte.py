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
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(0.0, look=None)] + [x for t in B2 for x in (k(t, toon=GRIP(OPEN, face={'gx': -0.4}), toonDur=0.03), k(t + 0.06, toon=GRIP(OPEN, face={'gx': 1.0}), toonDur=0.08), k(t + 0.2, toon=GRIP(OPEN), toonDur=0.08))] +   # his eyes alone follow each one in
            [k(B2[1], expr='unimpressed'), k(0.9, expr='deadpan')])] + [rusher(i, t) for i, t in enumerate(B2)],
        props=[DOOR(swing=[[0, OPEN]]), BEARD(0.01, keys=[k(B2[0] + 0.12, scale=0.5, dur=0.1, ease='outBack'), k(B2[1] + 0.12, scale=0.85, dur=0.1, ease='outBack'), k(B2[2] + 0.12, scale=1.25, dur=0.1, ease='outBack')]),
               WEB(scale=0.01, keys=[k(B2[2] + 0.05, scale=1.0, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [6.5, 1.5, -0.45], [6.65, 1.5, -0.5], [9.3, 1.38, -0.8], [9.3, 1.38, -0.8], lens=44)])   # close: the sign above the door stays out of the frame (it was cut in two)
# 3: behind her there was... first what he sees: the queue, down the pavement, out of sight; then his face, to us: eyes out, the jaw on his tie
QUEUE = lambda **kw: P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[7.7, 1.6], [7.5, 190.0]], 'gap': 0.8, 'people': True, 'seed': 9, **kw})
T3 = 0.56                                           # the cut to his face
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(-0.3, look=[7.6, 1.6, 12.0]), k(T3 + 0.06, look=None, expr='take'),
            k(T3 + 0.06, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.9, 'popLen': 0.14}, sq=[1.04, 0.95, 1.04]), toonDur=0.07, toonEase='outBack'), k(T3 + 0.4, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.9, 'popLen': 0.14}), toonDur=0.1)])],   # the jaw drops, the eyes come out at us; he does not stretch up (his eyes left the frame)
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
            [x for i, t in enumerate(R5) for x in (k(max(0.0, t - 0.05), look=[6.2, 1.6, 1.9]), k(t + 0.06, look=[7.4, 1.6, -0.6]))] +   # like a tennis match, between two points in front of him: his face stays on us
            [k(0.7, expr='worried'), k(0.7, toon={'hands': {'R': 'grip'}, 'reach': {'R': [8.95, 1.55, 1.0, 1, 0.05]}, 'scl': {'handR': [1.7, 1.7, 1.7]}}, toonDur=0.5, toonEase='in'), k(1.1, expr='scared')])] +
        [rusher(i, t, z0=0.3 + 0.1 * (i % 3)) for i, t in enumerate(R5)],
        props=[DOOR(swing=[[0, OPEN]]), CLICK(opts={'at': 0.05, 'rate': 9})],
        cams=[cam(0.0, [6.4, 1.65, 1.7], [6.55, 1.67, 1.65], [9.4, 1.55, 0.98], [9.4, 1.55, 0.98], lens=44)])
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
        cams=[cam(0.0, [3.4, 1.7, -0.05], [3.6, 1.7, -0.1], [9.6, 1.65, -0.18], [9.6, 1.65, -0.18], lens=44)])
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
              cam(T8, [7.0, 2.35, -1.2], [7.1, 2.35, -1.2], [9.12, 1.7, -1.12], [9.12, 1.7, -1.12], lens=44)])   # close on him, from a little above: the sign stays over the top of the frame
# 9: and a public service does not close: he tries to slip away: he tiptoes toward us, his hand still on the handle, the arm paid out behind him like
#    elastic; at the end of it his feet spin on the spot; it takes him back: he is shot against the wall and the leaf swings round on him: pressed in the
#    door like a flower in a book, seen through the glass; the leaf comes back, he peels off the wall
GO9, FAR9 = 0.25, [8.9, 0, -3.4]                     # he goes; how far he gets: sideways along the shop front, across the frame: the arm is a clothes line from his shoulder to the handle (walking toward the camera hid the arm behind him)
SNAP9 = 1.3                                         # it takes him back
SAND = [9.8, 0, -1.02]                              # between the wall and the leaf
SWING9 = [[0, OPEN], [SNAP9 + 0.02, OPEN], [SNAP9 + 0.1, 166], [SNAP9 + 0.48, 166], [SNAP9 + 0.68, OPEN]]
FLAT9 = [1.25, 1.0, 0.14]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[HOLDK(), k(0.0, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.08), k(0.12, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.08),   # a look each way, with the eyes only
            k(GO9, to=FAR9, dur=0.75, clip='sneak', ease='out', face='keep'), k(GO9, toon=GRIP(OPEN), toonDur=0.05), k(GO9, expr='determined'),
            k(GO9 + 0.75, clip='scramble', params={'dur': 0.5, 'expr': 'scared'}, blend=0.05), k(GO9 + 0.75, toon=GRIP(OPEN, bend={'spine': [0.35, 0, 0, 1, None]}), toonDur=0.1),   # at the end of the arm: his feet spin
            k(SNAP9, to=SAND, dur=0.09, glide=True, ease='in', face='keep'), k(SNAP9, clip='blownBack', expr='take', blend=0.02), k(SNAP9 + 0.02, toon=GRIP(166), toonDur=0.08),
            k(SNAP9 + 0.09, clip='pressGlass', expr='dizzy', blend=0.02), k(SNAP9 + 0.09, toon=GRIP(166, sq=FLAT9, face={'stars': 1}), toonDur=0.02),   # flat between the wall and the glass
            k(SNAP9 + 0.48, toon=GRIP(OPEN, sq=FLAT9, face={'stars': 1}), toonDur=0.2, toonEase='inOut'),   # the leaf comes back, his arm goes with it; he stays on the wall, as thin as a poster,
            k(SNAP9 + 0.66, clip='poster', params={'high': 0.0, 'slideAt': 0.04, 'slide': 0.35, 'peelK': 1.1, 'stars': 1}, expr='dizzy', blend=0.05)])],   # and starts to come off it: we leave him there
        props=[DOOR(swing=SWING9, **PUBLIC), BEARD(), WEB(keys=[k(GO9, visible=False)]), CAP()],
        fx=[{'type': 'shake', 'at': SNAP9 + 0.09, 'dur': 0.18, 'amount': 0.03}],
        cams=[cam(0.0, [4.6, 1.8, -7.0], [4.65, 1.8, -6.9], [9.2, 1.65, -2.0], [9.2, 1.65, -2.0], lens=44),   # three quarters along the shop front: the door and its whole sign on the right, he goes off to the left
              glide([cam(SNAP9 - 0.02, [6.6, 1.45, -2.2], [6.65, 1.45, -2.18], [9.9, 1.15, -1.0], [9.9, 1.15, -1.0], lens=44)], 0.1)])   # the camera goes back with him to the wall, under the sign

# 10: his replacement is in the queue: far down it a man in the same cap leans out, his neck up over the heads, and waves his ticket; the camera runs
#     down the queue to him
REMP = [7.05, 0, 9.4]
Z10 = 0.42                                          # the camera goes
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('remp', REMP, 185, 'stand', 'happy', keys=[k(0.0, look=[8.6, 1.7, -1.0]), k(0.1, clip='wave', blend=0.1),
            k(0.1, toon={'bend': {'neck': [0, 0, 0, 2.3, None], 'spine': [0, 0, -0.25, 1, None]}, 'sq': [0.96, 1.08, 0.96]}, toonDur=0.22, toonEase='outBack'),   # he leans out of the line, his neck up over the heads
            k(Z10 + 0.5, expr='bigGrin'), k(Z10 + 0.5, toon={'bend': {'neck': [0, 0, 0.12, 2.5, None], 'spine': [0, 0, -0.25, 1, None]}}, toonDur=0.1), k(Z10 + 0.7, toon={'bend': {'neck': [0, 0, -0.12, 2.5, None], 'spine': [0, 0, -0.25, 1, None]}}, toonDur=0.12)])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), QUEUE(), P('rcap', 'doormanCap', on={'actor': 'remp', 'joint': 'head', 'offset': CAPOFF, 'rot': [0, 0, 0]}),
               P('ticket', 'queueTicket', on={'actor': 'remp', 'hand': 'R', 'offset': [0, 0.02, 0.02], 'rot': [0, 0, 0]}, scale=3.0, opts={'num': '2', 'sub': 'Porte'})],
        cams=[cam(0.0, [8.7, 1.6, -1.6], [8.68, 1.62, -1.4], [7.5, 1.5, 14.0], [7.5, 1.5, 14.0], lens=44),
              glide([cam(Z10, [8.1, 2.3, 5.6], [8.05, 2.3, 5.75], [7.05, 2.75, 9.4], [7.05, 2.75, 9.4], lens=44)], 0.22)])
# 11: in the evening he goes home: from above the door, at night: he walks away down the pavement, waving good night without turning round; the arm is paid
#     out behind him, a long line from the handle, pigeons asleep on it
NIGHT = {**STREET, 'night': True}
W11 = [[8.95, -4.6], [8.9, -6.9]]                    # where he walks in this shot
st.shot('S11', 'parisStreet', setOpts=NIGHT, lighting='night', actors=[act('mec', [W11[0][0], 0, W11[0][1]], 180, 'walk', 'deadpan', keys=[k(-0.05, toon=GRIP(OPEN), toonDur=0),
            k(0.0, to=[W11[1][0], 0, W11[1][1]], dur=st.dur('S11'), clip='walk', ease='linear'), k(0.5, toon=GRIP(OPEN, hands={'L': 'grip', 'R': 'spread'}, reach={'L': [*handle(OPEN), 1, 0.05, [0.2, -1, 0.5]], 'R': [8.5, 2.75, -5.9, 1, 0.1]}), toonDur=0.16, toonEase='outBack'),   # a wave over his shoulder
            k(0.72, toon=GRIP(OPEN, hands={'L': 'grip', 'R': 'spread'}, reach={'L': [*handle(OPEN), 1, 0.05, [0.2, -1, 0.5]], 'R': [8.75, 2.8, -6.2, 1, 0.1]}), toonDur=0.1), k(0.9, toon=GRIP(OPEN), toonDur=0.2)])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(), CAP(), P('pg1', 'pigeon', pos=[9.0, 1.42, -2.2], ry=90, opts={'ph': 0.3}), P('pg2', 'pigeon', pos=[8.98, 1.52, -3.3], ry=90, opts={'ph': 1.7})],
        cams=[cam(0.0, [8.3, 3.0, 2.2], [8.35, 3.1, 2.5], [8.95, 1.3, -6.0], [8.95, 1.3, -6.4], lens=44)])   # low enough for the night sky and the lit windows
# 12: the arm stays: his bedroom: he sleeps on his back, cap on, the arm across him and out through the window; somebody uses the door: the arm twitches
#     and takes him off the bed, flat against the wall under the window; he does not wake up
WIN = [-4.7, 1.75, -0.6]                            # through the window
BED12 = [-2.6, 0.62, -1.7]                          # on the set's bed (2 m long along Z, the pillow toward -Z)
TUG = 0.5
ARM12 = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*WIN, 1, 0.05]}, **kw}
st.shot('S12', 'chambre', setOpts={'poster': 'SERVICE\nPUBLIC', 'posterBg': '#2A4B9B', 'posterFg': '#F4F1E8'}, actors=[act('mec', BED12, 0, 'lieBack', 'sleepy', keys=[k(-0.05, toon=ARM12(), toonDur=0), k(0.02, toon=ARM12(sq=[1.0, 1.0, 1.1], face={'jaw': 0.3}), toonDur=0.16, toonEase='inOut'), k(0.2, toon=ARM12(), toonDur=0.16, toonEase='inOut'),   # a snore: the chest comes up, goes down
            k(TUG - 0.12, toon=ARM12(sq=[1.03, 0.97, 1.03]), toonDur=0.1), k(TUG, to=[-4.05, 0.75, -1.1], dur=0.1, glide=True, ease='in', face='keep'), k(TUG, toon=ARM12(sq=[0.9, 1.2, 0.9]), toonDur=0.08),
            k(TUG + 0.1, clip='poster', params={'high': 0.0, 'slideAt': 9, 'stars': 0}, expr='sleepy', blend=0.02, face=90), k(TUG + 0.1, toon=ARM12(sq=[1.2, 1.0, 0.3]), toonDur=0.03), k(TUG + 0.16, toon=ARM12(sq=[1.0, 1.0, 0.6]), toonDur=0.15, toonEase='outBack')])],
        props=[BEARD(), CAP()],
        fx=[{'type': 'shake', 'at': TUG + 0.1, 'dur': 0.15, 'amount': 0.025}],
        cams=[cam(0.0, [3.4, 1.9, -1.65], [3.3, 1.9, -1.65], [-4.4, 1.25, -1.65], [-4.4, 1.25, -1.65], lens=44)])   # from the side of the room: he lies across the frame, the window over his feet
# 13: the door is listed as a historic monument: a bronze plaque over him; a tourist comes for a selfie with him, as with the guards, and pokes his cheek:
#     his head rocks, his eyes go to the finger; nothing else moves
PLQ = round(st.at('S13', 'L09', 4) - 0.05, 3)       # the plaque, on « monument »
BRONZE = lambda **kw: P('bronze', 'bronzePlaque', pos=[9.84, 2.62, -2.3], ry=-90, opts={'text': 'MONUMENT/HISTORIQUE', 'w': 1.3, 'h': 0.72}, **kw)   # over the heads
TOUR = [9.0, 0, -2.1]                               # beside him along the wall, on the camera's side of him but clear of him on the screen
POKE = 1.55
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stiffStand', 'deadpan', keys=[HOLDK(), k(0.0, look=None), k(POKE - 0.1, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.06),
            k(POKE, toon=GRIP(OPEN, face={'gx': -0.9}, bend={'neck': [0, 0, -0.22, 1, None]}), toonDur=0.05), k(POKE + 0.07, toon=GRIP(OPEN, face={'gx': -0.9}, bend={'neck': [0, 0, 0.1, 1, None]}), toonDur=0.07),
            k(POKE + 0.16, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.1), k(POKE + 0.35, toon=GRIP(OPEN), toonDur=0.1)]),   # his head rocks under the finger; only his eyes go to it
        act('t1', [8.6, 0, -5.6], 0, 'walk', 'happy', keys=[k(0.0, to=TOUR, dur=0.8, clip='walk', ease='out', face=-110), k(0.8, clip='showPhoneFaceL', expr='bigGrin', blend=0.12, look=None),
            k(0.85, toon={'sq': [1.05, 0.93, 1.05]}, toonDur=0.05), k(0.9, toon={'sq': [0.97, 1.05, 0.97], 'bend': {'spine': [0, 0, -0.18, 1, None]}}, toonDur=0.12, toonEase='outBack'),   # he leans in to be in the picture
            k(POKE - 0.22, toon={'hands': {'R': 'point'}, 'reach': {'R': [8.9, 2.02, -1.5, 1, 0.16]}, 'bend': {'spine': [0, 0, -0.18, 1, None]}}, toonDur=0.14, toonEase='out'),
            k(POKE - 0.03, toon={'hands': {'R': 'point'}, 'reach': {'R': [8.98, 2.02, -1.22, 1, 0.16]}, 'bend': {'spine': [0, 0, -0.18, 1, None]}}, toonDur=0.04),
            k(POKE + 0.1, toon={'hands': {'R': 'point'}, 'reach': {'R': [8.9, 2.02, -1.5, 1, 0.16]}, 'bend': {'spine': [0, 0, -0.18, 1, None]}}, toonDur=0.1), k(POKE + 0.1, expr='laugh')])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(1.6), CAP(), WEB(), BRONZE(scale=0.01, keys=[k(PLQ, scale=1.0, dur=0.12, ease='outBack')]),
               P('phone', 'smartPhone', on={'actor': 't1', 'hand': 'L', 'offset': [0, 0.02, 0.02], 'rot': [0, 0, 0]}, scale=1.6, opts={'call': False}, keys=[k(0.0, visible=False), k(0.8, visible=True)]),
               P('pg', 'pigeon', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.6, 0.0], 'rot': [0, 0, 0]}, opts={'ph': 0.5})],
        fx=[{'type': 'shake', 'at': PLQ + 0.1, 'dur': 0.1, 'amount': 0.012}],
        cams=[cam(0.0, [4.6, 1.8, -7.0], [4.7, 1.8, -6.85], [9.2, 1.65, -2.0], [9.2, 1.65, -2.0], lens=44)])   # three quarters along the shop front, as when he tried to leave
# 14: the arm too: close on him and his arm: a small plaque is screwed on the sleeve; the pigeon comes down from his cap to sit by it
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stiffStand', 'deadpan', keys=[HOLDK(), k(0.0, look=None), k(0.3, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.6}), toonDur=0.08), k(0.7, toon=GRIP(OPEN), toonDur=0.1)])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(1.6), CAP(), WEB(),
               P('bronze2', 'bronzePlaque', pos=[8.98, 1.17, -0.84], ry=-90, rot=[0, 0, -0.35], scale=0.01, opts={'text': 'BRAS/CLASSÉ', 'w': 0.3, 'h': 0.18}, keys=[k(0.14, scale=1.0, dur=0.1, ease='outBack')]),
               P('pg', 'pigeon', pos=[9.1, 2.62, -1.02], ry=-90, opts={'ph': 0.5}, keys=[k(0.35, to=[9.05, 1.42, -0.86], dur=0.22, ease='out', arc=0.2)])],
        fx=[{'type': 'shake', 'at': 0.2, 'dur': 0.08, 'amount': 0.01}],
        cams=[cam(0.0, [6.6, 2.25, -0.9], [6.7, 2.25, -0.9], [9.1, 1.58, -0.88], [9.1, 1.58, -0.88], lens=44)])   # from a little above: the sign stays over the top of the frame
# 15: yesterday a technician came by: he sets his toolbox down by the other jamb, finds a box on the wall: one big button, AUTO: he presses it
T15 = round(st.dur('S15') - 0.3, 3)                 # he presses
TECH = [9.2, 0, 1.6]
SW = [9.88, 1.4, 2.15]                              # the box on the wall, right of the door
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('tech', [9.0, 0, 4.4], 180, 'walk', 'neutral', keys=[k(0.0, to=TECH, dur=0.7, clip='walk', ease='out', face=-60), k(0.7, clip='stand', blend=0.1, look=[9.9, 2.4, 0.0], expr='hmm'),
            k(1.0, look=SW, expr='surprised'), k(T15 - 0.3, toon={'hands': {'L': 'point'}, 'reach': {'L': [SW[0] - 0.3, SW[1], SW[2] - 0.05, 1, 0.16]}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.2, toonEase='out'),
            k(T15 - 0.04, toon={'hands': {'L': 'point'}, 'reach': {'L': [SW[0] - 0.07, SW[1] - 0.05, SW[2], 1, 0.16]}}, toonDur=0.04), k(T15 + 0.08, expr='happy', look=[9.9, 1.6, 0.0])])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), P('box', 'toolbox', pos=[8.8, 0, 2.5], ry=-70), P('switch', 'wallSwitch', pos=SW, ry=-90, scale=0.01, opts={'at': T15, 'label': 'AUTO'}, keys=[k(0.95, scale=1.7, dur=0.12, ease='outBack')])],
        cams=[cam(0.0, [6.3, 1.45, 2.6], [6.45, 1.45, 2.55], [9.8, 1.4, 2.0], [9.8, 1.4, 2.0], lens=44)])   # right of the door: its sign stays out of the frame
# 16: it was automatic: the leaf leaves his hand: it shuts by itself, slides open, shuts, opens; his hand stays in the air, holding nothing: he looks at it,
#     at the door, at it again (a double take), then at us
SHUT16 = 0.3                                         # the leaf has swung shut
SLIDE16 = [[0, 0], [0.42, 0], [0.6, 0.95], [0.74, 0.95], [0.88, 0], [0.96, 0], [1.1, 0.95]]
AIR = handle(OPEN)                                  # where the handle was: his hand stays there
FREE = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*AIR, 1, 0.05, [0.2, -1, 0.5]]}, **kw}
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[k(-0.05, toon=FREE(), toonDur=0), k(0.1, look=[9.9, 1.3, 0.0], expr='surprised'), k(0.36, toon=FREE(face={'gx': 0.9, 'gy': 0.4}), toonDur=0.06),
            k(0.5, look=[9.9, 1.3, 0.2]), k(0.62, clip='doubleTakeToon', blend=0.04, look=None), k(0.62, toon=FREE(), toonDur=0.05), k(1.0, clip='stand', expr='deadpan', blend=0.1)])],
        props=[DOOR(swing=[[0, OPEN], [0.05, OPEN], [SHUT16, 0]], slide=SLIDE16, led=0.4, **PUBLIC), BEARD(1.6), CAP(), BRONZE()],
        cams=[cam(0.0, [5.2, 1.7, -2.6], [5.3, 1.7, -2.5], [9.6, 1.55, -0.5], [9.6, 1.55, -0.5], lens=44)])
# 17: the lady never said thank you: the door slides open for her; she comes out with her bread, goes by under his nose and away; he raises a finger, his
#     mouth opens; nothing; then his arm: he pushes it down with the other hand; it comes back up by itself, where the handle was
OUT17 = 0.25                                        # she comes out
LADY17 = [(10.5, 0.0), (8.6, 0.05), (8.2, -1.6), (7.9, -6.5)]
PUSH = 2.0                                          # he pushes his arm down
DOWN17 = [9.0, 0.95, -1.0]
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[k(-0.05, toon=FREE(), toonDur=0), k(0.3, look='dame', expr='surprised'),
            k(1.15, toon=FREE(hands={'L': 'grip', 'R': 'point'}, reach={'L': [*AIR, 1, 0.05, [0.2, -1, 0.5]], 'R': [8.75, 2.25, -1.5, 1, 0.16]}, sq=[0.97, 1.05, 0.97]), toonDur=0.14, toonEase='outBack'), k(1.2, expr='yell'),   # a finger, his mouth open
            k(1.62, toon=FREE(sq=[1.03, 0.96, 1.03]), toonDur=0.3, toonEase='inOut'), k(1.62, expr='sad', look=[8.0, 1.2, -5.0]),   # she has gone: the finger comes down
            k(PUSH - 0.12, look=AIR, expr='hmm'), k(PUSH, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*DOWN17, 1, 0.05, [0.2, -1, 0.5]], 'R': [DOWN17[0], DOWN17[1] + 0.1, DOWN17[2], 1, 0.08]}, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.22, toonEase='inOut'),   # he pushes it down
            k(PUSH + 0.36, toon=FREE(sq=[0.96, 1.06, 0.96]), toonDur=0.1, toonEase='outBack'), k(PUSH + 0.36, expr='surprised'),   # he lets go: it springs back to where the handle was
            k(PUSH + 0.6, look=None, expr='deadpan'), k(PUSH + 0.6, toon=FREE(), toonDur=0.1)]),
        act('dame', [LADY17[0][0], 0, LADY17[0][1]], -90, 'walk', 'smug', keys=[k(0.0, visible=False), k(OUT17, visible=True), k(OUT17, to=[LADY17[1][0], 0, LADY17[1][1]], dur=0.55, clip='walk', ease='linear'),
            k(OUT17 + 0.55, to=[LADY17[2][0], 0, LADY17[2][1]], dur=0.5, clip='walk', ease='linear'), k(OUT17 + 1.05, to=[LADY17[3][0], 0, LADY17[3][1]], dur=1.5, clip='walk', ease='linear')])],
        props=[DOOR(swing=[[0, 0]], slide=[[0, 0], [0.05, 0], [0.22, 0.95], [1.0, 0.95], [1.2, 0], [2.5, 0], [2.66, 0.95]], led=0.0, **PUBLIC), BEARD(1.6), CAP(), BRONZE(),
               P('bread', 'baguette', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0.1, 0], 'rot': [0, 0, 1.3]}, keys=[k(0.0, visible=False), k(OUT17, visible=True)])],
        cams=[cam(0.0, [4.6, 1.7, -2.0], [4.8, 1.7, -1.9], [9.5, 1.55, -0.6], [9.5, 1.55, -0.6], lens=44)])

# sound on the actions
st.cue('sfx:squeak', 'S01', O1, 0.3)
for t_ in B2: st.cue('whoosh', 'S02', t_, 0.35, 0.2, 500, 3500); st.cue('pop', 'S02', t_ + 0.12, 0.25)
st.cue('sfx:gasp', 'S03', T3 + 0.06, 0.35)
for i_, t_ in enumerate(R5): st.cue('whoosh', 'S05', t_, 0.25, 0.18, 500, 3500); st.cue('sfx:tick', 'S05', t_ + 0.06, 0.22 + 0.02 * i_)
st.cue('pop', 'S06', 0.02, 0.3); st.cue('sfx:slideUp', 'S06', 0.12, 0.3)
st.cue('pop', 'S07', 0.62, 0.3)
st.cue('clack', 'S08', P8 + 0.08, 0.45); st.cue('thud', 'S08', C8, 0.4)
st.cue('sfx:stretch', 'S09', GO9, 0.35); st.cue('sfx:zip', 'S09', SNAP9, 0.4); st.cue('sfx:splat', 'S09', SNAP9 + 0.09, 0.5); st.cue('sfx:squeak', 'S09', SNAP9 + 0.5, 0.3)
st.cue('whoosh', 'S10', Z10, 0.3, 0.22, 400, 3000); st.cue('pop', 'S10', Z10 + 0.22, 0.3)
st.cue('sfx:stretch', 'S12', TUG - 0.1, 0.3); st.cue('sfx:zip', 'S12', TUG, 0.35); st.cue('thud', 'S12', TUG + 0.1, 0.5)
st.cue('clack', 'S13', PLQ + 0.1, 0.4); st.cue('pop', 'S13', POKE, 0.3)
st.cue('clack', 'S14', 0.2, 0.35)
st.cue('sfx:tick', 'S15', T15, 0.45)
st.cue('sfx:slideUp', 'S16', 0.42, 0.3); st.cue('sfx:slideUp', 'S16', 0.74, 0.25); st.cue('sfx:slideUp', 'S16', 0.96, 0.25)
st.cue('sfx:slideUp', 'S17', 0.05, 0.3); st.cue('sfx:stretch', 'S17', PUSH, 0.3); st.cue('sfx:spring', 'S17', PUSH + 0.36, 0.45)

st.card('S12', 'LE BRAS RESTE')
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("La porte", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'dame': CITIZEN('mamie', 51, suit='#8A3A5A', glasses=False), 'agent': CITIZEN('officiel', 53, suit='#6E7A86', tie='#2F6E5C'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'remp': CITIZEN('lemec_brown', 71), 't1': CITIZEN('tourist', 73), 'tech': CITIZEN('worker', 77, glasses=False),
    **{f'r{i}': CITIZEN(['femme', 'proviseur', 'lyceen', 'madame', 'sportif', 'tourist', 'fermier', 'lyceenne'][i], 60 + i) for i in range(8)}})
