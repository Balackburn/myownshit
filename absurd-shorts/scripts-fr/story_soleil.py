#!/usr/bin/env python3
"""Le coup de soleil (story 62, cycle 24 of the cartoon staging): this man got sunburnt. He turned bright red. At night he lights up the whole
neighbourhood. The town hall installed him as a red light. The cars stop in front of him all day. Yesterday a lorry honked at him. He turned green with
fear. All the cars went through. The town hall painted him red again.
Staging: in a deckchair on a Paris pavement under a blazing cartoon sun he goes red like a thermometer filling (his hands, his neck, then his head),
steam puffing out of his ears; a boy cracks an egg on his forehead and it fries there. At night he glows red in the dark street, moths circling his
head, a neighbour reading her paper by his light. Two workers carry him stiff as a plank to a crossroads where the mayor points at a traffic light
with three empty holes; his face pops into the top hole, red. A queue of cars to the end of the street, stopped; the sun crosses the sky and goes
down behind him, he glows on. A lorry's horn blasts his face flat; he turns green, his face drops from the top hole to the bottom one; every car
shoots past. A painter on a ladder rolls him red again, stroke by stroke; the cars stop.
Natural look; cycle 24 tools: the skin channel of the rig (a colour that fills him from the hands to the head, a glow), props_soleil.js (deckChair,
friedEgg, moths, headLight, truck, glowLight)."""
from story_kit import *
import math

st = Story('soleil', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L04', 4), ('S06', 'L05', 0), ('S07', 'L05', 5),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def FLY(pts):
    """a flight through timed points [[t, x, y, z], ...] as prop keys in world space"""
    return {'pos': list(pts[0][1:]), 'keys': [k(pts[i][0], to=list(pts[i + 1][1:]), dur=round(pts[i + 1][0] - pts[i][0], 3), ease='linear') for i in range(len(pts) - 1)]}
DEAD = {'lid': 0.45}
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
STREET = {'eiffelStyle': 'v2', 'clear': [-16.0, 4.0]}                     # no tree or lamp on the right pavement where he sits or the light stands
RED = '#FF2A14'; GREEN = '#3FE04A'
SKIN = lambda col, k_=1.0, glow=0.0, fill=1.0: {'color': col, 'k': k_, 'glow': glow, 'fill': fill}   # (cycle 24) the skin channel

# 1: the hook. In a deckchair on the pavement, a blazing cartoon sun down the street: content, he basks; he goes red like a thermometer filling, his
#    hands, then his neck, then his whole head; steam puffs out of his ears; deadpan
D1 = st.dur('S01')
ME = [5.2, 0, -12.0]; RY = -60                                           # on the right pavement, turned to the road and down the street ((audit) at -90 the camera saw him in profile)
SEATED = [ME[0], -0.15, ME[2]]                                           # the deckchair's seat is lower than a chair's
LOUNGE = {'bend': {'spine': [-0.42, 0, 0, 1, None], 'neck': [0.12, 0, 0, 1, None]}}
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEATED, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'face': {'lid': 0.75, 'mouth': 'smile', 'cheeks': 0.4}}, toonDur=0.0),
            k(0.25, toon={**LOUNGE, 'skin': SKIN(RED, 0.6, 0.0, 0.4), 'face': {'lid': 0.7, 'mouth': 'smile', 'cheeks': 0.4}}, toonDur=0.18),   # his hands go red...
            k(0.6, toon={**LOUNGE, 'skin': SKIN(RED, 0.8, 0.0, 0.8), 'face': {'lid': 0.6, 'mouth': 'smile'}}, toonDur=0.18),   # ...his neck...
            k(0.95, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.1, 1.0), 'face': {'lid': 0.45, 'mouth': 'flat'}}, toonDur=0.14),   # ...his whole head, his smile gone...
            k(1.12, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15, 1.0), 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.45, 'mouth': 'flat', 'steam': 1.0}}, toonDur=0.06, toonEase='out'),   # ...steam puffs out of his ears
            k(1.45, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15, 1.0), 'face': {'lid': 0.45, 'mouth': 'flat', 'steam': 1.0}}, toonDur=0.15)])],
        props=[P('chair1', 'deckChair', pos=ME, ry=RY), P('sun1', 'sun', pos=[2.4, 4.4, -19.0], opts={'r': 1.1}, keys=[k(0.0, scale=1.0, dur=0.0), k(0.9, scale=1.12, dur=0.25, ease='inOut')])],   # (stills 1) nearer: in the corner of a closer frame
        cams=[FC(0.0, [4.0, 0.85, -10.4], [[r(ME[0] - 0.1), 1.5, ME[2]], [r(ME[0] + 0.3), 0.0, r(ME[2] + 0.4)], [r(ME[0] - 0.5), 0.6, ME[2]], [2.4, 5.3, -19.0]], top=0.08, bottom=0.8, drift=(0.0, 0.0, -0.08))])   # (stills 1) closer: his face reads as it goes red
