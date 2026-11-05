#!/usr/bin/env python3
"""Le vélo: his bike steals itself and rides off; the police can't catch it; it enters the Tour de France with no rider, seventy
kilos lighter than the others, wins the stage and the yellow jersey (doping test: a bit of oil on the chain); he sues for theft,
the court sides with the bike (it belongs to itself); he owes it alimony, two inner tubes a month. Today the bike is a star with
its own car and a chauffeur: him.
Round 2 (critic review): the bike's eyes sit side by side (it reads head-on), every line shows the bike, riders wear helmets and
numbers, the hook shows the cut chain, the podium puts the bike on top, and the last shot reveals him driving the bike."""
from story_kit import *

st = Story('velo')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 12)] + [('S12', 'L11', 3)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(12, 21)])
ST = 'parisStreet'
PI = math.pi
def face(deg):                                                           # livingBike rotation so it faces (sin deg, cos deg): 0 = +Z (toward a camera at +Z)
    return [0, math.radians(deg) - PI / 2, 0]
RZ = face(0)
BIKE = lambda pos, rot=RZ, scale=1.0, keys=None, pid='velo', **o: P(pid, 'livingBike', pos=pos, rot=rot, scale=scale, opts={'speed': o.pop('speed', 0), **o}, **({'keys': keys} if keys else {}))
RIDERS = [('r1', '#2F62B5', 12), ('r2', '#C9822E', 27), ('r3', '#2F7F5C', 45)]
def rider(aid, x, z, col, keys=None, bike_keys=None, expr='unimpressed', back=False, cadence=1.5, lean=0.6):   # a racing cyclist on a plain bicycle, facing +Z (or -Z)
    sz = -1 if back else 1
    return (act(aid, [x, 0.5, z - 0.16 * sz], 180 if back else 0, 'ride', expr, keys=keys or [], params={'cadence': cadence, 'lean': lean}),
            P(f'bk_{aid}', 'bicycle', pos=[x, 0, z], rot=[0, PI / 2 if back else -PI / 2, 0], opts={'color': col}, **({'keys': bike_keys} if bike_keys else {})))
KG = lambda pid, text, pos, at_, keys=None, rot=None, **kw: P(pid, 'noticeBoard', pos=pos, **({'rot': rot} if rot else {}), opts={'text': text, 'style': 'tag', 'w': kw.pop('w', 0.5), 'h': kw.pop('h', 0.17), 'popAt': at_, **kw}, **({'keys': keys} if keys else {}))
CAR = dict(color='#F0EBDD', interior='#B03A2E', plate='VÉLO-1', convertible=True)   # an ivory open-top limousine, red seats
CX, CZ = 3.9, 1.0                                                        # the star's car, parked at the right kerb, facing -Z (passenger side +X = the pavement)

# 1-5: stolen by itself, off on its own, the police can't catch it
st.shot('S01', ST, actors=[act('mec', [7.3, 0, 4.0], -35, 'drawUp', 'shocked')],
        props=[P('chain', 'cutChain', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, opts={'n': 5}), P('psign', 'bikeSign', pos=[7.55, 0, 2.15], rot=[0, -0.5, 0]),
               P('rack', 'bikeRack', pos=[7.85, 0, 2.35], rot=[0, PI / 2, 0], opts={'n': 2})],
        cams=[cam(0.0, [6.25, 1.78, 5.6], [6.38, 1.78, 5.38], [7.12, 1.84, 3.85], [7.12, 1.84, 3.85], lens=44, shake=0.006)])
st.shot('S02', ST, props=[BIKE([6.4, 0, 1.2], rot=face(180), speed=3.0, goAt=0.62, lookKeys=[[0.0, 0.0, -0.6], [0.3, 0.15, 0.7]], keys=[k(0.62, to=[6.4, 0, -2.6], dur=st.dur('S02') - 0.62, ease='in')]),
                          P('rack', 'bikeRack', pos=[7.05, 0, 1.0], rot=[0, PI / 2, 0], opts={'n': 2})],
        cams=[cam(0.0, [5.72, 1.08, -0.42], [5.76, 1.06, -0.3], [6.42, 0.93, 0.62], [6.42, 0.93, 0.62], lens=44)])
