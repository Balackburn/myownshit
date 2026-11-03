#!/usr/bin/env python3
"""LE CHRONO — v4 storyboard (python3 scripts-fr/chrono4.py -> chrono4.json)

Fully coherent with the plot of "A Kind of a Stopwatch" (The Twilight Zone, 1963), told in the
french-lowpoly-absurd-shorts style (deadpan narrator, real lines spoken by the characters with the SAME voice,
ce mec / ce con / putain / les flics), with extra absurd gags (police, 10 000 ans).

Plot beats (Wikipedia) -> scenes
  1. biggest bore on Earth, ten-year record of meaningless words at the coffee break          -> PAUSE
  2. summoned by the boss, thinks his suggestion-box ideas earned recognition; the ideas are
     about fields the company is not in -> fired for wasting time                              -> PATRON
  3. Joe Palucci's bar: drives the patrons away with his opinions on a match; Palucci asks him
     to drink elsewhere; he ignores him and buys a drink for Potts, the drunk who talks like
     long ago; Potts gives him the stopwatch; it stops time for everyone but its holder        -> BAR
  4. tries to show the boss (to save the company); the boss does not understand, dismisses him -> DEMO PATRON
     (time stopped, moustache drawn, time restarted: from the boss's side nothing happened)
  5. tries to show the bar customers; they do not understand (they think they are drunk)       -> DEMO BAR
  6. robs a bank: freezes everyone, wheels a cart of cash out of the vault, drops the watch,
     it breaks -> time frozen for good; no way to repair it                                    -> BANQUE
  7. begs the frozen people for help (+ the police gag: frozen mid racial-profiling check,
     the satire targets the cops' prejudice, never the man they check)                         -> RUE
  8. "he used it and he misused it, and now he's just been handed the bill": ten thousand years
     later he still has not paid his bill at Jo's                                              -> FIN
Coherence rules kept: frozen people keep their exact pose (he can carry them, rigid); no day/night and no growing
spider webs in frozen time; only his own body ages (the beard).
"""
import json, os

def L(id, text, speaker=None, **kw): return {'id': id, 'text': text, **({'speaker': speaker} if speaker else {}), **kw}
def act(id, pos, ry=0, clip='idle', expr=None, keys=None, **kw):
    d = {'id': id, 'pos': pos, 'ry': ry, 'clip': clip, 'keys': keys or [], **kw}
    if expr: d['expr'] = expr
    return d
def k(at, **kw): return {'at': at, **kw}
def cam(at, frame=None, size='ms', **kw):
    d = {'at': at, 'size': size, **kw}
    if frame is not None: d['frame'] = frame
    return d
def P(id, name, **kw): return {'id': id, 'name': name, **kw}
WM = lambda **kw: {'name': 'wmSign', 'id': 'wm', **kw}
STOOL_Y = 0.15
scenes = []

# ---------------------------------------------------------------- 1. la pause café ------------------
scenes.append({
  'id': 'pause', 'set': 'office', 'ambience': 'office',
  'lines': [L('C1', "Ce mec était le plus gros relou de la planète.", highlight=['relou']),
            L('C2', "Dix ans de record de mots inutiles à la pause café.", highlight=['record', 'inutiles'])],
  'actors': [
    act('mec', [1.3, 0, -1.0], 0, 'talk', 'happy', face='coll1', keys=[k('C2', clip='talk', speed=1.7), k('C2#8', look='coll1')]),
    act('coll1', [2.35, 0, -0.55], 0, 'holdOut', 'unimpressed', face='mec', keys=[
        k('C1#4', clip='nod', expr='unimpressed'), k('C2#3', expr='sleepy', clip='stand'),
        k('C2.end-0.55', clip='faint', params={'dur': 0.45}, expr='dead', sfx='thud', sfxAt=0.45)]),
    act('coll2', [0.35, 0, -0.35], 0, 'stand', 'happy', face='mec', keys=[
        k('C1.end', expr='unimpressed', clip='lookAround'), k('C2#3', clip='lookItem', expr='suspicious'),
        k('C2#5', to=[-2.6, 0, 1.6], clip='tiptoe', speed=0.9, then='idle')]),
  ],
  'props': [{'id': 'machine', 'name': 'coffeeMachine', 'pos': [2.7, 0, -2.4]},
            {'id': 'mug', 'name': 'mug', 'on': {'actor': 'coll1', 'hand': 'R'}, 'keys': [k('C2.end-0.5', detach=True, fall=True, impact='clink')]},
            WM(anchor='picture', offset=[1.5, -0.7, 0.03])],
  'cams': [cam(0, ['mec', 'coll1', 'coll2'], 'fs', worldAngle=15, elev=8, move='push', amount=0.08),
           cam('C1#4', 'mec', 'ms', angle=30), cam('C1.end-0.2', 'coll1', 'mcu', angle=-25),
           cam('C2', 'coll2', 'cu', angle=35), cam('C2#5', 'coll2', 'fs', angle=60, move='track'),
           cam('C2#8', 'mec', 'cu', angle=25, move='push'), cam('C2.end-0.6', ['coll1', 'mec'], 'fs', angle=-35)],
  'tail': 0.5,
})