st.cue('sfx:static', 'S01', 0.3, 0.12); st.cue('sfx:static', 'S01', 1.12, 0.22)

# 2: he turned bright red. Close on his red face: a boy beside the deckchair cracks an egg on his forehead; the egg fries there, bubbling, steam
#    rising; his eyes roll up to it, deadpan
D2 = st.dur('S02'); CRACK2 = 0.42
GAM2 = [4.7, 0, -12.85]                                                  # (stills 1) the neighbour at his side, her hand at his forehead height (the boy's arm stretched like a pole)
FORE2 = [r(ME[0] - 0.22), 1.32, ME[2]]                                   # his forehead, seated and leaning back
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEATED, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': DEAD}, toonDur=0.0),
            k(r(CRACK2 + 0.02), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 1.0}}, toonDur=0.03),   # CRAC: a blink...
            k(r(CRACK2 + 0.16), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {'lid': 0.3, 'gy': -0.85, 'gx': 0.1}}, toonDur=0.1),   # ...his eyes roll up to the egg frying on his forehead...
            k(r(CRACK2 + 0.75), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {'lid': 0.45, 'gy': -0.7, 'gx': 0.0}}, toonDur=0.2), k(r(D2 - 0.22), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': DEAD}, toonDur=0.15)]),   # ...deadpan
        act('voisine', GAM2, 20, 'stand', 'happy', keys=[k(0.0, look=[FORE2[0], FORE2[1], FORE2[2]]),
            k(0.0, toon={'reach': {'R': [r(FORE2[0] - 0.25), 1.5, r(FORE2[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.6}}, toonDur=0.0),   # the egg raised...
            k(r(CRACK2 - 0.06), toon={'reach': {'R': [r(FORE2[0] - 0.02), r(FORE2[1] + 0.02), FORE2[2], 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.96, 1.04], 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.8}}, toonDur=0.06, toonEase='in'),   # ...CRAC on his forehead...
            k(r(CRACK2 + 0.2), toon={'reach': {'R': [r(FORE2[0] - 0.35), 1.1, r(FORE2[2] + 0.15), 1, 0.05]}, 'hands': {'R': 'open'}, 'sq': [0.96, 1.05, 0.96], 'face': {'mouth': 'laugh', 'lid': 0.0, 'eye': 0.4, 'brow': 1.0}}, toonDur=0.12, toonEase='out')])],   # ...delighted
        props=[P('chair2', 'deckChair', pos=ME, ry=RY),
               P('egg2', 'friedEgg', on={'actor': 'voisine', 'hand': 'R', 'offset': [0.0, 0.04, 0.03]}, opts={'at': CRACK2, 'r': 0.11, 'dur': 1.2}, keys=[k(CRACK2, attach='mec', joint='head', offset=[0.0, 0.6, 0.21], rot=[round(PI / 2, 4), 0.0, 0.0])]),
               BURST('crac2', [r(FORE2[0] - 0.35), r(FORE2[1] + 0.35), r(FORE2[2] - 0.25)], CRACK2, 'CRAC !', 0.3)],
        cams=[FC(0.0, [3.6, 1.35, -10.8], [[r(ME[0] - 0.05), 1.8, ME[2]], [r(ME[0] - 0.15), 0.85, ME[2]], [r(ME[0] - 0.1), 1.4, r(ME[2] + 0.35)], [r(ME[0] - 0.1), 1.4, r(ME[2] - 0.35)], [GAM2[0], 2.0, GAM2[2]], [r(ME[0] - 0.4), 1.75, r(ME[2] - 0.35)]], top=0.12, bottom=0.72, drift=(0.06, 0.0, 0.0))])   # (stills 1) his whole head (it was cut by the edge)
st.cue('sfx:bonk', 'S02', CRACK2, 0.25); st.cue('sfx:static', 'S02', r(CRACK2 + 0.05), 0.3)

# 3: at night he lights up the whole neighbourhood. The street dark: he stands on the pavement glowing red, lighting the façades round him; moths
#    circle his head; a neighbour on a bench reads her paper by his light; a slow blink
D3 = st.dur('S03')
NIGHT = {**STREET, 'night': True}
NLOOK = {'sun': 0.25, 'sunColor': '#8DA4E0', 'fill': 0.55, 'exposure': 0.85}
ME3 = [5.5, 0, -12.0]; VOI3 = [5.7, 0, -10.5]
st.shot('S03', 'parisStreet', setOpts=NIGHT, look=NLOOK, actors=[
        act('mec', ME3, -110, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(RED, 1.0, 1.0), 'face': DEAD}, toonDur=0.0),
            k(0.6, toon={'skin': SKIN(RED, 1.0, 1.0), 'sq': [1.0, 1.012, 1.0], 'face': DEAD}, toonDur=0.3, toonEase='inOut'),
            k(1.2, toon={'skin': SKIN(RED, 1.0, 1.0), 'face': {'lid': 1.0}}, toonDur=0.14), k(1.45, toon={'skin': SKIN(RED, 1.0, 1.0), 'sq': [1.0, 0.996, 1.0], 'face': DEAD}, toonDur=0.18)]),   # glowing, a slow blink
        act('voisine', VOI3, -150, 'sit', 'neutral', keys=[k(0.0, look=[VOI3[0] - 0.3, 1.1, VOI3[2] - 0.35]), k(0.0, toon={'reach': {'R': [r(VOI3[0] - 0.25), 1.05, r(VOI3[2] - 0.32), 1, 0.05], 'L': [r(VOI3[0] - 0.05), 1.05, r(VOI3[2] - 0.42), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.5, 'gy': 0.4}}, toonDur=0.0),
            k(0.9, toon={'reach': {'R': [r(VOI3[0] - 0.25), 1.05, r(VOI3[2] - 0.32), 1, 0.05], 'L': [r(VOI3[0] - 0.05), 1.05, r(VOI3[2] - 0.42), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.5, 'gy': 0.45, 'gx': 0.3}}, toonDur=0.3)])],   # reading by his light
        props=[P('glow3', 'glowLight', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.3, 0.4]}, opts={'color': '#FF4A2A', 'k': 9, 'dist': 10, 'at': 0.0}),
               P('moths3', 'moths', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.55, 0.0]}, opts={'n': 7, 'r': 0.42}),
               P('bench3', 'bench', pos=[VOI3[0], 0, VOI3[2]], ry=-150), P('news3', 'newspaper', on={'actor': 'voisine', 'hand': 'R', 'offset': [0.0, 0.05, 0.05]})],
        cams=[FC(0.0, [3.4, 1.35, -9.9], [[ME3[0], 2.5, ME3[2]], [ME3[0], 0.0, ME3[2]], [VOI3[0], 1.4, VOI3[2]], [VOI3[0], 0.0, VOI3[2]], [r(ME3[0] + 1.6), 3.2, r(ME3[2] - 1.0)]], top=0.1, bottom=0.8, drift=(0.0, 0.0, -0.06))])