st.shot('S03', ST, props=[BIKE([2.0, 0, -4.0], speed=6, look=[0.1, 0], keys=[k(0.0, to=[2.0, 0, 4.0], dur=st.dur('S03'), ease='linear')]), P('speed', 'speedLines', pos=[2.0, 0.8, 0.0], rot=RZ)],
        cams=[cam(0.0, [4.0, 0.9, -2.4], [4.0, 0.9, 3.4], [2.0, 0.82, -3.6], [2.0, 0.82, 4.4], lens=46)], blur=[[0.0, st.dur('S03'), 0.01]], blurSamples=6)
st.shot('S04', ST, props=[BIKE([2.0, 0, -1.0], speed=6.5, look=[0.25, -0.2], keys=[k(0.0, to=[2.0, 0, 8.4], dur=st.dur('S04'), ease='linear')]),
                          P('pcar', 'policeCar', pos=[1.05, 0, -9.0], rot=RZ, keys=[k(0.0, to=[1.05, 0, 2.6], dur=st.dur('S04'), ease='linear')])],
        cams=[cam(0.0, [2.65, 0.72, 2.3], [2.65, 0.72, 11.7], [1.7, 1.0, -2.6], [1.7, 1.0, 6.8], lens=46, shake=0.012)], blur=[[0.0, st.dur('S04'), 0.005]], blurSamples=5)
st.shot('S05', ST, actors=[act('flic', [2.98, 0, 1.0], 12, 'shrug', 'sad')],
        props=[P('pcar', 'policeCar', pos=[0.4, 0, -2.2], rot=face(180)), BIKE([2.15, 0, -6.5], speed=6, keys=[k(0.0, to=[2.15, 0, -12.5], dur=st.dur('S05'), ease='linear')], rot=face(180))],
        cams=[cam(0.0, [2.6, 1.6, 3.45], [2.59, 1.6, 3.25], [3.1, 1.62, -10.0], [3.1, 1.62, -10.0], lens=46)])
