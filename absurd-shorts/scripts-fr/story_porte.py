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
RIP = lambda a, ph, n=2: {'armL': [a, n, ph, 0, 1.5708], 'foreL': [a, n, ph - n, 0, 1.5708]}   # a ripple along the stretched arm (toon channel `wave`): a metres high, n waves on each half, moved along by ph (rising: toward the hand)

# 1: he reaches the bakery door, sees a lady coming, pulls it open with a bow; she walks in without a look
O1 = 0.42                                           # the door starts to open
LADY = [(7.4, 4.6), (8.3, 0.25), (10.6, 0.0)]       # her way: along the pavement, then in
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [9.05, 0, 0.55], -90, 'stand', 'neutral', keys=[k(0.0, toon=GRIP(0), toonDur=0), k(0.0, look=[9.0, 1.2, 0.5]), k(0.14, look='dame', expr='surprised'),
            k(0.3, expr='happy'), k(O1, to=HOLD, dur=0.24, glide=True, ease='inOut', face=-90), k(O1, toon=GRIP(OPEN, sq=[1.03, 0.96, 1.03]), toonDur=0.24, toonEase='inOut'),
            k(O1 + 0.3, toon=GRIP(OPEN, bend={'spine': [0.5, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}), toonDur=0.16, toonEase='outBack'), k(O1 + 0.3, look=[7.8, 0.6, 0.3], expr='proud'),   # a bow
            k(1.35, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.2), k(1.35, look=None, expr='happy'), k(1.58, toon=GRIP(OPEN, face={'gx': 0.9, 'lid': 1}), toonDur=0.04), k(1.66, toon=GRIP(OPEN, face={'gx': 0.6, 'browL': 0.5}), toonDur=0.05),   # he straightens: his eyes go in after her; a blink
            k(1.75, expr='neutral'), k(1.78, toon=GRIP(OPEN, sq=[1.02, 0.97, 1.02]), toonDur=0.12)]),   # and he settles to wait
        act('dame', [LADY[0][0], 0, LADY[0][1]], 180, 'walk', 'smug', keys=[k(0.0, to=[LADY[1][0], 0, LADY[1][1]], dur=1.05, clip='walk', ease='linear'), k(1.05, to=[LADY[2][0], 0, LADY[2][1]], dur=0.55, clip='walk', ease='linear'),
            k(1.44, visible=False)])],
        props=[DOOR(swing=[[0, 0], [O1, 0], [O1 + 0.24, OPEN]])],
        cams=[cam(0.0, [4.3, 1.7, -2.3], [4.5, 1.7, -2.2], [9.7, 1.5, -0.3], [9.7, 1.5, -0.3], lens=44)])   # from the side he steps to: the open leaf is seen at an angle, a pane of glass beside him

# 2: he is still holding it: people shoot through the doorway one after the other; at each one his beard grows a notch; a cobweb between his arm and the leaf
HOLDK = lambda **kw: k(-0.05, toon=GRIP(OPEN, **kw), toonDur=0)
def rusher(i, t0, z0=0.25, x0=5.2):                    # somebody who dashes into the bakery
    return act(f'r{i}', [x0, 0, z0], 90, 'stand', 'neutral', keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, to=[DX + 0.6, 0, 0.0], dur=0.2, clip='dashOff', ease='linear', blend=0.01), k(t0 + 0.19, visible=False)])
