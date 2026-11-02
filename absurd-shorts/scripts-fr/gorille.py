#!/usr/bin/env python3
"""Storyboard for "Le gorille" -> scripts-fr/gorille.json  (python3 scripts-fr/gorille.py)

Narration = the user's text, verbatim, except:
  - the real politician's name -> fictional "Karim Bouamrane" (Gus-Fring-style boss)  [no false criminal claims about real people]
  - the real chain name        -> fictional "Master Poulet"
  - captions fix two typos ("dutout" -> "du tout", "toît" -> "toits").
Editing grammar (measured on the originals): one continuous take per location (cut: false inside a location).
"""
import json, os

M = 'mec'          # Le Mec (painted atlas + measured face)
MN = 'mecNu'       # same man, naked (censor bar)
MG = 'mecGorille'  # Le Mec turned gorilla (red tie)
shots = []

def S(line, actors=None, cam=None, cut=False, **kw):
    d = {'line': line, 'actors': actors or [], 'camera': cam or {'preset': 'medium'}}
    if not cut: d['cut'] = False
    d.update(kw); shots.append(d); return d

def A(id, pos=None, clip='idle', expr=None, **kw):
    d = {'id': id, 'clip': clip}
    if pos is not None: d['pos'] = pos
    if expr: d['expr'] = expr
    d.update(kw); return d

def G(i, pos, clip='idle', expr=None, **kw): return A(f'g{i}', pos, clip, expr, **kw)

vac = None
GOR = [[-2.2, 0, -2.4], [0.0, 0, -3.2], [2.0, 0, -2.2]]      # three gorillas in the enclosure

# ---- 1. bedroom ---------------------------------------------------------------------------------
S("Ce con s'était mis à la musculation une semaine plus tôt après avoir regardé un TikTok de merde.",
  [A(M, [0, 0, 0.3], 'holdPhoneFront', 'neutral', hold={'name': 'phone911', 'hand': 'R'}, actions=[{'at': 2.4, 'clip': 'liftBarbell', 'expr': 'angry'}])],
  {'preset': 'medium', 'angle': 20, 'push': 0.2}, cut=True, set='livingRoom', highlight=['musculation', 'TikTok', 'merde'],
  props=[{'name': 'dumbbell', 'pos': [0.6, 0.02, 0.9]}, {'name': 'dumbbell', 'pos': [0.9, 0.02, 0.7], 'ry': 40}])

# ---- 2. zoo, day ----------------------------------------------------------------------------------
gors = [G(i, p, 'idle', 'neutral', ry=r, scale=1.25) for i, (p, r) in enumerate(zip(GOR, [20, 0, -20]))]
S("Puis il est allé au zoo et là, il a vu les gorilles.", [A(M, [0, 0, 6.4], 'walk', ry=180, to=[0.3, 0, 5.2], moveEnd=1.6)] + gors,
  {'preset': 'wide', 'target': [0, 1.2, 1.0], 'angle': 0, 'zoom': 0.9, 'push': 0.12}, cut=True, set='zoo', highlight=['zoo', 'gorilles'])
S("Ces putains de gorilles étaient énormes, des bras trois fois plus gros que les siens.",
  [G(i, p, 'flex', 'smug', ry=r, scale=1.25) for i, (p, r) in enumerate(zip(GOR, [20, 0, -20]))],
  {'preset': 'low', 'target': 'g1', 'angle': 0, 'zoom': 1.1, 'push': 0.1, 'glide': 0.8}, highlight=['putains', 'énormes', 'trois'])
S("Ce con est devenu terriblement jaloux.", [A(M, [0.3, 0, 5.2], 'angryFist', 'angry', ry=180)],
  {'preset': 'close', 'target': M, 'angle': 180, 'push': 0.1, 'glide': 0.7}, highlight=['jaloux'])
S("Il croyait qu'ils contractaient leurs muscles pour le provoquer alors que pas du tout.", [G(1, None, 'flex', 'smug', actions=[{'at': 2.6, 'clip': 'idle', 'expr': 'neutral'}])],
  {'preset': 'full', 'target': 'g1', 'angle': 10, 'zoom': 0.8, 'push': 0.08, 'glide': 0.8}, say="Il croyait qu'ils contractaient leurs muscles pour le provoquer alors que pas du tout.", highlight=['provoquer', 'du tout'])
S("Il a voulu comprendre leur secret.", [A(M, None, 'thinkChin', 'suspicious')], {'preset': 'extremeClose', 'target': M, 'angle': 170, 'push': 0.05, 'glide': 0.7}, highlight=['secret'])
S("Première hypothèse : leur bouffe.", [G(i, None, 'eat', 'happy') for i in range(3)], {'preset': 'wide', 'target': [0, 1.1, -2.6], 'angle': 0, 'zoom': 0.7, 'push': 0.1, 'glide': 0.8},
  highlight=['hypothèse', 'bouffe'], overlays=[{'style': 'banner', 'text': 'HYPOTHÈSE N°1', 'at': 0.1}],
  props=[{'name': 'foodSack', 'pos': [-1.2, 0, -2.0], 'opts': {'text': 'PURINA HIGH PROTEIN'}}])
S("Il les a regardés manger leurs sac de nourriture pour primates.", [], {'preset': 'full', 'target': [-1.3, 1.0, -2.2], 'angle': 15, 'zoom': 0.7, 'push': 0.1, 'glide': 0.8}, highlight=['nourriture', 'primates'])
S("Purina High Protein.", [], {'preset': 'close', 'target': [-1.2, 0.6, -2.0], 'angle': 0, 'zoom': 0.6, 'push': 0.15, 'glide': 0.6}, highlight=['Purina', 'High', 'Protein'])
S("Avec ça, de la viande de chèvre vivantes, des œufs, du lait et du yaourt.",
  [A('chevre', [0.8, 0, -1.4], 'idle', 'scared', ry=-30)],
  {'preset': 'wide', 'target': [0.2, 1.0, -1.8], 'angle': 5, 'zoom': 0.75, 'push': 0.1, 'glide': 0.8}, highlight=['chèvre', 'œufs', 'lait', 'yaourt'],
  props=[{'name': 'eggs', 'pos': [-0.3, 0, -1.2]}, {'name': 'milkBottle', 'pos': [0.1, 0, -1.0]}, {'name': 'mug', 'pos': [-0.6, 0, -1.0], 'opts': {'color': '#FFFFFF'}}])