# 6-10: the Tour de France, no rider, seventy kilos lighter, the stage, the yellow jersey
st.shot('S06', ST, actors=[act('official', [7.3, 0, -1.15], -25, 'clipboard', 'suspicious')],
        props=[P('desk', 'table', pos=[7.05, 0, -0.55], opts={'w': 1.3, 'd': 0.6}), P('sign', 'noticeBoard', pos=[6.55, 2.75, -1.7], opts={'text': 'TOUR DE FRANCE\nINSCRIPTIONS', 'style': 'sign', 'w': 1.35, 'h': 0.42, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'}),
               BIKE([6.15, 0, 0.35], rot=face(35), look=[0.15, -0.5]), KG('bib', '1', [6.24, 1.06, 0.56], st.at('S06', 'L06', 4) - 0.05, w=0.2, h=0.16)],
        cams=[cam(0.0, [6.6, 1.42, 3.65], [6.58, 1.43, 3.4], [6.45, 1.3, -0.4], [6.45, 1.31, -0.4], lens=46)])
R7 = [rider(a, x, -0.75, c, cadence=0) for (a, c, n), x in zip(RIDERS[:2], (-0.82, 0.86))]
st.shot('S07', ST, actors=[r[0] for r in R7], props=[r[1] for r in R7] + [BIKE([0.0, 0, -0.35], rot=face(32), bib=1, look=[0.15, -0.6]),
        P('start', 'signBoard', pos=[0.2, 0, -3.2], opts={'text': 'DÉPART', 'w': 3.6, 'h': 0.5, 'height': 2.75, 'bg': '#F4F4F0', 'fg': '#C8322A', 'frame': '#C8322A'})],
        cams=[cam(0.0, [0.1, 1.05, 4.6], [0.1, 1.06, 4.35], [0.05, 1.45, -0.6], [0.05, 1.46, -0.6], lens=50)])
R8 = [rider('r1', 1.7, -0.6, RIDERS[0][1], expr='sad', cadence=1.0, lean=0.8, keys=[k(0.0, to=[1.7, 0.5, 0.75], dur=st.dur('S08'), clip='ride')], bike_keys=[k(0.0, to=[1.7, 0, 0.91], dur=st.dur('S08'))])]
st.shot('S08', ST, actors=[r[0] for r in R8], props=[r[1] for r in R8] + [BIKE([0.45, 0, -2.6], speed=3.4, bib=1, look=[0.1, -0.4], keys=[k(0.0, to=[0.45, 0, 3.4], dur=st.dur('S08'), ease='linear')]),
        P('sweat', 'sweatDrop', on={'actor': 'r1', 'joint': 'head', 'offset': [0.12, 0.3, 0.1]}),
        KG('kg', '− 70 KG', [0.45, 1.55, -2.6], st.at('S08', 'L08', 1) - 0.05, keys=[k(0.0, to=[0.45, 1.55, 3.4], dur=st.dur('S08'), ease='linear')], rot=[0, -PI / 2, 0], fg='#2F7F4F', frame='#2F7F4F')],
        cams=[cam(0.0, [-3.3, 1.05, -1.9], [-3.3, 1.05, 2.7], [1.0, 1.0, -1.6], [1.0, 1.0, 3.0], lens=46, roll=-7)])
FANS = [act(f'fan{i}', [x, 0, z], ry, 'celebrate', 'happy') for i, (x, z, ry) in enumerate(((1.5, -2.6, -110), (1.55, -4.2, -100), (1.5, -5.8, -100), (-1.5, -3.2, 110), (-1.55, -4.8, 100), (1.45, -1.0, -125), (-1.5, -1.7, 120)))]
st.shot('S09', ST, actors=FANS, props=[BIKE([0.25, 0, -3.6], speed=6, bib=1, look=[0.2, 0.2], keys=[k(0.0, to=[0.25, 0, 1.2], dur=st.dur('S09'), ease='out')]),
        P('arch', 'signBoard', pos=[0.0, 0, -0.6], opts={'text': 'ARRIVÉE', 'w': 3.8, 'h': 0.55, 'height': 2.7, 'bg': '#F4F4F0', 'fg': '#1C252A', 'frame': '#C8322A'}),
        P('bar1', 'crowdBarrier', pos=[1.12, 0, -3.0], rot=[0, PI / 2, 0], opts={'length': 6.4, 'sign': 'TOUR DE FRANCE'}), P('bar2', 'crowdBarrier', pos=[-1.12, 0, -3.2], rot=[0, -PI / 2, 0], opts={'length': 5.6, 'sign': 'TOUR DE FRANCE'})],
        cams=[cam(0.0, [0.3, 1.1, 5.8], [0.28, 1.11, 5.5], [0.1, 1.25, -1.0], [0.1, 1.27, -1.0], lens=48, shake=0.01)])
POD = dict(w=1.0, hs=1.85)                                               # step 1 is 1.11 m high: the bike stands above the slumped riders
PX, PZ = 1.0, 2.0                                                        # podium on the road, the camera looking +Z (open sky behind the winner)
st.shot('S10', ST, actors=[act('r2', [PX + 1.03, 0.28, PZ + 0.3], 180, 'sitSlump', 'sad'), act('r1', [PX - 1.03, 0.02, PZ + 0.3], 180, 'sitSlump', 'sad')],
        props=[P('pod', 'winnersPodium', pos=[PX, 0, PZ], rot=[0, PI, 0], opts=POD), BIKE([PX, 1.11, PZ], rot=face(150), scale=1.15, jersey=True, look=[0.25, 0.5]), P('fl', 'flowers', pos=[PX + 0.4, 1.11, PZ - 0.35], scale=1.3)],
        cams=[cam(0.0, [PX + 0.08, 0.9, PZ - 4.9], [PX + 0.06, 0.95, PZ - 4.4], [PX, 1.62, PZ], [PX, 1.68, PZ], lens=50)])
# 11-12: doping control: a bit of oil on the chain
st.shot('S11', 'office', actors=[act('docteur', [-0.2, -0.08, -0.6], 0, 'kneelLook', 'suspicious')], props=[BIKE([-0.1, 0, 0.0], rot=[0, 0, 0], jersey=True, look=[-0.3, 0.7]),
        P('loupe', 'magnifyingGlass', on={'actor': 'docteur', 'hand': 'R'}, scale=1.0), P('lab', 'noticeBoard', pos=[-0.75, 2.2, -1.3], opts={'text': 'ANTIDOPAGE', 'style': 'sign', 'w': 1.1, 'h': 0.28})],
        cams=[cam(0.0, [0.3, 1.05, 3.2], [0.28, 1.05, 3.0], [-0.25, 1.08, -0.2], [-0.25, 1.08, -0.2], lens=46)])
st.shot('S12', 'office', props=[BIKE([-0.1, 0, 0.0], rot=[0, 0, 0], jersey=True), P('oil', 'oilCan', pos=[-0.53, 0.555, 0.2], scale=1.3, opts={'dripAt': 0.1, 'color': '#2F9E5A', 'pour': True, 'drop': '#E0A020', 'dropR': 0.011, 'fall': 0.155})],
        cams=[cam(0.0, [-0.26, 0.7, 1.15], [-0.27, 0.69, 1.05], [-0.38, 0.5, 0.1], [-0.38, 0.5, 0.1], lens=46)])
# 13-16: the complaint, the court, a bike belongs to itself, alimony
st.shot('S13', 'policeStation', actors=[act('mec', [-1.85, 0, -1.2], -55, 'explain', 'angry', keys=st.talk('L12', 'S13', 'angry')), act('flic', [-2.7, 0, -2.75], 0, 'sitWrite', 'unimpressed')],
        cams=[cam(0.0, [-1.25, 1.45, 1.75], [-1.3, 1.45, 1.5], [-2.05, 1.36, -1.9], [-2.05, 1.36, -1.9], lens=46)])
J14 = JUDGE(round(st.at('S14', 'L13', 6) - 0.05, 3), 'TRIBUNAL')
J14['props'][0] = P('specs', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.25, 0.15]}, opts={'r': 0.042, 'dx': 0.07})
J14['cams'] = [cam(0.0, [-0.3, 1.36, -11.3], [-0.31, 1.37, -11.55], [-0.42, 1.68, -14.0], [-0.42, 1.68, -14.0], lens=45)]
st.shot('S14', **J14)
st.shot('S15', 'courtroom', actors=[act('mec', [0.8, 0, -1.6], -20, 'facepalmFlat', 'worried')], props=[BIKE([0.0, 0, -1.4], speed=2, rot=face(-15), look=[0.25, 0.2], keys=[k(0.0, to=[0.0, 0, 1.2], dur=st.dur('S15'), ease='linear')])],
        cams=[cam(0.0, [0.35, 1.0, 3.6], [0.33, 1.02, 3.35], [0.2, 0.9, -0.6], [0.2, 0.92, 0.2], lens=46)])
