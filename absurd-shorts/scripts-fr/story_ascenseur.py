#!/usr/bin/env python3
"""L'ascenseur (story 76, cycle 38; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man called the lift twenty years ago. The lift never came. So he waited. The neighbours bring him food. The concierge put an armchair there for
him. The residents' association voted for works. The works lasted fifteen years. He grew old in front of the button. The button is a listed monument.
Schools come to visit it. Yesterday the doors opened. Inside there was a man. He had been waiting twenty years for the ground floor. They shook hands.
And they took the stairs.
Staging: a building hall with lift doors, a floor display, a call button; he presses it and turns to us beside the doors, a 2006 calendar on the wall;
the display counts down to 1 and climbs again, never RC; a time-lapse with days and nights flickering and his beard growing; a neighbour's soup and
baguette; the concierge pushes in an armchair, he drops into it in a puff of dust; a residents' meeting with raised hands, his too; a jackhammer that
shakes him and his chair while he stares on; calendar pages flying; old, white-bearded, glasses, cobwebs; the button under a spotlight with a bronze
plaque and a velvet rope; a class of children, his walking stick swats a kid's hand away from it; RC lights up with a ding, the doors slide open and
their light falls across the hall, on an identical old man in an identical armchair, cobwebs and all, his finger on the RC button inside; a
handshake for the photographer; both climb the stairs while the doors close, and turn round to us.
Natural look; cycle 38: props_ascenseur.js (armchair, jackhammer, cobweb, liftPanel, lightCone, callButton; pass 3: tileFloor, doorGlow, cane,
yearCalendar, workDust, stairDoor)."""
from story_kit import *
import math

st = Story('ascenseur', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L05', 4),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L07', 4), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L09', 4), ('S14', 'L10', 0),
         ('S15', 'L11', 0), ('S16', 'L11', 3), ('S17', 'L12', 0), ('S18', 'L13', 0), ('S19', 'L13', 4), ('S20', 'L14', 0), ('S21', 'L15', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
GX = -0.8                                         # (pass 3) his pupils pinned on the lift doors, to his right when he faces us: he never takes his eyes off them
DEAD = {'lid': 0.45, 'gx': GX}
OLD = {'lid': 0.55, 'gx': GX}
OLDF = {'lid': 0.55}                              # the old face with free eyes (the double; the hero once the lift is there)
BACK = -3.0; ZF = BACK + 0.06                     # the hall's back wall and the lift doors' plane
ROOM = (-3.3, 3.3, 0.3, 3.4, BACK + 0.3, 6.0)     # where a camera may stand
BTN = [0.83, 1.12, BACK + 0.07]                   # the call button (our big one, over the set's)
DISP = [0.0, 2.4, ZF]                             # the floor display above the doors
ME = [1.42, 0, -2.42]                             # where he waits, beside the button, facing us
CH = [1.45, 0, -2.5]; SITP = [1.45, 0, -2.42]     # the armchair and where he sits in it
CAL = [-1.15, 1.62, BACK + 0.02]; CLK = [-1.15, 2.6, BACK + 0.04]
HALL = lambda **kw: {'notice': 'SYNDIC', 'car': True, **kw}   # (pass 2) a lit car behind the doors (the doorway showed the hall's own wall)
FLOOR = lambda pid: P(pid, 'tileFloor', pos=[0, 0, BACK])     # (pass 3) terracotta tiles over the set's near-white floor (the captions sat on white)
DIM = {'fill': 0.45, 'sun': 0.4, 'probe': 0.85, 'autoExposure': False}   # (pass 3) the hall once the lift is there: darker, so the car is the light
GLOW = lambda pid, doors, **kw: P(pid, 'doorGlow', pos=[0, 0, BACK], opts={'doors': doors, **kw})   # (pass 3) the car's light across the hall floor and on whoever is near
BUTTON = lambda pid, **kw: P(pid, 'callButton', pos=BTN, opts=kw)
CHAIR = lambda pid, **kw: P(pid, 'armchair', pos=CH, opts={'color': '#B5523A', **kw})
BEARD = lambda pid, who='mec', s=1.2, color='#E4E0D8', keys=None, swing=None: P(pid, 'beardHair', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.02, 0.1], 'hang': True, 'hangYaw': 0.4}, scale=s,   # (pass 3) hang: it hangs by gravity from the chin (nailed to the head it swung into the chest when the head turned)
                                                       opts={'len': 0.95, 'coil': 0.0, 'color': color, 'depth': 0.12, 'w': 0.26, **({'swing': swing, 'whip': True} if swing else {})}, **({'keys': keys} if keys else {}))
SPECS = lambda pid, who='mec', keys=None: P(pid, 'glasses', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.23, 0.106]}, opts={'r': 0.042, 'dx': 0.055}, **({'keys': keys} if keys else {}))   # (pass 2) at eye level (they sat at the jaw); (pass 3) on the face (z 0.16 floated 6 cm in front of it: seen in profile they hung in the air)
PLAID = '#2E7D5B'   # (pass 2) a green blanket against the red armchair (it was lost under the dust)
STICK = lambda pid, who='mec', hand='R': P(pid, 'slab', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.45, 0.04]}, opts={'w': 0.03, 'h': 0.95, 'd': 0.03, 'color': '#6B4A2E'})
WEBS = lambda pfx: [P(f'{pfx}a', 'cobweb', pos=[CH[0] + 0.43, 1.25, CH[2] - 0.3], ry=-90, opts={'s': 0.42}), P(f'{pfx}b', 'cobweb', pos=[0.55, 2.1, ZF + 0.02], opts={'s': 0.38})]
WEB = lambda pid, who='vieux': P(pid, 'cobweb', on={'actor': who, 'joint': 'head', 'offset': [0.125, 0.0, -0.01], 'hang': True, 'hangYaw': 1.0, 'rot': [0.0, 0.0, r(PI / 2)]}, opts={'s': 0.34})   # (pass 3) a web in the corner between his head and his shoulder (no web showed in the old-age shots)
SIT = lambda pid, t0=0.0: k(t0, clip='sit')

for g_ in [('S03', 1.2, 'mec', 'display'), ('S07', 0.25, 'mec', 'chair'), ('S14', 0.95, 'eleve1', 'stick'), ('S16', 0.5, 'vieux', 'doors'), ('S17', 0.6, 'autre', 'twin'), ('S21', 1.5, 'vieux', 'stairs')]:
    st.gag(*g_)
st.card('S08', 'VOTÉ', at=0.8)
st.card('S12', 'MONUMENT HISTORIQUE', at=0.35)

# 1: the hook. Close on the call button: his finger presses it, the ring lights up and breathes; the hand leaves the frame
D1 = st.dur('S01')
st.shot('S01', 'immeubleHall', setOpts=HALL(), actors=[act('mec', [1.3, 0, -2.38], 200, 'stand', 'neutral', keys=[k(0.0, look=BTN),
            k(0.1, toon={'reach': {'L': [BTN[0] + 0.01, BTN[1] + 0.01, BTN[2] + 0.05, 1, 0.04]}, 'hands': {'L': 'point'}}, toonDur=0.25, toonEase='out'),
            k(0.4, toon={'reach': {'L': [BTN[0], BTN[1] + 0.01, BTN[2] + 0.025, 1, 0.04]}, 'hands': {'L': 'point'}}, toonDur=0.06), k(0.7, toon={'reach': {'L': [1.12, 1.2, -2.5, 1, 0.04]}, 'hands': {'L': 'point'}}, toonDur=0.2),
            k(0.92, toon={'hands': {'L': 'open'}}, toonDur=0.25)])],   # (pass 3) the arm drops out of the frame (a fingertip stayed stuck at its edge for the last half second)
        props=[FLOOR('sol1'), BUTTON('bt1', pressAt=0.4)],
        cams=[FC(0.0, [0.3, 1.2, -2.3], [[BTN[0], 1.24, BTN[2]], [BTN[0], 1.0, BTN[2]], [BTN[0] - 0.12, 1.12, BTN[2]], [BTN[0] + 0.25, 1.12, BTN[2] + 0.2]], top=0.3, bottom=0.66, lenses=range(16, 50), drift=(0.03, 0.0, -0.05))])   # (stills 1) beside the button, left of his reach: from behind his shoulder his arm blacked out the frame
st.cue('sfx:beep', 'S01', 0.4, 0.3)

