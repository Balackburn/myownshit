#!/usr/bin/env python3
"""Le service client (story 73, cycle 35; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man called customer service. They put him on hold. The hold music has been playing for ten years. He knows every note by heart. The phone
ended up stuck to his ear. The firemen moved house with him. He got married on hold. His wife said yes on the speaker. The music became the national
anthem. The band played it at the parade. The children whistle it at school. Yesterday someone picked up. He cried for joy, live on television. The
voice said: for an adviser, press one. He pressed one. The music started again.
Staging: his living room, the phone to his ear, notes pouring out of it; a wall calendar flipping ten years; he conducts along with a finger, eyes
shut; he tries to put the phone down and it stays, his head pulled sideways with it; two firemen carry him down the street on his sofa; the town
hall wedding, the bride's yes into his phone; the flag rising at a ceremony while the anthem pours out of his phone; the parade band; a classroom
whistling it; the music stops: a take; tears of joy; TV cameras; the keypad, the finger on 1; the notes come back; a look at us.
Natural look; cycle 35: props_conseiller.js (holdNotes, brass, bridalVeil, flagPole, phoneKeypad), props reused (smartPhone, yearCalendar, sofaProp,
tearFountain, tvCamera, pressMic, hicBurst, flag, signBoard).
Pass 2 (review 1: 5.4 / 5.4): the phone is one big red handset (bigPhone), stuck flat on his LEFT ear, the ear on the side of the lens, held by his left
hand up to S05 and hanging there by itself from S07 to S17 (the old one sat in a fist in front of his chin: the right hand crossed over to the left
side of the face); the notes are bigger, edged in white and come out of the phone; the pull of S07 doubles the width of his head, the take of S06 and
the pop of S18 are played in full; the calendar tears its pages off; the escalation is restaged shot by shot (sofa carried face on, the yes in
profile, him in front of the flag, tuba and drum in the front rank, the children facing us); the 1 is pressed by one finger and stays green."""
from story_kit import *
import math

st = Story('conseiller', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L03', 3), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L05', 5),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L09', 0), ('S12', 'L10', 0), ('S13', 'L11', 0), ('S14', 'L12', 0),
         ('S15', 'L13', 0), ('S16', 'L13', 5), ('S17', 'L14', 0), ('S18', 'L14', 5), ('S19', 'L15', 0), ('S20', 'L16', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
OLD = 'mecVieux'                                     # him ten years on (from S14): grey hair, bags under the eyes
LR = {'pictureX': 2.3, 'pictureW': 1.0, 'pictureY': 2.5, 'carpet': False}   # (pass 2) his living room: the painting off to the right (the notes rose over it), no red rug (the captions sat on it)
ME = [0.0, 0, -1.0]                                  # him standing in his living room, facing us
SIT = [0.0, 0, -2.8]                                 # him on his sofa
# (pass 2) the phone, in the frame of his head (+X his left, +Y up from the collar, +Z his face; the head is 0.24 wide, 0.5 tall, 0.17 deep): on his left
# ear, its back turned 30 degrees to the front (flat on the ear it is a red edge from the front), or held in front of his chest, the screen to us
EAR = ([0.19, 0.25, 0.0], [-0.2, r(math.radians(-120)), 0.0])
FRONT = ([0.14, -0.4, 0.42], [-0.2, 0.0, 0.0])
GRIP = ['head', 0.27, 0.14, 0.045, 1, 0.02, [1, -0.5, 0.0]]      # his left hand on the lower half of the phone at his ear, the elbow out
FGRIP = ['head', 0.14, -0.53, 0.37, 1, 0.02, [1, -0.8, -0.2]]    # the same hand under the phone held in front of him
TAP0 = ['head', 0.0, -0.42, 0.64, 1, 0.1, [-1, -0.6, 0.3]]; TAP1 = ['head', 0.12, -0.36, 0.5, 1, 0.1, [-1, -0.6, 0.3]]   # the other index over the screen, on it
def eio(u): return 2 * u * u if u < 0.5 else 1 - 2 * (1 - u) * (1 - u)
def MIX(a, b, u): return [a[0], *[r(a[i] + (b[i] - a[i]) * u) for i in (1, 2, 3)], 1, 0.02, [r(a[6][i] + (b[6][i] - a[6][i]) * u) for i in range(3)]]
def CARRY(who, t0, dur, a, b):
    """The phone carried from one place of the head's frame to another: one attach key per frame (the offset of an attach is fixed), on the ease of a
    toon key (toonEase 'inOut' over the same time), so the hand that touches the same frame stays on it."""
    n = max(2, int(round(dur * 30)))
    return [k(r(t0 + dur * i / n), attach=who, joint='head', offset=[r(a[0][j] + (b[0][j] - a[0][j]) * eio(i / n)) for j in range(3)], rot=[r(a[1][j] + (b[1][j] - a[1][j]) * eio(i / n), 4) for j in range(3)]) for i in range(1, n + 1)]
def TEL(pid, who='mec', start=EAR, keys=None, **o): return P(pid, 'bigPhone', on={'actor': who, 'joint': 'head', 'offset': start[0], 'rot': start[1]}, keys=keys or [], opts=o)
def NOTES(pid, actor='mec', t0=0.0, t1=99.0, rate=3.5, size=0.12, off=None, **o):
    return P(pid, 'holdNotes', on={'actor': actor, 'joint': 'head', 'offset': off or [0.3, 0.42, 0.02], 'face': 'camera'}, opts={'from': t0, 'until': t1, 'rate': rate, 'size': size, 'side': 1, **o})
def HOLD(f=None, extra=None): return {'touch': {'L': GRIP}, 'hands': {'L': 'grip'}, 'face': f or {**DEAD, 'mouth': 'line'}, **(extra or {})}   # the phone held to his ear
def FREE(f=None, extra=None): return {'face': f or {**DEAD, 'mouth': 'line'}, **(extra or {})}                                           # the phone on his ear by itself, both hands free
def SHOW(f, tap=None, extra=None): return {'touch': {'L': FGRIP, **({'R': tap} if tap else {})}, 'hands': {'L': 'grip', 'R': 'point'}, 'face': f, **(extra or {})}   # the phone held in front of him
def BL(t, f, d=0.1): return [k(t, toon={'face': {**f, 'lid': 1.0}}, toonDur=0.06, keepPose=True), k(r(t + d), toon={'face': f}, toonDur=0.08, keepPose=True)]   # a blink that keeps the arms
def FK(t, f, dur=0.08, **kw): return k(t, toon={'face': f}, toonDur=dur, keepPose=True, **kw)                                           # the face alone changes

for g_ in [('S07', 0.5, 'mec', 'stuck'), ('S10', 1.0, 'femme', 'oui'), ('S11', 1.2, 'mec', 'anthem'), ('S14', 0.85, OLD, 'click'), ('S15', 0.6, OLD, 'tears'), ('S20', 1.3, OLD, 'end')]:
    st.gag(*g_)
st.card('S04', 'DIX ANS', at=0.3)
st.card('S11', 'HYMNE', at=0.6)
st.card('S19', 'UN', at=0.55)

# 1: the hook. His living room: the big red phone in his hand, he taps it once, lifts it to his ear and looks at us, deadpan
D1 = st.dur('S01'); LIFT1 = 0.5; F1 = {'lid': 0.3, 'mouth': 'line', 'gy': 0.7}; ME1 = [0.4, 0, -1.0]   # (stills 2) a step to his left: the sofa's red cushion sat right behind his free hand, a second red thing in the hook
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', ME1, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SHOW(F1, TAP0), toonDur=0.0),
            k(0.12, toon=SHOW(F1, TAP1), toonDur=0.07, toonEase='in'), k(0.26, toon=SHOW(F1, TAP0), toonDur=0.1),                       # he dials: one tap
            k(LIFT1, toon=HOLD({'lid': 0.3, 'mouth': 'line'}), toonDur=0.3, toonEase='inOut'),                                           # the phone goes up to his ear
            k(r(LIFT1 + 0.31), toon=HOLD({'lid': 0.3, 'mouth': 'line'}, {'sq': [1.03, 0.96, 1.03]}), toonDur=0.05), k(r(LIFT1 + 0.38), toon=HOLD(), toonDur=0.12),   # it lands: a little settle
            FK(1.08, {'lid': 0.3, 'mouth': 'line', 'gx': 0.8}, 0.1), FK(1.3, {**DEAD, 'mouth': 'line'}, 0.1),                               # a glance at the phone while it rings, and back to us
            *BL(1.55, {**DEAD, 'mouth': 'line'})])],
        props=[TEL('tel1', start=FRONT, keys=CARRY('mec', LIFT1, 0.3, FRONT, EAR))],
        cams=[FC(0.0, [1.65, 1.55, 1.3], [[ME1[0], 2.42, ME1[2]], [ME1[0], 1.0, ME1[2]], [r(ME1[0] + 0.55), 2.0, ME1[2]], [r(ME1[0] - 0.4), 2.0, ME1[2]], [r(ME1[0] + 0.2), 1.4, r(ME1[2] + 0.5)]], top=0.14, bottom=0.74)])   # (pass 2) from his left, three quarters: the phone side
