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
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.32: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56, 'hold': hold})   # (review 2) hold: how long it stays
STREET = {'eiffelStyle': 'v2', 'clear': [-16.0, 4.0]}                     # no tree or lamp on the right pavement where he sits or the light stands
RED = '#FF4FA8'; GREEN = '#3FE04A'                                       # (review 1) a crimson-pink sunburn: the orange-red matched his tie (hands on the tie made a red cross); (review 2) pinker still (hue 348: at 359 the face and the tie were one red column)
SKIN = lambda col, k_=1.0, glow=0.0, fill=1.0: {'color': col, 'k': k_, 'glow': glow, 'fill': fill}   # (cycle 24) the skin channel

# 1: the hook. In a deckchair on the pavement, a blazing cartoon sun down the street: content, he basks; he goes red like a thermometer filling, his
#    hands, then his neck, then his whole head; steam puffs out of his ears; deadpan
#    (stills 2: turned to the sun, we saw his tilted head from behind and small, the sitting arms stuck out like a sleepwalker's) turned up the street
#    toward us, the sun down the street beyond him, his hands folded on his belly, a closer camera from the pavement
D1 = st.dur('S01')
ME = [5.2, 0, -12.0]; RY = 10                                            # on the right pavement ((stills 2) turned up the street, toward the camera: the sun is down the street behind him)
SEATED = [ME[0], -0.15, ME[2]]                                           # the deckchair's seat is lower than a chair's
LOUNGE = {'bend': {'spine': [-0.42, 0, 0, 1, None], 'neck': [0.12, 0, 0, 1, None]},
          'touch': {'L': ['torso', 0.3, 0.1, 0.1, 1, 0.03], 'R': ['torso', -0.3, 0.1, 0.1, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}}   # (review 1) hands on the deckchair's frame beside his hips: folded on his belly they lay on the tie
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEATED, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'face': {'lid': 0.75, 'mouth': 'smile', 'cheeks': 0.4}}, toonDur=0.0),
            k(0.25, toon={**LOUNGE, 'skin': SKIN(RED, 0.6, 0.0, 0.4), 'face': {'lid': 0.7, 'mouth': 'smile', 'cheeks': 0.4}}, toonDur=0.18),   # his hands go red...
            k(0.5, toon={**LOUNGE, 'skin': SKIN(RED, 0.8, 0.0, 0.8), 'face': {'lid': 0.6, 'mouth': 'smile'}}, toonDur=0.18),   # ...his neck...
            k(0.62, toon={**LOUNGE, 'skin': SKIN(RED, 0.8, 0.0, 0.8), 'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.14),   # (review 1) the smile sags first...
            k(0.78, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.1, 1.0), 'face': {'lid': 0.45, 'mouth': 'line', 'gy': -0.4}}, toonDur=0.34, toonEase='linear'),   # ...then a level climbs his face from the chin to the crown in ten frames, his eyes going up with it...
            k(1.14, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15, 1.0), 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.45, 'mouth': 'line', 'steam': 1.0}}, toonDur=0.06, toonEase='out'),   # ...steam puffs out of his ears
            k(1.45, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15, 1.0), 'face': {'lid': 0.45, 'mouth': 'line', 'steam': 1.0}}, toonDur=0.15)])],
        props=[P('chair1', 'deckChair', pos=ME, ry=RY), P('sun1', 'sun', pos=[2.4, 4.4, -19.0], opts={'r': 1.1}, keys=[k(0.0, scale=1.0, dur=0.0), k(0.9, scale=1.12, dur=0.25, ease='inOut')])],   # (stills 1) nearer: in the corner of a closer frame
        cams=[FC(0.0, [6.9, 1.0, -9.6], [[ME[0], 1.8, r(ME[2] - 0.1)], [ME[0], 0.35, r(ME[2] + 0.5)], [r(ME[0] - 0.4), 0.9, ME[2]], [r(ME[0] + 0.4), 0.9, ME[2]], [2.4, 4.4, -19.0]], top=0.06, bottom=0.8, drift=(-0.06, 0.0, -0.06))])   # (stills 2) in front of him from the pavement, the sun beyond him
st.cue('sfx:static', 'S01', 0.3, 0.12); st.cue('sfx:static', 'S01', 1.12, 0.22)

# 2: he turned bright red. Close on his red face: a boy beside the deckchair cracks an egg on his forehead; the egg fries there, bubbling, steam
#    rising; his eyes roll up to it, deadpan
#    (review 1: a medium shot; no egg seen in her hand, a straight arm sweeping past his mouth, CRAC small and away from the impact, his eyes aside) a
#    real close-up (his head about 38 % of the frame): her hand comes in from the right on an arc with a big egg in it, a contact frame with the two half
#    shells springing apart and CRAC big at the impact; the white spreads and the yolk swells while his eyes roll up and cross toward it
D2 = st.dur('S02'); CRACK2 = 0.42
GAM2 = [5.3, 0, -12.62]                                                   # (stills 1) the neighbour at his side, her hand at his forehead height (the boy's arm stretched like a pole); (stills 2) at his left, the camera side; (stills p2) behind the deckchair: from his side her arm crossed his face at the crack
FORE2 = [5.24, 1.32, -11.78]                                             # his forehead, seated and leaning back ((stills 2) turned up the street)
ARC2 = lambda t_: [r(FORE2[0] - 0.42 + 0.44 * t_), r(FORE2[1] + 0.72 - 0.62 * t_ + 0.1 * math.sin(PI * t_)), r(FORE2[2] + 0.3 - 0.27 * t_)]   # (review 2: an empty fist, her forearm over his forehead at the contact) from high at the left of the frame, in front of her, down onto the top of his forehead   # (review 1) her hand on an arc; (stills p2) from high above his head straight down onto his forehead, a tall neighbour behind him: her arm over his head, clear of his eyes
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEATED, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {**DEAD, 'gx': 0.35}}, toonDur=0.0),   # his eyes on the egg coming
            k(r(CRACK2 + 0.02), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 1.0}}, toonDur=0.03),   # CRAC: a blink...
            k(r(CRACK2 + 0.14), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {'lid': 0.15, 'gy': -0.95, 'gx': 0.0, 'cross': 0.55, 'eye': 0.25}}, toonDur=0.1),   # ...his eyes roll up and cross toward the egg frying on his forehead...
            k(r(CRACK2 + 0.75), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': {'lid': 0.3, 'gy': -0.9, 'gx': 0.0, 'cross': 0.6, 'eye': 0.2}}, toonDur=0.25), k(r(D2 - 0.2), toon={**LOUNGE, 'skin': SKIN(RED, 1.0, 0.15), 'face': DEAD}, toonDur=0.14)]),   # ...held, then deadpan
        act('voisine', GAM2, 15, 'stand', 'happy', keys=[k(0.0, look=[FORE2[0], FORE2[1], FORE2[2]]),
            k(0.0, toon={'reach': {'L': ARC2(0.0) + [1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.6}}, toonDur=0.0),   # the egg up beside his head, in the frame...
            k(0.12, toon={'reach': {'L': ARC2(0.45) + [1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.7}}, toonDur=0.14, toonEase='in'),   # ...over the top of the arc...
            k(r(CRACK2 - 0.06), toon={'reach': {'L': ARC2(1.0) + [1, 0.03]}, 'hands': {'L': 'grip'}, 'sq': [1.04, 0.96, 1.04], 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.8}}, toonDur=0.06, toonEase='in'),   # ...CRAC on his forehead...
            k(r(CRACK2 + 0.2), toon={'reach': {'L': [r(FORE2[0] + 0.25), r(FORE2[1] + 0.55), r(FORE2[2] - 0.3), 1, 0.05]}, 'hands': {'L': 'open'}, 'sq': [0.96, 1.05, 0.96], 'face': {'mouth': 'laugh', 'lid': 0.0, 'eye': 0.4, 'brow': 1.0}}, toonDur=0.12, toonEase='out')])],   # ...delighted, her hand back up
        props=[P('chair2', 'deckChair', pos=ME, ry=RY),
               P('egg2', 'friedEgg', on={'actor': 'voisine', 'hand': 'L', 'offset': [0.0, 0.07, 0.07]}, opts={'at': CRACK2, 'r': 0.078, 'dur': 1.2, 'wholeR': 1.0, 'shellSpread': 2.6}, keys=[k(CRACK2, attach='mec', joint='head', offset=[0.0, 0.47, 0.088], rot=[round(PI / 2, 4), 0.0, 0.0])]),   # (review 2) a big white egg out of her fist, the shells thrown clear, the white high on the forehead (it covered his left eye)   # (stills 2) flat on the front of his head above the eyes; (review 1) a big whole egg in her hand, half shells at the crack
               BURST('crac2', [r(FORE2[0] + 0.4), r(FORE2[1] + 0.26), r(FORE2[2] - 0.14)], CRACK2, 'CRAC !', 0.36, hold=0.12)],   # (review 2) beside the impact against the facade, five frames (held fourteen it hid the landing)   # (review 1) at the impact, at TUUUT's scale (it was small, 0.2 m away); (stills p2) on the other side of the impact from her arm
        cams=[FC(0.0, [5.95, 1.45, -10.75], [[FORE2[0], r(FORE2[1] + 0.5), FORE2[2]], [FORE2[0], r(FORE2[1] - 0.4), r(FORE2[2] + 0.08)], [r(FORE2[0] + 0.28), r(FORE2[1] + 0.1), FORE2[2]], [r(FORE2[0] - 0.3), r(FORE2[1] + 0.1), FORE2[2]]],
                 top=0.08, bottom=0.74, lenses=range(26, 57), drift=(0.02, 0.0, 0.02))])   # (review 2) his head 35-40 % of the frame (it was a quarter): the egg comes in from the top left   # (review 1) a real close-up: his head and her hand's arc
