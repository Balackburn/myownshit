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
#    (stills 2: turned to the sun, we saw his tilted head from behind and small, the sitting arms stuck out like a sleepwalker's) turned up the street
#    toward us, the sun down the street beyond him, his hands folded on his belly, a closer camera from the pavement
D1 = st.dur('S01')
ME = [5.2, 0, -12.0]; RY = 10                                            # on the right pavement ((stills 2) turned up the street, toward the camera: the sun is down the street behind him)
SEATED = [ME[0], -0.15, ME[2]]                                           # the deckchair's seat is lower than a chair's
LOUNGE = {'bend': {'spine': [-0.42, 0, 0, 1, None], 'neck': [0.12, 0, 0, 1, None]},
          'touch': {'L': ['torso', 0.07, 0.3, 0.19, 1, 0.03], 'R': ['torso', -0.07, 0.34, 0.2, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}}   # (stills 2) hands folded on his belly
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEATED, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'face': {'lid': 0.75, 'mouth': 'smile', 'cheeks': 0.4}}, toonDur=0.0),
            k(0.25, toon={**LOUNGE, 'skin': SKIN(RED, 0.6, 0.0, 0.4), 'face': {'lid': 0.7, 'mouth': 'smile', 'cheeks': 0.4}}, toonDur=0.18),   # his hands go red...
            k(0.6, toon={**LOUNGE, 'skin': SKIN(RED, 0.8, 0.0, 0.8), 'face': {'lid': 0.6, 'mouth': 'smile'}}, toonDur=0.18),   # ...his neck...
            k(0.95, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.1, 1.0), 'face': {'lid': 0.45, 'mouth': 'flat'}}, toonDur=0.14),   # ...his whole head, his smile gone...
            k(1.12, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15, 1.0), 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.45, 'mouth': 'flat', 'steam': 1.0}}, toonDur=0.06, toonEase='out'),   # ...steam puffs out of his ears
            k(1.45, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15, 1.0), 'face': {'lid': 0.45, 'mouth': 'flat', 'steam': 1.0}}, toonDur=0.15)])],
        props=[P('chair1', 'deckChair', pos=ME, ry=RY), P('sun1', 'sun', pos=[2.4, 4.4, -19.0], opts={'r': 1.1}, keys=[k(0.0, scale=1.0, dur=0.0), k(0.9, scale=1.12, dur=0.25, ease='inOut')])],   # (stills 1) nearer: in the corner of a closer frame
        cams=[FC(0.0, [6.9, 1.0, -9.6], [[ME[0], 1.8, r(ME[2] - 0.1)], [ME[0], 0.35, r(ME[2] + 0.5)], [r(ME[0] - 0.4), 0.9, ME[2]], [r(ME[0] + 0.4), 0.9, ME[2]], [2.4, 4.4, -19.0]], top=0.06, bottom=0.8, drift=(-0.06, 0.0, -0.06))])   # (stills 2) in front of him from the pavement, the sun beyond him
st.cue('sfx:static', 'S01', 0.3, 0.12); st.cue('sfx:static', 'S01', 1.12, 0.22)

