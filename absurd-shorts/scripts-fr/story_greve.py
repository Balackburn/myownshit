#!/usr/bin/env python3
"""La grève des nuages: the clouds strike for a rain bonus; firemen water the fields; Christmas without snow; a rainbow a month; 40 days of rain."""
from story_kit import *

st = Story('greve')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 21)])
GREY = {'color': '#9AA4AE', 'color2': '#B0B9C2'}; DARK = {'color': '#6E7680', 'color2': '#808892'}; WHITE = {'color': '#F2F5F8', 'color2': '#FFFFFF'}
def cloud_talk(lid, sid, base='angry', mouth='shocked'):
    t0 = st.SH[sid][0]; e = [[0, base]]
    for w in st.L[lid]['words']: e += [[round(max(0, w['s'] - t0), 3), mouth], [round(max(0, w['e'] - t0 - 0.03), 3), base]]
    return e
CLOUDS = lambda y=4.5, z=-3, opts=GREY, face='angry', signs=None, **kw: [P(f'c{i}', 'cloudChar', pos=[x, y + 0.3 * (i % 2), z], scale=1.1, opts={**opts, 'face': face, 'seed': i + 3, **kw}) for i, x in enumerate((-2.4, 0, 2.4))] + \
    ([P(f's{i}', 'protestSign', pos=[x + 0.2, y - 1.9 + 0.3 * (i % 2), z + 0.6], scale=1.1, opts={'text': t}) for i, (x, t) in enumerate(zip((-2.4, 0, 2.4), signs))] if signs else [])
SKYCAM = [cam(0.0, [0.3, 1.2, 5.6], [0.25, 1.25, 5.1], [0, 3.4, -3], [0, 3.5, -3], lens=50)]

st.shot('S01', 'grassland', props=CLOUDS(signs=['GRÈVE', 'PRIME DE\nPLUIE', 'ON LÂCHE\nRIEN']), cams=SKYCAM)
st.shot('S02', 'seabed', setOpts={'dry': True}, actors=[act('fermier', [0, 0, 0], 0, 'lookUp', 'worried')], props=[P('can', 'wateringCan', pos=[0.6, 0, 0.3]), P('scare', 'scarecrow', pos=[-1.4, 0, -1.5])],
        cams=MS(0, 0, h=1.45, d=3.0))
st.shot('S03', 'seabed', setOpts={'dry': True}, actors=[act('fermier', [-0.6, 0, 0], 20, 'flail', 'scared'), act('fermier2', [0.7, 0, -0.3], -20, 'scared', 'shocked')], cams=WS(0, 0, h=1.4, d=5.2, look_h=1.1))
st.shot('S04', 'office', actors=[act('ministre', [0, 0, -0.4], 0, 'explain', 'suspicious')],
        props=[P('c1', 'cloudChar', pos=[-0.75, 1.0, 0.7], rot=[0, 2.8, 0], scale=0.45, opts={**GREY, 'face': 'grumpy'}), P('c2', 'cloudChar', pos=[0.75, 1.1, 0.8], rot=[0, -2.8, 0], scale=0.45, opts={**GREY, 'face': 'angry', 'seed': 7})],
        cams=WS(0, 0, h=1.5, d=4.6, look_h=1.2))
st.shot('S05', 'office', props=[P('c', 'cloudChar', pos=[0, 0.9, 0], scale=0.6, opts={**GREY, 'expr': cloud_talk('L05', 'S05')})], cams=[cam(0.0, [0.1, 1.35, 1.9], [0.1, 1.35, 1.7], [0, 1.3, 0], [0, 1.3, 0], lens=44)])
st.shot('S06', 'office', actors=[act('ministre', [0, 0, -0.4], 0, 'slamTable', 'angry')],
        props=[P('c1', 'cloudChar', pos=[-1.1, 0.9, 0.6], scale=0.5, opts={**GREY, 'face': 'angry'}, keys=[k(0.3, to=[-3.5, 1.4, 1.0], dur=0.8, ease='in')]),
               P('c2', 'cloudChar', pos=[1.1, 1.0, 0.7], scale=0.5, opts={**GREY, 'face': 'angry', 'seed': 7}, keys=[k(0.35, to=[3.5, 1.4, 1.0], dur=0.8, ease='in')])],
        cams=WS(0, 0, h=1.5, d=4.6, look_h=1.2, shake=0.02))