st.cue('sfx:static', 'S03', 0.05, 0.08)

# 4: the town hall installed him... A crossroads: the mayor in his sash points at a traffic light with three empty holes; two workers carry him in,
#    stiff as a plank on their shoulders
D4 = st.dur('S04')
LIGHT = [4.3, 0, 0.0]; LRY = 180; POLE = 2.0                             # the light at the kerb, facing the cars coming up the street (+Z)
HOLE = lambda i: [LIGHT[0], r(POLE + [0.32, 0.85, 1.38][i]), r(LIGHT[2] - 0.17)]   # the holes (0 green at the bottom, 2 red at the top), seen from the front (-Z)
CARRY0 = [1.2, 1.62, -1.7]; CARRY1 = [2.5, 1.62, -1.7]                   # (stills 1) along the kerb, toward the light, his length across the frame
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', CARRY0, 90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [round(-PI / 2, 4), 0.0], 'skin': SKIN(RED, 1.0, 0.2), 'face': DEAD}, toonDur=0.0),
            k(0.0, to=CARRY1, dur=D4, ease='inOut', face='keep')]),   # carried flat on his back, stiff, deadpan
        act('ouv1', [r(CARRY0[0] - 0.95), 0, CARRY0[2]], 90, 'stand', 'neutral', keys=[k(0.0, to=[r(CARRY1[0] - 0.95), 0, CARRY1[2]], dur=D4, clip='walk', then='stand', ease='inOut', face='keep'), k(0.0, look='camera'),
            k(0.0, toon={'touch': {'R': ['torso', -0.12, 0.95, 0.15, 1, 0.05], 'L': ['torso', 0.12, 0.95, 0.15, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.5, 'brow': -0.3}}, toonDur=0.0)]),   # under his head...
        act('ouv2', [r(CARRY0[0] + 0.8), 0, CARRY0[2]], 90, 'stand', 'neutral', keys=[k(0.0, to=[r(CARRY1[0] + 0.8), 0, CARRY1[2]], dur=D4, clip='walk', then='stand', ease='inOut', face='keep'), k(0.0, look='camera'),
            k(0.0, toon={'touch': {'R': ['torso', -0.12, 0.95, 0.15, 1, 0.05], 'L': ['torso', 0.12, 0.95, 0.15, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.5, 'brow': -0.3}}, toonDur=0.0)]),   # ...and under his feet
        act('maire', [5.3, 0, -1.2], -100, 'stand', 'determined', keys=[k(0.0, look=[LIGHT[0], 3.4, LIGHT[2]]), k(0.0, toon={'reach': {'R': [r(LIGHT[0] + 0.35), 3.0, r(LIGHT[2] - 0.6), 1, 0.08]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.4, 'brow': -0.2, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.35, look='camera'), k(0.4, toon={'reach': {'R': [r(LIGHT[0] + 0.35), 3.05, r(LIGHT[2] - 0.6), 1, 0.08]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.1)])],   # the mayor points, pleased
        props=[P('light4', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True})],
        cams=[FC(0.0, [2.6, 1.5, -6.6], [[LIGHT[0], 3.8, LIGHT[2]], [LIGHT[0], 0.0, LIGHT[2]], [r(CARRY0[0] - 1.2), 2.2, CARRY0[2]], [r(CARRY1[0] + 1.0), 1.9, CARRY1[2]], [5.3, 2.4, -1.2], [r(CARRY0[0] - 0.95), 0.0, CARRY0[2]]], top=0.1, bottom=0.8)])   # (stills 1) from in front: the plank across the frame, the light at the end

# 5: ...as a red light. Close on the light: his face pops up into the top hole, red, glowing, overshooting and settling; deadpan (FEU ROUGE)
D5 = st.dur('S05')
BEHIND = lambda i: [LIGHT[0], r(POLE + [0.32, 0.85, 1.38][i] - 2.2 + [0.13, 0.06, 0.0][i]), r(LIGHT[2] + 0.08)]   # where he stands for his face to fill hole i (his head centre about 2.2 m over his feet; (stills 1) in the bottom hole only his hair showed)
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BEHIND(2)[0], r(BEHIND(2)[1] - 0.7), BEHIND(2)[2]], LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(RED, 1.0, 0.6), 'face': DEAD}, toonDur=0.0),
            k(0.08, to=BEHIND(2), dur=0.12, ease='outBack', face='keep'), k(0.08, toon={'skin': SKIN(RED, 1.0, 0.7), 'sq': [0.9, 1.12, 0.9], 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.06, toonEase='out'),   # POP: into the top hole...
            k(0.22, toon={'skin': SKIN(RED, 1.0, 0.7), 'sq': [1.06, 0.95, 1.06], 'face': DEAD}, toonDur=0.06), k(0.32, toon={'skin': SKIN(RED, 1.0, 0.7), 'sq': [1.0, 1.0, 1.0], 'face': DEAD}, toonDur=0.08),   # ...settling...
            k(0.62, toon={'skin': SKIN(RED, 1.0, 0.7), 'face': {'lid': 1.0}}, toonDur=0.06), k(0.72, toon={'skin': SKIN(RED, 1.0, 0.7), 'face': DEAD}, toonDur=0.1)])],   # ...a blink: a red light
        props=[P('light5', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('glow5', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4, 'at': 0.1}),
               BURST('pop5', [r(LIGHT[0] - 0.55), r(HOLE(2)[1] + 0.35), r(LIGHT[2] - 0.4)], 0.1, 'POP !', 0.28)],
        cams=[FC(0.0, [LIGHT[0], 3.0, -2.7], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.4), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.5), r(POLE + 1.0), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 1.0), r(LIGHT[2] - 0.17)]], top=0.2, bottom=0.74, drift=(0.0, 0.0, 0.08))])