BEARD = lambda sc=1.25, **kw: P('beard', 'beard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.03, 0.09], 'rot': [0, 0, 0]}, scale=sc, opts={'color': '#17161A'}, **kw)   # it stays from now on
JAWB = [0.0, -0.19, 0.09]                           # where the beard hangs when his jaw has dropped (it stayed beside his mouth)
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
            [k(0.7, expr='worried'), k(0.7, toon={'hands': {'R': 'grip'}, 'reach': {'R': [8.95, 1.55, 1.0, 1, 0.05]}, 'scl': {'handR': [1.7, 1.7, 1.7]}}, toonDur=0.5, toonEase='in'), k(1.1, expr='scared')])] +
        [rusher(i, t, z0=0.3 + 0.1 * (i % 3)) for i, t in enumerate(R5)],
        props=[DOOR(swing=[[0, OPEN]]), CLICK(opts={'at': 0.05, 'rate': 9})],
        cams=[cam(0.0, [6.25, 1.55, 1.8], [6.4, 1.57, 1.75], [9.4, 1.36, 1.05], [9.4, 1.36, 1.05], lens=44)])   # tilted down: the bakery's sign stays over the top of the frame (it was cut to NGERIE)
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
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'unimpressed', keys=[HOLDK(face={'gx': 0.9}), k(0.0, look=None), k(0.2, toon=GRIP(OPEN, face={'gx': 0.9, 'lid': 1}), toonDur=0.04), k(0.28, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.05),   # his eyes on the mayor who marches up; a blink
            k(0.62, expr='surprised'), k(0.62, toon=GRIP(OPEN, sq=[0.95, 1.07, 0.95], face={'gx': 0.7, 'eye': 0.25}), toonDur=0.08, toonEase='outBack'), k(0.8, toon=GRIP(OPEN, face={'gx': 0.7, 'gy': -0.3, 'browL': 0.7, 'browR': -0.3}), toonDur=0.1)]),
        act('maire', [9.05, 0, 2.7], 180, 'marchPomp', 'proud', keys=[k(0.0, to=MAYOR, dur=0.5, clip='marchPomp', ease='linear', face=-125), k(0.5, clip='point', expr='determined', blend=0.08, look='mec'),
            k(0.5, toon={'sq': [1.06, 0.92, 1.06]}, toonDur=0.05), k(0.56, toon={'sq': [0.96, 1.06, 0.96], 'hands': {'R': 'point'}}, toonDur=0.1, toonEase='outBack'), k(0.72, toon={'hands': {'R': 'point'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.06),
            k(0.84, toon={'hands': {'R': 'point'}}, toonDur=0.08), k(0.96, toon={'hands': {'R': 'point'}, 'bend': {'spine': [0.14, 0, 0, 1, None]}, 'face': {'jaw': 0.3}}, toonDur=0.06), k(1.08, toon={'hands': {'R': 'point'}}, toonDur=0.08)])],   # the finger, jabbed twice more
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
        props=[DOOR(swing=[[0, OPEN]]), BEARD(), WEB(),
               P('plate', 'signBoard', pos=[DX - 0.13, 0, DZ], ry=-90, scale=0.01, opts={'text': 'SERVICE PUBLIC', 'w': SIGNW + 0.06, 'h': 0.64, 'height': 2.64, 'posts': False, 'frame': '#F4F1E8', 'bg': '#2A4B9B', 'fg': '#F4F1E8'},
                 keys=[k(P8, scale=1.0, dur=0.1, ease='outBack'), k(P8 + 0.1, squash=[1.1, 0.82, 1.0], dur=0.3)]),
               P('cap', 'doormanCap', pos=[9.12, 3.3, -1.02], ry=-90, keys=[k(0.0, visible=False), k(C8 - 0.13, visible=True), k(C8 - 0.13, to=[9.12, 2.42, -1.02], dur=0.13, ease='in'), k(C8, attach='mec', joint='head', offset=CAPOFF, rot=[0, 0, 0]), k(C8, squash=[1.35, 0.5, 1.35], dur=0.35)])],   # the plate and the cap squash where they land (prop key `squash`)
        fx=[{'type': 'shake', 'at': P8 + 0.08, 'dur': 0.12, 'amount': 0.016}, {'type': 'shake', 'at': C8, 'dur': 0.1, 'amount': 0.014}],
        cams=[cam(0.0, [5.9, 1.9, 0.25], [6.0, 1.95, 0.25], [9.9, 2.7, 0.2], [9.9, 2.72, 0.2], lens=44),   # the sign and the door (he is just out of the frame)
              cam(T8, [6.1, 2.25, -1.2], [6.2, 2.25, -1.2], [9.12, 1.6, -1.1], [9.12, 1.6, -1.1], lens=44)])   # on him, from a little above, far enough to hold him standing and sunk; the sign stays over the top of the frame
# 9: and a public service does not close: he tries to slip away: he tiptoes toward us, his hand still on the handle, the arm paid out behind him like
#    elastic; at the end of it his feet spin on the spot; it takes him back: he is shot against the wall and the leaf swings round on him: pressed in the
#    door like a flower in a book, seen through the glass; the leaf comes back, he peels off the wall
GO9, FAR9 = 0.25, [8.9, 0, -3.4]                     # he goes; how far he gets: sideways along the shop front, across the frame: the arm is a clothes line from his shoulder to the handle (walking toward the camera hid the arm behind him)
SNAP9 = 1.36                                        # it takes him back
SAND = [9.85, 0, -1.02]                             # between the wall and the leaf
SWING9 = [[0, OPEN], [SNAP9 + 0.02, OPEN], [SNAP9 + 0.1, 166], [SNAP9 + 0.48, 166], [SNAP9 + 0.68, OPEN]]
FLAT9 = [1.9, 1.0, 0.09]                            # pressed: nearly twice his width, no thicker than the pane
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[HOLDK(), k(0.0, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.08), k(0.12, toon=GRIP(OPEN, face={'gx': 0.9}), toonDur=0.08),   # a look each way, with the eyes only
            k(GO9, to=FAR9, dur=0.75, clip='sneak', ease='out', face='keep'), k(GO9, toon=GRIP(OPEN), toonDur=0.05), k(GO9, expr='determined'),
            k(GO9 + 0.75, clip='scramble', params={'dur': 0.5, 'expr': 'scared'}, blend=0.05), k(GO9 + 0.75, toon=GRIP(OPEN, bend={'spine': [0.35, 0, 0, 1, None]}), toonDur=0.1),   # at the end of the arm: his feet spin
            k(GO9 + 0.8, toon=GRIP(OPEN, bend={'spine': [0.35, 0, 0, 1, None]}, wave=RIP(0.06, 0)), toonDur=0.08), k(GO9 + 0.88, toon=GRIP(OPEN, bend={'spine': [0.4, 0, 0, 1, None]}, wave=RIP(0.08, 2.2)), toonDur=round(SNAP9 - GO9 - 0.9, 3)),   # and the arm, taut, hums like a string before it takes him back
            k(SNAP9, to=SAND, dur=0.09, glide=True, ease='in', face='keep'), k(SNAP9, clip='blownBack', expr='take', blend=0.02), k(SNAP9 + 0.02, toon=GRIP(166), toonDur=0.08),
            k(SNAP9 + 0.09, clip='pressGlass', expr='dizzy', blend=0.02), k(SNAP9 + 0.09, toon=GRIP(166, sq=FLAT9, scl={'handR': [1.6, 1.6, 1]}, hands={'L': 'grip', 'R': 'spread'}, face={'stars': 1, 'mouth': 'o', 'mouthW': 0.6}), toonDur=0.02),   # flat between the wall and the glass, a palm spread on it
            k(SNAP9 + 0.48, toon=GRIP(OPEN, sq=FLAT9, face={'stars': 1}), toonDur=0.2, toonEase='inOut'),   # the leaf comes back, his arm goes with it; he stays on the wall, as thin as a poster,
            k(SNAP9 + 0.6, clip='poster', params={'high': 0.0, 'slideAt': 0.02, 'slide': 0.5, 'peelK': 2.2, 'stars': 1}, expr='dizzy', blend=0.05)])],   # and comes off it head first, like wallpaper: we leave him there
        props=[DOOR(swing=SWING9, glass=0.14, **PUBLIC), BEARD(), WEB(keys=[k(GO9, visible=False)]), CAP()],
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
# 11: in the evening he goes home: from above the door, at night: he walks away down the pavement, waving good night without turning round; the arm is paid
#     out behind him, a long line from the handle, pigeons asleep on it
NIGHT = {**STREET, 'night': True}
W11 = [[8.95, -4.6], [8.9, -6.9]]                    # where he walks in this shot
NIGHTGRADE = dict(dark=[[0, 0.72, 0.001]], darkFloor=0.5, darkTint='#7A98F0')   # a night: half the light of the day, cold
H11 = handle(OPEN)
def on_arm(f, t01):   # a point of the arm paid out behind him: f of the way from the handle to his shoulder, when he has walked t01 of his way
    sx, sz = W11[0][0] - 0.26 + (W11[1][0] - W11[0][0]) * t01, W11[0][1] + (W11[1][1] - W11[0][1]) * t01
    return [round(H11[0] + f * (sx - H11[0]), 3), round(H11[1] + f * (1.63 - H11[1]) + 0.035, 3), round(H11[2] + f * (sz - H11[2]), 3)]