st.cue('sfx:click', 'S01', 0.14, 0.15); st.cue('sfx:ring', 'S01', 0.9, 0.12)

# 2: they put him on hold. Close: a click, and the hold music pours out of the phone; his eyes go to it, then follow the notes up
D2 = st.dur('S02')
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0),
            k(0.2, toon=HOLD(extra={'sq': [1.03, 0.96, 1.03]}), toonDur=0.04), k(0.26, toon=HOLD(), toonDur=0.1),                         # the click: a start
            k(0.42, toon=HOLD({'lid': 0.2, 'mouth': 'line', 'gx': 0.9, 'brow': 0.4}), toonDur=0.1),                                       # his eyes go to the phone...
            k(0.8, toon=HOLD({'lid': 0.4, 'mouth': 'line', 'gx': 0.5, 'gy': -0.7}), toonDur=0.25, toonEase='inOut')])],                   # ...and follow the notes up
        props=[TEL('tel2'), NOTES('mus2', t0=0.3, rate=4.0, size=0.13)],
        cams=[FC(0.0, [0.75, 1.95, 0.75], [[ME[0], 2.42, ME[2]], [ME[0], 1.6, ME[2]], [0.8, 2.75, ME[2]], [-0.3, 2.0, ME[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:click', 'S02', 0.2, 0.2); st.cue('sfx:ding', 'S02', 0.32, 0.12)

# 3: the hold music... Wider: he stands in front of his sofa, the phone at his ear, notes rising; a calendar on the wall: he glances at it
D3 = st.dur('S03'); CAL = [-0.7, 2.0, -3.55]; H3 = [0.35, 0, -2.2]
st.shot('S03', 'livingRoom', setOpts=LR, actors=[act('mec', H3, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0),
            k(0.3, toon=HOLD({'lid': 0.3, 'mouth': 'line', 'gx': -0.9}), toonDur=0.12), k(0.3, look=[CAL[0], CAL[1], CAL[2]]),          # a look at the calendar: the cut goes there
            *BL(0.72, {'lid': 0.3, 'mouth': 'line', 'gx': -0.9})])],
        props=[TEL('tel3'), NOTES('mus3', rate=3.5, size=0.2), P('cal3', 'tearCalendar', pos=CAL, opts={'years': [2016, 2026], 'from': 99.0, 'land': 100.0})],
        cams=[FC(0.0, [1.1, 1.2, 1.5], [[H3[0], 2.45, H3[2]], [H3[0], 0.6, H3[2]], [r(CAL[0] - 0.35), 2.35, CAL[2]], [r(CAL[0] - 0.35), 1.6, CAL[2]], [0.95, 2.7, H3[2]]], top=0.12, bottom=0.82)])   # low: the floor is a strip, the band falls on the sofa

# 4: ...has been playing for ten years. Close on the calendar: its pages rip off and fly, faster and faster, 2016 to 2026, which lands and stays (DIX ANS)
D4 = st.dur('S04')
st.shot('S04', 'livingRoom', setOpts=LR, actors=[],
        props=[P('cal4', 'tearCalendar', pos=CAL, opts={'years': [2016, 2026], 'from': 0.06, 'land': 0.98})],
        cams=[FC(0.0, [r(CAL[0] + 0.25), r(CAL[1] - 0.1), r(CAL[2] + 1.3)], [[CAL[0], r(CAL[1] + 0.42), CAL[2]], [CAL[0], r(CAL[1] - 0.42), CAL[2]], [r(CAL[0] - 0.42), CAL[1], CAL[2]], [r(CAL[0] + 0.42), CAL[1], CAL[2]]], top=0.24, bottom=0.72)])
for t_ in (0.06, 0.3, 0.5, 0.66, 0.8): st.cue('sfx:paper', 'S04', t_, 0.2)
st.cue('thud', 'S04', 0.98, 0.2)

# 5: he knows every note by heart. Eyes shut, swaying, he conducts along with one finger of his free hand, mouthing the tune
D5 = st.dur('S05')
CND = lambda j: HOLD({'lid': 1.0, 'mouth': 'O' if j % 2 else 'line'}, {'reach': {'R': [r(-0.5 + 0.1 * math.sin(j * 1.7)), r(1.95 + (0.14 if j % 2 else -0.06)), r(ME[2] + 0.35), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'point'}, 'bend': {'neck': [0, 0, r(0.12 if j % 2 else -0.12), 1, None]}})
st.shot('S05', 'livingRoom', setOpts=LR, actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=CND(0), toonDur=0.0), *[k(r(0.1 + 0.3 * j), toon=CND(j + 1), toonDur=0.2, toonEase='inOut') for j in range(6)]])],
        props=[TEL('tel5'), NOTES('mus5', rate=4.0, size=0.13)],
        cams=[FC(0.0, [-0.15, 1.15, 1.6], [[ME[0], 2.45, ME[2]], [ME[0], 1.15, ME[2]], [-0.7, 2.2, r(ME[2] + 0.35)], [0.75, 2.6, ME[2]]], top=0.12, bottom=0.74)])   # face on, from low: the finger and the notes either side

