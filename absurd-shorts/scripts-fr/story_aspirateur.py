#!/usr/bin/env python3
"""L'aspirateur (story 28): this man bought a robot vacuum. Day one it sucked up the dust; day two the socks; day three the cat
(the cat is fine). Then the sofa, the house, the neighbourhood. The town hall filed a complaint: it sucked up the town hall. The
army sent the tanks: it sucked up the tanks. Then it went back to its base. Low battery. Tonight the man has to empty it.

Round 2 (critic round 1: strategist 6.0, art director 6.5): the hook shows his face and the new robot held at chest height; S02 is
a power-on (dark eyes flicker on, brushes start, a hop and a turn); each day is a set-up shot then the suck on the noun (a small
grey dust ball, white socks with navy stripes); the cat faces the camera and is pulled backwards while he watches, kneeling; a
mustard sofa; the mayor marches with PLAINTE at chest height and his tricolour sash; faces and tanks out of the caption band; the
low-battery shot is centred with a battery icon; the payoff tips the robot over an open bin and the callbacks fall out in story
order before the cat pops out."""
from story_kit import *

st = Story('aspirateur')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4), ('S03', 'L02', 0), ('S04', 'L02', 3), ('S05', 'L03', 0), ('S06', 'L03', 3)]
        + [(f'S{i + 3:02d}', f'L{i:02d}', 0) for i in range(4, 16)])
PI = math.pi
LR = {'sofa': False, 'tv': False}
VAC = lambda pos=(0, 0, -1.0), ry=0, scale=1.0, keys=None, **o: P('vac', 'robotVacuum', pos=list(pos), ry=ry, scale=scale, opts=o, **({'keys': keys} if keys else {}))
LOWCAM = lambda x=0.0, z=-1.0, d=0.95, h=0.24, lens=44: [cam(0.0, [x + 0.1, h, z + d], [x + 0.09, h, z + d - 0.1], [x, 0.08, z], [x, 0.08, z], lens=lens)]
# an object pulled into a mouth: moves p0 -> p1 and shrinks s0 -> s1 from t0 over dur, then hides; spin: an absolute end rotation (radians)
INTO = lambda pid, name, p0, p1, t0, dur, s0=1.0, s1=0.05, spin=None, **kw: P(pid, name, pos=list(p0), scale=s0, keys=[k(t0, to=list(p1), dur=dur, ease='in'), k(t0, scale=s1, dur=dur, ease='in'), k(t0 + dur, visible=False)] + ([k(t0, rotTo=spin, dur=dur, ease='in')] if spin else []), **kw)
SOFA = {'color': '#D9A43A', 'color2': '#EBC362'}     # mustard: stands off the teal wainscot

# 1-2: the hook: he shows off his new robot (switched off), then it powers on
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.3], 0, 'carry', 'smug')],
        props=[P('vac', 'robotVacuum', pos=[0.0, 1.27, -0.86], rot=[0.6, 0, 0], opts={'onAt': 99})],
        cams=[cam(0.0, [0.12, 1.6, 1.1], [0.11, 1.59, 0.95], [0.0, 1.35, -1.3], [0.0, 1.35, -1.3], lens=44)])
T_ON, T_HOP = st.at('S02', 'L01', 5) - 0.05, st.at('S02', 'L01', 6) - 0.12
st.shot('S02', 'livingRoom', setOpts=LR, props=[VAC((0, 0, -1.0), 28, mood='happy', onAt=T_ON, hopAt=T_HOP, keys=[k(T_HOP, rotTo=[0, 0, 0], dur=0.3, ease='out')])],
        cams=[cam(0.0, [0.08, 0.2, -0.08], [0.07, 0.2, -0.16], [0.0, 0.07, -1.0], [0.0, 0.07, -1.0], lens=44)])
# 3-6: day one, the dust (a small grey ball); day two, the socks
D3 = st.dur('S03')
st.shot('S03', 'livingRoom', setOpts=LR, props=[P('dock', 'chargingDock', pos=[-0.3, 0, -1.72]), P('dust3', 'dustBunny', pos=[0.32, 0, -0.78]),
        VAC((-0.3, 0, -1.56), 0, mood='happy', keys=[k(0.05, to=[0.08, 0, -1.08], dur=D3 - 0.05, ease='inOut'), k(0.35, rotTo=[0, math.radians(38), 0], dur=0.5)])],
        cams=[cam(0.0, [1.05, 0.8, 0.15], [1.0, 0.77, 0.05], [-0.05, 0.05, -1.25], [0.02, 0.05, -1.2], lens=44)])
