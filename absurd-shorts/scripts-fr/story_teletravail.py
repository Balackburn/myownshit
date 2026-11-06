#!/usr/bin/env python3
"""Le télétravail: this man put his dog in remote work. The dog did all the meetings, answered "woof" to every question;
the bosses heard "yes". Promoted, then team leader: of the man's team. Now the dog walks him twice a day; he fetches the
files; annual review: "good boy"; end-of-year bonus: a bone. Yesterday he asked for a raise. The dog said "sit". He sat.
He got a sugar cube."""
from story_kit import *

st = Story('teletravail')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0), ('S08', 'L07', 0),
         ('S09', 'L08', 0), ('S10', 'L08', 7), ('S11', 'L09', 0), ('S12', 'L10', 0), ('S13', 'L11', 0), ('S14', 'L12', 0), ('S15', 'L13', 0), ('S16', 'L14', 0), ('S17', 'L15', 0)])
PI = math.pi
DOGS = 1.45                                   # the dog, upright, scaled to a small adult
TIE = lambda aid='chien': P(f'tie_{aid}', 'necktie', on={'actor': aid, 'joint': 'torso', 'offset': [0, 0.4, 0.12]}, opts={'len': 0.24})
DESK = lambda z=-1.4, x=0.0, tag=None: [P('desk', 'desk', pos=[x, 0, z]), P('chair', 'chair', pos=[x, 0, z - 0.55], opts={'color': '#3A3D44'})] + \
    ([P('tag', 'noticeBoard', pos=[x + 0.15, 0.84, z + 0.42], opts={'text': tag, 'style': 'tag', 'w': 0.46, 'h': 0.12})] if tag else [])
BUBBLE = lambda pid, text, pos, pop, tail='left', w=0.7, ry=0: P(pid, 'speechBubble', pos=pos, ry=ry, opts={'text': text, 'popAt': pop, 'tail': tail, 'w': w, 'h': w * 0.5})
COLLAR = P('collar', 'collar', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.66, 0.0]}, opts={'text': 'MEC'}, scale=1.6)

# 1-4: the dog works from home: meetings, "woof"
st.shot('S01', 'livingRoom', actors=[act('chien', [0.0, 0, -1.95], 0, 'sit', 'happy', scale=DOGS), act('mec', [0.75, 0, -1.55], -40, 'present', 'happy')],
        props=DESK() + [TIE(), P('lap', 'laptop', pos=[0, 0.75, -1.3], ry=180, opts={'text': 'RÉUNION\n9H00', 'bg': '#DCE8F2', 'fg': '#2C4A8A'})],
        cams=[cam(0.0, [0.5, 1.6, 2.4], [0.48, 1.6, 2.15], [0.32, 1.38, -1.7], [0.32, 1.38, -1.7], lens=44)])
st.shot('S02', 'livingRoom', actors=[act('chien', [0.0, 0, -1.95], 0, 'sitWrite', 'neutral', scale=DOGS)], props=DESK() + [TIE(), P('lap', 'laptop', pos=[0, 0.75, -1.3], ry=180)],
        cams=[cam(0.0, [0.3, 1.4, 0.35], [0.28, 1.4, 0.15], [0.0, 1.25, -1.95], [0.0, 1.25, -1.95], lens=44)])
st.shot('S03', 'livingRoom', props=DESK() + [P('grid', 'callGrid', pos=[0, 1.05, -1.3], opts={'w': 0.42})],
        cams=[cam(0.0, [0.02, 1.0, -0.2], [0.02, 1.0, -0.3], [0.0, 1.0, -1.3], [0.0, 1.0, -1.3], lens=44)])
st.shot('S04', 'livingRoom', actors=[act('chien', [0.0, 0, -1.95], 0, 'sitTalk', 'happy', scale=DOGS)], props=DESK() + [TIE(), BUBBLE('w', 'WOUF !', [0.36, 1.95, -1.7], 0.25, 'left', 0.5)],
        cams=[cam(0.0, [0.2, 1.65, 0.5], [0.19, 1.65, 0.3], [0.05, 1.62, -1.95], [0.05, 1.62, -1.95], lens=44, shake=0.004)])
# 5-8: the bosses hear "yes": promoted, team leader, of the man's team
st.shot('S05', 'office', setOpts={'door': False}, actors=[act('boss1', [-0.4, 0, -0.9], 15, 'nod', 'happy'), act('boss2', [0.45, 0, -0.95], -15, 'present', 'happy')],
        props=[BUBBLE('oui', 'OUI !', [-0.45, 2.68, -0.9], 0.3, 'down', 0.5), BUBBLE('oui2', 'OUI !', [0.5, 2.66, -0.95], 0.6, 'down', 0.5)],
        cams=[cam(0.0, [0.05, 1.6, 2.6], [0.05, 1.6, 2.35], [0.0, 1.55, -0.9], [0.0, 1.55, -0.9], lens=44)])