# 6: the phone ended up... He goes to put the phone down: his hand opens and comes away, the phone stays on his ear; a beat; his eyes go to the empty
#    hand, to the phone, and a take to us
D6 = st.dur('S06'); HAND6 = [0.55, 1.4, r(ME[2] + 0.45)]
AWAY6 = lambda f: {'reach': {'L': [*HAND6, 1, 0.03]}, 'hands': {'L': 'open'}, 'face': f}
st.shot('S06', 'livingRoom', setOpts=LR, actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0),
            k(0.08, toon=AWAY6({**DEAD, 'mouth': 'line'}), toonDur=0.2, toonEase='out'),                                                  # the hand opens and leaves: the phone does not
            FK(0.42, {'lid': 0.2, 'mouth': 'line', 'gx': 0.7, 'gy': 0.85, 'brow': 0.3}),                                                  # his eyes: the empty hand...
            FK(0.6, {'lid': 0.1, 'mouth': 'line', 'gx': 1.0, 'gy': -0.1, 'brow': 0.6}),                                                   # ...the phone still up there...
            k(0.78, toon={**AWAY6({'lid': 0.0, 'eye': 0.45, 'pop': 0.3, 'popLen': 0.1, 'mouth': 'o', 'brow': 1.0}), 'sq': [0.95, 1.07, 0.95]}, toonDur=0.05, toonEase='out'),   # ...and us: a take
            k(0.92, toon={**AWAY6({'lid': 0.0, 'eye': 0.35, 'mouth': 'line', 'brow': 0.8, 'pupilShake': 0.5}), 'sq': [1.0, 1.0, 1.0]}, toonDur=0.12)])],
        props=[TEL('tel6'), NOTES('mus6', size=0.12)],
        cams=[FC(0.0, [0.8, 1.5, 1.6], [[ME[0], 2.45, ME[2]], [ME[0], 1.05, ME[2]], [0.75, 1.4, HAND6[2]], [-0.38, 2.0, ME[2]], [0.7, 2.6, ME[2]]], top=0.12, bottom=0.76)])

# 7: ...stuck to his ear. Close, face on: both hands on the phone, he pulls: his head is dragged out to twice its width after it, trembles there, and
#    snaps back when his grip slips; the phone has not moved
D7 = st.dur('S07')
def PULL(s, f, extra=None):   # s: the width of his head (1 = its own); the body tips that way so that the far side of the head stays where it was
    return {'touch': {'L': ['head', 0.27, 0.3, 0.045, 1, 0.02, [1, -0.3, 0.0]], 'R': ['head', 0.23, 0.0, 0.1, 1, 0.02, [-0.5, -1, 0.6]]}, 'hands': {'L': 'grip', 'R': 'grip'},
            'scl': {'head': [s, r(1 - 0.12 * (s - 1)), 1.0]}, 'lay': [0, r(-0.063 * (s - 1))], 'face': f, **(extra or {})}
LOOSE7 = lambda s, sy, f: {'reach': {'L': [0.75, 1.5, r(ME[2] + 0.2), 1, 0.03], 'R': [-0.7, 1.5, r(ME[2] + 0.2), 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'scl': {'head': [s, sy, 1.0]}, 'lay': [0, r(-0.063 * (s - 1))], 'face': f}
STRAIN = {'lid': 0.15, 'mouth': 'clench', 'brow': -0.8, 'sweat': 1.0, 'tremble': 1.0, 'pupilShake': 1.0}
st.shot('S07', 'livingRoom', setOpts=LR, actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=PULL(1.0, {'lid': 0.3, 'mouth': 'clench', 'brow': -0.6}), toonDur=0.0),
            k(0.0, toon=PULL(0.86, {'lid': 0.4, 'mouth': 'clench', 'brow': -0.7}), toonDur=0.1, toonEase='inOut'),                        # the anticipation: he pushes it in...
            k(0.12, toon=PULL(2.0, STRAIN), toonDur=0.14, toonEase='out'),                                                               # ...and pulls: twice the width
            *[k(r(0.3 + 0.066 * j), toon=PULL(2.1 if j % 2 else 1.94, STRAIN), toonDur=0.05, toonEase='linear') for j in range(5)],      # it trembles there
            k(0.63, toon=PULL(2.25, {**STRAIN, 'mouth': 'grimace'}), toonDur=0.1, toonEase='in'),                                        # one more heave
            k(0.76, toon=LOOSE7(0.76, 1.2, {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}), toonDur=0.05, toonEase='out'),          # his grip slips: the head snaps back too far...
            k(0.85, toon=LOOSE7(1.14, 0.93, {'lid': 0.0, 'eye': 0.4, 'mouth': 'o', 'brow': 0.8}), toonDur=0.07),
            k(0.94, toon=LOOSE7(0.94, 1.04, {'lid': 0.2, 'mouth': 'wavy', 'brow': 0.3, 'cross': 0.5}), toonDur=0.07),
            k(1.03, toon=FREE({'lid': 0.3, 'mouth': 'wavy', 'cross': 0.3}, {'scl': {'head': [1.0, 1.0, 1.0]}, 'lay': [0, 0]}), toonDur=0.1),   # ...wobbles, and is a head again
            FK(1.2, {'lid': 0.2, 'mouth': 'line', 'gx': 1.0}, 0.1),                                                                      # a look at the phone: still there
            *BL(1.34, {**DEAD, 'mouth': 'line', 'gx': 0.6})])],
        props=[TEL('tel7'), NOTES('mus7', size=0.12)],
        cams=[FC(0.0, [0.3, 1.95, 1.3], [[ME[0], 2.5, ME[2]], [ME[0], 1.5, ME[2]], [0.85, 2.05, ME[2]], [-0.45, 2.05, ME[2]]], top=0.14, bottom=0.74)])
st.cue('sfx:stretch', 'S07', 0.12, 0.25); st.cue('sfx:stretch', 'S07', 0.6, 0.25); st.cue('sfx:boing', 'S07', 0.76, 0.25)

