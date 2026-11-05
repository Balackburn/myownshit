#!/usr/bin/env python3
"""L'escargot: a snail is flashed on the motorway for driving too slowly; trial, a tortoise lawyer, a motorbike, a speeding ticket, a driving school for slugs."""
from story_kit import *

st = Story('escargot')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 20)])
ROAD = 'runway'
SN = lambda x=0, z=0, ry=90, clip='walk', y=0, **kw: act('escargot', [x, y, z], ry, clip, **kw)
MACRO = lambda x=0, z=0, h=0.35, d=1.4: [cam(0.0, [x + 0.25, h, z + d], [x + 0.22, h, z + d - 0.12], [x, 0.25, z], [x, 0.25, z], lens=42)]
RADAR = lambda flash=None, val='0,03', col='#E0413A': [P('cam', 'trafficCamera', pos=[1.4, 0, -1.0], opts={'flashAt': flash} if flash is not None else {}), P('disp', 'speedDisplay', pos=[-1.3, 0, -1.2], opts={'value': val, 'color': col})]
SLUGS = lambda n, z=0: [P(f'l{i}', 'slug', pos=[-0.6 + i * 0.4, 0, z + (i % 2) * 0.12], scale=1.6) for i in range(n)]

st.shot('S01', ROAD, actors=[SN(-0.3, 0, keys=[k(0.0, to=[-0.24, 0, 0], dur=st.dur('S01'), clip='walk')], scale=2.2)], cams=MACRO(-0.1, 0, h=0.4, d=2.6))
st.shot('S02', ROAD, actors=[SN(0, 0.4, scale=2.2)], props=RADAR(0.25), cams=[cam(0.0, [0.3, 1.0, 3.6], [0.28, 1.0, 3.4], [0.1, 1.1, -0.6], [0.1, 1.1, -0.6], lens=44, shake=0.01)])
st.shot('S03', ROAD, actors=[SN(0, 0, ry=20, clip='idle', scale=2.2)], cams=MACRO(0, 0, h=0.55, d=2.0))
st.shot('S04', ROAD, props=RADAR(None), cams=[cam(0.0, [-1.1, 1.9, 1.2], [-1.12, 1.9, 1.0], [-1.3, 1.9, -1.2], [-1.3, 1.9, -1.2], lens=42)])
st.shot('S05', ROAD, actors=[SN(0.8, 0.4, ry=90, scale=2.2, keys=[k(0.0, to=[0.85, 0, 0.4], dur=st.dur('S05'), clip='walk')]), act('flic', [-2.2, 0.35, 0.0], 90, 'point', 'angry')],
        props=[P('car', 'policeCar', pos=[-2.0, 0, 0.4], rot=[0, 1.5708, 0], keys=[k(0.0, to=[-1.95, 0, 0.4], dur=st.dur('S05'))])],
        cams=[cam(0.0, [-0.4, 0.8, 7.6], [-0.45, 0.82, 7.2], [-0.5, 0.6, 0.4], [-0.5, 0.6, 0.4], lens=44)])
st.shot('S06', 'office', props=[P('clock', 'wallClock', pos=[0, 1.6, -0.1], scale=1.6, opts={'rate': 6})], cams=[cam(0.0, [0.1, 1.6, 1.6], [0.1, 1.6, 1.4], [0, 1.6, -0.1], [0, 1.6, -0.1], lens=42)])
st.shot('S07', ROAD, actors=[act('flic', [0, 0, 0], 0, 'holdOut', 'smug')], props=[P('permis', 'idCard', on={'actor': 'flic', 'hand': 'R'}, scale=8.0)], cams=MS(0, 0, h=1.5, d=2.4))
st.shot('S08', 'replicaCourt', setOpts={'handle': 'TRIBUNAL'}, actors=[SN(0.35, -10.0, ry=0, clip='idle', scale=2.2)], props=[P('avocat', 'tortoise', pos=[-0.35, 0, -10.0], rot=[0, -1.2, 0], scale=1.4)],
        cams=[cam(0.0, [0.05, 0.7, -7.2], [0.05, 0.72, -7.45], [0, 0.35, -10.0], [0, 0.35, -10.0], lens=44)])
st.shot('S09', **JUDGE(9.0, 'TRIBUNAL', extra_props=[P('clock', 'wallClock', pos=[1.6, 2.6, -15.5], scale=1.6, opts={'rate': 8})]))
st.shot('S10', 'replicaCourt', setOpts={'handle': 'TRIBUNAL'}, actors=[act('juge', [-1.5, 0, -11.0], 90, 'carryBox', 'sad', keys=[k(0.0, to=[1.5, 0, -11.0], dur=st.dur('S10'), clip='carryBox')])],
        props=[P('box', 'cardboardBox', on={'actor': 'juge', 'hand': 'R'}, scale=0.8)], cams=[cam(0.0, [0.3, 1.4, -6.5], [0.3, 1.4, -6.8], [0, 1.2, -11.0], [0, 1.2, -11.0], lens=44)])
