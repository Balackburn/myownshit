#!/usr/bin/env python3
"""Le vélo: his bike steals itself and rides off; the police can't catch it; it enters the Tour de France with no rider, seventy
kilos lighter than the others, wins the stage and the yellow jersey (doping test: a bit of oil on the chain); he sues for theft,
the court sides with the bike (it belongs to itself); he owes it alimony, two inner tubes a month. Today the bike is a star with
its own car and a chauffeur: him."""
from story_kit import *

st = Story('velo')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 12)] + [('S12', 'L11', 3)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(12, 21)])
ST = 'parisStreet'
RZ = [0, -1.5708, 0]                                                     # a bike facing +Z (local +X forward)
BIKE = lambda pos, rot=RZ, scale=1.0, keys=None, **o: P('velo', 'livingBike', pos=pos, rot=rot, scale=scale, opts={'speed': o.pop('speed', 0), **o}, **({'keys': keys} if keys else {}))
RIDERS = [('r1', '#2F62B5'), ('r2', '#C9822E'), ('r3', '#2F7F5C')]
def rider(aid, x, z, col, keys=None, bike_keys=None, expr='unimpressed'):   # a cyclist on a plain bicycle, both facing +Z
    return (act(aid, [x, 0.55, z - 0.16], 0, 'drive', expr, keys=keys or []),
            P(f'bk_{aid}', 'bicycle', pos=[x, 0, z], rot=RZ, opts={'color': col}, **({'keys': bike_keys} if bike_keys else {})))
CROWD = lambda x0, z0, n=5: [act(f'fan{i}', [x0 + 0.62 * (i % 2), 0, z0 - 0.9 * i], -90, 'celebrate', 'happy') for i in range(n)]

# 1-5: stolen by itself, off on its own, the police can't catch it
st.shot('S01', ST, actors=[act('mec', [6.4, 0, 0.8], 0, 'doubleTake', 'shocked')], props=[P('chain', 'innerTube', pos=[5.62, 0.9, 0.2], rot=[0, 0, 1.2], opts={'r': 0.12})],
        cams=CU(6.4, 0.8, h=1.66, dx=0.3, d=1.9))
st.shot('S02', ST, props=[BIKE([5.8, 0, -0.6], rot=[0, 1.5708, 0], speed=2.2, look=[0, -1], keys=[k(0.0, to=[5.8, 0, -3.0], dur=st.dur('S02'), ease='in')])],
        cams=[cam(0.0, [6.3, 0.55, 1.6], [6.25, 0.57, 1.35], [5.8, 0.75, -1.0], [5.8, 0.75, -2.4], lens=46)])
st.shot('S03', ST, props=[BIKE([2.0, 0, -4.0], speed=6, keys=[k(0.0, to=[2.0, 0, 4.0], dur=st.dur('S03'), ease='linear')]), P('speed', 'speedLines', pos=[2.0, 0.8, 0.0], rot=RZ)],
        cams=[cam(0.0, [3.4, 0.6, -2.6], [3.4, 0.6, 2.6], [2.0, 0.7, -4.0], [2.0, 0.7, 4.0], lens=46)], blur=[[0.0, st.dur('S03'), 0.012]], blurSamples=6)
st.shot('S04', ST, props=[BIKE([1.5, 0, -2.0], speed=7, keys=[k(0.0, to=[1.5, 0, 8.0], dur=st.dur('S04'), ease='linear')]),
                         P('pcar', 'policeCar', pos=[1.6, 0, -8.5], rot=RZ, keys=[k(0.0, to=[1.6, 0, 1.5], dur=st.dur('S04'), ease='linear')])],
        cams=[cam(0.0, [4.4, 1.0, -1.6], [4.4, 1.0, 8.4], [1.5, 0.9, -5.2], [1.5, 0.9, 4.8], lens=48, shake=0.015)], blur=[[0.0, st.dur('S04'), 0.01]], blurSamples=6)
st.shot('S05', ST, actors=[act('flic', [2.6, 0, 1.0], 160, 'bigShrug', 'sad')], props=[P('pcar', 'policeCar', pos=[1.4, 0, 1.2], rot=RZ), BIKE([1.4, 0, -6.0], speed=6, keys=[k(0.0, to=[1.4, 0, -14.0], dur=st.dur('S05'), ease='linear')])],
        cams=[cam(0.0, [3.4, 1.5, 3.6], [3.35, 1.52, 3.3], [2.0, 1.2, -2.0], [2.0, 1.2, -3.0], lens=46)])
