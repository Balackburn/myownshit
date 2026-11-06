#!/usr/bin/env python3
"""La file d'attente (story 32): this man saw a queue in the street. He joined the end without knowing what for. One hour, two hours, the whole
night. Behind him the queue went all round Paris. In the morning he was first. The door opened. The lady asked: « C'est pour quoi ? » He said:
« Je ne sais pas. » She said: « Moi non plus. » So they both went to the back of the queue."""
from story_kit import *

st = Story('attente')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 5)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(3, 13)])
GAP = 0.75
DOOR = [10.17, 0, -1.0]                                  # a red door in the right-hand facade (facade plane x = 10.2), facing the street
Q_SHORT = [[9.35, -1.0], [8.3, -1.9], [8.3, -30.0]]     # S01-S06: the front person faces the door
Q_LONG = [[9.35, -1.0], [8.3, -1.9], [8.3, -150.0], [12.0, -175.0], [7.0, -194.0], [-8.0, -200.0], [-24.0, -193.0], [-31.0, -175.0], [-25.0, -158.0], [-14.0, -152.0]]   # round the Eiffel tower


def path_len(path): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))
def after_tail(path, k):   # the spot k places behind the last figure of a queue drawn every GAP along path (what queueFigures does), and the facing (deg) toward the front
    L = path_len(path); d = math.floor(L / GAP - 1e-9) * GAP + k * GAP
    (x0, z0), (x1, z1) = path[-2], path[-1]; seg = math.hypot(x1 - x0, z1 - z0); u = ((x1 - x0) / seg, (z1 - z0) / seg)
    back = d - L
    return [round(x1 + u[0] * back, 3), 0, round(z1 + u[1] * back, 3)], round(math.degrees(math.atan2(-u[0], -u[1])), 1)


TAIL, _ = after_tail(Q_SHORT, 1.05)                       # where he joins: one gap behind the 40th person
QUEUE = lambda path, pid='queue', **o: P(pid, 'queueFigures', pos=[0, 0, 0], opts={'path': path, 'gap': GAP, 'people': True, 'size': 1.12, 'seed': 32, **o})
DOORP = lambda **o: P('door', 'door', pos=DOOR, ry=-90, opts={'color': '#C8322A', **o})
MORNING = {'sky': ['#8EC5EA', '#F6D1C1']}
WATCH = P('watch', 'wristWatch', on={'actor': 'mec', 'hand': 'L', 'offset': [0, 0.0, 0.06], 'rot': [1.5708, 0, 0]}, scale=1.6)
GOLDEN = {'sky': ['#F2A65A', '#F8D7A8']}
BUBBLE = lambda pid, text, pos, pop, ry=0, w=0.95: P(pid, 'speechBubble', pos=pos, ry=ry, opts={'text': text, 'popAt': pop, 'tail': 'down', 'w': w, 'h': w * 0.42})

# 1-3: a queue in the street; he joins the end; he does not know what for
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', actors=[act('mec', [6.45, 0, -5.9], 0, 'stand', 'suspicious', keys=[k(0.0, to=[6.45, 0, -1.5], dur=D1 * 0.8, clip='walk', face='keep', look=[8.3, 1.8, -9.0]), k(D1 * 0.8, clip='stand', look=[8.3, 1.8, -14.0])])],
        props=[QUEUE(Q_SHORT), DOORP()],
        cams=[cam(0.0, [6.15, 1.3, 3.3], [6.2, 1.32, 3.0], [7.5, 1.5, -12.0], [7.5, 1.5, -12.0], lens=44)])
D2 = st.dur('S02')
st.shot('S02', 'parisStreet', actors=[act('mec', [6.9, 0, -32.2], 40, 'stand', 'neutral', keys=[k(0.0, to=TAIL, dur=D2 * 0.75, clip='walk'), k(D2 * 0.75, clip='stand', face=0)])],
        props=[QUEUE(Q_SHORT), DOORP()],
        cams=[cam(0.0, [6.35, 1.65, -27.9], [6.42, 1.65, -28.1], [8.2, 1.5, -31.0], [8.25, 1.5, -31.0], lens=44)])
st.shot('S03', 'parisStreet', actors=[act('mec', TAIL, 0, 'shrug', 'unimpressed')], props=[QUEUE(Q_SHORT), DOORP()],
        cams=[cam(0.0, [6.9, 1.95, -28.35], [6.97, 1.95, -28.5], [8.3, 1.85, -30.6], [8.3, 1.86, -30.6], lens=44)])