# 2: he turned bright red. Close on his red face: a boy beside the deckchair cracks an egg on his forehead; the egg fries there, bubbling, steam
#    rising; his eyes roll up to it, deadpan
D2 = st.dur('S02'); CRACK2 = 0.42
GAM2 = [6.0, 0, -12.04]                                                  # (stills 1) the neighbour at his side, her hand at his forehead height (the boy's arm stretched like a pole); (stills 2) at his left, the camera side
FORE2 = [5.24, 1.32, -11.78]                                             # his forehead, seated and leaning back ((stills 2) turned up the street)
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEATED, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': DEAD}, toonDur=0.0),
            k(r(CRACK2 + 0.02), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 1.0}}, toonDur=0.03),   # CRAC: a blink...
            k(r(CRACK2 + 0.16), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {'lid': 0.3, 'gy': -0.85, 'gx': 0.1}}, toonDur=0.1),   # ...his eyes roll up to the egg frying on his forehead...
            k(r(CRACK2 + 0.75), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {'lid': 0.45, 'gy': -0.7, 'gx': 0.0}}, toonDur=0.2), k(r(D2 - 0.22), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': DEAD}, toonDur=0.15)]),   # ...deadpan
        act('voisine', GAM2, -60, 'stand', 'happy', keys=[k(0.0, look=[FORE2[0], FORE2[1], FORE2[2]]),
            k(0.0, toon={'reach': {'L': [r(FORE2[0] + 0.12), 1.78, r(FORE2[2] + 0.02), 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.6}}, toonDur=0.0),   # the egg raised over his head ((stills 2) her near hand: the far one crossed her body)...
            k(r(CRACK2 - 0.06), toon={'reach': {'L': [r(FORE2[0] + 0.03), r(FORE2[1] + 0.06), r(FORE2[2] + 0.05), 1, 0.03]}, 'hands': {'L': 'grip'}, 'sq': [1.04, 0.96, 1.04], 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.8}}, toonDur=0.06, toonEase='in'),   # ...CRAC on his forehead...
            k(r(CRACK2 + 0.2), toon={'reach': {'L': [r(FORE2[0] + 0.4), 1.15, r(FORE2[2] + 0.12), 1, 0.05]}, 'hands': {'L': 'open'}, 'sq': [0.96, 1.05, 0.96], 'face': {'mouth': 'laugh', 'lid': 0.0, 'eye': 0.4, 'brow': 1.0}}, toonDur=0.12, toonEase='out')])],   # ...delighted
        props=[P('chair2', 'deckChair', pos=ME, ry=RY),
               P('egg2', 'friedEgg', on={'actor': 'voisine', 'hand': 'L', 'offset': [0.0, 0.04, 0.03]}, opts={'at': CRACK2, 'r': 0.085, 'dur': 1.2}, keys=[k(CRACK2, attach='mec', joint='head', offset=[0.0, 0.415, 0.088], rot=[round(PI / 2, 4), 0.0, 0.0])]),   # (stills 2) flat on the front of his head above the eyes (head 0.5 high, 0.17 deep: at 0.6 up and 0.21 out it floated over him)
               BURST('crac2', [r(FORE2[0] - 0.42), r(FORE2[1] + 0.3), r(FORE2[2] + 0.05)], CRACK2, 'CRAC !', 0.3)],   # (stills 2) beside the impact, on his other side from her
        cams=[FC(0.0, [6.4, 1.5, -9.9], [[ME[0], 1.85, r(ME[2] - 0.05)], [ME[0], 0.75, r(ME[2] + 0.3)], [GAM2[0], 2.4, GAM2[2]], [r(FORE2[0] + 0.12), 1.88, FORE2[2]], [r(FORE2[0] - 0.5), 1.8, r(FORE2[2] + 0.05)]], top=0.08, bottom=0.76, drift=(0.05, 0.0, 0.0))])   # (stills 2) her head in the frame too (it was cut by the top); (stills 3) she leans in: her head point higher
st.cue('sfx:bonk', 'S02', CRACK2, 0.25); st.cue('sfx:static', 'S02', r(CRACK2 + 0.05), 0.3)

