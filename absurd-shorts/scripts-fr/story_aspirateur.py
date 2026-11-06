#!/usr/bin/env python3
"""L'aspirateur (story 28): this man bought a robot vacuum. Day one it sucked up the dust; day two the socks; day three the cat
(the cat is fine). Then the sofa, the house, the neighbourhood. The town hall filed a complaint: it sucked up the town hall. The
army sent the tanks: it sucked up the tanks. Then it went back to its base. Low battery. Tonight the man has to empty it."""
from story_kit import *

st = Story('aspirateur')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 16)])
PI = math.pi
LR = {'sofa': False, 'tv': False}
VAC = lambda pos=(0, 0, -1.0), ry=0, scale=1.0, keys=None, **o: P('vac', 'robotVacuum', pos=list(pos), ry=ry, scale=scale, opts=o, **({'keys': keys} if keys else {}))
LOWCAM = lambda x=0.0, z=-1.0, d=0.95, h=0.24, lens=44: [cam(0.0, [x + 0.1, h, z + d], [x + 0.09, h, z + d - 0.1], [x, 0.08, z], [x, 0.08, z], lens=lens)]
INTO = lambda pid, name, p0, p1, t0, dur, s0=1.0, s1=0.05, **kw: P(pid, name, pos=list(p0), scale=s0, keys=[k(t0, to=list(p1), dur=dur, ease='in'), k(t0, scale=s1, dur=dur, ease='in'), k(t0 + dur, visible=False)], **kw)

# 1-5: the vacuum; dust; socks; the cat; the cat is fine
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.7], -15, 'present', 'happy')], props=[VAC((-0.35, 0, -1.1), 20)],
        cams=[cam(0.0, [0.4, 1.35, 1.6], [0.38, 1.3, 1.35], [0.05, 0.95, -1.4], [0.05, 0.9, -1.4], lens=44)])
st.shot('S02', 'livingRoom', setOpts=LR, props=[VAC((0, 0, -1.0), 0, mood='happy', idleBob=True)], cams=LOWCAM(0.0, -1.0, 0.75, 0.2))
D3 = st.dur('S03')
st.shot('S03', 'livingRoom', setOpts=LR, props=[VAC((0.15, 0, -1.0), -10, suckAt=0.3, keys=[k(0.0, to=[-0.05, 0, -0.9], dur=D3, ease='linear')]),
        INTO('dust', 'dustPuff', (-0.05, 0.04, -0.5), (-0.05, 0.05, -0.75), 0.5, 0.8, 0.5, 0.05, opts={'color': '#B8B0A0'})], cams=LOWCAM(0.0, -0.9, 1.15, 0.28))
st.shot('S04', 'livingRoom', setOpts=LR, props=[VAC((0, 0, -1.0), 0, suckAt=0.2), INTO('socks', 'sockPair', (0.25, 0.25, -0.3), (0.0, 0.05, -0.8), 0.35, 0.75, 1.3, 0.1)],
        cams=LOWCAM(0.0, -0.9, 1.25, 0.32))
st.shot('S05', 'livingRoom', setOpts=LR, actors=[act('chat', [0.05, 0, -0.3], 180, 'sit', 'scared', keys=[k(0.25, to=[0.0, 0.04, -0.82], dur=1.35, glide=True, face='keep', ease='in'), k(0.25, scale=0.15, dur=1.35, ease='in'), k(1.62, visible=False)]),
        act('mec', [0.6, 0, -1.9], -20, 'stand', 'shocked')], props=[VAC((0, 0, -1.0), 0, suckAt=0.25, mood='menace')],
        cams=[cam(0.0, [0.45, 0.65, 0.9], [0.43, 0.65, 0.78], [0.05, 0.45, -1.0], [0.05, 0.45, -1.0], lens=44)])
st.shot('S06', 'livingRoom', setOpts=LR, actors=[act('chat', [0.0, 0.105, -1.02], 0, 'sit', 'happy', scale=0.32)], props=[VAC((0, 0, -1.0), 0, mood='happy'), P('dome', 'glassDome', pos=[0.0, 0.1, -1.02], opts={'radius': 0.13, 'opacity': 0.25, 'base': False})],
        cams=[cam(0.0, [0.12, 0.4, -0.35], [0.11, 0.39, -0.42], [0.0, 0.2, -1.02], [0.0, 0.2, -1.02], lens=40)])