# ---------------------------------------------------------------- 2. viré (idées hors sujet) --------
scenes.append({
  'id': 'patron', 'set': 'office', 'ambience': 'office',
  'lines': [L('C3', "Un jour, son patron l'a convoqué. Ce con pensait qu'on allait le féliciter.", highlight=['féliciter.']),
            L('C4', "Quatre cents idées dans la boîte à suggestions. Des fusées. Des sous-marins.", 'patron', highlight=['fusées.', 'sous-marins.']),
            L('C5', "Merci, patron !", 'mec'),
            L('C6', "On fabrique des yaourts. Vous êtes viré.", 'patron', highlight=['yaourts.', 'viré.'])],
  'actors': [
    act('patron', [-4.75, 0.12, -2.05], 0, 'sit', 'unimpressed', keys=[
        k('C3#3', clip='beckon'), k('C4', clip='sitShow', expr='suspicious'), k('C4:sous', clip='sitShow'),
        k('C5', clip='sit', expr='unimpressed'), k('C6', clip='sitShow', expr='unimpressed'), k('C6:viré', clip='sitPoint', expr='angry')]),
    act('mec', [-1.8, 0, 0.9], 0, 'idle', 'happy', keys=[
        k('C3', to=[-4.35, 0, -0.65], clip='strut', faceEnd='patron'),
        k('C4', clip='handsOnHips', expr='smug'), k('C5', clip='present', expr='happy'),
        k('C6:viré', clip='stareCamera', expr='shocked'),
        k('C6.end+0.5', to=[-1.2, 0, 2.2], clip='carryBox', expr='sad')]),
  ],
  'props': [P('pile', 'paperPile', pos=[-5.3, 0.76, -1.3], opts={'count': 150}),
            P('rocket', 'drawingSheet', opts={'kind': 'rocket', 'num': 312}, visible=False, on={'actor': 'patron', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}, keys=[k('C4:fusées', visible=True), k('C4:sous', visible=False)]),
            P('sub', 'drawingSheet', opts={'kind': 'sub', 'num': 313}, visible=False, on={'actor': 'patron', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}, keys=[k('C4:sous', visible=True), k('C5', visible=False)]),
            P('yaourt', 'mug', opts={'color': '#FFFFFF'}, visible=False, on={'actor': 'patron', 'hand': 'R'}, keys=[k('C6', visible=True), k('C6:viré', visible=False)]),
            P('box', 'cardboardBox', opts={'text': ''}, visible=False, pos=[-3.9, 0, -0.2], keys=[k('C6.end+0.45', visible=True, attach='mec', joint='torso', offset=[0, 0.28, 0.42])])],
  'cams': [cam(0, 'patron', 'ms', angle=10), cam('C3#4', 'mec', 'fs', angle=35, move='track'),
           cam('C3:con', 'mec', 'cu', angle=20),
           cam('C4', ots=['mec', 'patron', -1]), cam('C4:boîte', 'pile', 'mls', angle=-15),
           cam('C4:fusées', 'rocket', 'cu', worldAngle=10, noOcclusion=True), cam('C4:sous', 'sub', 'cu', worldAngle=-10, noOcclusion=True),
           cam('C5', 'mec', 'cu', angle=15), cam('C6', 'patron', 'mcu', angle=-35),
           cam('C6:viré', 'mec', 'ecu', angle=5, move='push'), cam('C6.end+0.45', 'mec', 'fs', angle=35, move='track', withProps=True)],
  'tail': 1.3,
})