# ---- 3. kitchen ------------------------------------------------------------------------------------
S("Alors, il a acheté la même chose et s'est mis à manger exactement comme eux.",
  [A(M, [0, 0, 0], 'sit', 'neutral', actions=[{'at': 1.5, 'clip': 'sitWrite', 'expr': 'disgusted'}]), A('chevre', [1.0, 0, 0.3], 'idle', 'scared', ry=-60)],
  {'preset': 'medium', 'target': M, 'angle': 18, 'push': 0.12, 'dy': -0.3, 'lookDy': -0.4}, cut=True, set='kitchenNight', lighting='interior', highlight=['même', 'exactement'],
  props=[{'name': 'table', 'pos': [0, 0, 0.6]}, {'name': 'foodSack', 'pos': [-0.55, 0.78, 0.55], 'scale': 0.5, 'opts': {'text': 'PURINA HIGH PROTEIN'}}, {'name': 'eggs', 'pos': [0.15, 0.78, 0.55]}, {'name': 'milkBottle', 'pos': [0.45, 0.78, 0.6]}])

# ---- 4. zoo again --------------------------------------------------------------------------------
gors2 = [G(i, p, 'flex', 'smug', ry=r, scale=1.6) for i, (p, r) in enumerate(zip(GOR, [20, 0, -20]))]
S("Il est revenu au zoo, toujours pas assez musclé.", [A(M, [0.3, 0, 5.2], 'flex', 'neutral', ry=180)] + gors2,
  {'preset': 'full', 'target': M, 'angle': 160, 'zoom': 0.9, 'push': 0.12}, cut=True, set='zoo', highlight=['toujours', 'musclé'])
S("Les gorilles étaient encore plus gros que lui.", [], {'preset': 'low', 'target': 'g1', 'angle': 0, 'zoom': 1.2, 'push': 0.1, 'glide': 0.8}, highlight=['encore', 'gros'])
S("Ça le rendait fou.", [A(M, None, 'yell', 'angry')], {'preset': 'extremeClose', 'target': M, 'angle': 175, 'push': 0.05, 'glide': 0.6}, highlight=['fou'],
  fx=[{'type': 'shake', 'at': 0.2, 'dur': 0.6, 'amount': 0.02}])
S("Deuxième hypothèse : les gorilles étaient à poil et faisaient des acrobaties toute la journée.",
  [G(0, None, 'jump', 'happy', params={'dur': 0.7, 'height': 0.8}), G(1, None, 'dance', 'happy'), G(2, None, 'celebrate', 'happy')],
  {'preset': 'wide', 'target': [0, 1.2, -2.6], 'angle': 0, 'zoom': 0.8, 'push': 0.1, 'glide': 0.8}, highlight=['hypothèse', 'poil', 'acrobaties'],
  overlays=[{'style': 'banner', 'text': 'HYPOTHÈSE N°2', 'at': 0.1}])

# ---- 5. the street, naked --------------------------------------------------------------------------
S("Il s'est donc mis à se balader complètement à poil, en pleine rue.", [A(MN, [-1.5, 0, 0.8], 'walk', 'neutral', ry=90, to=[1.0, 0, 0.8])],
  {'preset': 'full', 'target': MN, 'angle': 0, 'zoom': 0.9, 'push': 0.06}, cut=True, set='street', highlight=['poil', 'rue'])
S("Les gens le voyaient arriver et se barraient en courant.",
  [A(MN, [1.0, 0, 0.8], 'walk', 'neutral', ry=90, to=[2.0, 0, 0.8]), A('madame', [3.5, 0, 0.4], 'flee', 'scared', ry=90, to=[7, 0, 0.4]), A('mamie', [4.2, 0, 1.4], 'flee', 'scared', ry=90, to=[7.5, 0, 1.6]), A('gamin', [3.0, 0, 1.0], 'flee', 'scared', ry=90, to=[6.5, 0, 1.0])],
  {'preset': 'wide', 'target': [3.0, 1.2, 0.8], 'angle': 0, 'zoom': 0.65, 'push': 0.05, 'glide': 0.8}, highlight=['courant'], sfx=['whoosh'])
S("Il faisait du street workout partout, des tractions, des acrobaties",
  [A(MN, [2.0, 0, 0.8], 'jump', 'neutral', ry=0, params={'dur': 0.6, 'height': 0.7}, actions=[{'at': 0.8, 'clip': 'climbDown'}, {'at': 1.8, 'clip': 'jump', 'params': {'dur': 0.6, 'height': 0.7}}])],
  {'preset': 'full', 'target': MN, 'angle': 15, 'zoom': 0.95, 'push': 0.08, 'glide': 0.7}, highlight=['street', 'workout', 'tractions'],
  props=[{'name': 'streetLamp', 'pos': [2.6, 0, 0.3]}])
S("et il se balançait de lampadaire en lampadaire et sur les toits des maisons en marchant comme un gorille.",
  [A(MN, [-2, 3.25, -1.5], 'crawl', 'neutral', ry=90, to=[2, 3.25, -1.5])],
  {'preset': 'wide', 'target': [0, 3.6, -1.5], 'angle': 0, 'zoom': 0.75, 'push': 0.05}, cut=True, set='rooftopPowerLine',
  say="et il se balançait de lampadaire en lampadaire et sur les toits des maisons en marchant comme un gorille.", highlight=['lampadaire', 'toits', 'gorille'])

# ---- 6. zoo: he moves in ---------------------------------------------------------------------------
gors3 = [G(i, p, 'flex', 'smug', ry=r, scale=1.7) for i, (p, r) in enumerate(zip(GOR, [20, 0, -20]))]
S("Puis, retour au zoo, toujours moins musclé.", [A(MN, [0.3, 0, 5.2], 'flex', 'sad', ry=180)] + gors3,
  {'preset': 'full', 'target': MN, 'angle': 160, 'zoom': 0.9, 'push': 0.1}, cut=True, set='zoo', highlight=['moins', 'musclé'])
S("Il était tellement furieux que maintenant, même les visiteurs le craignaient.",
  [A(MN, None, 'yell', 'angry'), A('madame', [-1.4, 0, 6.2], 'scared', 'scared', ry=120), A('gamin', [1.6, 0, 6.4], 'scared', 'scared', ry=-130)],
  {'preset': 'full', 'target': [0.2, 1.3, 5.8], 'angle': 180, 'zoom': 1.0, 'push': 0.1, 'glide': 0.7}, highlight=['furieux', 'visiteurs'],
  fx=[{'type': 'shake', 'at': 0.3, 'dur': 0.5, 'amount': 0.02}])
S("Alors, il a sauté la barrière et s'est installé directement dans l'enclos des gorilles.",
  [A(MN, [0.3, 0, 5.2], 'jump', 'neutral', ry=0, params={'dur': 0.9, 'height': 1.4}, to=[0.3, 0, 2.6], moveEnd=0.9, actions=[{'at': 1.0, 'clip': 'walk'}, {'at': 2.2, 'clip': 'idle'}])],
  {'preset': 'wide', 'target': [0.3, 1.2, 3.0], 'angle': 25, 'zoom': 0.75, 'push': 0.08, 'glide': 0.7}, highlight=['barrière', 'enclos'])