# 6-8: the sofa, the house, the neighbourhood (it grows)
st.shot('S07', 'livingRoom', setOpts=LR, props=[VAC((0.9, 0, -0.6), -75, scale=5.0, suckAt=0.0, mood='menace'), INTO('sofa', 'sofaProp', (-1.2, 0, -1.4), (0.2, 0.15, -0.65), 0.15, 0.75, 1.0, 0.1)],
        cams=[cam(0.0, [0.0, 1.6, 3.6], [0.0, 1.55, 3.3], [-0.1, 0.7, -1.0], [-0.1, 0.7, -1.0], lens=44)])
st.shot('S08', 'suburbDay', props=[VAC((7.0, 0, -6.0), -60, scale=42.0, suckAt=0.0, mood='menace'), INTO('house', 'cottage', (-4.0, 0, -8.0), (2.0, 1.5, -6.5), 0.1, 0.7, 1.0, 0.05)],
        cams=[cam(0.0, [-1.0, 3.0, 14.0], [-0.8, 3.1, 13.4], [1.0, 3.0, -6.0], [1.0, 3.0, -6.0], lens=44)])
st.shot('S09', 'aerialSuburb', props=[VAC((0, 0, -40.0), 0, scale=260.0, suckAt=0.0, mood='menace')] + [INTO(f'h{i}', 'cottage', (x, 0, z), (0, 20, -10), 0.1 + i * 0.12, 0.7, 1.0, 0.05) for i, (x, z) in enumerate(((-22, 40), (18, 46), (-8, 60), (26, 62)))],
        cams=[cam(0.0, [10.0, 70.0, 150.0], [9.0, 68.0, 140.0], [0.0, 10.0, -20.0], [0.0, 10.0, -20.0], lens=44)])
# 9-12: the town hall complains, gets sucked up; the tanks, sucked up
TH = P('th', 'townHall', pos=[0, 0, -5.0], opts={'w': 6, 'h': 4.5, 'd': 4})
st.shot('S10', 'parisStreet', actors=[act('maire', [0.2, 0, -1.6], 0, 'holdSign', 'angry')], props=[TH, P('sash', 'necktie', on={'actor': 'maire', 'joint': 'torso', 'offset': [0.0, 0.4, 0.13]}, opts={'color': '#2F62B5', 'len': 0.3}),
        P('pl', 'noticeBoard', on={'actor': 'maire', 'hand': 'R', **SIGN_UP}, opts={'text': 'PLAINTE', 'style': 'sign', 'w': 0.7, 'h': 0.3, 'bg': '#F4F1E8', 'fg': '#C8322A', 'frame': '#1C2E4A'})],
        cams=[cam(0.0, [0.6, 1.6, 2.6], [0.58, 1.6, 2.35], [0.1, 1.85, -1.8], [0.1, 1.85, -1.8], lens=44)])
st.shot('S11', 'parisStreet', actors=[act('maire', [1.0, 0, 3.0], 160, 'stand', 'scared', keys=[k(0.2, to=[3.5, 0, 6.0], dur=1.2, clip='run')])],
        props=[VAC((-14.0, 0, -6.0), 80, scale=60.0, suckAt=0.0, mood='menace'), P('th', 'townHall', pos=[0, 0, -5.0], opts={'w': 6, 'h': 4.5, 'd': 4}, keys=[k(0.15, to=[-7.0, 2.0, -5.0], dur=1.0, ease='in'), k(0.15, scale=0.05, dur=1.0, ease='in'), k(1.16, visible=False)])],
        cams=[cam(0.0, [6.0, 3.0, 12.0], [5.6, 3.1, 11.4], [-3.0, 4.0, -5.0], [-3.0, 4.0, -5.0], lens=44)])
TANKS = lambda keys_fn: [P(f'tk{i}', 'armyTank', pos=[x, 0, z], scale=3.0, keys=keys_fn(i, x, z)) for i, (x, z) in enumerate(((-2.6, -1.0), (0.0, -2.2), (2.6, -1.0)))]
D12 = st.dur('S12')
st.shot('S12', 'desert', props=TANKS(lambda i, x, z: [k(0.0, to=[x, 0, z + 2.0], dur=D12, ease='linear')]), cams=[cam(0.0, [1.0, 1.4, 9.0], [0.9, 1.35, 8.6], [0.0, 1.2, 0.0], [0.0, 1.2, 0.5], lens=44, shake=0.01)])
st.shot('S13', 'desert', props=[VAC((0.0, 0, -30.0), 0, scale=70.0, suckAt=0.0, mood='menace')] + TANKS(lambda i, x, z: [k(0.1 + i * 0.12, to=[x * 0.3, 2.5 + i, -18.0], dur=0.75, ease='in'), k(0.1 + i * 0.12, scale=0.3, dur=0.75, ease='in'), k(0.86 + i * 0.12, visible=False)]),
        cams=[cam(0.0, [2.0, 2.0, 10.0], [1.8, 2.2, 9.5], [0.0, 3.5, -10.0], [0.0, 3.8, -10.0], lens=44, shake=0.012)])
