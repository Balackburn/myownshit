#!/usr/bin/env python3
"""La canicule (story 34): it was 40 degrees. This man opened the fridge to cool down, then stepped inside and closed the door. He stayed there
all summer — he even had his birthday party in it, and the postman delivered his mail to the vegetable drawer. In September he finally came out:
outside, it was snowing. So he went back into the fridge. To warm up. Natural look (engine/look.js: scene light probe, soft shadows)."""
from story_kit import *

st = Story('canicule', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 6), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0),
         ('S08', 'L07', 0), ('S09', 'L07', 6), ('S10', 'L08', 0), ('S11', 'L09', 0), ('S12', 'L10', 0), ('S13', 'L11', 0)])
def add(a, b): return [round(a[i] + b[i], 3) for i in range(3)]

KD = {'fridge': False}
FR = [-2.7, 0, -3.1]                     # the fridge (bigFridge origin: floor centre, the opening at z + 0.41)
SEAT = [-2.7, 0.22, -3.2]                # the mec cross-legged on the crisper's glass top
FRONT = [-2.45, 0, -2.0]                 # standing in front of the fridge, beside the door's swing
FRIDGE = lambda **o: P('fridge', 'bigFridge', pos=FR, opts={'mode': 'lived', 'notes': 6, **o})
INSIDE = lambda: [cam(0.0, [-2.62, 1.38, -1.0], [-2.63, 1.37, -1.2], [-2.7, 1.3, -3.2], [-2.7, 1.3, -3.2], lens=44)]

# 1: the heatwave: sweating, fanning himself, the thermometer climbs to 40° and shakes, the fan, the wilting plant
st.shot('S01', 'kitchenDay', setOpts=KD, actors=[act('mec', [-0.95, 0, -1.7], 8, 'fanSide', 'pain', fx={'sweat': True})],
        props=[FRIDGE(mode='full'), P('thermo', 'thermometer', pos=[-1.85, 1.55, -3.57], opts={'w': 0.3, 'h': 1.0, 'temp': 40, 'from': 27, 'riseAt': 0.12, 'dur': 0.9})],
        cams=[cam(0.0, [-0.85, 1.85, 0.9], [-0.86, 1.85, 0.72], [-1.15, 1.78, -2.0], [-1.15, 1.79, -2.0], lens=44)])
# 2-3: he opens the fridge: cold light and mist; then the fridge's view of him: eyes shut, bliss, vapour on his face
T2 = 0.32
st.shot('S02', 'kitchenDay', setOpts=KD, actors=[act('mec', FRONT, 148, 'stand', 'determined', fx={'sweat': True}, keys=[k(T2 - 0.15, clip='giveItem'), k(T2 + 0.5, expr='surprisedHappy')])],
        props=[FRIDGE(mode='full', openAt=T2)],
        cams=[cam(0.0, [-0.45, 1.9, -2.5], [-0.55, 1.9, -2.42], [-2.6, 1.78, -2.12], [-2.6, 1.79, -2.12], lens=44)])
st.shot('S03', 'kitchenDay', setOpts=KD, actors=[act('mec', FRONT, 180, 'stand', 'relieved')],
        props=[FRIDGE(mode='full', open=1)],
        cams=[cam(0.0, [-2.62, 1.72, -3.0], [-2.62, 1.72, -2.95], add(FRONT, [0, 1.98, 0]), add(FRONT, [0, 1.99, 0]), lens=44)], look={'exposure': 0.85})
# 4: he climbs in (side view) and sits cross-legged on the crisper
T4 = 0.25
st.shot('S04', 'kitchenDay', setOpts=KD, actors=[act('mec', FRONT, 180, 'walk', 'happy', keys=[k(T4, to=add(SEAT, [0.05, 0, 0.25]), dur=0.5, clip='boxSneak'), k(T4 + 0.5, clip='sitFloor', to=SEAT, dur=0.25, face=0, then='sitFloor')])],
        props=[FRIDGE(mode='lived', open=1)],
        cams=[cam(0.0, [-3.55, 1.85, 0.55], [-3.5, 1.84, 0.4], [-2.6, 1.3, -2.6], [-2.62, 1.25, -2.65], lens=44)])
