#!/usr/bin/env python3
"""Le champagne (story 68, cycle 30; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man opened the champagne. The cork never came down. It went through the ceiling, then through the neighbour's living room. The neighbour
complained. The police opened an inquiry. The town hall closed the sky. The air force gave chase. The cork won. It went into orbit. The scientists
named it Bouchon 1. Since then the television has a better picture. The government made it a national treasure. The other countries claimed it.
The man got a bill for taking up space. Yesterday the cork came down. Right into his glass. The champagne was flat.
Staging: in his living room he strains at the cork, cheeks puffed, face red, the bottle shaking: POP, the cork shoots up, a geyser of foam rains
back on him, his hair stands up; he holds his flute up under the ceiling to catch it; from below, the cork punches a hole in the plaster and the
chips rain on his face; upstairs the old neighbour eats her soup: the cork comes up through the floor, the table and the plate, the soup leaps
into her face and the cork goes on through her ceiling; dripping, a noodle on her head, she points up at the police desk; a detective looks up
the hole through a magnifying glass, his eye huge, his flute left on a side table under the hole; on the roof the mayor puts up a CIEL FERMÉ
sign and wags his finger at the sky (FERMÉ); two fighter jets climb after the cork; it pulls away and they sputter (GAGNÉ); it goes round the
Earth with solar panels; a control-room screen names it BOUCHON 1, the scientists toast; a family's television clears from snow to a sharp
match; a minister at a podium; a gilt portrait of the cork unveiled (TRÉSOR); four leaders' arms stretch across a round table to grab its
model; a postman hands him an envelope and the bill unrolls down to the floor; the cork comes back down in flames through the clouds; it drops
through the hole into the flute on the side table (PLOUF); he sips: flat, a last bubble, a look at us.
Natural look; cycle 30: props_champagne.js (cork, flute, foamJet, corkHole, soupBowl, gunk, magnifier, oldTv, orbitScreen, corkPortrait)."""
from story_kit import *
import math