st.cue('sfx:poof', 'S05', 0.1, 0.3)

# 6: the cars stop in front of him... From far down the street on a long lens: a queue of cars to the light at the end, his red face glowing over them
D6 = st.dur('S06')
CARS = [(2.2, -3.0, '#3A9BDC'), (2.2, -8.6, '#F5C33B'), (2.2, -14.2, '#5FB86A'), (2.2, -19.8, '#C255C8'), (2.2, -25.4, '#E8463A'), (2.2, -31.0, '#F08A3C'), (-1.6, -5.0, '#8C949A'), (-1.6, -10.6, '#3A9BDC'), (-1.6, -16.2, '#F5C33B'), (-1.6, -21.8, '#5FB86A')]
QUEUE = lambda sid, extra=lambda i: {}: [P(f'car{sid}{i}', 'car', pos=[x_, 0, z_], ry=-90, opts={'color': c_}, **extra(i)) for i, (x_, z_, c_) in enumerate(CARS)]
HEADON = lambda col=RED, glow=0.7, i=2: act('mec', BEHIND(i), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(col, 1.0, glow), 'face': DEAD}, toonDur=0.0),
                                                                  k(0.6, toon={'skin': SKIN(col, 1.0, glow), 'face': {'lid': 1.0}}, toonDur=0.1), k(0.78, toon={'skin': SKIN(col, 1.0, glow), 'face': DEAD}, toonDur=0.12)])   # (audit) a blink in the long hold
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[HEADON()],
        props=[P('light6', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('glow6', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4}), *QUEUE('6')],
        cams=[cam(0.0, [0.8, 2.6, -62.0], [0.8, 2.6, -60.0], [3.4, 2.6, 0.0], [3.4, 2.6, 0.0], lens=9)])   # a long lens down the queue: the light at its head