# 4-6: one hour (watch); two hours (golden light, a pigeon on his head, people behind him); the whole night (asleep standing, lamps lit)
st.shot('S04', 'parisStreet', actors=[act('mec', TAIL, 0, 'checkWatch', 'unimpressed')], props=[QUEUE(Q_SHORT), DOORP(), WATCH],
        cams=[cam(0.0, [9.75, 1.8, -28.55], [9.7, 1.8, -28.75], [8.3, 1.7, -30.6], [8.3, 1.7, -30.6], lens=44)])
HEADTOP = [TAIL[0], 2.2, TAIL[2]]
BEHIND = [[TAIL[0], TAIL[2] - 0.8], [TAIL[0], TAIL[2] - 3.2]]
st.shot('S05', 'parisStreet', setOpts=GOLDEN, actors=[act('mec', TAIL, 0, 'stand', 'unimpressed'), act('pigeon', HEADTOP, 35, 'idle', 'neutral', scale=0.8)],
        props=[QUEUE(Q_SHORT), QUEUE(BEHIND, 'queue2', seed=33), DOORP()],
        cams=[cam(0.0, [9.6, 1.6, -28.2], [9.55, 1.62, -28.4], [8.3, 2.0, -30.6], [8.3, 2.02, -30.6], lens=44)])
st.shot('S06', 'parisStreet', setOpts={'night': True}, actors=[act('mec', TAIL, 0, 'stand', 'sleepy'), act('pigeon', HEADTOP, 35, 'sleep', 'neutral', scale=0.8)],
        props=[QUEUE(Q_SHORT), QUEUE([[TAIL[0], TAIL[2] - 0.8], [TAIL[0], TAIL[2] - 40.0]], 'queue2', seed=34), DOORP()],
        cams=[cam(0.0, [9.8, 1.3, -28.3], [9.76, 1.32, -28.5], [8.3, 1.95, -31.0], [8.3, 1.97, -31.0], lens=44)])
# 7: behind him the queue went round Paris (aerial, morning: the line runs down the street to the Eiffel tower and round it)
CITY = P('city', 'cityBlocks', pos=[0, 0, 0], opts={'x0': -142, 'x1': 150, 'z0': -330, 'z1': 90, 'skip': [[-21, 21, -128, 120]], 'park': [-46, 32, -222, -132]})
st.shot('S07', 'parisStreet', setOpts=MORNING, props=[QUEUE(Q_LONG, max=400, size=1.8), DOORP(), CITY],
        cams=[cam(0.0, [40.0, 72.0, -96.0], [46.0, 86.0, -88.0], [-6.0, 0.0, -168.0], [-6.0, 0.0, -171.0], lens=44, ease='inOut')])
# 8-12: in the morning he is first; the door opens; « C'est pour quoi ? »; « Je ne sais pas. »; « Moi non plus. »
FRONT = [9.35, 0, -1.0]; DAME = [9.95, 0, -1.0]
st.shot('S08', 'parisStreet', setOpts=MORNING, actors=[act('mec', FRONT, 90, 'handsOnHips', 'smug', keys=[k(0.0, look=[6.4, 1.6, 2.4])])], props=[QUEUE(Q_LONG, skip=1, max=400), DOORP()],
        cams=[cam(0.0, [6.6, 1.5, 3.0], [6.66, 1.52, 2.8], [9.45, 1.7, -1.6], [9.45, 1.72, -1.6], lens=44)])
T9 = 0.12
st.shot('S09', 'parisStreet', setOpts=MORNING, actors=[act('mec', FRONT, 90, 'stand', 'neutral'), act('dame', DAME, -90, 'stand', 'neutral', visible=False, keys=[k(T9 + 0.22, visible=True)])],
        props=[QUEUE(Q_LONG, skip=1, max=400), DOORP(openAt=T9)],
        cams=[cam(0.0, [8.0, 2.15, 0.25], [8.06, 2.14, 0.12], [10.1, 1.5, -1.0], [10.1, 1.52, -1.0], lens=44)])
