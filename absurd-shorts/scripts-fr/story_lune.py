#!/usr/bin/env python3
"""La Lune: he declares the Moon his second home; the tax office sends the property tax, an inspector and a fine for the Americans."""
from story_kit import *

st = Story('lune')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0),
         ('S08', 'L07', 0), ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0), ('S14', 'L13', 0),
         ('S15', 'L14', 0), ('S16', 'L15', 0), ('S17', 'L16', 0), ('S18', 'L17', 0), ('S19', 'L18', 0), ('S20', 'L19', 0), ('S21', 'L20', 0),
         ('S22', 'L21', 0), ('S23', 'L22', 0)])
HELMET = lambda a: P(f'dome_{a}', 'glassDome', on={'actor': a, 'joint': 'head', 'offset': [0, 0.05, 0]}, opts={'radius': 0.32, 'opacity': 0.22, 'base': False})
MOON = lambda: [P('ground', 'moonSurface', pos=[0, 0, 0], opts={'r': 40}), P('earth', 'earthGlobe', pos=[-14, 14, -60], opts={'radius': 4, 'spin': 0.1})]
US = {'colors': ['#B22234', '#F4F4F0', '#3C3B6E']}
def doc(text, pop=0.15, stamp=None, w=0.8, h=1.0, size=0.42):
    return P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': text, 'style': 'doc', 'w': w, 'h': h, 'popAt': pop, 'textSize': size, **({'stamp': stamp} if stamp else {})})
DOCCAM = [cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.95], [0, 1.5, 0], [0, 1.5, 0], lens=42)]

st.shot('S01', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'clipboard', 'smug')], cams=MS(0, 0, h=1.45, d=2.6))
st.shot('S02', 'spaceDark', props=[P('moon', 'moon', pos=[0, 0, 0], opts={'radius': 3}), P('house', 'cottage', pos=[0, 5.85, 0], scale=0.25, opts={'w': 6, 'd': 6, 'h': 2.6, 'rh': 1.6, 'color': '#F2D06B', 'roof': '#C9473A'}),
                                   P('sign', 'noticeBoard', pos=[1.2, 6.6, 0.8], opts={'text': 'RÉSIDENCE\nSECONDAIRE', 'style': 'sign', 'w': 1.2, 'h': 0.5, 'popAt': 0.3})],
        cams=[cam(0.0, [0.5, 4.8, 13.5], [0.4, 4.9, 12.0], [0, 5.0, 0], [0, 5.2, 0], lens=40)])
st.shot('S03', 'office', props=[doc('DÉCLARATION\nRÉSIDENCE SECONDAIRE :\nLA LUNE', pop=None), P('ok', 'noticeBoard', pos=[0.05, 1.3, 0.03], opts={'text': 'ACCEPTÉ', 'style': 'sign', 'w': 0.5, 'h': 0.16, 'fg': '#2F7F4F', 'frame': '#2F7F4F', 'popAt': 0.35, 'tilt': 0.15})], cams=DOCCAM)
st.shot('S04', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'holdOut', 'shocked')], props=[P('tax', 'noticeBoard', pos=[0.05, 1.4, 0.45], opts={'text': 'TAXE FONCIÈRE\nLA LUNE', 'style': 'doc', 'w': 0.55, 'h': 0.7, 'popAt': 0.1, 'textSize': 0.4})],
        cams=MS(0, 0, h=1.5, d=2.4))
st.shot('S05', 'office', props=[P('sum', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': '38 000 000 000 €', 'style': 'sign', 'w': 0.62, 'h': 0.24, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': 0.1})],
        cams=[cam(0.0, [0.0, 1.5, 1.95], [0.0, 1.5, 1.72], [0, 1.5, 0], [0, 1.5, 0], lens=42, shake=0.02)])
st.shot('S06', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'angryFist', 'angry')], cams=MS(0, 0, h=1.45, d=2.6, shake=0.015))
st.shot('S07', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'point', 'angry', keys=st.talk('L06', 'S07', 'angry'))], cams=CU(0, 0))
st.shot('S08', 'office', actors=[act('inspecteur', [0.3, 0, 1.5], 180, 'walk', 'suspicious', keys=[k(0.0, to=[0.3, 0, -0.3], dur=st.dur('S08'), clip='walk')])],
        props=[P('case', 'briefcase', on={'actor': 'inspecteur', 'hand': 'R'})], cams=[cam(0.0, [0.0, 1.4, -2.6], [0.0, 1.4, -2.9], [0.3, 1.3, 1.5], [0.3, 1.3, -0.3], lens=44)])