# 6-10: the Tour de France, no rider, seventy kilos lighter, the stage, the yellow jersey
st.shot('S06', ST, actors=[act('official', [6.6, 0, -1.2], 0, 'clipboard', 'suspicious')],
        props=[P('desk', 'table', pos=[6.6, 0, -0.55], opts={'w': 1.2, 'd': 0.6}), P('sign', 'noticeBoard', pos=[6.6, 2.42, -1.7], opts={'text': 'TOUR DE FRANCE\nINSCRIPTIONS', 'style': 'sign', 'w': 1.3, 'h': 0.4, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'}),
               BIKE([6.6, 0, 0.35], rot=[0, 3.1416, 0], look=[0.3, 0]), P('bib', 'noticeBoard', pos=[6.75, 1.1, 0.42], opts={'text': '1', 'style': 'tag', 'w': 0.16, 'h': 0.13, 'popAt': st.at('S06', 'L06', 4) - 0.05})],
        cams=[cam(0.0, [7.4, 1.3, 3.0], [7.35, 1.32, 2.75], [6.6, 1.05, -0.4], [6.6, 1.05, -0.4], lens=46)])
R7 = [rider(a, x, -0.6, c) for (a, c), x in zip(RIDERS, (-1.0, 1.0, 1.9))]
st.shot('S07', ST, actors=[r[0] for r in R7], props=[r[1] for r in R7] + [BIKE([0.0, 0, 0.0], bib=1, look=[0.2, 0.5]),
        P('start', 'signBoard', pos=[0.4, 0, -1.4], opts={'text': 'DÉPART', 'w': 3.2, 'h': 0.45, 'height': 2.5, 'bg': '#F4F4F0', 'fg': '#C8322A', 'frame': '#C8322A'})],
        cams=[cam(0.0, [0.15, 0.62, 2.6], [0.15, 0.64, 2.35], [0.1, 0.95, -0.6], [0.1, 0.97, -0.6], lens=50)])
R8 = [rider('r1', 1.4, 1.0, RIDERS[0][1], expr='sad', keys=[k(0.0, to=[1.4, 0.55, 1.45], dur=st.dur('S08'), clip='drive')], bike_keys=[k(0.0, to=[1.4, 0, 1.6], dur=st.dur('S08'))])]
st.shot('S08', ST, actors=[r[0] for r in R8], props=[r[1] for r in R8] + [BIKE([0.4, 0, -0.6], speed=3, bib=1, keys=[k(0.0, to=[0.4, 0, 2.4], dur=st.dur('S08'), ease='linear')]),
        P('sweat', 'sweatDrop', on={'actor': 'r1', 'joint': 'head', 'offset': [0.12, 0.3, 0.1]}),
        P('kg', 'noticeBoard', pos=[0.4, 1.55, 1.2], opts={'text': '− 70 KG', 'style': 'tag', 'w': 0.5, 'h': 0.17, 'fg': '#2F7F4F', 'frame': '#2F7F4F', 'popAt': st.at('S08', 'L08', 1) - 0.05},
          keys=[k(0.0, to=[0.4, 1.55, 2.6], dur=st.dur('S08'), ease='linear')])],
        cams=[cam(0.0, [2.0, 0.9, 4.6], [2.0, 0.92, 5.6], [0.8, 0.9, 0.0], [0.8, 0.9, 1.8], lens=46)])
st.shot('S09', ST, actors=CROWD(5.6, 1.0), props=[BIKE([1.2, 0, -3.0], speed=6, bib=1, keys=[k(0.0, to=[1.2, 0, 3.0], dur=st.dur('S09'), ease='linear')]),
        P('arch', 'signBoard', pos=[1.4, 0, 0.0], opts={'text': 'ARRIVÉE', 'w': 4.2, 'h': 0.6, 'height': 2.8, 'bg': '#F4F4F0', 'fg': '#1C252A', 'frame': '#C8322A'})],
        cams=[cam(0.0, [2.6, 0.7, 5.2], [2.55, 0.72, 4.9], [1.3, 1.4, 0.0], [1.3, 1.45, 0.0], lens=48, shake=0.01)])
st.shot('S10', ST, actors=[act('r2', [6.0, 0.42, -0.5], 0, 'celebrate', 'happy'), act('r3', [7.25, 0.28, -0.5], 0, 'stand', 'unimpressed')],
        props=[P('pod', 'winnersPodium', pos=[6.62, 0, -0.5]), BIKE([6.62, 0.6, -0.5], rot=[0, 0, 0], jersey=True, bib=1, look=[0.3, 0]), P('fl', 'flowers', pos=[6.95, 0.6, -0.35], scale=1.2)],
        cams=[cam(0.0, [6.75, 1.45, 4.5], [6.72, 1.47, 4.2], [6.62, 1.25, -0.5], [6.62, 1.27, -0.5], lens=50)])
# 11-12: doping control: a bit of oil on the chain
st.shot('S11', 'office', actors=[act('docteur', [0.55, 0, -0.35], -40, 'lookItem', 'suspicious')], props=[BIKE([-0.1, 0, 0.0], rot=[0, 0, 0], jersey=True, look=[0, 0.5]),
        P('loupe', 'magnifyingGlass', on={'actor': 'docteur', 'hand': 'R'}, scale=0.45), P('lab', 'noticeBoard', pos=[0.0, 2.2, -1.3], opts={'text': 'ANTIDOPAGE', 'style': 'sign', 'w': 1.0, 'h': 0.26})],
        cams=MS(0.15, 0.0, h=1.35, d=3.0))
st.shot('S12', 'office', props=[BIKE([-0.1, 0, 0.0], rot=[0, 0, 0], jersey=True), P('oil', 'oilCan', pos=[-0.35, 0.36, 0.22], rot=[0, 0, -0.5], opts={'dripAt': 0.15})],
        cams=[cam(0.0, [0.12, 0.62, 1.1], [0.1, 0.6, 0.95], [-0.25, 0.38, 0.0], [-0.25, 0.38, 0.0], lens=44)])
# 13-16: the complaint, the court, a bike belongs to itself, alimony
st.shot('S13', 'policeStation', actors=[act('mec', [-1.85, 0, -1.2], -100, 'explain', 'angry', keys=st.talk('L12', 'S13', 'angry')), act('flic', [-2.7, 0, -2.75], 0, 'sitWrite', 'unimpressed')],
        cams=[cam(0.0, [-1.6, 1.5, 1.4], [-1.65, 1.5, 1.15], [-2.3, 1.2, -1.9], [-2.3, 1.2, -1.9], lens=46)])
st.shot('S14', **JUDGE(0.5, 'TRIBUNAL'))
st.shot('S15', 'courtroom', actors=[act('mec', [0.8, 0, -1.6], -20, 'angryFist', 'angry')], props=[BIKE([0.0, 0, -1.4], speed=2, look=[0.2, 0], keys=[k(0.0, to=[0.0, 0, 1.4], dur=st.dur('S15'), ease='linear')])],
        cams=[cam(0.0, [0.35, 1.0, 3.6], [0.33, 1.02, 3.35], [0.2, 0.9, -0.6], [0.2, 0.92, 0.2], lens=46)])
st.shot('S16', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': 'PENSION\nALIMENTAIRE', 'style': 'doc', 'w': 0.72, 'h': 0.9, 'popAt': 0.1, 'textSize': 0.4, 'stamp': 'À VIE'})],
        cams=[cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.95], [0, 1.5, 0], [0, 1.5, 0], lens=42)])