st.cue('sfx:bonk', 'S02', CRACK2, 0.25); st.cue('sfx:static', 'S02', r(CRACK2 + 0.05), 0.3)

# 3: at night he lights up the whole neighbourhood. The street dark: he stands on the pavement glowing red, lighting the façades round him; moths
#    circle his head; a neighbour on a bench reads her paper by his light; a slow blink
#    (stills 2: in profile, the moths too small to see, the whole frame red without sky: a red room, not a night) down the street from the pavement:
#    the night sky over the end of the street, a pool of red round him fading into the blue dark, the moths two and a half times bigger, him three
#    quarters to us, the neighbour on her bench beside him
D3 = st.dur('S03')
NIGHT = {**STREET, 'night': True, 'lampsOff': True, 'windowsOff': True}  # (review 1) no street lamp, no lit window: he is the only light
NLOOK = {'sun': 0.12, 'sunColor': '#7F96D8', 'fill': 0.32, 'exposure': 0.9}   # (review 1) a darker night: his red light carries the street
ME3 = [5.5, 0, -12.0]; VOI3 = [6.32, 0, -11.52]                          # (stills 2) she sits at his left, turned like him toward us
PAPER3 = lambda gx: {'reach': {'R': [6.09, 1.05, -11.26, 1, 0.05], 'L': [6.33, 1.05, -11.18, 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.5, 'gy': 0.45, 'gx': gx}}
st.shot('S03', 'parisStreet', setOpts=NIGHT, look=NLOOK, actors=[
        act('mec', ME3, -30, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'skin': SKIN('#FFA0B8', 1.0, 1.0), 'face': DEAD}, toonDur=0.0),
            k(0.6, toon={'skin': SKIN('#FFA0B8', 1.0, 1.0), 'sq': [1.0, 1.012, 1.0], 'face': DEAD}, toonDur=0.3, toonEase='inOut'),   # (review 1) a paler, hotter pink-red core at night
            k(1.2, toon={'skin': SKIN('#FFA0B8', 1.0, 1.0), 'face': {'lid': 1.0}}, toonDur=0.14), k(1.45, toon={'skin': SKIN('#FFA0B8', 1.0, 1.0), 'sq': [1.0, 0.996, 1.0], 'face': DEAD}, toonDur=0.18)]),   # glowing, a slow blink
        act('voisine', VOI3, -20, 'sit', 'neutral', keys=[k(0.0, look=[6.21, 1.0, -11.2]), k(0.0, toon={**PAPER3(0.0), 'skin': SKIN('#FF8A96', 0.6)}, toonDur=0.0), k(0.9, toon={**PAPER3(0.05), 'skin': SKIN('#FF8A96', 0.6)}, toonDur=0.3)])],   # (review 2) her face and hands washed in his red (her painted face took no light at all)   # reading by his light ((review 1) her eyes stay on the paper)
        props=[P('glow3', 'glowLight', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.3, 0.4]}, opts={'color': '#FF3A4A', 'k': 11, 'dist': 9, 'at': -1.0}),   # (review 2) lit from the first frame (it switched on at the cut)   # (stills 2) a pool of red; (review 1) stronger and wider: the facades, the bench, her face and her paper in his red
               P('halo3', 'halo', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.25, -0.12], 'face': 'camera'}, opts={'r': 0.55, 'k': 0.42, 'core': '#FF8A9C', 'color': '#FF3A50', 'at': -1.0}),   # (review 2) dimmer than his face now (the face was darker than its own halo)   # (review 1) a burning outline behind his head: the hottest thing in the frame ((stills p2) smaller and softer: at 0.75 a red balloon)
               P('moths3', 'moths', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.7, 0.0]}, opts={'n': 7, 'r': 0.36, 'size': 1.0, 'basic': True, 'color': ['#B8A688', '#9E8E74']}, scale=2.2),   # (review 2) smaller, unlit grey-brown, circling wide round his head (lit red they read as birds; one sat on his head)   # (stills 2) big enough to see; (review 1) grey-brown moths with antennae, lit red
               P('bench3', 'bench', pos=[VOI3[0], 0, VOI3[2]], ry=-20), P('news3', 'glowPaper', on={'actor': 'voisine', 'hand': 'R', 'offset': [-0.12, 0.12, 0.06], 'face': 'camera'}, opts={'tint': '#FFC2CE'})],   # (review 2) an open paper, pale, in columns, lit pink (the old one was a black slab)
        cams=[FC(0.0, [4.7, 1.0, -6.6], [[ME3[0], 2.8, ME3[2]], [ME3[0], 0.0, ME3[2]], [VOI3[0], 1.5, VOI3[2]], [VOI3[0], 0.0, VOI3[2]], [3.0, 14.0, -60.0]], top=0.06, bottom=0.8, drift=(0.0, 0.0, -0.06))])   # (stills 2) the sky over the end of the street
st.cue('sfx:static', 'S03', 0.05, 0.08)


