#!/usr/bin/env python3
"""La ventouse (story 55, cycle 17 of the cartoon staging): this man stuck a plunger on his forehead. It will not come off. His mutual insurer will not
pay: it is plumbing. The plumber will not either: it is a forehead. Since then he sticks to everything. The metro hired him as a handle. Yesterday the
plunger came off. The metro kept it. He is out of work.
Staging: at the kitchen island he plunges the sink, three pumps, it sticks, he pulls with all his weight: it pops out, spins up and lands handle first
on his forehead, the red cup outward like a horn; he pulls on it with both hands and his head comes out on a neck like chewing gum before it snaps
back; at the insurer's counter the clerk flicks the cup with a finger: the handle shivers and his head with it; the plumber knocks on his forehead,
TOC, TOC, his head squashing at each knock, then taps his own forehead and shrugs; in the street the cup slaps onto a lamp post and he hangs from it by
the forehead, his legs swinging; a bus going by catches the cup on its window and drags him along flat as a flag; in the metro he hangs from the
ceiling by his plunger, his face to the roof, two passengers holding his hands like straps, and at the brake everybody swings; POP: he drops to the
floor with a red ring on his forehead, the plunger stays on the ceiling; a passenger holds it like a strap; on the platform he sits on a bench with
his red ring as the train pulls out.
Natural look; cycle 17 tool: the pin channel (a point of a joint held on a point of the world: the body hangs from it).
(pass 2) the metro floors 1 cm above the void floor (they strobed), the island platform, the taller carriage."""
from story_kit import *
import math

st = Story('ventouse', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 5), ('S06', 'L04', 0), ('S07', 'L04', 4),
         ('S08', 'L05', 0), ('S09', 'L05', 2), ('S10', 'L06', 0), ('S11', 'L06', 4), ('S12', 'L07', 0), ('S13', 'L07', 4), ('S14', 'L08', 0),
         ('S15', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
LOOKI = {'warm': 0.5}                                                   # interiors: the whites stay white
STREETV = {'eiffelStyle': 'v2'}
FORE = [0.0, 0.36, 0.085]                                               # his forehead in the frame of his head (0.24 wide, 0.5 high, 0.17 deep, the joint at the chin)
LH = 0.36; CR = 0.09; PLEN = round(0.9 * CR + LH + 0.05, 3)              # the handle, the cup, and the plunger from the rim of its cup to the end of its knob
PLOPTS = {'len': LH, 'r': CR}
HA = 0.7                                                                # (check stills) the horn tilted 40 degrees up from his face: straight out at us it was a red disc
HORN = {'actor': 'mec', 'joint': 'head', 'offset': [0.0, r(FORE[1] + PLEN * math.sin(HA)), r(FORE[2] + PLEN * math.cos(HA))], 'rot': [round(-(PI / 2 + HA), 4), 0, 0]}   # the knob on his forehead, the cup out and up
HORNP = lambda pid, opts=None, keys=None: P(pid, 'plunger', on=HORN, opts={**PLOPTS, **(opts or {})}, keys=keys or [])
RING = lambda pid, at_: P(pid, 'ringMark', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, r(FORE[1] + 0.05), r(FORE[2] + 0.004)]}, opts={'r': 0.05}, keys=[k(0.0, visible=False), k(at_, visible=True)])   # (pass 2) smaller and higher (over his eye it read as a red monocle)
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
PIN = lambda at_, w=1: {'pin': {'joint': 'head', 'off': FORE, 'at': [r(at_[0]), r(at_[1]), r(at_[2])], 'w': w}}