# 8: the firemen moved house with him. Down the street, toward us: two firemen carry his sofa on two poles at chest height, like a sedan chair; he
#    sits on it above their heads, the phone on his ear by itself, bobbing a little late on their steps, notes rising behind
D8 = st.dur('S08'); X8 = 3.6; Z8 = 2.6; V8 = 1.0; Y8 = 1.4; S8 = 0.7; ZE8 = r(Z8 - V8 * D8); HY8 = r(Y8 + 0.56 * S8 - 0.56)
CARRY8 = lambda x, z: {'reach': {'R': [x, r(Y8 - 0.04), r(z - 0.28), 1, 0.04], 'L': [x, r(Y8 - 0.04), r(z + 0.28), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4, 'sweat': 0.6}}
st.shot('S08', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', [X8, HY8, Z8], 180, 'sit', 'neutral', keys=[k(0.0, to=[X8, HY8, ZE8], dur=D8, ease='linear'), k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0),
            *[k(r(0.14 + 0.24 * j), toon=FREE(extra={'sq': [1.04, 0.92, 1.04] if j % 2 == 0 else [0.97, 1.06, 0.97]}), toonDur=0.12, toonEase='inOut') for j in range(7)],   # he bobs, half a beat after their steps
            *BL(1.1, {**DEAD, 'mouth': 'line'})]),
        *[act(fid, [r(X8 + dx), 0, Z8], 180, 'walk', 'determined', keys=[k(0.0, to=[r(X8 + dx), 0, ZE8], dur=D8, clip='walk', ease='linear'),
            k(0.0, toon=CARRY8(r(X8 + dx), Z8), toonDur=0.0), k(0.001, toon=CARRY8(r(X8 + dx), ZE8), toonDur=D8, toonEase='linear')])
          for fid, dx in [('pomp1', -1.15), ('pomp2', 1.15)]]],
        props=[P('canape8', 'sofaProp', pos=[X8, Y8, Z8], ry=180, scale=S8, keys=[k(0.0, to=[X8, Y8, ZE8], dur=D8, ease='linear')]),
               *[P(f'perche8{j}', 'slab', pos=[X8, r(Y8 - 0.04), r(Z8 + dz)], opts={'w': 2.9, 'h': 0.07, 'd': 0.07, 'color': '#8A5A30', 'outline': 0.005}, keys=[k(0.0, to=[X8, r(Y8 - 0.04), r(ZE8 + dz)], dur=D8, ease='linear')]) for j, dz in enumerate((-0.28, 0.28))],
               TEL('tel8'), NOTES('mus8', size=0.32, rate=3.0, dy=0.8, dx=0.35, sway=0.08)],
        cams=[FC(0.0, [r(X8 + 0.6), 1.0, r(ZE8 - 4.6)], [[X8, r(HY8 + 1.9), ZE8], [r(X8 - 1.5), 0.1, ZE8], [r(X8 + 1.5), 0.1, ZE8], [r(X8 + 0.8), r(HY8 + 2.3), ZE8]], top=0.1, bottom=0.82)])   # (pass 2) face on, low
st.cue('sfx:stepSoft', 'S08', 0.3, 0.15); st.cue('sfx:stepSoft', 'S08', 0.8, 0.15); st.cue('sfx:stepSoft', 'S08', 1.3, 0.15)

# 9: he got married on hold. The town hall: the mayor in his sash reads from the register; the bride in her veil beside him; the phone on his ear by
#    itself, his hands free, notes rising over the wedding
D9 = st.dur('S09'); BR = [0.5, 0, 0.3]; GR = [-0.5, 0, 0.3]; MA = [0.0, 0, -1.55]; MAIRIE = {'map': False, 'bannerY': 3.25, 'plate': False}
BOUQ = {'touch': {'R': ['torso', 0.05, 0.4, 0.3, 1, 0.02], 'L': ['torso', -0.05, 0.4, 0.3, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
READ9 = lambda j: {'reach': {'R': [0.15, 1.35, r(MA[2] + 0.4), 1, 0.04], 'L': [-0.15, 1.35, r(MA[2] + 0.4), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'open' if j % 2 else 'line'}}
st.shot('S09', 'mairie', setOpts=MAIRIE, actors=[
        act('mec', GR, 5, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0), *BL(1.05, {**DEAD, 'mouth': 'line'}, 0.16)]),
        act('femme', BR, -5, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={**BOUQ, 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.0), k(0.5, look=[r(GR[0] + 0.25), 2.05, GR[2]]),
            k(0.55, toon={**BOUQ, 'face': {'lid': 0.1, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.1), k(1.15, look='camera'), k(1.15, toon={**BOUQ, 'face': {'lid': 1.0, 'mouth': 'bigsmile'}}, toonDur=0.12)]),   # a look at the phone on his ear, and she beams
        act('maire', MA, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.35, r(MA[2] + 0.4)]), k(0.0, toon=READ9(1), toonDur=0.0), *[k(r(0.15 + 0.22 * j), toon=READ9(j), toonDur=0.1) for j in range(6)], k(1.2, look=[GR[0], 2.1, GR[2]])])],
        props=[TEL('tel9'), NOTES('mus9', size=0.2, rate=3.5), P('voile9', 'bridalVeil', on={'actor': 'femme', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}), P('bouq9', 'bouquet', on={'actor': 'femme', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}),
               P('reg9', 'paperSheet', on={'actor': 'maire', 'hand': 'R', 'offset': [0.0, 0.0, 0.03], 'face': 'camera'}, opts={'w': 0.3, 'h': 0.22, 'lines': ['REGISTRE']})],
        cams=[FC(0.0, [0.0, 1.5, 4.3], [[r(GR[0] - 0.45), 0.15, GR[2]], [r(BR[0] + 0.5), 0.15, BR[2]], [0.0, 3.55, -2.55], [r(GR[0] - 0.45), 2.4, GR[2]], [r(BR[0] + 0.5), 2.4, BR[2]]], top=0.08, bottom=0.82)])   # (pass 2) both of them whole, the banner over them
st.cue('sfx:bell', 'S09', 0.2, 0.2)

# 10: his wife said yes on the speaker. In profile, she leans to the phone on his ear and says it into it: OUI !; he does not move; behind his
#     shoulder the mayor claps
D10 = st.dur('S10'); OUI10 = 0.75; BR10 = [0.27, 0, 0.2]; MA10 = [-1.12, 0, -1.2]   # (stills 2) she stands three quarters to us: in profile a box head shows no mouth
LEAN10 = lambda b, f, sq=None: {**BOUQ, 'bend': {'spine': [b, 0, 0, 1, None]}, 'face': f, **({'sq': sq} if sq else {})}
CLAP10 = lambda j: {'touch': {'R': ['torso', r(-0.03 if j % 2 else -0.16), 0.52, 0.3, 1, 0.04], 'L': ['torso', r(0.03 if j % 2 else 0.16), 0.52, 0.3, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}
st.shot('S10', 'mairie', setOpts=MAIRIE, actors=[
        act('mec', GR, 5, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0), FK(r(OUI10 + 0.1), {'lid': 0.3, 'mouth': 'line', 'gx': 0.8}), FK(r(OUI10 + 0.55), {**DEAD, 'mouth': 'line'}, 0.12),
            *BL(1.7, {**DEAD, 'mouth': 'line'})]),                                                                                       # one look aside at the yes, and back to us
        act('femme', BR10, -45, 'stand', 'happy', keys=[k(0.0, look=[-1.6, 1.8, 3.0]), k(0.0, toon=LEAN10(0.0, {'lid': 0.2, 'mouth': 'smile'}), toonDur=0.0),
            k(0.15, toon=LEAN10(0.42, {'lid': 0.2, 'mouth': 'smile'}), toonDur=0.4, toonEase='inOut'),                                    # she leans to the phone...
            k(r(OUI10 - 0.12), toon=LEAN10(0.36, {'lid': 0.6, 'mouth': 'o'}, [1.04, 0.95, 1.04]), toonDur=0.1),                           # ...takes a breath...
            k(OUI10, toon=LEAN10(0.46, {'lid': 0.0, 'mouth': 'scream', 'brow': 0.8}, [0.95, 1.07, 0.95]), toonDur=0.05, toonEase='out'),  # ...OUI !
            k(r(OUI10 + 0.5), toon=LEAN10(0.3, {'lid': 0.1, 'mouth': 'bigsmile'}), toonDur=0.25, toonEase='inOut'), k(r(OUI10 + 1.0), toon=LEAN10(0.25, {'lid': 1.0, 'mouth': 'bigsmile'}), toonDur=0.2)]),
        act('maire', MA10, 15, 'stand', 'happy', keys=[k(0.0, look=[r(GR[0] + 0.3), 2.0, GR[2]]), k(0.0, toon=CLAP10(0), toonDur=0.0), *[k(r(OUI10 + 0.15 + 0.13 * j), toon=CLAP10(j + 1), toonDur=0.07) for j in range(10)]])],
        props=[TEL('tel10'), NOTES('mus10', size=0.16, t1=r(OUI10 - 0.4)), P('voile10', 'bridalVeil', on={'actor': 'femme', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}),
               P('bouq10', 'bouquet', on={'actor': 'femme', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}), BURST('oui10', [-0.1, 2.85, 0.5], OUI10, 'OUI !', 0.55, 1.2)],
        cams=[FC(0.0, [0.1, 1.85, 3.2], [[GR[0], 2.45, GR[2]], [r(GR[0] - 0.42), 1.5, GR[2]], [0.7, 1.5, BR10[2]], [r(MA10[0] - 0.28), 2.3, MA10[2]], [-0.1, 3.05, 0.5], [0.0, 1.2, 0.3]], top=0.14, bottom=0.76)])   # (pass 2) face on to him, side on to her