# 17-21: two inner tubes a month; the star, its car, its chauffeur: him
st.shot('S17', ST, actors=[act('mec', [7.1, 0, 0.3], -100, 'giveItem', 'sad')], props=[BIKE([6.0, 0, 0.0], rot=[0, 0, 0], look=[0.4, 0]),
        P('tube1', 'innerTube', on={'actor': 'mec', 'hand': 'R'}, rot=[1.5708, 0, 0]), P('tube2', 'innerTube', pos=[6.65, 0.3, 0.55], rot=[1.5708, 0, 0.3])],
        cams=[cam(0.0, [6.55, 1.25, 3.6], [6.55, 1.27, 3.35], [6.55, 0.95, 0.1], [6.55, 0.97, 0.1], lens=48)])
st.shot('S18', ST, actors=[act(f'ph{i}', [x, 0, 0.9], ry, 'showPhone', 'happy') for i, (x, ry) in enumerate(((5.75, 120), (7.45, -120)))],
        props=[P('carpet', 'carpet', pos=[6.6, 0, 0.0], rot=RZ, opts={'color': '#B5302A'}), BIKE([6.6, 0, -1.6], speed=1.2, shades=True, keys=[k(0.0, to=[6.6, 0, 0.0], dur=st.dur('S18'), ease='out')]),
               P('st1', 'stanchions', pos=[5.9, 0, -0.5], rot=RZ), P('st2', 'stanchions', pos=[7.3, 0, -0.5], rot=RZ)],
        cams=[cam(0.0, [6.65, 1.0, 3.2], [6.63, 1.02, 2.95], [6.6, 0.95, -0.4], [6.6, 0.97, -0.1], lens=50)],
        fx=[{'type': 'flash', 'at': t, 'dur': 0.06} for t in (0.3, 0.75, 1.2, 1.6)])