# 1: the hook. His kitchen, the island sink between us and him: he plunges, three pumps, the cup squashing; it sticks; he pulls with all his weight
D1 = st.dur('S01')
ISL = [0.0, 0, -1.2]; DRAIN = [0.0, 0.745, -1.2]; MEK = [0.0, 0, -1.95]
HANDY = r(DRAIN[1] + 0.0675 + LH - 0.04)                                 # where his hands hold the handle, the cup in the drain
GRAB = lambda dy=0.0, w=1: {'reach': {'L': [-0.035, r(HANDY + dy), DRAIN[2], w, 0.03], 'R': [0.035, r(HANDY + 0.09 + dy), DRAIN[2], w, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}}
st.shot('S01', 'kitchenDay', look=LOOKI, actors=[
        act('mec', MEK, 0, 'stand', 'determined', keys=[k(0.0, look=[DRAIN[0], DRAIN[1], DRAIN[2]]), k(0.0, toon={**GRAB(), 'face': {'brow': -0.4, 'tongue': 0.5, 'tongueLen': 0.08}}, toonDur=0.0),
            *[x for i, t_ in enumerate((0.08, 0.36, 0.64)) for x in (
                k(t_, toon={**GRAB(-0.07), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [1.06, 0.93, 1.06], 'face': {'brow': -0.5, 'tongue': 0.6, 'tongueLen': 0.09}}, toonDur=0.1, toonEase='in'),   # a pump down...
                k(round(t_ + 0.13, 3), toon={**GRAB(0.02), 'bend': {'spine': [0.05, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'brow': -0.3, 'tongue': 0.4, 'tongueLen': 0.07}}, toonDur=0.1, toonEase='out'))],   # ...and up
            k(0.84, toon={**GRAB(0.12), 'lay': [-0.55, 0.0], 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'sq': [0.94, 1.08, 0.94], 'face': {'brow': -0.8, 'lid': 0.7, 'mouth': 'grimace', 'cheeks': 0.6}}, toonDur=0.16, toonEase='out')])],
            # it sticks: he leans back with all his weight, the arms stretched, a grimace
            # (pass 2) back 31 degrees on straight arms (upright, fists at his waist: no build for the POP)
        props=[P('isl1', 'islandSink', pos=ISL),
               P('pl1', 'plunger', pos=DRAIN, opts={**PLOPTS, 'squash': [[0.18, 0.5], [0.46, 0.5], [0.74, 0.5]]},
                 keys=[k(0.86, scale=1.0)])],
        cams=[FC(0.0, [1.55, 1.6, -0.35], [[MEK[0], 2.45, MEK[2]], [MEK[0], 1.0, MEK[2]], [MEK[0], 2.2, r(MEK[2] - 1.15)], [MEK[0], 0.0, r(MEK[2] - 0.3)], [-0.55, 0.9, ISL[2]], [0.55, 0.9, ISL[2]], [DRAIN[0], 0.75, DRAIN[2]]], top=0.12, bottom=0.74, drift=(-0.05, 0.0, -0.06))])   # (check stills) the leaning head inside (cut by the right edge)
        # (pass 2) three-quarters from his side, lower: the lean back reads as a diagonal (from the front, high, he stood upright in a white tray)
st.cue('sfx:squeak', 'S01', 0.18, 0.25); st.cue('sfx:squeak', 'S01', 0.46, 0.25); st.cue('sfx:squeak', 'S01', 0.74, 0.25)

# 2: a plunger on his forehead. Closer: POP, it comes out of the drain, spins up and lands handle first on his forehead with a SCHLOUP: his head knocked
#    back and squashed, his eyes out; he staggers; the red cup sticks out of his forehead like a horn
D2 = st.dur('S02'); POP2 = 0.08; HIT2 = 0.28
FORE2 = [MEK[0], 1.99, r(MEK[2] + 0.085)]                                  # his forehead, standing
st.shot('S02', 'kitchenDay', look=LOOKI, actors=[
        act('mec', MEK, 0, 'stand', 'determined', keys=[k(0.0, look=[DRAIN[0], DRAIN[1], DRAIN[2]]), k(0.0, toon={**GRAB(0.12), 'lay': [-0.22, 0.0], 'bend': {'spine': [-0.35, 0, 0, 1, None]}, 'hose': 0.15, 'face': {'brow': -0.8, 'lid': 0.7, 'mouth': 'grimace'}}, toonDur=0.0),
            k(POP2, toon={'reach': {'L': [-0.35, 1.5, -1.6, 1, 0.05], 'R': [0.35, 1.55, -1.6, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'lay': [-0.12, 0.0], 'face': {'eye': 0.3, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.06, toonEase='out'),   # POP: his hands fly up...
            k(round(HIT2 - 0.02, 3), look=[FORE2[0], 2.8, 0.0]),
            k(HIT2, toon={'bend': {'neck': [-0.55, 0, 0, 1, None]}, 'scl': {'head': [1.22, 0.78, 1.22]}, 'sq': [1.08, 0.9, 1.08], 'reach': {'L': [-0.45, 1.85, -1.7, 1, 0.05], 'R': [0.45, 1.85, -1.7, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'},
                          'face': {'pop': 0.65, 'popLen': 0.25, 'brow': 1.0, 'mouth': 'O', 'jaw': 0.4}}, toonDur=0.033, toonEase='out'),   # ...SCHLOUP: the head knocked back and squashed, eyes out
            k(round(HIT2 + 0.1, 3), to=[MEK[0], 0, r(MEK[2] - 0.22)], dur=0.22, ease='out', face='keep'),   # he staggers back a step
            k(round(HIT2 + 0.12, 3), toon={'bend': {'neck': [0.15, 0, 0, 1, None]}, 'scl': {'head': [0.94, 1.06, 0.94]}, 'lay': [0.06, 0.0], 'face': {'pop': 0.3, 'popLen': 0.2, 'brow': 0.6}}, toonDur=0.08),
            k(round(HIT2 + 0.3, 3), toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.3, 'cross': 1.0, 'gy': -0.5}}, toonDur=0.1), k(round(HIT2 + 0.3, 3), look='camera'),   # cross-eyed at the horn, the eyes wide (pass 2: half-lidded, two slits)
            k(round(D2 - 0.22, 3), toon={'face': {'lid': 0.45, 'cross': 0.0}}, toonDur=0.1)])],
        props=[P('isl2', 'islandSink', pos=ISL),
               P('pl2f', 'plunger', pos=DRAIN, opts=PLOPTS, keys=[k(POP2, to=[0.05, 2.75, -1.45], dur=0.12, ease='out'), k(POP2, rotTo=[3.6, 0.4, 0.0], dur=0.12),
                                                                  k(round(POP2 + 0.12, 3), to=[FORE2[0], r(FORE2[1] + PLEN * math.sin(HA)), r(FORE2[2] + PLEN * math.cos(HA))], dur=round(HIT2 - POP2 - 0.12, 3), ease='in'), k(round(POP2 + 0.12, 3), rotTo=[round(-(PI / 2 + HA) + 2 * PI, 4), 0.0, 0.0], dur=round(HIT2 - POP2 - 0.12, 3)),
                                                                  k(HIT2, visible=False)]),   # it flies up out of the drain, spins and comes down handle first...
               HORNP('pl2h', {'wobble': [[HIT2, 0.35, 30, 5]]}, [k(0.0, visible=False), k(HIT2, visible=True)]),   # ...and stays on his forehead, quivering
               BURST('sch2', [r(FORE2[0] + 0.45), 2.35, r(FORE2[2] + 0.3)], HIT2, 'SCHLOUP !', 0.55)],
        cams=[FC(0.0, [0.75, 1.75, 0.6], [[MEK[0], 2.85, MEK[2]], [MEK[0], 1.0, MEK[2]], [-0.6, 1.8, MEK[2]], [0.75, 2.4, MEK[2]], [DRAIN[0], 1.0, DRAIN[2]]], top=0.1, bottom=0.72),
              FC(0.62, [0.45, 2.15, -0.75], [[MEK[0], 2.95, r(MEK[2] - 0.22)], [MEK[0], 1.65, r(MEK[2] - 0.22)]], top=0.12, bottom=0.66)])   # (pass 2) a cut in on the take at the horn
st.cue('pop', 'S02', POP2, 0.45); st.cue('sfx:bonk', 'S02', HIT2, 0.45); st.cue('sfx:twang', 'S02', round(HIT2 + 0.02, 3), 0.3)

# 3: it will not come off. Three-quarters: both hands on the handle, he pulls: his head comes out on a neck like chewing gum, his body leaning back; his
#    hands slip: the head snaps back, wobbling; the plunger has not moved
D3 = st.dur('S03'); SL3 = 0.78; ME3 = [0.0, 0, -2.15]   # (pass 2) seen in profile: from three-quarters behind his raised arms covered the neck
PULL = lambda d, w=1: {'touch': {'L': ['head', -0.04, FORE[1], r(FORE[2] + 0.12 + d), w, 0.03], 'R': ['head', 0.04, FORE[1], r(FORE[2] + 0.24 + d), w, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}}
st.shot('S03', 'kitchenDay', look=LOOKI, actors=[
        act('mec', ME3, 0, 'stand', 'determined', keys=[k(0.0, look=None), k(0.0, toon={**PULL(0.0), 'face': {'brow': -0.5}}, toonDur=0.0),
            k(0.1, toon={**PULL(0.0), 'bend': {'neck': [0.35, 0, 0, 1.35, None], 'spine': [-0.25, 0, 0, 1, None]}, 'lay': [-0.12, 0.0], 'face': {'brow': -0.8, 'lid': 0.75, 'mouth': 'clench'}}, toonDur=0.25, toonEase='inOut'),
            k(0.4, toon={**PULL(0.0), 'bend': {'neck': [0.55, 0, 0, 2.1, None], 'spine': [-0.4, 0, 0, 1, None]}, 'lay': [-0.2, 0.0], 'sq': [0.95, 1.06, 0.95], 'face': {'brow': -1.0, 'lid': 0.9, 'mouth': 'clench', 'cheeks': 0.8, 'vein': 0.8}}, toonDur=0.3, toonEase='inOut'),
            *[k(round(0.7 + 0.033 * i, 3), toon={**PULL(0.0), 'bend': {'neck': [0.55, 0, 0, round(2.1 + (0.05 if i % 2 else -0.05), 3), None], 'spine': [-0.4, 0, 0, 1, None]}, 'lay': [-0.2, 0.0], 'face': {'brow': -1.0, 'lid': 0.9, 'mouth': 'clench', 'vein': 0.8}}, toonDur=0.03) for i in range(2)],
            # the head out on a neck twice its length, quivering at the limit...
            k(SL3, toon={'reach': {'L': [-0.55, 1.2, r(ME3[2] - 0.4), 1, 0.05], 'R': [0.55, 1.25, r(ME3[2] - 0.4), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'neck': [-0.2, 0, 0, 0.78, None]}, 'lay': [-0.28, 0.0], 'sq': [1.08, 0.92, 1.08], 'face': {'eye': 0.35, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),
            # ...his hands slip: the head snaps back past its place, his arms fly back...
            k(round(SL3 + 0.07, 3), toon={'bend': {'neck': [0.14, 0, 0, 1.18, None]}, 'lay': [-0.05, 0.0], 'face': {'brow': 0.3}}, toonDur=0.06), k(round(SL3 + 0.14, 3), toon={'bend': {'neck': [-0.08, 0, 0, 0.88, None]}, 'face': {'lid': 0.45}}, toonDur=0.06),
            k(round(SL3 + 0.21, 3), toon={'bend': {'neck': [0.05, 0, 0, 1.08, None]}, 'face': {'lid': 0.45}}, toonDur=0.06), k(round(SL3 + 0.28, 3), toon={'bend': {'neck': [-0.02, 0, 0, 0.96, None]}, 'face': {'lid': 0.45}}, toonDur=0.06),
            k(round(SL3 + 0.36, 3), toon={'bend': {'neck': [0.0, 0, 0, 1.0, None]}, 'face': {'lid': 0.45}}, toonDur=0.08)])],   # ...and wobbles to rest, four times, deadpan
        props=[P('isl3', 'islandSink', pos=ISL), HORNP('pl3', {'wobble': [[SL3, 0.3, 30, 5]]})],
        cams=[FC(0.0, [2.05, 2.05, -1.0], [[ME3[0], 2.95, ME3[2]], [ME3[0], 1.15, ME3[2]], [ME3[0], 2.1, r(ME3[2] + 1.1)], [ME3[0], 2.9, r(ME3[2] - 0.7)], [ME3[0], 2.9, r(ME3[2] + 0.7)]], top=0.12, bottom=0.72, drift=(0.0, 0.0, -0.04))])   # (check stills) the head inside as it leans back (cut by the right edge)   # (pass 2) three-quarters front from his right, 60 degrees: the neck a long line and his face still painted on (a true profile shows a blank box side)
st.cue('sfx:stretch', 'S03', 0.12, 0.3); st.cue('sfx:twang', 'S03', SL3, 0.4)

# 4: his mutual insurer will not pay. MUTUELLE: he stands with his back to the counter, the plunger sticking out of his forehead at us; the clerk leans
#    out over the counter behind him and looks at it over her glasses
D4 = st.dur('S04')
POSTEV = {'title': 'MUTUELLE', 'guichets': False}
ME4 = [-0.4, 0, -1.55]; CLK4 = [0.35, 0, -2.62]   # (stills v2) the clerk off his shoulder, to his left: behind him she was a pale ghost
LEAN4 = {'bend': {'spine': [0.75, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}}   # (pass 2) further out over the counter (she only tilted her head behind the glass)
TIP4 = [ME4[0], r(1.99 + PLEN * math.sin(HA)), r(ME4[2] + 0.085 + PLEN * math.cos(HA))]
st.shot('S04', 'poste', setOpts=POSTEV, look=LOOKI, actors=[
        act('mec', ME4, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.5, toon={'sq': [1.0, 1.015, 1.0], 'face': {'lid': 0.45}}, toonDur=0.3, toonEase='inOut'), k(1.3, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(1.4, toon={'face': {'lid': 0.45}}, toonDur=0.08)]),
        act('guichet', CLK4, -10, 'stand', 'unimpressed', keys=[k(0.0, look=[ME4[0], 2.0, r(ME4[2] + 0.3)]), k(0.0, toon={**LEAN4, 'face': {'lid': 0.55, 'gy': 0.3}}, toonDur=0.0),
            k(0.3, look=TIP4), k(0.46, look=[ME4[0], 2.0, r(ME4[2] + 0.3)]), k(0.66, look=TIP4),   # (pass 2) a double take: a glance at the cup, back to him, and the snap back to it
            k(0.62, toon={**LEAN4, 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.6, 'gy': 0.2}}, toonDur=0.04, toonEase='in'),
            k(0.66, toon={**LEAN4, 'face': {'pop': 0.55, 'popLen': 0.22, 'brow': 1.0, 'lid': 0.2, 'gy': 0.1}}, toonDur=0.05, toonEase='outBack'),
            k(1.05, toon={**LEAN4, 'face': {'lid': 0.4, 'brow': 0.7, 'gy': 0.1}}, toonDur=0.15)])],
        props=[HORNP('pl4')],
        cams=[FC(0.0, [0.55, 1.7, 1.5], [[ME4[0], 2.45, ME4[2]], [ME4[0], 0.9, ME4[2]], [r(ME4[0] - 0.45), 1.8, ME4[2]], [r(ME4[0] + 0.45), 1.8, ME4[2]], [ME4[0], 2.0, r(ME4[2] + 0.65)], [CLK4[0], 2.15, r(CLK4[2] + 0.4)], [-0.95, 3.3, -3.45], [0.95, 3.05, -3.45]],
                 top=0.06, bottom=0.74, lenses=range(30, 57), drift=(-0.04, 0.0, -0.08)),
              FC(1.1, [r(ME4[0] + 0.3), 2.05, r(ME4[2] + 1.4)], [[ME4[0], 2.95, r(ME4[2] + 0.3)], [ME4[0], 1.6, ME4[2]]], top=0.12, bottom=0.66)])   # (pass 2) then in on his deadpan blink   # (check stills) the word, not the whole plate
        # from in front: his face and the cup at us, her face over his shoulder, the whole word MUTUELLE

# 5: it is plumbing. Closer: her arm comes out over his shoulder, stretching to the cup, and flicks it: the handle shivers and his head with it
D5 = st.dur('S05'); FL5 = 0.24
TIP5 = [ME4[0], r(1.99 + PLEN * math.sin(HA)), r(ME4[2] + 0.085 + PLEN * math.cos(HA))]
st.shot('S05', 'poste', setOpts=POSTEV, look=LOOKI, actors=[
        act('mec', ME4, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            *[k(round(FL5 + 0.06 * i, 3), toon={'bend': {'neck': [0.0, round(0.16 * (0.72 ** i) * (1 if i % 2 == 0 else -1), 3), 0, 1, None]}, 'face': {'lid': 0.45, 'gx': (0.3 if i % 2 else -0.3)}}, toonDur=0.05) for i in range(8)],
            k(round(FL5 + 0.55, 3), toon={'face': {'lid': 0.45}}, toonDur=0.08)]),   # his head shivers with the handle, deadpan
        act('guichet', CLK4, -10, 'stand', 'unimpressed', keys=[k(0.0, look=TIP5), k(0.0, toon={**LEAN4, 'reach': {'R': [r(TIP5[0] + 0.25), r(TIP5[1] + 0.1), r(TIP5[2] - 0.3), 1, 0.05]}, 'hands': {'R': 'point'}, 'hose': 0.12, 'face': {'lid': 0.5}}, toonDur=0.0),
            k(round(FL5 - 0.14, 3), toon={**LEAN4, 'reach': {'R': [r(TIP5[0] + 0.12), r(TIP5[1] + 0.05), r(TIP5[2] - 0.02), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.12, 'face': {'lid': 0.5}}, toonDur=0.08, toonEase='inOut'),   # her arm stretched out over his shoulder: the finger cocked...
            k(round(FL5 - 0.03, 3), toon={**LEAN4, 'reach': {'R': [r(TIP5[0] + 0.04), TIP5[1], r(TIP5[2] + 0.02), 1, 0.05]}, 'hands': {'R': 'point'}, 'hose': 0.12, 'face': {'lid': 0.5}}, toonDur=0.03, toonEase='in'),   # ...the flick...
            k(round(FL5 + 0.04, 3), toon={**LEAN4, 'reach': {'R': [r(TIP5[0] - 0.15), r(TIP5[1] + 0.08), r(TIP5[2] + 0.06), 1, 0.05]}, 'hands': {'R': 'point'}, 'hose': 0.12, 'face': {'lid': 0.5, 'brow': 0.5}}, toonDur=0.05, toonEase='out'),
            k(round(FL5 + 0.14, 3), toon={**LEAN4, 'face': {'lid': 0.5, 'brow': 0.5}}, toonDur=0.16, toonEase='inOut'),   # ...and her hand away (it hung by the cup: a raised finger, 'ahem')
            k(round(FL5 + 0.4, 3), toon={**LEAN4, 'face': {'lid': 0.5, 'brow': 0.5, 'mouth': 'smirk'}}, toonDur=0.2)])],   # a smirk
        props=[HORNP('pl5', {'wobble': [[FL5, 0.45, 34, 4.5]]})],
        cams=[FC(0.0, [0.35, 1.85, 0.8], [[ME4[0], 2.3, ME4[2]], [ME4[0], 1.45, ME4[2]], [ME4[0], 2.0, TIP5[2]], [r(ME4[0] + 0.35), 1.8, ME4[2]], [r(ME4[0] - 0.4), 1.8, ME4[2]], [CLK4[0], 2.1, r(CLK4[2] + 0.4)]],
                 top=0.3, bottom=0.7, lenses=range(30, 57))])   # (pass 2) the cup and the flick at 30-40 % of the height, under the PLOMBERIE card (they sat in its band)
st.cue('sfx:boing', 'S05', FL5, 0.45)

# 6: the plumber will not either. His kitchen: the plumber in his blue overalls knocks on his forehead beside the plunger: TOC, TOC, his head squashing
D6 = st.dur('S06'); KN6 = (0.38, 0.72)
# (pass 2) the plumber at his left, his knocking arm behind the man's head (in front of it, the fist and the arm covered his face); the head squashed
# 38 % from the side at each TOC, held two frames, back past its shape (it only dipped); the bursts beside the knock, inside the frame (a corner); the
# second plunger on the worktop out (it competed with the one on his forehead)
ME6 = [-0.25, 0, -2.0]; PLB = [0.55, 0, -2.1]
KNOCK = [r(ME6[0] + 0.17), 2.08, r(ME6[2] - 0.02)]                       # his left temple
SQH = lambda k_: {'scl': {'head': [r(1 - 0.38 * k_), r(1 + 0.12 * k_), r(1 + 0.1 * k_)]}}
st.shot('S06', 'kitchenDay', look=LOOKI, actors=[
        act('mec', ME6, 20, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [PLB[0], 1.9, PLB[2]], 'cheat': 0.5}), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),   # (check stills) cheated to the lens (an 80-degree profile)
            *[x for t_ in KN6 for x in (k(t_, toon={**SQH(1.0), 'sq': [1.02, 0.98, 1.02], 'lay': [0.0, -0.06], 'face': {'lid': 0.8, 'gx': -0.4}}, toonDur=0.03, toonEase='out'),   # TOC: the head squashed from the side...
                                         k(round(t_ + 0.07, 3), toon={**SQH(0.95), 'lay': [0.0, -0.06], 'face': {'lid': 0.8, 'gx': -0.4}}, toonDur=0.03),             # ...held two frames...
                                         k(round(t_ + 0.13, 3), toon={**SQH(-0.2), 'face': {'lid': 0.45}}, toonDur=0.06, toonEase='outBack'),                          # ...back past its shape...
                                         k(round(t_ + 0.21, 3), toon={'face': {'lid': 0.45}}, toonDur=0.06))],
            k(1.15, look='camera')]),
        act('plombier', PLB, -100, 'stand', 'neutral', keys=[k(0.0, look=KNOCK), k(0.0, toon={'reach': {'R': [r(KNOCK[0] + 0.12), r(KNOCK[1] + 0.15), r(KNOCK[2] - 0.12), 1, 0.05]}, 'hands': {'R': 'fist'}, 'face': {'brow': 0.4, 'lid': 0.5}}, toonDur=0.0),
            *[x for t_ in KN6 for x in (k(round(t_ - 0.06, 3), toon={'reach': {'R': [*KNOCK, 1, 0.05]}, 'hands': {'R': 'fist'}, 'face': {'brow': 0.4, 'lid': 0.5}}, toonDur=0.06, toonEase='in'),
                                         k(round(t_ + 0.04, 3), toon={'reach': {'R': [r(KNOCK[0] + 0.12), r(KNOCK[1] + 0.15), r(KNOCK[2] - 0.12), 1, 0.05]}, 'hands': {'R': 'fist'}, 'face': {'brow': 0.6, 'lid': 0.5}}, toonDur=0.1))],
            k(1.1, toon={'reach': {'R': [r(PLB[0] - 0.1), 1.2, r(PLB[2] - 0.25), 0, 0.05]}, 'face': {'brow': 0.7, 'mouth': 'flat'}}, toonDur=0.2)])],
        props=[P('isl6', 'islandSink', pos=ISL), HORNP('pl6'),
               BURST('toc6a', [r(KNOCK[0] + 0.35), r(KNOCK[1] + 0.28), r(KNOCK[2] + 0.15)], KN6[0], 'TOC !', 0.4), BURST('toc6b', [r(KNOCK[0] + 0.42), r(KNOCK[1] - 0.02), r(KNOCK[2] + 0.2)], KN6[1], 'TOC !', 0.4)],
        cams=[FC(0.0, [0.25, 1.75, 1.2], [[ME6[0], 2.5, ME6[2]], [ME6[0], 0.9, ME6[2]], [PLB[0], 2.35, PLB[2]], [PLB[0], 0.9, PLB[2]], [r(ME6[0] - 0.4), 1.8, ME6[2]], [r(PLB[0] + 0.35), 1.8, PLB[2]]], top=0.12, bottom=0.72)])
st.cue('clack', 'S06', KN6[0], 0.45); st.cue('clack', 'S06', KN6[1], 0.45)

# 7: it is a forehead. The plumber taps his own forehead with a finger, eyebrows up, and shrugs; the man, deadpan, blinks
D7 = st.dur('S07')
st.shot('S07', 'kitchenDay', look=LOOKI, actors=[
        act('mec', ME6, 20, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [PLB[0], 1.9, PLB[2]], 'cheat': 0.5}), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0), k(0.55, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(0.66, toon={'face': {'lid': 0.45}}, toonDur=0.08)]),
        act('plombier', PLB, -8, 'stand', 'neutral', keys=[k(0.0, look='camera'),   # (check stills) turned to us (we saw the back of his head)
            k(0.0, toon={'touch': {'R': ['head', 0.05, 0.46, 0.11, 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'lid': 0.4, 'mouth': 'flat'}}, toonDur=0.0),   # (pass 2) on his forehead (at 0.38 the finger sat on his glasses)
            *[k(round(0.08 + 0.12 * i, 3), toon={'touch': {'R': ['head', 0.05, 0.46, (0.09 if i % 2 else 0.12), 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'lid': 0.4, 'mouth': 'flat'}}, toonDur=0.06) for i in range(3)],   # tap, tap, tap
            k(0.5, toon={'reach': {'L': [r(PLB[0] + 0.15), 1.25, r(PLB[2] - 0.45), 1, 0.05], 'R': [r(PLB[0] - 0.45), 1.25, r(PLB[2] + 0.15), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}, 'sq': [1.04, 0.96, 1.04], 'face': {'brow': 1.0, 'mouth': 'flat'}}, toonDur=0.12, toonEase='outBack')])],   # a shrug
        props=[P('isl7', 'islandSink', pos=ISL), HORNP('pl7')],
        cams=[FC(0.0, [0.2, 1.8, 0.6], [[PLB[0], 2.45, PLB[2]], [PLB[0], 1.1, PLB[2]], [ME6[0], 2.3, ME6[2]], [r(PLB[0] + 0.5), 1.6, PLB[2]], [r(ME6[0] - 0.3), 1.9, ME6[2]]], top=0.12, bottom=0.72)])   # (check stills) the two side by side (he stood in front of the man)

# 8: since then he sticks to everything. The street: walking, the cup slaps onto a lamp post: he hangs from it by the forehead, his legs swinging
D8 = st.dur('S08'); HIT8 = 0.24
LAMP = [6.0, 0, -0.6]; HANG8 = [r(LAMP[0] - 0.09 - PLEN * math.cos(HA)), 2.75, LAMP[2]]   # his forehead: the horn slants up to the post, its cup on it; (pass 2) 0.35 m higher: his feet off the ground (level with his standing forehead, he read as leaning on the post)
SW8 = lambda a: {'lay': [r(a), 0.0], 'bend': {'legL': [r(0.2 + a * 0.8), 0.05, 0, 1, None], 'legR': [r(0.05 - a * 0.6), -0.05, 0, 1, None], 'shinL': [0.4, 0, 0, 1, None], 'shinR': [0.25, 0, 0, 1, None]}}
st.shot('S08', 'parisStreet', setOpts=STREETV, actors=[
        act('mec', [r(HANG8[0] - 1.0), 0, LAMP[2]], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None),
            k(0.0, to=[HANG8[0], 0, LAMP[2]], dur=HIT8, clip='walk', then='stand', ease='linear', face='keep'),
            k(HIT8, toon={**PIN(HANG8), **SW8(0.55), 'sq': [1.08, 0.92, 1.08], 'face': {'eye': 0.3, 'brow': 0.8}}, toonDur=0.04, toonEase='out'),   # THWOK: stuck, his legs fly up...
            *[k(round(HIT8 + 0.12 + 0.12 * i, 3), toon={**PIN(HANG8), **SW8(0.55 * (0.62 ** (i + 1)) * (-1 if i % 2 == 0 else 1)), 'face': {'lid': 0.45}}, toonDur=0.12, toonEase='inOut') for i in range(4)]])],   # ...and swing, dying down
        props=[P('lamp8', 'streetLamp', pos=LAMP), HORNP('pl8', {'squash': [[HIT8, 0.5]]})],
        cams=[FC(0.0, [7.6, 1.25, 1.5], [[HANG8[0], 3.45, LAMP[2]], [HANG8[0], 0.0, LAMP[2]], [LAMP[0], 3.6, LAMP[2]], [r(HANG8[0] - 0.9), 1.6, LAMP[2]]], top=0.08, bottom=0.72, lenses=range(30, 57))])   # (check stills) closer: his feet 0.75 m off the pavement, his shadow under them (with the lamp's head in he was 7 % of the frame)
st.cue('sfx:splat', 'S08', HIT8, 0.45)

# 9: everything. Even what flies by: on the pavement a pigeon flies straight into the cup and sticks there, flapping; his head knocked back; deadpan
# (check stills) the bus dragging him hid his face and filled the frame; everything sticks to him instead
D9 = st.dur('S09'); HIT9 = 0.3
ME9 = [8.0, 0, -0.9]
CUP9 = [0.0, r(FORE[1] + (PLEN + 0.06) * math.sin(HA)), r(FORE[2] + (PLEN + 0.06) * math.cos(HA))]   # just past the cup's rim, in the frame of his head
st.shot('S09', 'parisStreet', setOpts={**STREETV, 'clear': [-14.0, 0.0]}, actors=[   # (pass 2) no lamp post behind his head (its arm met the cup: stuck to a lamp again)
        act('mec', ME9, 25, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            k(HIT9, toon={'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'scl': {'head': [1.1, 0.88, 1.1]}, 'lay': [-0.05, 0.0], 'face': {'lid': 0.6, 'brow': 0.4}}, toonDur=0.033, toonEase='out'),   # THWOK: his head knocked back...
            k(round(HIT9 + 0.12, 3), toon={'bend': {'neck': [0.06, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'gy': -0.6, 'cross': 0.5}}, toonDur=0.1),   # ...his eyes up at the pigeon on his horn...
            *[k(round(HIT9 + 0.2 + 0.08 * i, 3), toon={'bend': {'neck': [0.06, 0, round(0.3 * (0.75 ** i) * (1 if i % 2 == 0 else -1), 3), 1, None]}, 'face': {'lid': 0.45, 'gy': -0.6, 'cross': 0.5}}, toonDur=0.07) for i in range(4)],   # (pass 2) the pigeon tugs his head from side to side...
            k(round(D9 - 0.04, 3), toon={'face': {'lid': 0.45, 'gy': -0.6, 'cross': 0.5}}, toonDur=0.04)])],   # ...deadpan (it perched calmly)
        props=[HORNP('pl9', {'squash': [[HIT9, 0.5]], 'wobble': [[HIT9, 0.3, 30, 5]]}),
               P('pig9', 'pigeon', pos=[r(ME9[0] - 2.6), 3.2, r(ME9[2] - 1.2)], ry=60, scale=1.4, opts={'flap': [0.0, round(D9 + 0.5, 3)]},
                 keys=[k(0.0, to=[r(ME9[0] + 0.15), 2.45, r(ME9[2] + 0.35)], dur=HIT9, ease='in'),   # it flies straight at him...
                       k(HIT9, attach='mec', joint='head', offset=CUP9, rot=[0.0, round(PI / 2, 4), 0.0]), k(HIT9, squash=[0.75, 1.2, 1.15], dur=0.3)])],   # ...and stays stuck on the cup, still flapping
        cams=[FC(0.0, [9.3, 1.55, 1.7], [[ME9[0], 2.95, ME9[2]], [ME9[0], 0.6, ME9[2]], [r(ME9[0] - 0.45), 1.8, ME9[2]], [r(ME9[0] + 0.5), 2.6, r(ME9[2] + 0.3)], [r(ME9[0] - 1.2), 2.9, r(ME9[2] - 0.6)]], top=0.1, bottom=0.74, lenses=range(30, 57))])
st.cue('sfx:splat', 'S09', HIT9, 0.4); st.cue('sfx:cluck', 'S09', round(HIT9 + 0.05, 3), 0.3)

# 10: the metro hired him as a handle. In the carriage: he hangs from the ceiling by his plunger, his face to the roof; two passengers hold his hands
#     like straps
# (pass 2) a taller carriage (2.75 m): hung from its roof his feet clear the floor by 0.4 m (under a 2.3 m roof they touched it and he read as
# standing); a paler floor under his navy trousers (1.05 to 1); the passengers' hands closed on his, which hang
D10 = st.dur('S10'); CEIL = 2.74
MTR = [0.0, 0.0, 0.0]; HANG10 = [0.0, r(CEIL - PLEN), 0.0]
UPF = {'bend': {'neck': [round(-(PI / 2 - HA), 3), 0, 0, 1, None]}}      # the head back 50 degrees: the horn straight up to the roof, his face half up to us
ARMS10 = {'reach': {'L': [0.0, 1.95, -0.42, 1, 0.05], 'R': [0.0, 1.95, 0.42, 1, 0.05]}, 'hands': {'L': 'rest', 'R': 'rest'}}
P1 = [0.1, 0, -0.66]; P2 = [-0.1, 0, 0.66]   # close in: the camera looks down the carriage, 2.6 m wide
HOLD = lambda z: {'reach': {'R': [0.0, 1.95, r(z), 1, 0.05]}, 'hands': {'R': 'grip'}}
INSIDE = (-5.8, 5.8, 0.2, 2.65, -1.2, 1.2)
def METRO(sid, extra_keys=None, sway=None):
    return P(f'car{sid}', 'metroCar', pos=MTR, opts={'len': 12.0, 'h': 2.75, 'floor': '#A3A8AE', **({'sway': sway} if sway else {})})
st.shot('S10', 'whiteVoid', setOpts={'color': '#2A2E33'}, look=LOOKI, actors=[
        act('mec', [0.0, 0, 0.0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**PIN(HANG10), **UPF, **ARMS10, 'face': {'lid': 0.45, 'gy': 0.5}}, toonDur=0.0),
            k(0.45, toon={**PIN(HANG10), **UPF, **ARMS10, 'lay': [0.0, 0.04], 'face': {'lid': 0.45, 'gy': 0.6}}, toonDur=0.3, toonEase='inOut')]),
        act('p1', P1, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD(-0.42), 'face': {'lid': 0.5}}, toonDur=0.0), k(0.5, toon={**HOLD(-0.42), 'face': {'lid': 1.0}}, toonDur=0.05), k(0.6, toon={**HOLD(-0.42), 'face': {'lid': 0.5}}, toonDur=0.08)]),
        act('p2', P2, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.9, -1.0]), k(0.0, toon={**HOLD(0.42), 'face': {'lid': 0.5}}, toonDur=0.0)])],
        props=[METRO('S10'), HORNP('pl10'), P('bag10', 'shoppingBag', pos=[0.9, 0, 0.9])],
        cams=[FC(0.0, [2.4, 1.95, 0.35], [[0.0, CEIL, 0.0], [0.0, 1.0, 0.0], [P1[0], 2.25, P1[2]], [P2[0], 2.25, P2[2]], [0.0, 0.2, 0.0]], top=0.06, bottom=0.76, lenses=range(30, 57),
                 inside=INSIDE, drift=(-0.15, 0.0, 0.0))])
        # low, inside the carriage: from his feet to the plunger on the roof, the two passengers holding his hands