# 3: at night he lights up the whole neighbourhood. The street dark: he stands on the pavement glowing red, lighting the façades round him; moths
#    circle his head; a neighbour on a bench reads her paper by his light; a slow blink
#    (stills 2: in profile, the moths too small to see, the whole frame red without sky: a red room, not a night) down the street from the pavement:
#    the night sky over the end of the street, a pool of red round him fading into the blue dark, the moths two and a half times bigger, him three
#    quarters to us, the neighbour on her bench beside him
D3 = st.dur('S03')
NIGHT = {**STREET, 'night': True}
NLOOK = {'sun': 0.25, 'sunColor': '#8DA4E0', 'fill': 0.55, 'exposure': 0.85}
ME3 = [5.5, 0, -12.0]; VOI3 = [6.32, 0, -11.52]                          # (stills 2) she sits at his left, turned like him toward us
PAPER3 = lambda gx: {'reach': {'R': [6.09, 1.05, -11.26, 1, 0.05], 'L': [6.33, 1.05, -11.18, 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.5, 'gy': 0.45, 'gx': gx}}
st.shot('S03', 'parisStreet', setOpts=NIGHT, look=NLOOK, actors=[
        act('mec', ME3, -30, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN(RED, 1.0, 1.0), 'face': DEAD}, toonDur=0.0),
            k(0.6, toon={'skin': SKIN(RED, 1.0, 1.0), 'sq': [1.0, 1.012, 1.0], 'face': DEAD}, toonDur=0.3, toonEase='inOut'),
            k(1.2, toon={'skin': SKIN(RED, 1.0, 1.0), 'face': {'lid': 1.0}}, toonDur=0.14), k(1.45, toon={'skin': SKIN(RED, 1.0, 1.0), 'sq': [1.0, 0.996, 1.0], 'face': DEAD}, toonDur=0.18)]),   # glowing, a slow blink
        act('voisine', VOI3, -20, 'sit', 'neutral', keys=[k(0.0, look=[6.21, 1.0, -11.2]), k(0.0, toon=PAPER3(0.0), toonDur=0.0), k(0.9, toon=PAPER3(0.3), toonDur=0.3)])],   # reading by his light
        props=[P('glow3', 'glowLight', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.3, 0.4]}, opts={'color': '#FF4A2A', 'k': 5, 'dist': 7, 'at': 0.0}),   # (stills 2) softer: a pool of red, the dark beyond it
               P('moths3', 'moths', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.55, 0.0]}, opts={'n': 7, 'r': 0.2}, scale=2.6),   # (stills 2) big enough to see
               P('bench3', 'bench', pos=[VOI3[0], 0, VOI3[2]], ry=-20), P('news3', 'newspaper', on={'actor': 'voisine', 'hand': 'R', 'offset': [0.0, 0.05, 0.05]})],
        cams=[FC(0.0, [4.7, 1.0, -6.6], [[ME3[0], 2.8, ME3[2]], [ME3[0], 0.0, ME3[2]], [VOI3[0], 1.5, VOI3[2]], [VOI3[0], 0.0, VOI3[2]], [3.0, 14.0, -60.0]], top=0.06, bottom=0.8, drift=(0.0, 0.0, -0.06))])   # (stills 2) the sky over the end of the street
st.cue('sfx:static', 'S03', 0.05, 0.08)