# ---------------------------------------------------------------- 3. chez Jo : le match, le vieux, le chrono
scenes.append({
  'id': 'bar', 'set': 'bar', 'ambience': 'bar', 'lighting': 'interior',
  'freeze': {'at': 'C13+0.55', 'except': ['mec', 'watch']},
  'lines': [L('C7', "Alors il est allé chez Jo donner son avis sur le match.", highlight=['match.']),
            L('C8', "Le foot, c'est truqué. Le ballon est carré.", 'mec', highlight=['carré.']),
            L('C9', "Tout le bar s'est barré.", highlight=['barré.']),
            L('C10', "Va boire ailleurs.", 'jo', highlight=['ailleurs.']),
            L('C11', "Ce con a payé un verre au dernier client, un vieux poivrot qui parlait comme en 1900.", highlight=['1900.']),
            L('C12', "Mazette, un godet ! Tiens, mon brave : une tocante qui arrête le temps.", 'vieux', highlight=['tocante', 'temps.']),
            L('C13', "Il a appuyé."),
            L('C14', "Putain…", 'mec', pre=0.45)],
  'actors': [
    act('mec', [0.5, STOOL_Y, -1.25], -90, 'sitTalk', 'happy', face='client1', keys=[
        k('C8', clip='sitTalk', expr='smug'), k('C8:ballon', clip='sitShow', expr='smug', sfx='thud', sfxAt=0.3, vol=0.35),
        k('C10', clip='sit', expr='unimpressed', face='jo', turn=0.3),
        k('C11', face='vieux', turn=0.3, clip='sitGive', expr='happy', sfx='cash', sfxAt=0.4, vol=0.4),
        k('C12:Tiens', clip='sitTake', expr='suspicious'),
        k('C13', clip='sitLookItem', expr='neutral', sfx='click', sfxAt=0.55),
        k('C14', expr='shocked', clip='stareCamera', face=0, turn=0.3)]),
    act('client1', [-0.5, STOOL_Y, -1.25], 90, 'sit', 'unimpressed', face='mec', keys=[
        k('C8:ballon', expr='scared'), k('C9', to=[-6.6, 0, 2.0], clip='walk', speed=1.7, expr='unimpressed')]),
    act('client2', [-1.5, STOOL_Y, -1.25], 90, 'sit', 'unimpressed', keys=[
        k('C8:truqué', expr='shocked'), k('C9#1', to=[-6.9, 0, 2.7], clip='flee', speed=2.6, expr='scared')]),
    act('jo', [0.35, 0, -2.6], 0, 'wipeGlass', 'unimpressed', keys=[
        k('C10', clip='point', expr='angry', face='mec', turn=0.25),
        k('C11#4', to=[1.4, 0, -2.6], clip='walk', speed=1.2, faceEnd=0, then='wipeGlass', expr='unimpressed')]),
    act('vieux', [2.5, STOOL_Y, -1.25], -90, 'drunk', 'sleepy', face='mec', keys=[
        k('C11:vieux', clip='sitTake', expr='happy'), k('C12', clip='drinkUp', expr='happy', sfx='gulp', sfxAt=0.3),
        k('C12:Tiens', clip='sitGive', expr='happy'), k('C12.end', clip='drunk', expr='sleepy'),
        k('C13+0.15', clip='tipOverSit', params={'dur': 1.0}, expr='surprised')]),
  ],
  'props': [P('tv', 'tv', opts={'match': True}, pos=[-2.6, 1.11, -2.05]),
            P('ballon', 'squareBall', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('C8:ballon', visible=True), k('C10', visible=False)]),
            P('beer', 'beerGlass', on={'actor': 'mec', 'hand': 'R'}, visible=False, keys=[k('C11', visible=True), k('C11+0.9', attach='vieux', hand='L')]),
            P('coin', 'coin', pos=[1.2, 1.12, -1.75], visible=False, keys=[k('C11+0.4', visible=True)]),
            P('watch', 'stopwatch', scale=1.5, visible=False, on={'actor': 'vieux', 'hand': 'R'}, keys=[k('C12:tocante', visible=True), k('C12.end-0.2', attach='mec', hand='R')]),
            P('stream', 'beerStream', opts={'length': 0.5}, visible=False, on={'actor': 'vieux', 'joint': 'handL', 'offset': [0, -0.22, 0.02]}, keys=[k('C13+0.45', visible=True)]),
            WM(anchor='sign', offset=[2.0, -0.55, 0.03], opts={'bg': '#2A1E1A', 'fg': '#C9A86A'})],
  'cams': [
    cam(0, ['mec', 'client1', 'client2'], 'fs', worldAngle=15, elev=10),
    cam('C7:avis', 'mec', 'ms', angle=35), cam('C7:match', 'tv', 'ms', worldAngle=0, noOcclusion=True),
    cam('C8', 'mec', 'mcu', angle=20), cam('C8:ballon', ['mec', 'client1'], 'ms', worldAngle=10),
    cam('C9', ['mec', [-1.5, 1.0, -1.25]], 'fs', worldAngle=0, elev=8, move='push', amount=0.06),
    cam('C10', 'jo', 'mcu', angle=15), cam('C10.end', 'mec', 'cu', angle=25),
    cam('C11', ['mec', 'vieux'], 'ms', worldAngle=10), cam('C11:vieux', 'vieux', 'ms', angle=35),
    cam('C12', ots=['mec', 'vieux', 1]), cam('C12:tocante', 'watch', 'cu', angle=-35, elev=12),
    cam('C13', 'mec', 'cu', angle=30), cam('C13.end', ['vieux', 'mec', 'jo'], 'fs', worldAngle=10, move='push', amount=0.08),
    cam('C14', 'mec', 'ecu', angle=0), cam('C14.end', 'jo', 'ms', angle=-20),
  ],
  'tail': 0.9,
})