# 11: as a handle. The brake: everybody swings forward, his body further than anyone's, then back
D11 = st.dur('S11'); BR11 = 0.2
SWG = lambda a: {'lay': [0.0, r(a)]}
st.shot('S11', 'whiteVoid', setOpts={'color': '#2A2E33'}, look=LOOKI, actors=[
        act('mec', [0.0, 0, 0.0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**PIN(HANG10), **UPF, **ARMS10, 'face': {'lid': 0.45, 'gy': 0.5}}, toonDur=0.0),
            k(BR11, toon={**PIN(HANG10), **UPF, **ARMS10, **SWG(-0.55), 'sq': [0.94, 1.08, 0.94], 'face': {'lid': 0.45, 'gy': 0.5}}, toonDur=0.14, toonEase='out'),
            k(round(BR11 + 0.3, 3), toon={**PIN(HANG10), **UPF, **ARMS10, **SWG(0.3), 'face': {'lid': 0.45}}, toonDur=0.2, toonEase='inOut'),
            k(round(BR11 + 0.55, 3), toon={**PIN(HANG10), **UPF, **ARMS10, **SWG(-0.12), 'face': {'lid': 0.45}}, toonDur=0.18, toonEase='inOut')]),
        act('p1', P1, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD(-0.42), 'face': {'lid': 0.5}}, toonDur=0.0),
            k(BR11, toon={**HOLD(-0.42), 'lay': [0.0, -0.22], 'face': {'lid': 0.5, 'brow': 0.6}}, toonDur=0.16, toonEase='out'), k(round(BR11 + 0.35, 3), toon={**HOLD(-0.42), 'lay': [0.0, 0.08], 'face': {'lid': 0.5}}, toonDur=0.2)]),
        act('p2', P2, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.9, -1.0]), k(0.0, toon={**HOLD(0.42), 'face': {'lid': 0.5}}, toonDur=0.0),
            k(BR11, toon={**HOLD(0.42), 'lay': [0.0, 0.22], 'face': {'lid': 0.5, 'brow': 0.6}}, toonDur=0.16, toonEase='out'), k(round(BR11 + 0.35, 3), toon={**HOLD(0.42), 'lay': [0.0, -0.08], 'face': {'lid': 0.5}}, toonDur=0.2)])],
        props=[METRO('S11', sway=[0.02, 14]), HORNP('pl11')],
        fx=[{'type': 'shake', 'at': BR11, 'dur': 0.2, 'amount': 0.012}],
        cams=[FC(0.0, [2.7, 1.9, 0.3], [[0.0, CEIL, 0.0], [0.0, 0.3, 0.0], [P1[0], 2.25, P1[2]], [P2[0], 2.25, P2[2]]], top=0.06, bottom=0.76, lenses=range(30, 57), inside=INSIDE)])