# 4: the town hall installed him... A crossroads: the mayor in his sash points at a traffic light with three empty holes; two workers carry him in,
#    stiff as a plank on their shoulders
#    (stills 2: from the side and far, the plank was a dark stroke between two small workers) from high behind them: the plank comes up the frame
#    toward the light, his red face up to us, the light at the top with its empty holes facing us, the mayor beside it pointing at the top one
D4 = st.dur('S04')
LIGHT = [4.3, 0, 0.0]; LRY = 180; POLE = 2.0                             # the light at the kerb, facing the cars coming up the street (+Z)
HOLE = lambda i: [LIGHT[0], r(POLE + [0.32, 0.85, 1.38][i]), r(LIGHT[2] - 0.17)]   # the holes (0 green at the bottom, 2 red at the top), seen from the front (-Z)
CARRY0 = [4.1, 1.62, -6.4]; CARRY1 = [4.1, 1.62, -4.9]                   # (stills 2) up the kerb to the light's front, his head first
#    (review 1: a dark bundle draped over one worker, his head against the mayor's sash, no face, the body swinging toward the vertical) from high and
#    close above the carry, almost looking down: the plank level on both workers' shoulders, his red face up against the pale pavement, rigid, a small
#    bob at each step, the light ahead at the top of the frame and the mayor's arm pointing at its top hole
BOB = lambda: [k(r(0.14 + 0.24 * j), to=[CARRY0[0], r(1.62 + (0.07 if j % 2 == 0 else 0.0)), r(CARRY0[2] + (CARRY1[2] - CARRY0[2]) * (0.14 + 0.24 * (j + 1)) / D4)], dur=0.24, ease='inOut', face='keep') for j in range(3)]
SHOULDER = {'touch': {'R': ['torso', -0.14, 0.9, 0.12, 1, 0.05], 'L': ['torso', 0.14, 0.9, 0.12, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.5, 'brow': -0.3}}
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', CARRY0, 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [round(-PI / 2, 4), 0.0], 'hip': 0, 'skin': SKIN(RED, 1.0, 0.2), 'face': DEAD}, toonDur=0.0),
            k(0.0, to=[CARRY0[0], 1.62, r(CARRY0[2] + (CARRY1[2] - CARRY0[2]) * 0.14 / D4)], dur=0.14, ease='linear', face='keep'), *BOB(),
            k(0.62, toon={'lay': [round(-PI / 2, 4), 0.0], 'hip': 0, 'skin': SKIN(RED, 1.0, 0.2), 'face': {'lid': 1.0}}, toonDur=0.06), k(0.72, toon={'lay': [round(-PI / 2, 4), 0.0], 'hip': 0, 'skin': SKIN(RED, 1.0, 0.2), 'face': DEAD}, toonDur=0.08)]),   # carried flat on his back, stiff as a board, his face up to us, a blink
        act('ouv1', [CARRY0[0], 0, r(CARRY0[2] + 1.5)], 0, 'stand', 'neutral', keys=[k(0.0, to=[CARRY1[0], 0, r(CARRY1[2] + 1.5)], dur=D4, clip='walk', then='stand', ease='linear', face='keep'), k(0.0, toon=SHOULDER, toonDur=0.0)]),   # under his shoulders...
        act('ouv2', [CARRY0[0], 0, r(CARRY0[2] + 0.35)], 0, 'stand', 'neutral', keys=[k(0.0, to=[CARRY1[0], 0, r(CARRY1[2] + 0.35)], dur=D4, clip='walk', then='stand', ease='linear', face='keep'), k(0.0, toon=SHOULDER, toonDur=0.0)]),   # ...and under his shins
        act('maire', [5.35, 0, -0.95], -160, 'stand', 'determined', keys=[k(0.0, look=[LIGHT[0], 3.4, LIGHT[2]]), k(0.0, toon={'reach': {'L': [4.75, 3.3, -0.5, 1, 0.08]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.4, 'brow': -0.2, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.35, look='camera'), k(0.4, toon={'reach': {'L': [4.75, 3.36, -0.5, 1, 0.08]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.3, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.1)])],   # the mayor points at the top hole, pleased
        props=[P('light4', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True})],
        cams=[FC(0.0, [0.9, 4.2, -7.9], [[LIGHT[0], r(POLE + 1.6), r(LIGHT[2] - 0.2)], [CARRY0[0], 1.7, r(CARRY0[2] - 0.15)], [CARRY0[0], 1.7, r(CARRY0[2] + 2.0)], [CARRY0[0], 0.0, r(CARRY0[2] + 0.35)], [CARRY0[0], 0.0, r(CARRY0[2] + 1.5)]], top=0.08, bottom=0.8, drift=(0.0, 0.0, 0.2))])   # (review 2: from above, down the line of the walk, the plank hid between the two hard hats) high three-quarter from the road: the plank across the frame on the shoulders, head and shoes past the workers, the light behind   # (stills p2) tighter on the plank: the light's top hole the top of the frame   # (review 1) high and close, nearly looking down on the plank, the light at the top

# 5: ...as a red light. Close on the light: his face pops up into the top hole, red, glowing, overshooting and settling; deadpan (FEU ROUGE)
#    (stills 2: his head 18 cm under the hole's centre and 8 cm aside (his weight shift at rest), the sky through the open back round it) his feet
#    1.99 m under the hole's centre (measured with debugJoints), no weight shift, the head widened to fill the round hole, a dark back in the box
D5 = st.dur('S05')
BEHIND = lambda i: [LIGHT[0], r(POLE + [0.32, 0.85, 1.38][i] - 1.99), r(LIGHT[2] + 0.08)]   # where he stands for his head to fill hole i ((stills 2) measured: the head's centre 1.99 m over his feet)
FILL = {'head': [1.85, 0.97, 1.0]}                                       # (stills 2) his head widened to fill the round hole (at its own width the dark showed at its sides)
IN = lambda d, scl=None: {'hip': 0, 'headOnly': 1, **d, 'scl': (scl or FILL)}   # (stills 2) in the light: no weight shift at rest, the head filling the hole; (review 1) his head alone (his shirt, legs and hands showed through the holes and the walls)
#    (review 1: the stretched head up for four frames, then spread and settled at once) an anticipation, then up past the hole and HELD at the top six
#    frames (a glance down), the drop into it like a smear, a squash past the rim on the landing, and the face filling out over five frames
OVER5 = [BEHIND(2)[0], r(BEHIND(2)[1] + 0.3), BEHIND(2)[2]]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BEHIND(2)[0], r(BEHIND(2)[1] - 0.3), BEHIND(2)[2]], LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': DEAD}, {'head': [1.0, 1.0, 1.0]}), toonDur=0.0),   # (review 2) his crown already in the bottom of the hole...
            k(0.0, to=[BEHIND(2)[0], r(BEHIND(2)[1] - 0.36), BEHIND(2)[2]], dur=0.09, ease='in', face='keep'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': DEAD}, {'head': [1.25, 0.8, 1.0]}), toonDur=0.09, toonEase='in'),   # ...a squash down for three frames to wind up...
            k(0.12, to=OVER5, dur=0.1, ease='out', face='keep'), k(0.12, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': {'lid': 0.2, 'brow': 0.5}}, {'head': [0.78, 1.32, 1.0]}), toonDur=0.05, toonEase='out'),   # ...POP: up past the hole, stretched...
            k(0.2, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': {'lid': 0.2, 'brow': 0.4}}, {'head': [0.92, 1.12, 1.0]}), toonDur=0.08),   # ...hanging up there...
            k(0.28, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': {'lid': 0.25, 'gy': 0.7}}, {'head': [0.92, 1.12, 1.0]}), toonDur=0.06),   # ...a glance down at the hole...
            k(0.41, to=[BEHIND(2)[0], BEHIND(2)[1], r(BEHIND(2)[2] - 0.14)], dur=0.08, ease='in', face='keep'), k(0.41, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': {'lid': 0.3}}, {'head': [0.78, 1.3, 1.0]}), toonDur=0.05, toonEase='in'),   # ...down into it like a smear, (review 2) forward...
            k(0.49, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': {'lid': 0.6}}, {'head': [2.1, 0.8, 1.0]}), toonDur=0.03, toonEase='out'),   # ...splat bulging out in front of the rim (behind it the ring cut across his face)...
            k(0.56, to=BEHIND(2), dur=0.12, ease='inOut', face='keep'), k(0.56, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': DEAD}, {'head': [1.6, 1.06, 1.0]}), toonDur=0.08, toonEase='out'),   # ...back into the hole, filling out over five frames...
            k(0.66, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': DEAD}), toonDur=0.08),   # ...and settled: a red light
            k(0.86, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': {'lid': 1.0}}), toonDur=0.06), k(0.96, toon=IN({'skin': SKIN(RED, 1.0, 0.5), 'face': DEAD}), toonDur=0.1)])],   # a blink
        props=[P('light5', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[0.49, 0.03]]}), P('glow5', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4, 'at': 0.1}),
               BURST('pop5', [r(LIGHT[0] - 0.62), r(HOLE(2)[1] + 0.02), r(LIGHT[2] - 0.4)], 0.12, 'POP !', 0.45)],   # (review 1) at the hole, at TUUUT's scale, below the title card's band
        cams=[FC(0.0, [LIGHT[0], 3.0, -2.7], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.4), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.5), r(POLE + 1.0), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 1.0), r(LIGHT[2] - 0.17)]], top=0.2, bottom=0.74, drift=(0.0, 0.0, 0.08))])
