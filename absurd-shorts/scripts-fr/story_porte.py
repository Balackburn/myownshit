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
DOOR = lambda **kw: P('door', 'shopDoor', pos=[DX, 0, DZ], ry=-90, opts={'w': DW, 'h': 2.5, 'signW': 1.9, **kw})
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
B2 = [0.12, 0.42, 0.72]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(0.0, look=[5.5, 1.6, 0.3]), k(B2[0] + 0.1, look=[9.9, 1.6, 0.0]), k(B2[1], look=[5.5, 1.6, 0.3], expr='unimpressed'), k(B2[1] + 0.1, look=[9.9, 1.6, 0.0]),
            k(B2[2], look=[5.5, 1.6, 0.3]), k(B2[2] + 0.1, look=[9.9, 1.6, 0.0]), k(0.9, look=None, expr='deadpan')])] + [rusher(i, t) for i, t in enumerate(B2)],
        props=[DOOR(swing=[[0, OPEN]]),
               P('beard', 'beard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.03, 0.09], 'rot': [0, 0, 0]}, scale=0.01, opts={'color': '#17161A'},
                 keys=[k(B2[0] + 0.12, scale=0.5, dur=0.1, ease='outBack'), k(B2[1] + 0.12, scale=0.85, dur=0.1, ease='outBack'), k(B2[2] + 0.12, scale=1.25, dur=0.1, ease='outBack')]),
               P('web', 'spiderWeb', pos=[9.02, 1.42, -0.7], ry=-90, scale=0.01, opts={'r': 0.3}, keys=[k(B2[2] + 0.05, scale=1.0, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [5.7, 1.85, -0.2], [5.9, 1.85, -0.3], [9.3, 1.7, -0.75], [9.3, 1.7, -0.75], lens=44)])
# 3: behind her there was... he turns his head to the pavement: a queue to the horizon; his face whips back to us, eyes out
QUEUE = lambda **kw: P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[7.7, 1.6], [7.5, 190.0]], 'gap': 0.8, 'people': True, 'seed': 9, **kw})
T3 = 0.55                                           # the take
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK(), k(-0.3, look=[7.6, 1.6, 12.0]), k(T3, look=None, expr='take'),
            k(T3, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.8, 'popLen': 0.14}, sq=[0.92, 1.14, 0.92], hat=[0.2, 0, 0]), toonDur=0.07, toonEase='outBack'), k(T3 + 0.4, toon=GRIP(OPEN, face={'pop': 0.75, 'jaw': 0.8, 'popLen': 0.14}), toonDur=0.1)])],
        props=[DOOR(swing=[[0, OPEN]]), QUEUE()],
        cams=[cam(0.0, [10.4, 1.95, -3.6], [10.2, 1.95, -3.3], [8.3, 1.75, 2.0], [8.3, 1.75, 2.0], lens=44)])
# 4: ...the town: from above, the queue runs down the street out of sight
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[act('mec', HOLD, -90, 'stand', 'neutral', keys=[HOLDK()])],
        props=[DOOR(swing=[[0, OPEN]]), QUEUE()],
        cams=[cam(0.0, [5.5, 9.0, -9.0], [5.6, 10.5, -11.0], [7.6, 1.0, 14.0], [7.6, 1.0, 18.0], lens=44)])

st.write("La porte", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'dame': {'preset': 'mamie', 'seed': 51, 'build': {'width': 0.86, 'headWidth': 1.3}, 'suit': '#8A3A5A', 'glasses': False}})
