#!/usr/bin/env python3
"""LE LOOKSMAXING. Ce con se trouve moche -> a TikTok guru, Clavicule Large (fictional), sells him a course -> 72 injections:
steroids (he swells everywhere except the muscles), a tanning peptide (orange), smooth skin, slimming, one to get it up
again; every try fails and he gets uglier -> hard drugs for charisma (carfentanil, crystal meth) -> four surgeries (square
jaw, "attractive" eyes, wider clavicles, the rest) -> the gym, and micro-fractures with a chainsaw (by ellipsis) ->
disfigured, he finds himself handsome for the first time (we see how he sees himself) -> the date after 56 hours awake:
she leaves -> he did not go far enough: the $7000 conference, where Raphaël Glucksmann sits like a lost child -> Glucksmann
takes the full programme every morning; it works on him, and he still sleeps like a baby -> the perfect man: a 48-hour TV
interview, compared to God, president, then dictator of a utopia -> the jealous man's rebels confiscate the products ->
Glucksmann deflates, cries like a baby, his worshippers turn away -> he now makes videos on the dangers of looksmaxing.
Two hundred views.

Adjustments to the brief (see the delivery note): no sex scene and nothing on the private life of real people (the
"48 hours instead of 2 minutes" becomes a TV interview with a fictional journalist), no Hitler comparison, Glucksmann takes
"le programme" (no named hard drugs for a real person), the chainsaw happens off screen, and the guru is a fictional
character whose name is a pun."""
from actu_common import *

TIKTOK = 'contrast(1.02) saturate(1.2) brightness(1.06)'          # the guru's video
DREAM = 'contrast(0.82) saturate(1.15) brightness(1.18) sepia(0.12)'  # how he sees himself / the perfect man
SKIN_O = '#E99A60'                                                    # orange-tinted skin for the face add-ons
def face_on(actor, y, z, **kw):   # an add-on stuck on the face (head joint: origin at the bottom of the head)
    return {'actor': actor, 'joint': 'head', 'offset': [kw.get('x', 0), y, z], **({'rot': kw['rot']} if 'rot' in kw else {})}
def monster_face(actor, hs=0.8, lumps=True, vis=None):
    """the post-surgery face on an actor with head scale hs: square jaw, googly eyes, optional lumps + bandages"""
    hh, front = 0.5 * hs, 0.085 * hs
    ps = [P(f'jaw_{actor}', 'squareJaw', opts={'color': SKIN_O}, on=face_on(actor, 0.02, 0.05)),
          P(f'eyes_{actor}', 'googlyEyes', opts={'r': 0.042, 'sep': 0.05}, on=face_on(actor, hh * 0.6, front + 0.012))]
    if lumps: ps.append(P(f'lumps_{actor}', 'faceLumps', opts={'color': SKIN_O, 'seed': 5}, on=face_on(actor, hh * 0.55, front + 0.006)))
    if vis is not None:
        for p in ps: p.update(vis)
    return ps

