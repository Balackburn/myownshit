#!/usr/bin/env python3
"""L'ascenseur (story 76, cycle 38; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man called the lift twenty years ago. The lift never came. So he waited. The neighbours bring him food. The concierge put an armchair there for
him. The residents' association voted for works. The works lasted fifteen years. He grew old in front of the button. The button is a listed monument.
Schools come to visit it. Yesterday the doors opened. Inside there was a man. He had been waiting twenty years for the ground floor. They shook hands.
And they took the stairs.
Staging: a building hall with lift doors, a floor display, a call button; he presses it and turns to us beside the doors, a 2006 calendar on the wall;
the display counts down to 1 and climbs again, never RC; a time-lapse with the clock spinning and his beard growing; a neighbour's soup and baguette;
the concierge rolls in an armchair, he drops into it in a puff of dust; a residents' meeting with raised hands, his too; a jackhammer in dust while
he sits; calendar pages flying; old, white-bearded, glasses, cobwebs; the button under a spotlight with a bronze plaque and a velvet rope; a class
of children, his walking stick taps a kid's hand away from it; RC lights up with a ding, the doors slide open on an identical old man in an identical
armchair, cobwebs and all, his finger on the RC button inside; a handshake for the photographer; both climb the stairs while the doors close.
Natural look; cycle 38: props_ascenseur.js (armchair, jackhammer, cobweb, liftPanel, lightCone, callButton)."""
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
DEAD = {'lid': 0.45}
OLD = {'lid': 0.55}
BACK = -3.0; ZF = BACK + 0.06                     # the hall's back wall and the lift doors' plane
BTN = [0.83, 1.12, BACK + 0.07]                   # the call button (our big one, over the set's)
DISP = [0.0, 2.4, ZF]                             # the floor display above the doors
ME = [1.42, 0, -2.42]                             # where he waits, beside the button, facing us
CH = [1.45, 0, -2.5]; SITP = [1.45, 0, -2.42]     # the armchair and where he sits in it
CAL = [-1.15, 1.62, BACK + 0.02]; CLK = [-1.15, 2.6, BACK + 0.04]
HALL = lambda **kw: {'notice': 'SYNDIC', 'car': True, **kw}   # (pass 2) a lit car behind the doors (the doorway showed the hall's own wall)
BUTTON = lambda pid, **kw: P(pid, 'callButton', pos=BTN, opts=kw)
CHAIR = lambda pid, **kw: P(pid, 'armchair', pos=CH, opts={'color': '#B5523A', **kw})
BEARD = lambda pid, who='mec', s=1.2, color='#E4E0D8', keys=None, swing=None: P(pid, 'beardHair', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.02, 0.1], 'hang': True, 'hangYaw': 0.4}, scale=s,   # (pass 3) hang: it hangs by gravity from the chin (nailed to the head it swung into the chest when the head turned)
                                                       opts={'len': 0.95, 'coil': 0.0, 'color': color, 'depth': 0.12, 'w': 0.26, **({'swing': swing, 'whip': True} if swing else {})}, **({'keys': keys} if keys else {}))
SPECS = lambda pid, who='mec': P(pid, 'glasses', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.23, 0.106]}, opts={'r': 0.042, 'dx': 0.055})   # (pass 2) at eye level (they sat at the jaw); (pass 3) on the face (z 0.16 floated 6 cm in front of it: seen in profile they hung in the air)
PLAID = '#2E7D5B'   # (pass 2) a green blanket against the red armchair (it was lost under the dust)
STICK = lambda pid, who='mec', hand='R': P(pid, 'slab', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.45, 0.04]}, opts={'w': 0.03, 'h': 0.95, 'd': 0.03, 'color': '#6B4A2E'})
WEBS = lambda pfx: [P(f'{pfx}a', 'cobweb', pos=[CH[0] + 0.43, 1.25, CH[2] - 0.3], ry=-90, opts={'s': 0.42}), P(f'{pfx}b', 'cobweb', pos=[0.55, 2.1, ZF + 0.02], opts={'s': 0.38})]
SIT = lambda pid, t0=0.0: k(t0, clip='sit')

for g_ in [('S03', 1.15, 'mec', 'display'), ('S07', 0.25, 'mec', 'chair'), ('S14', 0.9, 'mec', 'stick'), ('S16', 0.5, 'mec', 'doors'), ('S17', 0.6, 'autre', 'twin'), ('S21', 0.6, 'mec', 'stairs')]:
    st.gag(*g_)
st.card('S08', 'VOTÉ', at=0.8)
st.card('S12', 'MONUMENT HISTORIQUE', at=0.35)

# 1: the hook. Close on the call button: his finger presses it, the ring lights up
D1 = st.dur('S01')
st.shot('S01', 'immeubleHall', setOpts=HALL(), actors=[act('mec', [1.3, 0, -2.38], 200, 'stand', 'neutral', keys=[k(0.0, look=BTN),
            k(0.1, toon={'reach': {'L': [BTN[0] + 0.01, BTN[1] + 0.01, BTN[2] + 0.05, 1, 0.04]}, 'hands': {'L': 'point'}}, toonDur=0.25, toonEase='out'),
            k(0.4, toon={'reach': {'L': [BTN[0], BTN[1] + 0.01, BTN[2] + 0.025, 1, 0.04]}, 'hands': {'L': 'point'}}, toonDur=0.06), k(0.75, toon={'reach': {'L': [1.0, 1.3, -2.55, 1, 0.04]}, 'hands': {'L': 'point'}}, toonDur=0.25)])],
        props=[BUTTON('bt1', pressAt=0.4)],
        cams=[FC(0.0, [0.3, 1.2, -2.3], [[BTN[0], 1.24, BTN[2]], [BTN[0], 1.0, BTN[2]], [BTN[0] - 0.12, 1.12, BTN[2]], [BTN[0] + 0.25, 1.12, BTN[2] + 0.2]], top=0.3, bottom=0.66, lenses=range(16, 50))])   # (stills 1) beside the button, left of his reach: from behind his shoulder his arm blacked out the frame