# 4: the town hall installed him... A crossroads: the mayor in his sash points at a traffic light with three empty holes; two workers carry him in,
#    stiff as a plank on their shoulders
#    (stills 2: from the side and far, the plank was a dark stroke between two small workers) from high behind them: the plank comes up the frame
#    toward the light, his red face up to us, the light at the top with its empty holes facing us, the mayor beside it pointing at the top one
D4 = st.dur('S04')
LIGHT = [4.3, 0, 0.0]; LRY = 180; POLE = 2.0                             # the light at the kerb, facing the cars coming up the street (+Z)
HOLE = lambda i: [LIGHT[0], r(POLE + [0.32, 0.85, 1.38][i]), r(LIGHT[2] - 0.17)]   # the holes (0 green at the bottom, 2 red at the top), seen from the front (-Z)
CARRY0 = [4.1, 1.62, -6.0]; CARRY1 = [4.1, 1.62, -4.4]                   # (stills 2) up the kerb to the light's front, his head first
SHOULDER = {'touch': {'R': ['torso', -0.12, 0.95, 0.15, 1, 0.05], 'L': ['torso', 0.12, 0.95, 0.15, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.5, 'brow': -0.3}}
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', CARRY0, 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [round(-PI / 2, 4), 0.0], 'skin': SKIN(RED, 1.0, 0.2), 'face': DEAD}, toonDur=0.0),
            k(0.0, to=CARRY1, dur=D4, ease='inOut', face='keep')]),   # carried flat on his back, stiff, his face up to us, deadpan
        act('ouv1', [CARRY0[0], 0, r(CARRY0[2] + 0.95)], 0, 'stand', 'neutral', keys=[k(0.0, to=[CARRY1[0], 0, r(CARRY1[2] + 0.95)], dur=D4, clip='walk', then='stand', ease='inOut', face='keep'), k(0.0, toon=SHOULDER, toonDur=0.0)]),   # under his head...
        act('ouv2', [CARRY0[0], 0, r(CARRY0[2] - 0.8)], 0, 'stand', 'neutral', keys=[k(0.0, to=[CARRY1[0], 0, r(CARRY1[2] - 0.8)], dur=D4, clip='walk', then='stand', ease='inOut', face='keep'), k(0.0, toon=SHOULDER, toonDur=0.0)]),   # ...and under his feet
        act('maire', [5.25, 0, -0.95], -160, 'stand', 'determined', keys=[k(0.0, look=[LIGHT[0], 3.4, LIGHT[2]]), k(0.0, toon={'reach': {'L': [4.75, 3.3, -0.5, 1, 0.08]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.4, 'brow': -0.2, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.35, look='camera'), k(0.4, toon={'reach': {'L': [4.75, 3.36, -0.5, 1, 0.08]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.3, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.1)])],   # the mayor points at the top hole, pleased
        props=[P('light4', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True})],
        cams=[FC(0.0, [0.6, 4.4, -9.2], [[LIGHT[0], 3.95, LIGHT[2]], [LIGHT[0], 2.0, r(LIGHT[2] - 0.17)], [5.25, 2.1, -0.95], [5.25, 1.0, -0.95], [CARRY0[0], 1.3, r(CARRY0[2] - 0.8)], [CARRY1[0], 2.15, r(CARRY1[2] + 0.95)], [3.7, 1.62, CARRY0[2]], [4.5, 1.62, CARRY0[2]]], top=0.08, bottom=0.8)])   # (stills 2) high behind the carry; (stills 3) and to its left: straight behind, the worker at his feet hid him


# 5: ...as a red light. Close on the light: his face pops up into the top hole, red, glowing, overshooting and settling; deadpan (FEU ROUGE)
#    (stills 2: his head 18 cm under the hole's centre and 8 cm aside (his weight shift at rest), the sky through the open back round it) his feet
#    1.99 m under the hole's centre (measured with debugJoints), no weight shift, the head widened to fill the round hole, a dark back in the box
D5 = st.dur('S05')
BEHIND = lambda i: [LIGHT[0], r(POLE + [0.32, 0.85, 1.38][i] - 1.99), r(LIGHT[2] + 0.08)]   # where he stands for his head to fill hole i ((stills 2) measured: the head's centre 1.99 m over his feet)
FILL = {'head': [1.85, 0.97, 1.0]}                                       # (stills 2) his head widened to fill the round hole (at its own width the dark showed at its sides)
IN = lambda d, scl=None: {'hip': 0, **d, 'scl': (scl or FILL)}           # (stills 2) in the light: no weight shift at rest, the head filling the hole
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BEHIND(2)[0], r(BEHIND(2)[1] - 0.7), BEHIND(2)[2]], LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'face': DEAD}, {'head': [1.0, 1.0, 1.0]}), toonDur=0.0),
            k(0.08, to=BEHIND(2), dur=0.12, ease='outBack', face='keep'), k(0.08, toon=IN({'skin': SKIN(RED, 1.0, 0.7), 'sq': [0.94, 1.07, 0.94], 'face': {'lid': 0.3, 'brow': 0.4}}, {'head': [0.85, 1.15, 1.0]}), toonDur=0.06, toonEase='out'),   # POP: up into the top hole, stretched...
            k(0.22, toon=IN({'skin': SKIN(RED, 1.0, 0.7), 'sq': [1.04, 0.96, 1.04], 'face': DEAD}, {'head': [2.15, 0.9, 1.0]}), toonDur=0.06),   # ...his head spreads past the rim...
            k(0.32, toon=IN({'skin': SKIN(RED, 1.0, 0.7), 'sq': [1.0, 1.0, 1.0], 'face': DEAD}), toonDur=0.08),   # ...and settles, filling it
            k(0.62, toon=IN({'skin': SKIN(RED, 1.0, 0.7), 'face': {'lid': 1.0}}), toonDur=0.06), k(0.72, toon=IN({'skin': SKIN(RED, 1.0, 0.7), 'face': DEAD}), toonDur=0.1)])],   # ...a blink: a red light
        props=[P('light5', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('glow5', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4, 'at': 0.1}),
               BURST('pop5', [r(LIGHT[0] - 0.55), r(HOLE(2)[1] + 0.35), r(LIGHT[2] - 0.4)], 0.1, 'POP !', 0.28)],
        cams=[FC(0.0, [LIGHT[0], 3.0, -2.7], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.4), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.5), r(POLE + 1.0), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 1.0), r(LIGHT[2] - 0.17)]], top=0.2, bottom=0.74, drift=(0.0, 0.0, 0.08))])
st.cue('sfx:poof', 'S05', 0.1, 0.3)