st.cue('sfx:pop', 'S10', OUI10, 0.2); st.cue('sfx:fanfare', 'S10', r(OUI10 + 0.2), 0.15)

# 11: the music became the national anthem. A ceremony in the street: him in front, in the middle, the phone on his ear; behind him the flag climbs
#     its pole, a column of notes rises from the phone up along it, officials and soldiers salute (HYMNE)
D11 = st.dur('S11'); POLE = [0.4, 0, -2.4]; H11 = [0.0, 0, 0.6]
HEART = lambda f: {'touch': {'R': ['torso', -0.08, 0.45, 0.25, 1, 0.02]}, 'hands': {'R': 'open'}, 'face': f}
st.shot('S11', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', H11, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0), FK(0.5, {'lid': 0.3, 'mouth': 'line', 'gx': 0.6, 'gy': -0.8}, 0.15),
            FK(1.5, {**DEAD, 'mouth': 'line'}, 0.15), *BL(1.85, {**DEAD, 'mouth': 'line'})]),                                            # his eyes follow his notes up, and come back to us
        *[act(oid, [x, 0, z], ry, 'salute' if pre == 'cop' else 'stand', 'determined', keys=[k(0.0, look=[POLE[0], 4.0, POLE[2]]),
            *([k(0.0, toon=HEART({'lid': 0.3, 'mouth': 'line'}), toonDur=0.0), k(r(0.7 + 0.4 * (x > 0)), toon=HEART({'lid': 1.0, 'mouth': 'line'}), toonDur=0.07), k(r(0.82 + 0.4 * (x > 0)), toon=HEART({'lid': 0.3, 'mouth': 'line'}), toonDur=0.08),
               k(1.6, look=[0.0, 1.9, 0.6])] if pre != 'cop' else [])])                                                                  # a blink, then a glance at him: the anthem is his phone
          for oid, x, z, ry, pre in [('off1', -0.85, -1.4, 8, 'politique'), ('sold1', 0.8, -1.2, -5, 'cop'), ('sold2', 1.35, -1.9, -8, 'cop')]]],
        props=[TEL('tel11'), NOTES('mus11', rate=4.0, size=0.27, dy=1.5, dx=0.04, life=1.7, sway=0.1), P('mat11', 'flagPole', pos=POLE, opts={'h': 5.0, 'w': 1.1, 'raise': [0.1, r(D11 - 0.3)]})],
        cams=[FC(0.0, [0.2, 0.9, 4.5], [[H11[0], 1.15, H11[2]], [H11[0], 2.45, H11[2]], [POLE[0], 5.25, POLE[2]], [r(POLE[0] + 1.25), 4.6, POLE[2]], [-0.95, 2.3, -1.4], [1.45, 2.3, -1.9]], top=0.08, bottom=0.86)])   # (pass 2) low, him in front, the pole over his shoulder
st.cue('sfx:fanfare', 'S11', 0.2, 0.25)

