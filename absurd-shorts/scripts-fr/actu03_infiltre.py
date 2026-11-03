#!/usr/bin/env python3
"""ACTU 03 — L'INFILTRÉ. A cop of thirty years is sent undercover into a high-school blockade with outdated slang ->
"Monsieur, personne parle comme ça." -> his slang guide is the 2019 edition -> the students challenge him to an aura
battle, he loses and arrests himself (motif: aura insuffisante) -> interrogation ("Où étiez-vous le 17 octobre ?") ->
the headteacher wins everyone back with a perfect scuba -> he goes back to class too: he sits the bac in June."""
from actu_common import *

scenes = []
SIGNS = [('s1', 'lyc1', '6-7'), ('s2', 'lyc2', 'ON VEUT\nDES PROFS'), ('s3', 'lyc4', "LECORNU\nT'ES FOUTU")]
LYC = [('lyc1', [0.95, 0, 0.55], -90, 'holdSign'), ('lyc2', [1.7, 0, 0.0], -110, 'holdSign'), ('lyc3', [2.1, 0, 0.95], -75, 'chant'), ('lyc4', [1.45, 0, 1.45], -70, 'holdSign')]
scenes.append({
  'id': 'blocus', 'set': 'street', 'ambience': 'street',
  'lines': [L('I1', "Ce mec était flic depuis trente ans. On l'a infiltré dans un blocus de lycée.", highlight=['infiltré', 'blocus']),
            L('I2', "Wesh la mif, c'est trop swag, YOLO, le 6-7 est dans la rue.", 'mec', highlight=['YOLO,', '6-7']),
            L('I3', "Monsieur, personne parle comme ça.", 'lyc1', highlight=['personne']),
            L('I4', "Il a vérifié son lexique.", highlight=['lexique.']),
            L('I5', "Les lycéens l'ont défié en bataille d'aura.", highlight=['bataille', "d'aura."]),
            L('I6', "Il a perdu. Alors il s'est arrêté lui-même. Motif : aura insuffisante.", highlight=['lui-même.', 'insuffisante.'])],
  'actors': [
    act('mec', [-5.0, 0, 0.75], 90, 'idle', 'smug', keys=[
        k(0.05, to=[-0.15, 0, 0.6], clip='strut', speed=1.6, faceEnd=90, then='idle'),
        k('I2', clip='sixSeven', expr='happy'),
        k('I3', clip='stand', expr='neutral'),
        k('I4', clip='showPhone', expr='suspicious', face=0, turn=0.2),
        k('I5:bataille', clip='flex', expr='angry'),
        k('I5:aura', clip='auraPose2', expr='smug'),
        k('I6', clip='cry', expr='sad'),
        k('I6:arrêté', clip='handcuffed', expr='sad', sfx='cuff', sfxAt=0.2)]),
    *[act(i, p, r, c, 'neutral', keys=[k('I2', expr='unimpressed'), k('I5', clip='auraPose', expr='smug')] + ([k('I5:aura', clip='scuba', expr='smug')] if i == 'lyc1' else [])) for i, p, r, c in LYC],
  ],
  'props': [*[P(sid, 'protestSign', opts={'text': t}, on={'actor': a, 'hand': 'R', **SIGN_UP}, keys=[k('I5', visible=False)]) for sid, a, t in SIGNS],
            P('lexique', 'notebook', scale=1.6, visible=False, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('I4', visible=True), k('I5', visible=False)]),
            P('cuffs', 'handcuffs', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('I6:arrêté', visible=True)]),
            P('lycee', 'signBoard', pos=[1.2, 0, -2.6], opts={'text': 'LYCÉE', 'bg': P_NAVY, 'fg': '#F6F1E3', 'w': 1.6, 'h': 0.5, 'height': 2.0}),
            *[P(f'bin{i}', 'trashCan', pos=[0.4 + i * 0.75, 0, -1.25]) for i in range(4)],
            WM(pos=[-4.2, 0, -1.3], opts={'kind': 'stand'})],
  'cams': [cam(0, 'mec', 'fs', angle=60, move='track'),
           cam('I1:infiltré', ['mec', 'lyc1', 'lyc2', 'lyc4'], 'fs', worldAngle=0, elev=6),
           cam('I2', 'mec', 'ms', angle=20),
           cam('I2:YOLO', 'mec', 'cu', angle=15),
           cam('I3', 'lyc1', 'mcu', angle=-15),
           cam('I4', 'mec', 'ms', angle=30),
           cam('I4:lexique', 'lexique', 'cu', worldAngle=0, noOcclusion=True, zoom=1.8),
           cam('I5', ['mec', 'lyc1'], 'ms', worldAngle=0),
           cam('I5:aura', 'lyc1', 'ms', angle=-10),
           cam('I6', 'mec', 'ms', angle=15),
           cam('I6:Motif', 'mec', 'ecu', angle=0)],
  'tail': 0.2,
})

scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('I7', "Où étiez-vous le 17 octobre ?", 'commissaire'),
            L('I8', "En bataille d'aura.", 'mec'),
            L('I9', "Vous avez perdu ?", 'commissaire'),
            L('I10', "Oui.", 'mec', pre=0.35),
            L('I11', "Quarante-huit heures.", 'commissaire', highlight=['Quarante-huit'])],
  'actors': [
    act('mec', IR_SUSPECT, 0, 'sitCuffed', 'sad'),
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[k('I11', clip='slamTable', expr='angry', sfx='thud', sfxAt=0.12)]),
  ],
  'props': [P('lexique', 'notebook', scale=1.6, pos=[-0.4, 0.795, -0.6], rot=[-1.5708, 0, 0.3])],
  'cams': [cam(0, ['commissaire', 'mec'], 'fs', worldAngle=10, elev=10),
           cam('I8', 'mec', 'cu', angle=0),
           cam('I9', 'commissaire', 'mcu', angle=60),
           cam('I10', 'mec', 'ecu', angle=0),
           cam('I11', 'commissaire', 'mcu', angle=60)],
  'tail': 0.2,
})

scenes.append({
  'id': 'scuba', 'set': 'street', 'ambience': 'street',
  'lines': [L('I12', "Le proviseur est venu le chercher. Un scuba parfait. Tout le monde en cours.", highlight=['scuba', 'parfait.'])],
  'actors': [
    act('proviseur', [-1.0, 0, 0.9], 90, 'idle', 'unimpressed', keys=[k('I12:scuba', clip='scuba', expr='smug'), k('I12:Tout', clip='point', expr='angry', face=180, turn=0.2)]),
    act('mec', [0.6, 0, 0.6], -90, 'stand', 'sad', keys=[k('I12:Tout+0.2', path=[[0.8, 0, -0.6], [1.2, 0, -2.3]], clip='walk', speed=1.6)]),
    *[act(i, p, r, 'stand', 'neutral', keys=[k('I12:scuba', expr='shocked'), k(f'I12:Tout+{0.1 * n:.1f}', path=[[p[0], 0, -0.7], [1.2 + 0.3 * n, 0, -2.4]], clip='walk', speed=1.7, expr='sad')]) for n, (i, p, r, c) in enumerate(LYC)],
  ],
  'props': [P('lycee', 'signBoard', pos=[1.2, 0, -2.6], opts={'text': 'LYCÉE', 'bg': P_NAVY, 'fg': '#F6F1E3', 'w': 1.6, 'h': 0.5, 'height': 2.0})],
  'cams': [cam(0, 'proviseur', 'ms', angle=30),
           cam('I12:scuba', 'proviseur', 'ms', angle=10),
           cam('I12:Tout', ['proviseur', 'mec', 'lyc1', 'lyc2'], 'fs', worldAngle=15, elev=8)],
  'tail': 0.3,
})

scenes.append({
  'id': 'classe', 'set': 'classroom', 'ambience': None,
  'lines': [L('I13', "Lui aussi. Il passe le bac en juin.", highlight=['bac'])],
  'actors': [
    act('mec', [0, 0.12, -0.45], 180, 'sitHoldUp', 'happy', keys=[k('I13:bac', clip='sit', expr='sad')]),
    act('lyc1', [-1.6, 0.12, -0.45], 180, 'sit', 'unimpressed'), act('lyc2', [1.6, 0.12, -0.45], 180, 'sit', 'neutral'),
    act('lyc4', [0, 0.12, 0.9], 180, 'sit', 'sleepy'),
  ],
  'props': [P('cuffs', 'handcuffs', on={'actor': 'mec', 'hand': 'L'})],
  'cams': [POV(0, [0.25, 1.85, -2.75], [0, 0.95, 0.2], 64),
           cam('I13:bac', 'mec', 'cu', worldAngle=180, allowBack=True, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu03_infiltre', "L'infiltré", scenes, {
  'mec': {'preset': 'infiltre'},
  'lyc1': {'preset': 'lyceen', 'suit': '#2F62B5', 'seed': 11}, 'lyc2': {'preset': 'lyceen', 'suit': '#C23A2E', 'skin': '#9A6A45', 'hair': 'curly', 'seed': 12},
  'lyc3': {'preset': 'lyceen', 'suit': '#3F8A84', 'hair': 'buzz', 'skin': '#C8955F', 'seed': 13}, 'lyc4': {'preset': 'lyceenne', 'seed': 14},
  'proviseur': {'preset': 'proviseur'},
})
