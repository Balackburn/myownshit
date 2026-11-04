#!/usr/bin/env python3
"""LE GPS (viral-video-writing loop, score_fr.py 100/100). Hook with a named thing (the GPS) -> the villain at 4 s (the GPS voice)
-> right turn into a lake -> recalculating: a field, the Channel -> four days later, Spain -> the boss reports him missing -> he
resigns by postcard and sells ice cream on the beach -> callback: the boss arrives on the beach with the same GPS."""
from actu_common import *

ROAD_Y, DRIVE = -0.14, -4.4
SEAT = (0.05, 0.12, -0.4)
def seat(x, z, y=ROAD_Y): return [x + SEAT[0], y + SEAT[1], z + SEAT[2]]
def drive(x0, x1, dur, z=DRIVE, y=ROAD_Y, color='#C9473A', gps_text='→ 200 m', extra_car=(), extra_mec=(), who='mec', car='voiture'):
    return (P(car, 'car', pos=[x0, y, z], opts={'color': color}, keys=[k(0, to=[x1, y, z], dur=dur, ease='linear'), *extra_car]),
            act(who, seat(x0, z, y), 90, 'drive', 'neutral', keys=[k(0, to=seat(x1, z, y), glide=True, dur=dur, ease='linear', clip='drive', then='drive', face='keep'), *extra_mec]),
            P(f'gps_{car}', 'gpsDevice', opts={'text': gps_text}, on={'actor': car, 'offset': [0.98, 1.12, -0.25]}))
scenes = []
car, mec, gps = drive(-14, 2.0, 4.6)
scenes.append({
  'id': 'route', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('GP1', "Ce mec a suivi son GPS à la lettre pour aller au travail.", highlight=['GPS', 'lettre']),
            L('GP2', "Dans deux cents mètres, tournez à droite.", 'gps')],
  'actors': [mec], 'props': [car, gps],
  'sfx': [{'at': 0, 'name': 'engine', 'vol': 0.35}],
  'cams': [POV(0, [2.0, 5.5, 1.5], [-8.0, 0.0, -4.4], 50),
           cam('GP1:GPS', 'mec', 'cu', worldAngle=65, move='track', noOcclusion=True),
           cam('GP2', 'gps_voiture', 'cu', worldAngle=-60, noOcclusion=True, move='track')],
  'tail': 0.15,
})
LAKE = [[3.0, 0, -1.0], [3.0, 0, -5.6], [3.0, -0.2, -8.4], [3.0, -1.2, -10.4]]     # car faces -z (ry 90): its driver seat is at (-0.4, 0.12, -0.05)
def lake_keys(dx=0.0, dy=0.0, dz=0.0, extra=None):
    pts = [[p[0] + dx, p[1] + dy, p[2] + dz] for p in LAKE]
    base = dict(extra or {})
    return [k(0.1, to=pts[1], dur=1.0, ease='linear', **base), k(1.1, to=pts[2], dur=0.45, ease='linear', **base), k(1.55, to=pts[3], dur=0.5, ease='in', **base)]
