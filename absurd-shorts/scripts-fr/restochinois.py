#!/usr/bin/env python3
"""LE RESTO CHINOIS. He eats with a fork and a knife in a Chinese restaurant -> the waiter loses it, sniffs cocaine in the
kitchen: four seconds of calm, then paranoia and a flashback (sepia) -> Mao-era China: Western products forbidden, he
buys Western music on the black market ("Fruit de la passion", he cries), then the dealer's treasure: cutlery -> three
absurd uses (spoon = phone to America, knife = tie, fork = antenna) -> arrested (motif: haute trahison et intelligence
avec l'ennemi) -> five years in a 40 cm cell (a photo of rice a year, one chopstick for a bed, a drawn window) -> France,
works like mad, opens his restaurant -> a second line: the greatness of China, love for the Party -> he denounces the man
online -> world scandal -> patriotic netizens with forks ("ça ferait moins mal avec des baguettes"), they "plant" his
animals -> led by Kylian Mbappé -> the man apologises, Mbappé humiliates him (twelve languages) -> he falls in love with
China, flies there, becomes a party official reading propaganda -> he calls the police on the waiter (motif: trafic de
stupéfiants) -> the waiter was right to be paranoid.

Adjustments to the brief (see the delivery note): every character speaks with the same voice and no put-on accent (the
skill's rule: no ethnicity as the butt of the joke; the satire aims at the regime and its propaganda); the song is not
downloaded, an original procedural zouk-style stand-in plays and the user can drop their own licensed file at
MUSIC_FILE; the violence stays cartoonish (a fork in the backside, animals "planted" in garden planters, unharmed);
Mbappé leads with a megaphone and does nothing violent."""
from actu_common import *

SEPIA = 'contrast(0.9) saturate(0.45) sepia(0.62) brightness(1.04)'
MUSIC_FILE = 'assets/music/user/fruit_de_la_passion.mp3'   # optional, not in the repo: a track the user holds the rights to
FORK_UP = {'offset': [0, 0.2, 0.02], 'rot': [3.1416, 0, 0]}   # a giant fork held up or forward (raised arm: hand +y points down)
LINE = [0.3, 0.925, -0.92]                                    # powder line on the prep island, in front of the waiter
WAITER_ISLAND = [0.3, 0, -1.42]
scenes = []

# ------------------------------------------------------------------ 1. the restaurant
scenes.append({
  'id': 'resto', 'set': 'chineseRestaurant', 'ambience': 'bar', 'ambienceVol': 0.6,
  'lines': [L('R1', "Ce mec a mangé dans un restaurant chinois. Avec une fourchette et un couteau.", highlight=['chinois.', 'fourchette']),
            L('R2', "Il ne savait pas se servir des baguettes.", highlight=['baguettes.']),
            L('R3', "Des couverts ? Dans mon restaurant ?", 'serveur'),
            L('R4', "Le serveur a pété un câble.", highlight=['câble.'])],
  'actors': [
    act('mec', [0, 0.12, -1.93], 0, 'sitEatSpoon', 'happy', keys=[
        k('R3', clip='sit', expr='shocked', look='serveur'),
        k('R4:câble', clip='sitEatSpoon', expr='unimpressed', look=None)]),
    act('serveur', [2.3, 0, -2.9], 180, 'idle', 'happy', keys=[
        k(0.4, to=[1.05, 0, -0.8], clip='walk', speed=1.7, faceEnd='mec', then='stand'),
        k('R2:baguettes', clip='doubleTake', expr='shocked'),
        k('R3', clip='point', expr='angry'),
        k('R4', clip='tantrum', expr='angry')]),
  ],
  'props': [P('fourchette', 'fork', on={'actor': 'mec', 'hand': 'R'}),
            P('couteau', 'knife', on={'actor': 'mec', 'hand': 'L'}),
            P('plat', 'noodlePlate', pos=[0, 0.786, -0.98]),
            P('bol', 'riceBowl', pos=[0.28, 0.786, -1.05]),
            P('baguettes', 'chopsticks', scale=1.2, pos=[-0.27, 0.794, -0.86], rot=[-1.5708, 0, 0.25])],
  'sfx': [{'at': 'R4', 'name': 'thud', 'vol': 0.5}, {'at': 'R4:pété', 'name': 'glass', 'vol': 0.35}],
  'cams': [cam(0, ['mec', [-1.4, 2.75, -3.5]], 'fs', worldAngle=12, elev=10),
           cam('R1:Avec', [[0, 0.86, -1.0]], 'cu', worldAngle=0, elev=35, noOcclusion=True),
           cam('R2', 'mec', 'cu', angle=0),
           cam('R2:baguettes', [[-0.27, 0.82, -0.9]], 'cu', worldAngle=-20, elev=25, noOcclusion=True, zoom=1.6),
           cam('R3', 'serveur', 'ms', angle=15),
           cam('R4', ['serveur', 'mec'], 'fs', worldAngle=-20, elev=6),
           cam('R4:câble', 'mec', 'cu', angle=0)],
  'tail': 0.15,
})