S("Il mangeait et dormait avec eux pour trouver leur putain de secret.",
  [A(MN, [0.6, 0, -1.6], 'lieDown', 'sleepy')] + [G(i, p, 'sleep', 'sleepy', ry=r, scale=1.7) for i, (p, r) in enumerate(zip(GOR, [20, 0, -20]))],
  {'preset': 'high', 'target': [0.4, 0.6, -2.2], 'angle': 10, 'zoom': 1.3, 'push': 0.08, 'glide': 0.8}, highlight=['putain', 'secret'],
  props=[{'name': 'foodSack', 'pos': [-1.0, 0, -1.2], 'opts': {'text': 'PURINA HIGH PROTEIN'}}])
S("Et là, il a remarqué un truc.", [A(MN, [0.6, 0, -1.4], 'stareCamera', 'suspicious')], {'preset': 'close', 'target': MN, 'angle': 5, 'push': 0.08}, cut=True, set='zoo', highlight=['truc'])
S("Ils étaient beaucoup plus poilus que lui.", [G(1, [0.0, 0, -3.2], 'flex', 'smug', scale=1.7)], {'preset': 'close', 'target': 'g1', 'angle': 0, 'zoom': 0.8, 'push': 0.1, 'glide': 0.7}, highlight=['poilus'])
S("Pour lui, aucun doute, ces bâtards devaient être dopés.", [A(MN, None, 'thinkChin', 'suspicious')], {'preset': 'extremeClose', 'target': MN, 'angle': 5, 'push': 0.05, 'glide': 0.6}, highlight=['bâtards', 'dopés'])

# ---- 7. zoo at night: the stealth bit -----------------------------------------------------------
sleepers = [G(i, p, 'sleep', 'sleepy', ry=r, scale=1.7) for i, (p, r) in enumerate(zip(GOR, [20, 0, -20]))]
S("Il a attendu la nuit jusqu'à ce que tous les gorilles aient l'air de dormir.", [A(MN, [0.6, 0, -1.4], 'idle', 'suspicious')] + sleepers,
  {'preset': 'wide', 'target': [0.3, 1.0, -2.4], 'angle': 0, 'zoom': 0.75, 'push': 0.08}, cut=True, set='zoo', setOpts={'night': True}, highlight=['nuit', 'dormir'],
  props=[{'name': 'zzz', 'pos': [-2.2, 2.0, -2.4]}, {'name': 'zzz', 'pos': [2.0, 2.0, -2.2]}])
S("Sauf un.", [G(1, None, 'idle', 'suspicious')], {'preset': 'close', 'target': 'g1', 'angle': 0, 'zoom': 0.8, 'push': 0.12, 'glide': 0.5}, highlight=['un'], sfx=[{'name': 'ding', 'at': 0.1, 'vol': 0.3}])
S("Le plus gros s'est levé discrètement et s'est caché derrière un rocher.", [G(1, [0.0, 0, -3.2], 'sneak', 'suspicious', ry=60, to=[2.2, 0, -3.9], moveEnd=2.4)],
  {'preset': 'wide', 'target': [1.2, 1.2, -3.4], 'angle': 0, 'zoom': 0.75, 'push': 0.06, 'glide': 0.7}, highlight=['rocher'])
box = {'name': 'cardboardBox', 'opts': {'text': ''}}
S("Le mec s'est planqué sous un carton, comme Snake dans Metal Gear Solid, et l'a suivi à petits pas.", [],
  {'preset': 'full', 'target': [0.6, 0.9, -1.6], 'angle': 0, 'zoom': 0.8, 'push': 0.08, 'glide': 0.6}, highlight=['carton', 'Snake', 'Metal', 'Gear'],
  props=[dict(box, pos=[0.6, 0, -1.4], to=[1.4, 0, -2.2])], remove=[MN], replaceProps=True,
  overlays=[{'style': 'label', 'text': '!', 'at': 0.2, 'until': 0.9, 'y': 0.3, 'size': 0.12, 'color': '#E8775F'}], sfx=[{'name': 'pop', 'at': 0.2, 'vol': 0.5}])
S("Quand le gorille regardait derrière lui, il s'arrêtait net.", [G(1, [2.2, 0, -3.9], 'lookAround', 'suspicious', ry=60, ryTo=200)],
  {'preset': 'wide', 'target': [1.8, 1.0, -3.0], 'angle': 10, 'zoom': 0.75, 'push': 0.05, 'glide': 0.6}, highlight=['net'], props=[], replaceProps=True)
shots[-1]['props'] = [dict(box, pos=[1.4, 0, -2.2])]
S("Derrière le rocher, le gorille se piquait aux stéroïdes.", [G(1, [2.2, 0, -3.9], 'idle', 'smug', ry=180, hold={'name': 'syringe', 'hand': 'R'})],
  {'preset': 'medium', 'target': 'g1', 'angle': 160, 'zoom': 1.2, 'push': 0.1}, cut=True, set='zoo', setOpts={'night': True}, highlight=['stéroïdes'],
  props=[{'name': 'steroidVial', 'pos': [2.6, 0.0, -4.4]}])
S("Ensuite, il prenait un pré-workout interdit qui contenait un dérivé de méthamphétamine.", [G(1, None, 'idle', 'happy', hold={'name': 'preWorkout', 'hand': 'R', 'opts': {'text': 'INTERDIT'}})],
  {'preset': 'close', 'target': 'g1', 'angle': 165, 'zoom': 1.2, 'push': 0.1, 'glide': 0.6}, highlight=['pré-workout', 'interdit', 'méthamphétamine'])
S("Puis, il est entré dans une grotte.", [G(1, [2.6, 0, -4.6], 'walk', 'neutral', ry=150, to=[3.6, 0, -6.3])],
  {'preset': 'wide', 'target': [3.1, 1.3, -5.4], 'angle': 0, 'zoom': 0.8, 'push': 0.06, 'glide': 0.6}, highlight=['grotte'])
S("Le mec l'a suivi, toujours sous son carton.", [], {'preset': 'full', 'target': [3.2, 0.8, -5.5], 'angle': 0, 'zoom': 0.75, 'push': 0.08, 'glide': 0.5}, highlight=['carton'],
  props=[dict(box, pos=[2.4, 0, -4.4], to=[3.5, 0, -6.2])], replaceProps=True, remove=['g1'])

# ---- 8. secret gym ---------------------------------------------------------------------------------
S("À l'intérieur, une salle de musculation ultra-moderne cachée sous le zoo avec un coach privé.",
  [G(1, [0, 0, -0.6], 'liftBarbell', 'angry', scale=1.7, hold={'name': 'barbell', 'hand': 'R'}), A('coach', [1.6, 0, 0.2], 'point', 'angry', ry=-60)],
  {'preset': 'wide', 'target': [0.6, 1.4, -0.3], 'angle': 0, 'zoom': 0.7, 'push': 0.1}, cut=True, set='secretGym', highlight=['ultra-moderne', 'coach'])