st.cue('sfx:poof', 'S05', 0.12, 0.3)


# 6: the cars stop in front of him... From far down the street on a long lens: a queue of cars to the light at the end, his red face glowing over them
D6 = st.dur('S06')
MUTE = {'#3A9BDC': '#5B8DB4', '#F5C33B': '#D6B25E', '#5FB86A': '#6F9E78', '#C255C8': '#97709C', '#E8463A': '#BE6258', '#F08A3C': '#C88A5C', '#8C949A': '#8C949A'}   # (review 2) the series' muted car colours (saturation 0.4-0.6)
CARS = [(2.2, -3.0, '#3A9BDC'), (2.2, -8.6, '#F5C33B'), (2.2, -14.2, '#5FB86A'), (2.2, -19.8, '#C255C8'), (2.2, -25.4, '#E8463A'), (2.2, -31.0, '#F08A3C'), (-1.6, -5.0, '#8C949A'), (-1.6, -10.6, '#3A9BDC'), (-1.6, -16.2, '#F5C33B'), (-1.6, -21.8, '#5FB86A')]
CARS += [(2.2, r(-36.6 - 5.6 * i), c_) for i, c_ in enumerate(['#8C949A', '#3A9BDC', '#F5C33B', '#5FB86A', '#C255C8', '#E8463A', '#F08A3C', '#3A9BDC'])] + [(-1.6, r(-27.4 - 5.6 * i), c_) for i, c_ in enumerate(['#E8463A', '#8C949A', '#F08A3C', '#5FB86A'])]   # (review 1) the queue to the end of the street
CARS = [(x_, z_, MUTE[c_]) for x_, z_, c_ in CARS]
QUEUE = lambda sid, extra=lambda i: {}, skip=(): [P(f'car{sid}{i}', 'car', pos=[x_, 0, z_], ry=-90, opts={'color': c_, 'glass': 0.85, 'glassColor': '#33485A', 'brake': True}, **extra(i)) for i, (x_, z_, c_) in enumerate(CARS) if i not in skip]   # (pass 3) brake lights lit   # (review 1) tinted windows: see-through cars stacked into one cage down a long lens
# (pass 3: from 10.5 m up the queue was a staircase of coloured slabs, the roofs only, and nothing moved for 1.27 s) the classic long lens of a jam:
#     from the road at 2.6 m, past the end of the queue, so the cars show their rear windows and their lit tail lights, one lane stacked up to the
#     light; the queue creeps forward in a wave from the front car back, each car dipping its nose as it stops; a red halo round his face
RLANE = sorted([i for i, (x_, z_, c_) in enumerate(CARS) if x_ > 0], key=lambda i: -CARS[i][1])   # the right lane, front car first
def CREEP(t0, gap=0.07, d=0.6, skip=()):
    """(pass 3) the queue inches forward d metres in a wave from the front car back (one car every `gap` s), each nose dipping as it stops (unused)"""
    out = {}
    for n, i in enumerate([j for j in RLANE if j not in skip]):
        x_, z_, c_ = CARS[i]; t = r(t0 + gap * n); YAW = round(-PI / 2, 4)
        out[i] = [k(t, to=[x_, 0, r(z_ + d)], dur=0.3, ease='inOut'), k(r(t + 0.27), rot=[0.0, YAW, -0.05], dur=0.05, ease='out'),
                  k(r(t + 0.32), rot=[0.0, YAW, 0.02], dur=0.1, ease='inOut'), k(r(t + 0.44), rot=[0.0, YAW, 0.0], dur=0.1, ease='inOut')]
    return out
def STOPS(t0, gap=0.06, lanes=(2.2, -1.6), hard=1.0):
    """(review 2: from behind the queue the cars were roof slabs, a rainbow of bars) the cars come up the street and stop at the light one after another,
    the front car first: each decelerates into its place and dips its nose toward us, a bounce after; seen from behind the light, their fronts"""
    out = {}; order = sorted(range(len(CARS)), key=lambda i: -CARS[i][1])
    for n, i in enumerate(order):
        x_, z_, c_ = CARS[i]; t = r(t0 + gap * n); YAW = round(-PI / 2, 4); dip = r(-0.07 * hard, 3)
        out[i] = {'pos': [x_, 0, r(z_ - 6.0 * t)], 'keys': [k(0.0, to=[x_, 0, z_], dur=max(0.05, t), ease='out'), k(r(max(0.0, t - 0.03)), rot=[0.0, YAW, dip], dur=0.05, ease='out'),
                  k(r(t + 0.08), rot=[0.0, YAW, r(0.035 * hard, 3)], dur=0.1, ease='inOut'), k(r(t + 0.2), rot=[0.0, YAW, 0.0], dur=0.12, ease='inOut')]}
    return out