st.cue('sfx:brake', 'S11', round(BR11 - 0.05, 3), 0.4)

# 12: yesterday the plunger came off. POP: he drops to the floor, a red ring on his forehead; the plunger stays up on the roof
# (pass 2) the POP on « ventouse » (it came on « hier », 0.9 s early); eight frames in the air after it, his eyes down then at us, then the drop and a
# pancake landing (POP to the floor took 0.13 s with inches to fall); the POP burst clear of the heads
D12 = st.dur('S12'); POP12 = 0.62; DROP12 = round(POP12 + 0.27, 3); LAND12 = round(DROP12 + 0.1, 3)
CEILPL = [0.0, CEIL, 0.0]; HANGY = 0.36                                 # his feet's height while he hung
UP12 = {'reach': {'L': [0.0, 2.35, -0.5, 1, 0.05], 'R': [0.0, 2.35, 0.5, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}
st.shot('S12', 'whiteVoid', setOpts={'color': '#2A2E33'}, look=LOOKI, actors=[
        act('mec', [0.0, 0, 0.0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**PIN(HANG10), **UPF, **ARMS10, 'face': {'lid': 0.45, 'gy': 0.5}}, toonDur=0.0),
            k(round(POP12 - 0.16, 3), toon={**PIN(HANG10), **UPF, **ARMS10, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.3, 'brow': 0.5, 'gy': 0.5}}, toonDur=0.08),   # a creak...
            k(POP12, to=[0.0, HANGY, 0.0], dur=0.02, glide=True, face='keep'),
            k(POP12, toon={**UP12, 'bend': {'neck': [0.25, 0, 0, 1, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'eye': 0.35, 'brow': 1.0, 'mouth': 'O', 'gy': 0.8}}, toonDur=0.06, toonEase='out'),   # ...POP: unstuck, still in the air, his eyes down...
            k(round(POP12 + 0.04, 3), look=[0.0, 0.0, 0.3]),
            k(round(POP12 + 0.17, 3), look='camera'), k(round(POP12 + 0.17, 3), toon={**UP12, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.45, 'brow': 0.6}}, toonDur=0.06),   # ...then at us, deadpan, hanging on nothing...
            k(DROP12, to=[0.0, 0.0, 0.0], dur=0.1, glide=True, ease='in', face='keep'),                                                                              # ...and down
            k(round(LAND12 - 0.02, 3), toon={'sq': [1.4, 0.55, 1.4], 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.6, 'brow': 0.4}}, toonDur=0.03, toonEase='out'),   # flat as a pancake...
            k(round(LAND12 + 0.1, 3), toon={'sq': [0.93, 1.08, 0.93], 'face': {'lid': 0.45}}, toonDur=0.06, toonEase='outBack'), k(round(LAND12 + 0.18, 3), toon={'face': {'lid': 0.45}}, toonDur=0.05)]),   # ...and back up, a red ring on his forehead
        act('p1', P1, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.0]), k(0.0, toon={**HOLD(-0.42), 'face': {'lid': 0.5}}, toonDur=0.0), k(POP12, toon={'face': {'lid': 0.2, 'brow': 0.8, 'pop': 0.4, 'popLen': 0.15}}, toonDur=0.06)]),
        act('p2', P2, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.0]), k(0.0, toon={**HOLD(0.42), 'face': {'lid': 0.5}}, toonDur=0.0), k(POP12, toon={'face': {'lid': 0.2, 'brow': 0.8}}, toonDur=0.06)])],
        props=[METRO('S12'), HORNP('pl12h', keys=[k(POP12, visible=False)]),
               P('pl12c', 'plunger', pos=CEILPL, rot=[round(PI, 4), 0, 0], opts={**PLOPTS, 'wobble': [[POP12, 0.45, 18, 3]]}, keys=[k(0.0, visible=False), k(POP12, visible=True)]),   # the plunger stays on the roof, swinging
               RING('ring12', POP12), BURST('pop12', [0.75, 2.6, 0.45], POP12, 'POP !', 0.42)],
        cams=[FC(0.0, [2.5, 1.3, 0.3], [[0.0, CEIL, 0.0], [0.0, 0.0, 0.0], [P1[0], 2.25, P1[2]], [P2[0], 2.25, P2[2]]], top=0.06, bottom=0.76, lenses=range(30, 57), inside=INSIDE)])