T10 = st.at('S10', 'L09', 3)
st.shot('S10', 'parisStreet', setOpts=MORNING, actors=[act('mec', FRONT, 90, 'stand', 'neutral'), act('dame', DAME, -90, 'talk', 'suspicious')],
        props=[QUEUE(Q_LONG, skip=1, max=400), DOORP(open=1), BUBBLE('b1', "C'EST POUR QUOI ?", [9.78, 2.32, -0.9], T10, ry=-51, w=0.36)],
        cams=[cam(0.0, [8.7, 1.98, -0.25], [8.76, 1.98, -0.33], [9.95, 1.95, -1.0], [9.95, 1.96, -1.0], lens=44)])
T11 = st.at('S11', 'L10', 3)
st.shot('S11', 'parisStreet', setOpts=MORNING, actors=[act('mec', FRONT, 45, 'shrug', 'neutral'), act('dame', DAME, -90, 'stand', 'neutral')],
        props=[QUEUE(Q_LONG, skip=1, max=400), DOORP(open=1), BUBBLE('b2', 'JE NE SAIS PAS.', [9.15, 2.52, -0.94], T11, ry=23, w=0.5)],
        cams=[cam(0.0, [10.0, 2.0, 1.25], [9.98, 2.0, 1.05], [9.35, 1.95, -1.0], [9.35, 1.96, -1.0], lens=44)])
T12 = st.at('S12', 'L11', 3)
st.shot('S12', 'parisStreet', setOpts=MORNING, actors=[act('mec', FRONT, 90, 'stand', 'neutral'), act('dame', DAME, -90, 'shrug', 'unimpressed')],
        props=[QUEUE(Q_LONG, skip=1, max=400), DOORP(open=1), BUBBLE('b3', 'MOI NON PLUS.', [9.8, 2.32, -0.92], T12, ry=-42.5, w=0.4)],
        cams=[cam(0.0, [8.6, 1.92, 0.15], [8.66, 1.92, 0.05], [9.95, 1.82, -1.0], [9.95, 1.83, -1.0], lens=44)])
# 13: so they both went to the back of the queue (by the Eiffel tower: he checks his watch again)
END_MEC, FACE13 = after_tail(Q_LONG, 1.05)
END_DAME, _ = after_tail(Q_LONG, 2.1)
U13 = [(Q_LONG[-1][0] - Q_LONG[-2][0]), (Q_LONG[-1][1] - Q_LONG[-2][1])]; n = math.hypot(*U13); U13 = [U13[0] / n, U13[1] / n]
SIDE = [-U13[1], U13[0]]
D13 = st.dur('S13')
def off(p, a, b): return [round(p[0] + a * U13[0] + b * SIDE[0], 3), 0, round(p[2] + a * U13[1] + b * SIDE[1], 3)]
CAM13 = off(END_MEC, -2.3, 4.4); LOOKP = off(END_MEC, 0.05, 0.0)
st.shot('S13', 'parisStreet', setOpts=MORNING, actors=[act('mec', off(END_MEC, 0, 2.2), FACE13, 'stand', 'neutral', keys=[k(0.0, to=END_MEC, dur=0.9, clip='walk'), k(0.95, clip='stand', face=FACE13), k(1.5, clip='checkWatch', expr='unimpressed')]),
        act('dame', off(END_DAME, 0, 2.2), FACE13, 'stand', 'neutral', keys=[k(0.1, to=END_DAME, dur=0.9, clip='walk'), k(1.05, clip='stand', face=FACE13)])],
        props=[QUEUE(Q_LONG, max=400), WATCH],
        cams=[cam(0.0, [CAM13[0], 1.7, CAM13[2]], [CAM13[0] + 0.3 * U13[0], 1.72, CAM13[2] + 0.3 * U13[1]], [LOOKP[0], 1.45, LOOKP[2]], [LOOKP[0], 1.5, LOOKP[2]], lens=44)])
st.card('S04', 'UNE HEURE'); st.card('S06', 'TOUTE LA NUIT'); st.card('S07', 'TOUT PARIS')
st.cue('sfx:step', 'S01', 0.2, 0.25); st.cue('sfx:step', 'S02', 0.1, 0.25); st.cue('sfx:tick', 'S04', 0.3, 0.35); st.cue('sfx:ticks', 'S05', 0.1, 0.25); st.cue('sfx:bell', 'S08', 0.05, 0.3)
st.cue('sfx:squeak', 'S09', T9, 0.35); st.cue('sfx:step', 'S13', 0.15, 0.25); st.cue('sfx:tick', 'S13', 1.55, 0.3)
st.write("La file d'attente", {'dame': {'preset': 'madame', 'seed': 105, 'suit': '#7A5C8E'}, 'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 2}}})