QUEUE2 = lambda sid, t0, skip=(), hard=1.0: [P(f'car{sid}{i}', 'car', pos=st_['pos'], ry=-90, opts={'color': CARS[i][2], 'glass': 0.85, 'glassColor': '#33485A'}, keys=st_['keys']) for i, st_ in STOPS(t0, hard=hard).items() if i not in skip]
JAMCAM = lambda t=0.0: cam(t, [5.0, 9.0, 9.0], [5.0, 8.9, 8.6], [2.2, 0.6, -16.0], [2.2, 0.6, -16.0], lens=34)   # (review 2) from high behind the light, down the street: the car fronts, bonnets and windscreens to the end of the street
HALOB = lambda sid, at=-1.0: P(f'halob{sid}', 'halo', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] + 0.45)], face='camera', opts={'r': 0.85, 'k': 0.8, 'core': '#FF8A9C', 'color': '#FF3A50', 'at': at})   # his red glow round the back of the light
PUFFS = lambda sid: [P(f'exh{sid}{n}', 'dustPuff', pos=[2.2, 0.35, r(CARS[i][1] - 2.15)], scale=0.6, opts={'period': 0.7, 'color': '#C8CCD2', 'seed': 640 + n}) for n, i in enumerate(RLANE[-6:])]   # exhaust on the near cars
HALO = lambda sid, at=0.0: P(f'halo{sid}', 'halo', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.35)], face='camera', opts={'r': 0.75, 'k': 0.75, 'core': '#FFE6E0', 'color': '#FF3A50', 'at': at})   # his glow read 110 m away
HEADON = lambda col=RED, glow=0.7, i=2: act('mec', BEHIND(i), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(col, 1.0, glow), 'face': DEAD}), toonDur=0.0),
                                                                  k(0.6, toon=IN({'skin': SKIN(col, 1.0, glow), 'face': {'lid': 1.0}}), toonDur=0.1), k(0.78, toon=IN({'skin': SKIN(col, 1.0, glow), 'face': DEAD}), toonDur=0.12)])   # (audit) a blink in the long hold
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[HEADON()],
        props=[P('light6', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('glow6', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.9)], opts={'color': '#FF4A2A', 'k': 5, 'dist': 7}), HALOB('6'),
               *QUEUE2('6', 0.1)],   # (review 2) the cars come up and stop at his red one after another, the first one's nose at the light, its bonnet in his red
        cams=[JAMCAM()])   # (pass 3) from the road; (stills p2) from beyond the end of the queue: nearer, its last cars filled the frame as blocks   # a long lens down the queue: the light at its head; (review 1) from higher and tighter: the roofs to the end of the street, the light big in the top third

# 7: ...all day long. The light against the sky: the sun races across behind him and goes down; he glows on, deadpan, a slow blink
#    (stills 2: from under the box his face was a red sliver in the top hole) in front of the light, a little below it: his face in the top hole, the
#    sky over the box, the sun rising at the left, crossing over the top of the light and setting behind the houses at the right
D7 = st.dur('S07')
SUNPATH = [[0.0, -3.4, 7.0, 24.0], [r(D7 * 0.25), 0.4, 16.5, 24.0], [r(D7 * 0.5), 4.2, 21.5, 24.0], [r(D7 * 0.75), 8.0, 15.0, 24.0], [D7, 11.4, 2.5, 24.0]]   # (review 1) it ends down behind the houses (it slid off in front of the facade)
#    (review 1: the sun slid off in front of the facade, the sky never changed, his glow did not grow and his eyes did not move) dusk falls over the
#    second half (the picture darkens, a pool of light stays round his face), the sun sets behind the roofs, his glow and its halo swell, his eyes
#    follow the sun up and over
EYE7 = [(0.0, 0.55, -0.2), (r(D7 * 0.3), 0.25, -0.5), (r(D7 * 0.55), -0.2, -0.52), (r(D7 * 0.8), -0.55, -0.3)]   # (review 2) not so far up: at -0.75 the pupils went under the lids
st.shot('S07', 'parisStreet', setOpts=STREET, dark=[[0.0, 0.0], [r(D7 * 0.42), 0.6, r(D7 * 0.55)]], darkTint='#2B2A5C', darkFloor=0.18,
        darkPool={'actor': 'mec', 'joint': 'head', 'lift': [0.0, 0.25, -0.1], 'r': 1.1, 'k': [[0.0, 1.0]], 'tint': '#FF9AA6'}, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': {**DEAD, 'gx': EYE7[0][1], 'gy': EYE7[0][2]}}), toonDur=0.0),
            *[k(t_, toon=IN({'skin': SKIN(RED, 1.0, r(0.45 + 0.55 * j / 3)), 'face': {'lid': 0.35, 'gx': gx_, 'gy': gy_}}), toonDur=0.2, toonEase='inOut') for j, (t_, gx_, gy_) in enumerate(EYE7[1:], 1)],   # his eyes follow the sun, his glow swelling...
            k(r(D7 - 0.3), toon=IN({'skin': SKIN(RED, 1.0, 1.0), 'face': {'lid': 1.0}}), toonDur=0.1), k(r(D7 - 0.14), toon=IN({'skin': SKIN(RED, 1.0, 1.0), 'face': DEAD}), toonDur=0.12)])],   # ...a slow blink at nightfall
        props=[P('light7', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True}), P('sun7', 'sun', opts={'r': 1.3}, **FLY(SUNPATH)),   # (review 2) not inDark: drawn over the darkened picture it slid down in front of the facade instead of behind the roofs   # (stills 1) no cars: the first one filled the side of the frame
               P('glow7', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A5A', 'k': 2.5, 'dist': 5}), P('glow7b', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A5A', 'k': 6, 'dist': 6, 'at': r(D7 * 0.5)}),
               P('halo7', 'halo', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] + 0.12)], face='camera', inDark=True, opts={'r': 0.7, 'k': 0.85, 'at': r(D7 * 0.5), 'core': '#FFE6E0', 'color': '#FF3A50'})],   # (review 1) the burning outline as night falls
        cams=[FC(0.0, [4.1, 1.7, -4.8], [[LIGHT[0], 3.95, LIGHT[2]], [LIGHT[0], r(POLE + 0.6), r(LIGHT[2] - 0.17)], [4.2, 21.5, 24.0], [4.2, 23.0, 24.0]], top=0.06, bottom=0.78)])   # (stills 2) his face in the top hole, the sun's arc over the box