PG11 = lambda i, f, ph: P(f'pg{i}', 'pigeon', pos=on_arm(f, 0), ry=-90, scale=1.5, opts={'ph': ph, 'sleep': True}, keys=[k(0.0, to=on_arm(f, 1), dur=st.dur('S11'), ease='linear')])   # it rides the arm as it pays out
st.shot('S11', 'parisStreet', setOpts=NIGHT, lighting='night', actors=[act('mec', [W11[0][0], 0, W11[0][1]], 180, 'walk', 'deadpan', keys=[k(-0.05, toon=GRIP(OPEN), toonDur=0),
            k(0.0, to=[W11[1][0], 0, W11[1][1]], dur=st.dur('S11'), clip='walk', ease='linear'), k(0.5, toon=GRIP(OPEN, hands={'L': 'grip', 'R': 'spread'}, reach={'L': [*handle(OPEN), 1, 0.05, [0.2, -1, 0.5]], 'R': [8.5, 2.75, -5.9, 1, 0.1]}), toonDur=0.16, toonEase='outBack'),   # a wave over his shoulder
            k(0.72, toon=GRIP(OPEN, hands={'L': 'grip', 'R': 'spread'}, reach={'L': [*handle(OPEN), 1, 0.05, [0.2, -1, 0.5]], 'R': [8.75, 2.8, -6.2, 1, 0.1]}), toonDur=0.1), k(0.9, toon=GRIP(OPEN), toonDur=0.2)])],
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(), CAP(), PG11(1, 0.3, 0.3), PG11(2, 0.55, 1.7),
               P('lampA', 'streetLamp', pos=[7.75, 0, -3.2], inDark=True, opts={'on': True, 'light': 9}), P('lampB', 'streetLamp', pos=[7.75, 0, -10.5], inDark=True, opts={'on': True, 'light': 9}),   # warm pools on the pavement
               P('winA', 'window', pos=[9.97, 3.3, -4.4], ry=-90, inDark=True, opts={'w': 1.0, 'h': 1.3, 'lit': True, 'color': '#3A3F4A'}), P('winB', 'window', pos=[9.97, 3.3, -8.6], ry=-90, inDark=True, opts={'w': 1.0, 'h': 1.3, 'lit': True, 'color': '#3A3F4A'})], **NIGHTGRADE,
        cams=[cam(0.0, [8.5, 1.7, 2.6], [8.5, 1.72, 2.4], [8.7, 1.25, -5.0], [8.7, 1.25, -5.0], lens=44)])   # from behind the open leaf: the handle and the hand that holds it in the right third, the arm running from it down the street to him