st.cue('pop', 'S12', POP12, 0.5); st.cue('sfx:thud', 'S12', LAND12, 0.45)

# 13: came off. Close, from below: the plunger alone on the roof, still swinging, between the two passengers' faces
# (pass 2) tight and low, the passengers closer together: the plunger a third of the frame between their faces looking up at it, swinging wide (a
# medium-wide, the cup 0.2 % of the frame, their backs to us)
D13 = st.dur('S13')
P1C = [0.12, 0, -0.32]; P2C = [-0.12, 0, 0.32]   # (check stills) closer still: their faces were cut by the edges
st.shot('S13', 'whiteVoid', setOpts={'color': '#2A2E33'}, look=LOOKI, actors=[
        act('p1', P1C, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CEIL, 0.0]), k(0.0, toon={'face': {'lid': 0.3, 'brow': 0.6}}, toonDur=0.0)]),
        act('p2', P2C, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CEIL, 0.0]), k(0.0, toon={'face': {'lid': 0.3, 'brow': 0.6}}, toonDur=0.0), k(0.4, toon={'face': {'lid': 1.0, 'brow': 0.6}}, toonDur=0.05), k(0.5, toon={'face': {'lid': 0.3, 'brow': 0.6}}, toonDur=0.08)])],
        props=[METRO('S13'), P('pl13', 'plunger', pos=CEILPL, rot=[round(PI, 4), 0, 0], opts={**PLOPTS, 'wobble': [[-0.25, 0.5, 14, 2.5]]})],
        cams=[FC(0.0, [1.7, 1.35, 0.0], [[0.0, CEIL, 0.0], [0.0, r(CEIL - PLEN - 0.05), 0.0], [P1C[0], 1.95, r(P1C[2] - 0.18)], [P2C[0], 1.95, r(P2C[2] + 0.18)], [P1C[0], 1.5, P1C[2]], [P2C[0], 1.5, P2C[2]]], top=0.08, bottom=0.62, lenses=range(30, 57), inside=INSIDE)])