S("Le gorille s'est entraîné douze heures d'affilée, toute la nuit, sans s'arrêter.", [G(1, None, 'liftBarbell', 'angry', params={})],
  {'preset': 'full', 'target': 'g1', 'angle': 15, 'zoom': 0.8, 'push': 0.1, 'glide': 0.7}, highlight=['douze', 'heures'],
  overlays=[{'style': 'banner', 'text': '12 HEURES', 'at': 0.3}])
S("Le coach lui faisait enchaîner les exercices.", [G(1, None, 'punch', 'angry'), A('coach', None, 'yell', 'angry')],
  {'preset': 'full', 'target': [0.8, 1.4, -0.2], 'angle': -20, 'zoom': 0.85, 'push': 0.08, 'glide': 0.6}, highlight=['coach', 'exercices'])
S("Le mec regardait tout depuis son carton.", [], {'preset': 'close', 'target': [-2.2, 0.6, 1.2], 'angle': 30, 'zoom': 0.6, 'push': 0.1, 'glide': 0.6}, highlight=['carton'],
  props=[dict(box, pos=[-2.2, 0, 1.2])], replaceProps=True)
S("Il avait enfin compris pourquoi ces cons étaient aussi musclés.", [A(MN, [-2.2, 0, 1.2], 'stareCamera', 'shocked')],
  {'preset': 'extremeClose', 'target': MN, 'angle': 20, 'push': 0.05, 'glide': 0.5}, highlight=['cons', 'musclés'], props=[], replaceProps=True)

# ---- 9. same programme -> transformation --------------------------------------------------------
S("Il a donc fait exactement pareil.", [A(MN, [0, 0, 0], 'liftBarbell', 'angry', hold={'name': 'barbell', 'hand': 'R'})],
  {'preset': 'full', 'target': MN, 'angle': 15, 'zoom': 0.9, 'push': 0.1}, cut=True, set='secretGym', highlight=['pareil'])
S("Les mêmes produits, les mêmes entraînements, le même putain de programme.", [A(MN, None, 'idle', 'angry', hold={'name': 'syringe', 'hand': 'R'}, actions=[{'at': 1.3, 'clip': 'punch'}, {'at': 2.6, 'clip': 'liftBarbell'}])],
  {'preset': 'medium', 'target': MN, 'angle': 25, 'push': 0.1, 'glide': 0.6}, highlight=['produits', 'entraînements', 'programme'],
  props=[{'name': 'preWorkout', 'pos': [0.7, 0, 0.5], 'opts': {'text': 'INTERDIT'}}, {'name': 'steroidVial', 'pos': [0.9, 0, 0.3]}])
S("Et à force, il s'est lui-même transformé en gorille.", [A(MN, [0, 0, 0], 'flex', 'shocked', scaleTo=1.15)],
  {'preset': 'full', 'target': [0, 1.8, 0], 'angle': 0, 'zoom': 0.9, 'push': 0.12, 'glide': 0.5}, highlight=['transformé', 'gorille'],
  fx=[{'type': 'flash', 'at': 1.3, 'dur': 0.4}, {'type': 'shake', 'at': 1.2, 'dur': 0.4, 'amount': 0.03}])
S("", [A(MG, [0, 0, 0], 'flex', 'surprised', scale=1.5)], {'preset': 'full', 'target': MG, 'angle': 0, 'zoom': 0.75, 'push': 0.1}, cut=True, set='secretGym', duration=1.1,
  fx=[{'type': 'flash', 'at': 0, 'dur': 0.3}], sfx=[{'name': 'boing', 'at': 0.05, 'vol': 0.5}])
S("Sauf qu'il ne voulait pas être un gorille parmi les autres.", [A(MG, [0, 0, -2.6], 'idle', 'neutral', scale=1.6)] + [G(i, p, 'idle', 'neutral', ry=r, scale=1.6) for i, (p, r) in enumerate(zip([[-2.0, 0, -2.4], [2.0, 0, -2.6]], [20, -20]))],
  {'preset': 'wide', 'target': [0, 1.2, -2.6], 'angle': 0, 'zoom': 0.7, 'push': 0.1}, cut=True, set='zoo', highlight=['gorille', 'parmi'])
S("Il voulait être le plus musclé de tous.", [A(MG, None, 'flex', 'smug')], {'preset': 'close', 'target': MG, 'angle': 0, 'zoom': 0.9, 'push': 0.1, 'glide': 0.6}, highlight=['plus', 'musclé'])
S("Alors, il a triplé la dose de chaque produit.", [A(MG, [0, 0, 0], 'idle', 'angry', scale=1.6, hold={'name': 'syringe', 'hand': 'R', 'scale': 2})],
  {'preset': 'medium', 'target': MG, 'angle': 20, 'zoom': 1.0, 'push': 0.12}, cut=True, set='secretGym', highlight=['triplé', 'dose'],
  overlays=[{'style': 'stamp', 'text': 'x3', 'at': 0.5, 'y': 0.25}],
  props=[{'name': 'preWorkout', 'pos': [x, 0, 0.7], 'opts': {'text': 'INTERDIT'}} for x in (-0.6, -0.3, 0.6)])
S("Puis, il s'est entraîné pendant une semaine entière sans aucune pause, jour et nuit.", [A(MG, None, 'liftBarbell', 'angry', hold={'name': 'barbell', 'hand': 'R'}, params={})],
  {'preset': 'full', 'target': MG, 'angle': 15, 'zoom': 0.8, 'push': 0.1, 'glide': 0.6}, highlight=['semaine', 'jour', 'nuit'], props=[], replaceProps=True,
  overlays=[{'style': 'banner', 'text': 'JOUR 1 → JOUR 7', 'at': 0.3}])
S("Tout passait en accéléré.", [A(MG, None, 'punch', 'angry', params={}), A('coach', [1.8, 0, 0.4], 'faint', 'dead', ry=-60, params={'dur': 0.8})],
  {'preset': 'full', 'target': [0.6, 1.6, 0.2], 'angle': 0, 'zoom': 0.9, 'push': 0.05, 'glide': 0.4}, highlight=['accéléré'],
  overlays=[{'style': 'label', 'text': '▶▶ x16', 'at': 0, 'y': 0.12, 'size': 0.06}])
S("Lui continuait.", [A(MG, None, 'liftBarbell', 'angry', hold={'name': 'barbell', 'hand': 'R'})], {'preset': 'close', 'target': MG, 'angle': 10, 'push': 0.08, 'glide': 0.4}, highlight=['continuait'])
S("Il est devenu énorme.", [A(MG, None, 'flex', 'smug', scale=1.6, scaleTo=2.4, scaleEnd=1.0)], {'preset': 'low', 'target': MG, 'angle': 0, 'zoom': 1.0, 'push': 0.0, 'glide': 0.5}, highlight=['énorme'],
  sfx=[{'name': 'boing', 'at': 0.2, 'vol': 0.4}], fx=[{'type': 'shake', 'at': 0.4, 'dur': 0.6, 'amount': 0.03}])