T4 = st.at('S04', 'L02', 7)     # « poussière »
st.shot('S04', 'livingRoom', setOpts=LR, props=[VAC((0, 0, -0.98), 0, mood='happy', suckAt=0.15, keys=[k(0.0, to=[0, 0, -0.92], dur=st.dur('S04'), ease='linear')]),
        INTO('dust', 'dustBunny', (0.03, 0, -0.66), (0.0, 0.02, -0.76), T4 - 0.3, 0.42, 1.0, 0.1)],
        cams=[cam(0.0, [0.07, 0.14, 0.1], [0.065, 0.135, 0.02], [0.0, 0.05, -0.9], [0.0, 0.05, -0.9], lens=44)])
D5, SOCKS0 = st.dur('S05'), (0.02, 0, -0.62)
st.shot('S05', 'livingRoom', setOpts=LR, props=[P('socks', 'sockPair', pos=list(SOCKS0), ry=20, scale=1.6), VAC((0.0, 0, -1.42), 0, mood='happy', keys=[k(0.0, to=[0.0, 0, -1.02], dur=D5, ease='out')])],
        cams=[cam(0.0, [0.05, 1.75, -0.48], [0.05, 1.7, -0.52], [0.0, 0.0, -0.95], [0.0, 0.0, -0.95], lens=44)])
st.shot('S06', 'livingRoom', setOpts=LR, props=[VAC((0.0, 0, -1.02), 0, mood='happy', suckAt=0.0), INTO('socks', 'sockPair', SOCKS0, (0.0, 0.05, -0.84), 0.08, 0.5, 1.6, 0.12, spin=[1.4, 2.2, 0.6], ry=20)],
        cams=[cam(0.0, [0.62, 0.32, -0.2], [0.6, 0.31, -0.28], [0.0, 0.08, -0.85], [0.0, 0.08, -0.85], lens=44)])
# 7-8: day three, the cat (faces the camera, pulled backwards, scrabbling; he watches, sitting on the floor); the cat is fine
T7, MOUTH7 = st.at('S07', 'L04', 4), (-0.09, 0.03, -0.8)     # « chat »
st.shot('S07', 'livingRoom', setOpts=LR,
        actors=[act('chat', [0.12, 0, -0.55], 0, 'sit', 'happy', scale=0.55, keys=[k(T7 - 0.3, expr='scared'), k(T7 - 0.15, to=list(MOUTH7), dur=0.5, glide=True, face='keep', ease='in', clip='run'),
                                                                   k(T7 - 0.15, scale=0.07, dur=0.5, ease='in'), k(T7 + 0.36, visible=False)]),
                act('mec', [0.3, 0, -1.5], -10, 'sitFloor', 'happy', keys=[k(T7 - 0.05, expr='shocked')])],
        props=[VAC((-0.17, 0, -0.95), 25, mood='menace', suckAt=T7 - 0.35)],
        cams=[cam(0.0, [0.2, 0.35, 1.75], [0.195, 0.35, 1.68], [0.05, 0.45, -1.0], [0.05, 0.45, -1.0], lens=44)])
st.shot('S08', 'livingRoom', setOpts=LR, actors=[act('chat', [0.0, 0.105, -1.02], 0, 'sit', 'happy', scale=0.32)], props=[VAC((0, 0, -1.0), 0, mood='happy'), P('dome', 'glassDome', pos=[0.0, 0.1, -1.02], opts={'radius': 0.13, 'opacity': 0.25, 'base': False})],
        cams=[cam(0.0, [0.12, 0.4, -0.35], [0.11, 0.39, -0.42], [0.0, 0.2, -1.02], [0.0, 0.2, -1.02], lens=40)])
# 9-11: the sofa, the house, the neighbourhood (it grows)
st.shot('S09', 'livingRoom', setOpts=LR, props=[VAC((0.9, 0, -0.6), -75, scale=5.0, suckAt=0.0, mood='menace'), INTO('sofa', 'sofaProp', (-1.2, 0, -1.4), (0.2, 0.15, -0.65), 0.15, 0.75, 1.0, 0.1, opts=SOFA)],
        cams=[cam(0.0, [0.0, 1.6, 3.6], [0.0, 1.55, 3.3], [-0.1, 0.7, -1.0], [-0.1, 0.7, -1.0], lens=44)])