# 12: the band played it at the parade. The street with flags: a marching band comes at us, the bass drum and the big tuba in the front rank, two
#     trumpets behind, in step, playing it
D12 = st.dur('S12'); X12 = 3.5; Z12 = 2.2; V12 = 1.2; ZE12 = r(Z12 - V12 * D12); BEATS = [0.1, 0.5, 0.9, 1.3, 1.7]
BAND = [('mus1', -0.55, 0.0, 'drum'), ('mus2', 0.55, 0.0, 'tuba'), ('mus3', 0.0, 1.25, 'trumpet'), ('mus4', -1.1, 1.25, 'trumpet')]   # (stills 2) the trumpets in the gaps of the front rank, seen from the camera
PUFF = {'lid': 0.4, 'mouth': 'kiss', 'cheeks': 0.9, 'puff': 0.6}
def PLAY12(kind, j=0):
    if kind == 'trumpet': return {'touch': {'R': ['head', 0.05, 0.1, 0.52, 1, 0.03], 'L': ['head', -0.05, 0.1, 0.36, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': PUFF, 'sq': [1.0, 1.03 if j % 2 else 0.98, 1.0]}
    if kind == 'tuba': return {'touch': {'R': ['torso', -0.3, 0.5, 0.3, 1, 0.03], 'L': ['torso', 0.32, 0.3, 0.3, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {**PUFF, 'cheeks': 1.0, 'puff': 1.0}, 'sq': [1.03, 0.97, 1.03] if j % 2 else [0.98, 1.03, 0.98]}
    return {'touch': {'R': ['torso', -0.42, 0.28 if j % 2 else 0.78, 0.42, 1, 0.03], 'L': ['torso', 0.42, 0.78 if j % 2 else 0.28, 0.42, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4}}   # the drummer: one fist up, one on the drum
INSTR = {'trumpet': ({'joint': 'head', 'offset': [0.0, 0.1, 0.1], 'rot': [-0.2, 0.0, 0.0]}, 2.0), 'tuba': ({'joint': 'torso', 'offset': [0.0, 0.25, 0.24]}, 2.3), 'drum': ({'joint': 'torso', 'offset': [0.0, 0.22, 0.36]}, 1.75)}
st.shot('S12', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act(mid, [r(X12 + dx), 0, r(Z12 + dz)], 180, 'walk', 'determined', keys=[k(0.0, to=[r(X12 + dx), 0, r(ZE12 + dz)], dur=D12, clip='walk', ease='linear'), k(0.0, toon=PLAY12(kind, 0), toonDur=0.0),
            *[k(r(b_ - 0.08), toon=PLAY12(kind, j + 1), toonDur=0.08, toonEase='in') for j, b_ in enumerate([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7])]])
        for mid, dx, dz, kind in BAND],
        props=[*[P(f'ins12{j}', 'brass', on={'actor': mid, **INSTR[kind][0]}, scale=INSTR[kind][1], opts={'kind': kind, 'beat': BEATS if kind == 'drum' else []}) for j, (mid, dx, dz, kind) in enumerate(BAND)],
               *[P(f'n12{j}', 'holdNotes', on={'actor': BAND[2 + j][0], 'joint': 'head', 'offset': [0.0, 0.25, 0.85], 'face': 'camera'}, opts={'rate': 2.5, 'size': 0.34, 'dy': 0.9, 'dx': 0.3, 'sway': 0.08, 'side': 1 if j else -1, 'from': -1.0}) for j in range(2)],
               *[P(f'dr12{j}', 'flag', pos=[r(6.2 if j % 2 else 0.8), 2.2, r(-2.0 + 2.6 * j)], scale=0.5, opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A']}) for j in range(3)]],
        cams=[FC(0.0, [r(X12 - 0.9), 0.75, r(ZE12 - 4.6)], [[r(X12 - 0.95), 0.1, ZE12], [r(X12 + 0.95), 2.95, ZE12], [r(X12 + 0.95), 0.2, ZE12], [r(X12 - 1.35), 2.5, r(ZE12 + 1.25)], [X12, 2.5, r(ZE12 + 1.25)]], top=0.1, bottom=0.82)])   # (pass 2) low, the big instruments in front
st.cue('sfx:fanfare', 'S12', 0.05, 0.3); st.cue('thud', 'S12', 0.1, 0.15); st.cue('thud', 'S12', 0.5, 0.15); st.cue('thud', 'S12', 0.9, 0.15); st.cue('thud', 'S12', 1.3, 0.15)

# 13: the children whistle it at school. A classroom: three children in a row in front of the board, facing us, whistle it, big chalk notes over
#     their heads; the teacher beside them, in profile, beats time with a ruler
D13 = st.dur('S13'); KIDS = [('el1', -0.6), ('el2', 0.0), ('el3', 0.6)]; ZK = -2.5; PROF = [0.33, 0, -3.15]   # (stills 2) the teacher behind them, between two heads: beside them she widened the frame past the first desks
st.shot('S13', 'classroom', setOpts={'board': 'MUSIQUE', 'board2': "L'hymne national", 'board3': 'la la la la'}, actors=[
        *[act(eid, [x, 0, ZK], 0, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'kiss', 'mouthW': 0.7, 'mouthH': 0.7, 'cheeks': 0.6}}, toonDur=0.0),
            *[k(r(0.08 + 0.28 * j + 0.09 * i), toon={'face': {'lid': 0.3 if j % 3 else 1.0, 'mouth': 'kiss', 'mouthW': 0.7, 'mouthH': 0.7, 'cheeks': 0.6 if j % 2 else 0.9, 'puff': 0.5}, 'sq': [0.97, 1.06, 0.97] if (j + i) % 2 else [1.04, 0.95, 1.04]}, toonDur=0.14, toonEase='inOut') for j in range(7)]])
          for i, (eid, x) in enumerate(KIDS)],
        act('prof', PROF, -90, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.2, ZK]), *[k(r(0.05 + 0.24 * j), toon={'reach': {'R': [r(PROF[0] - 0.45 + (0.12 if j % 2 else -0.05)), r(2.15 + (0.2 if j % 2 else -0.1)), r(PROF[2] + 0.1), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smile'}}, toonDur=0.14, toonEase='inOut') for j in range(8)]])],
        props=[*[P(f'n13{i}', 'holdNotes', on={'actor': eid, 'joint': 'head', 'offset': [0.0, 0.78, 0.1], 'face': 'camera'}, opts={'rate': 2.2, 'size': 0.2, 'from': r(-1.0 + 0.15 * i), 'dy': 0.5, 'dx': 0.12, 'side': (-1, 1, 1)[i], 'color': '#FFF6DC', 'halo': '#22305A'}) for i, (eid, x) in enumerate(KIDS)],
               P('regle13', 'slab', on={'actor': 'prof', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, opts={'w': 0.035, 'h': 0.5, 'd': 0.012, 'color': '#E2B53C'})],
        cams=[FC(0.0, [0.78, 1.25, 0.1], [[-0.78, 1.5, ZK], [0.78, 1.5, ZK], [0.0, 0.75, ZK], [0.0, 2.42, -3.55]], top=0.14, bottom=0.74, inside=(-4.0, 4.0, 0.5, 3.0, -3.3, 6.0))])   # (pass 2) the children facing us, the board behind
st.cue('sfx:whistle', 'S13', 0.1, 0.25)

# 14: yesterday someone picked up. Ten years on, on his sofa, the phone on his ear: click: the notes freeze in the air and drop; his eyes go to the
#     phone, he squashes, and the take: eyes out on stalks
D14 = st.dur('S14'); CLK14 = 0.45; AGE = {'low': 0.25}   # ten years on: grey hair (cast), heavier lower lids; the gloom over his eyes (shadow) only before the click and at the very end
A = lambda **f: {**AGE, **f}
SITCAM = lambda frm, extra=(), **kw: FC(0.0, frm, [[SIT[0], 1.92, SIT[2]], [SIT[0], 0.95, SIT[2]], [0.48, 1.6, SIT[2]], [-0.42, 1.6, SIT[2]], *extra], **kw)
st.shot('S14', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(A(lid=0.5, mouth='line', shadow=0.85)), toonDur=0.0),
            k(r(CLK14 + 0.04), toon=FREE(A(lid=0.25, mouth='line', gx=1.0, brow=0.3, shadow=0.3)), toonDur=0.06),                                    # the click: his eyes go to the phone
            k(r(CLK14 + 0.2), toon=FREE(A(lid=0.9, mouth='clench', brow=-0.7), {'sq': [1.08, 0.86, 1.08]}), toonDur=0.08, toonEase='in'),   # he squashes...
            k(r(CLK14 + 0.3), toon=FREE(A(lid=0.0, eye=0.6, pop=0.85, popLen=0.26, mouth='O', brow=1.0, pupilShake=0.8), {'sq': [0.93, 1.12, 0.93]}), toonDur=0.05, toonEase='out'),   # ...and the take
            k(r(CLK14 + 0.48), toon=FREE(A(lid=0.0, eye=0.6, pop=0.7, popLen=0.2, mouth='O', brow=1.0, pupilShake=1.0), {'sq': [1.0, 1.0, 1.0]}), toonDur=0.1),
            k(r(CLK14 + 0.95), toon=FREE(A(lid=0.0, eye=0.5, pop=0.4, popLen=0.14, mouth='o', brow=0.9, pupilShake=0.7, tremble=0.7)), toonDur=0.2)])],   # held, the pupils shivering
        props=[TEL('tel14', OLD), NOTES('mus14', OLD, t0=-2.0, rate=3.5, size=0.14, stopAt=CLK14)],
        cams=[SITCAM([0.4, 1.5, 0.3], [[0.85, 2.35, SIT[2]]], top=0.16, bottom=0.74)])
st.cue('sfx:click', 'S14', CLK14, 0.35); st.cue('sfx:gasp', 'S14', r(CLK14 + 0.3), 0.25)

# 15: he cried for joy... Close: his face crumples, tears jetting out sideways, his hands clasped, his shoulders heaving, the phone still on his ear
D15 = st.dur('S15')
JOY = {'touch': {'R': ['torso', -0.04, 0.45, 0.28, 1, 0.02], 'L': ['torso', 0.04, 0.45, 0.28, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
SOB = lambda j: {**JOY, 'face': A(tears=1.0, mouth='scream' if j % 2 else 'sob', brow=0.9, lid=0.85), 'sq': [r(1.0 + (0.04 if j % 2 else 0.0)), r(1.0 - (0.05 if j % 2 else -0.02)), r(1.0 + (0.04 if j % 2 else 0.0))], 'bend': {'spine': [r(0.14 if j % 2 else -0.04), 0, 0, 1, None]}}
TEARS = lambda pid, r_=0.026, rate=24, sp=1.9: P(pid, 'tearFountain', on={'actor': OLD, 'joint': 'head', 'offset': [0.0, 0.24, 0.17]}, opts={'at': 0.0, 'dx': 0.09, 'rate': rate, 'speed': sp, 'r': r_})
st.shot('S15', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SOB(0), toonDur=0.0), *[k(r(0.08 + 0.17 * j), toon=SOB(j + 1), toonDur=0.09, toonEase='inOut') for j in range(8)]])],
        props=[TEL('tel15', OLD), TEARS('larmes15')],
        cams=[SITCAM([0.45, 1.2, -1.2], [[0.66, 1.75, SIT[2]], [-0.62, 1.75, SIT[2]]], top=0.16, bottom=0.74)])   # low, from the phone side: the tears against the wall
st.cue('sfx:sniff', 'S15', 0.2, 0.25); st.cue('sfx:sniff', 'S15', 0.7, 0.2)

# 16: ...live on television. Wider: two TV cameras and their operators frame him, dark, left and right; he sobs in the middle, a reporter's mic comes
#     in from the side; over him a red EN DIRECT sign
D16 = st.dur('S16'); MIC16 = [0.4, 1.4, r(SIT[2] + 0.32)]; ZC16 = r(SIT[2] + 1.3)   # (stills 2) no operators (a back filled a quarter of the frame): two low cameras in the lower corners, the mic from the right
MICK = lambda p, b, f: {'reach': {'R': [*p, 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [b, 0, 0, 1, None]}, 'face': f}
st.shot('S16', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SOB(0), toonDur=0.0), *[k(r(0.06 + 0.17 * j), toon=SOB(j + 1), toonDur=0.09, toonEase='inOut') for j in range(8)]]),
        act('repo', [1.1, 0, r(SIT[2] + 0.45)], -100, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, SIT[2]]), k(0.0, toon=MICK([0.8, 1.5, r(SIT[2] + 0.4)], 0.0, {'lid': 0.2, 'mouth': 'open'}), toonDur=0.0),
            k(0.08, toon=MICK(MIC16, 0.3, {'lid': 0.1, 'mouth': 'open', 'brow': 0.5}), toonDur=0.3, toonEase='out'),                                  # she leans in with the mic...
            k(0.6, toon=MICK([r(MIC16[0] - 0.05), r(MIC16[1] - 0.06), MIC16[2]], 0.36, {'lid': 0.1, 'mouth': 'o', 'brow': 0.6}), toonDur=0.25, toonEase='inOut'),   # ...and it follows his sobs
            k(0.95, toon=MICK([r(MIC16[0] + 0.02), r(MIC16[1] + 0.04), MIC16[2]], 0.3, {'lid': 0.1, 'mouth': 'open', 'brow': 0.6}), toonDur=0.25, toonEase='inOut')])],
        props=[TEL('tel16', OLD), TEARS('larmes16', 0.024, 22, 1.7),
               P('mic16', 'pressMic', on={'actor': 'repo', 'hand': 'R', 'offset': [0.0, -0.02, 0.04]}, scale=1.5, opts={'text': 'INFO', 'color': '#C8322A'}),
               *[P(f'tv16{j}', 'tvCamera', pos=[x, 0, ZC16], ry=r(180 - 12 * (1 if x > 0 else -1)), opts={'h': 0.95},
                   keys=[k(0.0, to=[r(x * 0.92), 0, r(ZC16 - 0.12)], dur=D16, ease='inOut'), k(r(0.2 + 0.3 * j), rotTo=[0, r(math.radians(180 - 18 * (1 if x > 0 else -1)), 4), 0], dur=0.5, ease='inOut')]) for j, x in enumerate((-0.42, 0.42))],   # they push in and pan on him
               P('direct16', 'signBoard', pos=[0.0, 0, -3.45], opts={'text': 'EN DIRECT', 'bg': '#D22B2B', 'fg': '#FFFFFF', 'w': 1.15, 'h': 0.32, 'height': 2.2})],
        cams=[FC(0.0, [0.0, 1.45, -0.5], [[SIT[0], 1.92, SIT[2]], [SIT[0], 0.9, SIT[2]], [0.0, 2.6, -3.45], [-0.7, 1.75, SIT[2]], [0.7, 1.75, SIT[2]]], top=0.12, bottom=0.76)])   # (pass 2) between the two cameras