# 2: ...twenty years ago. Wide on the hall: he waits beside the doors, hands behind his back, his eyes on them; a 2006 calendar on the wall
D2 = st.dur('S02'); BEHIND = {'touch': {'R': ['torso', 0.1, 0.25, -0.2, 1, 0.02], 'L': ['torso', -0.1, 0.25, -0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'gx': GX}}
st.shot('S02', 'immeubleHall', setOpts=HALL(floor=[[0.0, '7']]), actors=[act('mec', ME, 0, 'stand', 'neutral', darts=0, keys=[k(0.0, look='camera'),
            k(0.0, toon=BEHIND, toonDur=0.0), k(0.5, toon={**BEHIND, 'sq': [1.0, 1.03, 1.0]}, toonDur=0.25, toonEase='inOut'),   # up on his toes and down again: waiting
            k(0.8, toon={**BEHIND, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.25, toonEase='inOut')])],
        props=[FLOOR('sol2'), BUTTON('bt2', litAfter=0.0), P('cal2', 'yearCalendar', pos=CAL, scale=1.3, opts={'months': ['2006']}), P('horloge2', 'wallClock', pos=CLK, scale=0.6, opts={'rate': 0.02})],
        cams=[FC(0.0, [0.5, 1.6, 2.4], [[ME[0], 2.45, ME[2]], [ME[0], 0.0, ME[2]], [ME[0] + 0.5, 1.2, ME[2]], [DISP[0], 2.6, DISP[2]], [CAL[0] - 0.25, 1.95, CAL[2]], [CAL[0] - 0.25, 1.3, CAL[2]]], top=0.14, bottom=0.76, drift=(0.0, 0.0, -0.3))])   # (pass 3) his whole width in the frame (the right edge cut half his face)

# 3: the lift never came. Low, looking up at the floor display: it counts down to 1... and climbs again; he rises on his toes at the 1, and is flattened
#    like a pancake when it jumps to 2
D3 = st.dur('S03'); FL3 = [[0.0, '6'], [0.13, '5'], [0.26, '4'], [0.39, '3'], [0.52, '2'], [0.65, '1'], [1.2, '2'], [1.38, '3'], [1.56, '4']]   # (pass 2) the 1 held 0.55 s
FLAT3 = {'face': {'lid': 0.7, 'mouth': 'line', 'brow': -0.5}}
st.shot('S03', 'immeubleHall', setOpts=HALL(floor=FL3), actors=[act('mec', ME, -20, 'stand', 'neutral', keys=[k(0.0, look=DISP),
            k(0.68, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'smile', 'brow': 0.9}, 'sq': [0.94, 1.08, 0.94]}, toonDur=0.1, toonEase='out'),   # (pass 2) up on his toes at the 1...
            k(1.2, toon={**FLAT3, 'sq': [1.26, 0.66, 1.26]}, toonDur=0.05, toonEase='in'), k(1.26, toon={**FLAT3, 'sq': [1.3, 0.62, 1.3]}, toonDur=0.2),   # (pass 3) ...a pancake when it jumps to 2, held a third of a second (it lasted one frame)...
            k(1.5, toon={**FLAT3, 'sq': [0.94, 1.08, 0.94]}, toonDur=0.07, toonEase='out'), k(1.6, toon={**FLAT3, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.12)])],   # ...then he pops back, overshoots and sags
        props=[FLOOR('sol3'), BUTTON('bt3', litAfter=0.0)],
        cams=[FC(0.0, [0.2, 1.3, -1.2], [[DISP[0], 2.58, DISP[2]], [DISP[0], 2.22, DISP[2]], [r(DISP[0] - 0.3), 2.4, DISP[2]], [ME[0], 2.4, ME[2]], [ME[0], 1.3, ME[2]], [r(ME[0] + 0.2), 1.7, ME[2]]], top=0.14, bottom=0.74, lenses=range(24, 66))])   # (pass 2) the display inside the frame; (pass 3) room for the pancake and for his whole face
for t_ in [0.13, 0.26, 0.39, 0.52, 0.65, 1.2, 1.38, 1.56]: st.cue('sfx:tick', 'S03', t_, 0.12)
st.cue('sfx:poof', 'S03', 1.2, 0.3)

# 4: so he waited. Time-lapse: days and nights flicker over the hall, the floors spin on the display, his beard grows from nothing to his chest and
#    he sags lower and lower
D4 = st.dur('S04')
st.shot('S04', 'immeubleHall', setOpts=HALL(floor=[[r(0.13 * j), str(v)] for j, v in enumerate([4, 9, 2, 6, 3, 8, 1, 7, 5, 9, 2, 6, 3])]),
        dark=[[0.0, 0.0], *[[r(0.15 + 0.26 * j), 0.62 if j % 2 == 0 else 0.0, 0.11] for j in range(6)]], darkFloor=0.55, darkTint='#9DB2F2',   # (pass 3) night, day, night, day: the time-lapse (small clock hands alone said it)
        actors=[act('mec', ME, 0, 'stand', 'neutral', darts=0, darkEyes=False, keys=[k(0.0, look='camera'),
            k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0), k(0.15, toon={'face': {'lid': 0.55, 'gx': GX, 'mouth': 'line'}, 'sq': [1.04, 0.94, 1.04]}, toonDur=0.5, toonEase='inOut'),
            k(0.7, toon={'face': {'lid': 0.7, 'gx': GX, 'mouth': 'line'}, 'sq': [1.1, 0.85, 1.1]}, toonDur=0.5, toonEase='inOut'),   # (pass 3) a real slump: a fifth shorter by the end
            k(1.25, toon={'face': {'lid': 0.85, 'gx': GX, 'mouth': 'line'}, 'sq': [1.16, 0.77, 1.16]}, toonDur=0.35, toonEase='inOut')])],
        props=[FLOOR('sol4'), BUTTON('bt4', litAfter=0.0), BEARD('barbe4', s=0.05, color='#5A4636', keys=[k(0.0, scale=0.05), k(0.05, scale=1.1, dur=1.45, ease='linear')])],
        cams=[FC(0.0, [-0.5, 1.4, 0.5], [[ME[0], 2.05, ME[2]], [r(ME[0] + 0.45), 1.0, ME[2]], [ME[0], 0.2, ME[2]], [r(DISP[0] - 0.3), 2.56, DISP[2]]], top=0.12, bottom=0.76, drift=(0.1, 0.0, -0.2))])   # (pass 3) him and the display (he was a quarter of the frame at its edge)
st.cue('sfx:ticks', 'S04', 0.0, 1.6)