st.shot('S16', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': 'PENSION\nALIMENTAIRE', 'style': 'doc', 'w': 0.72, 'h': 0.9, 'popAt': 0.1, 'textSize': 0.4, 'stamp': 'À VIE'})],
        cams=[cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.95], [0, 1.5, 0], [0, 1.5, 0], lens=42)])
# 17-21: two inner tubes a month; the star, its car, its chauffeur: him
TUBE = lambda pid, off, rot: P(pid, 'innerTube', on={'actor': 'mec', 'hand': 'R', 'rot': rot, 'offset': off}, opts={'r': 0.22})
st.shot('S17', ST, actors=[act('mec', [7.15, 0, 0.25], -95, 'giveItem', 'sad')], props=[BIKE([5.95, 0, 0.1], rot=face(55), look=[0.2, -0.3]),
        TUBE('tube1', [0, -0.1, -0.2], [PI / 2, PI / 2, 0]), TUBE('tube2', [0.0, -0.3, -0.24], [PI / 2, PI / 2 + 0.25, 0.08])],
        cams=[cam(0.0, [6.7, 1.25, 3.7], [6.7, 1.26, 3.45], [6.68, 1.0, 0.1], [6.68, 1.01, 0.1], lens=48)])
STAR = st.at('S18', 'L17', 5)                                            # « star »: the flashes go off together
FL0, FL1 = [0.35, 0.95, 1.23, STAR - 0.1, STAR + 0.25], [0.7, 1.12, 1.45, STAR, 1.75, 2.02]   # paparazzi: bursts all along, a volley on « star »
PHOTOG = [act('ph0', [7.7, 0, 3.48], 60, 'binocs', 'happy'), act('ph1', [7.7, 0, 4.52], 120, 'binocs', 'happy')]
st.shot('S18', ST, actors=PHOTOG,
        props=[P('door', 'door', pos=[10.12, 0, 4.0], rot=[0, -PI / 2, 0], opts={'color': '#2F5E58'}), P('carpet', 'carpet', pos=[8.0, 0, 4.0], opts={'color': '#B5302A', 'w': 4.2, 'd': 1.1}),
               BIKE([9.75, 0, 4.0], speed=1.2, rot=face(-72), shades=True, look=[0.1, 0.2], keys=[k(0.0, to=[8.15, 0, 4.0], dur=st.dur('S18'), ease='out')]),
               P('st1', 'stanchions', pos=[8.4, 0, 3.4]), P('st2', 'stanchions', pos=[8.4, 0, 4.6]),
               P('cam0', 'pressCamera', on={'actor': 'ph0', 'hand': 'R', **HAND_FLAT}, scale=1.8, opts={'flashAt': FL0, 'burst': 0.3}), P('cam1', 'pressCamera', on={'actor': 'ph1', 'hand': 'R', **HAND_FLAT}, scale=1.8, opts={'flashAt': FL1, 'burst': 0.3})],
        cams=[cam(0.0, [4.4, 1.4, 4.05], [4.65, 1.4, 4.03], [8.6, 1.05, 4.0], [8.6, 1.05, 4.0], lens=48)],
        fx=[{'type': 'flash', 'at': round(t, 3), 'dur': 0.05} for t in (STAR - 0.1, STAR)])
