#!/usr/bin/env python3
"""La file d'attente (story 32): this man saw a queue in the street. He joined the end without knowing what for. One hour, two hours, the whole
night. Behind him the queue went all round Paris. In the morning he was first. The door opened. The lady asked: « C'est pour quoi ? » He said:
« Je ne sais pas. » She said: « Moi non plus. » So they both went to the back of the queue: it had gone round the city and ended a few metres
behind the door. Geometry: the front of the queue is at the red door (right facade, x = 10.2); the queue runs north up the right sidewalk, along
the north edge of the city, down a western avenue, round the Eiffel tower and back north up the same sidewalk, ending 8 m south of the door.
Cameras keep the front of the queue (the door side) on screen right."""
from story_kit import *

st = Story('attente')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 5)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(3, 13)])
GAP = 0.75
DOOR = [10.17, 0, -1.0]
Q1 = [[9.35, -1.0], [8.3, -0.1], [8.3, 75.0]]                                   # S01-S06: already long, running north
LOOP = [[9.35, -1.0], [8.3, -0.1], [8.3, 110.0], [-51.0, 110.0], [-51.0, -150.0], [-25.0, -150.0], [-31.0, -175.0], [-24.0, -193.0], [-8.0, -200.0],
        [7.0, -194.0], [12.0, -175.0], [12.0, -150.0], [8.3, -128.0], [8.3, -9.0]]   # round the city and the tower, back up the same sidewalk


def path_len(path): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))
def last_index(path): return math.floor(path_len(path) / GAP - 1e-9)
def spot(path, d):   # position and facing (deg, toward the front) at distance d along the path; past the end it extends the last segment
    acc = 0.0
    for (x0, z0), (x1, z1) in zip(path, path[1:]):
        seg = math.hypot(x1 - x0, z1 - z0)
        if d <= acc + seg or (x1, z1) == tuple(path[-1]):
            u = (d - acc) / seg
            return [round(x0 + (x1 - x0) * u, 3), 0, round(z0 + (z1 - z0) * u, 3)], round(math.degrees(math.atan2(x0 - x1, z0 - z1)), 1)
        acc += seg
def at_index(path, i): return spot(path, i * GAP)
def after_tail(path, k): return spot(path, (last_index(path) + k) * GAP)


L1, LL = last_index(Q1), last_index(LOOP)
TAIL, FACE_T = after_tail(Q1, 1.05)
QUEUE = lambda path, pid='queue', **o: P(pid, 'queueFigures', pos=[0, 0, 0], opts={'path': path, 'gap': GAP, 'people': True, 'size': 1.12, 'seed': 32, **o})
EXTRA = lambda aid, path, i, clip='idle', expr='neutral', **kw: act(aid, at_index(path, i)[0], at_index(path, i)[1], clip, expr, **kw)
DOORP = lambda **o: P('door', 'door', pos=DOOR, ry=-90, opts={'color': '#C8322A', 'inside': 'empty', 'hinge': 'right', **o})
MORNING = {'sky': ['#8EC5EA', '#F6D1C1']}
GOLDEN = {'sky': ['#F2A65A', '#F8D7A8']}
BUBBLE = lambda pid, text, pos, pop, ry=0, w=0.4: P(pid, 'speechBubble', pos=pos, ry=ry, opts={'text': text, 'popAt': pop, 'tail': 'down', 'w': w, 'h': w * 0.42})
WATCH = P('watch', 'wristWatch', on={'actor': 'mec', 'hand': 'L', 'offset': [0, 0.0, 0.06], 'rot': [1.5708, 0, 0]}, scale=1.6)
def facing(frm, to): return round(math.degrees(math.atan2(to[0] - frm[0], to[2] - frm[2])), 1)

# 1-3: a very long queue in the street (close on his face, then the queue to the vanishing point); he joins the end; he does not know what for
D1 = st.dur('S01'); TP1 = 0.95
st.shot('S01', 'parisStreet', actors=[act('mec', [6.45, 0, -2.4], 0, 'stand', 'awe', keys=[k(0.0, to=[6.45, 0, 0.9], dur=D1 * 0.75, clip='walk', face='keep', look=[8.3, 1.8, 3.5]), k(D1 * 0.75, clip='stand', look=[8.3, 1.8, 14.0])]),
        EXTRA('q1', Q1, 1, expr='yawn'), EXTRA('q2', Q1, 2, expr='lookSide'), EXTRA('q3', Q1, 3, expr='unimpressed')],
        props=[QUEUE(Q1, holes=[1, 2, 3]), DOORP()],
        cams=[cam(0.0, [5.75, 2.05, 3.3], [5.78, 2.05, 3.15], [6.5, 1.95, 0.2], [6.5, 1.96, 0.4], lens=44), cam(TP1, [6.25, 1.35, -5.0], [6.28, 1.38, -4.7], [7.4, 1.6, 25.0], [7.4, 1.62, 25.0], lens=44)])