st.shot('S11', **JUDGE(0.5, 'VERDICT'))
st.shot('S12', ROAD, actors=[SN(-0.05, 0, ry=90, clip='idle', y=0.6, scale=1.4)], props=[P('moto', 'motorbike', pos=[0, 0, 0], rot=[0, 0, 0])], cams=LOW(0, 0, d=2.6, look_h=0.7, lens=48))
st.shot('S13', ROAD, actors=[SN(-6, 0, ry=90, clip='idle', y=0.6, scale=1.4, keys=[k(0.0, to=[6, 0.6, 0], dur=st.dur('S13'), ease='linear')])],
        props=[P('moto', 'motorbike', pos=[-6, 0, 0], opts={'roll': 40}, keys=[k(0.0, to=[6, 0, 0], dur=st.dur('S13'), ease='linear')])] + RADAR(0.45, '130'),
        cams=[cam(0.0, [0.3, 1.0, 4.4], [0.3, 1.0, 4.2], [-1.5, 0.8, 0], [1.5, 0.8, 0], lens=44, shake=0.03)], blur=[[0.0, st.dur('S13'), 0.012]], blurSamples=6)
st.shot('S14', ROAD, props=RADAR(None, '130'), cams=[cam(0.0, [-1.1, 1.9, 1.2], [-1.12, 1.9, 1.0], [-1.3, 1.9, -1.2], [-1.3, 1.9, -1.2], lens=42, shake=0.02)])
st.shot('S15', ROAD, actors=[act('flic', [0, 0, 0], 0, 'holdOut', 'smug')], props=[P('bag', 'evidenceBag', on={'actor': 'flic', 'hand': 'R'}, scale=2.2),
        P('saisie', 'noticeBoard', pos=[0.35, 1.8, 0.3], opts={'text': 'SAISIE', 'style': 'tag', 'w': 0.5, 'h': 0.22, 'popAt': 0.3})], cams=MS(0.15, 0, h=1.5, d=2.6))
st.shot('S16', ROAD, props=[P('nu', 'slug', pos=[0, 0, 0], scale=2.6)], cams=MACRO(0, 0, h=0.45, d=2.2))
st.shot('S17', ROAD, props=[P('nu', 'slug', pos=[0, 0, 0], scale=2.6)] + SLUGS(4, -0.5), cams=MACRO(0, -0.2, h=0.6, d=2.8))
st.shot('S18', ROAD, props=[P('sign', 'signBoard', pos=[0, 0, -1.4], opts={'text': 'AUTO-ÉCOLE', 'w': 1.4, 'h': 0.5, 'height': 0.6, 'bg': '#2F62B5', 'fg': '#FFFFFF'})] + SLUGS(4, 0) +
        [P(f'c{i}', 'trafficCone', pos=[-1.0 + i * 0.66, 0, 0.6], scale=0.6) for i in range(4)], cams=[cam(0.0, [0.3, 0.55, 2.8], [0.28, 0.58, 2.6], [0, 0.55, -0.6], [0, 0.6, -0.6], lens=44)])
st.shot('S19', ROAD, props=[P('score', 'noticeBoard', pos=[0, 1.2, 0], opts={'text': '100 %\nDE RÉUSSITE', 'style': 'sign', 'w': 1.0, 'h': 0.6, 'fg': '#2F7F4F', 'frame': '#2F7F4F', 'popAt': 0.15})] + SLUGS(4, 0.6),
        cams=[cam(0.0, [0.1, 0.9, 2.6], [0.1, 0.92, 2.4], [0, 0.95, 0], [0, 0.95, 0], lens=44)])
st.shot('S20', ROAD, props=SLUGS(5, 0) + [P('start', 'noticeBoard', pos=[0, 0.02, 0.35], rot=[-1.5708, 0, 0], opts={'text': 'DÉPART', 'style': 'sign', 'w': 2.4, 'h': 0.3}),
                                        P('flag', 'flag', pos=[0.4, 0, -30], scale=3, opts={'colors': ['#1C252A', '#F4F4F0', '#1C252A']})],
        cams=[cam(0.0, [0.6, 0.35, 2.2], [0.55, 0.36, 2.05], [0, 0.4, -10], [0, 0.4, -10], lens=46)])
st.card('S03', 'EXCÈS DE LENTEUR'); st.card('S07', 'RETRAIT DE PERMIS')
st.cue('clack', 'S02', 0.25, 0.6); st.cue('pop', 'S02', 0.25, 0.3); st.cue('thud', 'S03', 0.07, 0.45); st.cue('sfx:beep', 'S04', 0.15, 0.4)
st.cue('engine', 'S05', 0.0, 0.25, st.dur('S05')); st.cue('sfx:ticks', 'S06', 0.0, 0.5); st.cue('thud', 'S07', 0.07, 0.45); st.cue('sfx:ticks', 'S09', 0.0, 0.4)
[st.cue('sfx:step', 'S10', t, 0.4) for t in (0.2, 0.7, 1.2)]; st.cue('thud', 'S11', 0.5, 0.8); st.cue('engine', 'S12', 0.0, 0.35, st.dur('S12'))
st.cue('sfx:engine', 'S13', 0.0, 0.6); st.cue('whoosh', 'S13', 0.2, 0.6, 0.6, 500, 4000); st.cue('clack', 'S13', 0.45, 0.6); st.cue('sfx:beep', 'S14', 0.1, 0.5)
st.cue('pop', 'S15', 0.3, 0.5); st.cue('sfx:sniff', 'S16', 0.3, 0.4); st.cue('pop', 'S19', 0.15, 0.6); st.cue('sfx:whistle', 'S20', 0.2, 0.5)
st.write("L'escargot", {'escargot': {'type': 'creature', 'name': 'snail', 'opts': {'seed': 3}}})