# ---------------------------------------------------------------- 4. démo au patron (temps arrêté, relancé)
scenes.append({
  'id': 'demoPatron', 'set': 'office', 'ambience': 'office',
  'freeze': {'at': 'C15#13', 'until': 'C15#16+0.1', 'except': ['mec', 'moustache', 'marker', 'watch2']},
  'lines': [L('C15', "Il a voulu le montrer à son patron pour sauver la boîte. Temps arrêté, moustache, temps relancé.", highlight=['moustache,']),
            L('C16', "Et alors ? Vous êtes toujours viré.", 'patron', highlight=['toujours', 'viré.'])],
  'actors': [
    act('patron', [-4.75, 0.12, -2.05], 0, 'sit', 'unimpressed', face='mec', keys=[
        k('C15#4', clip='sitShow', expr='suspicious'), k('C15#12', clip='sit', expr='unimpressed'),
        k('C16', clip='sitPoint', expr='angry', face=20, turn=0.3)]),
    act('mec', [-4.25, 0, -2.5], -65, 'present', 'happy', face='patron', keys=[
        k('C15#12', clip='lookItem', expr='smug', sfx='click', sfxAt=0.5),
        k('C15#14', clip='drawOn', expr='happy', sfx='squeak'),
        k('C15#16-0.25', clip='lookItem', expr='smug', sfx='click', sfxAt=0.3),
        k('C16', clip='present', expr='happy'), k('C16:viré', clip='stand', expr='sad')]),
  ],
  'props': [P('watch2', 'stopwatch', scale=1.5, on={'actor': 'mec', 'hand': 'L'}),
            P('marker', 'marker', on={'actor': 'mec', 'hand': 'R'}),
            P('moustache', 'mustache3d', scale=0.01, on={'actor': 'patron', 'joint': 'head', 'offset': [0, 0.13, 0.115]}, keys=[k('C15#14', scale=1.5, dur=0.55)]),
            P('pile', 'paperPile', pos=[-5.3, 0.76, -1.3], opts={'count': 150})],
  'cams': [cam(0, ['patron', 'mec'], 'ms', worldAngle=25), cam('C15:sauver', 'mec', 'mcu', angle=20),
           cam('C15#12', 'mec', 'cu', angle=25),
           cam('C15#14', 'patron', 'ecu', angle=0, move='push', amount=0.06),
           cam('C15#16', ['patron', 'mec'], 'ms', worldAngle=20, elev=6),
           cam('C16', 'patron', 'cu', angle=5), cam('C16:viré', 'mec', 'cu', angle=15)],
  'tail': 0.6,
})