st.cue('sfx:beep', 'S01', 0.4, 0.3)

# 2: ...twenty years ago. Wide on the hall: he turns his back to the doors and waits beside them, hands behind his back; a 2006 calendar on the wall
D2 = st.dur('S02')
st.shot('S02', 'immeubleHall', setOpts=HALL(floor=[[0.0, '7']]), actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'touch': {'R': ['torso', 0.1, 0.25, -0.2, 1, 0.02], 'L': ['torso', -0.1, 0.25, -0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}}, toonDur=0.0),
            k(0.6, toon={'touch': {'R': ['torso', 0.1, 0.25, -0.2, 1, 0.02], 'L': ['torso', -0.1, 0.25, -0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.0, 1.02, 1.0]}, toonDur=0.3, toonEase='inOut'),
            k(0.95, toon={'touch': {'R': ['torso', 0.1, 0.25, -0.2, 1, 0.02], 'L': ['torso', -0.1, 0.25, -0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.3, toonEase='inOut')])],
        props=[BUTTON('bt2', litAfter=0.0), P('cal2', 'monthCalendar', pos=CAL, scale=1.3, opts={'months': ['2006']}), P('horloge2', 'wallClock', pos=CLK, scale=0.6, opts={'rate': 0.02})],
        cams=[FC(0.0, [0.5, 1.6, 2.4], [[ME[0], 2.45, ME[2]], [ME[0], 0.0, ME[2]], [DISP[0], 2.6, DISP[2]], [CAL[0] - 0.25, 1.95, CAL[2]], [CAL[0] - 0.25, 1.3, CAL[2]]], top=0.14, bottom=0.76, drift=(0.0, 0.0, -0.3))])

# 3: the lift never came. Low, looking up at the floor display: it counts down to 1... and climbs again; his face below falls
D3 = st.dur('S03'); FL3 = [[0.0, '6'], [0.13, '5'], [0.26, '4'], [0.39, '3'], [0.52, '2'], [0.65, '1'], [1.2, '2'], [1.38, '3'], [1.56, '4']]   # (pass 2) the 1 held 0.55 s
st.shot('S03', 'immeubleHall', setOpts=HALL(floor=FL3), actors=[act('mec', ME, -20, 'stand', 'neutral', keys=[k(0.0, look=DISP),
            k(0.68, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'smile', 'brow': 0.9}, 'sq': [0.94, 1.08, 0.94]}, toonDur=0.1, toonEase='out'),   # (pass 2) up on his toes at the 1...
            k(1.2, toon={'face': {'lid': 0.65, 'mouth': 'line', 'brow': -0.3}, 'sq': [1.1, 0.86, 1.1]}, toonDur=0.06, toonEase='in'), k(1.32, toon={'face': {'lid': 0.65, 'mouth': 'line', 'brow': -0.3}, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.15)])],   # ...flattened when it jumps to 2
        props=[BUTTON('bt3', litAfter=0.0)],
        cams=[FC(0.0, [0.2, 1.3, -1.2], [[DISP[0], 2.58, DISP[2]], [DISP[0], 2.22, DISP[2]], [r(DISP[0] - 0.3), 2.4, DISP[2]], [ME[0], 2.4, ME[2]], [ME[0], 1.7, ME[2]]], top=0.16, bottom=0.7, lenses=range(24, 64))])   # (pass 2) the display inside the frame (it was jammed in the corner)
for t_ in [0.13, 0.26, 0.39, 0.52, 0.65, 1.2, 1.38, 1.56]: st.cue('sfx:tick', 'S03', t_, 0.12)

# 4: so he waited. Time-lapse: the clock's hands whirl, his beard grows from nothing to his chest, he sags little by little
D4 = st.dur('S04')
st.shot('S04', 'immeubleHall', setOpts=HALL(floor=[[0.0, '4'], [0.4, '9'], [0.8, '2'], [1.2, '6']]), actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0), k(0.4, toon={'face': {'lid': 0.55, 'mouth': 'line'}, 'sq': [1.02, 0.97, 1.02]}, toonDur=0.6, toonEase='inOut'),
            k(1.0, toon={'face': {'lid': 0.65, 'mouth': 'line'}, 'sq': [1.04, 0.93, 1.04]}, toonDur=0.5, toonEase='inOut'), k(1.4, toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.04, 0.93, 1.04]}, toonDur=0.08)])],
        props=[BUTTON('bt4', litAfter=0.0), P('cal4', 'monthCalendar', pos=CAL, scale=1.3, opts={'months': ['2006']}), P('horloge4', 'wallClock', pos=CLK, scale=0.6, opts={'rate': 4.0}),
               BEARD('barbe4', s=0.05, color='#5A4636', keys=[k(0.0, scale=0.05), k(0.05, scale=1.1, dur=1.45, ease='linear')])],
        cams=[FC(0.0, [-1.8, 1.8, 0.7], [[ME[0], 2.45, ME[2]], [ME[0], 0.0, ME[2]], [CLK[0], 2.85, CLK[2]], [CAL[0], 1.3, CAL[2]]], top=0.14, bottom=0.76)])
st.cue('sfx:ticks', 'S04', 0.0, 1.6)