# ---- 10. zoo: alpha ------------------------------------------------------------------------------
pos3 = [[-2.0, 0, -2.4], [0.0, 0, -3.4], [2.0, 0, -2.6]]
S("Les autres gorilles avaient l'air de débutants.", [A(MG, [0, 0, -0.8], 'flex', 'smug', scale=2.4)] + [G(i, p, 'scared', 'scared', ry=r, scale=1.6) for i, (p, r) in enumerate(zip(pos3, [30, 0, -30]))],
  {'preset': 'wide', 'target': [0, 1.5, -1.8], 'angle': 0, 'zoom': 0.75, 'push': 0.1}, cut=True, set='zoo', highlight=['débutants'])
S("Il s'est battu contre eux et leur a foutu une rouste un par un.",
  [A(MG, None, 'punch', 'angry')] + [G(i, None, 'faint', 'dead', params={'dur': 0.5}, actions=[{'at': 0, 'clip': 'scared', 'expr': 'scared'}, {'at': 0.8 + i * 0.9, 'clip': 'faint', 'expr': 'dead', 'params': {'dur': 0.5}}]) for i in range(3)],
  {'preset': 'wide', 'target': [0, 1.5, -1.8], 'angle': 15, 'zoom': 0.7, 'push': 0.06, 'glide': 0.6}, highlight=['battu', 'rouste'],
  sfx=[{'name': 'thud', 'at': 0.8 + i * 0.9, 'vol': 0.6} for i in range(3)], fx=[{'type': 'shake', 'at': 0.8 + i * 0.9, 'dur': 0.2, 'amount': 0.03} for i in range(3)])
S("Il a battu tout le monde, est devenu l'alpha et s'est mis à vivre comme le chef de l'enclos.",
  [A(MG, [2.2, 1.0, -2.6], 'celebrate', 'happy', scale=2.4, attach=[{'name': 'crown', 'joint': 'head', 'pos': [0, 0.42, 0.05], 'scale': 1.4}])] + [G(i, p, 'kneel', 'sad', ry=r, scale=1.6) for i, (p, r) in enumerate(zip([[-0.6, 0, -0.6], [0.8, 0, -0.2], [-1.8, 0, -1.0]], [60, 20, 70]))],
  {'preset': 'wide', 'target': [1.0, 1.8, -1.6], 'angle': 10, 'zoom': 0.7, 'push': 0.1}, cut=True, set='zoo', highlight=['alpha', 'chef'],
  props=[{'name': 'rock', 'pos': [2.2, 0, -2.6], 'opts': {'size': 1.4}}])
S("Puis, un autre gros muscu est arrivé au zoo.", [A('muscu', [-1.6, 0, 6.4], 'walk', 'smug', ry=90, to=[0.2, 0, 6.0], moveEnd=1.8, scale=1.25, actions=[{'at': 1.9, 'clip': 'flex'}])],
  {'preset': 'full', 'target': 'muscu', 'angle': 180, 'zoom': 0.95, 'push': 0.08}, cut=True, set='zoo', highlight=['gros', 'muscu'])
S("Il a vu son physique, est devenu jaloux et a cru qu'il le provoquait.", [A(MG, [0, 0, 1.0], 'angryFist', 'angry', scale=2.4, attach=[{'name': 'crown', 'joint': 'head', 'pos': [0, 0.42, 0.05], 'scale': 1.4}])],
  {'preset': 'medium', 'target': MG, 'angle': 0, 'zoom': 1.0, 'push': 0.1}, cut=True, set='zoo', highlight=['jaloux', 'provoquait'])
S("Alors, il a appelé la police.", [A(MG, None, 'phone', 'angry', hold={'name': 'phone911', 'hand': 'R'})], {'preset': 'close', 'target': MG, 'angle': 10, 'push': 0.1, 'glide': 0.5}, highlight=['police'],
  overlays=[{'style': 'phone', 'text': '17', 'sub': 'POLICE', 'at': 0.4}])
S("Les flics sont arrivés en urgence et ont arrêté tous les gorilles pour dopage et possession de stéroïdes.",
  [A(MG, [0, 0, -1.0], 'handcuffed', 'sad', scale=2.4)] + [G(i, p, 'handcuffed', 'sad', ry=r, scale=1.6) for i, (p, r) in enumerate(zip(pos3, [20, 0, -20]))] + [A('flic1', [-1.4, 0, 1.2], 'point', 'angry', ry=150), A('flic2', [1.4, 0, 1.2], 'handsOnHips', 'angry', ry=-150)],
  {'preset': 'wide', 'target': [0, 1.4, -0.8], 'angle': 0, 'zoom': 0.8, 'push': 0.1}, cut=True, set='zoo', highlight=['flics', 'dopage', 'stéroïdes'],
  props=[{'name': 'policeCar', 'pos': [-3.5, 0, 6.5], 'ry': 90}], sfx=[{'name': 'siren', 'at': 0, 'vol': 0.4}])

# ---- 11. lab: the chemist --------------------------------------------------------------------------
hat = [{'name': 'porkpieHat', 'joint': 'head', 'pos': [0, 0.42, 0.06], 'scale': 1.0}, {'name': 'glasses', 'joint': 'head', 'pos': [0, 0.28, 0.24], 'opts': {'r': 0.055, 'dx': 0.075}}]
S("En remontant l'affaire, ils ont trouvé le chimiste qui fabriquait les produits.", [A('chimiste', [0, 0, -2.2], 'idle', 'neutral', attach=hat), A('flic1', [-1.4, 0, 0.6], 'point', 'angry', ry=140)],
  {'preset': 'wide', 'target': [-0.4, 1.3, -1.2], 'angle': 0, 'zoom': 0.7, 'push': 0.1}, cut=True, set='lab', highlight=['chimiste'])
S("Un gorille chauve avec des lunettes et un chapeau.", [A('chimiste', None, 'idle', 'unimpressed', attach=hat)], {'preset': 'close', 'target': 'chimiste', 'angle': 0, 'zoom': 0.9, 'push': 0.12, 'glide': 0.6}, highlight=['chauve', 'lunettes', 'chapeau'])
S("Walter White.", [A('chimiste', None, 'idle', 'smug', attach=hat)], {'preset': 'extremeClose', 'target': 'chimiste', 'angle': 0, 'zoom': 0.9, 'push': 0.05, 'glide': 0.4}, highlight=['Walter', 'White'], hold=0.3)
S("Ils l'ont arrêté aussi.", [A('chimiste', None, 'handcuffed', 'sad', attach=hat), A('flic1', [-0.8, 0, -1.6], 'handsOnHips', 'smug', ry=60)],
  {'preset': 'full', 'target': [-0.4, 1.4, -1.9], 'angle': 0, 'zoom': 0.8, 'push': 0.08, 'glide': 0.6}, highlight=['arrêté'])