st.shot('S09', 'runway', props=[P('rocket', 'rocket', pos=[0, 0, -10], scale=3.0, opts={'flame': True}, keys=[k(0.15, to=[0, 30, -10], dur=round(st.dur('S09') - 0.15, 3), ease='in')]),
                                P('dust', 'dustPuff', pos=[0, 0, -10], scale=4)],
        cams=[cam(0.0, [3, 0.6, 6], [3, 0.7, 5.6], [0, 3, -10], [0, 9, -10], lens=46, shake=0.04)])
st.shot('S10', 'spaceDark', actors=[act('inspecteur', [0.8, 0, 0.6], -40, 'lookItem', 'suspicious')], props=MOON() + [HELMET('inspecteur'), P('flag', 'starsStripes', pos=[-0.4, 0, -0.4], scale=1.4)],
        cams=WS(0.1, 0, h=1.1, d=4.6, look_h=1.0))
st.shot('S11', 'spaceDark', actors=[act('inspecteur', [0, 0, 0], 0, 'point', 'angry', keys=st.talk('L10', 'S11', 'angry'))], props=MOON() + [HELMET('inspecteur')], cams=CU(0, 0, d=1.9))
st.shot('S12', 'spaceDark', actors=[act('inspecteur', [0.35, 0, 0.4], -60, 'holdOut', 'smug')],
        props=MOON() + [HELMET('inspecteur'), P('flag', 'starsStripes', pos=[-0.4, 0, -0.2], scale=1.4), P('fine', 'noticeBoard', pos=[-0.12, 1.0, 0.6], opts={'text': 'AMENDE', 'style': 'tag', 'w': 0.4, 'h': 0.22, 'popAt': 0.4})],
        cams=WS(0.0, 0, h=1.35, d=4.3, look_h=1.2))
st.shot('S13', 'spaceDark', actors=[act('inspecteur', [0.4, 0, 0], -20, 'stand', 'suspicious')],
        props=MOON() + [HELMET('inspecteur')] + [P(f'm{i}', 'moneySack', pos=[-0.6 + i * 0.35, 3.0, 0.4], opts={'color': '#5BB06E'}, keys=[k(0.1 + i * 0.12, to=[-0.6 + i * 0.35, 0, 0.4], dur=0.35, ease='in')]) for i in range(3)],
        cams=WS(0.0, 0, h=1.2, d=3.6, look_h=0.9))
st.shot('S14', 'spaceDark', actors=[act('inspecteur', [-0.05, 0, 0], 0, 'shakeHead', 'unimpressed')],
        props=MOON() + [HELMET('inspecteur'), P('eur', 'noticeBoard', pos=[0.5, 1.5, 0.25], opts={'text': '€\nUNIQUEMENT', 'style': 'sign', 'w': 0.42, 'h': 0.32, 'popAt': 0.4})], cams=MS(0.2, 0, h=1.6, d=2.8))
for sid, txt, col in [('S15', 'BANQUE', '#203447'), ('S16', 'BOULANGERIE', '#B5302A'), ('S17', 'POSTE', '#E0B020')]:
    shops = [P('b1', 'shopFront', pos=[-2.2, 0, -2], opts={'text': 'BANQUE', 'signBg': '#203447', 'w': 2.0}), P('b2', 'shopFront', pos=[0, 0, -3.2], opts={'text': 'BOULANGERIE', 'signBg': '#B5302A', 'w': 2.4}), P('b3', 'shopFront', pos=[2.2, 0, -2], opts={'text': 'POSTE', 'signBg': '#E0B020', 'w': 2.0})]
    i = ['S15', 'S16', 'S17'].index(sid); shops[i]['opts']['popAt'] = 0.15
    st.shot(sid, 'spaceDark', props=MOON() + shops[:i + 1], cams=[cam(0.0, [0.4, 1.7, 13.0], [0.35, 1.75, 12.2], [0, 1.4, -2.4], [0, 1.45, -2.4], lens=46)])
