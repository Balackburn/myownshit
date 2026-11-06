#!/usr/bin/env python3
"""Les chaussettes (story 36): this man lost a sock in the washing machine, so he crawled in to look for it. At the bottom of the drum lay every
lost sock in the world: they had founded a kingdom, and the queen was his sock. He asked her to come home; she refused — at his place she was
« à ses pieds » (at his feet: worn, and at his service). The next day the other sock left too, leaving a note (« JE REJOINS MA MOITIÉ »).
Since then he lives barefoot. Natural look (engine/look.js)."""
from story_kit import *

st = Story('chaussettes', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L02', 0), ('S03b', 'L02', 5), ('S04', 'L03', 0), ('S05', 'L03', 7), ('S06', 'L04', 0), ('S07', 'L05', 0),
         ('S08', 'L05', 3), ('S08b', 'L05', 5), ('S09', 'L06', 0), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L10', 0), ('S14', 'L11', 0), ('S15', 22.5, 0)])

RED = ['#D9453A', '#F4F1E8', '#F4F1E8']                          # his socks: red, white stripes, white toe (prop colours)
REDC = {'body': '#D9453A', 'stripe': '#F4F1E8', 'toe': '#F4F1E8', 'cuff': '#F4F1E8'}   # the same, for the sock creatures
WASH = [-1.2, 0, -2.98]                                          # the washing machine in the laundry room (porthole centre [-1.2, 0.8, -2.405])
SEAT = [0, 0.7, -8.55]                                           # the queen's seat on the throne (sockKingdom)
SOCK = lambda: P('chau', 'sockSingle', on={'actor': 'mec', 'hand': 'R'}, opts={'colors': RED})
HOME = {'tint': [0.95, 0.985, 1.06], 'warm': 0.55, 'sunColor': '#FFF0DC'}   # home: cooler whites (the critics found the first pass sepia)
CROWN = lambda who, s=0.62: P('crown_' + who, 'crown', on={'actor': who, 'joint': 'cuff', 'offset': [0, 0.1, 0]}, scale=s)
CROWD = [('sk1', [-1.5, 0, -2.5], 15, 'hop'), ('sk2', [0.3, 0, -3.2], 0, 'idle'), ('sk3', [2.4, 0, -2.0], -20, 'talk'), ('sk4', [-3.2, 0, -4.0], 25, 'idle'),
         ('sk5', [3.6, 0, -4.6], -25, 'hop'), ('sk6', [-0.8, 0, -5.5], 5, 'celebrate')]

# 1: the laundry room: one red sock in his hand, the clothes horse full of pairs, the machine open
st.shot('S01', 'laundryRoom', setOpts={'open': 1}, look=HOME, actors=[act('mec', [-0.15, 0, -1.6], -12, 'dangleItem', 'suspicious', keys=[k(0.7, expr='sad')])],
        props=[SOCK()],
        cams=[cam(0.0, [0.2, 1.95, 0.25], [0.08, 1.93, -0.32], [-0.38, 1.86, -1.6], [-0.38, 1.86, -1.6], lens=44, ease='out')])
# 2: from inside the drum: his face peering in, framed by the porthole
st.shot('S02', 'laundryRoom', setOpts={'open': 1}, look=HOME, actors=[act('mec', [-1.2, 0, -1.6], 180, 'peerIn', 'suspicious')],
        cams=[cam(0.0, [-1.2, 0.82, -2.8], [-1.2, 0.83, -2.75], [-1.2, 1.3, -1.95], [-1.2, 1.31, -1.95], lens=50)])
# 3: he crawls in head first (squeezing in), the machine wobbles
st.shot('S03', 'laundryRoom', setOpts={'washer': False}, look=HOME, actors=[act('mec', [-1.2, -0.35, -1.9], 180, 'diveIn', 'determined',
        keys=[k(0.0, to=[-1.2, -0.35, -3.7], dur=1.0, glide=True), k(1.0, visible=False)])],
        props=[P('washer', 'bigWasher', pos=WASH, opts={'open': 1})],
        cams=[cam(0.0, [-0.45, 1.25, -0.2], [-0.5, 1.2, -0.35], [-1.2, 0.75, -2.5], [-1.2, 0.75, -2.5], lens=44)])
st.shot('S03b', 'laundryRoom', setOpts={'washer': False}, look=HOME, props=[P('washer', 'bigWasher', pos=WASH, opts={'open': 1, 'closeAt': 0.12, 'shakeAt': [0.45, 0.7], 'spinAt': 0.5})],
        cams=[cam(0.0, [-0.9, 1.15, 0.2], [-0.95, 1.1, 0.05], [-1.2, 0.85, -2.4], [-1.2, 0.85, -2.4], lens=44)])
# 4: inside the drum: a perforated steel tunnel, socks drifting, a light at the end
st.shot('S04', 'drumTunnel', actors=[act('mec', [0, 0, 5.5], 180, 'walk', 'surprised', keys=[k(0.0, to=[0, 0, 2.0], dur=st.dur('S04') + 0.2)])],
        cams=[cam(0.0, [0.4, 1.0, 8.2], [0.35, 1.05, 7.6], [0, 1.3, -10], [0, 1.3, -10], lens=44)])
# 5: the reveal: every lost sock in the world, sock people turning to look at him, the castle far off, the porthole in the sky
st.shot('S05', 'sockKingdom', setOpts={'castle': False, 'crowd': 260, 'crowdFace': [1.2, 9]}, actors=[act('mec', [1.2, 0, 2.6], 200, 'stand', 'shocked'), act('sk1', [-0.4, 0, 0.6], 25, 'hop'), act('sk3', [2.6, 0, 0.9], -20, 'talk')],
        cams=[cam(0.0, [2.6, 3.6, 7.0], [2.4, 3.4, 6.4], [0, 1.0, -8], [0, 0.9, -8.5], lens=44)])
# 6: the kingdom: the laundry-basket castle, washing-powder towers, the sock banner, guards at the gate, the queen on her throne
st.shot('S06', 'sockKingdom', actors=[act('sk7', [-1.0, 0, -10.6], 0, 'idle'), act('sk8', [1.0, 0, -10.6], 0, 'idle'), act('reine', SEAT, 0, 'idle', 'smug')],
        props=[CROWN('reine')],
        cams=[cam(0.0, [0.7, 1.15, -4.4], [0.6, 1.2, -4.9], [0, 2.7, -12.5], [0, 2.75, -12.5], lens=44)])
# 7: the queen, crowned, on the throne; courtiers bow; he stands before her
st.shot('S07', 'sockKingdom', actors=[act('reine', SEAT, 0, 'idle', 'smug'), act('sk1', [-0.48, 0, -7.8], 45, 'bow'), act('sk2', [0.48, 0, -7.8], -45, 'bow'), act('sk4', [-0.62, 0, -8.35], 70, 'bow')],
        props=[CROWN('reine')],
        cams=[cam(0.0, [0.05, 1.35, -5.2], [0.05, 1.35, -5.5], [0, 1.0, -8.3], [0, 1.0, -8.3], lens=44)])
# 8: the match: he holds up his red sock — the same stripes as the queen
st.shot('S08', 'sockKingdom', actors=[act('mec', [0.3, 0, -7.25], 180, 'dangleItem', 'shocked'), act('reine', SEAT, 0, 'idle', 'surprised')],
        props=[SOCK(), CROWN('reine')],
        cams=[cam(0.0, [-1.05, 1.5, -9.35], [-1.0, 1.5, -9.25], [0.15, 1.72, -7.25], [0.15, 1.73, -7.25], lens=44)])
st.shot('S08b', 'sockKingdom', actors=[act('mec', [0.3, 0, -7.35], 190, 'showPhone', 'shocked'), act('reine', SEAT, 0, 'idle', 'surprised')],
        props=[SOCK(), CROWN('reine')],
        cams=[cam(0.0, [1.75, 1.45, -7.85], [1.65, 1.45, -7.9], [0.08, 1.35, -8.38], [0.08, 1.35, -8.38], lens=44)])
# 9: on his knees, offering the sock: come home
st.shot('S09', 'sockKingdom', actors=[act('mec', [0.25, 0, -7.25], 180, 'kneelGive', 'sad'), act('reine', SEAT, 0, 'idle', 'suspicious')],
        props=[SOCK(), CROWN('reine')],
        cams=[cam(0.0, [-0.65, 0.75, -8.3], [-0.58, 0.8, -8.05], [0.25, 1.25, -7.25], [0.25, 1.27, -7.25], lens=44)])
# 10: she refuses: turns away, nose in the air
st.shot('S10', 'sockKingdom', actors=[act('reine', SEAT, 0, 'idle', 'smug', keys=[k(0.1, clip='refuse')])],
        props=[CROWN('reine')],
        cams=[cam(0.0, [0.45, 1.45, -6.9], [0.4, 1.45, -7.05], [0, 1.3, -8.55], [0, 1.3, -8.55], lens=44)])
# 11: what life at his place was: a huge bare foot coming down into her (the sock's view), stink lines
st.shot('S11', 'laundryRoom', setOpts={'open': 0}, look=HOME, actors=[act('reineH', [0.4, 0, -1.3], 0, 'idle', 'scared', keys=[k(0.55, clip='angry', expr='shocked')])],
        props=[P('pied', 'giantFoot', pos=[0.4, 2.6, -1.6], opts={'size': 0.8}, keys=[k(0.15, to=[0.4, 1.07, -1.6], dur=0.55, ease='in')]),
               P('stink', 'stinkLines', pos=[0.4, 1.15, -1.25], opts={'n': 4, 'w': 0.45, 'h': 0.6, 'at': 0.4})],
        cams=[cam(0.0, [1.3, 0.62, -0.45], [1.27, 0.6, -0.52], [0.4, 0.66, -1.35], [0.4, 0.66, -1.35], lens=50)])
# 12: the next day: the other sock hops to the machine with a bindle and dives in
st.shot('S12', 'laundryRoom', setOpts={'open': 1}, look=HOME, actors=[act('jumelle', [0.9, 0, -1.2], -100, 'idle', 'determined',
        keys=[k(0.15, to=[-1.0, 0, -1.9], dur=1.2, clip='hop'), k(1.4, to=[-1.2, 0.4, -2.45], dur=0.3, clip='hop'), k(1.7, to=[-1.2, 0.4, -2.95], dur=0.25, glide=True), k(1.95, visible=False)])],
        props=[P('bindle', 'bindle', on={'actor': 'jumelle', 'joint': 'cuff', 'offset': [0.0, 0.08, 0.0], 'rot': [0, 0, 0.7]})],
        cams=[cam(0.0, [0.55, 1.15, 0.5], [0.45, 1.1, 0.3], [-0.55, 0.55, -2.1], [-0.55, 0.55, -2.1], lens=44)])
# 13: a note taped on the porthole: « JE REJOINS MA MOITIÉ »
st.shot('S13', 'laundryRoom', setOpts={'washer': False}, look=HOME, props=[P('washer', 'bigWasher', pos=WASH, opts={'note': 'JE REJOINS|MA MOITIÉ'})],
        cams=[cam(0.0, [-1.06, 1.08, -1.5], [-1.06, 1.07, -1.68], [-1.08, 1.05, -2.3], [-1.08, 1.05, -2.3], lens=44, ease='out')])
# 14: since then he lives barefoot: from his sad face down to his bare toes on « pieds nus »
st.shot('S14', 'laundryRoom', setOpts={'open': 0}, look=HOME, actors=[act('mecPN', [-0.2, 0, -1.4], 10, 'slump', 'sad')],
        cams=[cam(0.0, [0.3, 1.6, 0.9], [0.3, 0.3, 0.45], [-0.2, 1.75, -1.4], [-0.2, 0.12, -1.4], lens=44, ease='inOut'), cam(1.07, [0.3, 0.3, 0.45], [0.3, 0.3, 0.4], [-0.2, 0.12, -1.4], [-0.2, 0.12, -1.4], lens=44)])
# 15: tail: in the kingdom, the pair reunited on the throne, both crowned, jumping for joy
st.shot('S15', 'sockKingdom', actors=[act('reine', [-0.15, 0.7, -8.55], 28, 'idle', 'closed'), act('jumelle', [0.15, 0.7, -8.55], -28, 'idle', 'closed')],
        props=[CROWN('reine'), CROWN('jumelle', 0.55), P('coeur', 'heartPop', pos=[0, 1.72, -8.45], opts={'at': 0.25, 'size': 0.2})],
        cams=[cam(0.0, [0.9, 1.3, -6.2], [0.8, 1.3, -6.5], [0, 1.0, -8.55], [0, 1.0, -8.55], lens=44)])

st.card('S06', 'LE ROYAUME'); st.card('S12', 'LE LENDEMAIN')
st.cue('whoosh', 'S01', 0.0, 0.12, 1.6, 300, 1200); st.cue('sfx:grunt', 'S03', 0.1, 0.3); st.cue('thud', 'S03b', 0.15, 0.5); st.cue('engine', 'S03b', 0.5, 0.18, 0.5); st.cue('whoosh', 'S04', 0.1, 0.3, 1.3, 200, 900)
st.cue('sfx:choir', 'S05', 0.1, 0.22); st.cue('sfx:fanfare', 'S06', 0.1, 0.22); st.cue('sfx:gasp', 'S08', 0.1, 0.35); st.cue('sfx:poof', 'S10', 0.15, 0.25)
st.cue('sfx:squeak', 'S11', 0.68, 0.35); st.cue('thud', 'S11', 0.72, 0.4); st.cue('sfx:boing', 'S12', 0.3, 0.2); st.cue('sfx:boing', 'S12', 0.75, 0.2); st.cue('sfx:boing', 'S12', 1.2, 0.2)
st.cue('whoosh', 'S12', 1.55, 0.25, 0.6, 400, 1600); st.cue('sfx:paper', 'S13', 0.1, 0.35); st.cue('sfx:sniff', 'S14', 0.5, 0.3); st.cue('sfx:fanfare', 'S15', 0.05, 0.18)
SK = lambda seed, b, s, t, c: {'type': 'creature', 'name': 'sock', 'opts': {'seed': seed, 'colors': {'body': b, 'stripe': s, 'toe': t, 'cuff': c}}}
st.write('Les chaussettes', {'mecPN': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'barefoot': True},
                             'reine': {'type': 'creature', 'name': 'sock', 'opts': {'seed': 3, 'colors': REDC, 'scale': 1.15}},
                             'reineH': {'type': 'creature', 'name': 'sock', 'opts': {'seed': 3, 'colors': REDC}},
                             'jumelle': {'type': 'creature', 'name': 'sock', 'opts': {'seed': 4, 'colors': REDC}},
                             'sk1': SK(11, '#2F5E8C', '#F2C94C', '#F2C94C', '#F2C94C'), 'sk2': SK(12, '#4CA36C', '#F4F1E8', '#2C6E4A', '#F4F1E8'),
                             'sk3': SK(13, '#F2C94C', '#E0413A', '#E0413A', '#E0413A'), 'sk4': SK(14, '#8E5BB5', '#F4F1E8', '#F4F1E8', '#F4F1E8'),
                             'sk5': SK(15, '#E8879E', '#F4F1E8', '#C8322A', '#F4F1E8'), 'sk6': SK(16, '#F4F1E8', '#2C3E66', '#2C3E66', '#2C3E66'),
                             'sk7': SK(17, '#3A3D44', '#C9CCD1', '#C9CCD1', '#C9CCD1'), 'sk8': SK(18, '#E07A2E', '#2F5E8C', '#2F5E8C', '#2F5E8C')})