st.cue('sfx:click', 'S16', 0.2, 0.15)

# 17: the voice said... Close on the phone on his ear: a flat electronic voice, a jagged little bubble with its tail on the phone; his eyes slide to it
D17 = st.dur('S17')
st.shot('S17', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(A(lid=0.0, eye=0.3, mouth='o', brow=0.6)), toonDur=0.0),
            FK(0.22, A(lid=0.0, eye=0.35, mouth='o', brow=0.9, gx=1.0), 0.1), FK(0.75, A(lid=0.0, eye=0.35, mouth='o', brow=0.9, gx=1.0, pupilShake=0.6), 0.1)])],   # his eyes slide to the voice
        props=[TEL('tel17', OLD), P('bulle17', 'voiceBubble', on={'actor': OLD, 'joint': 'head', 'offset': [0.3, 0.44, 0.02], 'face': 'camera'}, opts={'at': 0.1, 'text': 'BIP', 'w': 0.46})],
        cams=[FC(0.0, [0.85, 1.7, -1.35], [[SIT[0], 1.3, SIT[2]], [0.8, 2.22, SIT[2]], [-0.2, 1.6, SIT[2]], [0.85, 1.9, SIT[2]], [SIT[0], 1.9, SIT[2]]], top=0.18, bottom=0.7)])   # (pass 2) the ear and the phone above the middle, the chin above the captions
st.cue('sfx:ding', 'S17', 0.1, 0.15)