# 5: the neighbours bring him food. A grandmother from upstairs puts a bowl of soup and a baguette in his hands; he takes them without a word
D5 = st.dur('S05'); MAM = [0.55, 0, -1.5]
st.shot('S05', 'immeubleHall', setOpts=HALL(floor=[[0.0, '3']]), actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.5, 1.6, -1.6]), k(0.75, toon={'reach': {'R': [1.12, 1.25, -2.0, 1, 0.04], 'L': [1.25, 1.2, -1.95, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.2),
            k(1.2, look='camera', lookDur=0.25)]),
        act('mamie', [-0.4, 0, -0.9], 60, 'walk', 'happy', keys=[k(0.0, to=MAM, dur=0.6, clip='walk', then='giveItem', ease='out'), k(0.0, look=[ME[0], 2.0, ME[2]])])],
        props=[BUTTON('bt5', litAfter=0.0), BEARD('barbe5', s=0.75, color='#5A4636'),
               P('soupe5', 'soupBowl', on={'actor': 'mamie', 'hand': 'R', 'offset': [0.0, 0.0, 0.06]}, scale=1.5, keys=[k(0.85, attach={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.06]})]),
               P('pain5', 'baguette', on={'actor': 'mamie', 'hand': 'L', 'offset': [0, 0, 0.04]}, keys=[k(0.85, attach={'actor': 'mec', 'hand': 'L', 'offset': [0, 0, 0.04]})])],
        cams=[FC(0.0, [1.9, 1.6, 1.4], [[ME[0], 2.45, ME[2]], [ME[0], 0.0, ME[2]], [MAM[0], 2.3, MAM[2]], [-0.4, 2.3, -0.9]], top=0.14, bottom=0.76)])
st.cue('sfx:stepSoft', 'S05', 0.15, 0.15); st.cue('sfx:stepSoft', 'S05', 0.45, 0.15)

# 6: the concierge put an armchair there... She pushes a big old armchair across the hall toward him, cheerful
D6 = st.dur('S06'); CON0 = [-2.2, 0, -0.6]
st.shot('S06', 'immeubleHall', setOpts=HALL(floor=[[0.0, '8']]), actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look=[-1.0, 1.0, -1.2]), k(0.9, look=[0.2, 1.0, -1.6])]),
        act('concierge', CON0, 70, 'pushCart', 'happy', keys=[k(0.0, to=[0.1, 0, -1.45], dur=D6, clip='pushCart', ease='linear', face='keep'), k(0.0, look=[ME[0], 2.0, ME[2]])])],
        props=[BUTTON('bt6', litAfter=0.0), BEARD('barbe6', s=0.85, color='#6E6052'),
               P('fauteuil6', 'armchair', pos=[-1.55, 0, -0.85], ry=-20, keys=[k(0.0, to=[0.75, 0, -1.7], dur=D6, ease='linear')], opts={'color': '#B5523A'})],
        cams=[FC(0.0, [-0.2, 1.7, 2.2], [[ME[0], 2.45, ME[2]], [CON0[0], 2.3, CON0[2]], [0.75, 0.0, -1.7], [ME[0], 0.0, ME[2]]], top=0.14, bottom=0.76, drift=(0.35, 0.0, 0.0))])
st.cue('sfx:rattle', 'S06', 0.0, 1.0)