# 5: the neighbours bring him food. A grandmother from upstairs comes in with a bowl of soup and a baguette and puts them in his hands; he takes
#    them without taking his eyes off the doors
D5 = st.dur('S05'); MAM = [0.72, 0, -2.0]; GIVE = 0.8; CARRY = {'touch': {'R': ['torso', 0.16, 0.2, 0.3, 1, 0.02], 'L': ['torso', -0.16, 0.26, 0.3, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
st.shot('S05', 'immeubleHall', setOpts=HALL(floor=[[0.0, '3']]), actors=[act('mec', ME, 0, 'stand', 'neutral', darts=0, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(r(GIVE - 0.18), toon={'reach': {'R': [1.12, 1.22, -2.12, 1, 0.04], 'L': [1.52, 1.3, -2.1, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.18, toonEase='out'),
            k(r(GIVE + 0.2), toon={'reach': {'R': [1.2, 1.16, -2.1, 1, 0.04], 'L': [1.6, 1.32, -2.12, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {**DEAD, 'mouth': 'line'}, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.15),   # the weight of the bowl
            k(r(GIVE + 0.45), toon={'face': {'lid': 1.0, 'gx': GX, 'mouth': 'line'}}, keepPose=True, toonDur=0.07), k(r(GIVE + 0.57), toon={'face': {**DEAD, 'mouth': 'line'}}, keepPose=True, toonDur=0.08)]),
        act('mamie', [-0.25, 0, -1.4], 110, 'walk', 'happy', keys=[k(0.0, to=MAM, dur=0.55, clip='walk', then='stand', ease='out', face='keep'), k(0.45, face=60, turn=0.2), k(0.0, look=[ME[0], 1.7, ME[2]]),
            k(0.0, toon=CARRY, toonDur=0.0), k(r(GIVE - 0.25), toon={'reach': {'R': [1.0, 1.22, -2.1, 1, 0.04], 'L': [1.08, 1.4, -2.18, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.2, toonEase='out'),
            k(r(GIVE + 0.12), toon={'hands': {'R': 'open', 'L': 'open'}}, toonDur=0.25), k(r(GIVE + 0.3), look='camera', lookDur=0.2)])],   # (pass 3) she ends three-quarters to us beside him (she had her back to us)
        props=[FLOOR('sol5'), BUTTON('bt5', litAfter=0.0), BEARD('barbe5', s=0.75, color='#5A4636'),
               P('soupe5', 'soupBowl', on={'actor': 'mamie', 'hand': 'R', 'offset': [0.0, 0.04, 0.05], 'hang': True, 'hangYaw': 1.0}, scale=1.9, keys=[k(GIVE, attach='mec', hand='R', offset=[0.0, 0.04, 0.06], hang=True, hangYaw=1.0)]),   # (pass 3) the hand-over as a flat key (given as a dictionary it was not read: bowl and baguette fell to the floor, into the caption band); hang: the bowl stays level
               P('pain5', 'baguette', on={'actor': 'mamie', 'hand': 'L', 'offset': [0.0, 0.0, 0.04], 'hang': True, 'hangYaw': 1.0, 'rot': [0.0, 0.0, 1.15]}, scale=1.5, keys=[k(GIVE, attach='mec', hand='L', offset=[0.0, 0.0, 0.04], hang=True, hangYaw=1.0, rot=[0.0, 0.0, 1.15])])],
        cams=[FC(0.0, [0.45, 1.3, 0.9], [[ME[0], 2.02, ME[2]], [r(ME[0] + 0.45), 1.0, ME[2]], [r(MAM[0] - 0.3), 1.78, MAM[2]], [r(MAM[0] - 0.42), 0.72, MAM[2]], [1.2, 0.68, -2.1]], top=0.14, bottom=0.74, drift=(0.05, 0.0, -0.12))])   # (pass 3) low and close, from the knees up: nothing in the caption band
st.cue('sfx:stepSoft', 'S05', 0.15, 0.15); st.cue('sfx:stepSoft', 'S05', 0.4, 0.15)

# 6: the concierge put an armchair there... She pushes a big old armchair along the wall, past the lift doors, toward him, cheerful; he does not look
D6 = st.dur('S06'); CON0, CON1 = [-1.3, 0, -1.9], [0.05, 0, -1.98]
st.shot('S06', 'immeubleHall', setOpts=HALL(floor=[[0.0, '8']]), actors=[act('mec', ME, 0, 'stand', 'neutral', darts=0, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.5, toon={'face': {'lid': 1.0, 'gx': GX, 'mouth': 'line'}}, toonDur=0.07), k(0.62, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08)]),
        act('concierge', CON0, 95, 'pushCart', 'happy', keys=[k(0.0, to=CON1, dur=D6, clip='pushCart', ease='linear', face='keep'), k(0.0, look=[ME[0], 1.8, ME[2]]), k(0.55, look='camera', lookDur=0.2)])],
        props=[FLOOR('sol6'), BUTTON('bt6', litAfter=0.0), BEARD('barbe6', s=0.85, color='#6E6052'),
               P('fauteuil6', 'armchair', pos=[-0.6, 0, -1.95], ry=20, keys=[k(0.0, to=[0.78, 0, -2.05], dur=D6, ease='linear')], opts={'color': '#B5523A'})],
        cams=[FC(0.0, [2.7, 1.25, -0.2], [[ME[0], 2.02, ME[2]], [r(ME[0] + 0.42), 0.9, ME[2]], [-0.3, 1.85, -1.95], [0.78, 0.3, -1.65]], top=0.14, bottom=0.76, lenses=range(26, 62), drift=(-0.1, 0.0, -0.1), inside=ROOM)])   # (pass 3) from his side, low: he is big at the right, she comes toward us pushing (they were a third of the frame)
st.cue('sfx:rattle', 'S06', 0.0, 1.0)

# 7: ...an armchair. He drops into it: the cushion squashes and springs back in a puff of dust; she tucks a blanket over his knees
D7 = st.dur('S07'); SINK = 0.2
st.shot('S07', 'immeubleHall', setOpts=HALL(floor=[[0.0, '8']]), actors=[act('mec', [SITP[0], 0.6, SITP[2]], 0, 'sit', 'neutral', keys=[k(0.0, to=SITP, dur=SINK, ease='in', clip='sit', face='keep', glide=True), k(0.0, look='camera'),
            k(0.0, toon={'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.3, 'mouth': 'O'}}, toonDur=0.0),   # (pass 2) stretched as he drops from higher...
            k(SINK, toon={'sq': [1.18, 0.78, 1.18], 'face': {'lid': 0.8, 'mouth': 'O'}}, toonDur=0.04, toonEase='out'), k(r(SINK + 0.12), toon={'sq': [0.94, 1.07, 0.94], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08),   # ...squashed three frames, overshoot
            k(r(SINK + 0.3), toon={'sq': [1.0, 1.0, 1.0], 'face': {**DEAD, 'mouth': 'smile'}}, toonDur=0.15)]),
        act('concierge', [0.55, 0, -1.65], 60, 'stand', 'happy', keys=[k(0.0, look=[SITP[0], 1.0, SITP[2]]), k(0.45, toon={'reach': {'R': [1.25, 0.95, -2.05, 1, 0.04], 'L': [1.15, 0.95, -2.2, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.25)])],
        props=[FLOOR('sol7'), BUTTON('bt7', litAfter=0.0), CHAIR('fauteuil7', sinkAt=SINK), BEARD('barbe7', s=0.85, color='#6E6052'),
               P('poussiere7', 'dustPuff', pos=[SITP[0], 0.45, SITP[2] + 0.2], scale=1.05, opts={'once': True, 'startAt': SINK, 'period': 0.7, 'color': '#E8E0D0'}),
               P('plaid7', 'blanketDrape', pos=[SITP[0], 0.72, SITP[2] + 0.38], opts={'w': 0.75, 'h': 0.42, 'color': PLAID}, keys=[k(0.0, visible=False), k(0.75, visible=True)])],
        cams=[FC(0.0, [1.0, 1.25, 0.6], [[SITP[0], 2.1, SITP[2]], [SITP[0], 0.0, SITP[2] + 0.4], [0.55, 2.3, -1.65], [0.55, 0.0, -1.65], [CH[0] - 0.45, 1.2, CH[2]], [CH[0] + 0.48, 1.0, CH[2]]], top=0.16, bottom=0.74)])
st.cue('thud', 'S07', SINK, 0.4); st.cue('sfx:poof', 'S07', SINK, 0.4)

# 8: the residents' association voted for works. A meeting in the hall: the chairman bangs his gavel at a folding table, three residents raise their
#    hands, and so does he, from his armchair, his arm twice as long as theirs (VOTÉ)
D8 = st.dur('S08'); BANG8 = 0.75; SYN = [-0.42, 0, -2.78]; TAB = [-0.4, 0, -2.35]   # (pass 3) the chairman at his table in front of the lift doors, facing us
RES8 = [('voisin1', -0.04, -1.95, -60), ('voisin2', 0.34, -1.5, -60), ('voisin3', 0.58, -1.98, -62)]   # (pass 3) the three residents in a tight group between him and the armchair, three-quarters to us (two had their backs to us and one hid behind another)
UP8 = {'reach': {'R': [1.6, 2.7, -2.2, 1, 0.04]}, 'hands': {'R': 'open'}}
st.shot('S08', 'immeubleHall', setOpts=HALL(floor=[[0.0, '5']]), actors=[act('mec', SITP, 0, 'sit', 'neutral', darts=0, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.3, toon={**UP8, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2, toonEase='out'),
            k(1.3, toon={**UP8, 'face': {'lid': 1.0, 'gx': GX, 'mouth': 'line'}}, toonDur=0.08), k(1.42, toon={**UP8, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12)]),
        act('syndic', SYN, 20, 'stand', 'neutral', keys=[k(0.0, look=[0.5, 1.6, -1.0]), k(0.0, toon={'reach': {'R': [-0.68, 1.62, -2.38, 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(r(BANG8 - 0.14), toon={'reach': {'R': [-0.68, 1.8, -2.44, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.12),   # the gavel goes up a little first
            k(BANG8, toon={'reach': {'R': [-0.68, 0.86, -2.34, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.05, toonEase='in'),
            k(r(BANG8 + 0.15), toon={'reach': {'R': [-0.68, 0.98, -2.34, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15)]),
        *[act(rid, [rx, 0, rz], rry, 'stand', 'neutral', keys=[k(0.0, look=[SYN[0], 1.8, SYN[2]]),
            k(r(0.15 + 0.08 * j), toon={'reach': {'R': [r(rx - 0.1), r(2.55 + 0.08 * j), r(rz - 0.08), 1, 0.04]}, 'hands': {'R': 'open'}}, toonDur=0.2, toonEase='out'),
            k(r(0.9 + 0.2 * j), toon={'reach': {'R': [r(rx - 0.1), r(2.63 + 0.08 * j), r(rz - 0.08), 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0}}, toonDur=0.08),
            k(r(1.0 + 0.2 * j), toon={'reach': {'R': [r(rx - 0.1), r(2.55 + 0.08 * j), r(rz - 0.08), 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.2}}, toonDur=0.15)])
          for j, (rid, rx, rz, rry) in enumerate(RES8)]],
        props=[FLOOR('sol8'), BUTTON('bt8', litAfter=0.0), CHAIR('fauteuil8'), BEARD('barbe8', s=0.9, color='#7A6E62'), P('table8', 'desk', pos=TAB, ry=180, opts={'w': 0.9}),
               P('marteau8', 'gavel', on={'actor': 'syndic', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}),
               P('banniere8', 'signBoard', pos=[-0.2, 2.9, BACK + 0.05], opts={'text': 'ASSEMBLÉE GÉNÉRALE', 'bg': '#F3EBD6', 'fg': '#7A2A1E', 'w': 1.2, 'h': 0.26, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [0.65, 1.4, 2.2], [[1.62, 2.78, -2.2], [1.95, 0.7, CH[2]], [r(SYN[0] - 0.42), 1.3, SYN[2]], [r(TAB[0] - 0.5), 0.5, TAB[2]], [-0.8, 3.04, BACK], [0.34, 0.3, -1.5]], top=0.1, bottom=0.76, lenses=range(26, 61))])   # (pass 3) lower and closer: a frame 2.8 m wide instead of 4, his whole armchair in it, nobody in front of him
st.cue('sfx:gavel', 'S08', BANG8, 0.4)

# 9: the works lasted... A worker drills the floor in front of the lift with a jackhammer: the worker, the armchair, his beard and the camera all
#    shake; he hops in his chair with every blow and stares at the doors, greying
D9 = st.dur('S09'); OUV = [0.42, 0, -1.95]; HAM = [0.5, 1.02, -1.62]; N9 = int(D9 / 0.07)
st.shot('S09', 'immeubleHall', setOpts=HALL(floor=[[0.0, '—']]), fx=[{'type': 'shake', 'at': 0.0, 'dur': r(D9 * 1.6), 'amount': 0.02}],
        actors=[act('gris', SITP, 0, 'sit', 'neutral', darts=0, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            *[k(r(0.07 * j), to=[SITP[0], 0.05 if j % 2 else 0.0, SITP[2]], dur=0.035, glide=True, face='keep') for j in range(1, N9)],   # (pass 3) he hops with the chair at every blow (they shook by two pixels)
            *[k(r(0.07 * j), toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': [0.97, 1.05, 0.97] if j % 2 else [1.04, 0.94, 1.04]}, toonDur=0.035) for j in range(1, N9)]]),
        act('ouvrier', OUV, 25, 'stand', 'determined', keys=[k(0.0, look=[HAM[0], 0.0, HAM[2]]), k(0.0, toon={'reach': {'R': [r(HAM[0] - 0.17), 1.02, HAM[2], 1, 0.04], 'L': [r(HAM[0] + 0.17), 1.02, HAM[2], 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            *[k(r(0.07 * j), toon={'reach': {'R': [r(HAM[0] - 0.17), 1.02, HAM[2], 1, 0.04], 'L': [r(HAM[0] + 0.17), 1.02, HAM[2], 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.06, 0.93, 1.06] if j % 2 else [0.96, 1.05, 0.96]}, toonDur=0.035) for j in range(1, N9)]])],
        props=[FLOOR('sol9'), BUTTON('bt9', litAfter=0.0), P('fauteuil9', 'armchair', pos=CH, opts={'color': '#B5523A'}, keys=[k(r(0.07 * j), to=[CH[0], 0.05 if j % 2 else 0.0, CH[2]], dur=0.035) for j in range(1, N9)]),
               BEARD('barbe9', who='gris', s=0.95, color='#A49C90', swing=[0.0, D9, 0.14]),   # (pass 3) the beard buzzes
               P('piqueur9', 'jackhammer', pos=HAM, opts={'from': 0.0, 'floorY': -1.0}), P('panneau9', 'signBoard', pos=[1.6, 2.3, BACK + 0.05], opts={'text': 'TRAVAUX', 'bg': '#F2C230', 'fg': '#1B1B1E', 'w': 0.95, 'h': 0.34, 'posts': False, 'height': 0}),   # (pass 3) the sign on the wall over him (on the floor at the left it spread the frame too wide)
               P('nuage9', 'workDust', pos=[HAM[0], 0.0, HAM[2]], opts={'drift': [-0.75, 0, 0.3], 's': 1.15})],   # (pass 3) opaque puffs that drift away from him (translucent boulders ghosted him out)
        cams=[FC(0.0, [0.5, 1.25, 1.1], [[SITP[0], 1.75, SITP[2]], [r(SITP[0] + 0.48), 0.9, SITP[2]], [2.05, 2.5, BACK], [r(OUV[0] - 0.35), 1.95, OUV[2]], [r(OUV[0] - 0.3), 0.25, HAM[2]]], top=0.12, bottom=0.76)])   # (pass 3) close: the worker, him and the sign fill the frame
st.cue('sfx:rattle', 'S09', 0.0, 0.9); st.cue('sfx:chainsaw', 'S09', 0.0, 0.9)

# 10: ...fifteen years. Close on the wall calendar: the years fly off page after page, 2007 to 2021, past the clock spinning above
D10 = st.dur('S10'); YEARS = [str(y) for y in range(2007, 2022)]
st.shot('S10', 'immeubleHall', setOpts=HALL(floor=[[0.0, '—']]), actors=[],
        props=[P('cal10', 'yearCalendar', pos=CAL, scale=1.3, opts={'months': YEARS, 'flipAt': 0.05, 'dur': r((D10 - 0.25) / len(YEARS))}), P('horloge10', 'wallClock', pos=CLK, scale=0.6, opts={'rate': 9.0})],   # (pass 3) pages with blank backs (the lifting pages showed their print mirrored)
        cams=[FC(0.0, [-0.85, 1.95, -1.15], [[CAL[0], 1.97, CAL[2]], [CAL[0], 1.27, CAL[2]], [CLK[0], 2.82, CLK[2]], [CLK[0] - 0.25, 2.6, CLK[2]], [CLK[0] + 0.25, 1.3, CLK[2]]], top=0.12, bottom=0.78, lenses=range(20, 56))])
st.cue('sfx:paper', 'S10', 0.05, 1.0)

# 11: he grew old in front of the button. Old now: white beard to his lap, glasses, a walking stick, cobwebs; slowly he turns his head to the button
D11 = st.dur('S11')
st.shot('S11', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), actors=[act('vieux', SITP, 0, 'sit', 'neutral', darts=0, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0),
            k(0.45, look=BTN, lookDur=0.9), k(1.2, toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.15), k(1.4, toon={'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.15)])],
        props=[FLOOR('sol11'), BUTTON('bt11', litAfter=0.0), CHAIR('fauteuil11'), BEARD('barbe11', who='vieux', s=1.25), SPECS('lun11', who='vieux'), STICK('canne11', who='vieux'), *WEBS('toile11'), WEB('toile11c'),
               P('plaid11', 'blanketDrape', pos=[SITP[0], 0.72, SITP[2] + 0.38], opts={'w': 0.75, 'h': 0.42, 'color': PLAID})],   # (pass 3) the same green blanket as when she tucked it (it was white here)
        cams=[FC(0.0, [1.15, 1.6, 0.3], [[SITP[0], 2.2, SITP[2]], [SITP[0], 0.9, SITP[2]], [BTN[0], 1.25, BTN[2]], [CH[0] + 0.45, 1.3, CH[2]]], top=0.16, bottom=0.74, drift=(0.0, 0.0, -0.25))])

# 12: the button is a listed monument. Close on it: the hall light drops, a museum spotlight snaps on over it with a flicker; a bronze plaque under
#     it, the velvet rope in front
D12 = st.dur('S12'); SPOT = 0.26
st.shot('S12', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]),
        dark=[[0.0, 0.0], [SPOT, 0.6, 0.03], [r(SPOT + 0.07), 0.2, 0.02], [r(SPOT + 0.13), 0.62, 0.03]], darkFloor=0.6, darkTint='#D9CBB6',   # (pass 3) the spotlight snaps on: the hall round it dims (the cone lifted the wall from 0.81 to 0.87 only)
        darkPool={'at': [BTN[0], 1.0, BTN[2]], 'r': 0.6, 'k': 1.0, 'tint': '#FFEBC8'},
        actors=[act('vieux', SITP, 0, 'sit', 'neutral', darkEyes=False, keys=[k(0.0, look=BTN), k(0.0, toon={'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[FLOOR('sol12'), BUTTON('bt12', litAfter=0.0), P('plaque12', 'bronzePlaque', pos=[BTN[0], 0.82, BACK + 0.04], scale=0.8, opts={'text': "BOUTON D'APPEL/2006"}),
               P('spot12', 'lightCone', pos=[BTN[0], 3.3, BACK + 0.3], opts={'h': 2.4, 'r': 0.34, 'opacity': 0.14}, keys=[k(0.0, visible=False), k(SPOT, visible=True), k(r(SPOT + 0.07), visible=False), k(r(SPOT + 0.13), visible=True)]),
               P('cordon12', 'stanchions', pos=[BTN[0], 0, BACK + 0.75], opts={'w': 1.0}), CHAIR('fauteuil12')],
        cams=[FC(0.0, [0.8, 1.75, -1.6], [[BTN[0], 1.34, BTN[2]], [BTN[0], 0.66, BTN[2]], [BTN[0] - 0.26, 1.0, BTN[2]], [BTN[0] + 0.26, 1.0, BTN[2]]], top=0.2, bottom=0.66, lenses=range(18, 50), drift=(0.0, 0.0, -0.1))])   # (stills 1) centred on the button and the plaque; (pass 3) from higher, the plaque higher in the frame: the rope falls under the caption band
st.cue('sfx:choir', 'S12', SPOT, 0.7)

# 13: ...historic. Wider: the button roped off under the spotlight like a museum piece, the hall dim round it, the old man beside it like its guard
D13 = st.dur('S13')
st.shot('S13', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), dark=[[0.0, 0.5, 0.001]], darkFloor=0.6, darkTint='#D9CBB6', darkPool={'at': [r(BTN[0] + 0.28), 1.25, BACK + 0.45], 'r': 1.3, 'k': 1.0, 'tint': '#FFEBC8'},
        actors=[act('vieux', SITP, 0, 'sit', 'neutral', darts=0, darkEyes=False, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(0.47, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.1),   # (pass 2) a slow blink...
            k(0.7, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.3), k(1.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.3), k(1.1, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.22, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.1)])],
        props=[FLOOR('sol13'), BUTTON('bt13', litAfter=0.0), P('plaque13', 'bronzePlaque', pos=[BTN[0], 0.82, BACK + 0.04], scale=0.8, opts={'text': "BOUTON D'APPEL/2006"}),
               P('spot13', 'lightCone', pos=[BTN[0], 3.3, BACK + 0.45], opts={'h': 2.3, 'r': 0.42}), P('cordon13', 'stanchions', pos=[BTN[0], 0, BACK + 0.75], opts={'w': 1.0}),
               CHAIR('fauteuil13'), BEARD('barbe13', who='vieux', s=1.25), SPECS('lun13', who='vieux'), STICK('canne13', who='vieux'), *WEBS('toile13'), WEB('toile13c')],
        cams=[FC(0.0, [-0.3, 1.8, 1.6], [[SITP[0], 2.2, SITP[2]], [BTN[0], 3.3, BACK + 0.45], [BTN[0] - 0.5, 0.0, BACK + 0.75], [CH[0] + 0.45, 0.0, CH[2]], [DISP[0], 2.6, DISP[2]]], top=0.12, bottom=0.78)])

# 14: schools come to visit it. A teacher shows the button to a class; one child stretches a long arm over the rope to press it; the old man's walking
#     stick comes down on his hand
D14 = st.dur('S14'); TAP = 0.95
SIT14 = [1.62, 0, -2.42]; CH14 = [1.62, 0, -2.5]     # his armchair a hand's width further from the button in this shot: his arm clear of the button and its plaque
HANDP = [1.27, 0.73, -2.1]                          # his hand on the arm of the chair: the stick turns about it
KHAND = [0.7, 1.1, -2.3]                            # the child's hand, over the rope, on its way to the button
_dx, _dy, _dz = KHAND[0] - HANDP[0], KHAND[1] - HANDP[1], KHAND[2] - HANDP[2]
CRY = r(math.degrees(math.atan2(_dx, _dz)), 1); A1 = r(math.atan2(math.hypot(_dx, _dz), _dy))   # where the stick points when it lands, and how far it comes down
K1 = [0.3, 0, -2.3]; TEA = [0.1, 0, -2.86]
KREACH = lambda p, hand='point': {'reach': {'L': [*p, 1, 0.04]}, 'hands': {'L': hand}}
SHOCK = {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}
st.shot('S14', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), actors=[act('vieux', SIT14, 0, 'sit', 'neutral', darts=0, keys=[k(0.0, look=[0.5, 1.3, -1.0]),
            k(0.0, toon={'reach': {'R': [*HANDP, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(r(TAP - 0.2), toon={'reach': {'R': [*HANDP, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'gx': GX, 'mouth': 'line', 'brow': -0.8}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.12, toonEase='out'),   # he draws himself up, a side glance at the hand...
            k(TAP, toon={'reach': {'R': [*HANDP, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'gx': GX, 'mouth': 'line', 'brow': -0.8}, 'sq': [1.05, 0.94, 1.05]}, toonDur=0.05, toonEase='in'),   # ...and comes down with the stick
            k(r(TAP + 0.3), toon={'reach': {'R': [*HANDP, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {**OLD, 'mouth': 'line'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.2), k(r(TAP + 0.4), look='camera', lookDur=0.2)]),
        act('maitresse', TEA, 45, 'point', 'happy', keys=[k(0.0, look=[1.2, 1.2, -0.6]), k(r(TAP + 0.1), look=[K1[0], 1.0, K1[2]], lookDur=0.15), k(r(TAP + 0.12), toon={'face': {**SHOCK}}, toonDur=0.08)]),
        act('eleve1', K1, 95, 'stand', 'happy', keys=[k(0.0, look=BTN),
            k(0.2, toon=KREACH([0.5, 0.95, -2.34]), toonDur=0.3, toonEase='out'), k(0.6, toon=KREACH(KHAND), toonDur=0.28, toonEase='inOut'),   # (pass 3) a long rubber arm creeps over the rope toward the button
            k(TAP, toon={**KREACH([KHAND[0], r(KHAND[1] - 0.14), KHAND[2]], 'open'), 'sq': [1.1, 0.88, 1.1], 'face': {**SHOCK}}, toonDur=0.04, toonEase='out'),   # the hand is knocked down, he is squashed...
            k(r(TAP + 0.07), toon={**KREACH([0.44, 0.95, -2.22], 'open'), 'sq': [0.9, 1.14, 0.9], 'face': {**SHOCK}}, toonDur=0.06, toonEase='out'), k(r(TAP + 0.07), look='camera', lookDur=0.08),   # ...and jumps back, the hand snatched to his chest, his face to us
            *[k(r(TAP + 0.2 + 0.07 * i_), toon={**KREACH([r(0.5 + (0.07 if i_ % 2 else -0.05)), r(0.98 + (0.06 if i_ % 2 else 0.0)), -2.2], 'open'), 'sq': [1.0, 1.0, 1.0], 'face': {**SHOCK}}, toonDur=0.05) for i_ in range(8)]]),   # he shakes the hand
        *[act(kid, [kx, 0, kz], kry, 'stand', 'happy', keys=[k(0.0, look=BTN), k(r(0.3 + 0.2 * j), look=[K1[0], 0.9, K1[2]], lookDur=0.2), k(r(TAP + 0.1), toon={'face': {**SHOCK}, 'sq': [0.96, 1.06, 0.96]}, toonDur=0.08), k(r(TAP + 0.3), toon={'face': {**SHOCK}}, toonDur=0.15)])
          for j, (kid, kx, kz, kry) in enumerate([('eleve2', 0.42, -2.8, 70), ('eleve3', 0.14, -2.6, 75)])]],   # (pass 3) the class in a cluster with the teacher, behind him
        props=[FLOOR('sol14'), BUTTON('bt14', litAfter=0.0), P('plaque14', 'bronzePlaque', pos=[BTN[0], 0.82, BACK + 0.04], scale=0.8, opts={'text': "BOUTON D'APPEL/2006"}),
               P('spot14', 'lightCone', pos=[BTN[0], 3.3, BACK + 0.45], opts={'h': 2.3, 'r': 0.42, 'opacity': 0.14}),
               P('cordon14', 'stanchions', pos=[0.705, 0, BACK + 0.75], opts={'w': 0.59}), P('fauteuil14', 'armchair', pos=CH14, opts={'color': '#B5523A'}), BEARD('barbe14', who='vieux', s=1.25), SPECS('lun14', who='vieux'), WEB('toile14c'),
               P('canne14', 'cane', pos=HANDP, ry=CRY, opts={'len': 0.92, 'swing': [r(TAP - 0.07), -1.1, A1, 0.07], 'antic': 0.3, 'rest': 0.25})],   # (pass 3) the stick lies across his lap, whips over the top about his hand and lands on the child's hand over the rope, with a smear (it hung over the child's head and never touched anything)
        cams=[FC(0.0, [2.6, 1.3, 0.4], [[SIT14[0], 1.7, SIT14[2]], [r(SIT14[0] + 0.48), 0.9, SIT14[2]], [BTN[0], 0.66, BTN[2]], [r(K1[0] - 0.28), 1.1, K1[2]], [r(K1[0] - 0.28), 0.45, K1[2]], [TEA[0], 1.82, TEA[2]], [HANDP[0], 1.65, HANDP[2]]], top=0.12, bottom=0.76, lenses=range(26, 62), drift=(-0.1, 0.0, -0.12), inside=ROOM)])   # (pass 3) from his side, low: the child and his class at the left, the button and its plaque in the gap, the stick across it, him at the right (the button hid behind a child, he was cut by the edge)
st.cue('sfx:bonk', 'S14', TAP, 0.3); st.cue('whoosh', 'S14', r(TAP - 0.08), 0.2)

# 15: yesterday... The floor display at last shows RC; a ding; the old man's head snaps up, his eyes out past his glasses, which jump on his nose
D15 = st.dur('S15'); RC = 0.3
st.shot('S15', 'immeubleHall', setOpts=HALL(floor=[[0.0, '1'], [RC, 'RC']]), look={'fill': 0.75, 'sun': 0.7, 'autoExposure': False},   # (pass 3) the 1, then RC (2, 1, RC in a third of a second was cramped); the hall a little darker from here on
        actors=[act('vieux', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look=[0.5, 1.0, -1.0]), k(0.0, toon={'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.0),
            k(r(RC + 0.05), look=DISP, lookDur=0.08), k(r(RC + 0.05), toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'brow': 0.8}, 'sq': [1.16, 0.84, 1.16]}, toonDur=0.05, toonEase='out'),   # (pass 2) squashed...
            k(r(RC + 0.12), toon={'face': {'lid': 0.0, 'eye': 1.0, 'pop': 1.0, 'jaw': 0.6, 'brow': 1.0}, 'sq': [0.86, 1.22, 0.86]}, toonDur=0.06, toonEase='out'), k(r(RC + 0.12), to=[SITP[0], 0.16, SITP[2]], dur=0.07, glide=True, face='keep'),   # ...stretched up out of the chair; (pass 3) his eyes out on stalks and his jaw down (they were half-lidded with a small o)...
            k(r(RC + 0.5), toon={'face': {'lid': 0.0, 'eye': 0.7, 'pop': 0.35, 'mouth': 'O', 'brow': 1.0}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.15), k(r(RC + 0.5), to=SITP, dur=0.15, glide=True, face='keep')])],   # ...held, then settled
        props=[FLOOR('sol15'), BUTTON('bt15', litAfter=0.0), CHAIR('fauteuil15'), BEARD('barbe15', who='vieux', s=1.25, swing=[r(RC + 0.08), r(RC + 0.5), 0.25]), STICK('canne15', who='vieux'), WEB('toile15c'),
               SPECS('lun15', who='vieux', keys=[k(r(RC + 0.12), attach='vieux', joint='head', offset=[0.0, 0.47, 0.13], rot=[0.0, 0.0, 0.25]), k(r(RC + 0.3), attach='vieux', joint='head', offset=[0.0, 0.3, 0.115], rot=[0.0, 0.0, -0.12]),
                                                 k(r(RC + 0.42), attach='vieux', joint='head', offset=[0.0, 0.23, 0.106])])],   # (pass 3) the glasses jump off his nose, askew, and drop back
        cams=[FC(0.0, [-0.75, 1.3, -1.05], [[DISP[0], 2.58, DISP[2]], [DISP[0], 2.22, DISP[2]], [SITP[0], 2.25, SITP[2]], [SITP[0], 1.5, SITP[2]], [r(SITP[0] + 0.28), 1.95, SITP[2]], [r(SITP[0] + 0.5), 2.45, SITP[2]]], top=0.16, bottom=0.72, lenses=range(24, 64))])   # (stills 1) his whole head (it was cut at the edge); (pass 2) room for the stretch
st.cue('sfx:ding', 'S15', RC, 0.5)

# 16: ...the doors opened. From his side: the doors slide apart, their light widens across the dim hall floor and falls on him; in the gap, a
#     seated shape; he grips his stick, beard trembling
D16 = st.dur('S16'); OPEN = 0.1; AUT = [0.0, 0, BACK - 0.62]; DOORS16 = [[0.0, 0.0], [OPEN, 0.0], [r(D16 + 0.25), 0.6]]   # (pass 3) half open at the cut (fully open, the car stood empty before the cut to the man in it)
HCANE = lambda pid, who='vieux', hand='R': P(pid, 'cane', on={'actor': who, 'hand': hand, 'offset': [0.0, 0.0, 0.05], 'hang': True, 'hangYaw': 1.0}, opts={'a': r(PI), 'len': 0.7})   # (pass 3) a stick that stands on the floor under the hand of a seated man (carried along the forearm it lay level, like a lance: the double's went through the closed doors)
TWIN = lambda pfx, at_=AUT: [P(f'fauteuil{pfx}', 'armchair', pos=at_, opts={'color': '#B5523A'}), BEARD(f'barbe{pfx}', who='autre', s=1.25), SPECS(f'lun{pfx}', who='autre'), HCANE(f'canne{pfx}', who='autre'),
                             P(f'plaid{pfx}', 'blanketDrape', pos=[at_[0], 0.72, at_[2] + 0.46], opts={'w': 0.75, 'h': 0.42, 'color': PLAID})]
st.shot('S16', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=DOORS16), look=DIM, actors=[act('vieux', SITP, -35, 'sit', 'neutral', keys=[k(0.0, look=[0.0, 1.5, ZF]),
            k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.0), *[k(r(0.2 + 0.08 * j), toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0}, 'sq': [1.0, 1.02 if j % 2 else 0.98, 1.0]}, toonDur=0.04) for j in range(10)]]),
        act('autre', [AUT[0], 0, AUT[2] + 0.08], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[FLOOR('sol16'), GLOW('lueur16', DOORS16), BUTTON('bt16', litAfter=0.0), P('fauteuil16', 'armchair', pos=CH, ry=-35, opts={'color': '#B5523A'}), BEARD('barbe16', who='vieux', s=1.25, swing=[0.2, 1.0, 0.12]), SPECS('lun16', who='vieux'),
               HCANE('canne16'),
               WEB('toile16c'), *TWIN('16b')],
        cams=[FC(0.0, [-2.4, 1.3, -0.8], [[-0.62, 2.25, ZF], [-0.62, 0.25, ZF], [SITP[0], 1.72, SITP[2]], [1.95, 0.7, CH[2]], [0.3, 0.2, -1.5]], top=0.14, bottom=0.76, lenses=range(26, 62), drift=(0.15, 0.0, -0.05), inside=ROOM)])   # (pass 3) along the wall from the letter boxes: the doors part in front of us, their light runs across the floor to him, and he faces us, lit (the frontal wide left him small in profile in a pale frame, and showed the car empty)
st.cue('sfx:slideUp', 'S16', OPEN, 0.6)

# 17: inside there was a man. In the doorway, as the doors finish opening: an old man with a white beard in an armchair just like his, a blanket,
#     cobwebs, lit by the car; he blinks at us
D17 = st.dur('S17'); DOORS17 = [[0.0, 0.55], [0.3, 1.0]]
st.shot('S17', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=DOORS17), look=DIM, actors=[act('autre', [AUT[0], 0, AUT[2] + 0.08], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.0),
            k(0.5, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.15), k(0.78, toon={'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.15), k(1.1, look=[SITP[0], 2.0, SITP[2]], lookDur=0.4)])],   # (pass 2) a slow blink at us, shut four frames
        props=[FLOOR('sol17'), GLOW('lueur17', DOORS17), *TWIN('17'), P('toile17', 'cobweb', pos=[-0.5, 1.9, BACK - 0.2], ry=0, opts={'s': 0.7}),
               P('toile17b', 'cobweb', pos=[0.62, 1.15, AUT[2] + 0.1], ry=-90, opts={'s': 0.55})],   # (pass 2) the same red armchair and blanket as his, chunky cobwebs
        cams=[FC(0.0, [0.3, 1.5, -0.3], [[AUT[0], 2.25, AUT[2]], [AUT[0], 0.0, AUT[2] + 0.3], [-0.6, 2.2, ZF], [0.6, 2.2, ZF]], top=0.14, bottom=0.76, drift=(0.0, 0.0, -0.2))])

# 18: he had been waiting for the ground floor... Close on the car's panel beside him: his finger on the RC button, its amber ring breathing as in
#     the first shot, RC on a plate under it, dust everywhere but there; then up to his face
D18 = st.dur('S18'); PAN = [-0.78, 1.2, BACK - 0.78]; AUT18 = [0.22, 0, BACK - 0.62]; YRC = r(PAN[1] - 0.222); OPEN1 = [[0.0, 1.0]]   # (pass 3) the panel deeper on the car's left wall, filmed from inside the car, three-quarters, like the call button in the first shot
PRESS18 = {'reach': {'R': [r(PAN[0] + 0.06), YRC, PAN[2], 1, 0.04]}, 'hands': {'R': 'point'}}
st.shot('S18', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=OPEN1), look=DIM, actors=[act('autre', [AUT18[0], 0, AUT18[2] + 0.08], 0, 'sit', 'neutral', keys=[k(0.0, look=PAN), k(0.65, look='camera', lookDur=0.25),
            k(0.0, toon={**PRESS18, 'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.0),
            k(0.2, toon={'reach': {'R': [r(PAN[0] + 0.045), YRC, PAN[2], 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.06), k(0.34, toon={**PRESS18, 'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.1),   # (pass 3) he presses it once more, for nothing
            k(0.95, toon={**PRESS18, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07), k(1.07, toon={**PRESS18, 'face': {**OLDF, 'mouth': 'line'}}, toonDur=0.08)])],
        props=[FLOOR('sol18'), GLOW('lueur18', OPEN1), P('fauteuil18', 'armchair', pos=AUT18, opts={'color': '#B5523A'}), BEARD('barbe18', who='autre', s=1.25), SPECS('lun18', who='autre'),
               P('panneau18', 'liftPanel', pos=PAN, ry=90, opts={'lit': 'RC', 'dusty': True}), P('lambris18', 'slab', pos=[r(PAN[0] + 0.012), 0.42, BACK - 0.65], opts={'w': 0.02, 'h': 0.84, 'd': 1.26, 'color': '#7C6A58'}), P('toile18', 'cobweb', pos=[r(PAN[0] + 0.03), r(PAN[1] + 0.36), r(PAN[2] + 0.2)], ry=90, opts={'s': 0.3})],   # (pass 3) lambris18: a dark dado on the car's wall under the panel (the caption band lay on bare cream wall)
        cams=[FC(0.0, [-0.36, 1.12, BACK - 1.2], [[PAN[0], r(YRC + 0.12), PAN[2]], [PAN[0], r(YRC - 0.15), PAN[2]], [PAN[0], YRC, r(PAN[2] + 0.15)], [PAN[0], YRC, r(PAN[2] - 0.1)]], top=0.2, bottom=0.72, lenses=range(18, 66), step=0.02, most=0.06),   # (pass 3) from the back of the car, behind his arm: the button, its ring and its plate in front, the finger coming onto it from beyond, the open doors behind (no door edge, no glasses rim, no sleeve across the frame)
              FC(0.55, [0.3, 1.55, -1.9], [[AUT18[0], 2.15, AUT18[2]], [AUT18[0], 1.3, AUT18[2]], [r(AUT18[0] - 0.3), 1.8, AUT18[2]], [r(AUT18[0] + 0.3), 1.8, AUT18[2]]], top=0.16, bottom=0.74, lenses=range(18, 56))])   # (pass 3) a cut (the glide flew through his sleeve)   # (stills 2) out through the doorway to his face (inside the car the door post filled the frame)   # (pass 2) the callback to S01: close on the finger on RC, then up to his face
st.cue('sfx:beep', 'S18', 0.2, 0.25)

# 19: ...for twenty years. The two old men face to face across the threshold, identical beards, identical armchairs, the same deadpan; they blink
#     together
D19 = st.dur('S19')
AUT19 = [0.12, 0, BACK - 0.3]; HERO19 = [1.22, 0, -2.25]   # (pass 3) closer together and nearer the middle of the frame (both were cut by its edges)
st.shot('S19', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=OPEN1), look=DIM, actors=[act('vieux', HERO19, -32, 'sit', 'neutral', darts=0, keys=[k(0.0, look=[0.35, 1.5, -1.3]), k(0.0, toon={'face': {'lid': 0.55, 'gx': -0.75, 'mouth': 'line'}}, toonDur=0.0),   # (pass 3) his head three-quarters to us, his eyes on the other (his face was a blank profile)
            k(0.6, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(0.74, toon={'face': {'lid': 0.55, 'gx': -0.75, 'mouth': 'line'}}, toonDur=0.12)]),
        act('autre', [AUT19[0], 0, AUT19[2] + 0.08], 32, 'sit', 'neutral', darts=0, keys=[k(0.0, look=[1.0, 1.5, -1.3]), k(0.0, toon={'face': {'lid': 0.55, 'gx': 0.75, 'mouth': 'line'}}, toonDur=0.0),
            k(0.6, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(0.74, toon={'face': {'lid': 0.55, 'gx': 0.75, 'mouth': 'line'}}, toonDur=0.12)])],   # (pass 2) three-quarters to us both, blinking together (two strict profiles hid both faces)
        props=[FLOOR('sol19'), GLOW('lueur19', OPEN1), P('fauteuil19a', 'armchair', pos=[HERO19[0], 0, r(HERO19[2] - 0.08)], ry=-32, opts={'color': '#B5523A'}), P('fauteuil19b', 'armchair', pos=AUT19, ry=32, opts={'color': '#B5523A'}),
               BEARD('barbe19a', who='vieux', s=1.25), SPECS('lun19a', who='vieux'), WEB('toile19a'), BEARD('barbe19b', who='autre', s=1.25), SPECS('lun19b', who='autre'), WEB('toile19b', who='autre'), BUTTON('bt19', litAfter=0.0)],
        cams=[FC(0.0, [0.68, 1.5, 1.3], [[HERO19[0], 1.75, HERO19[2]], [r(HERO19[0] + 0.42), 1.25, HERO19[2]], [AUT19[0], 1.75, AUT19[2]], [r(AUT19[0] - 0.42), 1.25, AUT19[2]], [0.68, 0.72, -2.5]], top=0.16, bottom=0.74, lenses=range(26, 62))])   # (pass 2) square on, between them; (pass 3) both whole in the frame

# 20: they shook hands. Standing side by side facing us, as for an official photo, in the light of the open car, the two old men shake hands; a flash
D20 = st.dur('S20'); M20, A20 = [0.75, 0, -1.55], [-0.15, 0, -1.55]
SH20 = lambda hand, j: {'reach': {hand: [0.3, r(1.25 + (0.2 if j % 2 else -0.2)), -1.35, 1, 0.04]}, 'hands': {hand: 'grip'}, 'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.05, 0.93, 1.05] if j % 2 == 0 else [1.01, 0.98, 1.01]}   # (pass 3) big pumps, the bodies bobbing with them (the pumps were a few pixels)
st.shot('S20', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=OPEN1), look=DIM, actors=[act('vieux', M20, -10, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0),
            k(0.15, toon={'reach': {'R': [0.3, 1.25, -1.35, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.25, toonEase='out'),
            *[k(r(0.45 + 0.14 * j), toon=SH20('R', j), toonDur=0.12) for j in range(4)], k(1.05, toon={**SH20('R', 1), 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07), k(1.2, toon=SH20('R', 1), toonDur=0.1)]),   # a blink after the flash
        act('autre', A20, 10, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0),
            k(0.15, toon={'reach': {'L': [0.3, 1.25, -1.35, 1, 0.04]}, 'hands': {'L': 'grip'}, 'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.25, toonEase='out'),
            *[k(r(0.45 + 0.14 * j), toon=SH20('L', j), toonDur=0.12) for j in range(4)], k(1.05, toon={**SH20('L', 1), 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07), k(1.2, toon=SH20('L', 1), toonDur=0.1)])],
        props=[FLOOR('sol20'), GLOW('lueur20', OPEN1), BEARD('barbe20a', who='vieux', s=1.25), SPECS('lun20a', who='vieux'), STICK('canne20', who='vieux', hand='L'), BEARD('barbe20b', who='autre', s=1.25), SPECS('lun20b', who='autre'), BUTTON('bt20', litAfter=0.0),
               P('flash20', 'flashBursts', pos=[0.3, 1.8, 1.2], opts={'n': 1, 'w': 1.2, 'h': 1.2, 'at': [0.9]})],
        cams=[FC(0.0, [0.3, 1.2, 1.2], [[M20[0], 2.45, M20[2]], [A20[0], 2.45, A20[2]], [0.3, 1.1, -1.35], [M20[0], 0.9, M20[2]], [A20[0], 0.9, A20[2]], [r(M20[0] + 0.38), 1.3, M20[2]], [r(A20[0] - 0.38), 1.3, A20[2]]], top=0.16, bottom=0.74)],   # low and close, like the press photo
        fx=[{'type': 'flash', 'at': 0.9, 'dur': 0.14}])   # (pass 2) the flash over the whole frame (none of the draft's frames showed it)
st.cue('sfx:shutter', 'S20', 0.9, 0.4)

# 21: and they took the stairs. From the foot of the stairs: the two of them climb, one step at a time, toward the way up; behind them the lift doors
#     close with a ding and their light narrows on the floor; near the top they both turn round and look at us
D21 = st.dur('S21'); ST = [2.3, 0, -0.35]; TURN = 1.4; XV, XA = 1.96, 2.6   # (pass 3) the stairs a step nearer the lift; the two men a shoulder apart
def STEP(x, i): return [x, r(0.2 * i), r(-0.1 - 0.28 * i)]
def climb(x, i0, t0, n, step=0.32): return [k(r(t0 + i * step), to=STEP(x, i0 + i + 1), dur=r(step * 0.8), ease='inOut', clip='walk', face='keep') for i in range(n)]
DOORS21 = [[0.0, 1.0], [0.45, 1.0], [1.2, 0.0]]
F21 = {'face': {**OLDF, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}
st.shot('S21', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=DOORS21, plant=False), look=DIM, actors=[
        act('vieux', STEP(XV, 2), 180, 'stand', 'neutral', keys=[*climb(XV, 2, 0.0, 4), k(TURN, face=12, turn=0.3), k(TURN, look='camera', lookDur=0.2), k(0.0, toon=F21, toonDur=0.0),   # (pass 3) they turn right round to us and hold it (the look back was the back of two heads)
            k(r(TURN + 0.5), toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.08), k(r(TURN + 0.62), toon=F21, toonDur=0.1)]),
        act('autre', STEP(XA, 1), 180, 'stand', 'neutral', keys=[*climb(XA, 1, 0.12, 4), k(r(TURN + 0.06), face=6, turn=0.3), k(r(TURN + 0.06), look='camera', lookDur=0.2), k(0.0, toon=F21, toonDur=0.0),
            k(r(TURN + 0.5), toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.08), k(r(TURN + 0.62), toon=F21, toonDur=0.1)])],
        props=[FLOOR('sol21'), GLOW('lueur21', DOORS21), P('escalier21', 'stairs', pos=ST, opts={'steps': 9, 'w': 1.1, 'rail': False}), P('porte21', 'stairDoor', pos=[ST[0], 1.8, BACK + 0.03], opts={'w': 1.15, 'h': 1.6, 'sign': [-1.33, 0.5]}),   # (pass 3) the stairs lead somewhere: a dark way up and its sign (they ran into a blank wall)
               BEARD('barbe21a', who='vieux', s=1.25), SPECS('lun21a', who='vieux'), STICK('canne21a', who='vieux'), BEARD('barbe21b', who='autre', s=1.25), SPECS('lun21b', who='autre'),
               STICK('canne21b', who='autre'), BUTTON('bt21', litAfter=0.0)],
        cams=[FC(0.0, [2.9, 1.45, 2.7], [[XV, 3.0, STEP(XV, 6)[2]], [XA, 0.2, STEP(XA, 1)[2]], [r(XA + 0.3), 1.3, STEP(XA, 1)[2]], [0.5, 0.25, ZF], [-0.3, 2.15, ZF]], top=0.1, bottom=0.78, lenses=range(26, 61), inside=ROOM)])   # (pass 3) from the foot of the stairs: the two men big, the closing doors and their light in the left third
st.cue('sfx:step', 'S21', 0.0, 0.2); st.cue('sfx:step', 'S21', 0.32, 0.2); st.cue('sfx:step', 'S21', 0.64, 0.2); st.cue('sfx:step', 'S21', 0.96, 0.2); st.cue('sfx:ding', 'S21', 1.2, 0.4)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("L'ascenseur", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'vieux': {'preset': 'lemec', 'tint': '#E6F2FF', 'hairColor': '#ECEAE4', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 2) the same man twenty years on: white hair
    'gris': {'preset': 'lemec', 'tint': '#E6F2FF', 'hairColor': '#8E8A84', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 2) greying, during the works
    'autre': {'preset': 'lemec', 'tint': '#E6F2FF', 'hairColor': '#ECEAE4', 'tie': '#2E7D5B', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 2) his mirror: the same man, only the tie differs (bald, grey and yellow he was another man)
    'mamie': {'preset': 'mamie', 'seed': 822, 'build': {'width': 0.95, 'headWidth': 1.22}, 'toon': EX},
    'concierge': {'preset': 'madame', 'seed': 823, 'suit': '#4F7AA8', 'build': {'width': 1.0, 'headWidth': 1.22}, 'toon': EX},
    'syndic': {'preset': 'boss', 'seed': 824, 'suit': '#55627A', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},   # (pass 3) slate blue (near black he was a featureless block)
    'voisin1': {'preset': 'femme', 'seed': 825, 'build': {'width': 0.9, 'headWidth': 1.2}, 'toon': EX},
    'voisin2': {'preset': 'avocat', 'seed': 826, 'suit': '#B5762E', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},   # (pass 3) ochre, not black
    'voisin3': {'preset': 'madame', 'seed': 827, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'ouvrier': {'preset': 'worker', 'seed': 828, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'maitresse': {'preset': 'femme', 'seed': 829, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.2}, 'toon': EX},
    **{kid: {'preset': 'gamin', 'seed': 830 + j, 'suit': ['#E8A33C', '#5BB5A8', '#E25C7A'][j], 'build': {'height': 0.58, 'width': 0.85, 'headScale': 1.3, 'headWidth': 1.2}, 'toon': EX} for j, kid in enumerate(['eleve1', 'eleve2', 'eleve3'])},   # (pass 2) children's size (85 % of the teacher, adult proportions)
})