# 12: the arm stays: his bedroom: he sleeps on his back, cap on, the arm across him and out through the window; somebody uses the door: the arm twitches
#     and takes him off the bed, flat against the wall under the window; he does not wake up
WIN = [-4.7, 1.75, -0.6]                            # through the window
BED12 = [-2.6, 0.62, -1.7]                          # on the set's bed (2 m long along Z, the pillow toward -Z)
TUG = 0.5
ARM12 = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*WIN, 1, 0.05]}, **kw}
WALL12 = [-4.08, 0.3, -1.25]                        # where he ends, flat on the wall beside the window, his feet off the floor
ZZZ = lambda pos, at_, **kw: P('zzz' + kw.pop('n', ''), 'speechBubble', pos=pos, ry=90, scale=0.9, opts={'text': 'Zzz', 'w': 0.6, 'h': 0.32, 'tail': 'down', 'popAt': at_}, **kw)
st.shot('S12', 'chambre', setOpts={'poster': 'SERVICE\nPUBLIC', 'posterBg': '#2A4B9B', 'posterFg': '#F4F1E8', 'pane': '#131B3E', 'paneGlow': '#0B1230'}, actors=[act('mec', BED12, 0, 'lieBack', 'sleepy', keys=[k(-0.05, toon=ARM12(), toonDur=0), k(0.02, toon=ARM12(sq=[1.0, 1.0, 1.14], face={'jaw': 0.35}), toonDur=0.14, toonEase='inOut'), k(0.18, toon=ARM12(), toonDur=0.12, toonEase='inOut'),   # a snore: the chest comes up, goes down
            k(TUG - 0.3, toon=ARM12(wave=RIP(0.07, 1.5, 1.5)), toonDur=0.05), k(TUG - 0.25, toon=ARM12(wave=RIP(0.1, 0.2, 1.5)), toonDur=0.13),   # somebody uses the door: a ripple comes in through the window, along the arm, to him
            k(TUG - 0.12, toon=ARM12(sq=[1.03, 0.97, 1.03], wave=RIP(0.05, -0.4, 1.5)), toonDur=0.1), k(TUG, to=WALL12, dur=0.1, glide=True, ease='in', face='keep'), k(TUG, toon=ARM12(sq=[0.9, 1.2, 0.9]), toonDur=0.08),
            k(TUG + 0.1, clip='stiffStand', expr='sleepy', blend=0.02, face=90), k(TUG + 0.1, toon=ARM12(sq=[1.3, 1.0, 0.2], bend={'neck': [0, 0.22, 0, 1, None]}), toonDur=0.03),   # on the wall, flat, as he slept: straight, eyes shut, his head on one side
            k(TUG + 0.18, toon=ARM12(sq=[1.12, 1.0, 0.3], bend={'neck': [0, 0.22, 0, 1, None]}), toonDur=0.12, toonEase='outBack'),
            k(TUG + 0.36, toon=ARM12(sq=[1.12, 1.03, 0.34], bend={'neck': [0, 0.22, 0, 1, None]}, face={'jaw': 0.35}), toonDur=0.12, toonEase='inOut'), k(TUG + 0.5, toon=ARM12(sq=[1.12, 1.0, 0.3], bend={'neck': [0, 0.22, 0, 1, None]}), toonDur=0.1)])],   # and he snores on
        props=[BEARD(), CAP(), ZZZ([-2.55, 1.5, -2.55], 0.0, keys=[k(TUG - 0.05, visible=False)]), ZZZ([-4.0, 2.75, -1.95], TUG + 0.3, n='2', keys=[k(0.0, visible=False), k(TUG + 0.3, visible=True)]),
               P('pillow', 'pillow', pos=[-2.6, 0.7, -2.62], rot=[0.25, 0, 0], keys=[k(TUG, attach='mec', joint='head', offset=[0.0, 0.26, -0.13], rot=[0, 0, 0])])],   # his pillow goes with him
        fx=[{'type': 'shake', 'at': TUG + 0.1, 'dur': 0.15, 'amount': 0.025}], **NIGHTGRADE,
        cams=[cam(0.0, [3.4, 1.9, -1.65], [3.3, 1.9, -1.65], [-4.4, 1.25, -1.65], [-4.4, 1.25, -1.65], lens=44)])   # from the side of the room: he lies across the frame, the window over his feet
# 13: the door is listed as a historic monument: a bronze plaque over him; a tourist comes for a selfie with him, as with the guards, and pokes his cheek:
#     his head rocks, his eyes go to the finger; nothing else moves
PLQ = round(st.at('S13', 'L09', 4) - 0.05, 3)       # the plaque, on « monument »
BRONZE = lambda **kw: P('bronze', 'bronzePlaque', pos=[9.84, 2.62, -2.3], ry=-90, opts={'text': 'MONUMENT/HISTORIQUE', 'w': 1.3, 'h': 0.72}, **kw)   # over the heads
TOUR = [9.0, 0, -1.78]                              # beside him along the wall, shoulder to shoulder for the picture
CU13 = 1.04                                         # the cut to the two of them
SNAP13 = CU13 + 0.14                                # the picture is taken
POKES = [CU13 + 0.3, CU13 + 0.52, CU13 + 0.74]       # a finger in his cheek, three times
CHEEK = face_pt13 = [8.98, 2.0, -1.2]                # his cheek, on the tourist's side
PHONE13 = [8.55, 2.5, -2.3]                         # the phone, at arm's length: up and out on his far side (toward the camera, his arm filled the frame)
def rock(t_, i):   # his head under one poke: knocked over on its neck like a punch-bag, back past upright, his eyes on the finger
    a = 0.3 + 0.08 * i
    return [k(t_, toon=GRIP(OPEN, face={'gx': -0.9, 'gy': 0.2}, bend={'neck': [0, 0, a, 1.12, None]}), toonDur=0.04), k(t_ + 0.07, toon=GRIP(OPEN, face={'gx': -0.9, 'gy': 0.2}, bend={'neck': [0, 0, -0.5 * a, 1.05, None]}), toonDur=0.07),
            k(t_ + 0.15, toon=GRIP(OPEN, face={'gx': -0.9, 'gy': 0.2}, bend={'neck': [0, 0, 0.2 * a, 1, None]}), toonDur=0.06)]