# ---- 12. the chicken restaurant (fictional "Master Poulet") -----------------------------------
sign = {'name': 'signBoard', 'pos': [0, 2.2, -2.8], 'opts': {'text': 'MASTER POULET', 'bg': '#E1C25A', 'fg': '#C23A2E', 'w': 2.6, 'h': 0.6, 'posts': False, 'height': 0}}
S("Walter White leur a permis de remonter jusqu'au réseau de distribution.", [A('fringant', [0, 0, -1.2], 'armsCrossed', 'neutral')],
  {'preset': 'wide', 'target': [0, 1.4, -1.4], 'angle': 0, 'zoom': 0.7, 'push': 0.1}, cut=True, set='restaurant', highlight=['réseau', 'distribution'], props=[sign])
S("Le responsable s'appelait Karim Bouamrane.", [A('fringant', None, 'armsCrossed', 'unimpressed')], {'preset': 'close', 'target': 'fringant', 'angle': 0, 'zoom': 0.9, 'push': 0.1, 'glide': 0.7}, highlight=['Karim', 'Bouamrane'])
S("Il prétendait être opposé au restaurant de poulet.", [A('fringant', None, 'shakeHead', 'neutral')], {'preset': 'medium', 'target': 'fringant', 'angle': 15, 'push': 0.1, 'glide': 0.6}, highlight=['opposé', 'poulet'])
S("En réalité, il était derrière Master Poulet et faisait circuler les produits dans ce réseau.",
  [A('fringant', None, 'present', 'smug', hold={'name': 'preWorkout', 'hand': 'R', 'opts': {'text': 'INTERDIT'}})],
  {'preset': 'full', 'target': 'fringant', 'angle': -10, 'zoom': 0.8, 'push': 0.1, 'glide': 0.6}, highlight=['Master', 'Poulet', 'produits'],
  props=[{'name': 'foodSack', 'pos': [x, 0, -2.0], 'opts': {'text': 'MASTER POULET'}} for x in (-1.2, 1.2)])
S("Les flics l'ont arrêté, mais ils soupçonnaient un trafic beaucoup plus vaste.", [A('fringant', None, 'handcuffed', 'angry'), A('flic1', [-1.2, 0, -0.2], 'point', 'suspicious', ry=150), A('flic2', [1.2, 0, -0.2], 'think', 'suspicious', ry=-150)],
  {'preset': 'wide', 'target': [0, 1.4, -0.8], 'angle': 0, 'zoom': 0.75, 'push': 0.08, 'glide': 0.6}, highlight=['trafic', 'vaste'])

# ---- 13. the farms -----------------------------------------------------------------------------------
chick = lambda i, p, sc, clip='idle', expr='neutral', **kw: A(f'poulet{i}', p, clip, expr, scale=sc, **kw)
S("Alors, ils sont allés dans les fermes.", [A('flic1', [-0.8, 0, 2.0], 'walk', 'suspicious', ry=0, to=[-0.6, 0, 0.6]), A('flic2', [0.8, 0, 2.2], 'walk', 'suspicious', ry=0, to=[0.6, 0, 0.8])],
  {'preset': 'wide', 'target': [0, 1.3, -0.5], 'angle': 0, 'zoom': 0.8, 'push': 0.1}, cut=True, set='farm', highlight=['fermes'])
S("Les éleveurs donnaient des hormones de croissance aux poulets.", [A('fermier', [0, 0, -0.6], 'idle', 'smug', hold={'name': 'syringe', 'hand': 'R', 'scale': 2})] + [chick(i, p, 1.2, 'peck') for i, p in enumerate([[-1.2, 0, 0.2], [1.1, 0, 0.0], [-0.4, 0, 0.8]])],
  {'preset': 'full', 'target': [0, 1.2, -0.2], 'angle': 10, 'zoom': 0.85, 'push': 0.1}, cut=True, set='farm', highlight=['hormones', 'poulets'])
S("Les volailles étaient devenues beaucoup trop musclées.", [chick(i, p, 4.2, 'flex', 'smug', opts=None) for i, p in enumerate([[-1.4, 0, -0.4], [1.4, 0, -0.6], [0, 0, 0.6]])],
  {'preset': 'low', 'target': [0, 1.6, -0.2], 'angle': 0, 'zoom': 1.0, 'push': 0.1}, cut=True, set='farm', highlight=['volailles', 'musclées'], sfx=[{'name': 'boing', 'at': 0.2, 'vol': 0.4}])
S("Les policiers ont arrêté les poulets, puis les gens qui en avaient mangé.", [chick(i, p, 4.2, 'handcuffed', 'sad') for i, p in enumerate([[-1.4, 0, -0.4], [1.4, 0, -0.6]])] + [A('serveur', [0, 0, 0.8], 'handcuffed', 'sad'), A('flic1', [-0.6, 0, 2.0], 'point', 'angry', ry=180)],
  {'preset': 'wide', 'target': [0, 1.5, 0.2], 'angle': 0, 'zoom': 0.8, 'push': 0.08, 'glide': 0.7}, highlight=['poulets', 'mangé'])

# ---- 14. the police station: chickens = cops -------------------------------------------------------
cops = lambda n, clip='handcuffed', expr='sad': [A(f'flic{3 + i}', [-2.4 + i * 1.2, 0, -0.4 - (i % 2) * 0.6], clip, expr, ry=0) for i in range(n)]
S("Parmi eux, il y avait aussi des policiers qui avaient bouffé du poulet.", cops(4, 'handcuffed', 'sad'),
  {'preset': 'wide', 'target': [-0.6, 1.4, -0.6], 'angle': 0, 'zoom': 0.8, 'push': 0.1}, cut=True, set='policeStation', highlight=['policiers', 'poulet'])
S("Et là, un mec leur a dit : mais vous aussi, on vous appelle les poulets.", [A('prisonnier', [0.4, 0, 0.6], 'talk', 'smug', talk=True)],
  {'preset': 'close', 'target': 'prisonnier', 'angle': 10, 'push': 0.1, 'glide': 0.6}, highlight=['poulets'])
S("Les flics se sont regardés.", [A('flic1', [-0.5, 0, 0.4], 'stand', 'surprised', ry=90), A('flic2', [0.5, 0, 0.4], 'stand', 'surprised', ry=-90)],
  {'preset': 'medium', 'target': [0, 2.0, 0.4], 'angle': 0, 'zoom': 1.0, 'push': 0.08}, cut=True, set='policeStation', highlight=['regardés'], hold=0.3)
S("Putain, il avait raison.", [A('flic1', None, 'facepalm', 'shocked')], {'preset': 'extremeClose', 'target': 'flic1', 'angle': 60, 'push': 0.05, 'glide': 0.4}, highlight=['Putain', 'raison'])
S("Alors, ils ont commencé à arrêter les autres policiers.", [A('flic1', [-0.5, 0, 0.4], 'point', 'angry', ry=40), A('flic2', [0.5, 0, 0.4], 'handcuffed', 'sad', ry=-20)] + cops(3, 'handcuffed', 'sad'),
  {'preset': 'wide', 'target': [-0.4, 1.4, -0.2], 'angle': 0, 'zoom': 0.8, 'push': 0.08}, cut=True, set='policeStation', highlight=['arrêter', 'policiers'])