# 18: ...for an adviser, press one. His hand goes up to the phone and pulls: the ear and the head stretch after it, POP, it comes free, the head
#     springs back; he holds it in front of him, the keypad to us, and his eyes drop to it
D18 = st.dur('S18'); POP18 = 0.42; CAR18 = 0.24
def OFF18(u, s, sy, f, lay=0.0): return {'touch': {'L': MIX(GRIP, FGRIP, eio(min(1.0, max(0.0, u))))}, 'hands': {'L': 'grip'}, 'scl': {'head': [s, sy, 1.0]}, 'lay': [0, lay], 'face': f}
st.shot('S18', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(A(lid=0.0, eye=0.3, mouth='o')), toonDur=0.0),
            k(0.03, toon=HOLD(A(lid=0.2, mouth='clench', brow=-0.4)), toonDur=0.14, toonEase='inOut'),                                    # the hand goes up to the phone
            k(0.19, toon=OFF18(0, 0.9, 1.05, A(lid=0.3, mouth='clench', brow=-0.6, gx=0.8)), toonDur=0.06),                              # an anticipation...
            k(0.26, toon=OFF18(0, 1.6, 0.92, A(lid=0.15, mouth='grimace', brow=-0.8, gx=0.8, sweat=1.0), -0.04), toonDur=0.15, toonEase='out'),   # ...he pulls: the ear and the head stretch after it
            *[k(r(POP18 + 0.06 * j), toon=OFF18((0.06 * (j + 1)) / CAR18, s_, sy_, A(lid=0.0, eye=0.5, mouth='O', brow=1.0), l_), toonDur=0.06, toonEase='linear')
              for j, (s_, sy_, l_) in enumerate([(0.78, 1.16, 0.03), (1.12, 0.94, -0.01), (0.95, 1.04, 0.0), (1.0, 1.0, 0.0)])],          # POP: it comes free, the head springs back and wobbles
            FK(r(POP18 + 0.36), A(lid=0.3, mouth='line', gy=0.85), 0.1),                                                                 # his eyes drop to the screen
            *BL(1.2, A(lid=0.3, mouth='line', gy=0.85)),
            k(1.38, toon=SHOW(A(lid=0.3, mouth='line', gy=0.85), TAP0), toonDur=0.25, toonEase='inOut')])],                              # the other index comes up over the keypad
        props=[TEL('tel18', OLD, keys=CARRY(OLD, POP18, CAR18, EAR, FRONT), keypad=1), BURST('pop18', [0.55, 1.85, r(SIT[2] + 0.1)], POP18, 'POP !', 0.42, 0.4)],
        cams=[SITCAM([0.25, 1.1, -0.5], [[0.75, 2.05, SIT[2]], [0.15, 0.78, r(SIT[2] + 0.45)]], top=0.16, bottom=0.74)])   # lower and closer than S14
st.cue('sfx:stretch', 'S18', 0.26, 0.25); st.cue('pop', 'S18', POP18, 0.3)

# 19: he pressed one. Insert, from below: the red phone big in his hand, its keypad square to us; one finger comes in from the lower right, presses the
#     1 and lifts: the 1 stays green, in the clear (UN)
D19 = st.dur('S19'); PRESS19 = 0.55; PAD19 = [0.0, 1.45, -1.2]
st.shot('S19', 'livingRoom', setOpts=LR, actors=[],
        props=[P('pad19', 'phoneKeypad', pos=PAD19, face='camera', scale=0.3, opts={'label': 'SERVICE CLIENT', 'pressAt': PRESS19, 'case': '#E3241B', 'hold': 1, 'finger': 1})],
        cams=[FC(0.0, [0.04, 1.0, -0.5], [[-0.09, 1.62, PAD19[2]], [0.09, 1.62, PAD19[2]], [-0.09, 1.28, PAD19[2]], [0.12, 1.28, PAD19[2]]], top=0.22, bottom=0.72, lenses=range(16, 60))])   # (pass 2) no face behind it: the wall over the sofa
st.cue('sfx:click', 'S19', PRESS19, 0.35)

# 20: the music started again. The notes pour out of the phone in his hand; his face falls; he puts it back on his ear and looks at us, deadpan
D20 = st.dur('S20'); BACK20 = 0.5
st.shot('S20', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SHOW(A(lid=0.3, mouth='line', gy=0.85)), toonDur=0.0),
            FK(0.16, A(lid=0.1, mouth='o', gy=0.85, brow=0.7)), FK(0.34, A(lid=0.6, mouth='line', gy=0.85, brow=-0.3, shadow=0.9), 0.14),   # the notes: his brows go up, and down; the gloom comes over his eyes again
            k(BACK20, toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9)), toonDur=0.3, toonEase='inOut'),                                   # back on the ear
            k(r(BACK20 + 0.31), toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9), {'sq': [1.03, 0.96, 1.03]}), toonDur=0.05), k(r(BACK20 + 0.38), toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9)), toonDur=0.12),
            *BL(1.3, A(lid=0.5, mouth='line', shadow=0.9)), k(1.72, toon=HOLD(A(lid=1.0, mouth='line', shadow=0.9)), toonDur=0.18, toonEase='inOut'), k(1.98, toon=HOLD(A(lid=0.55, mouth='line', shadow=0.9)), toonDur=0.16)])],   # a long, slow blink
        props=[TEL('tel20', OLD, start=FRONT, keys=CARRY(OLD, BACK20, 0.3, FRONT, EAR), keypad=1), NOTES('mus20a', OLD, t0=0.08, t1=r(BACK20 - 0.05), rate=5.0, size=0.14, off=[0.2, -0.2, 0.46]),
               NOTES('mus20b', OLD, t0=r(BACK20 + 0.28), rate=4.0, size=0.14)],
        cams=[SITCAM([0.95, 1.6, -0.6], [[0.8, 2.4, SIT[2]], [0.2, 0.8, r(SIT[2] + 0.45)]], top=0.14, bottom=0.76)])   # three quarters from the phone side   # wider, from the phone side: the end hold
st.cue('sfx:ding', 'S20', 0.1, 0.12)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
FIRE = {'preset': 'pompier', 'suit': '#23304E', 'pants': '#23304E', 'hatColor': '#C9CED6', 'bandColor': '#D8372E', 'bandH': 0.05, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
st.write("Le service client", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec', OLD], extra_cast={
    'mec': MEC, OLD: {**MEC, 'hairColor': '#B9BDC4'},
    'pomp1': {**FIRE, 'seed': 731}, 'pomp2': {**FIRE, 'seed': 732},
    'femme': {'preset': 'femme', 'seed': 733, 'suit': '#F7F5EF', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 734, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'suit': '#26365F', 'lapel': '#26365F', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off1': {'preset': 'politique', 'seed': 735, 'suit': '#33363D', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold1': {'preset': 'cop', 'seed': 737, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold2': {'preset': 'cop2', 'seed': 738, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{mid: {'preset': 'officiel', 'seed': 740 + j, 'suit': '#8E2B2B', 'hat': 'copcap', 'hatColor': '#8E2B2B', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j, (mid, _, _, _) in enumerate(BAND)},
    **{eid: {'preset': 'gamin', 'seed': 750 + j, 'suit': c_, 'build': {'headScale': 1.25}, 'toon': EX} for j, ((eid, _), c_) in enumerate(zip(KIDS, ['#E0413A', '#3A9BDC', '#E8A33C']))},
    'prof': {'preset': 'madame', 'seed': 755, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'repo': {'preset': 'journaliste', 'seed': 756, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