# 5: he pulls the door shut from inside: the light goes, the fridge rocks
T5 = 0.35
st.shot('S05', 'kitchenDay', setOpts=KD, actors=[act('mec', SEAT, 0, 'sitFloor', 'smug')],
        props=[FRIDGE(mode='lived', open=1, closeAt=T5, shakeAt=T5 + 0.38, hanger='NE PAS|DÉRANGER')],
        cams=[cam(0.0, [-1.6, 1.45, 0.6], [-1.66, 1.45, 0.42], [-2.7, 1.1, -3.0], [-2.7, 1.1, -3.0], lens=44)])
# 6: all summer inside: a yogurt, the calendar flipping (JUILLET, AOÛT)
st.shot('S06', 'kitchenDay', setOpts=KD, look={'exposure': 0.8, 'bloom': 0.15}, actors=[act('mec', SEAT, 0, 'sitFloorSpoon', 'happy')],
        props=[FRIDGE(mode='lived', light=True, open=1, mist=False), P('yog', 'yogurt', on={'actor': 'mec', 'hand': 'L'}, opts={'open': True}),
               P('cal', 'monthCalendar', pos=[-2.3, 1.5, -3.49], ry=0, opts={'months': ['JUIN', 'JUILLET', 'AOÛT'], 'flipAt': 0.35, 'dur': 0.5, 'w': 0.26, 'h': 0.34})],
        cams=INSIDE())
# 7: his birthday party in the fridge: hat, cake, garland, confetti, the eggs in party hats; he blows the candles out
TB = st.at('S07', 'L06', 6) + 0.15
st.shot('S07', 'kitchenDay', setOpts=KD, actors=[act('mec', SEAT, 0, 'sitFloorClap', 'laugh', keys=[k(TB - 0.3, clip='sitFloorBlow', expr='kiss'), k(TB + 0.35, clip='sitFloorClap', expr='bigGrin')])],
        props=[FRIDGE(mode='party', light=True, open=0.82, mist=False), P('hat', 'partyHat', on={'actor': 'mec', 'joint': 'head', 'offset': [0.05, 0.5, 0.0]}, opts={'tilt': -0.2}),
               P('cake', 'birthdayCake', pos=[-2.7, 0.58, -2.86], scale=0.85, opts={'candles': 5, 'outAt': TB})],
        cams=[cam(0.0, [-2.22, 1.3, -0.72], [-2.24, 1.29, -0.86], [-2.75, 1.1, -3.15], [-2.75, 1.1, -3.15], lens=44)], look={'exposure': 0.8, 'bloom': 0.15})
# 8-9: the postman opens the fridge, the mec waves; the crisper slides out and a letter drops in among the lettuces
st.shot('S08', 'kitchenDay', setOpts=KD, actors=[act('facteur', [-2.05, 0, -2.15], 240, 'giveItem', 'smug'), act('mec', SEAT, 0, 'sitFloorWave', 'happy')],
        props=[FRIDGE(mode='lived', light=True, openAt=0.05, letters=2, mist=False), P('env', 'envelope', on={'actor': 'facteur', 'hand': 'R'}, opts={'to': 'M. LE MEC', 'addr': 'BAC À LÉGUMES', 'color': '#F2C94C', 'bold': True, 'w': 0.3})],
        cams=[cam(0.0, [-3.25, 1.85, -0.1], [-3.23, 1.85, -0.22], [-2.35, 1.45, -2.6], [-2.35, 1.45, -2.6], lens=50)], look={'exposure': 0.8, 'bloom': 0.15})