scenes.append({
  'id': 'lac', 'set': 'beach', 'ambience': 'beach', 'ambienceVol': 0.5,
  'lines': [L('GP3', "À droite, il y avait un lac.", highlight=['lac.'])],
  'actors': [act('mec', [LAKE[0][0] - 0.4, 0.12, LAKE[0][2] - 0.05], 180, 'drive', 'happy',
                 keys=lake_keys(-0.4, 0.12, -0.05, {'glide': True, 'clip': 'drive', 'then': 'drive', 'face': 'keep'}) + [k('GP3:lac', expr='shocked')])],
  'props': [P('voiture', 'car', pos=LAKE[0], ry=90, opts={'color': '#C9473A'}, keys=lake_keys())],
  'sfx': [{'at': 'GP3:lac', 'name': 'splash', 'vol': 0.8}, {'at': 'GP3:lac+0.3', 'name': 'gulp', 'vol': 0.5}],
  'cams': [POV(0, [7.5, 1.8, 0.5], [2.6, 0.3, -7.2], 50)],
  'tail': 0.2,
})
car, mec, gps = drive(-9, 9, 4.8, z=0.0, y=0.0, gps_text='RECALCUL…')
scenes.append({
  'id': 'champ', 'set': 'farm', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('GP4', "Le GPS a recalculé. Puis un champ. Puis la Manche.", highlight=['recalculé.', 'Manche.'])],
  'actors': [mec],
  'props': [car, gps, P('ble', 'tallGrass', pos=[0, 0, 0.2], opts={'w': 14, 'd': 3.0, 'h': 0.9, 'count': 420}),
            P('manche', 'floorSlab', pos=[16, -0.13, 0], opts={'w': 14, 'd': 12, 'floor': '#3E7FA8', 'lamp': False}),
            P('panneau', 'signBoard', pos=[8.6, 0, -1.8], opts={'text': 'LA MANCHE', 'bg': '#2C4A8A', 'fg': '#F6F1E3', 'w': 1.2, 'h': 0.4, 'height': 1.2})],
  'sfx': [{'at': 'GP4:recalculé', 'name': 'beep', 'vol': 0.5}, {'at': 'GP4:champ', 'name': 'engine', 'vol': 0.4}, {'at': 'GP4:Manche', 'name': 'splash', 'vol': 0.7}],
  'cams': [cam(0, 'gps_voiture', 'cu', worldAngle=-60, noOcclusion=True, move='track'),
           cam('GP4:Puis', 'mec', 'fs', worldAngle=20, elev=20, move='track', noOcclusion=True)],
  'tail': 0.15,
})
scenes.append({
  'id': 'espagne', 'set': 'beach', 'ambience': 'beach', 'ambienceVol': 0.5,
  'lines': [L('GP5', "Quatre jours plus tard, il était en Espagne.", highlight=['Quatre', 'Espagne.'])],
  'actors': [act('mec', seat(-6.0, -6.5, 0.0), 90, 'drive', 'neutral', keys=[k(0, to=seat(0.2, -4.2, 0.0), glide=True, dur=1.8, ease='out', clip='drive', then='drive', face='keep', expr='grin')])],
  'props': [P('voiture', 'car', pos=[-6.0, 0, -6.5], opts={'color': '#C9473A'}, keys=[k(0, to=[0.2, 0, -4.2], dur=1.8, ease='out')]),
            P('espana', 'signBoard', pos=[2.6, 0, -2.6], opts={'text': 'ESPAÑA', 'bg': '#C8202A', 'fg': '#F2C230', 'w': 1.2, 'h': 0.42, 'height': 1.4})],
  'sfx': [{'at': 'GP5:Espagne', 'name': 'tada', 'vol': 0.35}],
  'cams': [POV(0, [3.6, 1.7, 2.2], [-1.2, 0.8, -4.0], 52)],
  'tail': 0.2,
})
scenes.append({
  'id': 'patron', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('GP6', "Son patron a signalé sa disparition à la police.", highlight=['disparition', 'police.']),
            L('GP7', "Alors ce con a démissionné par carte postale.", highlight=['démissionné', 'postale.'])],
  'actors': [act('patron', [0.4, 0, -1.5], 15, 'phoneCall', 'angry', keys=[k('GP7', clip='showPhone', expr='shocked')])],
  'props': [P('tel', 'phone911', on={'actor': 'patron', 'hand': 'R'}, keys=[k('GP7', visible=False)]),
            P('affiche', 'fitPoster', pos=[-0.9, 1.75, -3.55], opts={'text': 'DISPARU', 'bg': '#F6F1E3', 'fg': '#B5302A'}),
            P('carte', 'notebook', scale=1.7, visible=False, opts={'text': 'BONS\nBAISERS\nD\'ESPAGNE\n—\nJE\nDÉMISSIONNE', 'bg': '#2C8AB5'}, on={'actor': 'patron', 'hand': 'R', **HAND_FLAT}, keys=[k('GP7', visible=True)])],
  'sfx': [{'at': 'GP6:police', 'name': 'siren', 'vol': 0.3}, {'at': 'GP7:carte', 'name': 'paper', 'vol': 0.5}],
  'cams': [cam(0, 'patron', 'ms', angle=10), cam('GP7:carte', 'carte', 'mcu', worldAngle=15, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'plage', 'set': 'beach', 'ambience': 'beach', 'ambienceVol': 0.5,
  'lines': [L('GP8', "Il vend des glaces sur la plage.", highlight=['glaces']),
            L('GP9', "Hier, son patron est arrivé sur la plage.", highlight=['patron']),
            L('GP10', "Putain, avec le même GPS.", highlight=['GPS.']),
            L('GP11', "Il allait au travail.", highlight=['travail.'])],
  'actors': [act('mec', [0.3, 0, -1.6], 10, 'giveItem', 'grin', keys=[k('GP9', clip='stand', expr='neutral'), k('GP10', expr='shocked'), k('GP11', clip='stareCamera', expr='unimpressed')]),
             act('patron', seat(-9.0, -4.6, 0.0), 90, 'drive', 'neutral', keys=[k('GP9', to=seat(-2.4, -4.6, 0.0), glide=True, dur=1.4, ease='out', clip='drive', then='drive', face='keep'),
                                                                               k('GP11', expr='shocked')])],
  'props': [P('chariot', 'iceCreamCart', pos=[1.4, 0, -2.0], ry=-20),
            P('glace', 'iceCream', scale=1.8, on={'actor': 'mec', 'hand': 'R'}, keys=[k('GP9', visible=False)]),
            P('voitureP', 'car', pos=[-9.0, 0, -4.6], opts={'color': '#8C949A', 'plate': 'BOSS-01'}, keys=[k('GP9', to=[-2.4, 0, -4.6], dur=1.4, ease='out')]),
            P('gpsP', 'gpsDevice', opts={'text': 'ARRIVÉE'}, on={'actor': 'voitureP', 'offset': [0.98, 1.12, -0.25]}),
            P('espana', 'signBoard', pos=[3.0, 0, -2.8], opts={'text': 'ESPAÑA', 'bg': '#C8202A', 'fg': '#F2C230', 'w': 1.2, 'h': 0.42, 'height': 1.4})],
  'sfx': [{'at': 'GP9', 'name': 'engine', 'vol': 0.4}, {'at': 'GP9:arrivé+0.4', 'name': 'brake', 'vol': 0.5}, {'at': 'GP10:GPS', 'name': 'beep', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'ms', angle=-20),
           POV('GP9', [3.4, 1.8, 1.8], [-1.5, 0.8, -3.8], 52),
           cam('GP10:même', 'gpsP', 'cu', worldAngle=-60, noOcclusion=True),
           cam('GP11', 'patron', 'cu', worldAngle=65, noOcclusion=True),
           cam('GP11:travail', 'mec', 'cu', angle=0, move='push', amount=0.04)],
  'tail': 1.4,
})
write('gps', 'Le GPS', scenes, {'patron': {'preset': 'lemec_beige', 'seed': 33}})