# ------------------------------------------------------------------ 2. the kitchen: four seconds of calm, then paranoia
scenes.append({
  'id': 'cuisine', 'set': 'proKitchen', 'ambience': 'lab', 'ambienceVol': 0.6,
  'lines': [L('R5', "Pour se calmer, il est allé sniffer de la cocaïne en cuisine.", highlight=['cocaïne']),
            L('R6', "Ça a marché pendant quatre secondes.", highlight=['quatre', 'secondes.']),
            L('R7', "Puis il est devenu complètement paranoïaque.", highlight=['paranoïaque.']),
            L('R8', "Et il a eu un flashback.", highlight=['flashback.'])],
  'actors': [act('serveur', WAITER_ISLAND, 0, 'stand', 'angry', keys=[
      k('R5:sniffer-0.15', clip='leanTable', expr='angry'),
      k('R6', clip='stand', expr='happy'),
      k('R7', clip='lookAround', expr='scared'),
      k('R7:paranoïaque', clip='wired', expr='scared'),
      k('R8', clip='stand', expr='shocked')])],
  'props': [P('ligne', 'powderLine', pos=LINE, opts={'goneAt': 'R5:cocaïne'})],
  'sfx': [{'at': 'R5:cocaïne', 'name': 'sniff', 'vol': 0.8},
          *[{'at': f'R6+{0.2 + i * 0.42:.2f}', 'name': 'tick', 'vol': 0.7} for i in range(4)],
          {'at': 'R7', 'name': 'heartbeat', 'vol': 0.8}, {'at': 'R7+0.62', 'name': 'heartbeat', 'vol': 0.8}, {'at': 'R7+1.24', 'name': 'heartbeat', 'vol': 0.8},
          {'at': 'R8:flashback', 'name': 'whoosh', 'vol': 0.6}],
  'fx': [{'type': 'flash', 'at': 'R8.end-0.05', 'dur': 0.3}],
  'cams': [cam(0, 'serveur', 'ms', angle=20),
           cam('R5:sniffer', [[0.3, 0.97, -0.95]], 'cu', worldAngle=25, elev=25, noOcclusion=True),
           cam('R6', 'serveur', 'cu', angle=0),
           cam('R6:quatre', [[-2.9, 2.35, -3.15]], 'cu', worldAngle=0, noOcclusion=True, zoom=1.15),
           cam('R7', 'serveur', 'cu', angle=-25),
           cam('R7:complètement', [[-4.4, 1.15, -3.1]], 'ms', worldAngle=15, noOcclusion=True),
           cam('R7:paranoïaque', 'serveur', 'ms', angle=10),
           cam('R8', 'serveur', 'cu', angle=0, move='push', amount=0.12)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 3. flashback: Mao-era China, the black market
BOOM, CASE = [2.5, 0.55, -3.6], [2.62, 0.45, -3.0]
scenes.append({
  'id': 'chine', 'set': 'maoStreet', 'grade': SEPIA, 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('R9', "Chine, époque Mao. Tout produit occidental était interdit.", highlight=['Mao.', 'interdit.']),
            L('R10', "Mais lui était passionné par les États-Unis.", highlight=['États-Unis.']),
            L('R11', "Au marché noir, il achetait de la musique occidentale.", highlight=['noir,', 'musique']),
            L('R12', "« Fruit de la passion », de Franky Vincent.", highlight=['Fruit', 'passion']),
            L('R13', "Il pleurait devant tant de beauté.", highlight=['pleurait']),
            L('R14', "J'ai autre chose. Un produit occidental, d'une beauté immense.", 'dealer', pre=1.6),
            L('R15', "Des couverts.", highlight=['couverts.'])],
  'actors': [
    act('garde1', [0.6, 0, 0.7], -90, 'idle', 'suspicious', keys=[k(0.05, to=[-8.5, 0, 0.7], clip='walk', speed=1.5, then='stand')]),
    act('jeune', [-5.2, 0, -0.6], 90, 'idle', 'neutral', keys=[
        k('R10-0.2', to=[1.5, 0, -2.3], clip='sneak', speed=1.9, faceEnd=127, then='stand'),
        k('R12', clip='lookItem', expr='happy', face=140, turn=0.2),
        k('R13', clip='cry', expr='sad'),
        k('R14', clip='stand', expr='shocked', face='dealer', turn=0.25),
        k('R15', clip='lookItem', expr='happy', face=122, turn=0.2)]),
    act('dealer', [3.45, 0, -3.75], -53, 'lurk', 'suspicious', keys=[
        k('R11:musique', clip='present', expr='smug'),
        k('R12-0.25', clip='giveItem', expr='smug'),
        k('R13', clip='lurk', expr='neutral'),
        k('R14', clip='talk', expr='smug'),
        k('R15-0.45', clip='present', expr='smug')]),
  ],
  'props': [P('boombox', 'boombox', pos=BOOM, ry=-30, opts={'text': 'FRUIT DE LA PASSION', 'playAt': 'R12-0.05', 'stopAt': 'R14+0.9', 'bpm': 112}),
            P('mallette', 'cutleryCase', pos=CASE, ry=-60, opts={'openAt': 'R15-0.3', 'beam': True})],
  'sfx': [{'at': 'R12-0.05', 'name': 'music:zouk', 'until': 'R14+1.0', 'vol': 0.34, 'file': MUSIC_FILE, 'offset': 0.0},
          {'at': 'R12-0.12', 'name': 'click', 'vol': 0.5}, {'at': 'R15-0.3', 'name': 'choir', 'vol': 0.75}],
  'fx': [{'type': 'flash', 'at': 0, 'dur': 0.35}],
  'cams': [cam(0, ['garde1'], 'fs', worldAngle=8, elev=10),
           cam('R9:interdit', [[0.9, 1.7, -3.99]], 'cu', worldAngle=0, noOcclusion=True, zoom=1.1),
           cam('R10', 'jeune', 'fs', angle=-70, move='track'),
           cam('R11', ['jeune', 'dealer'], 'ms', worldAngle=37),
           POV('R12', [2.95, 0.98, -2.72], [2.5, 0.68, -3.6], 40),
           cam('R13', 'jeune', 'cu', angle=0),
           cam('R13.end+0.5', ['jeune', 'dealer'], 'ms', worldAngle=37),
           cam('R14', 'dealer', 'cu', angle=15),
           cam('R15-0.35', [[CASE[0], CASE[1] + 0.12, CASE[2]]], 'cu', worldAngle=-35, elev=35, noOcclusion=True),
           cam('R15.end+0.1', 'jeune', 'cu', angle=-10)],
  'tail': 0.5,
})

# ------------------------------------------------------------------ 4. three absurd uses of cutlery
YNG = [-0.4, 0, -2.55]
TIE = {'actor': 'jeune', 'joint': 'torso', 'offset': [0, 0.62, 0.14], 'rot': [0, 0, 3.1416]}
ANTENNA = {'actor': 'jeune', 'joint': 'head', 'offset': [0, 0.5, 0], 'rot': [0, 0, 0.12]}
scenes.append({
  'id': 'usages', 'set': 'maoStreet', 'grade': SEPIA, 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('R16', "Il ne savait pas s'en servir."),
            L('R17', "La cuillère, il s'en servait pour appeler l'Amérique.", highlight=['cuillère,', "l'Amérique."]),
            L('R18', "Allô ? L'Amérique ?", 'jeune'),
            L('R19', "Le couteau, il le portait comme une cravate.", highlight=['couteau,', 'cravate.']),
            L('R20', "Et la fourchette lui servait d'antenne, pour capter la radio américaine.", highlight=['fourchette', "d'antenne,"])],
  'actors': [act('jeune', YNG, 0, 'lookItem', 'suspicious', keys=[
      k('R17', clip='phoneCall', expr='happy'),
      k('R18.end+0.15', expr='sad'),
      k('R19', clip='heroPose', expr='smug'),
      k('R20', clip='stand', expr='happy'),
      k('R20:capter', clip='lookAround', expr='happy')])],
  'props': [P('fourchette', 'fork', scale=1.5, on={'actor': 'jeune', 'hand': 'R'}, keys=[k('R17', visible=False)]),
            P('cuillere', 'spoon', scale=2.0, visible=False, on={'actor': 'jeune', 'hand': 'R', 'offset': [0, -0.04, 0.02], 'rot': [3.1416, 0, 0]}, keys=[k('R17', visible=True), k('R19', visible=False)]),
            P('cravate', 'knife', scale=2.1, opts={'handle': '#2A2420'}, visible=False, on=TIE, keys=[k('R19', visible=True)]),
            P('antenne', 'fork', scale=1.6, visible=False, on=ANTENNA, keys=[k('R20:fourchette', visible=True)])],
  'sfx': [{'at': 'R18.end+0.1', 'name': 'beep', 'vol': 0.4}, {'at': 'R18.end+0.35', 'name': 'beep', 'vol': 0.4},
          {'at': 'R19:cravate', 'name': 'pop', 'vol': 0.4}, {'at': 'R20:capter', 'name': 'static', 'vol': 0.6}],
  'cams': [cam(0, 'jeune', 'ms', angle=15),
           cam('R16:servir', 'jeune', 'cu', angle=30),
           cam('R17', 'jeune', 'ms', angle=20),
           cam('R18', 'jeune', 'cu', angle=10),
           cam('R18.end+0.1', 'jeune', 'cu', angle=0, move='push', amount=0.04),
           cam('R19', 'jeune', 'ms', angle=0),
           cam('R20', 'jeune', 'ms', angle=-15),
           cam('R20:capter', 'jeune', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 5. the arrest
scenes.append({
  'id': 'arrestation', 'set': 'maoStreet', 'grade': SEPIA, 'ambience': 'park', 'ambienceVol': 0.4,
  'lines': [L('R21', "La police est arrivée. Motif : haute trahison et intelligence avec l'ennemi.", highlight=['Motif', 'trahison'])],
  'actors': [
    act('jeune', YNG, 0, 'stand', 'happy', keys=[k('R21:police', expr='shocked', clip='startle'), k('R21:Motif', clip='handcuffed', expr='sad')]),
    act('garde1', [-5.6, 0, 1.4], 70, 'idle', 'angry', keys=[k(0.0, path=[[-3.2, 0, -0.4], [-1.25, 0, -2.25]], clip='run', speed=5.0, faceEnd='jeune', then='cuffOther')]),
    act('garde2', [6.5, 0, 0.6], -70, 'idle', 'angry', keys=[k(0.1, path=[[3.0, 0, -0.8], [0.45, 0, -2.1]], clip='run', speed=5.0, faceEnd='jeune', then='point')]),
  ],
  'props': [P('cravate', 'knife', scale=2.1, opts={'handle': '#2A2420'}, on=TIE), P('antenne', 'fork', scale=1.6, on=ANTENNA),
            P('cuffs', 'handcuffs', visible=False, on={'actor': 'jeune', 'hand': 'R'}, keys=[k('R21:Motif', visible=True)])],
  'sfx': [{'at': 0.05, 'name': 'whistle', 'vol': 0.6}, {'at': 'R21:Motif', 'name': 'cuff', 'vol': 0.6}],
  'cams': [cam(0, 'garde1', 'fs', angle=-60, move='track'),
           cam('R21:arrivée+0.2', ['jeune', 'garde1', 'garde2'], 'ms', worldAngle=5),
           cam('R21:Motif', 'jeune', 'cu', angle=0),
           cam('R21:trahison', ['jeune', 'garde1'], 'ms', worldAngle=-20),
           cam('R21:intelligence', 'jeune', 'cu', angle=10, move='push', amount=0.04)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 6. five years in a 40 cm cell
CELL = [-0.06, 0, -1.69]
scenes.append({
  'id': 'prison', 'set': 'tinyCell', 'grade': SEPIA, 'ambience': 'cave', 'ambienceVol': 0.8,
  'lines': [L('R22', "Cinq ans de prison, dans une cellule de quarante centimètres.", highlight=['Cinq', 'quarante']),
            L('R23', "Un repas par an : une photo de riz.", highlight=['photo', 'riz.']),
            L('R24', "Pour lit, une baguette. Une seule.", highlight=['baguette.', 'seule.']),
            L('R25', "Pour fenêtre, un dessin de fenêtre.", highlight=['dessin'])],
  'actors': [
    act('detenu', CELL, 0, 'stiff', 'sad', keys=[
        k('R23:photo-0.2', clip='takeItem', expr='neutral'), k('R23:riz', clip='lookItem', expr='sad'),
        k('R24', clip='lookItem', expr='sad'), k('R24:seule', expr='unimpressed'),
        k('R25', clip='lookUp', expr='sad')]),
    act('garde1', [2.8, 0, -0.5], -90, 'idle', 'unimpressed', keys=[k('R23-1.0', to=[0.62, 0, -0.85], clip='walk', speed=2.6, faceEnd=200, then='stand'), k('R23-0.1', clip='giveItem')]),
  ],
  'props': [P('photo', 'photo', scale=1.4, visible=False, on={'actor': 'garde1', 'hand': 'R', **HAND_FLAT},
              keys=[k('R23', visible=True), k('R23:photo', attach='detenu', hand='R', offset=[0, -0.12, 0.03], rot=[1.5708, 0, 0]), k('R24', visible=False)]),
            P('baguette', 'chopsticks', scale=1.7, visible=False, opts={'single': True}, on={'actor': 'detenu', 'hand': 'R', 'offset': [0, -0.04, 0.02], 'rot': [3.1416, 0, 0]}, keys=[k('R24', visible=True), k('R25', visible=False)])],
  'sfx': [{'at': 0.05, 'name': 'thud', 'vol': 0.6}],
  'cams': [cam(0, 'detenu', 'fs', worldAngle=0, elev=4),
           POV('R22:quarante', [0, 1.45, 2.6], [0, 1.25, -1.7], 50),
           cam('R23', ['detenu', 'garde1'], 'ms', worldAngle=25),
           cam('R23:riz', 'photo', 'cu', worldAngle=0, noOcclusion=True, zoom=1.4),
           cam('R24', 'detenu', 'ms', angle=0, withProps=True),
           cam('R24:seule', 'detenu', 'cu', angle=0),
           cam('R25', 'detenu', 'cu', angle=0, elev=-12),
           POV('R25:dessin', [-0.4, 1.3, -0.72], [0.16, 2.22, -1.98], 40)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 7. France: he works like mad, opens his restaurant
SACK = lambda hand: {'actor': 'serveur', 'hand': hand}
scenes.append({
  'id': 'france', 'set': 'street', 'grade': SEPIA, 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('R26', "Puis il est parti en France. Il a bossé comme un malade.", highlight=['France.', 'malade.'])],
  'actors': [act('serveur', [-6.5, 0, 0.6], 90, 'idle', 'neutral', keys=[
      k(0.05, to=[6.5, 0, 0.6], clip='run', speed=7.5, then='idle'),
      k('R26:bossé', to=[-6.5, 0, 1.2], clip='run', speed=8.0, then='idle', expr='sad')])],
  'props': [P('sac1', 'foodSack', scale=0.5, opts={'text': 'RIZ', 'color': '#E6DCC4'}, on=SACK('R')),
            P('sac2', 'foodSack', scale=0.5, opts={'text': 'RIZ', 'color': '#E6DCC4'}, on=SACK('L')),
            P('sac3', 'foodSack', scale=0.5, visible=False, opts={'text': 'RIZ', 'color': '#E6DCC4'}, on={'actor': 'serveur', 'joint': 'head', 'offset': [0, 0.5, 0]}, keys=[k('R26:bossé', visible=True)])],
  'cams': [cam(0, 'serveur', 'fs', angle=-70, move='track'),
           cam('R26:bossé', 'serveur', 'fs', angle=70, move='track')],
  'tail': 0.1,
})
scenes.append({
  'id': 'ouverture', 'set': 'chineseRestaurant', 'grade': SEPIA, 'ambience': 'bar', 'ambienceVol': 0.4,
  'lines': [L('R27', "Et il a ouvert son restaurant.", highlight=['restaurant.'])],
  'actors': [act('serveur', [-1.4, 0, -2.0], 0, 'heroPose', 'happy')],
  'sfx': [{'at': 'R27:restaurant', 'name': 'kaching', 'vol': 0.6}],
  'cams': [cam(0, 'serveur', 'ms', angle=0),
           cam('R27:ouvert', ['serveur', [-1.4, 2.75, -3.5]], 'fs', worldAngle=0)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 8. back to the kitchen: the second line, love for the Party, the post
POST = (0.75, 0.925, -0.45)
scenes.append({
  'id': 'trace2', 'set': 'proKitchen', 'ambience': 'lab', 'ambienceVol': 0.6,
  'lines': [L('R28', "Retour en cuisine. Il a pris une deuxième trace.", highlight=['deuxième']),
            L('R29', "Il s'est souvenu de la grandeur de la Chine.", highlight=['grandeur']),
            L('R30', "Et de son amour pour le Parti communiste chinois.", highlight=['amour', 'Parti']),
            L('R31', "Alors il a dénoncé ce mec sur les réseaux sociaux chinois.", highlight=['dénoncé'])],
  'actors': [act('serveur', WAITER_ISLAND, 0, 'wired', 'scared', keys=[
      k('R28:pris', clip='leanTable', expr='angry'),
      k('R29', clip='lookUp', expr='happy'),
      k('R30', clip='raiseOverhead', expr='happy'),
      k('R31', clip='readPhone', expr='angry')])],
  'props': [P('ligne', 'powderLine', pos=LINE, opts={'goneAt': 'R28:trace'}),
            P('drapeau', 'flag', scale=0.45, visible=False, opts={'colors': ['#DE2910'], 'prc': True, 'grip': True}, on={'actor': 'serveur', 'hand': 'R', **SIGN_UP},
              keys=[k('R30', visible=True), k('R31', visible=False)]),
            P('tel', 'phone911', visible=False, on={'actor': 'serveur', 'hand': 'R'}, keys=[k('R31', visible=True)]),
            tweet_on_table('post', *POST, name="Le Lotus d'Or", handle='@lotus_dor', initial='L', avatar='#B5302A', via='Publié il y a 1 min',
                           text="Un Français a mangé avec des COUVERTS dans mon restaurant. Honte à lui.", likes='1,4 milliard de partages')],
  'sfx': [{'at': 'R28:trace', 'name': 'sniff', 'vol': 0.8}, {'at': 'R29:souvenu', 'name': 'choir', 'vol': 0.7},
          {'at': 'R30:Parti', 'name': 'fanfare', 'vol': 0.7}, {'at': 'R31:réseaux', 'name': 'pop', 'vol': 0.5}],
  'cams': [cam(0, 'serveur', 'ms', angle=20),
           cam('R28:pris', [[0.3, 0.97, -0.95]], 'cu', worldAngle=25, elev=25, noOcclusion=True),
           cam('R29', 'serveur', 'cu', angle=0, elev=-10),
           cam('R30', 'serveur', 'ms', angle=10, elev=-6, withProps=True),
           cam('R31', 'serveur', 'ms', angle=-20),
           tweet_cam('R31:réseaux', *POST)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 9. world scandal
scenes.append({
  'id': 'scandale', 'set': 'pressRoom', 'setOpts': {'backdrop': 'FOURCHETTEGATE|SCANDALE|COUVERTS', 'bg': '#D9E2E8', 'fg': '#2E4563', 'fontScale': 0.6}, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('R32', "Scandale mondial.", highlight=['Scandale', 'mondial.'])],
  'actors': [],
  'props': [P('preuve', 'fork', scale=2.4, pos=[0, 1.15, -1.92]), P('cloche', 'glassDome', pos=[0, 1.15, -1.92], opts={'radius': 0.15, 'height': 0.62, 'base': False, 'opacity': 0.2})],
  'sfx': [{'at': 0.05, 'name': 'shutter', 'vol': 0.5}, {'at': 0.45, 'name': 'shutter', 'vol': 0.5}, {'at': 0.85, 'name': 'shutter', 'vol': 0.5}],
  'cams': [cam(0, [[0, 1.42, -1.92]], 'cu', worldAngle=0, elev=8, noOcclusion=True, zoom=1.3),
           POV('R32:mondial', [0, 2.3, 5.2], [0, 1.25, -2.0], 34)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 10. the mob of patriotic netizens, led by Mbappé
DOG_POT, CAT_POT = [2.3, 0, -2.85], [3.8, 0, -2.85]
EXTRAS = [{'id': 'foule', 'count': 3, 'spec': {'preset': 'internaute', 'suit': '#5A6E8C', 'seed': 60}, 'clip': 'chant', 'ry': 180, 'positions': [[-2.6, 0, 3.2], [-0.6, 0, 3.3], [3.6, 0, 3.7]]},
          {'id': 'foulb', 'count': 3, 'spec': {'preset': 'internaute2', 'suit': '#C9729A', 'seed': 70}, 'clip': 'chant', 'ry': 180, 'positions': [[-1.6, 0, 3.6], [2.6, 0, 3.4], [4.6, 0, 3.3]]}]
scenes.append({
  'id': 'foule', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.6,
  'crowd': EXTRAS,
  'lines': [L('R33', "Des internautes patriotes ont débarqué chez lui. Avec des fourchettes.", highlight=['patriotes', 'fourchettes.']),
            L('R34', "Avec des baguettes, ça ferait moins mal, pas vrai ?", 'internaute'),
            L('R35', "Ils ont aussi planté ses animaux. Au couteau.", highlight=['planté', 'couteau.']),
            L('R36', "Avec des baguettes, on y serait encore.", 'internaute2'),
            L('R37', "Gloire à la République populaire !", 'internaute'),
            L('R38', "En tête du cortège : Kylian Mbappé.", highlight=['Mbappé.']),
            L('R39', "Il dénonçait la gravité des couverts dans un restaurant chinois.", highlight=['gravité'])],
  'actors': [
    act('mec', [0.97, 0, -3.6], 0, 'idle', 'neutral', keys=[
        k(0.2, to=[0.97, 0, -1.95], clip='walk', speed=1.5, then='stand'),
        k('R33:débarqué', expr='shocked', clip='scared'),
        k('R33.end-0.15', face=180, turn=0.2, clip='scared'),
        k('R33.end+0.3', clip='startle', expr='shocked'),
        k('R34:moins', clip='scratchButt', expr='sad'),
        k('R37', face=0, turn=0.25, clip='scared', expr='scared'),
        k('R39', clip='cry', expr='sad')]),
    act('internaute', [0.2, 0, 5.4], 180, 'idle', 'angry', keys=[
        k(0.05, path=[[0.4, 0, 1.6], [0.85, 0, -0.95]], clip='walk', speed=2.3, faceEnd=180, then='chant'),
        k('R33.end+0.05', clip='pokeFinger', expr='angry'),
        k('R33.end+0.55', clip='stand', expr='smug'),
        k('R34', clip='laugh', expr='smug'),
        k('R37', clip='chant', expr='angry')]),
    act('internaute2', [1.8, 0, 5.6], 180, 'idle', 'angry', keys=[
        k(0.15, path=[[2.4, 0, 1.6], [4.8, 0, -2.15]], clip='walk', speed=2.6, faceEnd=-110, then='chant'),
        k('R36', clip='talk', expr='smug'), k('R37', clip='chant', expr='angry')]),
    act('mbappe', [1.15, 0, 6.0], 180, 'idle', 'angry', keys=[
        k(0.1, path=[[1.25, 0, 1.4], [1.7, 0, -0.35]], clip='walk', speed=2.2, faceEnd='mec', then='stand'),
        k('R37', clip='point', expr='angry'),
        k('R39', clip='point', expr='angry')]),
    act('fan1', [-0.7, 0, 6.2], 180, 'idle', 'angry', keys=[k(0.25, path=[[-0.6, 0, 1.8], [-1.35, 0, 0.7]], clip='walk', speed=2.3, faceEnd=170, then='holdSign')]),
    act('fan2', [2.6, 0, 6.3], 180, 'idle', 'angry', keys=[k(0.3, path=[[2.3, 0, 1.9], [2.95, 0, 0.8]], clip='walk', speed=2.3, faceEnd=-170, then='holdSign')]),
    act('chien', [DOG_POT[0] - 0.15, 0.3, DOG_POT[2]], 0, 'sit', 'neutral', scale=1.2, visible=False, keys=[k('R35-0.15', visible=True)]),
    act('chat', [CAT_POT[0], 0.33, CAT_POT[2]], 0, 'sit', 'neutral', scale=1.2, visible=False, keys=[k('R35-0.15', visible=True)]),
  ],
  'props': [P('f1', 'fork', scale=4.0, opts={'handle': '#B5302A'}, on={'actor': 'internaute', 'hand': 'R', **FORK_UP},
              keys=[k('R33.end+0.3', attach='mec', joint='hips', offset=[0.06, -0.05, -0.74], rot=[1.32, 0, 0], sfx='boing')]),
            P('f2', 'fork', scale=4.0, opts={'handle': '#B5302A'}, on={'actor': 'internaute2', 'hand': 'R', **FORK_UP}),
            P('mega', 'megaphone', on={'actor': 'mbappe', 'hand': 'R', 'offset': [0, -0.1, 0.0], 'rot': [1.5708, 0, 0]}),
            P('pancarte1', 'protestSign', scale=0.8, opts={'text': 'COUVERTS = CRIME', 'color': '#B3261E'}, on={'actor': 'fan1', 'hand': 'R', **SIGN_UP}),
            P('pancarte2', 'protestSign', scale=0.8, opts={'text': 'BAGUETTES OU RIEN', 'color': '#B3261E'}, on={'actor': 'fan2', 'hand': 'R', **SIGN_UP}),
            P('pot1', 'planter', pos=DOG_POT, visible=False, keys=[k('R35-0.15', visible=True)], opts={'w': 1.1, 'd': 0.75, 'sprouts': 2}),
            P('pot2', 'planter', pos=CAT_POT, visible=False, keys=[k('R35-0.15', visible=True)], opts={'w': 0.9, 'd': 0.75, 'sprouts': 2, 'seed': 9}),
            P('truelle', 'knife', scale=3.0, visible=False, keys=[k('R35-0.15', visible=True)], opts={'handle': '#2A2420'}, pos=[2.66, 0.86, -2.7], rot=[0.3, 0, 3.1416])],
  'sfx': [{'at': 'R33.end+0.3', 'name': 'thud', 'vol': 0.5}, {'at': 'R35:planté', 'name': 'pop', 'vol': 0.4}, {'at': 'R37:Gloire', 'name': 'fanfare', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=0, elev=6),
           POV('R33:débarqué', [0.4, 1.75, -3.85], [1.2, 1.25, 2.5], 34),
           cam('R33:fourchettes', 'internaute', 'ms', angle=10),
           cam('R33.end-0.1', ['mec', 'internaute'], 'ms', worldAngle=90),
           cam('R34+0.6', 'internaute', 'cu', angle=10),
           cam('R35', ['chien', 'chat'], 'ms', worldAngle=-8),
           cam('R35:couteau', ['chien', 'truelle'], 'cu', worldAngle=-5, withProps=True),
           cam('R36', 'internaute2', 'cu', angle=0),
           cam('R37', 'internaute', 'ms', angle=35),
           cam('R38', 'mbappe', 'cu', angle=0),
           cam('R39', ['mbappe', 'mec'], 'ms', worldAngle=60),
           cam('R39:restaurant', 'mec', 'cu', angle=-30)],
  'tail': 0.25,
})

# ------------------------------------------------------------------ 11. the apology, Mbappé humiliates him, he falls in love with China
BUTT_FORK = P('f1', 'fork', scale=4.0, opts={'handle': '#B5302A'}, on={'actor': 'mec', 'joint': 'hips', 'offset': [0.06, -0.05, -0.74], 'rot': [1.32, 0, 0]})
scenes.append({
  'id': 'excuses', 'set': 'pressRoom', 'setOpts': {'backdrop': 'PARDON|SORRY|EXCUSES|SCUSATE|LO SIENTO|DESCULPA', 'bg': '#D9E2E8', 'fg': '#2E4563', 'podium': False}, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('R40', "Ce mec avait tout perdu. Il a dû s'excuser.", highlight=['perdu.', "s'excuser."]),
            L('R41', "Mbappé l'a humilié : lui, il s'excusait en douze langues.", highlight=['humilié', 'douze']),
            L('R42', "Et là, d'un coup, ce mec est tombé amoureux de la Chine.", highlight=['amoureux'])],
  'actors': [
    act('mec', [0, 0, -1.6], 0, 'stand', 'sad', keys=[k('R40:excuser', clip='bowRepeat', params={'freq': 1.4}),
                                                       k('R41:douze', clip='stand', expr='shocked', look='mbappe'),
                                                       k('R42:coup', clip='lookUp', expr='happy', look=None)]),
    act('mbappe', [3.0, 0, -1.9], -90, 'stand', 'smug', keys=[k('R41', to=[1.05, 0, -1.65], clip='walk', speed=2.2, faceEnd=0, then='stand'),
                                                            k('R41:douze', clip='bowRepeat', params={'freq': 3.4}, expr='happy')]),
  ],
  'props': [BUTT_FORK],
  'sfx': [{'at': 'R40', 'name': 'shutter', 'vol': 0.5}, {'at': 'R41:douze', 'name': 'shutter', 'vol': 0.5}, {'at': 'R42:coup', 'name': 'choir', 'vol': 0.7}],
  'cams': [cam(0, 'mec', 'ms', angle=0),
           cam('R40:excuser', 'mec', 'fs', angle=80),
           POV('R41', [0.5, 1.95, 2.7], [0.5, 1.35, -1.6], 30),
           cam('R41:douze', 'mbappe', 'mcu', angle=15),
           cam('R42', 'mec', 'cu', angle=0, move='push', amount=0.08)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 12. the plane, he becomes Chinese
scenes.append({
  'id': 'avion', 'set': 'airport', 'ambience': 'station',
  'lines': [L('R43', "Il a pris l'avion. Il est devenu chinois.", highlight=["l'avion.", 'chinois.'])],
  'actors': [act('mecMao', [0.3, 0, -2.6], 0, 'idle', 'happy', visible=False, keys=[k('R43:devenu-0.05', visible=True), k('R43:devenu-0.3', to=[0.3, 0, -0.2], clip='walk', speed=1.6, then='salute')])],
  'props': [P('avion', 'plane', pos=[-26, 8.5, -25], keys=[k(0.0, to=[18, 10.5, -25], dur=2.0, ease='inOut')])],
  'sfx': [{'at': 0.0, 'name': 'jet', 'vol': 0.7}],
  'cams': [POV(0, [0, 1.1, 3.5], [-1, 7.2, -25], 40),
           cam('R43:devenu', 'mecMao', 'ms', angle=0)],
  'tail': 0.25,
})

# ------------------------------------------------------------------ 13. party official, the propaganda speech, the call to the police
RED_ROOM = {'backdrop': 'DÉMOCRATIE|HARMONIE|BONHEUR|PROSPÉRITÉ', 'bg': '#B5302A', 'fg': '#F2D16B', 'flagOpts': {'colors': ['#DE2910'], 'prc': True}}
scenes.append({
  'id': 'politique', 'set': 'pressRoom', 'setOpts': RED_ROOM, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('R44', "Il a rencontré les dirigeants chinois. Puis il est devenu dirigeant chinois.", highlight=['rencontré', 'devenu']),
            L('R45', "La Chine est la plus grande démocratie du monde. Économiquement, culturellement, socialement.", 'mecMao'),
            L('R46', "Je suis l'homme le plus heureux du monde.", 'mecMao'),
            L('R47', "La Chine n'a que de bonnes intentions. Elle n'a jamais été une dictature.", 'mecMao'),
            L('R48', "Ça, c'est la propagande occidentale.", 'mecMao')],
  'actors': [
    act('mecMao', [-0.45, 0, -1.0], 90, 'holdOut', 'happy', keys=[
        k('R44:devenu', to=PR_SPEAKER, glide=True, dur=0.05, face=0, clip='podiumTalk', expr='happy'),
        k('R46', expr='happy', clip='stand'), k('R47', clip='podiumTalk', expr='neutral'), k('R48', clip='podiumTalk', expr='smug')]),
    act('off1', [0.35, 0, -1.0], -90, 'holdOut', 'neutral', keys=[k('R44:devenu', to=[-1.05, 0, -2.55], glide=True, dur=0.05, face=0, clip='stand'),
                                                               k('R47', clip='nod'), k('R48', clip='celebrate', expr='happy')]),
    act('off2', [1.3, 0, -1.5], -60, 'nod', 'neutral', keys=[k('R44:devenu', to=[1.05, 0, -2.55], glide=True, dur=0.05, face=0, clip='stand'),
                                                          k('R47', clip='nod'), k('R48', clip='celebrate', expr='happy')]),
    act('souffleur', [2.1, 0, -1.35], -70, 'stand', 'unimpressed', keys=[k('R46-0.2', clip='holdSign')]),
  ],
  'props': [P('carton', 'protestSign', scale=0.55, visible=False, opts={'text': 'SOURIEZ', 'color': '#1E2E44'}, on={'actor': 'souffleur', 'hand': 'R', **SIGN_UP},
              keys=[k('R46-0.2', visible=True), k('R47', visible=False)])],
  'sfx': [{'at': 'R44:devenu', 'name': 'shutter', 'vol': 0.5}, {'at': 'R48:propagande', 'name': 'shutter', 'vol': 0.4}],
  'cams': [POV(0, [0.6, 2.05, 3.0], [-0.05, 1.25, -1.0], 30),
           cam('R44:devenu', 'mecMao', 'ms', angle=0),
           cam('R45', 'mecMao', 'mcu', angle=10),
           cam('R45:Économiquement', ['mecMao', 'off1', 'off2'], 'fs', worldAngle=0, elev=5),
           cam('R46', 'mecMao', 'cu', angle=0),
           cam('R46:heureux', 'carton', 'cu', worldAngle=-25, noOcclusion=True, zoom=1.2),
           cam('R47', 'mecMao', 'mcu', angle=-10),
           cam('R47:dictature', ['off1', 'off2'], 'ms', worldAngle=0),
           cam('R48', 'mecMao', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})
scenes.append({
  'id': 'appel', 'set': 'pressRoom', 'setOpts': RED_ROOM, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('R49', "Puis il a appelé la police. Motif : trafic de stupéfiants.", highlight=['Motif', 'stupéfiants.']),
            L('R50', "Et sa cuisine n'est pas à la hauteur d'une nation souveraine.", 'mecMao')],
  'actors': [act('mecMao', PR_SPEAKER, 0, 'phoneCall', 'smug')],
  'props': [P('tel', 'phone911', on={'actor': 'mecMao', 'hand': 'R'})],
  'cams': [cam(0, 'mecMao', 'mcu', angle=20),
           cam('R49:Motif', 'mecMao', 'cu', angle=0),
           cam('R50', 'mecMao', 'cu', angle=-20)],
  'tail': 0.15,
})

# ------------------------------------------------------------------ 14. the waiter was right
scenes.append({
  'id': 'fin', 'set': 'proKitchen', 'ambience': 'lab', 'ambienceVol': 0.6,
  'lines': [L('R51', "Le serveur avait raison d'être paranoïaque.", pre=0.5, highlight=['paranoïaque.'])],
  'actors': [
    act('serveur', WAITER_ISLAND, 0, 'leanTable', 'happy', keys=[k(0.45, clip='startle', expr='shocked'), k(0.95, clip='handcuffed', expr='scared'),
                                                               k('R51:paranoïaque', clip='stareCamera', expr='unimpressed')]),
    act('flic1', [-4.4, 0, -2.4], 120, 'idle', 'angry', keys=[k(0.0, path=[[-2.4, 0, -1.6], [-0.55, 0, -1.55]], clip='run', speed=5.5, faceEnd='serveur', then='cuffOther')]),
    act('flic2', [-4.6, 0, -1.6], 100, 'idle', 'angry', keys=[k(0.1, path=[[-2.0, 0, -0.1], [1.35, 0, -1.65]], clip='run', speed=6.0, faceEnd='serveur', then='point')]),
  ],
  'props': [P('ligne', 'powderLine', pos=LINE),
            P('cuffs', 'handcuffs', visible=False, on={'actor': 'serveur', 'hand': 'R'}, keys=[k(0.95, visible=True)])],
  'sfx': [{'at': 0.0, 'name': 'siren', 'vol': 0.5}, {'at': 0.95, 'name': 'cuff', 'vol': 0.6}],
  'cams': [cam(0, ['serveur', [-0.55, 1.0, -1.55], [1.35, 1.0, -1.65]], 'ms', worldAngle=10, elev=8),
           cam('R51:raison', 'serveur', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.5,
})

write('restochinois', 'Le resto chinois', scenes, {
  'serveur': {'preset': 'restaurateur', 'seed': 77},
  'jeune': {'preset': 'restaurateurMao', 'seed': 77},
  'detenu': {'preset': 'restaurateurMao', 'seed': 77, 'hat': 'none'},
  'dealer': {'preset': 'dealer', 'seed': 12},
  'garde1': {'preset': 'policeMao', 'seed': 21},
  'garde2': {'preset': 'policeMao', 'seed': 22},
  'internaute': {'preset': 'internaute', 'seed': 31},
  'internaute2': {'preset': 'internaute2', 'seed': 32},
  'fan1': {'preset': 'internaute', 'suit': '#2C4A8A', 'seed': 33},
  'fan2': {'preset': 'internaute2', 'suit': '#3E8A5A', 'seed': 34},
  'mbappe': {'preset': 'footballeur'},
  'chien': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 4}},
  'chat': {'type': 'creature', 'name': 'cat', 'opts': {'seed': 6}},
  'mecMao': {'preset': 'mecMao'},
  'off1': {'preset': 'officiel', 'seed': 41},
  'off2': {'preset': 'officiel', 'seed': 42, 'glasses': False},
  'souffleur': {'preset': 'officiel', 'seed': 43, 'build': {'belly': 0.0}},
})