TPOSE = lambda finger, **kw: {'hands': {'R': 'grip', 'L': 'point'}, 'reach': {'R': [PHONE13[0], PHONE13[1] - 0.08, PHONE13[2] - 0.03, 1, 0.05], 'L': finger}, 'bend': {'spine': [0, 0, -0.16, 1, None]}, **kw}
BACK13, IN13 = [8.9, 1.95, -1.52, 1, 0.16], [CHEEK[0], CHEEK[1], CHEEK[2] - 0.02, 1, 0.16]
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stiffStand', 'deadpan', keys=[HOLDK(), k(0.0, look=None), k(0.5, toon=GRIP(OPEN, face={'lid': 1}), toonDur=0.04), k(0.58, toon=GRIP(OPEN), toonDur=0.05), k(CU13 + 0.04, toon=GRIP(OPEN, face={'gx': -0.9}), toonDur=0.06)] +   # a blink; then his eyes on the man beside him
            [x for i, t_ in enumerate(POKES) for x in rock(t_, i)] + [k(POKES[2] + 0.24, toon=GRIP(OPEN, face={'gx': -0.9, 'gy': 0.2, 'browL': -0.4, 'browR': 0.6}), toonDur=0.08)]),
        act('t1', [8.6, 0, -5.2], 0, 'walk', 'happy', keys=[k(0.0, to=TOUR, dur=0.8, clip='walk', ease='out', face=-100), k(0.8, clip='stand', expr='bigGrin', blend=0.12, look=None),
            k(0.84, toon=TPOSE(BACK13, sq=[1.05, 0.93, 1.05]), toonDur=0.12, toonEase='outBack'), k(SNAP13 + 0.06, toon=TPOSE(BACK13), toonDur=0.06)] +   # the phone up at arm's length, he leans in
            [x for t_ in POKES for x in (k(t_ - 0.05, toon=TPOSE(IN13), toonDur=0.05, toonEase='in'), k(t_ + 0.08, toon=TPOSE(BACK13), toonDur=0.08))] + [k(POKES[0] + 0.02, expr='laugh')])],   # and pokes: once, twice, three times
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(1.6), CAP(), WEB(), BRONZE(scale=0.01, keys=[k(PLQ, scale=1.0, dur=0.12, ease='outBack'), k(PLQ + 0.12, squash=[1.1, 0.85, 1.0], dur=0.3), k(CU13, visible=False)]),   # (put away in the two-shot: it was cut by the frame behind them)
               P('phone', 'smartPhone', pos=[8.4, 1.2, -1.9], ry=60, scale=1.7, opts={'call': False, 'case': '#F2C230'}, keys=[k(0.0, visible=False), k(0.84, visible=True), k(0.84, to=PHONE13, dur=0.12, ease='outBack')]),
               P('pg', 'pigeon', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.62, 0.0], 'rot': [0, 1.5708, 0]}, scale=1.1, opts={'ph': 0.5})],
        fx=[{'type': 'shake', 'at': PLQ + 0.1, 'dur': 0.1, 'amount': 0.012}, {'type': 'flash', 'at': SNAP13, 'dur': 0.12}],
        cams=[cam(0.0, [4.6, 1.8, -7.0], [4.7, 1.8, -6.85], [9.2, 1.65, -2.0], [9.2, 1.65, -2.0], lens=44),   # three quarters along the shop front, as when he tried to leave
              cam(CU13, [6.1, 1.85, -1.6], [6.2, 1.85, -1.58], [9.05, 1.85, -1.45], [9.05, 1.85, -1.45], lens=44)])   # the two of them from the hips, heads in the upper half: the poke on the side of his face that we see
# 14: the arm too: close on him and his arm: a small plaque is screwed on the sleeve; the pigeon comes down from his cap to sit by it
LAND14 = 0.5
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stiffStand', 'deadpan', keys=[HOLDK(), k(0.0, look=None), k(0.22, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.7}), toonDur=0.08), k(LAND14 + 0.08, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.5, 'lid': 1}), toonDur=0.04),
            k(LAND14 + 0.16, toon=GRIP(OPEN, face={'gx': 0.9, 'gy': 0.5}), toonDur=0.05), k(0.8, toon=GRIP(OPEN, face={'browL': 0.6, 'browR': -0.4}), toonDur=0.1)])],   # his eyes go down to the plaque; a blink when the pigeon lands; then to us
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), BEARD(1.6), CAP(), WEB(),
               P('bronze2', 'bronzePlaque', pos=[8.97, 1.2, -0.6], ry=-90, rot=[0, 0, -0.5], scale=0.01, opts={'text': 'BRAS/CLASSÉ', 'w': 0.3, 'h': 0.18}, keys=[k(0.14, scale=1.0, dur=0.1, ease='outBack'), k(0.24, squash=[1.15, 0.85, 1.0], dur=0.25)]),   # on the forearm, between elbow and wrist
               P('pg', 'pigeon', pos=[8.95, 2.75, -0.2], ry=180, scale=1.15, opts={'ph': 0.5, 'flap': [0.0, LAND14 + 0.04]}, keys=[k(0.0, visible=False), k(0.24, visible=True), k(0.26, to=[9.0, 1.4, -0.7], dur=round(LAND14 - 0.26, 3), ease='out', arc=0.25), k(LAND14, squash=[1.2, 0.8, 1.2], dur=0.25)])],   # in profile, down onto his arm
        fx=[{'type': 'shake', 'at': 0.2, 'dur': 0.08, 'amount': 0.01}],
        cams=[cam(0.0, [6.6, 2.2, -1.35], [6.7, 2.2, -1.33], [9.1, 1.55, -0.8], [9.1, 1.55, -0.8], lens=44)])   # from a little above and from his side: the forearm stands against the lit doorway