# 6: the cars stop in front of him... From far down the street on a long lens: a queue of cars to the light at the end, his red face glowing over them
D6 = st.dur('S06')
CARS = [(2.2, -3.0, '#3A9BDC'), (2.2, -8.6, '#F5C33B'), (2.2, -14.2, '#5FB86A'), (2.2, -19.8, '#C255C8'), (2.2, -25.4, '#E8463A'), (2.2, -31.0, '#F08A3C'), (-1.6, -5.0, '#8C949A'), (-1.6, -10.6, '#3A9BDC'), (-1.6, -16.2, '#F5C33B'), (-1.6, -21.8, '#5FB86A')]
QUEUE = lambda sid, extra=lambda i: {}: [P(f'car{sid}{i}', 'car', pos=[x_, 0, z_], ry=-90, opts={'color': c_}, **extra(i)) for i, (x_, z_, c_) in enumerate(CARS)]
HEADON = lambda col=RED, glow=0.7, i=2: act('mec', BEHIND(i), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(col, 1.0, glow), 'face': DEAD}), toonDur=0.0),
                                                                  k(0.6, toon=IN({'skin': SKIN(col, 1.0, glow), 'face': {'lid': 1.0}}), toonDur=0.1), k(0.78, toon=IN({'skin': SKIN(col, 1.0, glow), 'face': DEAD}), toonDur=0.12)])   # (audit) a blink in the long hold
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[HEADON()],
        props=[P('light6', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('glow6', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4}), *QUEUE('6')],
        cams=[cam(0.0, [0.8, 2.6, -62.0], [0.8, 2.6, -60.0], [3.4, 2.6, 0.0], [3.4, 2.6, 0.0], lens=9)])   # a long lens down the queue: the light at its head

# 7: ...all day long. The light against the sky: the sun races across behind him and goes down; he glows on, deadpan, a slow blink
#    (stills 2: from under the box his face was a red sliver in the top hole) in front of the light, a little below it: his face in the top hole, the
#    sky over the box, the sun rising at the left, crossing over the top of the light and setting behind the houses at the right
D7 = st.dur('S07')
SUNPATH = [[0.0, -3.4, 7.0, 24.0], [r(D7 * 0.25), 0.4, 16.5, 24.0], [r(D7 * 0.5), 4.2, 21.5, 24.0], [r(D7 * 0.75), 8.0, 16.5, 24.0], [D7, 11.8, 7.0, 24.0]]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': DEAD}), toonDur=0.0),
            k(0.4, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'face': {'lid': 1.0}}), toonDur=0.16), k(0.66, toon=IN({'skin': SKIN(RED, 1.0, 0.9), 'face': DEAD}), toonDur=0.2),   # a slow blink, glowing brighter as the sun goes...
            k(r(D7 - 0.1), toon=IN({'skin': SKIN(RED, 1.0, 1.0), 'face': DEAD}), toonDur=0.1)])],
        props=[P('light7', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('sun7', 'sun', opts={'r': 1.3}, **FLY(SUNPATH))],   # (stills 1) no cars: the first one filled the side of the frame
        cams=[FC(0.0, [4.1, 1.7, -4.8], [[LIGHT[0], 3.95, LIGHT[2]], [LIGHT[0], r(POLE + 0.6), r(LIGHT[2] - 0.17)], [4.2, 21.5, 24.0], [4.2, 23.0, 24.0]], top=0.06, bottom=0.78)])   # (stills 2) his face in the top hole, the sun's arc over the box