st.shot('S07', 'grassland', actors=[act('pompier', [-0.4, 0, 0.6], 20, 'salute', 'smug'), act('pompier2', [0.5, 0, 0.8], -20, 'handsOnHips', 'smug')], props=[P('truck', 'fireTruck', pos=[0, 0, -1.6])],
        cams=WS(0, 0, h=1.4, d=6.5, look_h=1.3))
st.shot('S08', 'grassland', props=[P('truck', 'fireTruck', pos=[3, 0, -2], rot=[0, 0.3, 0], opts={'spray': [[0.1, True]]})], cams=[cam(0.0, [-3, 1.2, 8], [-2.8, 1.3, 7.5], [0, 1.5, -3], [0, 1.6, -3], lens=46)])
st.shot('S09', 'grassland', props=CLOUDS(y=6, face='angry') + [P('truck', 'fireTruck', pos=[0, 0, -2.5], rot=[0, 0.3, 0])], cams=[cam(0.0, [0.4, 0.8, 9], [0.35, 0.85, 8.5], [0, 3.6, -3], [0, 3.8, -3], lens=50, shake=0.015)])
st.shot('S10', 'grassland', props=CLOUDS(y=4.0, z=-1.5, opts=DARK, face='angry'), cams=[cam(0.0, [0.2, 2.5, 7.5], [0.2, 2.6, 6.6], [0, 3.8, -1.5], [0, 3.9, -1.5], lens=46, shake=0.02)])
st.shot('S11', 'grassland', actors=[act('bonhomme', [0, 0, 0], 0, 'idle', 'sad')], props=[P('fir', 'giantFir', pos=[1.0, 0, -0.6], opts={'h': 1.6})], cams=MS(0.3, 0, h=1.0, d=3.0))
st.shot('S12', 'parisStreet', actors=[act(f'g{i}', [6 + x, 0, 0], 0, 'holdSign', 'angry', scale=0.75) for i, x in enumerate((-0.8, 0, 0.8))],
        props=[P(f's{i}', 'protestSign', opts={'text': t}, on={'actor': f'g{i}', 'hand': 'R', **SIGN_UP}) for i, t in enumerate(['ON VEUT\nDE LA NEIGE', 'NEIGE\nPOUR TOUS', 'NOËL\nBLANC'])],
        cams=WS(6, 0, h=1.1, d=4.8, look_h=1.0))
st.shot('S13', 'office', actors=[act('ministre', [0, 0, 0], 0, 'bigShrug', 'sad')], cams=MS(0, 0, h=1.5, d=2.6))
st.shot('S14', 'grassland', actors=[act('ministre', [-1.6, 0, 1.0], 40, 'present', 'happy')], props=CLOUDS(y=3.5, z=-2.5, face='happy') + [P('arc', 'rainbow', pos=[0, 0, -4], opts={'r': 4.5, 't0': 0.2})],
        cams=[cam(0.0, [0.0, 1.4, 9.0], [0.0, 1.5, 8.5], [0, 2.6, -2], [0, 2.7, -2], lens=46)])
st.shot('S15', 'grassland', props=CLOUDS(y=4.5, face='happy', raining=True, rainH=4.0, drops=90), cams=SKYCAM)
st.shot('S16', 'grassland', props=CLOUDS(y=4.5, face='grumpy', raining=True, rainH=4.0, drops=90) + [P('clock', 'wallClock', pos=[0, 2.4, -2.4], scale=2.0, opts={'rate': 5})], cams=SKYCAM)
st.shot('S17', 'parisStreet', props=[P('rain', 'rain', pos=[7, 0, 0], opts={'w': 8, 'd': 6, 'h': 8, 'n': 500, 'speed': 4}),
                                     P('cal', 'noticeBoard', pos=[7, 1.8, -1.0], opts={'text': '40 JOURS', 'style': 'sign', 'w': 1.0, 'h': 0.34, 'popAt': 0.3})], cams=WS(7, 0, h=1.5, d=5.0, look_h=1.6))