# 14: the metro kept it. A passenger holds the plunger like a strap, swaying with the train, reading; the man is gone
# (pass 2) her hand on the knob, above her head, her face clear (the stick ran down across her face, her hand at her forehead: the plunger stuck to
# her); a newspaper in her other hand
D14 = st.dur('S14')
GRIPC = [0.0, r(CEIL - PLEN + 0.04), 0.0]; P14 = [0.05, 0, -0.42]; NEWS14 = [0.3, 1.32, -0.2]
st.shot('S14', 'whiteVoid', setOpts={'color': '#2A2E33'}, look=LOOKI, actors=[
        act('p1', P14, 0, 'stand', 'neutral', keys=[k(0.0, look=NEWS14), k(0.0, toon={'reach': {'R': [*GRIPC, 1, 0.05], 'L': [*NEWS14, 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': [*GRIPC, 1, 0.05], 'L': [*NEWS14, 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'lay': [0.0, 0.06], 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.35, toonEase='inOut'),
            k(0.8, toon={'reach': {'R': [*GRIPC, 1, 0.05], 'L': [*NEWS14, 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'lay': [0.0, -0.04], 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.35, toonEase='inOut')]),
        act('p2', [0.0, 0, 0.85], 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, 0.0]), k(0.0, toon={'face': {'lid': 0.5}}, toonDur=0.0), k(0.7, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(0.8, toon={'face': {'lid': 0.5}}, toonDur=0.08)])],
        props=[METRO('S14', sway=[0.01, 6]), P('pl14', 'plunger', pos=CEILPL, rot=[round(PI, 4), 0, 0], opts={**PLOPTS, 'wobble': [[0.3, 0.06, 6, 0.5]]}),
               P('news14', 'newspaper', on={'actor': 'p1', 'hand': 'L', 'offset': [0.0, 0.0, 0.0]}, rot=[round(PI / 2, 4), 0, 0], scale=0.9)],
        cams=[FC(0.0, [2.3, 1.4, 0.6], [[0.0, CEIL, 0.0], [P14[0], 0.3, P14[2]], [P14[0], 2.0, P14[2]], [0.0, 2.25, 0.85]], top=0.06, bottom=0.76, lenses=range(30, 57), inside=INSIDE, drift=(-0.12, 0.0, 0.0))])

# 15: he is out of work. The platform: he sits on the bench, the red ring on his forehead, deadpan; behind him the train pulls out
# (pass 2) an island platform: he sits at its edge with his back to the track, facing us, his hands on his knees and his shoulders slumped; behind him
# the train, stopped, pulls out and leaves the far platform's tiled wall and its sign; a slow push in to a medium shot (a train wiping across the lens,
# a locked wide, his face 60 px across, his arms crossed in an X); the platform and the train above the void's floor (the floor strobed navy and beige)
D15 = st.dur('S15'); SEAT15 = [0.0, 0, -0.8]; TRAIN15 = 1.7
KNEES = {'reach': {'L': [-0.15, 0.58, -1.25, 1, 0.05], 'R': [0.15, 0.58, -1.25, 1, 0.05]}, 'hands': {'L': 'rest', 'R': 'rest'}, 'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [-0.18, 0, 0, 1, None]}}
st.shot('S15', 'whiteVoid', setOpts={'color': '#2A2E33'}, look=LOOKI, actors=[
        act('mec', SEAT15, 180, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**KNEES, 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.9, toon={**KNEES, 'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.45}}, toonDur=0.4, toonEase='inOut'),
            k(1.7, toon={**KNEES, 'face': {'lid': 1.0}}, toonDur=0.07),
            k(1.85, toon={**KNEES, 'face': {'lid': 0.45}}, toonDur=0.12),
            k(2.6, toon={**KNEES, 'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.45, 'gx': 0.4}}, toonDur=0.4, toonEase='inOut')])],
        props=[P('plat15', 'metroPlatform', pos=[0.0, 0, 0.0], opts={'len': 16.0, 'depth': 4.0, 'name': 'RUE DES ARTS', 'benchX': 0.0, 'benchZ': 3.2, 'benchFlip': True}),
               P('plat15b', 'metroPlatform', pos=[0.0, 0, 3.4], ry=180, opts={'len': 16.0, 'depth': 4.0, 'name': 'RUE DES ARTS', 'bench': False, 'signX': -1.35, 'signY': 1.9}),   # the far platform across the track
               RING('ring15', 0.0),
               P('car15', 'metroCar', pos=[0.0, 0.05, TRAIN15], opts={'len': 12.0, 'glass': '#7FA2B8'}, keys=[k(0.35, to=[15.0, 0.05, TRAIN15], dur=2.7, ease='in')])],   # it pulls out behind him
        cams=[FC(0.0, [0.3, 1.2, -3.55], [[SEAT15[0], 1.8, SEAT15[2]], [SEAT15[0], 0.25, SEAT15[2]], [-0.75, 1.0, SEAT15[2]], [0.75, 1.0, SEAT15[2]]], top=0.24, bottom=0.74, lenses=range(30, 57), drift=(0.0, 0.08, 0.8))])
st.cue('whoosh', 'S15', 0.5, 0.35, 2.4, 200, 900)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.9, 'mec', 'stuck'), ('S02', round(HIT2 + 0.05, 3), 'mec', 'horn'), ('S03', 0.65, 'mec', 'gum_neck'), ('S04', 0.8, 'mec', 'counter'), ('S05', round(FL5 + 0.1, 3), 'mec', 'shiver'),
           ('S06', KN6[0], 'mec', 'toc'), ('S07', 0.3, 'plombier', 'own_forehead'), ('S08', round(HIT8 + 0.2, 3), 'mec', 'lamp_post'), ('S09', 0.6, 'mec', 'flag'),
           ('S10', 0.5, 'mec', 'handle'), ('S11', round(BR11 + 0.15, 3), 'mec', 'brake'), ('S12', round(POP12 + 0.12, 3), 'mec', 'hang'), ('S15', 2.0, 'mec', 'out_of_work')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S04', 0.3, 'pl4', 'plunger'), ('S15', 3.0, 'plat15b', 'station')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S05', 'PLOMBERIE')
st.card('S15', 'CHÔMAGE')

st.write("La ventouse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'guichet': {'preset': 'madame', 'seed': 551, 'suit': '#8E2A3A', 'hair': 'bun', 'hairColor': '#B8B8B8', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'plombier': {'preset': 'worker', 'seed': 552, 'suit': '#2F5C9E', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'p1': {'preset': 'madame', 'seed': 553, 'suit': '#C8643A', 'hairColor': '#6B3A1E', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'p2': {'preset': 'boss', 'seed': 554, 'suit': '#6B4E8A', 'build': {'width': 0.95, 'headWidth': 1.2}},
})
