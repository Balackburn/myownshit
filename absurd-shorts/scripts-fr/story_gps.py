#!/usr/bin/env python3
"""Le GPS (story 27): he asks his GPS to take him far from his problems (three small grey storm clouds with faces). "In 3000 km,
turn right." He drives all night. In the desert his problems are already waiting: they took the plane. He leaves again. The North
Pole: his problems are skiing. A rocket to the Moon: his problems booked the seats next to him. On the Moon the GPS recalculates:
"shortest route: apologise". He switches the GPS off. Today he lives on the Moon. With his problems."""
from story_kit import *

st = Story('gps')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 7), ('S03', 'L02', 0), ('S04', 'L02', 4), ('S05', 'L03', 0), ('S06', 'L04', 0), ('S07', 'L04', 3), ('S08', 'L05', 0), ('S09', 'L06', 0),
         ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L10', 0), ('S14', 'L11', 0), ('S15', 'L12', 0), ('S16', 'L13', 0), ('S17', 'L14', 0), ('S18', 'L15', 0)])
PI = math.pi
SEAT = (0.05, 0.12, -0.4)
def seat(x, z, y=0.0): return [x + SEAT[0], y + SEAT[1], z + SEAT[2]]
CAR = lambda x=0.0, z=0.0, keys=None, gps='LOIN DE MES\nPROBLÈMES': [P('car', 'car', pos=[x, 0, z], opts={'color': '#C9473A'}, **({'keys': keys} if keys else {})),
                                                                      P('gps', 'gpsDevice', opts={'text': gps.split('\n')[0]}, on={'actor': 'car', 'offset': [0.98, 1.12, -0.25]})]
PB = lambda i, pos, **o: P(f'pb{i}', 'problemCloud', pos=pos, opts={'seed': 11 + i, 'mood': ['smug', 'angry', 'smug'][i % 3], **o})
TRIO = lambda c, y=2.3, dx=0.75, **o: [PB(i, [c[0] + (i - 1) * dx, y + (0.12 if i == 1 else 0), c[2] + (0.1 if i == 1 else 0)], **o) for i in range(3)]
SCREEN = lambda text, **o: P('scr', 'gpsScreen', pos=[0, 1.2, 0], opts={'text': text, **{'w': 0.5, **o}})
SCREEN_CAM = [cam(0.0, [0.02, 1.2, 1.0], [0.02, 1.2, 0.9], [0, 1.2, 0], [0, 1.2, 0], lens=44)]
NIGHT = {'hemi': 0.45, 'sky': '#4A5C8A', 'ground': '#1B2238', 'keyI': 0.55, 'key': '#B8C8FF'}

# 1-5: the request; the problems; "in 3000 km turn right"; all night
st.shot('S01', 'parisStreet', actors=[act('mec', seat(0.0, 3.0), 90, 'drive', 'neutral')], props=CAR(0.0, 3.0),
        cams=[cam(0.0, [2.6, 1.7, 6.6], [2.5, 1.7, 6.3], [0.55, 1.2, 2.7], [0.55, 1.2, 2.7], lens=44)])
st.shot('S02', 'parisStreet', actors=[act('mec', seat(0.0, 3.0), 90, 'drive', 'unimpressed', keys=[k(0.2, look=[0.2, 2.6, 2.6])])], props=CAR(0.0, 3.0) + TRIO([0.3, 0, 2.6], y=2.45, dx=0.8, bolt=True),
        cams=[cam(0.0, [0.9, 1.3, 7.6], [0.85, 1.35, 7.2], [0.3, 1.75, 2.6], [0.3, 1.8, 2.6], lens=44)])
st.shot('S03', 'parisStreet', props=[SCREEN('CALCUL DE\nL\'ITINÉRAIRE…', recalc=False)], cams=SCREEN_CAM)
st.shot('S04', 'parisStreet', props=[SCREEN('DANS 3000 KM,\nTOURNEZ À DROITE')], cams=[cam(0.0, [0.03, 1.2, 0.98], [0.03, 1.2, 0.84], [0, 1.2, 0], [0, 1.2, 0], lens=44)])
D5 = st.dur('S05')
st.shot('S05', 'spaceDark', light=NIGHT, actors=[act('mec', seat(-3.0, 0.0), 90, 'drive', 'sleepy', keys=[k(0, to=seat(3.0, 0.0), glide=True, dur=D5, ease='linear', clip='drive', then='drive', face='keep')])],
        props=[P('sand', 'carpet', pos=[0, -0.02, 0], opts={'w': 300, 'd': 300, 'color': '#3A3550', 'inner': '#3A3550'}), P('road', 'carpet', pos=[0, -0.005, 0.0], opts={'w': 300, 'd': 3.0, 'color': '#2A2D36', 'inner': '#2A2D36'}),
               P('car', 'car', pos=[-3.0, 0, 0.0], opts={'color': '#C9473A'}, keys=[k(0, to=[3.0, 0, 0.0], dur=D5, ease='linear')]), P('moon', 'moon', pos=[-6, 9, -30], opts={'radius': 2.0})],
        cams=[cam(0.0, [-1.6, 1.4, 7.5], [1.6, 1.4, 7.5], [-1.0, 1.0, 0.0], [1.0, 1.0, 0.0], lens=44)])