# 8: yesterday a lorry honked at him. Side on across the road: the lorry at the head of the queue blasts its horns: TUUUT, the blast hits his face:
#    flattened wide in the hole, eyes bulging, hair blown back, the light rattling
#    (stills 2: the light cut by the edge of the frame, the lorry's side filling the rest) two shots: the lorry rolls up to the light and stops nose
#    down, its horns seen from beside the light: TUUUT; cut to his face in the hole, flattened by the blast, the wind lines coming from the side
#    (review 1: the lorry a blue wall side-on, the horns a sliver; the face hardly flattened, no pre-take, no hair streaming, the wind lines on the
#    wrong holes) the lorry from low in front, three-quarter: its grille, its driver, two big chrome trumpets against the sky, nose dipping as it
#    stops: TUUUT; cut to his face: two frames of narrowing eyes, then the blast squashes it flat and wide past the rim, cheeks rippling, hair streaming
#    sideways, wind lines hitting it, the light rocking; then it pops back with an overshoot, his hair left frazzled
D8 = st.dur('S08'); HONK8 = 0.36; CUT8 = 0.72; BLAST8 = 0.79; BACK8 = 1.24   # (review 2) TUUUT eleven frames on the lorry before the cut (it had four)
TRUCK = [2.2, 0, -4.4]
BLASTF = lambda i: IN({'skin': SKIN(RED, 1.0, 0.45), 'wind': [-15.0, 0.6, 0.0], 'hairUp': 1.0, 'face': {'lid': 0.0, 'pop': 0.32, 'popLen': (0.06 if i % 2 else 0.045), 'eyeScale': 1.2, 'pupilSize': -0.3, 'brow': 1.0, 'mouth': 'O', 'tremble': 1.0, 'cheeks': (1.0 if i % 2 else 0.2), 'puff': (0.0 if i % 2 else 0.6)}},
                      ({'head': [1.72, 0.72, 0.5]} if i % 2 else {'head': [1.8, 0.7, 0.48]}))   # (review 2) inside the box: at 2.8 wide red blocks poked out of its sides
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': {**DEAD, 'gx': 0.6}}), toonDur=0.0),
            k(CUT8, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': {'lid': 0.62, 'gx': 0.6, 'brow': -0.5}}), toonDur=0.05),   # two frames of narrowing eyes...
            k(BLAST8, to=[BEHIND(2)[0], r(BEHIND(2)[1] + 0.06), BEHIND(2)[2]], dur=0.03, ease='out', face='keep'), k(BLAST8, toon=BLASTF(0), toonDur=0.03, toonEase='out'),   # ...WHAM: flattened wide, (review 2) lifted to fill the hole (squashed toward his chin the top of the hole was black)...
            *[k(r(BLAST8 + 0.05 + 0.05 * i), toon=BLASTF(i + 1), toonDur=0.04) for i in range(10)],   # ...held while the horn lasts, cheeks rippling, quivering...
            k(BACK8, to=BEHIND(2), dur=0.05, ease='out', face='keep'), k(BACK8, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.6, 'brow': 0.8, 'mouth': 'o'}}, {'head': [1.3, 1.3, 1.0]}), toonDur=0.05, toonEase='out'),   # ...POP back, past his size...
            k(r(BACK8 + 0.1), toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'hairUp': 0.95, 'face': {'lid': 0.1, 'eye': 0.5, 'brow': 0.7, 'mouth': 'o'}}), toonDur=0.1, toonEase='out')]),   # ...and settled, his hair frazzled
        ],
        props=[P('light8', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[BLAST8, 0.08], [r(BLAST8 + 0.3), 0.05]]}),
               P('truck8', 'truck', pos=[TRUCK[0], 0, -13.0], ry=-90, opts={'color': '#2F6FB2', 'hornLen': 1.1, 'honkAt': HONK8, 'honkDur': 0.62}, keys=[k(0.0, to=TRUCK, dur=0.28, ease='out'), k(0.25, rot=[0.0, round(-PI / 2, 4), -0.1], dur=0.06, ease='out'), k(0.33, rot=[0.0, round(-PI / 2, 4), 0.045], dur=0.1, ease='inOut'), k(0.45, rot=[0.0, round(-PI / 2, 4), -0.02], dur=0.1, ease='inOut'), k(0.57, rot=[0.0, round(-PI / 2, 4), 0.0], dur=0.1, ease='inOut')]),   # it rolls up and stops nose down, (review 2) harder, a bounce on its springs; the driver leans on the horn, the trumpets flare and ring
               P('blast8', 'speedLines', **FLY([[BLAST8, r(LIGHT[0] - 1.4), r(HOLE(2)[1] + 0.05), r(LIGHT[2] - 0.45)], [r(BLAST8 + 0.55), r(LIGHT[0] - 0.9), r(HOLE(2)[1] + 0.05), r(LIGHT[2] - 0.45)]]), face='camera', opts={'n': 8, 'len': 0.75, 'w': 0.5, 'angle': 0.0, 'soft': True, 'alpha': 0.85, 'at': [[BLAST8, r(BLAST8 + 0.55)]]}),   # (review 1) the wind lines hit his face
               BURST('tut8', [0.9, 3.7, -1.6], HONK8, 'TUUUT !', 0.85, hold=0.3)],   # (review 2) big, across the sky, held to the cut
        cams=[cam(0.0, [0.2, 0.55, 5.2], [0.22, 0.56, 5.12], [2.0, 2.45, -1.6], [2.0, 2.45, -1.6], lens=46),   # (review 2) tilted up: the trumpets against the sky (on the cargo box they were grey)   # (review 1) low in front, three-quarter: the grille, the driver, the chrome horns against the sky
              FC(CUT8, [LIGHT[0], 3.0, -2.7], [[LIGHT[0], r(POLE + 1.78), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE + 0.6), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.72), r(POLE + 1.2), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.72), r(POLE + 1.2), r(LIGHT[2] - 0.17)]], top=0.16, bottom=0.76)])   # ...his face in the hole, flattened
st.cue('sfx:honkLong', 'S08', HONK8, 0.6); st.cue('sfx:honkLong', 'S08', BLAST8, 0.45); st.cue('whoosh', 'S08', BLAST8, 0.3, 0.5, 300, 1200); st.cue('sfx:boing', 'S08', BACK8, 0.2)   # (review 2) the horn still blaring on his face