# 15: yesterday a technician came by: he sets his toolbox down by the other jamb, finds a box on the wall: one big button, AUTO: he presses it
T15 = round(st.dur('S15') - 0.3, 3)                 # he presses
TECH = [9.2, 0, 1.6]
SW = [9.88, 1.4, 2.15]                              # the box on the wall, right of the door
PRESS = lambda dx, **kw: {'hands': {'L': 'point'}, 'reach': {'L': [SW[0] - dx, SW[1] - 0.05, SW[2], 1, 0.16, [0.3, -1, -0.2]]}, **kw}   # his left index on the button, the arm out behind him (his face stays on us: a look at the box showed the back of his head)
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('tech', [9.0, 0, 4.4], 180, 'walk', 'neutral', keys=[k(0.0, to=TECH, dur=0.7, clip='walk', ease='out', face=-78), k(0.7, clip='stand', blend=0.1, look=None, expr='hmm'),
            k(0.72, toon={'face': {'gx': -0.8, 'gy': -0.5}}, toonDur=0.1), k(1.02, toon={'face': {'gx': 0.95, 'eye': 0.25}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.07, toonEase='outBack'), k(1.02, expr='surprised'),   # the door, then the box that pops up behind him: with his eyes alone
            k(T15 - 0.34, expr='smug'), k(T15 - 0.34, toon=PRESS(0.32, face={'browL': 0.9, 'browR': -0.3}), toonDur=0.22, toonEase='out'),   # the arm goes back to it, one brow up: he knows
            k(T15 - 0.04, toon=PRESS(0.07, face={'browL': 0.9, 'browR': -0.3}), toonDur=0.04), k(T15 + 0.06, toon=PRESS(0.09, face={'browL': 0.9, 'lidR': 1, 'mouth': 'smirk'}), toonDur=0.06)])],   # pressed, without a look; a wink at us
        props=[DOOR(swing=[[0, OPEN]], **PUBLIC), P('box', 'toolbox', pos=[8.8, 0, 2.5], ry=-70), P('switch', 'wallSwitch', pos=SW, ry=-90, scale=0.01, opts={'at': T15, 'label': 'AUTO'}, keys=[k(0.95, scale=1.7, dur=0.12, ease='outBack')])],
        cams=[cam(0.0, [6.3, 1.45, 2.6], [6.45, 1.45, 2.55], [9.8, 1.4, 2.0], [9.8, 1.4, 2.0], lens=44)])   # right of the door: its sign stays out of the frame
# 16: it was automatic: the leaf leaves his hand: it shuts by itself, slides open; his hand stays in the air, holding nothing. Close on him: he lifts
#     the fist that holds nothing under his eyes, looks at the door, back at the fist: a squash, and the take, eyes out at it
SHUT16 = 0.18                                        # the leaf has swung shut
SLIDE16 = [[0, 0], [0.2, 0], [0.34, 0.95], [0.6, 0.95], [0.74, 0], [0.9, 0], [1.04, 0.95]]
AIR = handle(OPEN)                                  # where the handle was: his hand stays there
FREE = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*AIR, 1, 0.05, [0.2, -1, 0.5]]}, **kw}
CU16 = 0.36                                         # the cut to his face
HAND16 = [9.0, 1.5, -0.55]                          # the empty fist, lifted under his eyes (where the handle was, it sat in the caption band)
LIFT = lambda **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [*HAND16, 1, 0.05, [0.2, -1, 0.5]]}, **kw}
TAKE16 = CU16 + 0.46
POP16 = {'pop': 1.0, 'popLen': 0.2, 'eyeScale': 1.3, 'jaw': 0.9, 'eyeYaw': 0.55}   # eyes out, the pupils on the fist (to his left)
CAM16 = [7.5, 1.8, 1.3]                              # the close camera: at the take his head comes round to it
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'deadpan', keys=[k(-0.05, toon=FREE(), toonDur=0), k(0.0, look=None), k(0.06, toon=FREE(face={'gx': 0.9, 'gy': 0.3}), toonDur=0.06), k(0.1, expr='surprised'),   # his eyes alone go after the leaf
            k(CU16 + 0.02, toon=LIFT(face={'gx': 0.8, 'gy': 0.6}), toonDur=0.12, toonEase='outBack'),   # the fist comes up: he looks at what it holds
            k(CU16 + 0.2, toon=LIFT(face={'gx': 1.0, 'gy': -0.1, 'browL': 0.7}), toonDur=0.05),   # the door, behind him: with his eyes
            k(CU16 + 0.34, toon=LIFT(face={'gx': 0.8, 'gy': 0.6}), toonDur=0.05),   # the fist again
            k(TAKE16 - 0.07, toon=LIFT(sq=[1.1, 0.84, 1.1], scl={'head': [1.14, 0.84, 1]}, face={'lid': 1}), toonDur=0.05),   # a squash: he winds up
            k(TAKE16 - 0.02, expr='take', look=CAM16), k(TAKE16, toon=LIFT(sq=[0.96, 1.06, 0.96], bend={'neck': [0, 0, 0, 1.15, None]}, face=POP16), toonDur=0.06, toonEase='outBack'),   # the take: his head to us, eyes out, the pupils on the fist
            k(TAKE16 + 0.2, toon=LIFT(bend={'neck': [0, 0, 0, 1.1, None]}, face=POP16), toonDur=0.15)])],
        props=[DOOR(swing=[[0, OPEN], [0.03, OPEN], [SHUT16, 0]], slide=SLIDE16, led=0.2, **PUBLIC), BEARD(1.25, keys=[k(TAKE16, attach='mec', joint='head', offset=JAWB, rot=[0, 0, 0])]), CAP(), BRONZE(keys=[k(CU16, visible=False)])],   # the bronze plaque would sit behind his cap in the close shot: put away
        cams=[cam(0.0, [5.2, 1.7, -2.6], [5.3, 1.7, -2.5], [9.6, 1.55, -0.5], [9.6, 1.55, -0.5], lens=44),
              cam(CU16, CAM16, [7.55, 1.8, 1.2], [9.05, 1.6, -0.9], [9.05, 1.6, -0.9], lens=44)])   # from up the pavement, on his left: the dark window behind his head, no sign in the frame, the fist at mid-height