# 8: yesterday a lorry honked at him. Side on across the road: the lorry at the head of the queue blasts its horns: TUUUT, the blast hits his face:
#    flattened wide in the hole, eyes bulging, hair blown back, the light rattling
#    (stills 2: the light cut by the edge of the frame, the lorry's side filling the rest) two shots: the lorry rolls up to the light and stops nose
#    down, its horns seen from beside the light: TUUUT; cut to his face in the hole, flattened by the blast, the wind lines coming from the side
D8 = st.dur('S08'); HONK8 = 0.45; CUT8 = 0.62
TRUCK = [2.2, 0, -4.4]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'face': {**DEAD, 'gx': 0.6}}), toonDur=0.0),   # (stills 3) his head stays in the hole (turned to the lorry it slid out of it), his eyes go to it
            k(HONK8, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'wind': [0.0, 0.5, -14.0], 'hairUp': 1.0, 'face': {'lid': 0.0, 'pop': 0.55, 'popLen': 0.06, 'eyeScale': 1.4, 'pupilSize': -0.3, 'brow': 1.0, 'mouth': 'O'}}, {'head': [2.2, 0.95, 0.65]}), toonDur=0.04, toonEase='out'),   # (stills 4) flattened in depth and spread wide, not in height (squashed, his wide eyes read as heavy lids)   # (stills 3) the blast blows back (forward, his tie came out through the glass)   # TUUUT: his face flattened by the blast...
            *[k(r(HONK8 + 0.06 + 0.05 * i), toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'wind': [0.0, 0.5, -14.0], 'hairUp': 1.0, 'face': {'lid': 0.0, 'pop': 0.55, 'popLen': (0.07 if i % 2 else 0.05), 'eyeScale': 1.4, 'pupilSize': -0.3, 'brow': 1.0, 'mouth': 'O', 'tremble': 1.0}}, ({'head': [2.15, 0.97, 0.67]} if i % 2 else {'head': [2.25, 0.93, 0.63]})), toonDur=0.04) for i in range(10)],   # ...held while the horn lasts, quivering...
            k(r(HONK8 + 0.62), toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.7, 'brow': 0.8, 'mouth': 'o'}}), toonDur=0.1, toonEase='out')]),   # ...and back, his hair on end
        ],
        props=[P('light8', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[HONK8, 0.05]]}),
               P('truck8', 'truck', pos=[TRUCK[0], 0, -12.0], ry=-90, opts={'color': '#2F6FB2'}, keys=[k(0.0, to=TRUCK, dur=0.3, ease='out'), k(0.3, squash=[1.0, 0.92, 1.04], dur=0.35)]),   # (stills 2) it rolls up and stops, nose down
               P('blast8', 'speedLines', **FLY([[HONK8, 2.6, 2.6, -1.1], [r(HONK8 + 0.6), 3.4, 2.9, -0.6]]), face='camera', opts={'n': 7, 'len': 0.9, 'w': 0.7, 'angle': 0.25, 'soft': True, 'alpha': 0.8, 'at': [[HONK8, r(HONK8 + 0.6)]]}),
               BURST('tut8', [2.2, 3.3, -1.5], HONK8, 'TUUUT !', 0.5)],
        cams=[cam(0.0, [0.7, 1.7, 1.2], [0.72, 1.71, 1.15], [2.0, 2.25, -1.4], [2.0, 2.25, -1.4], lens=50),   # (stills 2) the lorry's horns...; (stills 3) from in front of its cab, a little low: backed off behind the light we saw its side and not its horns
              FC(CUT8, [LIGHT[0], 3.0, -2.7], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE + 0.6), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.62), r(POLE + 1.2), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 1.2), r(LIGHT[2] - 0.17)]], top=0.16, bottom=0.76)])   # ...his face in the hole, flattened
st.cue('sfx:honkLong', 'S08', HONK8, 0.6)


# 9: he turned green with fear. Close on the light: his red face, eyes popping, goes green from the chin up; then it drops out of the top hole and pops
#    into the bottom one, green, glowing; a gulp
#    (stills 2) no weight shift, the head filling the hole; on the landing his head spreads past the rim (a body squash dropped his face out of it)
D9 = st.dur('S09'); TURN9 = 0.25; DROP9 = 0.8
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.7, 'brow': 0.8, 'mouth': 'o'}}), toonDur=0.0),
            k(TURN9, toon=IN({'skin': SKIN(GREEN, 1.0, 0.6), 'hairUp': 0.9, 'sq': [0.98, 1.02, 0.98], 'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'wavy', 'tremble': 1.0}}), toonDur=0.3, toonEase='inOut'),   # red to green, eyes popping, quivering...
            k(r(DROP9 - 0.06), toon=IN({'skin': SKIN(GREEN, 1.0, 0.6), 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.0, 'eye': 0.9, 'brow': 1.0, 'mouth': 'wavy'}}), toonDur=0.05, toonEase='in'),
            k(DROP9, to=BEHIND(0), dur=0.12, ease='in', face='keep'),   # ...and down, out of the top hole into the bottom one...
            k(r(DROP9 + 0.12), toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.3, 'gulp': 1.0}}, {'head': [2.2, 0.84, 1.0]}), toonDur=0.03, toonEase='out'),   # ...a landing squash in his head, a gulp...
            k(r(DROP9 + 0.26), toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'sq': [1.0, 1.0, 1.0], 'face': DEAD}), toonDur=0.1), k(r(D9 - 0.2), toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'face': {'lid': 1.0}}), toonDur=0.1)])],   # ...a green light, a blink
        props=[P('light9', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'open': [[0.0, 2], [r(DROP9 + 0.06), 0]]}),
               P('glow9r', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4}, keys=[k(TURN9, visible=False)]),
               P('glow9g', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#44FF55', 'k': 3, 'dist': 4, 'at': r(DROP9 + 0.1)})],
        cams=[FC(0.0, [LIGHT[0], 2.9, -2.8], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.1), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.5), r(POLE + 0.9), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 0.9), r(LIGHT[2] - 0.17)]], top=0.16, bottom=0.76, drift=(0.0, 0.0, 0.06))])