D2 = st.dur('S02')
st.shot('S02', 'parisStreet', actors=[act('mec', [7.0, 0, TAIL[2] + 1.9], 160, 'stand', 'neutral', keys=[k(0.0, to=TAIL, dur=D2 * 0.75, clip='walk'), k(D2 * 0.75, clip='stand', face=FACE_T)]),
        EXTRA('qf', Q1, L1)],
        props=[QUEUE(Q1, holes=[L1]), DOORP()],
        cams=[cam(0.0, [9.9, 1.8, TAIL[2] + 2.3], [9.88, 1.8, TAIL[2] + 2.1], [7.8, 1.55, TAIL[2] - 0.3], [7.8, 1.56, TAIL[2] - 0.3], lens=44)])
st.shot('S03', 'parisStreet', actors=[act('mec', TAIL, FACE_T, 'shrug', 'confused'), EXTRA('qf', Q1, L1, expr='lookSide')], props=[QUEUE(Q1, holes=[L1]), DOORP()],
        cams=[cam(0.0, [9.9, 1.95, TAIL[2] - 0.95], [9.85, 1.95, TAIL[2] - 0.85], [8.3, 1.9, TAIL[2]], [8.3, 1.91, TAIL[2]], lens=44)])
# 4-6: one hour (watch + a sweeping clock); two hours (golden light, a pigeon on his head, people behind him); the whole night (asleep standing)
CAM4 = [9.85, 1.95, TAIL[2] - 1.35]; LOOK4 = [8.35, 1.95, TAIL[2] + 0.1]
def _onscreen(cam_, look, d, sx, sy):
    f = [look[i] - cam_[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    r = [-f[2], 0.0, f[0]]; n = math.sqrt(r[0] ** 2 + r[2] ** 2); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return [round(cam_[i] + d * (f[i] + 0.2272 * sx * r[i] + 0.4040 * sy * u[i]), 3) for i in range(3)]
CLOCK4 = _onscreen(CAM4, LOOK4, 1.1, -0.58, 0.52)
st.shot('S04', 'parisStreet', actors=[act('mec', TAIL, FACE_T, 'checkWatch', 'eyeRoll'), EXTRA('qf', Q1, L1, expr='yawn')],
        props=[QUEUE(Q1, holes=[L1]), DOORP(), WATCH, P('clock', 'clockCard', pos=CLOCK4, ry=facing(CLOCK4, CAM4), opts={'r': 0.085, 'popAt': 0.2, 'spin': 1.2})],
        cams=[cam(0.0, CAM4, [CAM4[0] - 0.03, CAM4[1], CAM4[2] + 0.12], [8.35, 1.95, TAIL[2] + 0.1], [8.35, 1.96, TAIL[2] + 0.1], lens=44)])
HEADTOP = [TAIL[0], 2.2, TAIL[2]]
B1, FB = after_tail(Q1, 2.1); B2, _ = after_tail(Q1, 3.15)
BEHIND = [[TAIL[0], TAIL[2] + 2.4], [TAIL[0], TAIL[2] + 7.0]]
st.shot('S05', 'parisStreet', setOpts=GOLDEN, actors=[act('mec', TAIL, FACE_T, 'stand', 'lookUp'), act('pigeon', HEADTOP, 150, 'idle', 'neutral', scale=0.8), EXTRA('qf', Q1, L1, expr='sleepy'),
        act('qb1', B1, FB, 'idle', 'nervous'), act('qb2', B2, FB, 'readPhone', 'lookDown')],
        props=[QUEUE(Q1, holes=[L1]), QUEUE(BEHIND, 'queue2', seed=33), DOORP()],
        cams=[cam(0.0, [9.75, 1.6, TAIL[2] - 2.2], [9.7, 1.62, TAIL[2] - 2.05], [8.3, 2.0, TAIL[2] + 0.5], [8.3, 2.02, TAIL[2] + 0.5], lens=44)])
st.shot('S06', 'parisStreet', setOpts={'night': True}, actors=[act('mec', TAIL, FACE_T, 'stand', 'drool'), act('pigeon', HEADTOP, 150, 'sleep', 'neutral', scale=0.8), EXTRA('qf', Q1, L1, expr='sleepy'),
        act('qb1', B1, FB, 'idle', 'yawn'), act('qb2', B2, FB, 'idle', 'drool')],
        props=[QUEUE(Q1, holes=[L1]), QUEUE([[TAIL[0], TAIL[2] + 2.4], [TAIL[0], 110.0], [-20.0, 110.0]], 'queue2', seed=34), DOORP()],
        cams=[cam(0.0, [9.8, 1.35, TAIL[2] - 2.3], [9.76, 1.37, TAIL[2] - 2.15], [8.3, 1.85, TAIL[2] + 0.6], [8.3, 1.87, TAIL[2] + 0.6], lens=44)])
# 7: behind him the queue went round Paris (low on him with the queue behind, then a fast crane up over the city: a red ribbon of people round it)
CITY = P('city', 'cityBlocks', pos=[0, 0, 0], opts={'x0': -402, 'x1': 420, 'z0': -657, 'z1': 460, 'skip': [[-21, 21, -128, 120]], 'park': [-46, 32, -222, -132]})
LOW7 = [6.4, 1.9, TAIL[2] - 3.6]; LOOK7 = [8.1, 1.85, TAIL[2] + 4.0]
st.shot('S07', 'parisStreet', setOpts=MORNING, actors=[act('mec', TAIL, FACE_T, 'stand', 'yawn'), EXTRA('qf', Q1, L1), act('qb1', B1, FB, 'idle', 'neutral'), act('qb2', B2, FB, 'idle', 'neutral')],
        props=[QUEUE(LOOP, max=1000, size=2.2, holes=[L1], ribbon={'color': '#D7262E', 'width': 4.5}), DOORP(), CITY],
        cams=[cam(0.0, LOW7, [LOW7[0], LOW7[1] + 0.1, LOW7[2] - 0.2], LOOK7, LOOK7, lens=44), cam(0.6, [LOW7[0], LOW7[1] + 0.1, LOW7[2] - 0.2], [-16.0, 370.0, -165.0], LOOK7, [-20.0, 0.0, -45.0], lens=44, ease='inOut')], far=1600)
# 8-12: in the morning he is first (the whole red door in frame, the queue behind him to the vanishing point); the door opens on « ouverte » onto an empty lit cupboard
FRONT, _ = at_index(LOOP, 0); DAME = [9.95, 0, -1.0]
EX8 = [EXTRA('q1', LOOP, 1, expr='lookSide'), EXTRA('q2', LOOP, 2, expr='yawn')]
st.shot('S08', 'parisStreet', setOpts=MORNING, actors=[act('mec', FRONT, 90, 'handsOnHips', 'proud', keys=[k(0.0, look=[9.6, 1.6, -7.5])]), *EX8], props=[QUEUE(LOOP, skip=1, holes=[1, 2], max=1000), DOORP()],
        cams=[cam(0.0, [9.6, 1.5, -7.6], [9.55, 1.52, -6.6], [9.0, 1.7, 6.0], [9.0, 1.72, 6.0], lens=44)])
T9 = st.at('S09', 'L08', 3) - 0.3
st.shot('S09', 'parisStreet', actors=[act('mec', FRONT, 90, 'stand', 'neutral'), act('dame', DAME, -90, 'stand', 'neutral', visible=False, keys=[k(T9 + 0.22, visible=True)]), *EX8],
        props=[QUEUE(LOOP, skip=1, holes=[1, 2], max=1000), DOORP(openAt=T9)],
        cams=[cam(0.0, [8.15, 2.15, -2.45], [8.25, 2.12, -2.3], [10.1, 1.5, -0.85], [10.1, 1.52, -0.9], lens=44)])
T10 = st.at('S10', 'L09', 3); CAM10 = [8.9, 1.98, -2.35]; BUB10 = [9.86, 2.33, -1.12]
st.shot('S10', 'parisStreet', actors=[act('mec', FRONT, 90, 'stand', 'neutral'), act('dame', DAME, -90, 'talk', 'squint'), *EX8],
        props=[QUEUE(LOOP, skip=1, holes=[1, 2], max=1000), DOORP(open=1), BUBBLE('b1', "C'EST POUR QUOI ?", BUB10, T10, ry=facing(BUB10, CAM10), w=0.36)],
        cams=[cam(0.0, CAM10, [CAM10[0] + 0.16, CAM10[1], CAM10[2] + 0.2], [9.95, 1.95, -1.0], [9.95, 1.96, -1.0], lens=44)])
T11 = st.at('S11', 'L10', 3); CAM11 = [10.0, 2.0, 1.25]; BUB11 = [9.12, 2.52, -0.92]
st.shot('S11', 'parisStreet', actors=[act('mec', FRONT, 45, 'shrug', 'confused'), act('dame', DAME, -90, 'stand', 'neutral'), *EX8],
        props=[QUEUE(LOOP, skip=1, holes=[1, 2], max=1000), DOORP(open=1), BUBBLE('b2', 'JE NE SAIS PAS.', BUB11, T11, ry=facing(BUB11, CAM11), w=0.5)],
        cams=[cam(0.0, CAM11, [9.96, 2.0, 1.0], [9.35, 1.95, -1.0], [9.35, 1.96, -1.0], lens=44)])
T12 = st.at('S12', 'L11', 3); CAM12 = [8.65, 1.95, -2.45]; BUB12 = [9.8, 2.25, -1.18]
st.shot('S12', 'parisStreet', actors=[act('mec', FRONT, 90, 'stand', 'neutral'), act('dame', DAME, -90, 'shrug', 'eyeRoll'), *EX8],
        props=[QUEUE(LOOP, skip=1, holes=[1, 2], max=1000), DOORP(open=1), BUBBLE('b3', 'MOI NON PLUS.', BUB12, T12, ry=facing(BUB12, CAM12), w=0.4)],
        cams=[cam(0.0, CAM12, [CAM12[0] + 0.25, CAM12[1], CAM12[2] + 0.32], [9.95, 1.85, -1.0], [9.95, 1.86, -1.0], lens=44)])
# 13: so they went to the back of the queue: it ends a few metres behind the door (low behind them, the queue to the tower; the crane reveals the door)
END_MEC, FACE_E = after_tail(LOOP, 1.05); END_DAME, _ = after_tail(LOOP, 2.1)
CLK13 = [END_MEC[0] + 0.15, 2.6, END_MEC[2]]
st.shot('S13', 'parisStreet', actors=[act('mec', [6.6, 0, END_MEC[2] + 2.6], 150, 'stand', 'neutral', keys=[k(0.0, to=END_MEC, dur=0.9, clip='walk'), k(0.95, clip='stand', face=FACE_E), k(1.45, clip='checkWatch', expr='eyeRoll')]),
        act('dame', [6.4, 0, END_DAME[2] + 2.9], 150, 'stand', 'neutral', keys=[k(0.15, to=END_DAME, dur=0.9, clip='walk'), k(1.1, clip='stand', face=FACE_E)]), EXTRA('qt', LOOP, LL, expr='lookSide'), *EX8],
        props=[QUEUE(LOOP, skip=1, holes=[1, 2, LL], max=1000), DOORP(open=1), WATCH, P('clock', 'clockCard', pos=CLK13, ry=0, opts={'r': 0.22, 'popAt': 1.5, 'spin': 1.2})],
        cams=[cam(0.0, [6.8, 1.45, -1.6], [6.82, 1.47, -1.9], [8.3, 1.4, -26.0], [8.3, 1.42, -26.0], lens=44), cam(1.55, [6.82, 1.47, -1.9], [6.3, 11.5, 9.5], [8.3, 1.42, -26.0], [10.2, 0.0, -10.0], lens=44, ease='inOut')])
st.card('S04', 'UNE HEURE'); st.card('S06', 'TOUTE LA NUIT'); st.card('S07', 'TOUT PARIS')
st.cue('sfx:step', 'S01', 0.2, 0.25); st.cue('sfx:step', 'S02', 0.1, 0.25); st.cue('sfx:tick', 'S04', 0.3, 0.35); st.cue('sfx:ticks', 'S05', 0.1, 0.25); st.cue('sfx:bell', 'S08', 0.05, 0.3)
st.cue('sfx:squeak', 'S09', T9, 0.35); st.cue('sfx:step', 'S13', 0.15, 0.25); st.cue('sfx:tick', 'S13', 1.5, 0.3)
st.write("La file d'attente", {'dame': {'preset': 'madame', 'seed': 105, 'suit': '#7A5C8E'}, 'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 2}},
                               'q1': {'preset': 'boss', 'seed': 141, 'suit': '#D9A441'}, 'q2': {'preset': 'madame', 'seed': 142, 'suit': '#4F9FB0'}, 'q3': {'preset': 'tourist', 'seed': 143},
                               'qf': {'preset': 'boss', 'seed': 144, 'suit': '#3E7D5A'}, 'qb1': {'preset': 'madame', 'seed': 145, 'suit': '#E07A5F'}, 'qb2': {'preset': 'worker', 'seed': 146},
                               'qt': {'preset': 'politique', 'seed': 147}})