# 6-9: the desert: they were waiting (sunglasses), they took the plane; he leaves again
st.shot('S06', 'desert', actors=[act('mec', [0.6, 0, -0.2], -30, 'stand', 'happy')], props=CAR(-1.2, -1.2) + TRIO([0.6, 0, -2.8], y=1.1, dx=0.9, glasses=True),
        cams=[cam(0.0, [1.4, 1.5, 4.2], [1.35, 1.5, 3.9], [0.4, 1.15, -1.0], [0.4, 1.15, -1.0], lens=44)])
st.shot('S07', 'desert', actors=[act('mec', [0.8, 0, 0.3], -60, 'doubleTake', 'shocked')], props=TRIO([-0.4, 0, -0.6], y=1.4, dx=0.7, glasses=True),
        cams=[cam(0.0, [0.5, 1.55, 3.9], [0.48, 1.55, 3.6], [0.3, 1.45, -0.2], [0.3, 1.45, -0.2], lens=44)])
st.shot('S08', 'desert', props=TRIO([0.0, 0, 0.0], y=1.3, dx=0.8, suitcase=True, ticket=True) + [P('jet', 'plane', pos=[-30, 14, -45], ry=-10, keys=[k(0.0, to=[25, 18, -55], dur=st.dur('S08'), ease='linear')])],
        cams=[cam(0.0, [0.1, 1.35, 3.1], [0.1, 1.38, 2.85], [0.0, 1.6, 0.0], [0.0, 1.62, 0.0], lens=44)])
D9 = st.dur('S09')
st.shot('S09', 'desert', actors=[act('mec', seat(-1.0, 0.0), 90, 'drive', 'angry', keys=[k(0, to=seat(9.0, 0.0), glide=True, dur=D9, ease='in', clip='drive', then='drive', face='keep')])],
        props=[P('car', 'car', pos=[-1.0, 0, 0.0], opts={'color': '#C9473A'}, keys=[k(0, to=[9.0, 0, 0.0], dur=D9, ease='in')])] + TRIO([-1.6, 0, -1.6], y=1.4, dx=0.8, glasses=True, mood='happy'),
        cams=[cam(0.0, [-0.2, 1.3, 5.6], [0.2, 1.3, 5.4], [-0.3, 1.0, -0.4], [0.6, 1.0, -0.4], lens=44)])
# 10-13: the North Pole: they ski; the rocket: they booked the seats next to him
st.shot('S10', 'snow', actors=[act('mec', [0.0, 0, 0.0], 0, 'scared', 'sad')], props=[P('np', 'signBoard', pos=[-0.75, 0, -0.9], opts={'text': 'PÔLE NORD', 'w': 1.0, 'h': 0.32, 'height': 1.85, 'bg': '#F4F1E8', 'fg': '#2C4A8A', 'frame': '#C8322A'})],
        cams=[cam(0.0, [0.35, 1.5, 3.0], [0.33, 1.5, 2.75], [-0.2, 1.3, -0.3], [-0.2, 1.3, -0.3], lens=44)])
D11 = st.dur('S11')
st.shot('S11', 'snow', props=[PB(i, [-1.6 + i * 0.75, 1.55 - i * 0.18, -0.6 - i * 0.5], skis=True, mood='happy', size=1.35, keys=[k(0.0, to=[0.6 + i * 0.75, 0.75 - i * 0.18, 0.4 - i * 0.5], dur=D11, ease='linear')]) for i in range(3)],
        cams=[cam(0.0, [0.0, 1.35, 3.6], [0.1, 1.3, 3.4], [-0.5, 1.05, -0.6], [0.4, 0.85, -0.3], lens=44)])
D12 = st.dur('S12')
st.shot('S12', 'desert', props=[P('rk', 'rocket', pos=[0, 0, -2.0], scale=1.4, keys=[k(0.1, to=[0, 7, -2.0], dur=D12 - 0.1, ease='inOut')]), P('smk', 'dustPuff', pos=[0, 0.1, -2.0], scale=3.0), P('fl', 'flame', on={'actor': 'rk', 'offset': [0, 0.1, 0]}, rot=[3.1416, 0, 0], scale=2.5)],
        cams=[cam(0.0, [0.5, 1.6, 7.2], [0.48, 1.9, 6.9], [0.0, 2.6, -2.0], [0.0, 6.4, -2.0], lens=44, shake=0.012)])
SEATS = [P(f'st{i}', 'chair', pos=[x, 0, 0.0], opts={'color': '#3A3D44'}) for i, x in enumerate((-0.7, 0.0, 0.7))]
st.shot('S13', 'spaceDark', actors=[act('mec', [0.0, 0, 0.0], 0, 'sit', 'unimpressed')], props=SEATS + [PB(0, [-0.7, 1.0, 0.05], belt=True), PB(1, [0.7, 1.0, 0.05], belt=True, mood='smug')],
        cams=[cam(0.0, [0.1, 1.4, 3.6], [0.1, 1.4, 3.35], [0.0, 1.1, 0.0], [0.0, 1.1, 0.0], lens=44)])