st.shot('S19', ST, props=[P('car', 'car', pos=[CX, 0, CZ], rot=[0, PI / 2, 0], opts=CAR), BIKE([CX + 1.1, 0, CZ - 2.55], rot=face(-150), shades=True, look=[0.15, 0.3])],
        cams=[cam(0.0, [CX + 2.7, 1.3, CZ - 5.6], [CX + 2.2, 1.15, CZ - 4.75], [CX + 0.45, 0.75, CZ - 1.6], [CX + 0.3, 0.68, CZ - 2.0], lens=46)])
st.shot('S20', ST, actors=[act('chauffeur', [CX + 1.45, 0, CZ - 0.35], -90, 'presentL', 'unimpressed')],
        props=[P('car', 'car', pos=[CX, 0, CZ], rot=[0, PI / 2, 0], opts={**CAR, 'rearDoorAt': 0.05, 'rearDoor': 1.2}),
               BIKE([CX + 1.6, 0, CZ + 2.9], rot=face(180), shades=True, speed=1.4, look=[0.15, -0.4], keys=[k(0.0, to=[CX + 1.45, 0, CZ + 1.05], dur=st.dur('S20'), ease='out')])],
        cams=[cam(0.0, [CX + 5.4, 1.5, CZ + 0.95], [CX + 5.15, 1.5, CZ + 0.9], [CX + 1.0, 1.12, CZ + 0.35], [CX + 1.0, 1.12, CZ + 0.35], lens=46)])