# 7: ...all day long. The light against the sky: the sun races across behind him and goes down; he glows on, deadpan, a slow blink
D7 = st.dur('S07')
SUNPATH = [[0.0, -9.0, 3.0, 22.0], [r(D7 * 0.5), 3.0, 13.0, 26.0], [D7, 15.0, 2.0, 22.0]]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(RED, 1.0, 0.5), 'face': DEAD}, toonDur=0.0),
            k(0.4, toon={'skin': SKIN(RED, 1.0, 0.6), 'face': {'lid': 1.0}}, toonDur=0.16), k(0.66, toon={'skin': SKIN(RED, 1.0, 0.9), 'face': DEAD}, toonDur=0.2),   # a slow blink, glowing brighter as the sun goes...
            k(D7 - 0.1, toon={'skin': SKIN(RED, 1.0, 1.0), 'face': DEAD}, toonDur=0.1)])],
        props=[P('light7', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('sun7', 'sun', opts={'r': 1.3}, **FLY(SUNPATH))],   # (stills 1) no cars: the first one filled the side of the frame
        cams=[FC(0.0, [4.1, 1.2, -3.0], [[LIGHT[0], r(POLE + 1.8), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE + 0.2), r(LIGHT[2] - 0.17)], [0.0, 9.0, 24.0], [9.0, 9.0, 24.0]], top=0.08, bottom=0.78)])   # from below, the sky behind the light