st.cue('sfx:slideDown', 'S09', DROP9, 0.3); st.cue('sfx:gulp', 'S09', r(DROP9 + 0.12), 0.25)


# 10: all the cars went through. Low beside the light: every car shoots past, one after the other, speed lines, his hair whipped in the bottom hole,
#     the light rattling; deadpan
#     (stills 2: one car in the frame, his face a speck in a light at the edge) from across the lane, the light nearer: his green face in the bottom
#     hole, the lorry first, then a car every fifth of a second, streaking between us and him all through the shot
D10 = st.dur('S10')
STREAM = [('truck', '#2F6FB2'), ('car', '#F5C33B'), ('car', '#5FB86A'), ('car', '#C255C8'), ('car', '#E8463A'), ('car', '#F08A3C'), ('car', '#3A9BDC'), ('car', '#8C949A')]
CROSS = lambda i: r(0.05 + 0.19 * i)                                     # when vehicle i crosses the line from the camera through the light (z 3.2, behind it), at 57 m/s
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(0), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'wind': [-6.0, 0.5, -10.0], 'hairUp': 0.9, 'face': DEAD}), toonDur=0.0),
            *[k(r(CROSS(i) + 0.03), toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'wind': [-6.0, 0.5, -10.0], 'hairUp': (1.0 if i % 2 else 0.8), 'sq': ([1.01, 0.99, 1.01] if i % 2 else [1.0, 1.0, 1.0]), 'face': DEAD}), toonDur=0.08) for i in range(len(STREAM))],   # each car's wind
            k(1.2, toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'hairUp': 0.9, 'face': {'lid': 1.0}}), toonDur=0.08), k(1.3, toon=IN({'skin': SKIN(GREEN, 1.0, 0.7), 'hairUp': 0.9, 'face': DEAD}), toonDur=0.1)])],
        props=[P('light10', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[CROSS(i), 0.02] for i in range(0, len(STREAM), 2)], 'open': [[0.0, 0]]}), P('glow10', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#44FF55', 'k': 3, 'dist': 4}),
               *[P(f'veh10{i}', kind_, pos=[2.2, 0, r(3.2 - 57.0 * CROSS(i))], ry=-90, opts={'color': c_}, keys=[k(0.0, to=[2.2, 0, r(3.2 + 57.0 * (D10 - CROSS(i)))], dur=D10, ease='linear')]) for i, (kind_, c_) in enumerate(STREAM)],
               P('spd10', 'speedLines', pos=[2.2, 1.2, 3.2], face='camera', opts={'n': 9, 'len': 2.4, 'w': 1.4, 'angle': 0.0, 'soft': True, 'taper': True, 'alpha': 0.6, 'at': [[0.0, D10]]})],
        cams=[FC(0.0, [6.8, 1.6, -3.8], [[LIGHT[0], r(POLE + 1.75), r(LIGHT[2] - 0.17)], [LIGHT[0], 0.3, LIGHT[2]], [2.2, 1.6, 3.2], [2.2, 0.2, 3.2]], top=0.1, bottom=0.8)])   # (stills 2) 33 degrees off the light's axis; (stills 3) from the pavement: the cars streak behind the light (across the lane they filled the lens)
st.cue('whoosh', 'S10', 0.05, 0.4, 1.2, 200, 1400); st.cue('sfx:engine', 'S10', 0.1, 0.3)