st = Story('champagne', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S13', 'L13', 0), ('S14', 'L13', 4),
         ('S15', 'L14', 0), ('S16', 'L15', 0), ('S17', 'L15', 6), ('S18', 'L16', 0), ('S19', 'L17', 0), ('S20', 'L18', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
FOAM = '#FFF6DC'; SOUP = '#E39A3A'
CEIL = 3.4                                          # the living-room ceiling (the room's walls go up to 7 m: a plaster ceiling is laid at this height)
ME = [0.0, 0, 0.0]                                  # him in his living room, facing us
BOT = [0.0, 1.3, 0.42]; BS = 1.5                    # the bottle in front of his chest (scale 1.5: its mouth 0.35 m above its middle)
MOUTH_Y = r(BOT[1] + 0.232 * BS)
CS = 1.6                                            # the cork at the near shots (8 cm)
CORK0 = [BOT[0], r(MOUTH_Y + 0.02), BOT[2]]         # the cork in the neck
HOLE = [0.0, CEIL, 0.42]                            # where it went through the ceiling, straight above the bottle
SIDE = [0.0, 0, 0.42]; SIDE_H = 0.95                 # the side table later put under the hole, the flute on it
HEADBOX = {'w': 0.31, 'h': 0.5, 'd': 0.17}           # his head box (headWidth 1.3) for the foam stuck on it
CEILING = lambda pid, y=CEIL, cx=0.0, cz=0.0: P(pid, 'ceilingPlaster', pos=[cx, y, cz], rot=[PI / 2, 0, 0], opts={'w': 9.0, 'h': 9.0})
HOLEP = lambda pid, pos, at_=-1.0, inner='#2E2A28', fall=1, rr=0.1: P(pid, 'corkHole', pos=pos, rot=[PI / 2 if fall > 0 else -PI / 2, 0, 0], opts={'at': at_, 'r': rr, 'inner': inner, 'fall': fall})

for g_ in [('S01', 1.55, 'mec', 'pop'), ('S04', 0.75, 'voisine', 'soup'), ('S06', 0.9, 'commissaire', 'loupe'), ('S07', 1.0, 'maire', 'ferme'), ('S12', 1.0, 'pere', 'tele'),
           ('S15', 0.9, 'chef1', 'grab'), ('S17', 1.2, 'mec', 'bill'), ('S20', 1.2, 'mec', 'end')]:
    st.gag(*g_)
st.card('S07', 'FERMÉ', at=0.6)
st.card('S09', 'GAGNÉ', at=0.45)
st.card('S14', 'TRÉSOR', at=0.4)


# 1: the hook. His living room: he strains at the cork with both thumbs, cheeks puffed, face going red, the bottle shaking, the cork creeping
#    out...; POP on « champagne »: the cork shoots up out of the frame, foam gushes up and rains back on him, his hair stands up
D1 = st.dur('S01'); POP1 = r(st.at('S01', 'L01', 5) + 0.12)
SHAKE1 = [r(0.18 + 0.12 * j) for j in range(int((POP1 - 0.2) / 0.12))]
K1 = [k(0.0, look=[BOT[0], MOUTH_Y, BOT[2]]), k(0.0, toon={'reach': {'L': [-0.08, 1.24, 0.44, 1, 0.04], 'R': [0.07, r(MOUTH_Y + 0.03), 0.44, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'pinch'},
                                                          'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'clench', 'brow': -0.5, 'cheeks': 0.4}}, toonDur=0.0)]
for j, tj in enumerate(SHAKE1):
    p = (j + 1) / len(SHAKE1); s = 1 if j % 2 else -1
    K1.append(k(tj, toon={'reach': {'L': [-0.08, 1.24, 0.44, 1, 0.04], 'R': [0.07, r(MOUTH_Y + 0.03 + 0.012 * p), 0.44, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'pinch'},
                          'bend': {'spine': [r(0.12 + 0.03 * p), r(0.04 * s * p), 0, 1, None]}, 'sq': [r(1 + 0.03 * s * p), r(1 - 0.03 * s * p), r(1 + 0.03 * s * p)],
                          'face': {'lid': r(0.45 + 0.4 * p), 'mouth': 'clench', 'brow': -0.7, 'cheeks': r(0.4 + 0.6 * p), 'blush': r(0.9 * p), 'vein': r(p), 'sweat': 1.0 if p > 0.5 else 0.0}}, toonDur=0.06))   # straining harder, redder...
K1 += [k(POP1, toon={'reach': {'L': [-0.08, 1.24, 0.44, 1, 0.04], 'R': [0.16, r(MOUTH_Y + 0.2), 0.5, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'spread'}, 'sq': [1.12, 0.86, 1.12], 'hairUp': 1.0,
                     'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.04, toonEase='out'),   # ...POP: the recoil, hair up, eyes wide...
       k(r(POP1 + 0.04), look=[0.0, 7.0, 0.8]),
       k(r(POP1 + 0.1), toon={'reach': {'L': [-0.08, 1.24, 0.44, 1, 0.04], 'R': [0.18, r(MOUTH_Y + 0.25), 0.5, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'spread'}, 'sq': [0.95, 1.07, 0.95], 'hairUp': 1.0,
                              'bend': {'neck': [-0.3, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.08, toonEase='out')]   # ...and his face up after it
SH1 = [k(tj, to=[r(BOT[0] + 0.01 * (1 if j % 2 else -1) * (j + 1) / len(SHAKE1)), BOT[1], BOT[2]], dur=0.06, ease='inOut') for j, tj in enumerate(SHAKE1)]
SC1 = [k(tj, to=[r(CORK0[0] + 0.01 * (1 if j % 2 else -1) * (j + 1) / len(SHAKE1)), r(CORK0[1] + 0.014 * (j + 1) / len(SHAKE1)), CORK0[2]], dur=0.06, ease='inOut') for j, tj in enumerate(SHAKE1)]
st.shot('S01', 'livingRoom', actors=[act('mec', ME, 0, 'stand', 'determined', keys=K1)],
        props=[P('bot1', 'champagneBottle', pos=BOT, scale=BS, keys=SH1),
               P('cork1', 'cork', pos=CORK0, scale=CS, opts={'spin': 3.0, 'trail': [[POP1, r(POP1 + 0.3)]]}, keys=SC1 + [k(POP1, to=[CORK0[0], 6.0, CORK0[2]], dur=0.16, ease='in')]),
               P('foam1', 'foamJet', pos=[BOT[0], MOUTH_Y, BOT[2]], opts={'at': [POP1, r(POP1 + 0.55)], 'len': 1.6, 'spread': 0.35, 'size': 0.055, 'n': 40, 'color': FOAM}),
               P('gunk1', 'gunk', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={**HEADBOX, 'color': FOAM, 'at': r(POP1 + 0.3), 'n': 10}),
               BURST('pop1', [0.55, 2.3, 0.6], POP1, 'POP !', 0.42, 0.28)],
        cams=[FC(0.0, [0.9, 1.55, 2.7], [[0.0, 2.55, 0.0], [0.0, 1.0, 0.42], [0.0, 3.05, 0.42], [-0.45, 1.4, 0.3], [0.55, 2.0, 0.4]], top=0.12, bottom=0.76)])
for tj in SHAKE1[::3]: st.cue('sfx:squeak', 'S01', tj, 0.12)
st.cue('sfx:pop', 'S01', POP1, 0.55); st.cue('sfx:splash', 'S01', r(POP1 + 0.05), 0.3)

# 2: the cork never came down. From up under the ceiling, looking down on him: foam on his head, the bottle still foaming over at his side, he
#    holds his flute up to catch the cork when it falls; he waits; blinks; tilts his head; waits
D2 = st.dur('S02'); BOT2 = [-0.5, 1.02, 0.28]
st.shot('S02', 'livingRoom', actors=[
        act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.22, 2.78, 0.3, 1, 0.05], 'L': [-0.47, 0.98, 0.33, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hairUp': 0.6, 'face': {'lid': 0.3, 'eye': 0.15, 'mouth': 'line', 'gy': -0.5}}, toonDur=0.0),
            k(0.55, toon={'reach': {'R': [0.22, 2.78, 0.3, 1, 0.05], 'L': [-0.47, 0.98, 0.33, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hairUp': 0.6, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.04),
            k(0.62, toon={'reach': {'R': [0.22, 2.78, 0.3, 1, 0.05], 'L': [-0.47, 0.98, 0.33, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hairUp': 0.6, 'face': {'lid': 0.3, 'eye': 0.15, 'mouth': 'line', 'gy': -0.5}}, toonDur=0.06),   # a blink...
            k(1.0, toon={'reach': {'R': [0.22, 2.82, 0.3, 1, 0.05], 'L': [-0.47, 0.98, 0.33, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hairUp': 0.6, 'bend': {'neck': [0.0, 0.0, 0.22, 1, None]}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.6, 'browTilt': 12}}, toonDur=0.25, toonEase='inOut'),   # ...his head on one side...
            k(1.55, toon={'reach': {'R': [0.22, 2.78, 0.3, 1, 0.05], 'L': [-0.47, 0.98, 0.33, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hairUp': 0.6, 'face': {'lid': 0.45, 'mouth': 'line', 'gy': -0.4}}, toonDur=0.3, toonEase='inOut')])],   # ...still waiting
        props=[P('flute2', 'flute', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.1, 0.03]}, scale=CS, opts={'level': 0.0}),
               P('bot2', 'champagneBottle', pos=BOT2, scale=BS), P('foam2', 'foamJet', pos=[BOT2[0], r(BOT2[1] + 0.232 * BS), BOT2[2]], opts={'at': [-0.5, r(D2 + 0.5)], 'len': 0.16, 'spread': 0.6, 'size': 0.035, 'n': 70, 'color': FOAM}),
               P('gunk2', 'gunk', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={**HEADBOX, 'color': FOAM, 'at': -1.0, 'n': 10})],
        cams=[FC(0.0, [0.55, 3.7, 1.7], [[0.22, 3.0, 0.3], [0.0, 2.5, 0.0], [0.0, 0.0, 0.0], [-0.55, 0.0, 0.3], [0.5, 0.0, 0.5]], top=0.14, bottom=0.76)])
st.cue('sfx:tick', 'S02', 0.5, 0.15); st.cue('sfx:tick', 'S02', 1.0, 0.15); st.cue('sfx:tick', 'S02', 1.5, 0.15)

# 3: it went through the ceiling. From low, looking up past him: the cork punches a hole in the plaster, cracks run out, chips and dust rain on
#    his upturned face; he blinks them off
D3 = st.dur('S03'); PUNCH3 = 0.22
st.shot('S03', 'livingRoom', actors=[
        act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look=HOLE), k(0.0, toon={'hairUp': 0.6, 'bend': {'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.0),
            k(r(PUNCH3 + 0.32), toon={'hairUp': 0.6, 'bend': {'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'mouth': 'wavy', 'brow': -0.4}}, toonDur=0.05),   # the chips land: eyes shut tight...
            k(r(PUNCH3 + 0.6), toon={'hairUp': 0.6, 'bend': {'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 0.25, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.12),   # ...open again, flat
            k(r(PUNCH3 + 0.85), toon={'hairUp': 0.6, 'bend': {'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.04), k(r(PUNCH3 + 0.91), toon={'hairUp': 0.6, 'bend': {'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.06)])],
        props=[CEILING('ceil3'), HOLEP('hole3', [HOLE[0], r(CEIL - 0.006), HOLE[2]], at_=PUNCH3), P('cracks3', 'ceilingCracks', pos=[HOLE[0], r(CEIL - 0.008), HOLE[2]], rot=[PI / 2, 0, 0], opts={'r': 0.8, 'n': 13, 'at': PUNCH3, 'thick': 1.4}),
               P('cork3', 'cork', pos=[HOLE[0], 2.6, HOLE[2]], scale=CS, opts={'spin': 3.0, 'trail': [[0.0, PUNCH3]]}, keys=[k(0.0, to=[HOLE[0], 4.2, HOLE[2]], dur=r(PUNCH3 * 2), ease='linear')]),
               P('gunk3', 'gunk', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={**HEADBOX, 'color': FOAM, 'at': -1.0, 'n': 10}),
               BURST('crac3', [0.75, 3.05, 0.6], r(PUNCH3 + 0.02), 'CRAC !', 0.4, 0.3)],
        cams=[FC(0.0, [1.3, 0.75, 2.5], [[HOLE[0], r(CEIL + 0.02), HOLE[2]], [0.75, r(CEIL + 0.02), 0.0], [0.0, 1.55, 0.0], [-0.4, 2.55, 0.0]], top=0.08, bottom=0.8)])
st.cue('sfx:crunch', 'S03', PUNCH3, 0.4); st.cue('sfx:rattleShort', 'S03', r(PUNCH3 + 0.3), 0.2)

# 4: then the neighbour's living room. Upstairs, her kitchen table: she lifts a spoonful of soup; the cork comes up through the floor, the table
#    and her plate: the soup leaps into her face, the cork goes on through her ceiling; she freezes, dripping, a noodle on her head, the spoon up
D4 = st.dur('S04'); BURST4 = 0.42
TB4 = [0.0, 0, -0.5]; TH4 = 1.0; BOWL4 = [0.0, TH4, -0.55]
st.shot('S04', 'kitchenDay', actors=[
        act('voisine', [0.0, 0, -1.25], 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.0, -0.55]), k(0.0, toon={'reach': {'R': [0.12, 1.25, -0.75, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.35, 'mouth': 'line', 'gy': 0.4}}, toonDur=0.0),
            k(0.1, toon={'reach': {'R': [0.08, 1.72, -1.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'O'}}, toonDur=0.28, toonEase='inOut'),   # the spoon up to her mouth...
            k(BURST4, toon={'reach': {'R': [0.08, 1.74, -1.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'sq': [0.92, 1.1, 0.92], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.04, toonEase='out'), k(BURST4, look=[0.0, 3.4, -0.55]),   # ...WHOOSH under her nose...
            k(r(BURST4 + 0.14), toon={'reach': {'R': [0.08, 1.74, -1.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'hairUp': 1.0, 'face': {'lid': 1.0, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.04),   # ...the soup in her face...
            k(r(BURST4 + 0.45), look='camera'), k(r(BURST4 + 0.45), toon={'reach': {'R': [0.08, 1.72, -1.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'hairUp': 0.5, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.12),   # ...and she opens her eyes on us
            k(r(BURST4 + 0.85), toon={'reach': {'R': [0.08, 1.72, -1.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'hairUp': 0.5, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.04), k(r(BURST4 + 0.91), toon={'reach': {'R': [0.08, 1.72, -1.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'hairUp': 0.5, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.06)])],
        props=[P('table4', 'table', pos=TB4, opts={'w': 1.2, 'd': 0.8, 'h': TH4}), P('bowl4', 'soupBowl', pos=BOWL4, scale=1.4, opts={'burstAt': BURST4, 'up': 1.0, 'floor': r(-TH4 / 1.4 + 0.01), 'soup': SOUP}),
               P('spoon4', 'slab', on={'actor': 'voisine', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'w': 0.025, 'h': 0.12, 'd': 0.012, 'color': '#C9CDD2'}),
               HOLEP('hf4', [0.0, 0.006, -0.55], at_=r(BURST4 - 0.04), fall=-1), HOLEP('ht4', [0.0, r(TH4 + 0.004), -0.55], at_=r(BURST4 - 0.01), fall=-1, inner='#1E1A18', rr=0.08),
               CEILING('ceil4', cz=-0.5), HOLEP('hc4', [0.0, r(CEIL - 0.006), -0.55], at_=r(BURST4 + 0.05), inner='#2E2A28'),
               P('cork4', 'cork', pos=[0.0, -0.4, -0.55], scale=CS, opts={'spin': 3.0, 'trail': [[r(BURST4 - 0.06), r(BURST4 + 0.12)]]}, keys=[k(r(BURST4 - 0.06), to=[0.0, 4.4, -0.55], dur=0.16, ease='linear')]),
               P('gunk4', 'gunk', on={'actor': 'voisine', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.26, 'h': 0.48, 'd': 0.17, 'color': SOUP, 'at': r(BURST4 + 0.13), 'n': 11, 'noodle': True}),
               BURST('splash4', [0.6, 2.2, -0.4], r(BURST4 + 0.02), 'SPLASH !', 0.46, 0.3)],
        cams=[FC(0.0, [0.9, 1.3, 2.1], [[0.0, 2.35, -1.25], [0.0, 0.0, -0.55], [0.0, r(CEIL + 0.02), -0.55], [0.65, 1.0, -0.15], [-0.6, 1.0, -0.15]], top=0.08, bottom=0.8)])
st.cue('sfx:crunch', 'S04', r(BURST4 - 0.04), 0.35); st.cue('sfx:splash', 'S04', BURST4, 0.45); st.cue('sfx:crunch', 'S04', r(BURST4 + 0.05), 0.25)

# 5: the neighbour complained. The police desk: dripping soup, the noodle on her head, she points up at the ceiling, furious; behind the desk the
#    officer types it in, two fingers, without looking up
D5 = st.dur('S05'); DESK5 = [-2.7, 0, -2.1]
TYPE5 = [r(0.15 + 0.16 * j) for j in range(int((D5 - 0.2) / 0.16))]
st.shot('S05', 'policeStation', actors=[
        act('voisine', [-2.7, 0, -1.05], 180, 'stand', 'angry', keys=[k(0.0, look=[-2.7, 1.9, -2.6]), k(0.0, toon={'reach': {'R': [-2.5, 2.75, -1.25, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.1, 'mouth': 'open', 'brow': -0.8, 'vein': 1.0}}, toonDur=0.0),
            *[k(r(0.12 + 0.3 * j), toon={'reach': {'R': [-2.5, r(2.75 + (0.08 if j % 2 else 0.0)), -1.25, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.1, 'mouth': 'open' if j % 2 else 'teeth', 'brow': -0.8, 'vein': 1.0}}, toonDur=0.08) for j in range(5)]]),   # jabbing up at the ceiling
        act('flic', [-2.7, 0, -2.75], 0, 'stand', 'unimpressed', keys=[k(0.0, look=[-2.7, 1.05, -2.25]), k(0.0, toon={'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.0),
            *[k(tj, toon={'bend': {'spine': [0.25, 0, 0, 1, None]}, 'reach': {('R' if j % 2 else 'L'): [r(-2.6 if j % 2 else -2.8), r(1.08 if (j // 2) % 2 else 1.04), -2.3, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'point'}, 'face': {'lid': 0.55, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.06) for j, tj in enumerate(TYPE5)]])],   # two fingers on the keys
        props=[P('gunk5', 'gunk', on={'actor': 'voisine', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.26, 'h': 0.48, 'd': 0.17, 'color': SOUP, 'at': -1.0, 'n': 11, 'noodle': True})],
        cams=[FC(0.0, [-1.0, 1.95, -3.35], [[-2.7, 2.45, -1.05], [-2.5, 2.95, -1.25], [-2.7, 1.3, -1.05]], top=0.12, bottom=0.78, inside=(-6.8, 6.8, 0.3, 3.4, -3.45, 13.0))])   # (stills 1) over the officer's shoulder onto her face (we saw his back and half of her)
for tj in TYPE5: st.cue('sfx:click', 'S05', tj, 0.12)

# 6: the police opened an inquiry. Back in his living room, from low: a detective in a trench coat looks up the hole through a magnifying glass,
#    his eye huge in the lens; his flute stands on a side table under the hole in the light that falls through it; foam still on his head, he
#    looks up too
D6 = st.dur('S06'); DET6 = [0.45, 0, 0.62]
st.shot('S06', 'livingRoom', actors=[
        act('commissaire', DET6, -20, 'stand', 'neutral', keys=[k(0.0, look=HOLE), k(0.0, toon={'touch': {'R': ['face', 0.12, 0.62, 0.14, 1, 0.02]}, 'hands': {'R': 'grip'}, 'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eyeR': 1.1, 'lidL': 0.7, 'mouth': 'pout', 'brow': 0.3}}, toonDur=0.0),
            k(0.6, toon={'touch': {'R': ['face', 0.14, 0.63, 0.12, 1, 0.02]}, 'hands': {'R': 'grip'}, 'bend': {'neck': [-0.38, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eyeR': 1.3, 'lidL': 0.8, 'mouth': 'pout', 'brow': 0.6}}, toonDur=0.2, toonEase='inOut'),   # leaning in: the eye fills the lens
            k(1.2, toon={'touch': {'R': ['face', 0.12, 0.62, 0.14, 1, 0.02]}, 'hands': {'R': 'grip'}, 'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eyeR': 1.1, 'lidL': 0.7, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.2), k(1.25, look='camera')]),
        act('mec', [-0.65, 0, 0.15], 15, 'stand', 'unimpressed', keys=[k(0.0, look=HOLE), k(0.0, toon={'bend': {'neck': [-0.3, 0, 0, 1, None]}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.9, toon={'bend': {'neck': [-0.3, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.04), k(0.96, toon={'bend': {'neck': [-0.3, 0, 0, 1, None]}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.06)])],
        props=[CEILING('ceil6'), HOLEP('hole6', [HOLE[0], r(CEIL - 0.006), HOLE[2]], inner='#8EC5EA'),
               P('light6', 'holeLight', pos=[HOLE[0], 0.0, HOLE[2]], face='camera', opts={'w': 0.45, 'h': CEIL}),
               P('mag6', 'magnifier', on={'actor': 'commissaire', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=1.3),
               P('side6', 'table', pos=SIDE, opts={'w': 0.55, 'd': 0.45, 'h': SIDE_H}), P('flute6', 'flute', pos=[SIDE[0], SIDE_H, SIDE[2]], scale=CS, opts={'level': 0.75}),
               P('gunk6', 'gunk', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={**HEADBOX, 'color': FOAM, 'at': -1.0, 'n': 10})],
        cams=[FC(0.0, [-1.9, 0.85, 2.4], [[DET6[0], 2.5, DET6[2]], [-0.65, 2.5, 0.15], [HOLE[0], r(CEIL + 0.02), HOLE[2]], [SIDE[0], 0.7, SIDE[2]], [0.9, 1.5, 0.6]], top=0.08, bottom=0.8)])   # low from his side (the S01 set-up was repeated)
st.cue('sfx:sniff', 'S06', 0.3, 0.25); st.cue('sfx:click', 'S06', 1.1, 0.2)

# 7: the town hall closed the sky. On the roof, by the hole behind a police tape: the mayor in his sash sets up a folding sign CIEL FERMÉ, then
#    points at the sky and wags his finger at it (FERMÉ)
D7 = st.dur('S07'); MAY7 = [1.25, 0, 0.65]; SIGN7 = [0.55, 0, 1.25]
st.shot('S07', 'rooftopPowerLine', actors=[
        act('maire', MAY7, -35, 'stand', 'determined', keys=[k(0.0, look=SIGN7), k(0.0, toon={'reach': {'R': [0.75, 1.05, 1.05, 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            k(0.4, toon={'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.2, toonEase='out'), k(0.45, look=[0.6, 8.0, 0.0]),   # straightens up...
            k(0.65, toon={'reach': {'R': [1.05, 3.25, 0.55, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.1, 'mouth': 'open', 'brow': -0.8}}, toonDur=0.15, toonEase='out'),   # ...the finger up at the sky...
            *[k(r(0.95 + 0.14 * j), toon={'reach': {'R': [r(1.05 + (0.14 if j % 2 else -0.14)), 3.25, 0.55, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.1, 'mouth': 'line', 'brow': -0.8}}, toonDur=0.07) for j in range(5)],   # ...non, non, non
            k(r(D7 - 0.2), look='camera')])],
        props=[HOLEP('hole7', [0.0, 0.006, 0.0], inner='#2A2A30', fall=-1, rr=0.12), P('cord7', 'cordon', pos=[0.0, 0, 0.0], opts={'w': 1.3, 'd': 1.3, 'sign': 'DANGER'}),
               P('sign7', 'closedSign', pos=SIGN7, ry=-25, opts={'text': 'CIEL|FERMÉ', 'at': 0.15, 'w': 0.95, 'h': 0.72})],
        cams=[FC(0.0, [3.3, 1.5, 4.6], [[MAY7[0], 2.55, MAY7[2]], [1.05, 3.35, 0.55], [SIGN7[0], 0.0, SIGN7[2]], [-0.75, 0.0, -0.7], [0.75, 0.0, 0.8]], top=0.12, bottom=0.78)])
st.cue('sfx:paper', 'S07', 0.15, 0.3); st.cue('sfx:whistle', 'S07', 0.7, 0.3)

# 8: the air force gave chase. Above the clouds, from just over the climbing cork: it streaks up at us, trailing white; two fighter jets climb after
#    it on their afterburners, the cloud deck far below
D8 = st.dur('S08'); C8 = [0.0, 60.0, 0.0]; V8 = 40.0; J1 = [-7.0, 34.0, -6.0]; J2 = [6.0, 27.0, -9.0]; VJ = 37.0
st.shot('S08', 'skyHigh', actors=[],
        props=[P('cork8', 'cork', pos=C8, scale=30, opts={'spin': 2.0, 'trail': [[0.0, 9.0]]}, keys=[k(0.0, to=[C8[0], r(C8[1] + V8 * D8), C8[2]], dur=D8, ease='linear')]),
               P('jet81', 'fighterJet', pos=J1, rot=[-PI / 2, 0, 0], opts={'burner': 1.0}, keys=[k(0.0, to=[J1[0], r(J1[1] + VJ * D8), J1[2]], dur=D8, ease='linear')]),
               P('jet82', 'fighterJet', pos=J2, rot=[-PI / 2, 0, 0.3], opts={'burner': 1.0}, keys=[k(0.0, to=[J2[0], r(J2[1] + VJ * D8), J2[2]], dur=D8, ease='linear')])],
        cams=[FC(0.0, [4.0, 68.0, 5.0], [[0.0, 61.0, 0.0], [0.0, 59.0, 0.0], [J1[0], r(J1[1] + 9), J1[2]], [J1[0], r(J1[1] - 9), J1[2]], [J2[0], r(J2[1] + 9), J2[2]], [J2[0], r(J2[1] - 9), J2[2]]], top=0.12, bottom=0.8, drift=(0.0, r(V8 * D8 * 0.97), 0.0))])
st.cue('sfx:jet', 'S08', 0.05, 0.5); st.cue('whoosh', 'S08', 0.3, 0.3, 0.4, 300, 1400)

# 9: the cork won. From the side: the cork bursts away upward (ZOUM), the jets fall behind, cough out black puffs and peel off (GAGNÉ)
D9 = st.dur('S09'); C9 = [0.0, 150.0, 0.0]; J91 = [-7.0, 118.0, -6.0]; J92 = [6.0, 111.0, -9.0]; DASH9 = 0.22
st.shot('S09', 'skyHigh', actors=[],
        props=[P('cork9', 'cork', pos=C9, scale=30, opts={'spin': 3.0, 'trail': [[0.0, 9.0]]}, keys=[k(DASH9, to=[C9[0], r(C9[1] + 90.0), C9[2]], dur=0.5, ease='in')]),
               P('jet91', 'fighterJet', pos=J91, rot=[-PI / 2, 0, 0], opts={'burner': 0.4}, keys=[k(0.0, to=[J91[0], r(J91[1] + 8), J91[2]], dur=0.6, ease='out'), k(0.6, rot=[-PI / 2 + 0.9, 0, 0.6], dur=0.6, ease='inOut'), k(0.6, to=[r(J91[0] - 6), r(J91[1] + 4), J91[2]], dur=0.6, ease='inOut')]),
               P('jet92', 'fighterJet', pos=J92, rot=[-PI / 2, 0, 0.3], opts={'burner': 0.4}, keys=[k(0.0, to=[J92[0], r(J92[1] + 7), J92[2]], dur=0.6, ease='out'), k(0.55, rot=[-PI / 2 + 0.9, 0, -0.5], dur=0.6, ease='inOut'), k(0.55, to=[r(J92[0] + 6), r(J92[1] + 3), J92[2]], dur=0.6, ease='inOut')]),
               P('puff91', 'dustPuff', pos=[J91[0], r(J91[1] - 1.0), J91[2]], scale=8, opts={'color': '#3A3A3E', 'once': True, 'startAt': 0.45, 'period': 0.8}),
               P('puff92', 'dustPuff', pos=[J92[0], r(J92[1] - 1.5), J92[2]], scale=8, opts={'color': '#3A3A3E', 'once': True, 'startAt': 0.55, 'period': 0.8}),
               BURST('zoum9', [3.0, 160.0, 4.0], r(DASH9 + 0.05), 'ZOUM !', 9.0, 0.3)],
        cams=[FC(0.0, [62.0, 128.0, 52.0], [[0.0, 153.0, 0.0], [0.0, 147.0, 0.0], [J91[0], r(J91[1] + 9), J91[2]], [J91[0], r(J91[1] - 9), J91[2]], [J92[0], r(J92[1] - 9), J92[2]]], top=0.14, bottom=0.8)])
st.cue('whoosh', 'S09', DASH9, 0.45, 0.35, 400, 2000); st.cue('sfx:rattleShort', 'S09', 0.45, 0.3); st.cue('sfx:rattleShort', 'S09', 0.6, 0.25)

# 10: it went into orbit. Space: the Earth below, the cork goes round it with two solar panels out, a streak of its orbit behind it
D10 = st.dur('S10')
st.shot('S10', 'spaceDark', actors=[],
        props=[P('earth10', 'earthGlobe', pos=[0.0, -7.0, -16.0], scale=9.0, opts={'spin': 0.08}),
               P('orb10', 'orbitTrail', pos=[0.0, -7.0, -16.0], scale=9.0, rot=[0.25, 0, 0.1], opts={'r': 1.25}),
               P('cork10', 'cork', pos=[-3.2, 1.0, -2.5], rot=[0, 0, -1.2], scale=22, opts={'spin': 0.5, 'panels': True}, keys=[k(0.0, to=[2.6, 1.5, -3.2], dur=D10, ease='linear')])],
        cams=[FC(0.0, [0.0, 1.6, 5.0], [[-3.2, 1.0, -2.5], [2.6, 1.5, -3.2], [0.0, -2.0, -8.0], [0.0, 2.5, -3.0]], top=0.16, bottom=0.76)])
st.cue('whoosh', 'S10', 0.1, 0.25, 0.8, 200, 600); st.cue('sfx:ding', 'S10', 0.6, 0.2)

# 11: the scientists named it Bouchon 1. A control room: the big screen draws its orbit round the Earth; on « Bouchon » the name springs up under
#    it; the two scientists in white coats raise their flutes to it
D11 = st.dur('S11'); NAME11 = st.at('S11', 'L11', 4)
TOAST11 = lambda x, z: {'reach': {'R': [x, 2.6, z, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'open', 'brow': 0.7}}
st.shot('S11', 'office', setOpts={'wall': '#3A4A5E', 'band': '#2C3A4C', 'trim': '#1E2A38', 'floor': '#4A525C', 'picture': False, 'carpet': False, 'door': False, 'printer': False}, actors=[
        act('savant1', [-1.15, 0, -2.2], 30, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.8, -3.45]), k(0.0, toon={'reach': {'R': [-0.85, 1.6, -2.0, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.45, toon={'reach': {'R': [-0.85, 1.6, -2.0, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'smirk'}}, toonDur=0.04), k(0.51, toon={'reach': {'R': [-0.85, 1.6, -2.0, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.06), k(0.8, look=[1.15, 2.2, -2.1]),
            k(NAME11, toon=TOAST11(-0.95, -1.95), toonDur=0.15, toonEase='out'), k(r(NAME11 + 0.1), look='camera'), k(r(NAME11 + 0.55), toon={**TOAST11(-0.95, -1.95), 'face': {'lid': 1.0, 'mouth': 'open'}}, toonDur=0.04), k(r(NAME11 + 0.61), toon=TOAST11(-0.95, -1.95), toonDur=0.06)]),
        act('savant2', [1.15, 0, -2.1], -30, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.8, -3.45]), k(0.0, toon={'reach': {'R': [0.85, 1.6, -1.9, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.3, look=[-1.15, 2.2, -2.2]), k(0.75, toon={'reach': {'R': [0.85, 1.6, -1.9, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'smirk'}}, toonDur=0.04), k(0.81, toon={'reach': {'R': [0.85, 1.6, -1.9, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.06), k(1.0, look=[0.0, 1.8, -3.45]),
            k(r(NAME11 + 0.05), toon=TOAST11(0.95, -1.85), toonDur=0.15, toonEase='out'), k(r(NAME11 + 0.15), look='camera')])],
        props=[P('screen11', 'orbitScreen', pos=[0.0, 0.85, -3.45], opts={'w': 2.7, 'h': 1.5, 'nameAt': NAME11, 'period': 2.6}),
               P('fl11a', 'flute', on={'actor': 'savant1', 'hand': 'R', 'offset': [0.0, -0.1, 0.03]}, scale=CS, opts={'level': 0.7}), P('fl11b', 'flute', on={'actor': 'savant2', 'hand': 'R', 'offset': [0.0, -0.1, 0.03]}, scale=CS, opts={'level': 0.7})],
        cams=[FC(0.0, [0.4, 1.6, 2.4], [[-1.35, 1.0, -3.45], [1.35, 2.35, -3.45], [-1.5, 2.5, -2.2], [1.5, 2.5, -2.1], [-0.95, 2.8, -1.95], [0.95, 2.8, -1.85], [0.0, 0.3, -2.2]], top=0.12, bottom=0.78)])
st.cue('sfx:fanfare', 'S11', NAME11, 0.3); st.cue('sfx:clink', 'S11', r(NAME11 + 0.2), 0.3)

# 12: since then the television gets a better picture. A family in front of an old set: the father holds the rabbit ears, the screen snow; it
#    clears to a sharp match; they jump for joy, the father lets go of the aerial slowly
D12 = st.dur('S12'); CLEAR12 = 0.55; TV12 = [1.1, 0, -0.9]   # (stills 1) the set at the right, its screen turned to us and to them (we saw its back)
st.shot('S12', 'livingRoom', setOpts={'tv': False}, actors=[
        act('pere', [0.5, 0, -1.3], 60, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 0.63, -0.85]), k(0.0, toon={'reach': {'R': [1.05, 1.32, -0.95, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.4, 'tongue': 0.0}}, toonDur=0.0),
            k(CLEAR12, toon={'reach': {'R': [1.05, 1.32, -0.95, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.06, toonEase='out'),   # it clears: he freezes...
            k(r(CLEAR12 + 0.55), toon={'reach': {'R': [0.95, 1.5, -0.85, 1, 0.05]}, 'hands': {'R': 'spread'}, 'bend': {'spine': [0.08, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'smirk', 'brow': 0.7}}, toonDur=0.3, toonEase='inOut')]),   # ...lets go, very slowly
        act('mere', [-0.4, 0, -1.65], 50, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 0.63, -0.85]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(r(CLEAR12 + 0.05), toon={'reach': {'R': [-0.18, 1.6, -1.42, 1, 0.04], 'L': [-0.3, 1.6, -1.48, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.1, toonEase='out'),
            *[k(r(CLEAR12 + 0.2 + 0.14 * j), toon={'reach': {'R': [r(-0.18 + (0.05 if j % 2 else 0.0)), 1.6, -1.42, 1, 0.04], 'L': [r(-0.3 - (0.05 if j % 2 else 0.0)), 1.6, -1.48, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.06) for j in range(6)]]),   # clapping
        act('gamin', [0.05, 0, -0.95], 55, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 0.63, -0.85]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(r(CLEAR12 + 0.08), clip='hop'), k(r(CLEAR12 + 0.08), toon={'reach': {'R': [0.3, 2.1, -0.75, 1, 0.05], 'L': [-0.15, 2.1, -1.05, 1, 0.05]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'open', 'brow': 0.9}}, toonDur=0.1, toonEase='out')])],
        props=[P('tv12', 'oldTv', pos=TV12, ry=-60, opts={'clearAt': CLEAR12})],
        cams=[FC(0.0, [0.2, 1.55, 2.3], [[0.5, 2.45, -1.3], [-0.4, 2.4, -1.65], [0.05, 2.0, -0.95], [TV12[0], 1.45, TV12[2]], [TV12[0], 0.6, TV12[2]], [-0.4, 1.05, -1.65], [0.05, 1.0, -0.95]], top=0.12, bottom=0.78)])
st.cue('sfx:static', 'S12', 0.0, 0.3); st.cue('sfx:ding', 'S12', CLEAR12, 0.3); st.cue('sfx:fanfare', 'S12', r(CLEAR12 + 0.1), 0.2)

# 13: the government declared it... At the podium, under the flashes, the minister lifts a solemn finger
D13 = st.dur('S13'); FL13 = [0.25, 0.6, 0.95]
st.shot('S13', 'pressRoom', setOpts={'backdrop': 'GOUVERNEMENT', 'fontScale': 0.55}, actors=[
        act('ministre', [0.0, 0, -2.45], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.25, 1.35, -1.85, 1, 0.04], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': [0.32, 2.45, -1.95, 1, 0.05], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'open', 'brow': 0.6}}, toonDur=0.2, toonEase='out'),   # the finger up...
            k(0.8, toon={'reach': {'R': [0.32, 2.5, -1.95, 1, 0.05], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.7}}, toonDur=0.2)])],
        props=[*[P(f'flash13{j}', 'glowLight', pos=[r(-1.2 + 1.2 * j), 1.8, 1.2], opts={'color': '#FFFFFF', 'k': 6.0, 'dist': 6.0}, keys=[k(0.0, visible=False), k(FL13[j], visible=True), k(r(FL13[j] + 0.06), visible=False)]) for j in range(3)]],
        cams=[FC(0.0, [0.7, 1.7, 1.6], [[0.0, 2.6, -2.45], [0.32, 2.6, -1.95], [0.0, 0.9, -2.0], [-0.6, 1.3, -2.0]], top=0.14, bottom=0.78)])
for f_ in FL13: st.cue('sfx:click', 'S13', f_, 0.25)

# 14: ...a national treasure. A town-hall salon: the minister pulls the veil off a gilt portrait of the cork with a tricolour sash; a guard
#    salutes (TRÉSOR)
D14 = st.dur('S14'); UNV14 = 0.15; PORT14 = [0.0, 1.0, -1.9]
st.shot('S14', 'mairie', actors=[
        act('ministre', [0.95, 0, -1.35], -55, 'stand', 'happy', keys=[k(0.0, look=[0.4, 1.8, -1.9]), k(0.0, toon={'reach': {'L': [0.52, 2.2, -1.75, 1, 0.04]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.0),
            k(UNV14, toon={'reach': {'L': [0.95, 1.3, -1.45, 1, 0.04]}, 'hands': {'L': 'grip'}, 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.2, toonEase='out'),   # the veil whipped off...
            k(0.7, look='camera'), k(0.75, toon={'face': {'lid': 0.25, 'mouth': 'smirk', 'brow': 0.6}}, toonDur=0.15)]),
        act('garde', [-1.0, 0, -1.4], 40, 'stand', 'determined', keys=[k(0.0, look=[0.0, 1.8, -1.9]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(r(UNV14 + 0.2), toon={'touch': {'R': ['face', 0.38, 0.86, 0.06, 1, 0.02]}, 'hands': {'R': 'open'}, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.2, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.12, toonEase='out')])],   # the salute
        props=[P('port14', 'corkPortrait', pos=PORT14, opts={'w': 1.0, 'h': 1.25, 'unveilAt': UNV14}), P('stand14', 'slab', pos=[0.0, 0.5, -1.98], opts={'w': 0.3, 'h': 1.0, 'd': 0.2, 'color': '#6B4F3A'})],
        cams=[FC(0.0, [0.25, 1.6, 2.2], [[0.0, 2.45, -1.9], [0.0, 1.0, -1.9], [0.95, 2.4, -1.35], [-1.0, 2.4, -1.4], [0.0, 1.15, -1.4]], top=0.14, bottom=0.76)])
st.cue('sfx:paper', 'S14', UNV14, 0.3); st.cue('sfx:fanfare', 'S14', r(UNV14 + 0.15), 0.35)

# 15: the other countries claimed it. Seen from above, a round summit table, little flags, the model of the cork in the middle: four leaders'
#    arms stretch across the table and grab it at once, and tug
D15 = st.dur('S15'); GRAB15 = 0.42; TC15 = [0.0, 0, -0.6]; MOD15 = [0.0, 1.12, -0.6]
CHEFS = [('chef1', 45), ('chef2', 135), ('chef3', 225), ('chef4', 315)]
def chef(cid, ang):
    a = ang * PI / 180; x, z = r(TC15[0] + 1.25 * math.sin(a)), r(TC15[2] + 1.25 * math.cos(a)); ry = r((ang + 180) % 360 - 360 if (ang + 180) % 360 > 180 else (ang + 180) % 360)
    tug = lambda d: [r(MOD15[0] + 0.06 * d * math.sin(a)), r(MOD15[1] + 0.02), r(MOD15[2] + 0.06 * d * math.cos(a))]
    return act(cid, [x, 0, z], ry, 'stand', 'angry', keys=[k(0.0, look=MOD15), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.0),
               k(GRAB15, toon={'reach': {'R': [*tug(0), 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'mouth': 'teeth', 'brow': -0.9}}, toonDur=0.12, toonEase='out'),   # the arms shoot across the table...
               *[k(r(GRAB15 + 0.2 + 0.16 * j), toon={'reach': {'R': [*tug(1 if (j + int(ang / 90)) % 2 else -1), 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [r(0.3 - (0.08 if (j + int(ang / 90)) % 2 else 0.0)), 0, 0, 1, None]}, 'lay': [r(-0.06 if (j + int(ang / 90)) % 2 else 0.0), 0.0],
                                                                   'face': {'lid': 0.0, 'mouth': 'clench' if j % 2 else 'teeth', 'brow': -0.9, 'vein': 1.0}}, toonDur=0.08) for j in range(6)]])   # ...and they tug
st.shot('S15', 'mairie', setOpts={'wall': '#E8E2F2', 'band': '#8C7AA8', 'trim': '#5E4C7A', 'banner': False}, actors=[chef(c, a) for c, a in CHEFS],
        props=[P('tab15', 'bistroTable', pos=TC15, opts={'r': 0.85, 'h': 1.0}), P('mod15', 'cork', pos=MOD15, scale=6.0), P('plinth15', 'slab', pos=[MOD15[0], 1.04, MOD15[2]], opts={'w': 0.22, 'h': 0.08, 'd': 0.22, 'color': '#2E3440'}),
               *[P(f'flag15{j}', 'flag', pos=[r(TC15[0] + 0.62 * math.sin((a + 12) * PI / 180)), 1.0, r(TC15[2] + 0.62 * math.cos((a + 12) * PI / 180))], scale=0.35, opts={'colors': cl})
                 for j, ((c_, a), cl) in enumerate(zip(CHEFS, [['#2F8F6B', '#F4F4F0', '#D9A13A'], ['#3A62B5', '#E0413A'], ['#F2C94E', '#2E3440', '#E0413A'], ['#8E5AA8', '#F4F4F0']]))]],
        cams=[FC(0.0, [2.0, 3.6, 2.3], [[-0.9, 2.45, -1.5], [0.9, 2.45, 0.3], [-0.9, 2.45, 0.3], [0.9, 2.45, -1.5], [0.0, 1.2, -0.6], [0.9, 1.7, 0.3]], top=0.12, bottom=0.74)])
st.cue('sfx:stretch', 'S15', GRAB15, 0.4); st.cue('sfx:grunt', 'S15', r(GRAB15 + 0.3), 0.3)

# 16: the man got a bill... On his landing: the postman in his cap holds out a big envelope; he takes it, the foam long gone
D16 = st.dur('S16'); HAND16 = 0.5
st.shot('S16', 'immeubleHall', actors=[
        act('facteur', [0.75, 0, 0.35], -50, 'stand', 'neutral', keys=[k(0.0, look=[-0.3, 2.2, 0.35]), k(0.0, toon={'reach': {'R': [0.28, 1.5, 0.45, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0),
            k(r(HAND16 + 0.1), toon={'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.25, toonEase='inOut')]),
        act('mec', [-0.4, 0, 0.3], 45, 'stand', 'unimpressed', keys=[k(0.0, look=[0.3, 1.5, 0.45]), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(r(HAND16 - 0.2), toon={'reach': {'L': [0.22, 1.5, 0.42, 1, 0.05]}, 'hands': {'L': 'pinch'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2, toonEase='inOut'),
            k(r(HAND16 + 0.15), toon={'reach': {'L': [-0.05, 1.55, 0.6, 1, 0.05], 'R': [0.05, 1.6, 0.62, 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {**DEAD, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.25, toonEase='inOut'), k(r(HAND16 + 0.2), look=[0.0, 1.5, 0.62])])],
        props=[P('env16a', 'bigEnvelope', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'w': 0.34}, keys=[k(0.0, visible=True), k(HAND16, visible=False)]),
               P('env16b', 'bigEnvelope', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, 0.0, 0.05]}, opts={'w': 0.34}, keys=[k(0.0, visible=False), k(HAND16, visible=True)])],
        cams=[FC(0.0, [0.25, 1.65, 2.6], [[-0.4, 2.45, 0.3], [0.75, 2.45, 0.35], [0.2, 1.2, 0.45], [-0.4, 0.6, 0.3]], top=0.14, bottom=0.78)])
st.cue('sfx:bell', 'S16', 0.05, 0.25); st.cue('sfx:paper', 'S16', HAND16, 0.25)

# 17: ...for taking up space. He opens it: the bill unrolls out of his hands, down to the floor and on along it toward us, line after line;
#    his eyes pop on their stalks
D17 = st.dur('S17'); POP17 = r(D17 - 0.55)
st.shot('S17', 'immeubleHall', actors=[
        act('mec', [-0.2, 0, 0.0], 0, 'stand', 'unimpressed', keys=[k(0.0, look=[-0.2, 1.3, 0.5]), k(0.0, toon={'reach': {'L': [-0.38, 1.55, 0.42, 1, 0.04], 'R': [-0.02, 1.55, 0.42, 1, 0.04]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {**DEAD, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.0),
            k(0.3, look=[-0.2, 0.0, 2.0]), k(0.3, toon={'reach': {'L': [-0.38, 1.55, 0.42, 1, 0.04], 'R': [-0.02, 1.55, 0.42, 1, 0.04]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 0.2, 'mouth': 'line', 'gy': 0.8}}, toonDur=0.2),   # his eyes follow it down...
            k(POP17, look='camera'), k(POP17, toon={'reach': {'L': [-0.38, 1.6, 0.42, 1, 0.04], 'R': [-0.02, 1.6, 0.42, 1, 0.04]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'sq': [0.94, 1.08, 0.94], 'hairUp': 1.0,
                                                    'face': {'lid': 0.0, 'pop': 0.6, 'popLen': 0.16, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out')])],   # ...POP: eyes out on stalks
        props=[P('bill17', 'billScroll', pos=[-0.2, 1.5, 0.45], opts={'w': 0.36, 'top': 1.5, 'head': 'FACTURE', 'items': ['OCCUPATION', "DE L'ESPACE", 'ORBITE', 'SURVOL', 'FRAIS DE DOSSIER', 'TIMBRE'], 'len': [[0.0, 0.25], [0.25, 1.5], [r(D17 - 0.2), 4.5]]})],
        cams=[FC(0.0, [0.75, 1.0, 3.2], [[-0.2, 2.6, 0.0], [-0.2, 0.0, 0.45], [-0.2, 0.0, 2.2], [0.35, 1.5, 0.3], [-0.75, 1.5, 0.3]], top=0.12, bottom=0.8)])
st.cue('sfx:paper', 'S17', 0.05, 0.3); st.cue('sfx:paper', 'S17', 0.45, 0.25); st.cue('sfx:cash', 'S17', POP17, 0.3); st.cue('sfx:gasp', 'S17', r(POP17 + 0.05), 0.3)

# 18: yesterday, the cork came back down. Above the clouds: it falls cap first in flames, a red streak plunging through the frame into the clouds
D18 = st.dur('S18'); C18 = [0.0, 150.0, 0.0]
st.shot('S18', 'skyHigh', actors=[],
        props=[P('cork18', 'cork', pos=C18, rot=[PI, 0, 0.3], scale=34, opts={'spin': 1.5, 'fire': [[0.0, 9.0]]}, keys=[k(0.0, to=[r(C18[0] - 10.0), 26.0, r(C18[2] + 3.0)], dur=D18, ease='linear')])],
        cams=[FC(0.0, [14.0, 146.0, 18.0], [[0.0, 159.0, 0.0], [0.0, 147.0, 0.0], [0.0, 138.0, 0.0]], top=0.12, bottom=0.8, drift=(-10.0, r(26.0 - C18[1]), 3.0))])   # the camera falls with it: the cloud deck rushes up
st.cue('whoosh', 'S18', 0.1, 0.4, 1.6, 900, 150); st.cue('sfx:jet', 'S18', 0.2, 0.25)

# 19: right into his glass. His living room: the flute still on the side table under the hole, flat; he bends close to look at it; the cork drops
#    through the hole straight into it: PLOUF, the wine jumps into his face
D19 = st.dur('S19'); DROP19 = 0.42; FLY19 = 0.12
st.shot('S19', 'livingRoom', actors=[
        act('mec', [-0.55, 0, 0.3], 30, 'stand', 'unimpressed', keys=[k(0.0, look=[SIDE[0], r(SIDE_H + 0.2), SIDE[2]]), k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1, None]}, 'face': {**DEAD, 'mouth': 'line', 'gy': 0.3}}, toonDur=0.0),
            k(DROP19, toon={'bend': {'spine': [0.35, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 1.0, 'mouth': 'wavy', 'brow': -0.4, 'sweat': 1.0}}, toonDur=0.04),   # PLOUF: eyes shut on the splash...
            k(r(DROP19 + 0.4), toon={'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'line', 'sweat': 1.0}}, toonDur=0.12), k(r(DROP19 + 0.45), look='camera')])],   # ...open, on us
        props=[CEILING('ceil19'), HOLEP('hole19', [HOLE[0], r(CEIL - 0.006), HOLE[2]], inner='#8EC5EA'),
               P('side19', 'table', pos=SIDE, opts={'w': 0.55, 'd': 0.45, 'h': SIDE_H}),
               P('flute19', 'flute', pos=[SIDE[0], SIDE_H, SIDE[2]], scale=CS, opts={'level': 0.75, 'flatAt': -1.0, 'splashAt': DROP19}),
               P('cork19', 'cork', pos=[HOLE[0], r(CEIL + 0.2), HOLE[2]], scale=CS, opts={'spin': 2.0, 'trail': [[r(DROP19 - FLY19), DROP19]], 'hideAt': DROP19}, keys=[k(r(DROP19 - FLY19), to=[SIDE[0], r(SIDE_H + 0.2), SIDE[2]], dur=FLY19, ease='in')]),
               BURST('plouf19', [0.45, 1.75, 0.65], r(DROP19 + 0.02), 'PLOUF !', 0.4, 0.3)],
        cams=[FC(0.0, [1.1, 2.3, 1.3], [[SIDE[0], r(SIDE_H - 0.1), SIDE[2]], [-0.55, 2.45, 0.3], [HOLE[0], r(CEIL + 0.02), HOLE[2]], [0.45, 1.3, 0.55]], top=0.08, bottom=0.78)])   # close over the flute, the hole above (the S01 set-up was repeated)
st.cue('whoosh', 'S19', r(DROP19 - FLY19), 0.25, 0.2, 1200, 400); st.cue('sfx:splash', 'S19', DROP19, 0.45)

# 20: the champagne was flat. Close: he lifts the flute, the cork in it, and sips; nothing fizzes; one last bubble comes up and pops (blop); his
#    mouth goes down; a look at us
D20 = st.dur('S20'); SIP20 = 0.35; BLOP20 = 1.0
st.shot('S20', 'livingRoom', actors=[
        act('mec', [-0.1, 0, 0.2], 10, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.6, 0.8]), k(0.0, toon={'touch': {'R': ['face', 0.02, 0.05, 0.22, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(SIP20, toon={'touch': {'R': ['face', 0.02, 0.12, 0.16, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'kiss'}}, toonDur=0.15, toonEase='inOut'), k(SIP20, look=[0.0, 1.2, 1.0]),   # a sip...
            k(r(SIP20 + 0.35), toon={'touch': {'R': ['face', 0.02, 0.02, 0.24, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'wavy', 'mouthTilt': -8, 'brow': -0.3, 'browTilt': 10}}, toonDur=0.18, toonEase='inOut'),   # ...flat...
            k(r(BLOP20 + 0.1), look='camera'), k(r(BLOP20 + 0.1), toon={'touch': {'R': ['face', 0.02, 0.02, 0.24, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.15),
            k(r(BLOP20 + 0.6), toon={'touch': {'R': ['face', 0.02, 0.02, 0.24, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.04), k(r(BLOP20 + 0.66), toon={'touch': {'R': ['face', 0.02, 0.02, 0.24, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.06),
            k(r(BLOP20 + 0.95), toon={'touch': {'R': ['face', 0.02, 0.0, 0.25, 1, 0.02]}, 'hands': {'R': 'grip'}, 'sq': [1.02, 0.97, 1.02], 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.12, toonEase='out'), k(r(BLOP20 + 1.15), toon={'touch': {'R': ['face', 0.02, 0.02, 0.24, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.15)])],   # ...and on us
        props=[P('flute20', 'flute', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.1, 0.03]}, scale=CS, opts={'level': 0.68, 'flatAt': -1.0, 'splashAt': -2.0, 'lastBubble': BLOP20})],
        cams=[FC(0.0, [0.45, 2.05, 1.6], [[-0.1, 2.55, 0.2], [-0.1, 1.45, 0.2], [0.25, 1.9, 0.5], [-0.45, 2.0, 0.2]], top=0.14, bottom=0.74)])
st.cue('sfx:gulp', 'S20', r(SIP20 + 0.15), 0.3); st.cue('sfx:pop', 'S20', BLOP20, 0.15)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.4}}
st.write("Le champagne", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': MEC,
    'voisine': {'preset': 'mamie', 'seed': 681, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'flic': {'preset': 'cop', 'seed': 682, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'commissaire': {'preset': 'commissaire', 'seed': 683, 'build': {'width': 1.0, 'headWidth': 1.25}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 684, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'suit': '#4A4F5A', 'lapel': '#4A4F5A', 'tie': '#7A2333', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant1': {'preset': 'savant', 'seed': 685, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 686, 'hairColor': '#6B4A2E', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'pere': {'preset': 'sportif', 'seed': 687, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'mere': {'preset': 'femme', 'seed': 688, 'suit': '#D9734E', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'gamin': {'preset': 'gamin', 'seed': 689, 'suit': '#3A9BDC', 'build': {'headScale': 1.25}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 690, 'suit': '#2B3A55', 'lapel': '#2B3A55', 'tie': '#9A2A2A', 'hairColor': '#5A4A3A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'garde': {'preset': 'pompier', 'seed': 691, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef1': {'preset': 'politique', 'seed': 692, 'suit': '#2F5E4A', 'lapel': '#2F5E4A', 'tie': '#D9A13A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef2': {'preset': 'prefet', 'seed': 693, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef3': {'preset': 'officiel', 'seed': 694, 'suit': '#6B3A3A', 'lapel': '#6B3A3A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef4': {'preset': 'avocat', 'seed': 695, 'suit': '#5A4A7A', 'lapel': '#5A4A7A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'facteur': {'preset': 'worker', 'seed': 696, 'hat': 'copcap', 'hatColor': '#2F62B5', 'suit': '#3A62A8', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