st.shot('S10', 'suburbDay', props=[VAC((7.0, 0, -6.0), -60, scale=42.0, suckAt=0.0, mood='menace'), INTO('house', 'cottage', (-4.0, 0, -8.0), (2.0, 1.5, -6.5), 0.1, 0.7, 1.0, 0.05)],
        cams=[cam(0.0, [-1.0, 3.0, 14.0], [-0.8, 3.1, 13.4], [1.0, 3.0, -6.0], [1.0, 3.0, -6.0], lens=44)])
st.shot('S11', 'aerialSuburb', props=[VAC((0, 0, -40.0), 0, scale=260.0, suckAt=0.0, mood='menace')] + [INTO(f'h{i}', 'cottage', (x, 0, z), (0, 20, -10), 0.1 + i * 0.12, 0.7, 1.0, 0.05) for i, (x, z) in enumerate(((-22, 40), (18, 46), (-8, 60), (26, 62)))],
        cams=[cam(0.0, [10.0, 70.0, 150.0], [9.0, 68.0, 140.0], [0.0, 10.0, -20.0], [0.0, 10.0, -20.0], lens=44)])
# 12-15: the mayor marches with his complaint (sign at chest height, tricolour sash); the town hall is sucked up; the tanks, sucked up
TH = P('th', 'townHall', pos=[0, 0, -5.0], opts={'w': 6, 'h': 4.5, 'd': 4})
st.shot('S12', 'parisStreet', actors=[act('maire', [0.2, 0, -1.9], 0, 'stand', 'angry', keys=[k(0.0, to=[0.2, 0, -1.55], dur=0.75, clip='carryBox', then='carry')])],
        props=[TH, P('pl', 'noticeBoard', on={'actor': 'maire', 'joint': 'torso', 'offset': [0.0, 0.4, 0.56]}, opts={'text': 'PLAINTE', 'style': 'sign', 'w': 0.72, 'h': 0.28, 'bg': '#F4F1E8', 'fg': '#C8322A', 'frame': '#1C2E4A'})],
        cams=[cam(0.0, [0.6, 1.6, 2.6], [0.58, 1.6, 2.35], [0.1, 1.85, -1.8], [0.1, 1.85, -1.8], lens=44)])
st.shot('S13', 'parisStreet', actors=[act('maire', [1.2, 0, 3.0], 120, 'stand', 'scared', keys=[k(0.15, to=[3.2, 0, 4.6], dur=1.3, clip='run')])],
        props=[VAC((-14.0, 0, -6.0), 80, scale=60.0, suckAt=0.0, mood='menace'), P('th', 'townHall', pos=[0, 0, -5.0], opts={'w': 6, 'h': 4.5, 'd': 4}, keys=[k(0.15, to=[-7.0, 2.0, -5.0], dur=1.0, ease='in'), k(0.15, scale=0.05, dur=1.0, ease='in'), k(1.16, visible=False)])],
        cams=[cam(0.0, [5.0, 2.0, 9.0], [4.7, 2.05, 8.6], [-3.0, 2.5, -5.0], [-3.0, 2.6, -5.0], lens=44)])
TANKS = lambda keys_fn: [P(f'tk{i}', 'armyTank', pos=[x, 0, z], scale=3.0, keys=keys_fn(i, x, z)) for i, (x, z) in enumerate(((-1.6, -0.7), (0.15, -2.5), (1.8, -0.9)))]
D14 = st.dur('S14')
st.shot('S14', 'desert', props=TANKS(lambda i, x, z: [k(0.0, to=[x, 0, z + 2.0], dur=D14, ease='linear')]), cams=[cam(0.0, [1.0, 1.4, 9.0], [0.9, 1.35, 8.6], [0.0, 1.2, 0.0], [0.0, 1.2, 0.5], lens=44, shake=0.01)])
st.shot('S15', 'desert', props=[VAC((0.0, 0, -30.0), 0, scale=70.0, suckAt=0.0, mood='menace')] + TANKS(lambda i, x, z: [k(0.1 + i * 0.12, to=[x * 0.3, 2.5 + i, -18.0], dur=0.75, ease='in'), k(0.1 + i * 0.12, scale=0.3, dur=0.75, ease='in'), k(0.86 + i * 0.12, visible=False)]),
        cams=[cam(0.0, [1.0, 1.8, 9.0], [0.9, 1.85, 8.6], [0.0, 1.1, -10.0], [0.0, 1.3, -10.0], lens=44, shake=0.012)])