# ---------------------------------------------------------------- 5. démo au bar (personne ne comprend)
GL = [[-1.15, 1.11, -1.72], [-0.15, 1.11, -1.72], [0.85, 1.11, -1.72]]
scenes.append({
  'id': 'demoBar', 'set': 'bar', 'ambience': 'bar', 'lighting': 'interior',
  'freeze': {'at': 'C17:figé', 'until': 'C17.end+0.15', 'except': ['mec', 'watch3'] + [f'up{i}' for i in range(3)] + [f'dn{i}' for i in range(3)]},
  'lines': [L('C17', "Au bar, il a figé tout le monde et retourné toutes les bières.", highlight=['retourné']),
            L('C18', "Jo… je crois que j'ai trop bu.", 'client1', highlight=['trop', 'bu.']),
            L('C19', "Personne n'a rien compris.", highlight=['rien', 'compris.'])],
  'actors': [
    act('client1', [-1.15, STOOL_Y, -1.2], 180, 'sit', 'happy', keys=[k('C18', clip='sitLookItem', expr='shocked'), k('C18:Jo', face='jo', turn=0.3)]),
    act('client2', [-0.15, STOOL_Y, -1.2], 180, 'sit', 'happy', keys=[k('C18', expr='surprised')]),
    act('vieux', [0.85, STOOL_Y, -1.2], 180, 'drunk', 'sleepy'),
    act('jo', [-0.3, 0, -2.6], 0, 'wipeGlass', 'neutral', keys=[k('C18:bu', clip='bigShrug', expr='unimpressed'),
        k('C19', clip='holdOut', expr='angry', face='mec', turn=0.3)]),
    act('mec', [-2.4, 0, -0.6], 60, 'idle', 'smug', keys=[
        k('C17:figé-0.35', clip='lookItem', expr='smug', sfx='click', sfxAt=0.35),
        k('C17:figé+0.1', path=[[-1.15, 0, -0.6], [0.85, 0, -0.6]], clip='walk', speed=1.4, faceEnd=180),
        k('C17.end-0.15', clip='lookItem', expr='smug', sfx='click', sfxAt=0.3, face=60),
        k('C18', clip='facepalm', expr='unimpressed'),
        k('C19', to=[-6.5, 0, 1.8], clip='walk', speed=1.5, expr='sad')]),
  ],
  'props': [P('watch3', 'stopwatch', scale=1.5, on={'actor': 'mec', 'hand': 'R'}),
            *[P(f'up{i}', 'beerGlass', pos=p, keys=[k(f'C17:retourné+{0.25 * i:.2f}', visible=False)]) for i, p in enumerate(GL)],
            *[P(f'dn{i}', 'beerGlass', pos=[p[0], p[1] + 0.168, p[2]], rot=[3.14159, 0, 0], visible=False, keys=[k(f'C17:retourné+{0.25 * i:.2f}', visible=True, sfx='clink', vol=0.35)]) for i, p in enumerate(GL)],
            P('bill', 'bill', opts={'items': [['1 demi', '4,50'], ['3 bières retournées', '13,50']], 'total': '18,00 €'}, scale=1.4, visible=False, on={'actor': 'jo', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}, keys=[k('C19', visible=True)])],
  'cams': [cam(0, ['client1', 'client2', 'vieux'], 'fs', worldAngle=0, elev=8),
           cam('C17:figé', 'mec', 'ms', angle=20, move='track'),
           cam('C17:retourné', [[-1.2, 1.2, -1.72], [-0.1, 1.2, -1.72]], 'cu', worldAngle=180, elev=20),
           cam('C18', 'client1', 'cu', worldAngle=175), cam('C18:bu', 'jo', 'ms', angle=10),
           cam('C19', ['jo', 'mec'], 'fs', worldAngle=20, elev=6)],
  'tail': 0.6,
})