# 14-18: on the Moon the GPS recalculates: "apologise"; he switches it off; he lives there, with his problems
MOON = [P('ground', 'moonSurface', pos=[0, 0, 0], opts={'r': 40}), P('earth', 'earthGlobe', pos=[-6, 10, -40], opts={'radius': 3.2, 'spin': 0.1})]
HELMET = P('dome', 'glassDome', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.05, 0]}, opts={'radius': 0.32, 'opacity': 0.2, 'base': False})
st.shot('S14', 'spaceDark', actors=[act('mec', [0.0, 0, 0.0], 0, 'readPhone', 'unimpressed')], props=MOON + [HELMET, P('hgps', 'gpsDevice', opts={'text': 'RECALCUL…'}, on={'actor': 'mec', 'hand': 'R', 'rot': [-1.2, 0, 0], 'offset': [0, -0.12, 0.04]}, scale=1.5)] + TRIO([0.0, 0, -1.4], y=2.2, dx=0.8),
        cams=[cam(0.0, [0.35, 1.55, 3.0], [0.33, 1.55, 2.75], [0.0, 1.5, -0.4], [0.0, 1.5, -0.4], lens=44)])
st.shot('S15', 'spaceDark', props=[SCREEN('ITINÉRAIRE LE PLUS COURT :\nVOUS EXCUSER', dest='CHEZ ELLE', w=0.42)], cams=[cam(0.0, [0.02, 1.2, 1.12], [0.02, 1.2, 1.0], [0, 1.2, 0], [0, 1.2, 0], lens=44)])
st.shot('S16', 'spaceDark', props=[P('scr', 'gpsScreen', pos=[0, 1.2, 0], opts={'text': 'VOUS EXCUSER', 'w': 0.5}, keys=[k(0.55, visible=False)]), P('scr2', 'gpsScreen', pos=[0, 1.2, 0.001], opts={'off': True, 'w': 0.5}, visible=False, keys=[k(0.55, visible=True)])],
        cams=[cam(0.0, [0.02, 1.2, 1.05], [0.02, 1.2, 0.95], [0, 1.2, 0], [0, 1.2, 0], lens=44)])
st.shot('S17', 'spaceDark', props=MOON + [P('house', 'cottage', pos=[0.3, 0, -1.5], scale=0.35, opts={'w': 6, 'd': 6, 'h': 2.6, 'rh': 1.6, 'color': '#F2D06B', 'roof': '#C9473A'}), P('mail', 'noticeBoard', pos=[1.6, 0, -0.4], opts={'text': 'LE MEC', 'style': 'tag', 'w': 0.4, 'h': 0.14, 'height': 0.9})],
        cams=[cam(0.0, [1.2, 1.6, 6.0], [1.1, 1.65, 5.6], [0.3, 1.3, -1.5], [0.3, 1.35, -1.5], lens=44)])
st.shot('S18', 'spaceDark', actors=[act('mec', [0.0, 0, 0.0], 160, 'sit', 'unimpressed')], props=MOON + [HELMET, P('ch', 'chair', pos=[0.0, 0, 0.0], ry=160, opts={'color': '#2F7F8C'}), PB(0, [-0.85, 1.25, 0.1], glasses=True), PB(1, [0.85, 1.2, -0.05], glasses=True, mood='happy'), PB(2, [0.1, 1.95, 0.55], glasses=True), P('earth2', 'earthGlobe', pos=[5, 9, 40], opts={'radius': 3.2, 'spin': 0.1})],
        cams=[cam(0.0, [-0.7, 1.45, -3.4], [-0.65, 1.47, -3.15], [0.0, 1.15, 0.0], [0.0, 1.17, 0.0], lens=44)])
st.card('S04', '3000 KM'); st.card('S15', 'VOUS EXCUSER')
st.cue('sfx:beep', 'S01', 0.5, 0.25); st.cue('thunder', 'S02', 0.25, 0.35); st.cue('sfx:beep', 'S04', 0.1, 0.3); st.cue('engine', 'S05', 0.0, 0.35); st.cue('sfx:jet', 'S08', 0.1, 0.25)
st.cue('engine', 'S09', 0.0, 0.45); st.cue('whoosh', 'S09', 0.3, 0.4); st.cue('gust', 'S10', 0.0, 0.3); st.cue('whoosh', 'S11', 0.1, 0.35); st.cue('sfx:jet', 'S12', 0.2, 0.45); st.cue('thud', 'S12', 0.25, 0.4)
st.cue('sfx:beep', 'S14', 0.3, 0.3); st.cue('sfx:beep', 'S15', 0.1, 0.3); st.cue('sfx:click', 'S16', 0.55, 0.45); st.cue('pop', 'S17', 0.1, 0.25)
st.write('Le GPS')