# 9: he turned green with fear. Close on the light: his red face, eyes popping, goes green from the chin up; then it drops out of the top hole and pops
#    into the bottom one, green, glowing; a gulp
#    (stills 2) no weight shift, the head filling the hole; on the landing his head spreads past the rim (a body squash dropped his face out of it)
#    (review 1: the dip, the jump, the drop and the bounce one sample each: no hang time; his trousers in the bottom hole, his hands at the foot of the
#    post) his head alone; red to green, then a dip, a jump up out of the top hole HELD six frames with a look down, a smear down into the bottom hole,
#    a splat past its rim, the face filling out over five frames, a gulp, a blink
D9 = st.dur('S09'); TURN9 = 0.25; DROP9 = 0.66; MID9 = 1.06; LAND9 = 1.18   # (review 2: the S05 gag again, frontal, the fall never on screen, brown and olive between red and green)
UP9 = [BEHIND(2)[0], r(BEHIND(2)[1] + 0.32), BEHIND(2)[2]]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(2), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.7, 'brow': 0.8, 'mouth': 'o'}}), toonDur=0.0),
            k(TURN9, toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'hairUp': 0.9, 'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'wavy', 'tremble': 1.0}}), toonDur=0.07, toonEase='inOut'),   # red to green in two frames (over 0.3 s it went through brown and olive), eyes popping, quivering...
            k(r(DROP9 - 0.08), toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': {'lid': 0.0, 'eye': 0.9, 'brow': 1.0, 'mouth': 'wavy'}}, {'head': [2.1, 0.8, 1.0]}), toonDur=0.06, toonEase='in'),   # ...a dip...
            k(DROP9, to=UP9, dur=0.09, ease='out', face='keep'), k(DROP9, toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': {'lid': 0.0, 'eye': 0.9, 'brow': 1.0, 'mouth': 'O'}}, {'head': [0.8, 1.3, 1.0]}), toonDur=0.05, toonEase='out'),   # ...a jump up out of the top hole...
            k(r(DROP9 + 0.1), toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': {'lid': 0.0, 'eye': 0.9, 'brow': 1.0, 'mouth': 'O', 'gy': 0.85}}, {'head': [0.95, 1.08, 1.0]}), toonDur=0.06),   # ...hanging there, a look down at the drop...
            k(r(DROP9 + 0.2), look='camera'), k(r(DROP9 + 0.2), toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': {'lid': 0.1, 'eye': 0.7, 'brow': 0.9, 'mouth': 'wavy', 'gy': 0.0}}, {'head': [0.95, 1.08, 1.0]}), toonDur=0.05),   # ...(review 2) then a look to us, a long one...
            k(r(MID9 - 0.07), to=BEHIND(1), dur=0.07, ease='in', face='keep'), k(r(MID9 - 0.07), toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': {'lid': 0.0, 'eye': 0.9, 'mouth': 'O'}}, {'head': [0.72, 1.45, 1.0]}), toonDur=0.04, toonEase='in'),   # ...down like a smear...
            k(MID9, toon=IN({'skin': SKIN('#FFB22E', 1.0, 0.5), 'face': {'lid': 0.0, 'eye': 0.9, 'mouth': 'O'}}, {'head': [0.8, 1.3, 1.0]}), toonDur=0.02),   # ...flashing amber in the middle hole for three frames on the way...
            k(r(LAND9 - 0.04), to=BEHIND(0), dur=0.04, ease='in', face='keep'), k(r(LAND9 - 0.03), toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': {'lid': 0.0, 'eye': 0.9, 'mouth': 'O'}}, {'head': [0.72, 1.45, 1.0]}), toonDur=0.02),
            k(LAND9, to=[BEHIND(0)[0], BEHIND(0)[1], r(BEHIND(0)[2] - 0.14)], dur=0.03, ease='out', face='keep'), k(LAND9, toon=IN({'skin': SKIN(GREEN, 1.0, 0.5), 'face': {'lid': 0.5}}, {'head': [2.1, 0.78, 1.0]}), toonDur=0.03, toonEase='out'),   # ...splat bulging out over the bottom rim...
            k(r(LAND9 + 0.07), to=BEHIND(0), dur=0.12, ease='inOut', face='keep'), k(r(LAND9 + 0.07), toon=IN({'skin': SKIN(GREEN, 1.0, 0.5), 'face': {'lid': 0.35, 'gulp': 0.4}}, {'head': [1.6, 1.08, 1.0]}), toonDur=0.08, toonEase='out'),   # ...filling out over five frames...
            k(r(LAND9 + 0.17), toon=IN({'skin': SKIN(GREEN, 1.0, 0.5), 'face': {'lid': 0.3, 'gulp': 1.0}}), toonDur=0.12),   # ...a gulp...
            k(r(D9 - 0.22), toon=IN({'skin': SKIN(GREEN, 1.0, 0.5), 'face': {'lid': 1.0}}), toonDur=0.08), k(r(D9 - 0.1), toon=IN({'skin': SKIN(GREEN, 1.0, 0.5), 'face': DEAD}), toonDur=0.08)])],   # ...a green light, a blink
        props=[P('light9', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'open': [[0.0, 2], [r(MID9 - 0.04), 1], [r(LAND9 - 0.04), 0]], 'shake': [[LAND9, 0.04]]}),
               P('glow9r', 'glowLight', pos=[LIGHT[0], HOLE(2)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4}, keys=[k(TURN9, visible=False)]),
               P('glow9g', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#44FF55', 'k': 3, 'dist': 4, 'at': LAND9})],
        cams=[FC(0.0, [r(LIGHT[0] - 1.7), 2.5, -2.6], [[LIGHT[0], r(POLE + 2.05), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.1), r(LIGHT[2] - 0.17)], [r(LIGHT[0] - 0.5), r(POLE + 0.9), r(LIGHT[2] - 0.17)], [r(LIGHT[0] + 0.5), r(POLE + 0.9), r(LIGHT[2] - 0.17)]], top=0.12, bottom=0.76, drift=(0.04, 0.0, 0.04))])   # (review 2) three-quarter from the road side (S05 is frontal)
st.cue('sfx:boing', 'S09', DROP9, 0.2); st.cue('sfx:slideDown', 'S09', r(MID9 - 0.07), 0.3); st.cue('sfx:splat', 'S09', LAND9, 0.2); st.cue('sfx:gulp', 'S09', r(LAND9 + 0.17), 0.25)


# 10: all the cars went through. Low beside the light: every car shoots past, one after the other, speed lines, his hair whipped in the bottom hole,
#     the light rattling; deadpan
#     (stills 2: one car in the frame, his face a speck in a light at the edge) from across the lane, the light nearer: his green face in the bottom
#     hole, the lorry first, then a car every fifth of a second, streaking between us and him all through the shot
D10 = st.dur('S10')
STREAM = [('truck', '#2F6FB2'), ('car', '#F5C33B'), ('car', '#5FB86A'), ('car', '#C255C8'), ('car', '#E8463A'), ('car', '#F08A3C'), ('car', '#3A9BDC'), ('car', '#8C949A')]
CROSS = lambda i: r(0.05 + 0.19 * i)                                     # when vehicle i crosses the line from the camera through the light (z 3.2, behind it), at 57 m/s
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BEHIND(0)[0], BEHIND(0)[1], r(BEHIND(0)[2] - 0.08)], LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN('#9CFF9C', 1.0, 0.6), 'wind': [-6.0, 0.5, -10.0], 'hairUp': 0.9, 'face': DEAD}), toonDur=0.0),   # (review 2) forward in the hole and a paler green (deep in a green ring it vanished)
            *[k(r(CROSS(i) + 0.03), toon=IN({'skin': SKIN('#9CFF9C', 1.0, 0.6), 'wind': ([-9.0, 0.5, -12.0] if i % 2 else [6.0, 0.8, -12.0]), 'hairUp': (1.0 if i % 2 else 0.75), 'sq': ([1.01, 0.99, 1.01] if i % 2 else [1.0, 1.0, 1.0]), 'face': {'lid': 0.0, 'gx': (0.95 if i % 2 else -0.95), 'eye': 0.6, 'brow': 0.6}}), toonDur=0.04) for i in range(len(STREAM))],   # (review 2) the eyes snapping wide after each car   # each car's wind: (review 1) his hair whipped one way then the other, his eyes snapping after each car
            k(1.2, toon=IN({'skin': SKIN('#9CFF9C', 1.0, 0.6), 'hairUp': 0.9, 'face': {'lid': 1.0}}), toonDur=0.08), k(1.3, toon=IN({'skin': SKIN('#9CFF9C', 1.0, 0.6), 'hairUp': 0.9, 'face': DEAD}), toonDur=0.1)])],
        props=[P('light10', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'shake': [[CROSS(i), 0.02] for i in range(0, len(STREAM), 2)], 'open': [[0.0, 0]]}), P('glow10', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#44FF55', 'k': 3, 'dist': 4}),
               *[P(f'veh10{i}', kind_, pos=[2.2, 0, r(3.2 - 57.0 * CROSS(i))], ry=-90, opts={'color': c_}, keys=[k(0.0, to=[2.2, 0, r(3.2 + 57.0 * (D10 - CROSS(i)))], dur=D10, ease='linear')]) for i, (kind_, c_) in enumerate(STREAM)],
               P('spd10', 'speedLines', pos=[2.2, 1.2, 3.2], face='camera', opts={'n': 9, 'len': 2.4, 'w': 1.4, 'angle': 0.0, 'soft': True, 'taper': True, 'alpha': 0.6, 'at': [[0.0, D10]]})],
        cams=[FC(0.0, [5.9, 1.2, -3.6], [[LIGHT[0], r(POLE + 0.9), r(LIGHT[2] - 0.17)], [LIGHT[0], 0.5, LIGHT[2]], [2.2, 1.6, 3.2], [2.2, 0.2, 3.2]], top=0.1, bottom=0.8)])   # (review 2) nearer and straighter on the bottom hole   # (stills 2) 33 degrees off the light's axis; (stills 3) from the pavement: the cars streak behind the light (across the lane they filled the lens)
st.cue('whoosh', 'S10', 0.05, 0.4, 1.2, 200, 1400); st.cue('sfx:engine', 'S10', 0.1, 0.3)


