#!/usr/bin/env python3
"""LE FRIGO. Ce mec installs a camera to watch his fridge -> at night someone eats his yoghurts -> he watches the video ->
it was him, sleepwalking -> ce con files a complaint against himself -> the cops arrest him -> two years -> he visits
himself in the visiting room -> he brings himself yoghurts. (Classic formula.)"""
from actu_common import *

NV = 'sepia(1) hue-rotate(55deg) saturate(2.2) contrast(1.25) brightness(0.85)'   # night-vision camera footage
FR = [-2.7, 0, -3.22]                                                          # the set's fridge
CAMPOS = [1.5, 2.5, -3.48]                                                     # CCTV on the back wall, far corner: a wide view of the fridge
CAMVIEW = lambda at: {**POV(at, [CAMPOS[0] - 0.08, CAMPOS[1] - 0.12, CAMPOS[2] + 0.2], [-2.4, 1.0, -1.8], 48), 'grade': NV}
scenes = []
scenes.append({
  'id': 'cuisine', 'set': 'kitchenNight', 'lighting': 'night', 'ambience': 'night', 'ambienceVol': 0.4,
  'lines': [L('R1', "Ce mec a installé une caméra pour surveiller son frigo.", highlight=['caméra', 'frigo.']),
            L('R2', "La nuit, quelqu'un mangeait ses yaourts.", highlight=['yaourts.']),
            L('R3', "Il a regardé la vidéo.", highlight=['vidéo.']),
            L('R4', "C'était lui. Somnambule.", highlight=['lui.', 'Somnambule.'])],
  'actors': [act('mec', [0.4, 0, -1.9], 10, 'armsCrossed', 'smug', keys=[k('R2', visible=False), k('R3', visible=True), k('R3', to=[-0.2, 0.12, -1.2], glide=True, dur=0.05, face=0, clip='sit', then='sit', expr='neutral'),
                                                                            k('R3:vidéo', clip='sitLookItem'), k('R4:Somnambule', expr='shocked')]),
             act('somnambule', [-2.55, 0, -1.75], 70, 'holdOut', 'sleepy', visible=False, keys=[k('R2', visible=True), k('R2:yaourts', clip='eatSpoon'), k('R3', visible=False), k('R4', visible=True), k('R4', clip='holdOut'), k('R4:Somnambule', visible=False)])],
  'props': [P('cam', 'securityCam', pos=CAMPOS, ry=-68), P('chaise', 'chair', pos=[-0.2, 0, -1.28]),
            P('yaourt', 'yogurt', visible=False, on={'actor': 'somnambule', 'hand': 'L', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}, keys=[k('R2:yaourts', visible=True)]),
            P('cuillere', 'spoon', visible=False, on={'actor': 'somnambule', 'hand': 'R'}, keys=[k('R2:yaourts', visible=True)]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('R3', visible=True)])],
  'sfx': [{'at': 'R1:caméra', 'name': 'beep', 'vol': 0.4}, {'at': 'R2', 'name': 'squeak', 'vol': 0.3}, {'at': 'R4:Somnambule', 'name': 'sting', 'vol': 0.35}],
  'cams': [cam(0, ['mec', 'cam'], 'ms', worldAngle=10, withProps=True),
           cam('R1:caméra', [CAMPOS], 'cu', worldAngle=-40, noOcclusion=True, zoom=1.2),
           CAMVIEW('R2'),
           cam('R3', 'mec', 'ms', angle=0),
           CAMVIEW('R4'),
           cam('R4:Somnambule', 'mec', 'cu', angle=0)],
  'tail': 0.2,
})
DESK = [-2.7, 0, -2.1]
scenes.append({
  'id': 'commissariat', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('R5', "Alors ce con a porté plainte. Contre lui-même.", highlight=['plainte.', 'lui-même.']),
            L('R6', "Les flics l'ont arrêté.", highlight=['arrêté.']),
            L('R7', "Deux ans ferme.", highlight=['Deux', 'ferme.'])],
  'actors': [act('commissaire', [DESK[0], 0.12, DESK[2] - 0.62], 0, 'sitWrite', 'neutral', keys=[k('R5#7', clip='sit', expr='suspicious')]),
             act('mec', [DESK[0] + 0.2, 0, DESK[2] + 1.0], 180, 'stand', 'angry', keys=[k('R5:Contre', clip='pointSelf', expr='angry'), k('R6', face='flic1', turn=0.3, clip='stand', expr='neutral'),
                                                                            k('R6:arrêté', clip='cuffedFront', expr='shocked'), k('R7', face=10, turn=0.3, expr='sad')]),
             act('flic1', [-0.4, 0, -0.5], -110, 'idle', 'neutral', keys=[k('R6-0.4', to=[DESK[0] + 1.0, 0, DESK[2] + 1.2], clip='walk', speed=3.0, faceEnd='mec', then='cuffOther')])],
  'props': [P('menottes', 'handcuffs', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('R6:arrêté', visible=True)])],
  'sfx': [{'at': 'R6:arrêté', 'name': 'cuff', 'vol': 0.6}, {'at': 'R7', 'name': 'gavel', 'vol': 0.5}],
  'cams': [POV(0, [-0.7, 1.6, 0.4], [-2.6, 1.1, -1.9], 50),
           cam('R5:Contre', 'mec', 'mcu', angle=0),
           cam('R5#7', 'commissaire', 'cu', angle=0),
           cam('R6', ['mec', 'flic1'], 'ms', worldAngle=-10),
           cam('R7', 'mec', 'cu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'parloir', 'set': 'interrogation', 'ambience': None,
  'lines': [L('R8', "Putain, il se rend visite au parloir.", highlight=['parloir.']),
            L('R9', "Il s'apporte des yaourts.", highlight=['yaourts.'])],
  'actors': [act('detenu', IR_SUSPECT, 0, 'sit', 'sad', keys=[k('R9:yaourts', clip='sitTake', expr='happy')]),
             act('mec', [0.98, 0, -0.85], -90, 'stand', 'neutral', keys=[k('R9', clip='giveItem', expr='neutral')])],
  'props': [P('yaourt', 'yogurt', on={'actor': 'mec', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}, keys=[k('R9:yaourts', attach='detenu', hand='R', rot=[1.5708, 0, 0], offset=[0, -0.12, -0.05])])],
  'cams': [cam(0, ['detenu', 'mec'], 'ms', worldAngle=-20),
           cam('R8:parloir', 'detenu', 'cu', angle=0),
           cam('R9', ['detenu', 'mec'], 'ms', worldAngle=-20),
           cam('R9:yaourts+0.3', 'mec', 'cu', angle=-35, move='push', amount=0.04)],
  'tail': 1.4,
})
write('frigo', 'Le frigo', scenes, {'mec': {'preset': 'mecPyjama'}, 'somnambule': {'preset': 'mecPyjama'}, 'detenu': {'preset': 'mecPrisonnier'}})
