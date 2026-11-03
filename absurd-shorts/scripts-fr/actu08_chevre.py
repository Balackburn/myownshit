#!/usr/bin/env python3
"""ACTU 08 — LA CHÈVRE. His goat joins the high-school blockade and eats the signs, even the 6-7 one -> he calls the
cops (motif: dégradation de biens publics en réunion) -> in custody the goat eats the official report ("Mèèè." ->
destruction de preuves) -> Matignon receives the goat with TikTokers ("Et pour Parcoursup ?" "Lien en bio.") ->
the goat eats the budget -> the goat is admitted on Parcoursup; he is still on the waiting list."""
from actu_common import *

scenes = []
SIGN_POS = [(-0.6, '6-7'), (0.5, 'ON VEUT\nDES PROFS'), (1.6, 'GRÈVE')]
scenes.append({
  'id': 'blocus', 'set': 'street', 'ambience': 'street',
  'lines': [L('K1', "La chèvre de ce mec a rejoint le blocus du lycée.", highlight=['chèvre', 'blocus']),
            L('K2', "Elle mangeait les pancartes. Même celle du 6-7.", highlight=['pancartes.', '6-7.']),
            L('K3', "Il a appelé les flics. Motif : dégradation de biens publics en réunion.", highlight=['Motif', 'réunion.'])],
  'actors': [
    act('chevre', [-3.5, 0, 0.6], 90, 'idle', 'happy', scale=1.15, keys=[
        k(0.1, to=[1.9, 0, 0.1], clip='walk', speed=1.6, then='eat', faceEnd=-150),
        k('K2:Même', to=[-0.35, 0, 0.15], clip='walk', speed=2.0, faceEnd=-150, then='eat', expr='smug'),
        k('K3', clip='celebrate', expr='happy', face=20, turn=0.2)]),
    act('lyc1', [0.0, 0, -0.9], 10, 'chant', 'happy', keys=[k('K2', clip='stand', expr='shocked')]),
    act('lyc4', [1.1, 0, -1.0], -10, 'chant', 'happy', keys=[k('K2:Même', clip='stand', expr='angry')]),
    act('mec', [-2.6, 0, 1.3], 60, 'idle', 'neutral', keys=[k('K2', clip='facepalm', expr='unimpressed'), k('K3', clip='phoneCall', expr='angry', face=-10, turn=0.2)]),
  ],
  'props': [*[P(f'pan{i}', 'protestSign', scale=0.75, pos=[x, 0, -0.35], opts={'text': t},
                keys=[k('K2:Même+0.3' if t == '6-7' else f'K2:pancartes{0.25 + 0.5 * i - 0.5:+.2f}' if i else 'K2:mangeait', scale=0.01, dur=0.7)]) for i, (x, t) in enumerate(SIGN_POS)],
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('K3', visible=True)]),
            P('lycee', 'signBoard', pos=[0.5, 0, -2.6], opts={'text': 'LYCÉE', 'bg': P_NAVY, 'fg': '#F6F1E3', 'w': 1.6, 'h': 0.5, 'height': 2.0}),
            *[P(f'bin{i}', 'trashCan', pos=[-0.8 + i * 0.8, 0, -1.6]) for i in range(4)]],
  'sfx': [{'at': 'K2:mangeait', 'name': 'scratch', 'vol': 0.4}, {'at': 'K2:Même+0.3', 'name': 'scratch', 'vol': 0.5}],
  'cams': [cam(0, 'chevre', 'fs', angle=-70, move='track'),
           cam('K1:blocus', ['chevre', 'lyc1', 'lyc4'], 'fs', worldAngle=10, elev=6),
           cam('K2', 'chevre', 'ms', worldAngle=20),
           cam('K2:Même+0.15', ['chevre', 'pan0'], 'ms', worldAngle=10, withProps=True),
           cam('K3', 'mec', 'cu', angle=-35),
           cam('K3:biens', 'chevre', 'cu', angle=0)],
  'tail': 0.2,
})

scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('K4', "Garde à vue pour la chèvre. Elle a mangé le procès-verbal.", highlight=['procès-verbal.']),
            L('K5', "Vous avez quelque chose à déclarer ?", 'commissaire'),
            L('K6', "Mèèè.", 'chevre', pre=0.2),
            L('K7', "Destruction de preuves. Ça s'aggrave.", 'commissaire', highlight=['Destruction', 'preuves.'])],
  'actors': [
    act('chevre', [0, 0, -1.35], 0, 'idle', 'smug', scale=1.15, keys=[k('K4:mangé', clip='eat', expr='happy'), k('K6', clip='talk', expr='neutral'), k('K7', clip='idle', expr='smug')]),
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[k('K5', clip='leanTable', expr='angry'), k('K7', clip='slamTable', expr='angry', sfx='thud', sfxAt=0.12)]),
  ],
  'props': [P('pv', 'documents', pos=[-0.1, 0.785, -0.85], keys=[k('K4:mangé', scale=0.01, dur=0.8)])],
  'sfx': [{'at': 'K4:mangé', 'name': 'paper', 'vol': 0.6}],
  'cams': [cam(0, ['commissaire', 'chevre'], 'fs', worldAngle=10, elev=10),
           cam('K4:mangé', 'chevre', 'ms', angle=0),
           cam('K5', 'commissaire', 'mcu', angle=60),
           cam('K6', 'chevre', 'cu', angle=0),
           cam('K7', 'commissaire', 'mcu', angle=50)],
  'tail': 0.2,
})