# 8: yesterday a lorry honked at him. Side on across the road: the lorry at the head of the queue blasts its horns: TUUUT, the blast hits his face:
#    flattened wide in the hole, eyes bulging, hair blown back, the light rattling
D8 = st.dur('S08'); HONK8 = 0.45
TRUCK = [2.2, 0, -4.4]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look=[TRUCK[0], 2.5, -1.4]), k(0.0, toon={'skin': SKIN(RED, 1.0, 0.6), 'face': DEAD}, toonDur=0.0),
            k(HONK8, toon={'skin': SKIN(RED, 1.0, 0.6), 'scl': {'head': [1.3, 0.8, 1.0]}, 'wind': [0.0, 0.5, 14.0], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 1.0, 'eyeScale': 1.9, 'pupilSize': -0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.04, toonEase='out'),   # TUUUT: his face flattened by the blast...
            *[k(r(HONK8 + 0.06 + 0.05 * i), toon={'skin': SKIN(RED, 1.0, 0.6), 'scl': {'head': ([1.26, 0.82, 1.0] if i % 2 else [1.32, 0.78, 1.0])}, 'wind': [0.0, 0.5, 14.0], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 1.0, 'eyeScale': 1.9, 'pupilSize': -0.5, 'brow': 1.0, 'mouth': 'O', 'tremble': 1.0}}, toonDur=0.04) for i in range(10)],   # ...held while the horn lasts, quivering...
            k(r(HONK8 + 0.62), toon={'skin': SKIN(RED, 1.0, 0.6), 'scl': {'head': [1.0, 1.0, 1.0]}, 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.7, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.1, toonEase='out')]),   # ...and back, his hair on end
        ],
        props=[P('light8', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[HONK8, 0.05]]}), P('truck8', 'truck', pos=TRUCK, ry=-90, opts={'color': '#2F6FB2'}),
               P('blast8', 'speedLines', **FLY([[HONK8, 2.6, 2.6, -1.1], [r(HONK8 + 0.6), 3.4, 2.9, -0.6]]), face='camera', opts={'n': 7, 'len': 0.9, 'w': 0.7, 'angle': 0.25, 'soft': True, 'alpha': 0.8, 'at': [[HONK8, r(HONK8 + 0.6)]]}),
               BURST('tut8', [2.6, 3.4, -1.6], HONK8, 'TUUUT !', 0.5)],
        cams=[FC(0.0, [4.6, 3.0, -3.0], [[2.8, 2.7, -1.4], [2.4, 2.1, -1.0], [TRUCK[0], 0.5, -0.82], [LIGHT[0], r(POLE + 1.8), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE + 1.0), r(LIGHT[2] - 0.17)], [2.6, 3.8, -1.6]], top=0.12, bottom=0.74)])   # (stills 1) close on his face in the light, the cab's horns at its side (from across the road the lorry filled the frame)
st.cue('sfx:honkLong', 'S08', HONK8, 0.6)

# 9: he turned green with fear. Close on the light: his red face, eyes popping, goes green from the chin up; then it drops out of the top hole and pops
#    into the bottom one, green, glowing; a gulp
D9 = st.dur('S09'); TURN9 = 0.25; DROP9 = 0.8
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(RED, 1.0, 0.6), 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.7, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.0),
            k(TURN9, toon={'skin': SKIN(GREEN, 1.0, 0.6), 'hairUp': 0.9, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.0, 'eye': 1.0, 'eyeScale': 1.5, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'wavy', 'tremble': 1.0}}, toonDur=0.3, toonEase='inOut'),   # red to green, eyes popping, quivering...
            k(r(DROP9 - 0.06), toon={'skin': SKIN(GREEN, 1.0, 0.6), 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.0, 'eye': 0.9, 'brow': 1.0, 'mouth': 'wavy'}}, toonDur=0.05, toonEase='in'),
            k(DROP9, to=BEHIND(0), dur=0.12, ease='in', face='keep'),   # ...and down, out of the top hole into the bottom one...
            k(r(DROP9 + 0.12), toon={'skin': SKIN(GREEN, 1.0, 0.7), 'sq': [1.1, 0.9, 1.1], 'face': {'lid': 0.3, 'gulp': 1.0}}, toonDur=0.03, toonEase='out'),   # ...a landing squash, a gulp...
            k(r(DROP9 + 0.26), toon={'skin': SKIN(GREEN, 1.0, 0.7), 'sq': [1.0, 1.0, 1.0], 'face': DEAD}, toonDur=0.1), k(r(D9 - 0.2), toon={'skin': SKIN(GREEN, 1.0, 0.7), 'face': {'lid': 1.0}}, toonDur=0.1)])],   # ...a green light, a blink
        props=[P('light9', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'open': [[0.0, 2], [r(DROP9 + 0.06), 0]]}),
               P('glow9r', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4}, keys=[k(TURN9, visible=False)]),
               P('glow9g', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#44FF55', 'k': 3, 'dist': 4, 'at': r(DROP9 + 0.1)})],
        cams=[FC(0.0, [LIGHT[0], 2.9, -2.8], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.1), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.5), r(POLE + 0.9), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 0.9), r(LIGHT[2] - 0.17)]], top=0.16, bottom=0.76, drift=(0.0, 0.0, 0.06))])