T9 = 0.12
st.shot('S09', 'kitchenDay', setOpts=KD, actors=[act('mec', SEAT, 0, 'sitFloor', 'happy')],
        props=[FRIDGE(mode='lived', light=True, open=1, letters=2, drawerAt=T9, mist=False),
               P('env2', 'envelope', pos=[-2.62, 0.62, -2.35], rot=[-1.2, 0.2, 0.3], opts={'to': 'M. LE MEC', 'addr': 'BAC À LÉGUMES', 'color': '#F2C94C', 'bold': True, 'w': 0.3}, keys=[k(T9 + 0.4, to=[-2.6, 0.3, -2.58], dur=0.35, ease='in'), k(T9 + 0.4, rotTo=[-1.5, 0.1, 0.6], dur=0.35)])],
        cams=[cam(0.0, [-2.5, 1.2, -1.85], [-2.52, 1.15, -1.95], [-2.64, 0.3, -2.6], [-2.64, 0.3, -2.6], lens=44)], look={'exposure': 0.8, 'bloom': 0.15})
# 10: September: the door opens in a cloud of vapour, he comes out frozen stiff (frost, icicles, breath), shivering
T10 = 0.2
st.shot('S10', 'kitchenDay', setOpts={'fridge': False, 'cold': True}, look={'tint': [0.9, 0.97, 1.08], 'sunColor': '#DCE8FF', 'warm': 0.3, 'sat': 0.92}, actors=[act('mec', SEAT, 0, 'sitFloor', 'cold', fx={'frozen': True, 'breath': True, 'shiver': True},
        keys=[k(T10 + 0.35, to=[-2.66, 0.22, -2.74], dur=0.35, glide=True, face='keep'), k(T10 + 0.75, clip='frozenTopple', params={'dur': 0.5}, to=[-2.66, 0.0, -2.25], dur=0.5, glide=True, face='keep', then='frozenTopple')])],
        props=[FRIDGE(mode='lived', light=True, openAt=T10)],
        cams=[cam(0.0, [-1.9, 1.3, 0.85], [-1.95, 1.25, 0.7], [-2.6, 0.85, -2.45], [-2.6, 0.8, -2.4], lens=44)])
# 11: outside, the street under snow: frozen on the doorstep, a pharmacy cross reads -12°, a bundled-up passer-by
COLD = {'sunColor': '#EAF2FF', 'sun': 0.55, 'hazeColor': '#E4EAEE', 'hazeNear': 14, 'hazeFar': 90, 'warm': 0.25, 'sat': 0.95, 'elevation': 30, 'deepSky': False, 'sunDisc': False, 'shafts': 0}
D11 = st.dur('S11')
st.shot('S11', 'parisStreet', setOpts={'snow': True, 'snowN': 7000, 'snowSize': 0.15, 'snowX': 9}, actors=[act('mec', [9.55, 0, 2.0], -25, 'hugCold', 'shocked', fx={'frozen': True, 'breath': True, 'shiver': True}, keys=[k(0.5, expr='cold')]),
        act('passant', [8.3, 0, -9.0], 0, 'walk', 'neutral', keys=[k(0.0, to=[8.3, 0, -5.5], dur=D11)])],
        props=[P('pharma', 'pharmacyCross', pos=[9.75, 3.6, -1.0], ry=0, opts={'text': '−12°', 'size': 0.85, 'period': 1.0})],
        cams=[cam(0.0, [8.6, 1.5, 7.0], [8.62, 1.52, 6.75], [9.3, 1.75, 1.0], [9.3, 1.76, 1.0], lens=44)], look=COLD)