scenes.append({
  'id': 'matignon', 'set': 'pressRoom', 'setOpts': {'backdrop': 'MATIGNON|RÉPUBLIQUE|FRANÇAISE', 'bg': '#D9E2E8', 'fg': '#2E4563', 'podium': False}, 'ambience': 'station',
  'lines': [L('K8', "Matignon a reçu la chèvre avec des TikTokeurs.", highlight=['Matignon', 'TikTokeurs.']),
            L('K9', "Et pour Parcoursup ?", 'mec'),
            L('K10', "Lien en bio.", 'tiktok1', highlight=['Lien', 'bio.']),
            L('K11', "La chèvre a mangé le budget.", highlight=['budget.'])],
  'actors': [
    act('pm', [0, 0, -2.15], 0, 'podiumTalk', 'neutral', keys=[k('K11:budget', clip='startle', expr='shocked')]),
    act('tiktok1', [-1.35, 0, -1.05], 60, 'showPhone', 'happy', keys=[k('K10', clip='readPhone', expr='smug')]),
    act('tiktok2', [1.35, 0, -1.05], -60, 'showPhone', 'happy'),
    act('chevre', [-0.55, 0, -0.85], 30, 'idle', 'happy', scale=1.15, keys=[k('K11', to=[-0.2, 0, -1.0], clip='walk', speed=1.5, faceEnd=-10, then='eat', expr='smug')]),
    act('mec', [0.65, 0, -0.55], -30, 'stand', 'neutral', keys=[k('K9', clip='present', expr='suspicious', face='tiktok1', turn=0.2), k('K10', clip='facepalm', expr='unimpressed')]),
  ],
  'props': [P('table', 'table', pos=[0, 0, -1.55], opts={'w': 2.0, 'd': 0.8, 'color': '#7A5C3A'}),
            P('budget', 'notebook', scale=1.8, pos=[-0.2, 0.775, -1.45], rot=[-1.5708, 0, 0], opts={'text': 'BUDGET\n2027', 'bg': '#2C4A8A'}, keys=[k('K11:budget', scale=0.01, dur=0.7)]),
            P('tel1', 'phone911', opts={'screen': 'tiktok'}, on={'actor': 'tiktok1', 'hand': 'R', **HAND_FLAT}),
            P('tel2', 'phone911', opts={'screen': 'tiktok'}, on={'actor': 'tiktok2', 'hand': 'R', **HAND_FLAT})],
  'sfx': [{'at': 'K11:budget', 'name': 'paper', 'vol': 0.6}],
  'cams': [cam(0, ['pm', 'tiktok1', 'tiktok2', 'chevre'], 'fs', worldAngle=0, elev=8),
           cam('K9', 'mec', 'mcu', angle=10),
           cam('K10', 'tiktok1', 'mcu', angle=-10),
           cam('K11', ['chevre', 'pm'], 'ms', worldAngle=0),
           cam('K11:budget', 'pm', 'cu', angle=0)],
  'tail': 0.2,
})

scenes.append({
  'id': 'parcoursup', 'set': 'street', 'ambience': 'street',
  'lines': [L('K12', "Elle a été acceptée sur Parcoursup. Ce mec est toujours en liste d'attente.", highlight=['acceptée', "d'attente."])],
  'actors': [
    act('chevre', [-0.6, 0, 0.5], 20, 'celebrate', 'happy', scale=1.15),
    act('mec', [0.7, 0, 0.6], -20, 'readPhone', 'sad', keys=[k('K12:Ce', clip='stareCamera', expr='unimpressed')]),
  ],
  'props': [P('admis', 'notebook', scale=2.2, opts={'text': 'PARCOURSUP\n—\nADMISE\nSCIENCES\nPO', 'bg': '#3F8A84'}, on={'actor': 'chevre', 'joint': 'head', 'offset': [0, 0.05, 0.28]}),
            tweet_on_table('attente', 2.6, 0.0, 1.8, name='Parcoursup', handle='@parcoursup', initial='P', avatar='#2C4A8A', via='Notification', text="Statut : liste d'attente. Rang : 67 000.", likes=''),
            P('lycee', 'signBoard', pos=[0.5, 0, -2.6], opts={'text': 'LYCÉE', 'bg': P_NAVY, 'fg': '#F6F1E3', 'w': 1.6, 'h': 0.5, 'height': 2.0})],
  'sfx': [{'at': 'K12', 'name': 'tada', 'vol': 0.35}],
  'cams': [cam(0, ['chevre', 'mec'], 'ms', worldAngle=0),
           cam('K12:acceptée', 'chevre', 'cu', angle=0),
           tweet_cam('K12:liste', 2.6, 0.0, 1.8),
           cam('K12.end+0.1', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu08_chevre', 'La chèvre', scenes, {
  'chevre': {'type': 'creature', 'name': 'goat', 'opts': {'seed': 5}},
  'lyc1': {'preset': 'lyceen', 'suit': '#2F62B5', 'seed': 11}, 'lyc4': {'preset': 'lyceenne', 'seed': 14},
  'pm': {'preset': 'lemec_charcoal', 'hair': 'slick', 'glasses': True, 'facial': 'none', 'tie': '#2C4A8A', 'seed': 71},
  'tiktok1': {'preset': 'lyceen', 'suit': '#C9729A', 'hair': 'mohawk', 'build': {'height': 1.0}, 'seed': 72},
  'tiktok2': {'preset': 'lyceenne', 'suit': '#E6B84A', 'build': {'height': 0.98}, 'seed': 73},
})