st.cue('sfx:slideDown', 'S09', DROP9, 0.3); st.cue('sfx:gulp', 'S09', r(DROP9 + 0.12), 0.25)

# 10: all the cars went through. Low beside the light: every car shoots past, one after the other, speed lines, his hair whipped in the bottom hole,
#     the light rattling; deadpan
D10 = st.dur('S10')
PASS = lambda i, x_, z_: {'keys': [k(r(0.05 + 0.12 * i), to=[x_, 0, r(z_ + 40.0)], dur=0.6, ease='in')]}
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(0), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(GREEN, 1.0, 0.7), 'wind': [-6.0, 0.5, 10.0], 'hairUp': 0.9, 'face': DEAD}, toonDur=0.0),
            *[k(r(0.1 + 0.12 * i), toon={'skin': SKIN(GREEN, 1.0, 0.7), 'wind': [-6.0, 0.5, 10.0], 'hairUp': (1.0 if i % 2 else 0.8), 'sq': ([1.02, 0.98, 1.02] if i % 2 else [1.0, 1.0, 1.0]), 'face': DEAD}, toonDur=0.08) for i in range(8)],   # each car's wind
            k(1.2, toon={'skin': SKIN(GREEN, 1.0, 0.7), 'hairUp': 0.9, 'face': {'lid': 1.0}}, toonDur=0.08), k(1.3, toon={'skin': SKIN(GREEN, 1.0, 0.7), 'hairUp': 0.9, 'face': DEAD}, toonDur=0.1)])],
        props=[P('light10', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[0.1, 0.03], [0.5, 0.03]], 'open': [[0.0, 0]]}), P('glow10', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#44FF55', 'k': 3, 'dist': 4}),
               P('truck10', 'truck', pos=[2.2, 0, -4.4], ry=-90, keys=[k(0.0, to=[2.2, 0, 40.0], dur=0.7, ease='in')]),
               *[P(f'car10{i}', 'car', pos=[x_, 0, z_], ry=-90, opts={'color': c_}, **PASS(i, x_, z_)) for i, (x_, z_, c_) in enumerate(CARS[1:6])],
               P('spd10', 'speedLines', pos=[1.6, 1.2, 1.5], face='camera', opts={'n': 9, 'len': 2.4, 'w': 1.4, 'angle': 0.0, 'soft': True, 'taper': True, 'alpha': 0.6, 'at': [[0.05, 1.0]]})],
        cams=[FC(0.0, [0.8, 1.1, -3.6], [[LIGHT[0], r(POLE + 1.75), r(LIGHT[2] - 0.17)], [LIGHT[0], 0.0, LIGHT[2]], [2.2, 1.6, -2.4], [2.2, 0.0, 2.4]], top=0.1, bottom=0.8)])   # (stills 1) across the lane from the light: the cars streak between us and him   # low beside the light, in front of it ((audit) behind it we saw his back), the traffic streaking past
st.cue('whoosh', 'S10', 0.05, 0.4, 1.2, 200, 1400); st.cue('sfx:engine', 'S10', 0.1, 0.3)