scenes = []
# ------------------------------------------------------------------ 1. the bedroom: he finds himself ugly, the TikTok
MIRROR_B = [0.9, 0, -1.55]
scenes.append({
  'id': 'chambre', 'set': 'chambre', 'ambience': None,
  'lines': [L('K1', "Ce con se trouvait moche.", highlight=['moche.']),
            L('K2', "Un soir, sur TikTok, il est tombé sur Clavicule Large, gourou du looksmaxing.", highlight=['Clavicule', 'Large,'])],
  'actors': [act('mec', MIRROR_B, 180, 'stand', 'sad', keys=[
      k('K2', to=[-2.15, 0.27, -1.6], glide=True, dur=0.05, face=90, clip='sitLookItem', then='sitLookItem', expr='neutral'),
      k('K2:Clavicule', expr='happy')])],
  'props': [P('tel', 'phone911', visible=False, opts={'screen': 'tiktok'}, on={'actor': 'mec', 'hand': 'R'}, keys=[k('K2', visible=True)])],
  'cams': [POV(0, [0.9, 1.7, -2.86], [0.9, 1.74, -1.55], 58),
           cam('K2', 'mec', 'ms', angle=20),
           cam('K2:Clavicule', 'mec', 'cu', angle=10)],
  'tail': 0.1,
})
scenes.append({
  'id': 'tiktok', 'set': 'gym', 'grade': TIKTOK, 'ambience': None,
  'lines': [L('K3', "T'es moche ? Normal. Achète ma formation.", 'clavicule')],
  'actors': [act('clavicule', [0, 0, -1.6], 0, 'flex', 'smug', keys=[k('K3:Achète', clip='point', expr='smug')])],
  'props': [P('neon', 'fitPoster', scale=1.6, pos=[0, 1.75, -3.55], opts={'text': 'CLAVICULE\nLARGE'}), P('ring', 'ringLight', pos=[1.1, 0, -0.5], ry=-30)],
  'sfx': [{'at': 0.05, 'name': 'whoosh', 'vol': 0.4}],
  'cams': [cam(0, 'clavicule', 'ms', angle=0), cam('K3:Achète', 'clavicule', 'cu', angle=0, move='push', amount=0.06)],
  'tail': 0.1,
})
scenes.append({
  'id': 'panneau', 'set': 'chambre', 'ambience': None,
  'lines': [L('K4', "Ce con est tombé dans le panneau. Il était vraiment trop moche.", highlight=['panneau.'])],
  'actors': [act('mec', [-2.15, 0.27, -1.6], 90, 'sitLookItem', 'happy', keys=[k('K4:vraiment', clip='sit', expr='unimpressed')])],
  'props': [P('tel', 'phone911', opts={'screen': 'tiktok'}, on={'actor': 'mec', 'hand': 'R'}, keys=[k('K4:vraiment', visible=False)])],
  'sfx': [{'at': 'K4:panneau', 'name': 'kaching', 'vol': 0.6}],
  'cams': [cam(0, 'mec', 'ms', angle=-25), cam('K4:vraiment', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 2. the 72 products, each one a failure
SINK = [3.2, 0, -2.3]                        # in front of the bathroom mirror, facing it
MIRROR_POV = lambda at, y=1.76: POV(at, [3.2, 1.72, -3.3], [3.2, y, -2.3], 60)
SIDE_POV = lambda at: POV(at, [5.25, 1.45, -2.45], [3.2, 1.35, -2.3], 46)
KIT = [2.15, 0.86, -3.0]
scenes.append({
  'id': 'kit', 'set': 'bathroom', 'ambience': None,
  'lines': [L('K5', "La méthode : soixante-douze produits à s'injecter.", highlight=['soixante-douze']),
            L('K6', "Des stéroïdes : il a gonflé partout, sauf les muscles.", highlight=['stéroïdes', 'muscles.']),
            L('K7', "Un peptide pour bronzer : il est devenu orange.", highlight=['bronzer', 'orange.']),
            L('K8', "Un pour la peau lisse. Un pour maigrir.", highlight=['lisse.', 'maigrir.']),
            L('K9', "Et un pour bander, parce que les autres l'en empêchaient.", highlight=['bander,']),
            L('K10', "À chaque essai, raté. Il était encore plus moche.", highlight=['raté.', 'moche.'])],
  'actors': [
    act('mec', SINK, 180, 'stand', 'neutral', keys=[k('K6', clip='injectArm', expr='neutral'), k('K6:gonflé', visible=False)]),
    act('mecG', SINK, 180, 'stand', 'shocked', visible=False, keys=[k('K6:gonflé', visible=True), k('K7', clip='injectArm', expr='neutral'), k('K7:orange', visible=False)]),
    act('mecO', SINK, 180, 'stand', 'shocked', visible=False, keys=[
        k('K7:orange', visible=True), k('K8', clip='injectButt', expr='neutral'), k('K8:maigrir', clip='injectArm'),
        k('K9', clip='injectButt', expr='suspicious'), k('K9:empêchaient', clip='lookDown', expr='sad'), k('K10', clip='stand', expr='sad')]),
  ],
  'props': [P('table', 'table', pos=[2.15, 0, -3.0], opts={'w': 0.8, 'd': 0.55, 'h': 0.86, 'color': '#E6E2D8'}),
            P('kit', 'kit72', pos=KIT),
            P('syr1', 'syringeBig', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('K6', visible=True)]),
            P('syr2', 'syringeBig', visible=False, on={'actor': 'mecG', 'hand': 'R'}, keys=[k('K7', visible=True)]),
            P('syr3', 'syringeBig', visible=False, on={'actor': 'mecO', 'hand': 'R'}, keys=[k('K8', visible=True), k('K10', visible=False)])],
  'sfx': [{'at': 'K6:gonflé', 'name': 'poof', 'vol': 0.6}, {'at': 'K7:orange', 'name': 'poof', 'vol': 0.6}, {'at': 'K8', 'name': 'needle', 'vol': 0.5},
          {'at': 'K8:maigrir', 'name': 'needle', 'vol': 0.5}, {'at': 'K9', 'name': 'needle', 'vol': 0.5}, {'at': 'K10:raté', 'name': 'sting', 'vol': 0.3}],
  'cams': [cam(0, [[KIT[0], KIT[1] + 0.15, KIT[2]]], 'cu', worldAngle=10, elev=35, noOcclusion=True, move='push', amount=0.08),
           SIDE_POV('K6'),
           POV('K6:gonflé', [5.5, 1.35, -1.15], [3.2, 1.05, -2.3], 58),
           MIRROR_POV('K6:muscles'),
           SIDE_POV('K7'),
           MIRROR_POV('K7:orange'),
           SIDE_POV('K8'),
           SIDE_POV('K9'),
           SIDE_POV('K9:empêchaient'),
           MIRROR_POV('K10')],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 3. hard drugs at night
scenes.append({
  'id': 'drogues', 'set': 'chambre', 'lighting': 'night', 'ambience': 'night', 'ambienceVol': 0.6,
  'lines': [L('K11', "Pour le charisme, le programme prévoyait des drogues dures.", highlight=['charisme,', 'dures.']),
            L('K12', "Du carfentanil, pour ne plus stresser en parlant à une femme.", highlight=['carfentanil,']),
            L('K13', "Et du crystal meth : plus de faim, plein d'énergie, et une confiance en béton.", highlight=['crystal', 'béton.'])],
  'actors': [act('mecO', [2.5, 0, -1.6], 0, 'stand', 'neutral', keys=[
      k('K11:drogues', clip='injectArm', expr='neutral'),
      k('K12:femme', clip='idle', expr='sleepy', speed=0.4),
      k('K13', clip='injectArm', expr='suspicious'),
      k('K13:faim', clip='wired', expr='shocked'),
      k('K13:béton', clip='heroPose', expr='smug')])],
  'props': [P('syr', 'syringeBig', visible=False, on={'actor': 'mecO', 'hand': 'R'}, keys=[k('K11:drogues', visible=True), k('K12:femme', visible=False), k('K13', visible=True), k('K13:faim', visible=False)])],
  'sfx': [{'at': 'K11:drogues', 'name': 'needle', 'vol': 0.5}, {'at': 'K13', 'name': 'needle', 'vol': 0.5}, {'at': 'K13:faim', 'name': 'ticks', 'vol': 0.6},
          {'at': 'K13:faim+0.6', 'name': 'heartbeat', 'vol': 0.7}],
  'cams': [cam(0, 'mecO', 'ms', angle=20),
           cam('K12', 'mecO', 'cu', angle=0),
           cam('K13', 'mecO', 'ms', angle=-20),
           cam('K13:faim', 'mecO', 'cu', angle=0, move='push', amount=0.1)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 4. four surgeries
BED = [-2.5, 0.64, -2.3]
scenes.append({
  'id': 'chirurgie', 'set': 'hospital', 'ambience': 'office', 'ambienceVol': 0.6,
  'lines': [L('K14', "Ensuite, quatre chirurgies.", highlight=['quatre']),
            L('K15', "Une mâchoire carrée. Des yeux plus attirants.", highlight=['carrée.', 'attirants.']),
            L('K16', "Des clavicules plus larges, évidemment.", highlight=['clavicules']),
            L('K17', "Et l'agrandissement du sexe.", highlight=["l'agrandissement"]),
            L('K18', "Je vais avoir besoin d'une loupe.", 'chirurgien')],
  'actors': [
    act('mecO', BED, 0, 'lieBack', 'sleepy', keys=[k('K16:larges', visible=False)]),
    act('mecM', BED, 0, 'lieBack', 'sleepy', visible=False, keys=[k('K16:larges', visible=True)]),
    act('chirurgien', [-1.35, 0, -2.0], -80, 'clipboard', 'neutral', keys=[k('K15', clip='lookItem'), k('K17:sexe', clip='lookDown', expr='suspicious'), k('K18', clip='lookItem', expr='unimpressed')]),
  ],
  'props': [P('jaw_mecO', 'squareJaw', visible=False, opts={'color': SKIN_O}, on=face_on('mecO', 0.02, 0.05), keys=[k('K15:carrée', visible=True, sfx='pop')]),
            P('eyes_mecO', 'googlyEyes', visible=False, opts={'r': 0.042, 'sep': 0.05}, on=face_on('mecO', 0.5 * 0.86 * 0.6, 0.085 * 0.86 + 0.012), keys=[k('K15:yeux', visible=True, sfx='pop')]),
            *monster_face('mecM', 0.8, lumps=False),
            P('loupe', 'magnifyingGlass', visible=False, on={'actor': 'chirurgien', 'hand': 'R'}, keys=[k('K18', visible=True)])],
  'sfx': [{'at': 'K16:larges', 'name': 'poof', 'vol': 0.6}, {'at': 'K14', 'name': 'beep', 'vol': 0.3}, {'at': 'K14+0.9', 'name': 'beep', 'vol': 0.3}],
  'cams': [cam(0, ['mecO', 'chirurgien'], 'fs', worldAngle=30, elev=12),
           POV('K15', [-2.45, 2.05, -2.45], [-2.5, 0.78, -3.0], 42),
           cam('K16', ['mecM', 'chirurgien'], 'ms', worldAngle=35, elev=15),
           cam('K17', 'chirurgien', 'ms', angle=10),
           cam('K18', 'chirurgien', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 5. the gym, and the chainsaw (off screen)
scenes.append({
  'id': 'salle', 'set': 'gym', 'ambience': 'gym', 'ambienceVol': 0.6,
  'lines': [L('K19', "Il fallait aussi du sport. Les stéroïdes, ça ne marche pas si on ne branle rien.", highlight=['sport.', 'branle']),
            L('K20', "Pour un visage plus masculin : des micro-fractures. À la tronçonneuse.", 'clavicule', highlight=['tronçonneuse.']),
            L('K21', "Ce con l'a fait.", highlight=['fait.'])],
  'actors': [
    act('mecM', [-0.7, 0, -1.4], 25, 'curls', 'angry', params={'freq': 1.6}, keys=[k('K20', clip='stand', expr='neutral', face='clavicule', turn=0.2), k('K21', clip='lookItem', expr='happy', face=0, turn=0.2)]),
    act('clavicule', [0.9, 0, -1.2], -70, 'armsCrossed', 'smug', keys=[k('K20', clip='talk', expr='smug'), k('K20:tronçonneuse', clip='giveItem'), k('K21', clip='armsCrossed', expr='smug')]),
  ],
  'props': [*monster_face('mecM', 0.8, lumps=False),
            P('db', 'dumbbell', on={'actor': 'mecM', 'hand': 'R'}, keys=[k('K20', visible=False)]),
            P('db2', 'dumbbell', on={'actor': 'mecM', 'hand': 'L'}, keys=[k('K20', visible=False)]),
            P('scie', 'chainsaw', visible=False, opts={'runAt': 'K21', 'stopAt': 'K21.end+0.4'}, on={'actor': 'clavicule', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.1, 0.05]},
              keys=[k('K20:tronçonneuse', visible=True), k('K21-0.1', attach='mecM', hand='R', rot=[1.5708, 0, 0], offset=[0, -0.1, 0.05])]),
            P('neon', 'fitPoster', scale=1.6, pos=[0, 1.75, -3.55], opts={'text': 'CLAVICULE\nLARGE'})],
  'sfx': [{'at': 'K21', 'name': 'chainsaw', 'vol': 0.8}],
  'fx': [{'type': 'fadeBlack', 'at': 'K21.end-0.05', 'dur': 0.3}],
  'cams': [cam(0, 'mecM', 'ms', angle=15),
           cam('K19:branle', 'mecM', 'cu', angle=0),
           cam('K20', 'clavicule', 'ms', angle=10),
           cam('K20:tronçonneuse', ['clavicule', 'mecM'], 'ms', worldAngle=10),
           cam('K21', 'mecM', 'ms', angle=0)],
  'tail': 0.35,
})

# ------------------------------------------------------------------ 6. disfigured, he finds himself handsome (his view, then the date)
scenes.append({
  'id': 'miroir', 'set': 'bathroom', 'ambience': None,
  'lines': [L('K22', "Il était défiguré. Mais pour la première fois, il se trouvait beau.", highlight=['défiguré.', 'beau.'])],
  'actors': [
    act('mecM', SINK, 180, 'stand', 'happy', keys=[k('K22:première', visible=False)]),
    act('mecBeau', SINK, 180, 'heroPose', 'smug', visible=False, keys=[k('K22:première', visible=True)]),
  ],
  'props': monster_face('mecM', 0.8),
  'sfx': [{'at': 'K22:première', 'name': 'choir', 'vol': 0.7}],
  'fx': [{'type': 'fadeIn', 'at': 0, 'dur': 0.35}],
  'cams': [MIRROR_POV(0),
           {**MIRROR_POV('K22:première', 1.86), 'grade': DREAM}],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 7. the date, 56 hours awake
SEAT_L, SEAT_R = [-0.62, 0.12, -2.6], [0.62, 0.12, -2.6]
scenes.append({
  'id': 'rdv', 'set': 'restaurant', 'setOpts': {'brand': 'POULET ROYAL'}, 'ambience': 'bar', 'ambienceVol': 0.6,
  'lines': [L('K23', "Il avait un rendez-vous. Il n'avait pas dormi depuis cinquante-six heures.", highlight=['rendez-vous.', 'cinquante-six']),
            L('K24', "Salut. Je suis très détendu.", 'mecM'),
            L('K25', "Elle est partie.", highlight=['partie.']),
            L('K26', "Une seule explication : il n'était pas allé assez loin.", highlight=['assez', 'loin.'])],
  'actors': [
    act('mecM', SEAT_L, 90, 'sit', 'shocked', keys=[k('K23:dormi', clip='sitTalk', expr='shocked', params={'freq': 3.0}), k('K24', clip='sitTalk', expr='happy'), k('K25', clip='sit', expr='shocked'), k('K26', expr='suspicious')]),
    act('femme', SEAT_R, -90, 'sit', 'happy', keys=[k('K23:heures', expr='shocked'), k('K24.end', expr='scared'),
        k('K25-0.25', to=[1.3, 0, -2.0], glide=True, dur=0.15, clip='stand', then='stand', face='keep'), k('K25', to=[6.5, 0, 0.8], clip='run', speed=4.5, then='idle')]),
  ],
  'props': monster_face('mecM', 0.8),
  'sfx': [{'at': 'K23:dormi', 'name': 'heartbeat', 'vol': 0.7}, {'at': 'K25', 'name': 'whoosh', 'vol': 0.5}, {'at': 'K25.end+0.1', 'name': 'crickets', 'vol': 0.5}],
  'cams': [cam(0, ['mecM', 'femme'], 'ms', worldAngle=0),
           cam('K23:dormi', 'mecM', 'cu', angle=0),
           cam('K24', 'mecM', 'cu', angle=-15),
           cam('K24.end', 'femme', 'cu', angle=0),
           cam('K25', 'mecM', 'ms', angle=-30),
           cam('K26', 'mecM', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 8. the $7000 conference, Glucksmann like a lost child
AUD = [[-2.4, 0.12, 2.1], [-1.2, 0.12, 2.1], [1.2, 0.12, 2.1], [2.4, 0.12, 2.1]]
scenes.append({
  'id': 'conference', 'set': 'pressRoom', 'setOpts': {'backdrop': 'CLAVICULE LARGE|LOOKSMAXING|72 PRODUITS', 'bg': '#1E1E22', 'fg': '#F2C230', 'flags': False, 'fontScale': 0.55}, 'ambience': 'station',
  'crowd': [{'id': 'aud', 'count': 3, 'spec': {'preset': 'looksmaxeur', 'seed': 80}, 'clip': 'sit', 'ry': 180, 'positions': [[-2.4, 0.12, 3.2], [0.0, 0.12, 3.2], [2.4, 0.12, 3.2]]}],
  'lines': [L('K27', "Il a payé sept mille dollars pour la conférence de Clavicule Large.", highlight=['sept', 'mille']),
            L('K28', "Vous êtes encore moches ? Allez plus loin.", 'clavicule'),
            L('K29', "Dans la salle, il y avait Raphaël Glucksmann. Il avait l'air d'un enfant perdu.", highlight=['Glucksmann.', 'perdu.']),
            L('K30', "Il pensait que si personne ne votait pour lui, c'est qu'il ne prenait pas assez de produits.", highlight=['personne', 'produits.'])],
  'actors': [
    act('mecM', AUD[1], 180, 'sitHoldUp', 'happy', keys=[k('K28', clip='sit', expr='happy')]),
    act('glucksPeur', [0.0, 0.12, 2.1], 180, 'sit', 'scared', keys=[k('K30:produits', clip='sitWrite', expr='suspicious')]),
    act('lm1', AUD[0], 180, 'sit', 'neutral'), act('lm2', AUD[2], 180, 'sit', 'neutral'),
    act('clavicule', PR_SPEAKER, 0, 'podiumTalk', 'smug'),
  ],
  'props': [P('pass', 'notebook', scale=1.8, opts={'text': 'PASS VIP\n—\n7 000 $', 'bg': '#1E1E22'}, on={'actor': 'mecM', 'hand': 'R', **HAND_FLAT}, keys=[k('K28', visible=False)]),
            *monster_face('mecM', 0.8),
            P('jaw_lm1', 'squareJaw', opts={'color': '#E8935A'}, on=face_on('lm1', 0.02, 0.05)), P('jaw_lm2', 'squareJaw', opts={'color': '#E8935A'}, on=face_on('lm2', 0.02, 0.05))],
  'sfx': [{'at': 'K27:dollars', 'name': 'kaching', 'vol': 0.6}],
  'cams': [cam(0, 'pass', 'cu', worldAngle=180, allowBack=True, noOcclusion=True, zoom=1.4),
           POV('K27:conférence', [0, 2.4, 5.8], [0, 1.4, -2.0], 34),
           cam('K28', 'clavicule', 'mcu', angle=0),
           cam('K29', 'glucksPeur', 'ms', angle=0),
           cam('K30', 'glucksPeur', 'mcu', angle=20)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 9. Glucksmann's morning programme -> the perfect man
SINK_G = [3.2, 0, -2.3]
scenes.append({
  'id': 'glucksmatin', 'set': 'bathroom', 'ambience': None,
  'lines': [L('K31', "Alors, chaque matin, il s'est injecté le programme complet.", highlight=['programme']),
            L('K32', "Un cocktail qui aurait tué un cheval. Sur Glucksmann, ça a marché.", highlight=['cheval.', 'marché.']),
            L('K33', "Et il dormait quand même, comme un bébé. Sa nature molle le protégeait.", highlight=['bébé.', 'molle']),
            L('K34', "Il est devenu l'homme parfait.", highlight=['parfait.'])],
  'actors': [
    act('glucksPeur', SINK_G, 180, 'stand', 'scared', keys=[
        k('K31:injecté', clip='injectArm', expr='scared'), k('K32', clip='injectButt', expr='scared'), k('K32:marché', clip='stand', expr='happy'),
        k('K33', clip='nod', expr='sleepy', params={'freq': 0.6}), k('K34', visible=False)]),
    act('glucksBeau', SINK_G, 0, 'heroPose', 'smug', visible=False, keys=[k('K34', visible=True)]),
  ],
  'props': [P('table', 'table', pos=[2.15, 0, -3.0], opts={'w': 0.8, 'd': 0.55, 'h': 0.86, 'color': '#E6E2D8'}), P('kit', 'kit72', pos=KIT),
            P('syr', 'syringeBig', visible=False, on={'actor': 'glucksPeur', 'hand': 'R'}, keys=[k('K31:injecté', visible=True), k('K33', visible=False)])],
  'sfx': [{'at': 'K31:injecté', 'name': 'needle', 'vol': 0.5}, {'at': 'K32', 'name': 'needle', 'vol': 0.5}, {'at': 'K32:marché', 'name': 'bell', 'vol': 0.5}, {'at': 'K34', 'name': 'choir', 'vol': 0.75}],
  'cams': [SIDE_POV(0),
           MIRROR_POV('K31:injecté', 1.3),
           SIDE_POV('K32'),
           MIRROR_POV('K32:marché', 1.3),
           MIRROR_POV('K33', 1.37),
           {**cam('K34', 'glucksBeau', 'fs', angle=0, move='push', amount=0.08), 'grade': DREAM}],
  'tail': 0.25,
})

# ------------------------------------------------------------------ 10. the 48-hour TV interview, compared to God, president, dictator
scenes.append({
  'id': 'jt', 'set': 'pressRoom', 'setOpts': {'backdrop': 'LE 20H|INFO|DIRECT', 'bg': '#1E2E44', 'fg': '#F6F1E3', 'podium': False, 'flags': False}, 'ambience': 'station',
  'daynight': {'from': 'K35:Elle', 'period': 0.5},
  'lines': [L('K35', "Son interview au journal de vingt heures devait durer deux minutes. Elle a duré quarante-huit heures.", highlight=['deux', 'quarante-huit']),
            L('K36', "Vous allez devenir président.", 'journaliste')],
  'actors': [act('glucksBeau', [-0.65, 0.12, -1.7], 55, 'sitTalk', 'smug'),
             act('journaliste', [0.65, 0.12, -1.7], -55, 'sit', 'neutral', keys=[k('K35:Elle', expr='happy'), k('K36', clip='sitTalk', expr='happy')])],
  'props': [P('c1', 'chair', pos=[-0.77, 0, -1.78], ry=55, opts={'color': '#B5302A'}), P('c2', 'chair', pos=[0.77, 0, -1.78], ry=-55, opts={'color': '#B5302A'}),
            P('horloge', 'wallClock', scale=1.4, pos=[0, 2.95, -2.97], opts={'rate': 0}, alt={'opts': {'rate': 4}, 'at': 'K35:Elle'})],
  'sfx': [{'at': 'K35:Elle', 'name': 'ticks', 'vol': 0.6}, {'at': 'K35:Elle+1.4', 'name': 'ticks', 'vol': 0.6}],
  'cams': [cam(0, ['glucksBeau', 'journaliste'], 'ms', worldAngle=0),
           cam('K35:Elle', [[0, 2.95, -2.95], [-0.65, 1.2, -1.7], [0.65, 1.2, -1.7]], 'fs', worldAngle=0, noOcclusion=True),
           cam('K36', 'journaliste', 'cu', angle=0)],
  'tail': 0.15,
})
scenes.append({
  'id': 'meeting', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.4,
  'crowd': [{'id': 'fid', 'count': 6, 'spec': {'preset': 'lemec_charcoal', 'seed': 90}, 'clip': 'kneelBow', 'ry': 180,
             'positions': [[-1.8, 0, 1.4], [-0.6, 0, 1.6], [0.6, 0, 1.5], [1.8, 0, 1.4], [-1.2, 0, 2.5], [1.2, 0, 2.6]]}],
  'lines': [L('K37', "À ses meetings, certains le comparaient à Dieu.", highlight=['Dieu.'])],
  'actors': [act('glucksBeau', [0, 0, -0.6], 0, 'armsUp', 'smug')],
  'props': [P('estrade', 'podium', pos=[0, 0, 0.0]), P('aureole', 'halo', on={'actor': 'glucksBeau', 'joint': 'head', 'offset': [0, 0.55, 0]}, visible=False, keys=[k('K37:comparaient', visible=True, sfx='choir')])],
  'cams': [cam(0, ['glucksBeau', 'fid0', 'fid3'], 'fs', worldAngle=0, elev=12),
           {**POV('K37:comparaient', [0.0, 1.25, 1.7], [0, 2.0, -0.6], 36), 'grade': DREAM}],
  'tail': 0.2,
})
scenes.append({
  'id': 'elysee', 'set': 'office', 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('K38', "Glucksmann est devenu président. Puis dictateur.", highlight=['président.', 'dictateur.'])],
  'actors': [act('glucksBeau', [0, 0, -1.9], 0, 'stand', 'smug', keys=[k('K38:dictateur', clip='armsUp', expr='smug')])],
  'props': [P('bureau', 'desk', pos=[0, 0, -1.25]),
            P('drap1', 'flag', pos=[-1.2, 0, -3.1], opts={'colors': ['#2C4A8A', '#F6F1E3', '#B5302A']}), P('drap2', 'flag', pos=[1.2, 0, -3.1], opts={'colors': ['#2C4A8A', '#F6F1E3', '#B5302A']}),
            P('portrait', 'memePoster', scale=2.2, pos=[0, 1.95, -3.52], visible=False, opts={'text': 'GLUCKSMANN', 'skin': '#E0B48A'}, keys=[k('K38:dictateur', visible=True)])],
  'sfx': [{'at': 'K38:dictateur', 'name': 'fanfare', 'vol': 0.7}],
  'cams': [cam(0, 'glucksBeau', 'ms', angle=0), cam('K38:dictateur', 'glucksBeau', 'fs', angle=0, elev=-6)],
  'tail': 0.15,
})
scenes.append({
  'id': 'utopie', 'set': 'street', 'grade': DREAM, 'ambience': 'park', 'ambienceVol': 0.5,
  'crowd': [{'id': 'cit', 'count': 5, 'spec': {'preset': 'lemec_beige', 'seed': 95}, 'clip': 'dance', 'ry': 0,
             'positions': [[-2.2, 0, 0.4], [-0.9, 0, 0.9], [0.5, 0, 0.5], [1.8, 0, 0.9], [3.0, 0, 0.3]]}],
  'lines': [L('K39', "Une utopie. Les trains à l'heure, plus une seule grève. Même les Français ne râlaient plus.", highlight=['utopie.', 'râlaient'])],
  'actors': [],
  'props': [P('aff1', 'memePoster', scale=2.0, pos=[-1.5, 1.6, -1.3], opts={'text': 'MERCI GLUCKSMANN', 'skin': '#E0B48A'}),
            P('quai', 'signBoard', pos=[1.6, 0, -1.3], opts={'text': 'TRAINS : À L’HEURE', 'bg': '#1E2E44', 'fg': '#F2C230', 'w': 1.6, 'h': 0.45, 'height': 1.9}),
            P('greve', 'protestSign', scale=0.9, pos=[3.4, 0, -0.8], opts={'text': 'GRÈVE ANNULÉE', 'color': '#3E8A5A'})],
  'sfx': [{'at': 'K39:Français', 'name': 'bell', 'vol': 0.4}],
  'cams': [cam(0, ['cit1', 'cit2', 'cit3'], 'fs', worldAngle=0, elev=8),
           cam('K39:trains', [[1.6, 1.9, -1.3]], 'ms', worldAngle=0, noOcclusion=True),
           cam('K39:Français', 'cit2', 'ms', angle=0)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 11. the jealous rebels, the fall
scenes.append({
  'id': 'rebelles', 'set': 'streetNight', 'ambience': 'night', 'ambienceVol': 0.6,
  'lines': [L('K40', "Mais ce mec connaissait son secret.", highlight=['secret.']),
            L('K41', "Lui n'avait jamais réussi à s'aimer. Jaloux, il a monté un groupe rebelle.", highlight=['Jaloux,', 'rebelle.']),
            L('K42', "Confisquez les produits.", 'mecM')],
  'actors': [act('mecM', [0.3, 0, 0.6], 190, 'stand', 'angry', keys=[k('K41', face=0, turn=0.3, clip='stand', expr='sad'), k('K41:Jaloux', clip='armsCrossed', expr='angry'), k('K42', clip='point', expr='angry')]),
             *[act(f'r{i}', [x, 0, z], 0, 'chant', 'angry', visible=False, keys=[k('K41:Jaloux', visible=True)]) for i, (x, z) in enumerate([[-0.9, -0.2], [0.3, -0.5], [1.5, -0.2]])]],
  'props': [*monster_face('mecM', 0.8), P('panneau', 'signBoard', pos=[0.4, 0, -1.4], opts={'text': 'GLUCKSMANN\nPRÉSIDENT À VIE', 'bg': '#B5302A', 'fg': '#F6F1E3', 'w': 1.8, 'h': 0.9, 'height': 2.3})],
  'cams': [cam(0, ['mecM', [0.4, 2.0, -1.4]], 'ms', worldAngle=20),
           cam('K41', 'mecM', 'cu', angle=0),
           cam('K41:Jaloux', ['mecM', 'r0', 'r2'], 'fs', worldAngle=0, elev=6),
           cam('K42', 'mecM', 'cu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'chute', 'set': 'office', 'lighting': 'dusk', 'ambience': 'office', 'ambienceVol': 0.4,
  'lines': [L('K43', "Sans ses produits, Glucksmann est redevenu tout mou.", highlight=['mou.']),
            L('K44', "Il pleurait comme un bébé. Ses adorateurs l'ont renié.", highlight=['bébé.', 'renié.'])],
  'actors': [
    act('glucksBeau', [0, 0, -1.9], 0, 'stand', 'shocked', keys=[k('K43:redevenu', visible=False)]),
    act('glucksMou', [0, 0, -1.9], 0, 'stand', 'sad', visible=False, keys=[k('K43:redevenu', visible=True), k('K44', clip='cry', expr='sad')]),
    act('rebelle', [-1.9, 0, -0.2], 60, 'stand', 'angry', keys=[k('K43', to=[-0.5, 0, -0.55], clip='walk', speed=2.2, then='takeItem'), k('K43:mou', to=[-2.6, 0, 0.6], clip='run', speed=3.5, then='idle')]),
    act('fan1', [1.6, 0, -0.4], -100, 'kneelBow', 'happy', keys=[k('K44:adorateurs', clip='armsCrossed', expr='unimpressed', face=80, turn=0.4)]),
    act('fan2', [2.4, 0, 0.1], -110, 'kneelBow', 'happy', keys=[k('K44:adorateurs+0.15', clip='armsCrossed', expr='unimpressed', face=70, turn=0.4)]),
  ],
  'props': [P('bureau', 'desk', pos=[0, 0, -1.25]),
            P('kit', 'kit72', pos=[-0.45, 0.76, -1.25], keys=[k('K43:produits', attach='rebelle', hand='R', offset=[0, -0.12, 0.1], rot=[1.5708, 0, 0])])],
  'sfx': [{'at': 'K43:redevenu', 'name': 'poof', 'vol': 0.6}],
  'cams': [cam(0, ['glucksBeau', 'rebelle'], 'ms', worldAngle=0),
           cam('K43:redevenu', 'glucksMou', 'ms', angle=0),
           cam('K44', 'glucksMou', 'cu', angle=0),
           cam('K44:adorateurs', ['fan1', 'fan2', 'glucksMou'], 'fs', worldAngle=-10)],
  'tail': 0.2,
})

# ------------------------------------------------------------------ 12. two hundred views
POSTV = (2.85, 0.775, -2.65)
scenes.append({
  'id': 'fin', 'set': 'chambre', 'setOpts': {'wall': '#E6D8C4', 'band': '#C9B79C', 'poster': 'DANGER\nLOOKSMAXING', 'posterBg': '#F6F1E3', 'posterFg': '#B5302A', 'blanket': '#C9729A'}, 'ambience': None,
  'lines': [L('K45', "Aujourd'hui, il fait des vidéos sur les dangers du looksmaxing.", highlight=['dangers']),
            L('K46', "Deux cents vues.", pre=0.4, highlight=['Deux', 'cents'])],
  'actors': [act('glucksMou', [0.9, 0, -1.7], 0, 'talk', 'sad', keys=[k('K45:dangers', clip='cry', expr='sad'), k('K46', clip='stareCamera', expr='sad')])],
  'props': [P('ring', 'ringLight', pos=[1.75, 0, -1.05], ry=-125),
            tweet_on_table('vues', *POSTV, name='Raphaël G.', handle='@raph_officiel', initial='R', avatar='#2C4A8A', via='Vidéo',
                           text='Les dangers du looksmaxing (partie 47) · 200 vues', likes='2 likes')],
  'cams': [cam(0, 'glucksMou', 'ms', angle=0),
           tweet_cam('K46', *POSTV),
           cam('K46.end+0.3', 'glucksMou', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.5,
})

write('looksmaxing', 'Le looksmaxing', scenes, {
  'clavicule': {'preset': 'clavicule'},
  'mecG': {'preset': 'mecGonfle'},
  'mecO': {'preset': 'mecOrange'},
  'mecM': {'preset': 'mecMonstre'},
  'mecBeau': {'preset': 'mecBeau'},
  'chirurgien': {'preset': 'doctor', 'seed': 12},
  'femme': {'preset': 'femme', 'seed': 21},
  'glucksPeur': {'preset': 'glucksPeur'},
  'glucksBeau': {'preset': 'glucksBeau'},
  'glucksMou': {'preset': 'glucksMou'},
  'journaliste': {'preset': 'journaliste', 'seed': 31},
  'lm1': {'preset': 'looksmaxeur', 'seed': 41}, 'lm2': {'preset': 'looksmaxeur', 'seed': 42},
  'rebelle': {'preset': 'swat', 'seed': 51},
  'r0': {'preset': 'swat', 'seed': 52}, 'r1': {'preset': 'looksmaxeur', 'seed': 53}, 'r2': {'preset': 'swat', 'seed': 54},
  'fan1': {'preset': 'lemec_beige', 'seed': 61}, 'fan2': {'preset': 'lemec_brown', 'seed': 62},
})