# ---------------------------------------------------------------- 6. la banque : ticket, caddie, chrono cassé, scotch
scenes.append({
  'id': 'banque', 'set': 'bank', 'ambience': 'bank',
  'freeze': {'at': 'C20:braqué+0.35', 'except': ['mec', 'cart', 'cash', 'watch', 'ticket', 'tape']},
  'lines': [L('C20', "Alors il a braqué une banque.", highlight=['braqué']),
            L('C21', "Il a quand même pris un ticket.", highlight=['ticket.']),
            L('C22', "Mais en sortant, ce con a fait tomber le chrono.", highlight=['tomber', 'chrono.']),
            L('C23', "Il a essayé de le réparer avec du scotch.", highlight=['scotch.']),
            L('C24', "Le temps ne repartirait plus jamais.", highlight=['jamais.'])],
  'actors': [
    act('guichetier', [-1.2, 0, -2.15], 0, 'giveItem', 'neutral'),
    act('vigile', [-2.6, 0, 1.0], 60, 'yawnStretch', 'sleepy'),
    act('cliente', [-0.4, 0, 0.9], 120, 'walk', 'neutral', params={'freq': 1.6}),
    act('mec', [1.0, 0, 2.6], 180, 'idle', 'smug', keys=[
        k('C20:braqué', clip='lookItem', expr='smug', sfx='click', sfxAt=0.35),
        k('C21', to=[1.55, 0, 1.75], clip='walk', speed=1.3, faceEnd=90, then='takeItem'),
        k('C21.end+0.05', to=[2.4, 0, -2.0], glide=True, dur=0.05, face=0, clip=None),
        k('C22', path=[[1.9, 0, -0.6], [1.25, 0, 0.85]], clip='pushCartWalk', until='C22:tomber'),
        k('C22:tomber+0.05', to=[0.95, 0, 1.75], clip='pushCartWalk', speed=1.15, then='scared', expr='surprised'),
        k('C22.end', face=-160, turn=0.3),
        k('C23', to=[1.7, 0, 1.25], clip='walk', speed=1.4, faceEnd=-148, then='kneel', expr='worried'),
        k('C24', clip='stareCamera', expr='shocked')]),
  ],
  'props': [P('tm', 'ticketMachine', pos=[1.95, 0, 1.75], ry=-90, opts={'num': '042'}),
            P('ticket', 'documents', opts={'count': 1}, scale=0.4, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('C21:ticket-0.2', visible=True), k('C22', visible=False)]),
            P('cart', 'shoppingCart', visible=False, on={'actor': 'mec', 'joint': 'hips', 'offset': [0, -1.02, 0.78]}, keys=[k('C21.end+0.05', visible=True), k('C23', detach=True)]),
            P('cash', 'money', opts={'stacks': 6}, visible=False, on={'actor': 'cart', 'offset': [0, 0.55, 0.05]}, keys=[k('C21.end+0.05', visible=True)]),
            P('watch', 'stopwatch', scale=1.5, on={'actor': 'mec', 'hand': 'R'},
              keys=[k('C21', attach='mec', joint='hips', offset=[0.16, 0.02, -0.14]), k('C22:tomber', detach=True, fall=True, impact='glass', spinFall=6)],
              alt=[{'opts': {'broken': True}, 'at': 'C22:tomber+0.5', 'rot': [-1.5708, 0, 0.4]}, {'opts': {'broken': True, 'taped': True}, 'at': 'C23:scotch', 'rot': [-1.5708, 0, 0.4]}]),
            P('tape', 'tapeRoll', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('C23', visible=True)]),
            WM(anchor='sign', offset=[2.3, -0.95, 0.03])],
  'sfx': [{'at': 'C22:tomber+0.62', 'name': 'spring', 'vol': 0.5}, {'at': 'C23:scotch', 'name': 'paper', 'vol': 0.5}],
  'cams': [cam(0, ['mec', 'cliente'], 'fs', worldAngle=200, elev=10, allowBack=True),
           cam('C20:braqué', 'mec', 'cu', angle=15),
           cam('C21', 'mec', 'fs', angle=40, move='track'), cam('C21:ticket', ['mec', 'tm'], 'ms', worldAngle=-60),
           cam('C21.end+0.05', 'mec', 'ms', angle=30, move='track'),
           cam('C22', 'mec', 'fs', angle=-30, move='track'), cam('C22:tomber-0.1', 'mec', 'mls', angle=160, elev=10, allowBack=True),
           cam('C22:tomber+0.55', 'watch', 'ecu', angle=0, elev=45),
           cam('C23', 'mec', 'ms', angle=20), cam('C23:scotch', 'watch', 'cu', worldAngle=200, elev=45),
           cam('C24', ['mec', 'vigile', 'cliente', 'guichetier'], 'fs', worldAngle=10, elev=12)],
  'tail': 0.8,
})