st.shot('S06', 'office', setOpts={'door': False}, actors=[act('chien', [0.0, 0, -1.95], 0, 'sit', 'happy', scale=DOGS)],
        props=DESK(tag='MANAGER') + [TIE()],
        cams=[cam(0.0, [0.35, 1.3, 1.1], [0.33, 1.3, 0.85], [0.0, 1.32, -1.7], [0.0, 1.32, -1.7], lens=44)])
TAB = [P('mt', 'table', pos=[0, 0, -0.8], opts={'w': 0.9, 'd': 2.2, 'h': 0.74, 'color': '#C99A62'})] + [P(f'mc{i}', 'chair', pos=[x, 0, z], ry=r, opts={'color': '#2F62B5'}) for i, (x, z, r) in enumerate(((-0.75, -0.3, 90), (-0.75, -1.2, 90), (0.75, -0.3, -90), (0.75, -1.2, -90)))]
TEAM = lambda e='neutral': [act('emp1', [-0.75, 0, -1.2], 90, 'sit', 'neutral'), act('emp2', [0.75, 0, -1.2], -90, 'sit', 'neutral'), act('emp3', [0.75, 0, -0.3], -90, 'sit', 'neutral'), act('mec', [-0.75, 0, -0.3], 90, 'sit', e)]
st.shot('S07', 'office', setOpts={'door': False}, actors=TEAM() + [act('chien', [0.0, 0, -2.2], 0, 'point', 'smug', scale=DOGS)],
        props=TAB + [TIE(), P('chf', 'noticeBoard', pos=[0, 2.28, -2.3], opts={'text': "CHEF D'ÉQUIPE", 'style': 'sign', 'w': 0.9, 'h': 0.22, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'})],
        cams=[cam(0.0, [0.1, 1.8, 2.4], [0.1, 1.78, 2.15], [0.0, 1.45, -1.1], [0.0, 1.45, -1.1], lens=44)])
st.shot('S08', 'office', setOpts={'door': False}, actors=TEAM('shocked') + [act('chien', [0.0, 0, -2.2], 0, 'point', 'smug', scale=DOGS)], props=TAB + [TIE()],
        cams=[cam(0.0, [0.55, 1.5, 0.55], [0.5, 1.5, 0.4], [-0.75, 1.42, -0.3], [-0.75, 1.42, -0.3], lens=44, shake=0.005)])
# 9-10: now the dog walks him, twice a day
D9, D10 = st.dur('S09'), st.dur('S10')
WALK = lambda x0, x1, z, d: [act('chien', [x0, 0, z], 90, 'stand', 'happy', scale=DOGS, keys=[k(0.0, to=[x1, 0, z], dur=d, clip='walk', face='keep')]),
                             act('mec', [x0 - 1.15, 0, z + 0.05], 90, 'stand', 'unimpressed', keys=[k(0.0, to=[x1 - 1.15, 0, z + 0.05], dur=d, clip='walk', face='keep')])]
LEASH = [{'a': {'actor': 'chien', 'hand': 'R', 'offset': [0, -0.05, 0]}, 'b': {'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.66, 0.1]}, 'color': '#C8322A', 'radius': 0.012, 'sag': 0.15}]
st.shot('S09', 'parisStreet', actors=WALK(-1.0, 1.4, 6.0, D9), props=[TIE(), COLLAR], tethers=LEASH,
        cams=[cam(0.0, [3.2, 1.45, 10.4], [4.6, 1.45, 10.2], [-0.2, 1.15, 6.0], [1.2, 1.15, 6.0], lens=44)])
st.shot('S10', 'park', actors=WALK(-0.8, 0.9, 0.0, D10), props=[TIE(), COLLAR], tethers=LEASH,
        cams=[cam(0.0, [2.6, 1.0, 2.6], [2.8, 1.0, 2.3], [-0.2, 1.2, 0.0], [0.4, 1.2, 0.0], lens=44)])
# 11-13: he fetches the files; annual review "good boy"; the bonus is a bone (the boss desk turned side-on: the dog at its left, him at its right, both cheated 3/4)
st.shot('S11', 'office', setOpts={'door': False}, actors=[act('chien', [-0.9, 0, -1.6], 60, 'raiseOverhead', 'happy', scale=DOGS), act('mec', [0.9, 0, -0.6], -110, 'stand', 'happy', keys=[k(0.35, to=[-0.4, 0, -1.1], dur=0.7, clip='run', then='giveItem')])],
        props=[TIE(), P('fold', 'folderDoc', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.08, 0.17], 'rot': [-1.4, 0, 0]}, scale=1.6, opts={'text': 'DOSSIER', 'color': '#F2A33A'})],
        cams=[cam(0.0, [-0.3, 1.45, 3.0], [-0.3, 1.45, 2.7], [-0.2, 1.2, -1.1], [-0.35, 1.2, -1.2], lens=44)])
BD = [P('desk', 'desk', pos=[0.0, 0, -1.4], ry=90), P('chair', 'chair', pos=[-0.55, 0, -1.4], ry=90, opts={'color': '#3A3D44'}),
      P('tag', 'noticeBoard', pos=[0.42, 0.84, -1.28], ry=90, opts={'text': 'MANAGER', 'style': 'tag', 'w': 0.46, 'h': 0.12})]
DOGD = lambda clip='sit', expr='smug', keys=None: act('chien', [-0.55, 0, -1.4], 70, clip, expr, scale=DOGS, keys=keys)
TWO = lambda: [cam(0.0, [0.4, 1.5, 2.9], [0.39, 1.5, 2.65], [0.15, 1.25, -1.35], [0.15, 1.25, -1.35], lens=44)]
st.shot('S12', 'office', setOpts={'door': False}, actors=[DOGD('sitTalk', 'smug'), act('mec', [0.75, 0, -1.3], -50, 'sit', 'happy')],
        props=BD + [TIE(), P('mch', 'chair', pos=[0.75, 0, -1.3], ry=-50, opts={'color': '#2F62B5'}), BUBBLE('bg', 'BON GARÇON !', [-0.35, 2.2, -1.4], 0.35, 'down', 0.9)], cams=TWO())
st.shot('S13', 'office', setOpts={'door': False}, actors=[act('mec', [0.0, 0, -1.2], 0, 'lookDown', 'unimpressed', keys=[k(0.9, expr='sad')])],
        props=[P('t', 'table', pos=[0, 0, -0.75], opts={'w': 0.8, 'd': 0.6, 'h': 0.74, 'color': '#C99A62'}), P('gift', 'giftBone', pos=[0, 0.74, -0.7], opts={'openAt': 0.3})],
        cams=[cam(0.0, [0.3, 1.9, 1.75], [0.29, 1.88, 1.55], [0.0, 1.32, -0.95], [0.0, 1.32, -0.95], lens=44)])
# 14-17: he asks for a raise; "sit"; he sits; he gets a sugar cube
st.shot('S14', 'office', setOpts={'door': False}, actors=[DOGD('sit', 'unimpressed'), act('mec', [0.8, 0, -1.25], -45, 'explain', 'worried')], props=BD + [TIE()], cams=TWO())
st.shot('S15', 'office', setOpts={'door': False}, actors=[act('chien', [0.25, 0, -0.75], 28, 'commandSit', 'angry', scale=DOGS)], props=BD + [TIE()],
        cams=[cam(0.0, [1.35, 0.8, 1.35], [1.3, 0.78, 1.25], [0.3, 1.55, -0.8], [0.3, 1.55, -0.8], lens=44, shake=0.005)])
st.shot('S16', 'office', setOpts={'door': False}, actors=[DOGD('sit', 'smug'), act('mec', [0.8, 0, -1.25], -35, 'stand', 'neutral', keys=[k(0.15, clip='sitFloor', expr='neutral')])], props=BD + [TIE()],
        cams=[cam(0.0, [1.6, 3.0, 0.9], [1.55, 2.95, 0.8], [0.6, 0.6, -1.2], [0.6, 0.55, -1.2], lens=44)])
st.shot('S17', 'office', setOpts={'door': False}, actors=[act('chien', [0.15, 0, -1.65], 40, 'feedTreat', 'happy', scale=DOGS), act('mec', [0.8, 0, -1.25], -35, 'sitFloor', 'neutral', keys=[k(st.at('S17', 'L15', 4) + 0.05, expr='happy')])],
        props=BD + [TIE(), P('sugar', 'sugarCube', on={'actor': 'chien', 'hand': 'R', 'offset': [0, -0.12, 0.05]}, scale=4.2, keys=[k(st.at('S17', 'L15', 4) + 0.05, visible=False)])],
        cams=[cam(0.0, [-0.1, 1.25, 0.45], [-0.08, 1.24, 0.35], [0.6, 1.08, -1.3], [0.6, 1.08, -1.3], lens=44)])
st.card('S06', 'PROMU'); st.card('S15', 'ASSIS')
st.cue('pop', 'S04', 0.25, 0.4); st.cue('pop', 'S05', 0.3, 0.35); st.cue('pop', 'S05', 0.6, 0.35); st.cue('sfx:fanfare', 'S06', 0.1, 0.3); st.cue('sfx:step', 'S09', 0.2, 0.3)
st.cue('whoosh', 'S11', 0.3, 0.4); st.cue('pop', 'S12', 0.35, 0.35); st.cue('sfx:ding', 'S13', 0.3, 0.35); st.cue('pop', 'S15', 0.2, 0.45); st.cue('thud', 'S16', 0.4, 0.4); st.cue('sfx:clink', 'S17', st.at('S17', 'L15', 4) + 0.05, 0.35)
st.write('Le télétravail', {'chien': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 4, 'upright': True}},
                            'boss1': {'preset': 'boss', 'seed': 51}, 'boss2': {'preset': 'madame', 'seed': 52, 'glasses': True},
                            'emp1': {'preset': 'politique', 'seed': 53}, 'emp2': {'preset': 'madame', 'seed': 54}, 'emp3': {'preset': 'prefet', 'seed': 55}})