# 12: back home at a run, he dives into the fridge, the door slams, it rocks
T12 = 0.15
st.shot('S12', 'kitchenDay', setOpts={'fridge': False, 'cold': True}, look={'tint': [0.9, 0.97, 1.08], 'sunColor': '#DCE8FF', 'warm': 0.3, 'sat': 0.92}, actors=[act('mec', [1.4, 0, -1.2], -110, 'run', 'determined', fx={'frozen': 'thaw', 'breath': True},
        keys=[k(T12, to=FRONT, dur=0.85), k(T12 + 0.9, to=SEAT, dur=0.3, clip='sitFloor', face=0, then='sitFloor')])],
        props=[FRIDGE(mode='lived', open=1, closeAt=T12 + 1.3, shakeAt=T12 + 1.62)],
        cams=[cam(0.0, [0.7, 1.6, 1.3], [0.6, 1.58, 1.15], [-1.5, 1.0, -2.35], [-2.2, 1.0, -2.7], lens=44)])
TR = st.at('S13', 'L11', 2)
# 13: to warm up: wrapped in a blanket with a hot chocolate, fairy lights, the fridge's thermometer at 4°
st.shot('S13', 'kitchenDay', setOpts=KD, actors=[act('mec', SEAT, 0, 'sitFloorSip', 'relieved', fx={'blush': True}, keys=[k(1.3, expr='happy')])],
        props=[FRIDGE(mode='cosy', light=True, open=1, mist=False), P('blanket', 'shoulderBlanket', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.42, 0]}),
               P('mug', 'hotMug', on={'actor': 'mec', 'hand': 'R'}), P('thermo4', 'thermometer', pos=[-2.33, 1.42, -3.49], ry=0, opts={'w': 0.17, 'h': 0.52, 'temp': 4}, keys=[k(0, scale=0.01, dur=0), k(TR, scale=1.15, dur=0.18, ease='out'), k(TR + 0.18, scale=1.0, dur=0.12)])],
        cams=[cam(0.0, [-2.6, 1.32, -0.9], [-2.62, 1.3, -1.15], [-2.7, 1.22, -3.2], [-2.7, 1.22, -3.2], lens=44, ease='out')], look={'sunColor': '#FFD9A6', 'exposure': 0.85, 'bloom': 0.18})
st.card('S01', '40°'); st.card('S06', "TOUT L'ÉTÉ"); st.card('S10', 'SEPTEMBRE')
st.cue('whoosh', 'S01', 0.0, 0.12, 1.6, 300, 1200); st.cue('sfx:squeak', 'S02', T2, 0.35); st.cue('gust', 'S02', T2 + 0.1, 0.25, 1.2)
st.cue('sfx:step', 'S04', T4 + 0.2, 0.3); st.cue('thud', 'S05', T5 + 0.35, 0.45); st.cue('sfx:paper', 'S06', 0.45, 0.3); st.cue('sfx:paper', 'S06', 1.0, 0.3)
st.cue('sfx:fanfare', 'S07', 0.05, 0.22); st.cue('sfx:poof', 'S07', TB, 0.35); st.cue('sfx:squeak', 'S08', 0.05, 0.3); st.cue('sfx:paper', 'S09', T9 + 0.6, 0.35)
st.cue('sfx:squeak', 'S10', T10, 0.35); st.cue('thud', 'S10', T10 + 1.25, 0.55); st.cue('gust', 'S10', T10 + 0.1, 0.3, 1.4); st.cue('gust', 'S11', 0.0, 0.3, 1.6); st.cue('sfx:gasp', 'S11', 0.2, 0.35)
st.cue('sfx:stepRun', 'S12', T12, 0.3); st.cue('thud', 'S12', T12 + 1.6, 0.5); st.cue('sfx:gulp', 'S13', 0.6, 0.3); st.cue('sfx:bell', 'S13', 1.5, 0.15)
st.write('La canicule', {'facteur': {'preset': 'cop', 'seed': 96, 'suit': '#2F62B5', 'hatColor': '#F2C94C'},
                         'passant': {'preset': 'lemec_brown', 'hat': 'beanie', 'hatColor': '#C8322A', 'seed': 44, 'glasses': True}})