# 16-18: back to its base; low battery; tonight he empties it into the bin
D16 = st.dur('S16')
st.shot('S16', 'livingRoom', setOpts=LR, props=[P('dock', 'chargingDock', pos=[0.0, 0, -1.6]), VAC((0.0, 0, -0.6), 180, keys=[k(0.1, to=[0.0, 0, -1.45], dur=D16 - 0.3, ease='out')], idleBob=True)],
        cams=[cam(0.0, [0.55, 0.55, 0.6], [0.52, 0.53, 0.5], [0.0, 0.1, -1.2], [0.0, 0.1, -1.4], lens=44)])
st.shot('S17', 'livingRoom', setOpts=LR, props=[P('dock', 'chargingDock', pos=[0.0, 0, -1.6], opts={'low': True}), VAC((0.0, 0, -1.45), 0, low=True, mood='tired'),
        P('batt', 'batteryIcon', pos=[0.0, 0.25, -1.45], opts={'w': 0.14, 'popAt': 0.25})],
        cams=[cam(0.0, [0.0, 0.17, -0.45], [0.0, 0.17, -0.5], [0.0, 0.1, -1.45], [0.0, 0.1, -1.45], lens=40)])
ROB18 = [0.0, 1.3, -1.08]
SHAKE = [k(0.08 + 0.27 * i, to=[ROB18[0], ROB18[1] + (0.035 if i % 2 == 0 else 0.0), ROB18[2]], dur=0.12) for i in range(6)]
DROP = lambda pid, name, s, t0, opts=None, ry=0: P(pid, name, pos=[0.0, 1.2, -1.06], ry=ry, scale=s, opts=opts or {},
                                                  keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, to=[0.0, 0.6, -1.05], dur=0.3, ease='in'), k(t0 + 0.31, visible=False)])
PILE = [DROP('ps', 'sockPair', 1.0, 0.15, ry=30), DROP('pf', 'sofaProp', 0.1, 0.42, SOFA, ry=-20), DROP('pc', 'cottage', 0.05, 0.69, ry=25),
        DROP('pm', 'townHall', 0.045, 0.96, ry=-15), DROP('pt', 'armyTank', 0.25, 1.23, ry=40)]
EVENING = {'hemi': 0.78, 'sky': '#FFE3BE', 'ground': '#5A4A3C', 'keyI': 0.82, 'key': '#FFC88E'}
st.shot('S18', 'livingRoom', setOpts=LR, light=EVENING,
        actors=[act('mec', [0.0, 0, -1.55], 15, 'carry', 'unimpressed'), act('chat', [0.0, 0.6, -1.05], 20, 'celebrate', 'happy', scale=0.5, keys=[k(0.0, visible=False), k(1.55, visible=True)])],
        props=PILE + [P('bin', 'trashCan', pos=[0.0, 0, -1.05], opts={'open': True}), P('vac', 'robotVacuum', pos=ROB18, ry=23, rot=[0.4, 0, 3.1416], opts={'mood': 'tired', 'low': True}, keys=SHAKE)],
        cams=[cam(0.0, [0.7, 2.2, 1.2], [0.67, 2.18, 1.08], [0.0, 1.2, -1.2], [0.0, 1.18, -1.2], lens=44)])
st.card('S11', 'LE QUARTIER'); st.card('S17', 'BATTERIE FAIBLE')
st.cue('sfx:beep', 'S02', T_ON, 0.3); st.cue('sfx:boing', 'S02', T_HOP, 0.25); st.cue('sfx:click', 'S03', 0.05, 0.3); st.cue('whoosh', 'S04', T4 - 0.3, 0.35); st.cue('whoosh', 'S06', 0.08, 0.4)
st.cue('whoosh', 'S07', T7 - 0.15, 0.45); st.cue('sfx:boing', 'S08', 0.2, 0.25); st.cue('whoosh', 'S09', 0.2, 0.5); st.cue('whoosh', 'S10', 0.1, 0.55); st.cue('gust', 'S11', 0.0, 0.5)
st.cue('sfx:paper', 'S12', 0.2, 0.35); st.cue('whoosh', 'S13', 0.15, 0.55); st.cue('engine', 'S14', 0.0, 0.45); st.cue('whoosh', 'S15', 0.1, 0.55); st.cue('sfx:beep', 'S16', 0.9, 0.3)
[st.cue('sfx:beep', 'S17', 0.15 + 0.35 * i, 0.22) for i in range(3)]; [st.cue('thud', 'S18', t0 + 0.28, 0.3) for t0 in (0.15, 0.69, 1.23)]; st.cue('pop', 'S18', 1.55, 0.4)
st.write("L'aspirateur", {'chat': {'type': 'creature', 'name': 'cat', 'opts': {'seed': 6, 'ol': 0.0035}},
                         'maire': {'preset': 'politique', 'seed': 61, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12}})