# ---------------------------------------------------------------- 7. la rue : au secours ; les flics
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': None, 'music': None,
  'freeze': {'at': 0, 'except': ['mec', 'cart', 'cash', 'billets']},
  'lines': [L('C25', "Au secours ! Aidez-moi !", 'mec', highlight=['secours']),
            L('C26', "Il est allé se rendre aux flics. Ils étaient figés en plein contrôle au faciès d'un mec qui attendait le bus.", highlight=['flics.', 'faciès']),
            L('C27', "Lui, avec son caddie de billets, ils l'ont même pas regardé.", highlight=['même', 'regardé.'])],
  'actors': [
    act('passant', [-1.4, 0, 0.9], 90, 'walk', 'neutral', params={'freq': 1.7}),
    act('pigeon', [-0.6, 2.4, 0.2], 90, 'fly', 'neutral'),
    act('busguy', [2.9, 0, -0.75], 0, 'stand', 'unimpressed'),
    act('flic1', [2.35, 0, 0.15], 150, 'holdOut', 'suspicious'),
    act('flic2', [3.55, 0, 0.25], -150, 'handsOnHips', 'suspicious'),
    act('mec', [-4.2, 0, 1.4], 90, 'idle', 'scared', keys=[
        k(0.05, to=[-1.9, 0, 1.1], clip='pushCartWalk', speed=2.0, then='yell'),
        k('C25#2', clip='waveFace', expr='scared', face='passant'),
        k('C26', path=[[0.2, 0, 1.6], [1.5, 0, 1.9]], clip='pushCartWalk', speed=1.3, faceEnd='flic1', then='surrender', expr='sad'),
        k('C27', clip='waveFace', expr='angry', face='flic1'),
        k('C27:regardé', clip='bigShrug', expr='unimpressed', face=20)]),
  ],
  'props': [P('stop', 'busStop', pos=[2.9, 0, -1.2]),
            P('idcard', 'idCard', scale=1.4, on={'actor': 'flic1', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}),
            P('briefcase', 'briefcase', on={'actor': 'busguy', 'hand': 'R'}),
            P('cart', 'shoppingCart', on={'actor': 'mec', 'joint': 'hips', 'offset': [0, -1.02, 0.78]}),
            P('cash', 'money', opts={'stacks': 6}, on={'actor': 'cart', 'offset': [0, 0.55, 0.05]}),
            P('billets', 'money', opts={'stacks': 1}, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('C27', visible=True)]),
            WM(pos=[-5.2, 0, -1.3], opts={'kind': 'stand'})],
  'cams': [cam(0, 'mec', 'fs', angle=40, move='track'), cam('C25', 'mec', 'mcu', angle=15),
           cam('C25#2', ['mec', 'passant'], 'ms', worldAngle=20),
           cam('C26', 'mec', 'fs', angle=60, move='track'), cam('C26:figés', ['flic1', 'busguy', 'flic2'], 'fs', worldAngle=10, elev=6),
           cam('C26:faciès', ots=['flic1', 'busguy', 1]), cam('C26:bus', 'busguy', 'cu', angle=0),
           cam('C27', ['mec', 'flic1'], 'ms', worldAngle=205), cam('C27:billets', 'flic1', 'cu', angle=0),
           cam('C27:regardé', ['mec', 'flic1', 'busguy', 'flic2'], 'fs', worldAngle=15, elev=8)],
  'tail': 0.6,
})

# ---------------------------------------------------------------- 8. dix mille ans plus tard : l'addition
AUD = [('flic1', [2.6, 0, 0.9], -120, 'holdOut', 'suspicious'), ('flic2', [3.4, 0, 0.2], -100, 'handsOnHips', 'suspicious'),
       ('busguy', [1.7, 0, 1.6], -150, 'stand', 'unimpressed'), ('cliente', [3.6, 0, 1.6], -110, 'walk', 'neutral'),
       ('vigile', [0.6, 0, 1.9], 170, 'yawnStretch', 'sleepy'), ('guichetier', [4.2, 0, -0.6], -95, 'giveItem', 'neutral')]