S("Pour être sûrs de n'oublier personne, ils ont appelé la Belgique, puis Montréal, puis tous les pays où les flics pouvaient être appelés les poulets en français.",
  [A('flic1', [0, 0, 0.4], 'phone', 'neutral', hold={'name': 'phone911', 'hand': 'R'})],
  {'preset': 'medium', 'target': 'flic1', 'angle': 15, 'push': 0.15}, cut=True, set='policeStation', highlight=['Belgique', 'Montréal', 'poulets'],
  overlays=[{'style': 'banner', 'text': '📞 BELGIQUE', 'at': 2.0, 'until': 3.2}, {'style': 'banner', 'text': '📞 MONTRÉAL', 'at': 3.2, 'until': 4.4}, {'style': 'banner', 'text': '📞 SUISSE · LUXEMBOURG · …', 'at': 4.4}])
S("Chaque policier arrêtait le suivant.", [A(f'flic{3 + i}', [-3 + i * 1.0, 0, 0], 'handcuffed', 'sad', ry=90) for i in range(6)],
  {'preset': 'wide', 'target': [-0.5, 1.3, 0], 'angle': 0, 'zoom': 0.9, 'push': 0.06, 'orbit': 20}, cut=True, set='policeStation', highlight=['suivant'])
S("Les commissariats se remplissaient de leurs propres employés.", [], {'preset': 'wide', 'target': [0, 1.4, 0], 'angle': 0, 'zoom': 0.75, 'push': 0.1}, cut=True, set='prisonCell', highlight=['commissariats', 'employés'],
  crowd=[{'spec': {'preset': 'cop'}, 'count': 9, 'center': [0, 0, -1.2], 'spread': 3.2, 'clip': 'handcuffed', 'seed': 5}])
S("À la fin, il ne restait qu'un seul flic libre.", [A('flic1', [0, 0, 0], 'stand', 'sad')], {'preset': 'wide', 'target': 'flic1', 'angle': 0, 'zoom': 0.8, 'push': 0.15}, cut=True, set='policeStation', highlight=['seul', 'libre'],
  sfx=[{'name': 'crickets', 'at': 0.3, 'vol': 0.3}])
S("Il a menotté son premier poignet.", [A('flic1', None, 'handcuffed', 'unimpressed', hold={'name': 'handcuffs', 'hand': 'L'})], {'preset': 'medium', 'target': 'flic1', 'angle': 10, 'push': 0.1, 'glide': 0.6}, highlight=['menotté', 'poignet'],
  sfx=[{'name': 'click', 'at': 0.8, 'vol': 0.6}])
S("L'autre main a essayé de le libérer.", [A('flic1', None, 'pressGlass', 'worried', hold={'name': 'handcuffs', 'hand': 'L'})], {'preset': 'close', 'target': 'flic1', 'angle': 0, 'push': 0.1, 'glide': 0.5}, highlight=['libérer'])
S("Complicité.", [A('flic1', None, 'handcuffed', 'dead', hold={'name': 'handcuffs', 'hand': 'L'})], {'preset': 'extremeClose', 'target': 'flic1', 'angle': 0, 'push': 0.04, 'glide': 0.4}, highlight=['Complicité'],
  overlays=[{'style': 'stamp', 'text': 'COMPLICITÉ', 'at': 0.4, 'y': 0.3}], sfx=[{'name': 'sting', 'at': 0.4, 'vol': 0.4}], hold=1.2)

# ---- framing pass after contact-sheet review -----------------------------------------------------
BIG = lambda t: isinstance(t, str) and (t.startswith('g') or t in (MG, 'chimiste') or t.startswith('poulet'))
UP = {'extremeClose': 'close', 'close': 'medium', 'medium': 'full'}
for sh in shots:
    c = sh['camera']; t = c.get('target')
    if BIG(t):   # creatures are much wider/bulkier than the human the presets were tuned on
        c['preset'] = UP.get(c.get('preset', 'medium'), c.get('preset')); c['zoom'] = round(c.get('zoom', 1) * 1.35, 2)
def fix(i, **cam):
    shots[i]['camera'].update(cam)
fix(20, target=[0.2, 1.4, 5.8], angle=75, zoom=1.4, preset='full')
for a in shots[20]['actors']:
    if a['id'] == MN: a['ry'] = 0
shots[21]['remove'] = ['madame', 'gamin']
fix(22, preset='high', target=[0.3, 0.9, -2.2], angle=8, zoom=0.75)
fix(38, preset='full', target=[-2.2, 0.8, 1.2], zoom=0.75)
fix(51, target=[0, 2.6, -1.8], zoom=1.25); fix(52, target=[0, 2.6, -1.8], zoom=1.2)
fix(53, target=[1.0, 2.6, -1.6], zoom=1.15)
fix(57, target=[0, 2.2, -0.8], zoom=1.35)
fix(61, target=[-0.4, 2.0, -1.9], zoom=1.2)
fix(69, target=[0, 2.6, -0.2], zoom=2.0, preset='full')
fix(18, zoom=0.45, target=[0, 3.8, -1.5])
shots[21]['camera'] = {'from': [4.5, 2.6, 8.0], 'to': [3.6, 2.2, 6.6], 'lookAt': [0.3, 1.0, 3.2], 'fov': 42}
shots[22]['camera'] = {'from': [2.4, 6.0, 7.5], 'to': [2.0, 5.2, 6.4], 'lookAt': [0.3, 0.6, -2.4], 'fov': 45}
shots[53]['camera'] = {'from': [0.0, 3.6, 10.0], 'to': [0.3, 3.4, 8.6], 'lookAt': [1.2, 2.6, -2.0], 'fov': 45}

# ---- v2: no 2D overlays at all, discreet 3D watermark, funnier acting -----------------------------
for sh in shots: sh.pop('overlays', None)
def act(i, id):
    return next(a for a in shots[i]['actors'] if a['id'] == id)