# 7: ...an armchair. He drops into it: the cushion squashes and springs back in a puff of dust; she tucks a blanket over his knees
D7 = st.dur('S07'); SINK = 0.2
st.shot('S07', 'immeubleHall', setOpts=HALL(floor=[[0.0, '8']]), actors=[act('mec', [SITP[0], 0.6, SITP[2]], 0, 'sit', 'neutral', keys=[k(0.0, to=SITP, dur=SINK, ease='in', clip='sit', face='keep', glide=True), k(0.0, look='camera'),
            k(0.0, toon={'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.3, 'mouth': 'O'}}, toonDur=0.0),   # (pass 2) stretched as he drops from higher...
            k(SINK, toon={'sq': [1.18, 0.78, 1.18], 'face': {'lid': 0.8, 'mouth': 'O'}}, toonDur=0.04, toonEase='out'), k(r(SINK + 0.12), toon={'sq': [0.94, 1.07, 0.94], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08),   # ...squashed three frames, overshoot
            k(r(SINK + 0.3), toon={'sq': [1.0, 1.0, 1.0], 'face': {**DEAD, 'mouth': 'smile'}}, toonDur=0.15)]),
        act('concierge', [0.55, 0, -1.65], 60, 'stand', 'happy', keys=[k(0.0, look=[SITP[0], 1.0, SITP[2]]), k(0.45, toon={'reach': {'R': [1.25, 0.95, -2.05, 1, 0.04], 'L': [1.15, 0.95, -2.2, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.25)])],
        props=[BUTTON('bt7', litAfter=0.0), CHAIR('fauteuil7', sinkAt=SINK), BEARD('barbe7', s=0.85, color='#6E6052'),
               P('poussiere7', 'dustPuff', pos=[SITP[0], 0.45, SITP[2] + 0.2], scale=1.05, opts={'once': True, 'startAt': SINK, 'period': 0.7, 'color': '#E8E0D0'}),
               P('plaid7', 'blanketDrape', pos=[SITP[0], 0.72, SITP[2] + 0.38], opts={'w': 0.75, 'h': 0.42, 'color': PLAID}, keys=[k(0.0, visible=False), k(0.75, visible=True)])],
        cams=[FC(0.0, [1.0, 1.25, 0.6], [[SITP[0], 2.1, SITP[2]], [SITP[0], 0.0, SITP[2] + 0.4], [0.55, 2.3, -1.65], [0.55, 0.0, -1.65], [CH[0] - 0.45, 1.2, CH[2]]], top=0.16, bottom=0.74)])
st.cue('thud', 'S07', SINK, 0.4); st.cue('sfx:poof', 'S07', SINK, 0.4)

# 8: the residents' association voted for works. A meeting in the hall: the chairman bangs his gavel at a folding table, three residents raise their
#    hands, and so does he, from his armchair (VOTÉ)
D8 = st.dur('S08'); BANG8 = 0.75
st.shot('S08', 'immeubleHall', setOpts=HALL(floor=[[0.0, '5']]), actors=[act('mec', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look=[-0.6, 1.8, -0.6]), k(0.3, toon={'reach': {'R': [1.6, 2.7, -2.2, 1, 0.04]}, 'hands': {'R': 'open'}}, toonDur=0.2, toonEase='out'),
            k(1.0, look='camera', lookDur=0.25), k(1.3, toon={'reach': {'R': [1.6, 2.7, -2.2, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0}}, toonDur=0.08), k(1.42, toon={'reach': {'R': [1.6, 2.7, -2.2, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {**DEAD}}, toonDur=0.12)]),
        act('syndic', [-0.75, 0, -1.6], 30, 'stand', 'neutral', keys=[k(0.0, look=[0.2, 1.6, 0.6]), k(0.0, toon={'reach': {'R': [-0.55, 1.6, -1.15, 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(BANG8, toon={'reach': {'R': [-0.55, 0.85, -1.15, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.05, toonEase='in')]),
        *[act(rid, [rx, 0, rz], rry, 'stand', 'neutral', keys=[k(0.0, look=[-0.75, 2.0, -1.6]),
            k(r(0.15 + 0.08 * j), toon={'reach': {'R': [r(rx + 0.15), 2.7, r(rz - 0.1), 1, 0.04]}, 'hands': {'R': 'open'}}, toonDur=0.2, toonEase='out'),
            k(r(0.9 + 0.2 * j), toon={'reach': {'R': [r(rx + 0.15), 2.78, r(rz - 0.1), 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0}}, toonDur=0.08),
            k(r(1.0 + 0.2 * j), toon={'reach': {'R': [r(rx + 0.15), 2.7, r(rz - 0.1), 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.2}}, toonDur=0.15)])
          for j, (rid, rx, rz, rry) in enumerate([('voisin1', -2.05, -0.9, 80), ('voisin2', -1.55, 0.2, 145), ('voisin3', 0.35, -0.5, -115)])]],
        props=[BUTTON('bt8', litAfter=0.0), CHAIR('fauteuil8'), BEARD('barbe8', s=0.9, color='#7A6E62'), P('table8', 'desk', pos=[-0.75, 0, -1.15], ry=180, opts={'w': 1.3}),
               P('marteau8', 'gavel', on={'actor': 'syndic', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}),
               P('banniere8', 'signBoard', pos=[-0.75, 2.45, BACK + 0.05], opts={'text': 'ASSEMBLÉE GÉNÉRALE', 'bg': '#F3EBD6', 'fg': '#7A2A1E', 'w': 2.0, 'h': 0.32, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [0.1, 2.0, 3.3], [[SITP[0], 2.75, SITP[2]], [-0.75, 2.75, BACK], [-2.05, 2.4, -0.9], [-1.55, 2.4, 0.2], [-1.55, 0.0, 0.2]], top=0.14, bottom=0.76)])
st.cue('sfx:gavel', 'S08', BANG8, 0.4)

# 9: the works lasted... A worker drills the floor in front of the lift with a jackhammer, dust everywhere; he sits through it, unmoved, greying
D9 = st.dur('S09'); OUV = [0.15, 0, -1.9]
st.shot('S09', 'immeubleHall', setOpts=HALL(floor=[[0.0, '—']]), actors=[act('gris', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            *[k(r(0.1 + 0.07 * j), toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': [1.0, 0.99 if j % 2 else 1.01, 1.0]}, toonDur=0.035) for j in range(20)]]),
        act('ouvrier', OUV, 20, 'stand', 'determined', keys=[k(0.0, look=[0.15, 0.0, -1.5]), k(0.0, toon={'reach': {'R': [0.07, 1.02, -1.6, 1, 0.04], 'L': [0.37, 1.02, -1.6, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            *[k(r(0.08 * j), toon={'reach': {'R': [0.07, 1.02, -1.6, 1, 0.04], 'L': [0.37, 1.02, -1.6, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.02 if j % 2 else 0.99, 0.98 if j % 2 else 1.01, 1.0]}, toonDur=0.04) for j in range(1, 12)]])],
        props=[BUTTON('bt9', litAfter=0.0), CHAIR('fauteuil9'), BEARD('barbe9', who='gris', s=0.95, color='#A49C90'),
               P('piqueur9', 'jackhammer', pos=[0.22, 1.02, -1.6], opts={'from': 0.0, 'floorY': -1.0}), P('panneau9', 'signBoard', pos=[-0.95, 0, -1.15], ry=15, opts={'text': 'TRAVAUX', 'bg': '#F2C230', 'fg': '#1B1B1E', 'w': 0.8, 'h': 0.4}),
               P('nuage9', 'dustPuff', pos=[0.2, 0.05, -1.55], scale=2.4, opts={'startAt': 0.0, 'period': 0.5, 'color': '#E3DBCB'})],
        cams=[FC(0.0, [0.6, 1.5, 1.6], [[SITP[0], 2.3, SITP[2]], [r(SITP[0] + 0.4), 1.2, SITP[2]], [OUV[0], 2.45, OUV[2]], [OUV[0], 0.0, OUV[2]], [-1.35, 1.4, -1.15]], top=0.14, bottom=0.76)])   # (pass 2) him whole and the sign whole
st.cue('sfx:rattle', 'S09', 0.0, 0.9); st.cue('sfx:chainsaw', 'S09', 0.0, 0.9)

# 10: ...fifteen years. Close on the wall calendar: the years fly off page after page, 2007 to 2021, past the clock spinning above
D10 = st.dur('S10'); YEARS = [str(y) for y in range(2007, 2022)]
st.shot('S10', 'immeubleHall', setOpts=HALL(floor=[[0.0, '—']]), actors=[],
        props=[P('cal10', 'monthCalendar', pos=CAL, scale=1.3, opts={'months': YEARS, 'flipAt': 0.05, 'dur': r((D10 - 0.25) / len(YEARS))}), P('horloge10', 'wallClock', pos=CLK, scale=0.6, opts={'rate': 9.0})],
        cams=[FC(0.0, [-0.85, 1.95, -1.15], [[CAL[0], 1.97, CAL[2]], [CAL[0], 1.27, CAL[2]], [CLK[0], 2.82, CLK[2]], [CLK[0] - 0.25, 2.6, CLK[2]], [CLK[0] + 0.25, 1.3, CLK[2]]], top=0.12, bottom=0.78, lenses=range(20, 56))])
st.cue('sfx:paper', 'S10', 0.05, 1.0)

# 11: he grew old in front of the button. Old now: white beard to his lap, glasses, a walking stick, cobwebs; slowly he turns his head to the button
D11 = st.dur('S11')
st.shot('S11', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), actors=[act('vieux', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0),
            k(0.45, look=BTN, lookDur=0.9), k(1.2, toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.15), k(1.4, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.15)])],
        props=[BUTTON('bt11', litAfter=0.0), CHAIR('fauteuil11'), BEARD('barbe11', who='vieux', s=1.25), SPECS('lun11', who='vieux'), STICK('canne11', who='vieux'), *WEBS('toile11'),
               P('plaid11', 'blanketDrape', pos=[SITP[0], 0.72, SITP[2] + 0.38], opts={'w': 0.75, 'h': 0.42})],
        cams=[FC(0.0, [1.15, 1.6, 0.3], [[SITP[0], 2.2, SITP[2]], [SITP[0], 0.9, SITP[2]], [BTN[0], 1.25, BTN[2]], [CH[0] + 0.45, 1.3, CH[2]]], top=0.16, bottom=0.74, drift=(0.0, 0.0, -0.25))])

# 12: the button is a listed monument. Close on it: a museum spotlight, a bronze plaque under it, the velvet rope in front
D12 = st.dur('S12')
st.shot('S12', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), actors=[act('vieux', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look=BTN), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[BUTTON('bt12', litAfter=0.0), P('plaque12', 'bronzePlaque', pos=[BTN[0], 0.82, BACK + 0.04], scale=0.8, opts={'text': "BOUTON D'APPEL/2006"}),
               P('spot12', 'lightCone', pos=[BTN[0], 3.3, BACK + 0.3], opts={'h': 2.4, 'r': 0.34, 'opacity': 0.07}), P('cordon12', 'stanchions', pos=[BTN[0], 0, BACK + 0.75], opts={'w': 1.0}), CHAIR('fauteuil12')],
        cams=[FC(0.0, [0.8, 1.05, -1.6], [[BTN[0], 1.34, BTN[2]], [BTN[0], 0.66, BTN[2]], [BTN[0] - 0.26, 1.0, BTN[2]], [BTN[0] + 0.26, 1.0, BTN[2]]], top=0.22, bottom=0.72, lenses=range(18, 50))])   # (stills 1) centred on the button and the plaque (a wide frame put the cone over it and cut the chair)
st.cue('sfx:choir', 'S12', 0.0, 0.8)

# 13: ...historic. Wider: the button roped off under the spotlight like a museum piece, the old man beside it like its guard
D13 = st.dur('S13')
st.shot('S13', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), actors=[act('vieux', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(0.47, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.1),   # (pass 2) a slow blink...
            k(0.7, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.3), k(1.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.3), k(1.1, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.22, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.1)])],
        props=[BUTTON('bt13', litAfter=0.0), P('plaque13', 'bronzePlaque', pos=[BTN[0], 0.82, BACK + 0.04], scale=0.8, opts={'text': "BOUTON D'APPEL/2006"}),
               P('spot13', 'lightCone', pos=[BTN[0], 3.3, BACK + 0.45], opts={'h': 2.3, 'r': 0.42}), P('cordon13', 'stanchions', pos=[BTN[0], 0, BACK + 0.75], opts={'w': 1.0}),
               CHAIR('fauteuil13'), BEARD('barbe13', who='vieux', s=1.25), SPECS('lun13', who='vieux'), STICK('canne13', who='vieux'), *WEBS('toile13')],
        cams=[FC(0.0, [-0.3, 1.8, 1.6], [[SITP[0], 2.2, SITP[2]], [BTN[0], 3.3, BACK + 0.45], [BTN[0] - 0.5, 0.0, BACK + 0.75], [CH[0] + 0.45, 0.0, CH[2]], [DISP[0], 2.6, DISP[2]]], top=0.12, bottom=0.78)])

# 14: schools come to visit it. A teacher shows the button to a line of children; one reaches over the rope to press it; the old man's walking stick
#     taps his hand away
D14 = st.dur('S14'); TAP = 0.9; KIDS = [('eleve1', 0.55, -1.75), ('eleve2', 0.05, -1.35), ('eleve3', -0.45, -1.05)]
st.shot('S14', 'immeubleHall', setOpts=HALL(floor=[[0.0, '6']]), actors=[act('vieux', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look=[0.55, 1.3, -1.75]), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(r(TAP - 0.2), toon={'reach': {'R': [0.95, 1.25, -2.1, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.7}}, toonDur=0.12, toonEase='out'),
            k(r(TAP + 0.2), toon={'reach': {'R': [1.25, 0.9, -2.2, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {**OLD, 'mouth': 'line'}}, toonDur=0.25), k(r(TAP + 0.35), look='camera')]),
        act('maitresse', [-0.85, 0, -1.9], 60, 'point', 'happy', keys=[k(0.0, look=BTN)]),
        *[act(kid, [kx, 0, kz], 160 if j else 150, 'stand', 'happy', keys=[k(0.0, look=BTN)] + ([k(0.5, toon={'reach': {'R': [0.9, 1.1, -2.6, 1, 0.04]}, 'hands': {'R': 'point'}}, toonDur=0.3, toonEase='out'),
            k(TAP, toon={'reach': {'R': [0.75, 0.95, -2.2, 1, 0.04]}, 'hands': {'R': 'open'}, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O'}}, toonDur=0.06, toonEase='out'),
            *[k(r(TAP + 0.1 + 0.07 * i_), toon={'reach': {'R': [r(0.5 + (0.06 if i_ % 2 else -0.06)), 1.15, -1.9, 1, 0.04]}, 'hands': {'R': 'open'}, 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05) for i_ in range(6)]] if j == 0 else   # (pass 2) the hand snaps back and shakes (it stayed out)
            [k(r(0.3 + 0.2 * j), look=[0.55, 1.4, -1.75], lookDur=0.2), k(r(TAP + 0.1), toon={'face': {'lid': 0.0, 'mouth': 'O'}}, toonDur=0.08)])) for j, (kid, kx, kz) in enumerate(KIDS)]],
        props=[BUTTON('bt14', litAfter=0.0), P('plaque14', 'bronzePlaque', pos=[BTN[0], 0.82, BACK + 0.04], scale=0.8, opts={'text': "BOUTON D'APPEL/2006"}),
               P('cordon14', 'stanchions', pos=[BTN[0], 0, BACK + 0.75], opts={'w': 1.0}), CHAIR('fauteuil14'), BEARD('barbe14', who='vieux', s=1.25), SPECS('lun14', who='vieux'), STICK('canne14', who='vieux')],
        cams=[FC(0.0, [2.6, 1.55, 1.0], [[SITP[0], 2.2, SITP[2]], [-0.85, 2.45, -1.9], [-0.45, 1.8, -1.05], [0.55, 1.8, -1.75], [-0.45, 0.0, -1.05]], top=0.14, bottom=0.76)])
st.cue('sfx:bonk', 'S14', TAP, 0.3)

# 15: yesterday... The floor display at last shows RC; a ding; the old man's head snaps up
D15 = st.dur('S15'); RC = 0.35
st.shot('S15', 'immeubleHall', setOpts=HALL(floor=[[0.0, '2'], [0.18, '1'], [RC, 'RC']]), actors=[act('vieux', SITP, 0, 'sit', 'neutral', keys=[k(0.0, look=[0.5, 1.0, -1.0]), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(r(RC + 0.05), look=DISP, lookDur=0.08), k(r(RC + 0.05), toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'brow': 0.8}, 'sq': [1.16, 0.84, 1.16]}, toonDur=0.05, toonEase='out'),   # (pass 2) squashed...
            k(r(RC + 0.12), toon={'face': {'lid': 0.0, 'eye': 0.9, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.86, 1.22, 0.86]}, toonDur=0.06, toonEase='out'), k(r(RC + 0.12), to=[SITP[0], 0.16, SITP[2]], dur=0.07, glide=True, face='keep'),   # ...stretched up out of the chair, eyes wide...
            k(r(RC + 0.5), toon={'face': {'lid': 0.0, 'eye': 0.6, 'mouth': 'O', 'brow': 1.0}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.15), k(r(RC + 0.5), to=SITP, dur=0.15, glide=True, face='keep')])],   # ...held, then settled
        props=[BUTTON('bt15', litAfter=0.0), CHAIR('fauteuil15'), BEARD('barbe15', who='vieux', s=1.25, swing=[r(RC + 0.08), r(RC + 0.5), 0.25]), SPECS('lun15', who='vieux'), STICK('canne15', who='vieux')],
        cams=[FC(0.0, [-0.75, 1.3, -1.05], [[DISP[0], 2.58, DISP[2]], [DISP[0], 2.22, DISP[2]], [SITP[0], 2.25, SITP[2]], [SITP[0], 1.5, SITP[2]], [r(SITP[0] + 0.28), 1.95, SITP[2]], [r(SITP[0] + 0.5), 2.45, SITP[2]]], top=0.16, bottom=0.72, lenses=range(24, 64))])   # (stills 1) his whole head (it was cut at the edge); (pass 2) room for the stretch
st.cue('sfx:ding', 'S15', RC, 0.5)

# 16: ...the doors opened. Wide: the doors slide apart onto the lit car; he grips his stick, beard trembling
D16 = st.dur('S16'); OPEN = 0.15
st.shot('S16', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=[[0.0, 0.0], [OPEN, 0.0], [r(OPEN + 0.7), 1.0]]), actors=[act('vieux', SITP, -15, 'sit', 'neutral', keys=[k(0.0, look=[0.0, 1.5, ZF]),
            k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.0), *[k(r(0.2 + 0.08 * j), toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0}, 'sq': [1.0, 1.01 if j % 2 else 0.99, 1.0]}, toonDur=0.04) for j in range(10)]])],
        props=[BUTTON('bt16', litAfter=0.0), CHAIR('fauteuil16'), BEARD('barbe16', who='vieux', s=1.25, swing=[0.2, 1.0, 0.12]), SPECS('lun16', who='vieux'), STICK('canne16', who='vieux'),
               ],
        cams=[FC(0.0, [1.0, 1.55, 2.6], [[0.0, 2.6, ZF], [-0.6, 0.0, ZF], [SITP[0], 2.2, SITP[2]], [SITP[0], 0.0, SITP[2] + 0.4]], top=0.14, bottom=0.72, drift=(0.0, 0.0, -0.3))])
st.cue('sfx:slideUp', 'S16', OPEN, 0.6)

# 17: inside there was a man. In the doorway: an old man with a white beard in an armchair just like his, a blanket, cobwebs; he blinks at us
D17 = st.dur('S17'); AUT = [0.0, 0, BACK - 0.62]   # (pass 2) inside the car
st.shot('S17', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=[[0.0, 1.0]]), actors=[act('autre', [AUT[0], 0, AUT[2] + 0.08], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.5, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.15), k(0.78, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.15), k(1.1, look=[SITP[0], 2.0, SITP[2]], lookDur=0.4)])],   # (pass 2) a slow blink at us, shut four frames
        props=[P('fauteuil17', 'armchair', pos=AUT, opts={'color': '#B5523A'}), BEARD('barbe17', who='autre', s=1.25), SPECS('lun17', who='autre'), STICK('canne17', who='autre'),
               P('plaid17', 'blanketDrape', pos=[AUT[0], 0.72, AUT[2] + 0.46], opts={'w': 0.75, 'h': 0.42, 'color': PLAID}), P('toile17', 'cobweb', pos=[-0.5, 1.9, BACK - 0.2], ry=0, opts={'s': 0.7}),
               P('toile17b', 'cobweb', pos=[0.62, 1.15, AUT[2] + 0.1], ry=-90, opts={'s': 0.55})],   # (pass 2) the same red armchair and blanket as his, chunky cobwebs
        cams=[FC(0.0, [0.3, 1.5, -0.3], [[AUT[0], 2.25, AUT[2]], [AUT[0], 0.0, AUT[2] + 0.3], [-0.6, 2.2, ZF], [0.6, 2.2, ZF]], top=0.14, bottom=0.76, drift=(0.0, 0.0, -0.2))])

# 18: he had been waiting for the ground floor... Close on the car's panel beside him: his finger still on the lit RC button, dusty, a cobweb in the corner
D18 = st.dur('S18'); PAN = [-0.76, 1.2, BACK - 0.35]; AUT18 = [-0.12, 0, BACK - 0.62]   # (pass 2) the panel on the car's left wall beside him, seen from inside the car
st.shot('S18', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=[[0.0, 1.0]]), actors=[act('autre', [AUT18[0], 0, AUT18[2] + 0.08], 0, 'sit', 'neutral', keys=[k(0.0, look=PAN), k(0.65, look='camera', lookDur=0.25),
            k(0.0, toon={'reach': {'R': [PAN[0] + 0.04, PAN[1] - 0.2, PAN[2] + 0.04, 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.8, toon={'reach': {'R': [PAN[0] + 0.05, PAN[1] - 0.2, PAN[2] + 0.05, 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {**OLD, 'mouth': 'line'}}, toonDur=0.4, toonEase='inOut')])],
        props=[P('fauteuil18', 'armchair', pos=AUT18, opts={'color': '#B5523A'}), BEARD('barbe18', who='autre', s=1.25), SPECS('lun18', who='autre'),
               P('panneau18', 'liftPanel', pos=PAN, ry=90, opts={'lit': 'RC', 'dusty': True}), P('toile18', 'cobweb', pos=[r(PAN[0] + 0.03), r(PAN[1] - 0.02), r(PAN[2] + 0.1)], ry=90, opts={'s': 0.3})],
        cams=[FC(0.0, [0.3, 1.25, BACK - 0.2], [[PAN[0], 1.42, PAN[2]], [PAN[0], 0.92, PAN[2]], [PAN[0], 1.2, r(PAN[2] + 0.22)], [PAN[0], 1.2, r(PAN[2] - 0.22)]], top=0.2, bottom=0.7, lenses=range(18, 56)),
              glide([FC(0.55, [0.2, 1.55, -1.9], [[AUT18[0], 2.15, AUT18[2]], [AUT18[0], 1.3, AUT18[2]], [r(AUT18[0] - 0.3), 1.8, AUT18[2]], [r(AUT18[0] + 0.3), 1.8, AUT18[2]]], top=0.16, bottom=0.74, lenses=range(18, 56))], 0.45)])   # (stills 2) out through the doorway to his face (inside the car the door post filled the frame)   # (pass 2) the callback to S01: close on the finger on RC, then up to his face

# 19: ...for twenty years. The two old men face to face across the threshold, identical beards, identical armchairs, the same deadpan
D19 = st.dur('S19')
AUT19 = [-0.1, 0, BACK - 0.35]
st.shot('S19', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=[[0.0, 1.0]]), actors=[act('vieux', SITP, -30, 'sit', 'neutral', keys=[k(0.0, look=[AUT[0], 2.0, AUT[2]]), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.6, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(0.74, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.12)]),
        act('autre', [AUT19[0], 0, AUT19[2] + 0.08], 30, 'sit', 'neutral', keys=[k(0.0, look=[SITP[0], 2.0, SITP[2]]), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.6, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(0.74, toon={'face': {**OLD, 'mouth': 'line'}}, toonDur=0.12)])],   # (pass 2) three-quarters to us both, blinking together (two strict profiles hid both faces)
        props=[P('fauteuil19a', 'armchair', pos=CH, ry=-30, opts={'color': '#B5523A'}), P('fauteuil19b', 'armchair', pos=AUT19, ry=30, opts={'color': '#B5523A'}),
               BEARD('barbe19a', who='vieux', s=1.25), SPECS('lun19a', who='vieux'), BEARD('barbe19b', who='autre', s=1.25), SPECS('lun19b', who='autre'), BUTTON('bt19', litAfter=0.0)],
        cams=[FC(0.0, [0.68, 1.55, 0.9], [[SITP[0], 2.25, SITP[2]], [AUT19[0], 2.25, AUT19[2]], [SITP[0], 0.9, SITP[2] + 0.3], [AUT19[0], 0.9, AUT19[2] + 0.3]], top=0.18, bottom=0.74)])   # (pass 2) square on, between them

# 20: they shook hands. Standing side by side facing us, as for an official photo, the two old men shake hands; a flash
D20 = st.dur('S20'); M20, A20 = [0.75, 0, -1.55], [-0.15, 0, -1.55]
st.shot('S20', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=[[0.0, 1.0]]), actors=[act('vieux', M20, -10, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0),
            k(0.15, toon={'reach': {'R': [0.3, 1.25, -1.35, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.25, toonEase='out'),
            *[k(r(0.45 + 0.14 * j), toon={'reach': {'R': [0.3, 1.25 + (0.12 if j % 2 else -0.12), -1.35, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.12) for j in range(5)]]),
        act('autre', A20, 10, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0),
            k(0.15, toon={'reach': {'L': [0.3, 1.25, -1.35, 1, 0.04]}, 'hands': {'L': 'grip'}, 'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.25, toonEase='out'),
            *[k(r(0.45 + 0.14 * j), toon={'reach': {'L': [0.3, 1.25 + (0.12 if j % 2 else -0.12), -1.35, 1, 0.04]}, 'hands': {'L': 'grip'}, 'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.12) for j in range(5)]])],
        props=[BEARD('barbe20a', who='vieux', s=1.25), SPECS('lun20a', who='vieux'), STICK('canne20', who='vieux', hand='L'), BEARD('barbe20b', who='autre', s=1.25), SPECS('lun20b', who='autre'), BUTTON('bt20', litAfter=0.0),
               P('flash20', 'flashBursts', pos=[0.3, 1.8, 1.2], opts={'n': 1, 'w': 1.2, 'h': 1.2, 'at': [0.9]})],
        cams=[FC(0.0, [0.3, 1.2, 1.2], [[M20[0], 2.45, M20[2]], [A20[0], 2.45, A20[2]], [0.3, 1.1, -1.35], [M20[0], 0.9, M20[2]], [A20[0], 0.9, A20[2]]], top=0.16, bottom=0.74)],   # low and close, like the press photo
        fx=[{'type': 'flash', 'at': 0.9, 'dur': 0.14}])   # (pass 2) the flash over the whole frame (none of the draft's frames showed it)
st.cue('sfx:shutter', 'S20', 0.9, 0.4)

# 21: and they took the stairs. Wide: the two of them climb the stairs at the side of the hall, one step at a time, sticks first; behind them the lift
#     doors close with a ding; at the top step he looks back at us
D21 = st.dur('S21'); ST = [2.55, 0, -0.35]
def climb(x, z0, t0, n, step=0.42):
    out = []
    for i in range(n):
        out.append(k(r(t0 + i * step), to=[x, r(0.2 * (i + 1)), r(z0 - 0.28 * (i + 1))], dur=r(step * 0.8), ease='inOut', clip='walk', face='keep'))
    return out
st.shot('S21', 'immeubleHall', setOpts=HALL(floor=[[0.0, 'RC']], doors=[[0.0, 1.0], [0.6, 1.0], [1.3, 0.0]], plant=False), actors=[
        act('vieux', [2.25, 0, -0.1], 180, 'stand', 'neutral', keys=[*climb(2.25, -0.1, 0.0, 5), k(r(D21 - 0.75), look='camera', lookDur=0.25), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0)]),
        act('autre', [2.68, 0, 0.4], 180, 'stand', 'neutral', keys=[*climb(2.68, 0.4, 0.3, 5), k(0.0, toon={'face': {**OLD, 'mouth': 'line'}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.0)])],
        props=[P('escalier21', 'stairs', pos=ST, opts={'steps': 9, 'w': 1.1}), BEARD('barbe21a', who='vieux', s=1.25), SPECS('lun21a', who='vieux'), STICK('canne21a', who='vieux'), BEARD('barbe21b', who='autre', s=1.25), SPECS('lun21b', who='autre'),
               STICK('canne21b', who='autre'), BUTTON('bt21', litAfter=0.0)],
        cams=[FC(0.0, [0.2, 1.8, 2.4], [[2.25, 3.5, -1.3], [2.68, 0.0, 0.4], [2.25, 1.0, -0.1], [0.45, 2.3, ZF]], top=0.12, bottom=0.78)])   # (pass 2) closer: the beards, the sticks and the look back read; the doors at the left edge
st.cue('sfx:step', 'S21', 0.0, 0.2); st.cue('sfx:step', 'S21', 0.42, 0.2); st.cue('sfx:step', 'S21', 0.84, 0.2); st.cue('sfx:ding', 'S21', 1.3, 0.4)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("L'ascenseur", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'vieux': {'preset': 'lemec', 'tint': '#E6F2FF', 'hairColor': '#ECEAE4', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 2) the same man twenty years on: white hair
    'gris': {'preset': 'lemec', 'tint': '#E6F2FF', 'hairColor': '#8E8A84', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 2) greying, during the works
    'autre': {'preset': 'lemec', 'tint': '#E6F2FF', 'hairColor': '#ECEAE4', 'tie': '#2E7D5B', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 2) his mirror: the same man, only the tie differs (bald, grey and yellow he was another man)
    'mamie': {'preset': 'mamie', 'seed': 822, 'build': {'width': 0.95, 'headWidth': 1.22}, 'toon': EX},
    'concierge': {'preset': 'madame', 'seed': 823, 'suit': '#4F7AA8', 'build': {'width': 1.0, 'headWidth': 1.22}, 'toon': EX},
    'syndic': {'preset': 'boss', 'seed': 824, 'suit': '#2E3138', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'voisin1': {'preset': 'femme', 'seed': 825, 'build': {'width': 0.9, 'headWidth': 1.2}, 'toon': EX},
    'voisin2': {'preset': 'avocat', 'seed': 826, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'voisin3': {'preset': 'madame', 'seed': 827, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'ouvrier': {'preset': 'worker', 'seed': 828, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'maitresse': {'preset': 'femme', 'seed': 829, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.2}, 'toon': EX},
    **{kid: {'preset': 'gamin', 'seed': 830 + j, 'suit': ['#E8A33C', '#5BB5A8', '#E25C7A'][j], 'build': {'height': 0.58, 'width': 0.85, 'headScale': 1.3, 'headWidth': 1.2}, 'toon': EX} for j, kid in enumerate(['eleve1', 'eleve2', 'eleve3'])},   # (pass 2) children's size (85 % of the teacher, adult proportions)
})