st.shot('S18', 'seaSurface', setOpts={'parasols': False, 'shore': 200}, props=[P('eiffel', 'eiffelTower', pos=[0, -14, -40], opts={'h': 40})] +
        [P(f'h{i}', 'cottage', pos=[x, -1.9, z], opts={'w': 5, 'd': 5, 'h': 2.4, 'rh': 1.5, 'color': c, 'roof': '#C9473A'}) for i, (x, z, c) in enumerate([(-8, -14, '#F2D06B'), (7, -18, '#B9A6D6'), (-3, -24, '#9EC7E8')])],
        cams=[cam(0.0, [2, 3.0, 14], [1.8, 3.2, 13], [0, 8, -30], [0, 9, -30], lens=46)])
st.shot('S19', 'pressRoom', actors=[act('ministre', [0, 0, 0], 0, 'podiumTalk', 'sad')],
        props=[P('pod', 'podium', pos=[0, 0, 0.45]), P('dem', 'noticeBoard', pos=[0.45, 1.8, 0.35], opts={'text': 'DÉMISSION', 'style': 'doc', 'w': 0.6, 'h': 0.4, 'popAt': 0.3})], cams=MS(0.2, 0, h=1.55, d=2.9))
st.shot('S20', 'seaSurface', setOpts={'parasols': False, 'shore': 200}, actors=[act('ministreBain', [0, -0.95, 0], 0, 'stand', 'unimpressed', keys=[k(0.9, expr='sad')])],
        cams=[cam(0.0, [0.3, 0.9, 2.6], [0.28, 0.9, 2.4], [0, 0.8, 0], [0, 0.82, 0], lens=44)])
st.card('S01', 'GRÈVE'); st.card('S06', 'NÉGOCIATIONS ROMPUES')
st.cue('thud', 'S01', 0.07, 0.45); st.cue('sfx:static', 'S01', 0.0, 0.15); st.cue('gust', 'S02', 0.0, 0.35, st.dur('S02')); st.cue('sfx:gasp', 'S03', 0.2, 0.5)
st.cue('thud', 'S06', 0.25, 0.8); st.cue('thud', 'S06', 0.07, 0.45); st.cue('whoosh', 'S06', 0.3, 0.5, 0.8, 300, 2500); st.cue('engine', 'S07', 0.0, 0.25, st.dur('S07'))
st.cue('rain', 'S08', 0.1, 0.45, st.dur('S08')); st.cue('thunder', 'S10', 0.1, 0.6); st.cue('sfx:bell', 'S11', 0.3, 0.3); st.cue('pop', 'S14', 0.2, 0.5); st.cue('sfx:choir', 'S14', 0.25, 0.25)
st.cue('rain', 'S15', 0.0, 0.5, st.dur('S15')); st.cue('rain', 'S16', 0.0, 0.5, st.dur('S16')); st.cue('sfx:ticks', 'S16', 0.0, 0.4); st.cue('rain', 'S17', 0.0, 0.7, st.dur('S17')); st.cue('thunder', 'S17', 0.2, 0.5)
st.cue('gust', 'S18', 0.0, 0.4, st.dur('S18')); st.cue('pop', 'S19', 0.3, 0.5); st.cue('gust', 'S20', 0.0, 0.3, st.dur('S20'))
st.write('La grève des nuages', {'fermier': {'preset': 'fermier'}, 'fermier2': {'preset': 'fermier', 'seed': 12, 'facial': 'mustache'}, 'ministre': {'preset': 'politique'},
                                 'pompier': {'preset': 'pompier'}, 'pompier2': {'preset': 'pompier', 'seed': 21}, 'bonhomme': {'type': 'creature', 'name': 'snowman', 'opts': {'seed': 2}},
                                 'g0': {'preset': 'gamin'}, 'g1': {'preset': 'gamin', 'seed': 5}, 'g2': {'preset': 'lyceenne'},
                                 'ministreBain': {'preset': 'politique', 'atlasBody': False, 'suit': '#D9A47E', 'lapel': '#D9A47E', 'tie': '#D9A47E', 'shirt': '#D9A47E', 'cuff': '#D9A47E', 'pants': '#2F62B5'}})