def props(i, *ps): shots[i].setdefault('props', []); shots[i]['props'] += list(ps)
WM = lambda **kw: {'name': 'wmSign', **kw}
# watermark: one per location, in the background, muted (continuous takes carry it across several shots)
props(0, WM(anchor='picture', offset=[1.7, -0.75, 0.03]))
props(1, WM(pos=[2.6, 0.35, 4.37], opts={'kind': 'sticker'}))                 # sticker on the enclosure wall
props(11, WM(pos=[-4.6, 0, -3.6], opts={'kind': 'stand'}))
props(15, WM(pos=[4.2, 0, -1.2], opts={'kind': 'stand', 'bg': '#E6E1D3'}))
props(18, WM(anchor='wall', offset=[1.6, -0.3, 0.03]))
props(35, WM(anchor='mirror', offset=[-2.4, 0.5, 0.02], opts={'bg': '#1E242C', 'fg': '#8FA3B5'}))
props(58, WM(pos=[1.7, 1.7, -3.56], opts={'kind': 'poster'}))
props(62, WM(anchor='menu', offset=[0, -0.75, 0.03]))
props(67, WM(pos=[-2.8, 0, -1.4], opts={'kind': 'stand'}))
props(71, WM(anchor='board', offset=[0.1, -0.85, 0.03]))
# funnier acting
act(2, 'g1')['clip'] = 'chestBeat'; act(2, 'g0')['clip'] = 'posing'; act(2, 'g2')['clip'] = 'posing'; act(2, 'g2')['phase'] = 0.5
act(3, M).update(clip='doubleTake', actions=[{'at': 0.9, 'clip': 'angryFist', 'expr': 'angry'}], expr='surprised')
act(4, 'g1').update(clip='posing')
for g in shots[6]['actors']: g['speed'] = 1.7
act(10, M).update(clip='shovelFood', actions=[{'at': 2.2, 'clip': 'shovelFood', 'expr': 'disgusted'}]); act(10, 'chevre').update(clip='flee', expr='scared', to=[3.0, 0, 0.6], moveStart=1.5)
for g in shots[11]['actors']:
    if g['id'].startswith('g'): g['clip'] = 'chestBeat'
act(13, M)['speed'] = 1.6
act(15, MN)['clip'] = 'strut'; act(16, MN)['clip'] = 'strut'
for id in ('madame', 'mamie', 'gamin'): act(16, id)['clip'] = 'flail'
act(17, MN)['speed'] = 1.3
act(18, MN)['speed'] = 1.5
for id in ('madame', 'gamin'): act(20, id).update(clip='flail', to=[act(20, id)['pos'][0] * 3, 0, 9.0], moveStart=0.6, moveEnd=2.2)
for g in shots[19]['actors']:
    if g['id'].startswith('g'): g['clip'] = 'posing'
act(28, 'g1')['clip'] = 'tiptoe'
props(29, {'name': 'exclamationMark', 'pos': [0.6, 1.4, -1.4], 'scaleTo': 0.01, 'scaleStart': 0.8, 'scaleEnd': 1.0})
shots[29]['props'][0].update(moveEase='steps', steps=7)
shots[34]['props'][0].update(moveEase='steps', steps=6)
act(30, 'g1').update(clip='doubleTake', expr='suspicious')
act(36, 'g1')['speed'] = 1.6
act(37, 'g1')['speed'] = 1.4; act(37, 'coach')['speed'] = 1.4
act(42, MN).update(clip='scared', expr='shocked')
act(44, MG)['clip'] = 'chestBeat'
act(45, MG)['clip'] = 'posing'
act(47, MG)['speed'] = 2.2
act(48, MG)['speed'] = 8; shots[48]['actors'][1].update(clip='spinFall', params={'dur': 0.9})
act(49, MG)['speed'] = 3
act(50, MG)['clip'] = 'chestBeat'
for g in shots[51]['actors']:
    if g['id'].startswith('g'): g['clip'] = 'flail'; g['speed'] = 0.6
for i in range(3):
    gi = act(52, f'g{i}'); gi['actions'] = [{'at': 0, 'clip': 'scared', 'expr': 'scared'}, {'at': 0.8 + i * 0.9, 'clip': 'spinFall', 'expr': 'dead', 'params': {'dur': 0.7}}]
props(52, *[{'name': 'explosionBurst', 'pos': [p[0], 1.6, p[2] + 0.6], 'scale': 0.01, 'scaleTo': 1.2, 'scaleStart': 0.8 + i * 0.9, 'scaleEnd': 1.0 + i * 0.9} for i, p in enumerate(pos3)])
act(53, MG)['clip'] = 'chestBeat'
act(54, 'muscu').update(clip='strut', actions=[{'at': 1.9, 'clip': 'posing', 'expr': 'smug'}])
act(55, MG)['clip'] = 'chestBeat'
act(73, 'flic1').update(clip='doubleTake', expr='sideLook'); act(73, 'flic2').update(clip='doubleTake', expr='sideLook', phase=0.15)
act(74, 'flic1')['clip'] = 'facepalm'
act(81, 'flic1').update(clip='selfStruggle', expr='angry')
act(82, 'flic1').update(clip='selfStruggle', expr='dead', speed=0.6)
shots[30]['camera'].update(target=[2.0, 2.2, -3.4], zoom=1.25)
shots[35]['camera'].update(target=[0.6, 2.4, -0.3], zoom=1.15)
shots[48]['camera'].update(target=[0.6, 2.7, 0.2], zoom=1.3)

episode = {
    'title': 'Le gorille', 'captionWords': 3, 'minShot': 1.0, 'tail': 0.0,
    'music': {'mood': 'quirky', 'vol': 0.07},
    'voice': {'engine': 'elevenlabs', 'name': 'allan tiktok', 'model': 'eleven_v4', 'stability': 0.8, 'rate': 1.08, 'gap': 0.16},
    'cast': {
        M: {'preset': 'lemec'}, MN: {'preset': 'lemec', 'naked': True},
        MG: {'type': 'creature', 'name': 'gorilla', 'opts': {'clothes': 'tie', 'seed': 21}},
        **{f'g{i}': {'type': 'creature', 'name': 'gorilla', 'opts': {'seed': 30 + i}} for i in range(3)},
        'chevre': {'type': 'creature', 'name': 'goat', 'opts': {'seed': 3}},
        'coach': {'preset': 'sportif'}, 'muscu': {'preset': 'sportif', 'build': {'width': 1.35, 'height': 1.05}},
        'madame': {'preset': 'madame'}, 'mamie': {'preset': 'mamie'}, 'gamin': {'preset': 'gamin'},
        'chimiste': {'type': 'creature', 'name': 'gorilla', 'opts': {'seed': 77, 'colors': {'body': '#4A4B52'}}},
        'fringant': {'preset': 'fringant'}, 'fermier': {'preset': 'fermier'}, 'serveur': {'preset': 'serveur'}, 'prisonnier': {'preset': 'prisoner'},
        'flic1': {'preset': 'cop'}, 'flic2': {'preset': 'cop2'},
        **{f'flic{3 + i}': {'preset': 'cop' if i % 2 else 'cop2', 'seed': 40 + i} for i in range(6)},
        **{f'poulet{i}': {'type': 'creature', 'name': 'chicken', 'opts': {'seed': 50 + i}} for i in range(3)},
    },
    'shots': shots,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gorille.json')
json.dump(episode, open(out, 'w'), ensure_ascii=False, indent=1)
words = sum(len(s['line'].split()) for s in shots)
print(out, len(shots), 'shots,', words, 'words, ~%.0f s' % (words / 2.9))