st.shot('S18', 'spaceDark', actors=[act(f'q{i}', [3 + 0.25 * (i % 2), 0, -0.6 + i * 1.1], 180, 'idle', 'unimpressed') for i in range(6)],
        props=MOON() + [P('b3', 'shopFront', pos=[3, 0, -2], opts={'text': 'POSTE', 'signBg': '#E0B020'})] + [HELMET(f'q{i}') for i in range(6)],
        cams=[cam(0.0, [5.5, 0.9, 9.5], [5.2, 1.0, 9.0], [3.0, 1.2, 0.5], [3.0, 1.2, 0.5], lens=46)])
st.shot('S19', 'spaceDark', actors=[act('mec', [-0.1, 0, 0], 0, 'present', 'happy')],
        props=MOON() + [HELMET('mec'), P('sale', 'noticeBoard', pos=[0.5, 1.25, 0.25], opts={'text': 'À\nVENDRE', 'style': 'sign', 'w': 0.44, 'h': 0.4, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': 0.2})], cams=MS(0.15, 0, h=1.45, d=3.0))
st.shot('S20', 'spaceDark', props=MOON() + [P('tw', 'tumbleweed', pos=[-4, 0.4, 0], scale=1.2, keys=[k(0.0, to=[4, 0.4, 0], dur=st.dur('S20'), ease='linear')])],
        cams=[cam(0.0, [0, 1.0, 6], [0, 1.0, 5.6], [0, 0.8, 0], [0, 0.8, 0], lens=44)])
st.shot('S21', 'spaceDark', actors=[act('acheteuse', [0, 0, 0], 0, 'handsOnHips', 'unimpressed', keys=st.talk('L20', 'S21', 'unimpressed'))], props=MOON() + [HELMET('acheteuse')], cams=CU(0, 0, d=1.9))
st.shot('S22', 'spaceDark', actors=[act('mec', [1.1, 0, 0.6], -30, 'handsOnHips', 'smug')], props=MOON() + [HELMET('mec'), P('gate', 'barrierGate', pos=[-0.4, 0, 0], opts={'length': 3.5, 'angle': 0, 'sign': 'PÉAGE'})],
        cams=WS(0.35, 0, h=1.2, d=6.0, look_h=1.0))
st.shot('S23', 'seaSurface', setOpts={'parasols': False}, props=[P('gate', 'barrierGate', pos=[-1.5, 0, 6.4], opts={'length': 4.0, 'angle': 0, 'open': [[0.9, 80]], 'sign': 'PÉAGE'}),
                                                                 P('moon', 'moon', pos=[-6, 18, -50], opts={'radius': 5})],
        cams=[cam(0.0, [0.2, 1.0, 13.5], [0.1, 1.05, 13.0], [-0.6, 3.0, 5.0], [-0.6, 3.4, 5.0], lens=46)])
st.card('S04', 'TAXE FONCIÈRE'); st.card('S11', 'OCCUPATION ILLÉGALE')
st.cue('pop', 'S02', 0.3, 0.5); st.cue('clack', 'S03', 0.35, 0.7); st.cue('thud', 'S04', 0.07, 0.45); st.cue('sfx:paper', 'S04', 0.1, 0.5)
st.cue('pop', 'S05', 0.1, 0.6); st.cue('sfx:gasp', 'S05', 0.3, 0.6); [st.cue('sfx:step', 'S08', t, 0.4) for t in (0.2, 0.7, 1.2)]
st.cue('sfx:jet', 'S09', 0.1, 0.7); st.cue('thunder', 'S09', 0.1, 0.4); st.cue('thud', 'S11', 0.07, 0.45); st.cue('pop', 'S12', 0.4, 0.6)
[st.cue('thud', 'S13', 0.45 + 0.12 * i, 0.5) for i in range(3)]; st.cue('pop', 'S14', 0.4, 0.5)
st.cue('pop', 'S15', 0.15, 0.6); st.cue('pop', 'S16', 0.15, 0.6); st.cue('pop', 'S17', 0.15, 0.6); st.cue('pop', 'S19', 0.2, 0.5)
st.cue('gust', 'S20', 0.0, 0.4, st.dur('S20')); st.cue('clack', 'S22', 0.3, 0.4); st.cue('gust', 'S23', 0.0, 0.4, st.dur('S23')); st.cue('clack', 'S23', 0.9, 0.6); st.cue('sfx:cash', 'S23', 1.0, 0.5)
st.write('La Lune', {'inspecteur': {'preset': 'boss'}, 'acheteuse': {'preset': 'madame'}, **{f'q{i}': {'preset': ['madame', 'worker', 'tourist', 'mamie', 'boss', 'gamin'][i]} for i in range(6)}})