# 11: the town hall painted him red again. A painter on a ladder in front of the light rolls his green face red, stroke by stroke, his eyes shutting at
#     each stroke; the cars stop again behind; deadpan (REPEINT)
#     (stills 2: the car that stops was out of the frame) a second shot to end on: from the street, the light with his red face in the green hole, the
#     painter on his ladder looking at us, and the next car braking hard at the light, nose down
D11 = st.dur('S11'); STROKES = [0.3, 0.62, 0.94]; CUT11 = 1.55; BRAKE11 = 1.95
LAD = [r(LIGHT[0] + 0.85), 0, r(LIGHT[2] - 0.55)]                          # (stills 1) beside the light: in front of it the painter hid his face; (stills 4) on its pavement side, clear of the shot from the road
ROLL = lambda dy: {'reach': {'R': [LIGHT[0], r(HOLE(0)[1] + dy), r(LIGHT[2] - 0.3), 1, 0.05], 'L': [r(LIGHT[0] + 0.3), 1.9, r(LAD[2] + 0.1), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
COLS = ['#8FCB3A', '#E0A22A', RED]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(0), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(GREEN, 1.0, 0.6), 'face': DEAD}), toonDur=0.0),
            *[k(t_, toon=IN({'skin': SKIN(COLS[i], 1.0, 0.6), 'face': {'lid': 1.0}}), toonDur=0.06) for i, t_ in enumerate(STROKES)],   # each stroke: his eyes shut, a colour nearer red...
            *[k(r(t_ + 0.12), toon=IN({'skin': SKIN(COLS[i], 1.0, 0.6), 'face': DEAD}), toonDur=0.08) for i, t_ in enumerate(STROKES)],
            k(1.7, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'sq': [1.0, 1.006, 1.0], 'face': DEAD}), toonDur=0.3), k(2.1, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'face': {'lid': 1.0}}), toonDur=0.14), k(2.35, toon=IN({'skin': SKIN(RED, 1.0, 0.6), 'face': DEAD}), toonDur=0.15)]),   # ...red again; a slow blink
        act('peintre', [LAD[0], 0.9, r(LAD[2] - 0.2)], -60, 'stand', 'neutral', keys=[k(0.0, look=HOLE(0)), k(0.0, toon={**ROLL(0.3), 'face': {'lid': 0.5, 'gy': 0.2}}, toonDur=0.0),
            *[k(r(t_ - 0.12), toon={**ROLL(0.28), 'face': {'lid': 0.5}}, toonDur=0.1) for t_ in STROKES], *[k(t_, toon={**ROLL(-0.22), 'face': {'lid': 0.5}}, toonDur=0.12, toonEase='inOut') for t_ in STROKES],   # the roller up and down his face
            k(1.3, toon={**ROLL(0.0), 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.2), k(1.35, look='camera')])],
        props=[P('light11', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'open': [[0.0, 0]]}), P('lad11', 'ladder', pos=LAD, ry=20, opts={'h': 2.2, 'lean': 0.18}),
               P('roller11', 'paintRoller', on={'actor': 'peintre', 'hand': 'R'}, opts={'len': 0.5, 'color': RED}),
               *[P(f'car11{i}', 'car', pos=[x_, 0, z_], ry=-90, opts={'color': c_}) for i, (x_, z_, c_) in enumerate(CARS) if i != 5],   # (stills 4) the queue again: the second shot is the long lens of S06
               P('car11', 'car', pos=[2.2, 0, -44.0], ry=-90, opts={'color': '#F08A3C'}, keys=[k(r(BRAKE11 - 0.35), to=[2.2, 0, -31.0], dur=0.35, ease='out'), k(BRAKE11, squash=[1.0, 0.86, 1.06], dur=0.4)]),   # ...its last car braking hard into place, nose down
               P('glow11', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4, 'at': 0.94})],
        cams=[FC(0.0, [4.9, 2.1, -3.4], [[LIGHT[0], r(POLE + 1.75), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.2), r(LIGHT[2] - 0.17)], [LAD[0], 2.8, r(LAD[2] - 0.2)], [LAD[0], 0.9, r(LAD[2] - 0.2)]], top=0.12, bottom=0.76, drift=(0.04, 0.0, -0.04)),
              cam(CUT11, [0.8, 2.6, -62.0], [0.8, 2.6, -60.5], [3.4, 2.6, 0.0], [3.4, 2.6, 0.0], lens=9)])   # (stills 4) ...cut to the long lens of S06: the queue stopped again at his red light, its last car braking into place (a vertical frame cannot hold the light and a car side by side up close: from behind, beside or across, the car filled it)
for t_ in STROKES: st.cue('sfx:squeak', 'S11', t_, 0.15)
st.cue('sfx:brake', 'S11', r(BRAKE11 - 0.25), 0.3)


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