# 17: the lady never said thank you: the door slides open for her; she comes out with her bread, goes by under his nose and away; once she is past he
#     raises a finger, his mouth opens; nothing; it shuts. Then his arm: he pushes it down with the other hand, out at his side: it bows like a springboard;
#     he lets go; it stays; a sigh. It comes back up by itself, past where the handle was; the door opens for nobody. A look at it, a look at us
OUT17 = 0.25                                        # she comes out
LADY17 = [(10.5, 0.0), (8.6, 0.05), (8.2, -1.6), (7.9, -6.5)]
F17, PUSH, REL, RISE = 1.45, 2.08, 2.52, 2.86        # the finger; he pushes his arm down; he lets go; it comes back up
LOW17 = [9.02, 0.72, -0.45]                         # the hand, pushed straight down: still out at his side, over the pale door
POLE = [0.2, -1, 0.5]
ONARM = lambda y: [9.03, round(y + 0.13, 3), -0.52, 1, 0.08, [-0.3, -0.5, 0.7]]   # his other hand, flat on the forearm
EYE17 = {'gx': 0.9, 'gy': 0.5}                       # his eyes on the arm
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'surprised', keys=[k(-0.05, toon=FREE(bend={'neck': [0.25, 0, 0, 1.3, None]}, face={'pop': 0.9, 'popLen': 0.2, 'jaw': 0.8}), toonDur=0),   # still in the take:
            k(0.03, toon=FREE(sq=[1.03, 0.96, 1.03]), toonDur=0.22, toonEase='outBack'), k(0.3, look='dame'),   # it settles while the door opens
            k(F17, toon=FREE(hands={'L': 'grip', 'R': 'point'}, reach={'L': [*AIR, 1, 0.05, POLE], 'R': [8.75, 2.3, -1.5, 1, 0.16]}, sq=[0.96, 1.07, 0.96], face={'jaw': 0.6, 'brow': 0.7}), toonDur=0.12, toonEase='outBack'), k(F17, look=[8.0, 1.6, -5.0]),   # she is past: a finger, his mouth open
            k(F17 + 0.4, toon=FREE(hands={'L': 'grip', 'R': 'point'}, reach={'L': [*AIR, 1, 0.05, POLE], 'R': [8.75, 2.26, -1.5, 1, 0.16]}, face={'brow': 0.3}), toonDur=0.05),   # nothing: it shuts
            k(F17 + 0.5, toon=FREE(sq=[1.03, 0.96, 1.03]), toonDur=0.12, toonEase='inOut'), k(F17 + 0.5, expr='sad', look=None),   # the finger comes down
            k(PUSH - 0.1, toon=FREE(face=EYE17), toonDur=0.06), k(PUSH - 0.1, expr='hmm'),   # his eyes on his arm
            k(PUSH, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*AIR, 1, 0.05, POLE], 'R': ONARM(AIR[1])}, 'face': EYE17}, toonDur=0.1, toonEase='out'),   # the other hand, across, onto the forearm
            k(PUSH + 0.12, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE], 'R': ONARM(LOW17[1])}, 'bend': {'spine': [0.12, 0, -0.14, 1, None], 'foreL': [0.4, 0, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {**EYE17, 'browTilt': -10, 'mouth': 'grimace'}}, toonDur=0.16, toonEase='inOut'),   # down: the forearm bows like a springboard
            k(PUSH + 0.3, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE], 'R': ONARM(LOW17[1])}, 'bend': {'spine': [0.14, 0, -0.14, 1, None], 'foreL': [0.5, 0, 0, 1, None]}, 'wave': RIP(0.035, 1.2, 1), 'sq': [1.04, 0.95, 1.04], 'face': {**EYE17, 'browTilt': -10, 'mouth': 'grimace'}}, toonDur=0.12),   # it pushes back: held, trembling
            k(REL, toon={'hands': {'L': 'grip'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE]}, 'face': EYE17}, toonDur=0.08), k(REL + 0.06, expr='relieved', look=None),   # he lets go: it stays down
            k(REL + 0.08, toon={'hands': {'L': 'grip'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE]}, 'sq': [1.03, 0.96, 1.03], 'bend': {'spine': [0.05, 0, 0, 0.97, None]}, 'face': {'lid': 1, 'mouth': 'smile'}}, toonDur=0.14),   # a sigh, eyes shut
            k(RISE - 0.05, toon={'hands': {'L': 'grip'}, 'reach': {'L': [*LOW17, 1, 0.05, POLE]}, 'face': {**EYE17, 'eye': 0.25}}, toonDur=0.04), k(RISE - 0.05, expr='surprised'),   # his eyes go to it before it moves
            k(RISE, toon=FREE(reach={'L': [AIR[0], AIR[1] + 0.2, AIR[2], 1, 0.05, POLE]}, wave=RIP(0.1, 0.6, 1.5), sq=[0.96, 1.06, 0.96], face={**EYE17, 'eye': 0.25}), toonDur=0.07, toonEase='out'),   # it comes back up, past where the handle was
            k(RISE + 0.09, toon=FREE(wave=RIP(0.05, 1.5, 1.5), face={'gx': 0.9, 'gy': 0.3}), toonDur=0.08), k(RISE + 0.2, toon=FREE(face={'gx': 0.9, 'gy': 0.3}), toonDur=0.08),
            k(RISE + 0.28, expr='deadpan'), k(RISE + 0.28, toon=FREE(), toonDur=0.08)]),   # and at us: held to the end
        act('dame', [LADY17[0][0], 0, LADY17[0][1]], -90, 'walk', 'smug', keys=[k(0.0, visible=False), k(OUT17, visible=True), k(OUT17, to=[LADY17[1][0], 0, LADY17[1][1]], dur=0.55, clip='walk', ease='linear'),
            k(OUT17 + 0.55, to=[LADY17[2][0], 0, LADY17[2][1]], dur=0.5, clip='walk', ease='linear'), k(OUT17 + 1.05, to=[LADY17[3][0], 0, LADY17[3][1]], dur=1.5, clip='walk', ease='linear')])],
        props=[DOOR(swing=[[0, 0]], slide=[[0, 0], [0.05, 0], [0.22, 0.95], [1.0, 0.95], [1.2, 0], [RISE + 0.04, 0], [RISE + 0.2, 0.95]], led=0.0, **PUBLIC), BEARD(1.25), CAP(), BRONZE(),
               P('bread', 'baguette', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0.1, 0], 'rot': [0, 0, 1.3]}, keys=[k(0.0, visible=False), k(OUT17, visible=True)])],
        cams=[cam(0.0, [4.75, 1.65, -1.85], [4.95, 1.65, -1.75], [9.5, 1.45, -0.45], [9.5, 1.45, -0.45], lens=44)])   # a little to the right: the bronze plaque stays out of the left edge