st.shot('S21', ST, actors=[act('chauffeur', [CX - 0.4, 0.12, CZ - 0.15], 180, 'drive', 'unimpressed', keys=[k(1.2, expr='sad')])],
        props=[P('car', 'car', pos=[CX, 0, CZ], rot=[0, PI / 2, 0], opts=CAR), BIKE([CX + 0.05, 0.61, CZ + 0.85], rot=face(165), scale=0.82, shades=True, look=[0.2, 0.4])],
        cams=[cam(0.0, [CX + 1.2, 1.95, CZ - 3.0], [CX + 0.9, 1.85, CZ - 2.45], [CX - 0.1, 1.3, CZ + 0.2], [CX - 0.13, 1.32, CZ + 0.15], lens=48, ease='out')])
st.card('S07', 'SANS CYCLISTE'); st.card('S14', 'RELAXÉ')
st.cue('sfx:gasp', 'S01', 0.4, 0.4); st.cue('sfx:spring', 'S02', 0.25, 0.25); st.cue('whoosh', 'S02', 0.65, 0.3, 0.6, 500, 3000); st.cue('whoosh', 'S03', 0.1, 0.4, 1.0, 400, 3500)
st.cue('sfx:siren', 'S04', 0.0, 0.3); st.cue('engine', 'S04', 0.0, 0.35, st.dur('S04')); st.cue('sfx:grunt', 'S05', 0.3, 0.3)
st.cue('clack', 'S06', st.at('S06', 'L06', 4) - 0.05, 0.5); st.cue('sfx:whistle', 'S07', 0.3, 0.35); st.cue('thud', 'S07', 0.07, 0.45)
st.cue('pop', 'S08', st.at('S08', 'L08', 1) - 0.05, 0.45); st.cue('whoosh', 'S09', 0.3, 0.4, 0.8, 400, 3000); st.cue('sfx:fanfare', 'S09', 0.5, 0.35)
st.cue('sfx:choir', 'S10', 0.1, 0.25); st.cue('sfx:sniff', 'S11', 0.5, 0.3); [st.cue('sfx:pour', 'S12', t, 0.25) for t in (0.2, 0.8)]
st.cue('thud', 'S13', 0.4, 0.3); st.cue('thud', 'S14', 0.07, 0.45); st.cue('thud', 'S14', st.at('S14', 'L13', 6) - 0.05, 0.8); st.cue('sfx:spring', 'S15', 0.2, 0.2)
st.cue('sfx:paper', 'S16', 0.1, 0.45); st.cue('clack', 'S16', 0.5, 0.5); st.cue('sfx:squeak', 'S17', 0.5, 0.3)
[st.cue('clack', 'S18', round(t, 3), 0.3) for t in sorted(FL0 + FL1)]; st.cue('sfx:carDoor', 'S20', 0.1, 0.35); st.cue('engine', 'S21', 0.0, 0.3, st.dur('S21'))
st.write('Le vélo', {
    'official': {'preset': 'lemec_glasses', 'seed': 21}, 'docteur': {'preset': 'doctor'},
    **{a: {'preset': 'sportif', 'seed': s, 'suit': c, 'hat': 'bikehelmet', 'hatColor': '#F4F4F0', 'bib': n} for (a, c, n), s in zip(RIDERS, (11, 13, 17))},   # r1 #12 and r2 #27 also sit on the podium
    **{f'fan{i}': {'preset': p, 'seed': 40 + i} for i, p in enumerate(('femme', 'tourist', 'mamie', 'gamin', 'fermier', 'chef', 'worker'))},
    'ph0': {'preset': 'journaliste'}, 'ph1': {'preset': 'lemec_brown', 'seed': 7},
    'chauffeur': {'preset': 'lemec', 'hat': 'copcap', 'hatColor': '#1C1C22', 'gloves': '#F4F4F0', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}})