# 11: the town hall painted him red again. A painter on a ladder in front of the light rolls his green face red, stroke by stroke, his eyes shutting at
#     each stroke; the cars stop again behind; deadpan (REPEINT)
D11 = st.dur('S11'); STROKES = [0.3, 0.62, 0.94]
LAD = [r(LIGHT[0] - 0.85), 0, r(LIGHT[2] - 0.55)]                          # (stills 1) beside the light: in front of it the painter hid his face
ROLL = lambda dy: {'reach': {'R': [LIGHT[0], r(HOLE(0)[1] + dy), r(LIGHT[2] - 0.3), 1, 0.05], 'L': [r(LIGHT[0] - 0.3), 1.9, r(LAD[2] + 0.1), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
COLS = ['#8FCB3A', '#E0A22A', RED]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(0), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(GREEN, 1.0, 0.6), 'face': DEAD}, toonDur=0.0),
            *[k(t_, toon={'skin': SKIN(COLS[i], 1.0, 0.6), 'face': {'lid': 1.0}}, toonDur=0.06) for i, t_ in enumerate(STROKES)],   # each stroke: his eyes shut, a colour nearer red...
            *[k(r(t_ + 0.12), toon={'skin': SKIN(COLS[i], 1.0, 0.6), 'face': DEAD}, toonDur=0.08) for i, t_ in enumerate(STROKES)],
            k(1.7, toon={'skin': SKIN(RED, 1.0, 0.6), 'sq': [1.0, 1.012, 1.0], 'face': DEAD}, toonDur=0.3), k(2.1, toon={'skin': SKIN(RED, 1.0, 0.6), 'face': {'lid': 1.0}}, toonDur=0.14), k(2.35, toon={'skin': SKIN(RED, 1.0, 0.6), 'face': DEAD}, toonDur=0.15)]),   # ...red again; a slow blink
        act('peintre', [LAD[0], 0.9, r(LAD[2] - 0.2)], 60, 'stand', 'neutral', keys=[k(0.0, look=HOLE(0)), k(0.0, toon={**ROLL(0.3), 'face': {'lid': 0.5, 'gy': 0.2}}, toonDur=0.0),
            *[k(r(t_ - 0.12), toon={**ROLL(0.28), 'face': {'lid': 0.5}}, toonDur=0.1) for t_ in STROKES], *[k(t_, toon={**ROLL(-0.22), 'face': {'lid': 0.5}}, toonDur=0.12, toonEase='inOut') for t_ in STROKES],   # the roller up and down his face
            k(1.3, toon={**ROLL(0.0), 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.2), k(1.35, look='camera')])],
        props=[P('light11', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'open': [[0.0, 0]]}), P('lad11', 'ladder', pos=LAD, ry=-20, opts={'h': 2.2, 'lean': 0.18}),
               P('roller11', 'paintRoller', on={'actor': 'peintre', 'hand': 'R'}, opts={'len': 0.5, 'color': RED}),
               P('car11', 'car', pos=[2.2, 0, -16.0], ry=-90, opts={'color': '#3A9BDC'}, keys=[k(0.9, to=[2.2, 0, -7.0], dur=0.6, ease='out')])],   # the next car stops again ((stills 1) further back: at the light it drove into the lens)
        cams=[FC(0.0, [4.9, 2.1, -3.4], [[LIGHT[0], r(POLE + 1.75), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.2), r(LIGHT[2] - 0.17)], [LAD[0], 2.8, r(LAD[2] - 0.2)], [LAD[0], 0.9, r(LAD[2] - 0.2)]], top=0.12, bottom=0.76, drift=(0.04, 0.0, -0.04))])
for t_ in STROKES: st.cue('sfx:squeak', 'S11', t_, 0.15)
st.cue('sfx:brake', 'S11', 1.3, 0.3)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.2, 'mec', 'sunburn'), ('S02', 0.8, 'mec', 'egg'), ('S03', 1.0, 'mec', 'glow'), ('S05', 0.5, 'mec', 'redlight'), ('S08', 0.6, 'mec', 'honk'), ('S09', 1.2, 'mec', 'green'), ('S11', 2.0, 'mec', 'repaint')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
st.card('S05', 'FEU ROUGE', at=0.3)
st.card('S11', 'REPEINT', at=0.6)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
st.write("Le coup de soleil", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'gamin': {'preset': 'gamin', 'seed': 621, 'suit': '#F08A3C', 'hat': 'beanie', 'hatColor': '#3A9BDC', 'build': {'height': 0.55, 'headScale': 1.35}, 'toon': EX},
    'voisine': {'preset': 'madame', 'seed': 622, 'suit': '#8E5AA8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 623, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ouv1': {'preset': 'sportif', 'seed': 624, 'suit': '#F08A3C', 'hat': 'hardhat', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ouv2': {'preset': 'sportif', 'seed': 625, 'suit': '#F08A3C', 'hat': 'hardhat', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'peintre': {'preset': 'sportif', 'seed': 626, 'suit': '#F2F0EA', 'hat': 'beanie', 'hatColor': '#F2F0EA', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
})