st.shot('S19', ST, props=[P('car', 'car', pos=[6.4, 0, -0.8], rot=[0, 0.25, 0], opts={'color': '#1C1C22', 'plate': 'VÉLO-1'}), BIKE([7.0, 0, 0.9], rot=[0, 0.4, 0], shades=True, look=[0.2, 0.3])],
        cams=[cam(0.0, [8.2, 1.2, 4.2], [8.1, 1.22, 3.9], [6.7, 0.9, 0.0], [6.7, 0.92, 0.0], lens=46)])
st.shot('S20', ST, actors=[act('chauffeur', [5.9, 0, 0.3], 30, 'present', 'unimpressed')], props=[P('car', 'car', pos=[6.4, 0, -0.8], rot=[0, 0.25, 0], opts={'color': '#1C1C22', 'plate': 'VÉLO-1'}),
        BIKE([7.6, 0, 1.4], rot=[0, 2.6, 0], shades=True, speed=1.0, keys=[k(0.0, to=[6.9, 0, 0.7], dur=st.dur('S20'), ease='out')])],
        cams=[cam(0.0, [7.0, 1.4, 3.6], [6.95, 1.42, 3.35], [6.4, 1.15, 0.2], [6.4, 1.17, 0.2], lens=46)])
st.shot('S21', ST, actors=[act('chauffeur', [6.45, 0.12, -0.4], 90, 'drive', 'unimpressed', keys=[k(0.9, expr='sad')])],
        props=[P('car', 'car', pos=[6.4, 0, 0.0], opts={'color': '#1C1C22', 'plate': 'VÉLO-1'}), BIKE([5.55, 0.32, 0.38], rot=[0, 0, 0], scale=0.62, shades=True, look=[0, 0])],
        cams=[cam(0.0, [8.9, 1.35, -0.55], [8.75, 1.35, -0.52], [6.45, 1.2, -0.3], [6.45, 1.2, -0.3], lens=44)])
st.card('S07', 'SANS CYCLISTE'); st.card('S14', 'RELAXÉ')
st.cue('sfx:gasp', 'S01', 0.4, 0.4); st.cue('sfx:spring', 'S02', 0.1, 0.25); st.cue('whoosh', 'S03', 0.1, 0.4, 1.0, 400, 3500)
st.cue('engine', 'S04', 0.0, 0.4, st.dur('S04')); st.cue('whoosh', 'S04', 0.2, 0.4, 1.0, 400, 3500); st.cue('sfx:grunt', 'S05', 0.3, 0.3)
st.cue('clack', 'S06', st.at('S06', 'L06', 4) - 0.05, 0.5); st.cue('sfx:whistle', 'S07', 0.3, 0.35); st.cue('thud', 'S07', 0.07, 0.45)
st.cue('pop', 'S08', st.at('S08', 'L08', 1) - 0.05, 0.45); st.cue('whoosh', 'S09', 0.3, 0.4, 0.8, 400, 3000); st.cue('sfx:fanfare', 'S09', 0.5, 0.35)
st.cue('sfx:choir', 'S10', 0.1, 0.25); st.cue('sfx:sniff', 'S11', 0.5, 0.3); [st.cue('sfx:pour', 'S12', t, 0.25) for t in (0.2, 0.8)]
st.cue('thud', 'S13', 0.4, 0.3); st.cue('thud', 'S14', 0.07, 0.45); st.cue('thud', 'S14', 0.5, 0.8); st.cue('sfx:spring', 'S15', 0.2, 0.2)
st.cue('sfx:paper', 'S16', 0.1, 0.45); st.cue('clack', 'S16', 0.5, 0.5); st.cue('sfx:squeak', 'S17', 0.5, 0.3)
[st.cue('clack', 'S18', t, 0.3) for t in (0.3, 0.75, 1.2, 1.6)]; st.cue('sfx:carDoor', 'S20', 0.6, 0.35); st.cue('engine', 'S21', 0.0, 0.3, st.dur('S21'))
st.write('Le vélo', {
    'official': {'preset': 'lemec_glasses', 'seed': 21}, 'docteur': {'preset': 'doctor'},
    'r1': {'preset': 'sportif', 'seed': 11, 'suit': '#2F62B5'}, 'r2': {'preset': 'sportif', 'seed': 13, 'suit': '#C9822E'}, 'r3': {'preset': 'sportif', 'seed': 17, 'suit': '#2F7F5C'},
    **{f'fan{i}': {'preset': p, 'seed': 40 + i} for i, p in enumerate(('femme', 'tourist', 'mamie', 'gamin', 'fermier'))},
    'ph0': {'preset': 'journaliste'}, 'ph1': {'preset': 'lemec_brown', 'seed': 7},
    'chauffeur': {'preset': 'lemec', 'hat': 'copcap', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}})