# 13-16: back to its base; low battery; tonight he empties it
D14 = st.dur('S14')
st.shot('S14', 'livingRoom', setOpts=LR, props=[P('dock', 'chargingDock', pos=[0.0, 0, -1.6]), VAC((0.0, 0, -0.6), 180, keys=[k(0.1, to=[0.0, 0, -1.45], dur=D14 - 0.3, ease='out')], idleBob=True)],
        cams=[cam(0.0, [0.55, 0.55, 0.6], [0.52, 0.53, 0.5], [0.0, 0.1, -1.2], [0.0, 0.1, -1.4], lens=44)])
st.shot('S15', 'livingRoom', setOpts=LR, props=[P('dock', 'chargingDock', pos=[0.0, 0, -1.6], opts={'low': True}), VAC((0.0, 0, -1.45), 0, low=True, mood='tired')], cams=LOWCAM(0.0, -1.45, 0.62, 0.17, 40))
PILE = [P('ps', 'sockPair', pos=[0.1, 0.75, -1.05], scale=0.8, keys=[k(0.3, to=[0.05, 0.05, -1.25], dur=0.4, ease='in')]),
        P('pc', 'cottage', pos=[-0.05, 0.85, -1.05], scale=0.035, keys=[k(0.45, to=[-0.15, 0.05, -1.35], dur=0.4, ease='in')]),
        P('pt', 'armyTank', pos=[0.0, 0.85, -1.05], scale=0.16, keys=[k(0.6, to=[0.18, 0.05, -1.35], dur=0.4, ease='in')]),
        P('pm', 'townHall', pos=[0.0, 0.9, -1.05], scale=0.03, keys=[k(0.75, to=[-0.05, 0.05, -1.45], dur=0.4, ease='in')])]
st.shot('S16', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.75], 20, 'holdOut', 'unimpressed'), act('chat', [0.55, 0.0, -1.15], -20, 'celebrate', 'happy')],
        props=PILE + [P('bin', 'trashCan', pos=[0.0, 0, -1.3]), P('vac', 'robotVacuum', on={'actor': 'mec', 'hand': 'R', 'rot': [3.1416, 0, 0], 'offset': [0.0, -0.2, 0.18]}, opts={'mood': 'tired', 'low': True})],
        cams=[cam(0.0, [0.85, 1.45, 2.05], [0.82, 1.43, 1.9], [0.15, 1.0, -1.4], [0.15, 0.98, -1.4], lens=44)])
st.card('S09', 'LE QUARTIER'); st.card('S15', 'BATTERIE FAIBLE')
st.cue('sfx:beep', 'S02', 0.2, 0.3); st.cue('whoosh', 'S03', 0.5, 0.35); st.cue('whoosh', 'S04', 0.35, 0.4); st.cue('whoosh', 'S05', 0.45, 0.45); st.cue('sfx:boing', 'S06', 0.2, 0.25)
st.cue('whoosh', 'S07', 0.2, 0.5); st.cue('whoosh', 'S08', 0.1, 0.55); st.cue('gust', 'S09', 0.0, 0.5); st.cue('sfx:paper', 'S10', 0.2, 0.35); st.cue('whoosh', 'S11', 0.15, 0.55)
st.cue('engine', 'S12', 0.0, 0.45); st.cue('whoosh', 'S13', 0.1, 0.55); st.cue('sfx:beep', 'S14', 0.9, 0.3); [st.cue('sfx:beep', 'S15', 0.15 + 0.35 * i, 0.22) for i in range(3)]; st.cue('thud', 'S16', 0.7, 0.35)
st.write("L'aspirateur", {'chat': {'type': 'creature', 'name': 'cat', 'opts': {'seed': 6}}, 'maire': {'preset': 'politique', 'seed': 61}})