scenes.append({
  'id': 'fin', 'set': 'bar', 'ambience': None, 'music': None, 'lighting': 'interior',
  'freeze': {'at': 0, 'except': ['mec', 'beard']},
  'lines': [L('C28', "Dix mille ans plus tard, il est retourné chez Jo.", highlight=['Dix', 'mille', 'ans']),
            L('C29', "Bon… je vous raconte le match ?", 'mec', pre=0.4, highlight=['match']),
            L('C30', "Pour la première fois, personne ne s'est barré.", highlight=['personne']),
            L('C31', "Par contre, il avait toujours pas payé l'addition.", highlight=["l'addition."], pre=0.4)],
  'actors': [
    act('jo', [1.25, 0, -2.6], 15, 'holdOut', 'angry'),
    *[act(i, p, r, c, e, params={'freq': 1.6} if c == 'walk' else {}) for i, p, r, c, e in AUD],
    act('mec', [-3.2, 0, 0.8], 90, 'idle', 'neutral', keys=[
        k(0.1, to=[1.5, STOOL_Y, -1.25], clip='walk', speed=1.2, faceEnd='flic1', then='sitTalk'),
        k('C29', clip='sitTalk', expr='happy'), k('C30', clip='sitTalk', speed=1.6),
        k('C31', clip='sit', expr='unimpressed', look='jo')]),
  ],
  'props': [P('beard', 'beard', opts={'color': '#E8E4DA'}, scale=3.2, on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.06, 0.1]}),
            P('bill', 'bill', opts={'items': [['1 demi', '4,50'], ['3 bières retournées', '13,50']], 'total': '18,00 €'}, scale=1.8, on={'actor': 'jo', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}),
            P('idcard', 'idCard', scale=1.4, on={'actor': 'flic1', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}), P('briefcase', 'briefcase', on={'actor': 'busguy', 'hand': 'R'}),
            P('books', 'bookStack', pos=[-1.1, 0, -0.85], opts={'n': 46}), P('books2', 'bookStack', pos=[-1.6, 0, -0.6], opts={'n': 30, 'seed': 9}),
            P('tally', 'tallyBoard', pos=[-3.6, 1.7, -3.52], opts={'w': 2.4, 'h': 1.3})],
  'cams': [cam(0, 'mec', 'fs', worldAngle=60, move='track'), cam('C28:retourné', ['mec', 'jo', 'books'], 'fs', worldAngle=-20, elev=8),
           cam('C29', 'mec', 'cu', angle=20), cam('C29:match', ots=['flic1', 'mec', 1]),
           cam('C30', ['mec', 'flic1', 'flic2', 'busguy', 'cliente', 'vigile'], 'fs', worldAngle=10, elev=12, move='push', amount=0.06),
           cam('C31', 'jo', 'ms', angle=-10), cam('C31:addition', 'bill', 'ms', worldAngle=10, noOcclusion=True, move='push', amount=0.06, zoom=1.5, compose=0.17)],
  'tail': 1.8,
})

ep = {
  'version': 3, 'title': 'Le chrono', 'captionWords': 3, 'captionY': 0.66,
  'voice': {'name': 'allan tiktok', 'model': 'eleven_v4',
            'narrator': {'stability': 0.8, 'style': 0.0, 'rate': 1.07},
            'character': {'stability': 0.4, 'style': 0.4, 'rate': 1.02}},
  'music': {'mood': 'quirky', 'vol': 0.06},
  'cast': {
    'mec': {'preset': 'lemec'}, 'coll1': {'preset': 'lemec_glasses'}, 'coll2': {'preset': 'madame'},
    'patron': {'preset': 'boss', 'facial': 'none'},
    'vieux': {'preset': 'lemec_beige', 'hair': 'receding', 'hairColor': '#D8D8D8', 'facial': 'beard', 'beardColor': '215,215,210', 'redNose': True, 'build': {'height': 0.92}},
    'jo': {'preset': 'serveur'}, 'client1': {'preset': 'fermier'}, 'client2': {'preset': 'mamie'},
    'guichetier': {'preset': 'lemec_charcoal'}, 'vigile': {'preset': 'swat'}, 'cliente': {'preset': 'madame', 'seed': 9},
    'passant': {'preset': 'tourist'}, 'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 2}},
    'flic1': {'preset': 'cop'}, 'flic2': {'preset': 'cop2', 'seed': 41},
    'busguy': {'preset': 'lemec_charcoal', 'skin': '#6B4A33', 'hair': 'buzz', 'facial': 'none', 'glasses': True, 'tie': '#2C4A8A', 'seed': 17},
  },
  'scenes': scenes,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrono4.json')
json.dump(ep, open(out, 'w'), ensure_ascii=False, indent=1)
words = sum(len(l['text'].split()) for s in scenes for l in s['lines'])
print(out, len(scenes), 'scenes,', sum(len(s['lines']) for s in scenes), 'lines,', words, 'words,', sum(len(s['cams']) for s in scenes), 'camera setups')