# sound on the actions
st.cue('sfx:squeak', 'S01', O1, 0.3)
for t_ in B2: st.cue('whoosh', 'S02', t_, 0.35, 0.2, 500, 3500); st.cue('pop', 'S02', t_ + 0.12, 0.25)
st.cue('sfx:gasp', 'S03', T3 + 0.06, 0.35)
for i_, t_ in enumerate(R5): st.cue('whoosh', 'S05', t_, 0.25, 0.18, 500, 3500); st.cue('sfx:tick', 'S05', t_ + 0.06, 0.22 + 0.02 * i_)
st.cue('pop', 'S06', 0.02, 0.3); st.cue('sfx:slideUp', 'S06', 0.12, 0.3)
st.cue('pop', 'S07', 0.56, 0.3)
st.cue('clack', 'S08', P8 + 0.08, 0.45); st.cue('thud', 'S08', C8, 0.4); st.cue('sfx:boing', 'S08', UP8, 0.35)
st.cue('sfx:stretch', 'S09', GO9, 0.35); st.cue('sfx:zip', 'S09', SNAP9, 0.4); st.cue('sfx:splat', 'S09', SNAP9 + 0.09, 0.5); st.cue('sfx:squeak', 'S09', SNAP9 + 0.5, 0.3)
st.cue('whoosh', 'S10', 0.02, 0.3, 0.3, 400, 3000); st.cue('sfx:slideUp', 'S10', N10, 0.4); st.cue('sfx:boing', 'S10', N10 + 0.3, 0.3)
st.cue('sfx:stretch', 'S12', TUG - 0.1, 0.3); st.cue('sfx:zip', 'S12', TUG, 0.35); st.cue('thud', 'S12', TUG + 0.1, 0.5)
st.cue('clack', 'S13', PLQ + 0.1, 0.4); st.cue('sfx:click', 'S13', SNAP13, 0.45)
for t_ in POKES: st.cue('pop', 'S13', t_, 0.3)
st.cue('clack', 'S14', 0.2, 0.35); st.cue('sfx:poof', 'S14', LAND14, 0.25)
st.cue('sfx:tick', 'S15', T15, 0.45)
st.cue('sfx:slideUp', 'S16', 0.2, 0.3); st.cue('sfx:slideUp', 'S16', 0.6, 0.2); st.cue('sfx:boing', 'S16', TAKE16, 0.4)
st.cue('sfx:slideUp', 'S17', 0.05, 0.3); st.cue('sfx:stretch', 'S17', PUSH + 0.1, 0.3); st.cue('sfx:squeak', 'S17', PUSH + 0.3, 0.25); st.cue('sfx:spring', 'S17', RISE, 0.5); st.cue('sfx:slideUp', 'S17', RISE + 0.05, 0.3)

st.card('S12', 'LE BRAS RESTE')
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("La porte", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'dame': CITIZEN('mamie', 51, suit='#8A3A5A', glasses=False), 'agent': CITIZEN('officiel', 53, suit='#6E7A86', tie='#2F6E5C'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'remp': CITIZEN('lemec_brown', 71), 't1': CITIZEN('tourist', 73), 'tech': CITIZEN('worker', 77, glasses=False),
    **{f'r{i}': CITIZEN(['femme', 'proviseur', 'lyceen', 'madame', 'sportif', 'tourist', 'fermier', 'lyceenne'][i], 60 + i) for i in range(8)}})