# 11: the town hall painted him red again. A painter on a ladder in front of the light rolls his green face red, stroke by stroke, his eyes shutting at
#     each stroke; the cars stop again behind; deadpan (REPEINT)
#     (stills 2: the car that stops was out of the frame) a second shot to end on: from the street, the light with his red face in the green hole, the
#     painter on his ladder looking at us, and the next car braking hard at the light, nose down
D11 = st.dur('S11'); STROKES = [0.3, 0.62, 0.94]; CUT11 = 1.3; BRAKE11 = 1.62; BACK11 = 2.12   # (review 2) the queue, then back on his face for the last blink
LAD = [r(LIGHT[0] + 0.85), 0, r(LIGHT[2] - 0.55)]                          # (stills 1) beside the light: in front of it the painter hid his face; (stills 4) on its pavement side, clear of the shot from the road
ROLL = lambda dy: {'reach': {'R': [LIGHT[0], r(HOLE(0)[1] + dy), r(LIGHT[2] - 0.3), 1, 0.05], 'L': [r(LIGHT[0] + 0.3), 1.9, r(LAD[2] + 0.1), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
COLS = ['#8FCB3A', '#E0A22A', RED]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', BEHIND(0), LRY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=IN({'skin': SKIN(GREEN, 1.0, 0.45), 'face': DEAD}), toonDur=0.0),
            *[k(t_, toon=IN({'skin': SKIN(COLS[i], 1.0, 0.45), 'face': {'lid': 1.0}}), toonDur=0.06) for i, t_ in enumerate(STROKES)],   # each stroke: his eyes shut, a colour nearer red...
            *[k(r(t_ + 0.12), toon=IN({'skin': SKIN(COLS[i], 1.0, 0.45), 'face': DEAD}), toonDur=0.08) for i, t_ in enumerate(STROKES)],
            k(1.7, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'sq': [1.0, 1.006, 1.0], 'face': DEAD}), toonDur=0.3), k(2.24, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': {'lid': 1.0}}), toonDur=0.1), k(2.4, toon=IN({'skin': SKIN(RED, 1.0, 0.45), 'face': DEAD}), toonDur=0.12)]),   # ...red again; (review 2) one deadpan blink to end on
        act('peintre', [LAD[0], 0.9, r(LAD[2] - 0.2)], -60, 'stand', 'neutral', keys=[k(0.0, look=HOLE(0)), k(0.0, toon={**ROLL(0.3), 'face': {'lid': 0.5, 'gy': 0.2}}, toonDur=0.0),
            *[k(r(t_ - 0.12), toon={**ROLL(0.28), 'face': {'lid': 0.5}}, toonDur=0.1) for t_ in STROKES], *[k(t_, toon={**ROLL(-0.22), 'face': {'lid': 0.5}}, toonDur=0.12, toonEase='inOut') for t_ in STROKES],   # the roller up and down his face
            k(1.3, toon={**ROLL(0.0), 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.2), k(1.35, look='camera')])],
        props=[P('light11', 'headLight', pos=LIGHT, ry=LRY, opts={'pole': POLE, 'column': True, 'open': [[0.0, 0]]}), P('lad11', 'ladder', pos=LAD, ry=20, opts={'h': 2.2, 'lean': 0.18}),
               P('roller11', 'paintRoller', on={'actor': 'peintre', 'hand': 'R'}, opts={'len': 0.62, 'color': RED, 'sleeve': '#E9CF52', 'frame': True, 'rollerR': 0.06, 'rollerW': 0.3}),   # (review 1) a frame and a white sleeve with its band of red (a red cylinder alone read as a cap)
               *QUEUE2('11', r(BRAKE11 - 0.04), hard=1.6), HALOB('11', at=CUT11),   # (review 2) the queue stops again at his red, front car first, braking harder   # (stills 4) the queue again: the second shot is the long lens of S06; (pass 3) the near car's slot free for the braking car, the queue inching on after it (a 0.6 s freeze at the end)
               P('skid11', 'skidMarks', pos=[2.2, 0, r(CARS[0][1] + 1.3)], opts={'at': r(BRAKE11 - 0.3), 'len': 3.2}),   # the front car's skid at the light
               P('glow11', 'glowLight', pos=[LIGHT[0], HOLE(0)[1], r(LIGHT[2] - 0.6)], opts={'color': '#FF4A2A', 'k': 3, 'dist': 4, 'at': 0.94})],
        cams=[FC(0.0, [4.9, 2.1, -3.4], [[LIGHT[0], r(POLE + 1.75), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.2), r(LIGHT[2] - 0.17)], [LAD[0], 2.8, r(LAD[2] - 0.2)], [LAD[0], 0.9, r(LAD[2] - 0.2)]], top=0.12, bottom=0.76, drift=(0.04, 0.0, -0.04)),
              JAMCAM(CUT11), FC(BACK11, [4.9, 2.1, -3.4], [[LIGHT[0], r(POLE + 1.75), r(LIGHT[2] - 0.17)], [LIGHT[0], r(POLE - 0.2), r(LIGHT[2] - 0.17)], [LAD[0], 2.8, r(LAD[2] - 0.2)], [LAD[0], 0.9, r(LAD[2] - 0.2)]], top=0.12, bottom=0.76)])   # (review 2) back to his red face in the green hole for the last blink   # (stills 4) ...cut to the long lens of S06: the queue stopped again at his red light, its last car braking into place (a vertical frame cannot hold the light and a car side by side up close: from behind, beside or across, the car filled it)
for t_ in STROKES: st.cue('sfx:squeak', 'S11', t_, 0.15)
st.cue('sfx:brake', 'S11', r(BRAKE11 - 0.25), 0.3)


# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.2, 'mec', 'sunburn'), ('S02', 0.8, 'mec', 'egg'), ('S03', 1.0, 'mec', 'glow'), ('S05', 0.5, 'mec', 'redlight'), ('S08', 0.6, 'mec', 'honk'), ('S09', 1.2, 'mec', 'green'), ('S11', 2.0, 'mec', 'repaint')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
st.card('S05', 'FEU ROUGE', at=0.6)   # (review 2) after the splat (at 0.3 it came down on his hair mid-hang)
st.card('S11', 'REPEINT', at=0.6)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'autoSq': 0}}   # (stills p2) no automatic landing squash: after the drop into a hole it shortened him 0.4 m and his face sank out of it
st.write("Le coup de soleil", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'gamin': {'preset': 'gamin', 'seed': 621, 'suit': '#F08A3C', 'hat': 'beanie', 'hatColor': '#3A9BDC', 'build': {'height': 0.55, 'headScale': 1.35}, 'toon': EX},
    'voisine': {'preset': 'madame', 'seed': 622, 'suit': '#8E5AA8', 'build': {'width': 0.9, 'headWidth': 1.25, 'height': 1.22}, 'toon': EX},   # (stills p2) a tall neighbour: her arm comes down onto his forehead from above, not across his eyes
    'maire': {'preset': 'politique', 'seed': 623, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ouv1': {'preset': 'sportif', 'seed': 624, 'suit': '#F08A3C', 'hat': 'hardhat', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ouv2': {'preset': 'sportif', 'seed': 625, 'suit': '#F08A3C', 'hat': 'hardhat', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'peintre': {'preset': 'sportif', 'seed': 626, 'suit': '#F2F0EA', 'hat': 'beanie', 'hatColor': '#F2F0EA', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
})
