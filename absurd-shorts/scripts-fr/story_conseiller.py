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
Natural look; cycle 35: props_conseiller.js (holdNotes, brass, bridalVeil, flagPole, phoneKeypad; pass 2: bigPhone, tearCalendar, voiceBubble), props reused (sofaProp,
tearFountain, tvCamera, pressMic, hicBurst, flag, signBoard).
Pass 2 (review 1: 5.4 / 5.4): the phone is one big red handset (bigPhone), stuck flat on his LEFT ear, the ear on the side of the lens, held by his left
hand up to S05 and hanging there by itself from S07 to S17 (the old one sat in a fist in front of his chin: the right hand crossed over to the left
side of the face); the notes are bigger, edged in white and come out of the phone; the pull of S07 doubles the width of his head, the take of S06 and
the pop of S18 are played in full; the calendar tears its pages off; the escalation is restaged shot by shot (sofa carried face on, the yes in
profile, him in front of the flag, tuba and drum in the front rank, the children facing us); the 1 is pressed by one finger and stays green.
Pass 3 (review 2: 6.8 / 7.0): S10 the bride bends and stretches up to the phone, OUI bursts out of it in a yellow bubble with its tail on it (camera
from the left front, her lean later so that her head never crosses his face); S14 click, notes hanging 7 frames, eyes to the phone, drop, squash,
then eyes out on long stalks with the jaw dropped, overshoot and wobble (S06 keeps the round-eyed take); S18 the head pulled to 2.6 times its width
(2.25 in S07), held trembling, POP and three smaller bounces; S07 brace, lean back, the width dragged over 6 frames, a visible tremble; S11 the two
soldiers and the official salute together on « hymne », the flag starts above the heads; S16 newsCamera (props_conseiller.js: light grey, lens, TV
plate, red light) at his sides three quarters to us, the reporter's head out of frame; S08 closer, chrome helmets, yellow bands; S09 and S11 his head
rocks on the music, S20 he flattens into the sofa and re-inflates, S03 his eyes lead the glance; S13 chalk-white notes on the board, the camera above
the heads; the old man's hair mid-grey."""
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
def SWAY(t0, t1, per, faces, amp=0.07):   # (pass 3) the music takes his body: the head and the shoulders rock on the beat (faces: [(t, face)], the face of each moment)
    out, j, t = [], 0, t0
    while t < t1 - 1e-6:
        f = [fc for tt, fc in faces if tt <= t + 1e-6][-1]; sd = 1 if j % 2 == 0 else -1
        out.append(k(r(t), toon=FREE(f, {'bend': {'neck': [0.03, r(amp * sd), 0, 1, None], 'spine': [0, r(0.35 * amp * sd), 0, 1, None]}}), toonDur=r(per * 0.8), toonEase='inOut'))
        j += 1; t += per
    return out

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

# 3: the hold music... Wider: he stands in front of his sofa, the phone at his ear, notes rising; a calendar on the wall: his eyes go to it first,
#    then his head half turns after them (one eye still to us); a blink
D3 = st.dur('S03'); CAL = [-0.7, 2.0, -3.55]; H3 = [0.35, 0, -2.2]
st.shot('S03', 'livingRoom', setOpts=LR, actors=[act('mec', H3, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0),
            k(0.22, toon=HOLD({'lid': 0.25, 'mouth': 'line', 'gx': -1.0, 'brow': 0.3}), toonDur=0.08),                                     # (pass 3) his eyes go to the calendar first...
            k(0.4, look=[r(CAL[0] + 0.75), CAL[1], r(CAL[2] + 1.6)], lookDur=0.2),                                                         # ...then his head, half way: one eye stays to us
            k(0.4, toon=HOLD({'lid': 0.3, 'mouth': 'line', 'gx': -0.8}), toonDur=0.12),
            *BL(0.78, {'lid': 0.3, 'mouth': 'line', 'gx': -0.8})])],
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

# 7: ...stuck to his ear. Close, face on: both hands on the phone, he braces and leans back, then pulls: his head is dragged out over a fifth of a
#    second to twice its width after the phone, trembles there, heaves once more, and snaps back when his grip slips; the phone has not moved
D7 = st.dur('S07')
def PULL(s, f, extra=None, brace=0.0, dy=0.0):   # s: the width of his head (1 = its own); the body tips that way so that the far side of the head stays where it was
    # (pass 3) brace: he leans back and away from the phone (the spine, not the scale of the body); dy: the head's height, for the tremble
    return {'touch': {'L': ['head', 0.27, 0.3, 0.045, 1, 0.02, [1, -0.3, 0.0]], 'R': ['head', 0.23, 0.0, 0.1, 1, 0.02, [-0.5, -1, 0.6]]}, 'hands': {'L': 'grip', 'R': 'grip'},
            'scl': {'head': [s, r(1 - 0.12 * (s - 1) + dy), 1.0]}, 'lay': [0, r(-0.063 * (s - 1))], 'bend': {'spine': [r(-0.14 * brace), r(0.1 * brace), 0, 1, None]}, 'face': f, **(extra or {})}
LOOSE7 = lambda s, sy, f: {'reach': {'L': [0.75, 1.5, r(ME[2] + 0.2), 1, 0.03], 'R': [-0.7, 1.5, r(ME[2] + 0.2), 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'scl': {'head': [s, sy, 1.0]}, 'lay': [0, r(-0.063 * (s - 1))], 'face': f}
STRAIN = {'lid': 0.15, 'mouth': 'clench', 'brow': -0.8, 'sweat': 1.0, 'tremble': 1.0, 'pupilShake': 1.0}
st.shot('S07', 'livingRoom', setOpts=LR, actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=PULL(1.0, {'lid': 0.3, 'mouth': 'clench', 'brow': -0.6}), toonDur=0.0),
            k(0.0, toon=PULL(0.88, {'lid': 0.4, 'mouth': 'clench', 'brow': -0.7}, brace=1.0), toonDur=0.12, toonEase='inOut'),            # (pass 3) he braces, leans back: 4 frames...
            k(0.13, toon=PULL(1.35, STRAIN, brace=1.2), toonDur=0.08, toonEase='in'),                                                    # ...and pulls: the head is dragged after the phone...
            k(0.22, toon=PULL(2.0, STRAIN, brace=1.3), toonDur=0.1, toonEase='out'),                                                     # ...over 6 frames, to twice its width
            *[k(r(0.33 + 0.066 * j), toon=PULL(2.14 if j % 2 else 1.9, STRAIN, brace=1.3, dy=0.03 if j % 2 else -0.03), toonDur=0.05, toonEase='linear') for j in range(5)],   # it trembles there, up and down too
            k(0.66, toon=PULL(2.3, {**STRAIN, 'mouth': 'grimace'}, brace=1.5), toonDur=0.08, toonEase='in'),                             # one more heave
            k(0.77, toon=LOOSE7(0.76, 1.2, {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}), toonDur=0.05, toonEase='out'),          # his grip slips: the head snaps back too far...
            k(0.85, toon=LOOSE7(1.14, 0.93, {'lid': 0.0, 'eye': 0.4, 'mouth': 'o', 'brow': 0.8}), toonDur=0.07),
            k(0.94, toon=LOOSE7(0.94, 1.04, {'lid': 0.2, 'mouth': 'wavy', 'brow': 0.3, 'cross': 0.5}), toonDur=0.07),
            k(1.03, toon=FREE({'lid': 0.3, 'mouth': 'wavy', 'cross': 0.3}, {'scl': {'head': [1.0, 1.0, 1.0]}, 'lay': [0, 0]}), toonDur=0.1),   # ...wobbles, and is a head again
            FK(1.2, {'lid': 0.2, 'mouth': 'line', 'gx': 1.0}, 0.1),                                                                      # a look at the phone: still there
            *BL(1.34, {**DEAD, 'mouth': 'line', 'gx': 0.6})])],
        props=[TEL('tel7'), NOTES('mus7', size=0.12)],
        cams=[FC(0.0, [0.3, 1.95, 1.3], [[ME[0], 2.5, ME[2]], [ME[0], 1.5, ME[2]], [0.85, 2.05, ME[2]], [-0.45, 2.05, ME[2]]], top=0.14, bottom=0.74)])
st.cue('sfx:stretch', 'S07', 0.12, 0.25); st.cue('sfx:stretch', 'S07', 0.6, 0.25); st.cue('sfx:boing', 'S07', 0.76, 0.25)

# 8: the firemen moved house with him. Down the street, toward us, close: two firemen in chrome helmets carry his sofa on two poles at chest height,
#    like a sedan chair; he sits on it above their heads, the phone on his ear by itself, bobbing and nodding a little late on their steps, notes rising
D8 = st.dur('S08'); X8 = 3.6; Z8 = 2.6; V8 = 1.0; Y8 = 1.4; S8 = 0.7; DX8 = 1.0; ZE8 = r(Z8 - V8 * D8); HY8 = r(Y8 + 0.56 * S8 - 0.56)
CARRY8 = lambda x, z: {'reach': {'R': [x, r(Y8 - 0.04), r(z - 0.28), 1, 0.04], 'L': [x, r(Y8 - 0.04), r(z + 0.28), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4, 'sweat': 0.6}}
st.shot('S08', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', [X8, HY8, Z8], 180, 'sit', 'neutral', keys=[k(0.0, to=[X8, HY8, ZE8], dur=D8, ease='linear', glide=True),   # (stills 3) glide: a move without a clip walks, and he stood on his sofa
            k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0),
            *[k(r(0.14 + 0.24 * j), toon=FREE(extra={'sq': [1.04, 0.92, 1.04] if j % 2 == 0 else [0.97, 1.06, 0.97], 'bend': {'neck': [r(0.12 if j % 2 == 0 else -0.06), r(0.07 if j % 2 else -0.07), 0, 1, None]}}), toonDur=0.12, toonEase='inOut') for j in range(7)],   # he bobs, half a beat after their steps; (pass 3) his head nods and rocks with it
            *BL(1.1, {**DEAD, 'mouth': 'line'})]),
        *[act(fid, [r(X8 + dx), 0, Z8], 180, 'walk', 'determined', keys=[k(0.0, to=[r(X8 + dx), 0, ZE8], dur=D8, clip='walk', ease='linear'),
            k(0.0, toon=CARRY8(r(X8 + dx), Z8), toonDur=0.0), k(0.001, toon=CARRY8(r(X8 + dx), ZE8), toonDur=D8, toonEase='linear')])
          for fid, dx in [('pomp1', -DX8), ('pomp2', DX8)]]],   # (pass 3) closer together (1.15): the group fills the width
        props=[P('canape8', 'sofaProp', pos=[X8, Y8, Z8], ry=180, scale=S8, keys=[k(0.0, to=[X8, Y8, ZE8], dur=D8, ease='linear')]),
               *[P(f'perche8{j}', 'slab', pos=[X8, r(Y8 - 0.04), r(Z8 + dz)], opts={'w': 2.5, 'h': 0.07, 'd': 0.07, 'color': '#8A5A30', 'outline': 0.005}, keys=[k(0.0, to=[X8, r(Y8 - 0.04), r(ZE8 + dz)], dur=D8, ease='linear')]) for j, dz in enumerate((-0.28, 0.28))],
               TEL('tel8'), NOTES('mus8', size=0.32, rate=3.0, dy=0.8, dx=0.35, sway=0.08)],
        cams=[FC(0.0, [r(X8 + 0.45), 1.05, r(ZE8 - 3.6)], [[X8, r(HY8 + 1.75), ZE8], [r(X8 - 1.2), 0.6, ZE8], [r(X8 + 1.2), 0.6, ZE8], [r(X8 + 0.55), r(HY8 + 1.95), ZE8]], top=0.1, bottom=0.84)])   # (pass 2) face on, low; (pass 3) closer: the group fills the width, the firemen's outer arms at the edges
st.cue('sfx:stepSoft', 'S08', 0.3, 0.15); st.cue('sfx:stepSoft', 'S08', 0.8, 0.15); st.cue('sfx:stepSoft', 'S08', 1.3, 0.15)

# 9: he got married on hold. The town hall: the mayor in his sash reads from the register; the bride in her veil beside him; the phone on his ear by
#    itself, his hands free, notes rising over the wedding; his head and shoulders rock on the hold music
D9 = st.dur('S09'); BR = [0.5, 0, 0.3]; GR = [-0.5, 0, 0.3]; MA = [0.0, 0, -1.55]; MAIRIE = {'map': False, 'bannerY': 3.25, 'plate': False}
BOUQ = {'touch': {'R': ['torso', 0.05, 0.4, 0.3, 1, 0.02], 'L': ['torso', -0.05, 0.4, 0.3, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
READ9 = lambda j: {'reach': {'R': [0.15, 1.35, r(MA[2] + 0.4), 1, 0.04], 'L': [-0.15, 1.35, r(MA[2] + 0.4), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'open' if j % 2 else 'line'}}
st.shot('S09', 'mairie', setOpts=MAIRIE, actors=[
        act('mec', GR, 5, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0), *SWAY(0.05, r(D9 - 0.1), 0.4, [(0.0, {**DEAD, 'mouth': 'line'})]), *BL(1.05, {**DEAD, 'mouth': 'line'}, 0.16)]),
        act('femme', BR, -5, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={**BOUQ, 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.0), k(0.5, look=[r(GR[0] + 0.25), 2.05, GR[2]]),
            k(0.55, toon={**BOUQ, 'face': {'lid': 0.1, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.1), k(1.15, look='camera'), k(1.15, toon={**BOUQ, 'face': {'lid': 1.0, 'mouth': 'bigsmile'}}, toonDur=0.12)]),   # a look at the phone on his ear, and she beams
        act('maire', MA, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.35, r(MA[2] + 0.4)]), k(0.0, toon=READ9(1), toonDur=0.0), *[k(r(0.15 + 0.22 * j), toon=READ9(j), toonDur=0.1) for j in range(6)], k(1.2, look=[GR[0], 2.1, GR[2]])])],
        props=[TEL('tel9'), NOTES('mus9', size=0.2, rate=3.5, life=0.95, dx=0.5, dy=0.38), P('voile9', 'bridalVeil', on={'actor': 'femme', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}), P('bouq9', 'bouquet', on={'actor': 'femme', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}),
               P('reg9', 'paperSheet', on={'actor': 'maire', 'hand': 'R', 'offset': [0.0, 0.0, 0.03], 'face': 'camera'}, opts={'w': 0.3, 'h': 0.22, 'lines': ['REGISTRE']})],
        cams=[FC(0.0, [0.0, 1.5, 4.3], [[r(GR[0] - 0.45), 0.15, GR[2]], [r(BR[0] + 0.5), 0.15, BR[2]], [0.0, 3.55, -2.55], [r(GR[0] - 0.45), 2.4, GR[2]], [r(BR[0] + 0.5), 2.4, BR[2]]], top=0.08, bottom=0.82)])   # (pass 2) both of them whole, the banner over them
st.cue('sfx:bell', 'S09', 0.2, 0.2)

# 10: his wife said yes on the speaker. Three quarters to us, she bends at the waist and stretches up to the phone on his ear, her mouth on it, and
#     says it into it: OUI ! bursts out of the phone; he does not move; she eases back up; behind her shoulder the mayor claps
D10 = st.dur('S10'); OUI10 = 0.75; BR10 = [-0.02, 0, 0.08]; MA10 = [1.15, 0, -1.3]   # (stills 2) she stands three quarters to us: in profile a box head shows no mouth; (pass 3) closer to him (0.27)
# (pass 3) u 0..1: how far she reaches for the phone: the spine bows forward and toward her right (his side) and stretches, the neck tips her mouth onto it
LEAN10 = lambda u, f, sq=None: {**BOUQ, 'bend': {'spine': [r(0.42 * u), r(0.3 * u), 0, r(1 + 0.3 * u), None], 'neck': [r(0.25 * u), r(0.2 * u), 0, 1, None]}, 'face': f, **({'sq': sq} if sq else {})}
CLAP10 = lambda j: {'touch': {'R': ['torso', r(-0.03 if j % 2 else -0.16), 0.52, 0.3, 1, 0.04], 'L': ['torso', r(0.03 if j % 2 else 0.16), 0.52, 0.3, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}
st.shot('S10', 'mairie', setOpts=MAIRIE, actors=[
        act('mec', GR, 5, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0), FK(r(OUI10 + 0.1), {'lid': 0.3, 'mouth': 'line', 'gx': 0.8}), FK(r(OUI10 + 0.55), {**DEAD, 'mouth': 'line'}, 0.12),
            *BL(1.7, {**DEAD, 'mouth': 'line'})]),                                                                                       # one look aside at the yes, and back to us
        act('femme', BR10, -45, 'stand', 'happy', keys=[k(0.0, look=[-1.6, 1.8, 3.0]), k(0.0, toon=LEAN10(0.0, {'lid': 0.2, 'mouth': 'smile'}), toonDur=0.0),
            k(0.26, toon=LEAN10(1.0, {'lid': 0.2, 'mouth': 'smile'}), toonDur=0.33, toonEase='inOut'),                                    # (pass 3) she bends to the phone, her mouth on it (later: earlier her head crossed his face while he still stood close)...
            k(r(OUI10 - 0.13), toon=LEAN10(0.92, {'lid': 0.6, 'mouth': 'o'}, [1.04, 0.95, 1.04]), toonDur=0.08),                          # ...takes a breath...
            k(OUI10, toon=LEAN10(1.05, {'lid': 0.0, 'mouth': 'scream', 'brow': 0.8}, [0.95, 1.07, 0.95]), toonDur=0.05, toonEase='out'),  # ...OUI ! into it
            k(r(OUI10 + 0.4), toon=LEAN10(1.0, {'lid': 0.1, 'mouth': 'bigsmile'}), toonDur=0.15),
            k(r(OUI10 + 0.6), toon=LEAN10(0.3, {'lid': 0.1, 'mouth': 'bigsmile'}), toonDur=0.5, toonEase='inOut'),                        # she eases back up
            k(r(OUI10 + 1.2), toon=LEAN10(0.2, {'lid': 1.0, 'mouth': 'bigsmile'}), toonDur=0.2)]),
        act('maire', MA10, -15, 'stand', 'happy', keys=[k(0.0, look=[0.0, 2.0, 0.3]), k(0.0, toon=CLAP10(0), toonDur=0.0), *[k(r(OUI10 + 0.15 + 0.13 * j), toon=CLAP10(j + 1), toonDur=0.07) for j in range(10)]])],
        props=[TEL('tel10'), NOTES('mus10', size=0.16, t1=r(OUI10 - 0.4), life=0.95, dx=0.3, dy=0.38), P('voile10', 'bridalVeil', on={'actor': 'femme', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}),
               P('bouq10', 'bouquet', on={'actor': 'femme', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}),
               P('oui10', 'voiceBubble', on={'actor': 'mec', 'joint': 'head', 'offset': [0.26, 0.42, 0.22], 'face': 'camera'}, opts={'at': OUI10, 'until': r(OUI10 + 1.0), 'text': 'OUI !', 'w': 0.66, 'fill': '#FFD83A', 'ink': '#D22B2B', 'jagK': 0.72})],   # (pass 3) the yes bursts out of the phone, its tail on it (it floated over the banner)
        cams=[FC(0.0, [-0.6, 1.75, 3.0], [[GR[0], 2.45, GR[2]], [r(GR[0] - 0.25), 1.9, GR[2]], [0.45, 1.6, BR10[2]], [r(MA10[0] + 0.22), 2.3, MA10[2]], [0.35, 2.7, 0.5], [0.0, 1.4, 0.3]], top=0.14, bottom=0.76)])   # (pass 3) from the left front: her head beside the phone, not in front of it or of his face   # (pass 2) face on to him; (after stills 4, by calculation) tighter than S09: cut at the belt, his far shoulder out of frame
st.cue('sfx:pop', 'S10', OUI10, 0.2); st.cue('sfx:fanfare', 'S10', r(OUI10 + 0.2), 0.15)

# 11: the music became the national anthem. A ceremony in the street: him in front, in the middle, the phone on his ear, his head rocking on it;
#     behind him the flag climbs its pole from above their heads, a column of notes rises from the phone up along it; on « hymne » the two soldiers
#     and the official snap a salute together, hand to the brow, with a little bounce (HYMNE)
D11 = st.dur('S11'); POLE = [0.55, 0, -2.4]; H11 = [0.0, 0, 0.6]   # (pass 3) x 0.8: a cloud sat on the pole
HEART = lambda f: {'touch': {'R': ['torso', -0.08, 0.45, 0.25, 1, 0.02]}, 'hands': {'R': 'open'}, 'face': f}
SAL11 = 0.98                                                     # (pass 3) « l'hymne »: they all salute on it
ATT = lambda f: {'face': f}                                      # at attention, arms down
SALUTE = lambda f, up=0.0, sq=None: {'touch': {'R': ['head', -0.11, r(0.33 + up), 0.13, 1, 0.02, [-1, 0.35, 0.25]]}, 'hands': {'R': 'open'}, 'face': f, **({'sq': sq} if sq else {})}   # the right hand flat at the brow, the elbow out
st.shot('S11', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', H11, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(), toonDur=0.0),
            *SWAY(0.05, r(D11 - 0.1), 0.42, [(0.0, {**DEAD, 'mouth': 'line'}), (0.5, {'lid': 0.3, 'mouth': 'line', 'gx': 0.6, 'gy': -0.8}), (1.5, {**DEAD, 'mouth': 'line'})]),   # (pass 3) his head rocks on his anthem
            *BL(1.85, {**DEAD, 'mouth': 'line'})]),                                                                                       # his eyes follow his notes up, and come back to us
        *[act(oid, [x, 0, z], ry, 'stand', 'determined', keys=[k(0.0, look=[r(POLE[0] * 0.5), 2.2, 2.0]), k(0.0, toon=ATT({'lid': 0.3, 'mouth': 'line'}), toonDur=0.0),
            k(r(SAL11 - 0.1), toon=ATT({'lid': 0.3, 'mouth': 'line', 'brow': -0.3}), toonDur=0.06, toonEase='in'),                      # (pass 3) a little dip...
            k(SAL11, toon=SALUTE({'lid': 0.2, 'mouth': 'line', 'brow': -0.4}, 0.04, [0.97, 1.04, 0.97]), toonDur=0.07, toonEase='out'),   # ...and the salute snaps up, all three together
            k(r(SAL11 + 0.1), toon=SALUTE({'lid': 0.2, 'mouth': 'line', 'brow': -0.4}, -0.02, [1.02, 0.98, 1.02]), toonDur=0.08),        # the bounce
            k(r(SAL11 + 0.2), toon=SALUTE({'lid': 0.25, 'mouth': 'line', 'brow': -0.4}), toonDur=0.08),
            *BL(r(1.5 + 0.15 * i), {'lid': 0.25, 'mouth': 'line', 'brow': -0.4})])
          for i, (oid, x, z, ry, pre) in enumerate([('off1', -0.85, -1.4, 8, 'politique'), ('sold1', 0.8, -1.2, -5, 'cop'), ('sold2', 1.35, -1.9, -8, 'cop')])]],
        props=[TEL('tel11'), NOTES('mus11', rate=4.0, size=0.27, dy=1.5, dx=0.04, life=1.7, sway=0.1), P('mat11', 'flagPole', pos=POLE, opts={'h': 5.0, 'w': 1.1, 'raise': [0.1, r(D11 - 0.3)], 'y0': 2.5})],   # (pass 3) from above their heads (it started behind them)
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

# 13: the children whistle it at school. A classroom: three children in a row in front of the board, facing us, whistle it, big white chalk notes
#     over their heads on the green board, MUSIQUE above them; the teacher behind them beats time with a ruler
D13 = st.dur('S13'); KIDS = [('el1', -0.85), ('el2', -0.27), ('el3', 0.31)]; ZK = -2.5; PROF = [0.92, 0, -3.1]   # (stills 2) the teacher behind them, between two heads: beside them she widened the frame past the first desks
st.shot('S13', 'classroom', setOpts={'board': 'MUSIQUE', 'board2': "L'hymne national", 'board3': 'la la la la'}, actors=[
        *[act(eid, [x, 0, ZK], 0, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'kiss', 'mouthW': 0.7, 'mouthH': 0.7, 'cheeks': 0.6}}, toonDur=0.0),
            *[k(r(0.08 + 0.28 * j + 0.09 * i), toon={'face': {'lid': 0.3 if j % 3 else 1.0, 'mouth': 'kiss', 'mouthW': 0.7, 'mouthH': 0.7, 'cheeks': 0.6 if j % 2 else 0.9, 'puff': 0.5}, 'sq': [0.97, 1.06, 0.97] if (j + i) % 2 else [1.04, 0.95, 1.04]}, toonDur=0.14, toonEase='inOut') for j in range(7)]])
          for i, (eid, x) in enumerate(KIDS)],
        act('prof', PROF, -90, 'stand', 'happy', keys=[k(0.0, look=[-0.5, 2.05, PROF[2]]), *[k(r(0.05 + 0.24 * j), toon={'reach': {'R': [r(PROF[0] - 0.45 + (0.12 if j % 2 else -0.05)), r(2.15 + (0.2 if j % 2 else -0.1)), r(PROF[2] + 0.1), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smile'}}, toonDur=0.14, toonEase='inOut') for j in range(8)]])],
        props=[*[P(f'n13{i}', 'holdNotes', on={'actor': eid, 'joint': 'head', 'offset': [0.0, 0.62, 0.1], 'face': 'camera'}, opts={'rate': 2.2, 'size': 0.2, 'from': r(-1.0 + 0.15 * i), 'dy': 0.32, 'dx': 0.12, 'side': (-1, 1, 1)[i], 'color': '#FFFFFF', 'halo': '#2B3A33'}) for i, (eid, x) in enumerate(KIDS)],   # (pass 3) chalk white, kept low on the green board (they rose onto the cream wall)
               P('regle13', 'slab', on={'actor': 'prof', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, opts={'w': 0.035, 'h': 0.5, 'd': 0.012, 'color': '#E2B53C'})],
        cams=[FC(0.0, [0.78, 1.8, 0.1], [[-1.05, 1.5, ZK], [0.5, 1.5, ZK], [-0.27, 0.75, ZK], [0.0, 2.62, -3.55], [r(PROF[0] + 0.2), 2.35, PROF[2]]], top=0.12, bottom=0.74, inside=(-4.0, 4.0, 0.5, 3.0, -3.3, 6.0))])   # (pass 2) the children facing us, the board behind; (pass 3) above their heads, looking down a little: the board's title clears them
st.cue('sfx:whistle', 'S13', 0.1, 0.25)

# 14: yesterday someone picked up. Ten years on, on his sofa, the phone on his ear: click: the notes stop and hang in the air; his eyes slide to the
#     phone; the notes drop; he squashes; and the biggest take of the film: his eyes shoot out on long stalks, his jaw drops, the stalks overshoot and
#     wobble back
D14 = st.dur('S14'); CLK14 = 0.4; HANG14 = 0.24; TAK14 = 0.82; AGE = {'low': 0.32}   # (pass 3) the notes hang 7 frames, then drop; the take after the squash   # ten years on: grey hair (cast), heavier lower lids; the gloom over his eyes (shadow) only before the click and at the very end
A = lambda **f: {**AGE, **f}
SITCAM = lambda frm, extra=(), **kw: FC(0.0, frm, [[SIT[0], 1.92, SIT[2]], [SIT[0], 0.95, SIT[2]], [0.48, 1.6, SIT[2]], [-0.42, 1.6, SIT[2]], *extra], **kw)
st.shot('S14', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(A(lid=0.5, mouth='line', shadow=0.85)), toonDur=0.0),
            FK(r(CLK14 + 0.03), A(lid=0.45, mouth='line', shadow=0.6)),                                                                             # (pass 3) the click: the notes hang still...
            FK(r(CLK14 + 0.12), A(lid=0.2, mouth='line', gx=1.0, brow=0.4, shadow=0.2), 0.1),                                                        # ...his eyes slide to the phone...
            k(r(TAK14 - 0.14), toon=FREE(A(lid=0.9, mouth='clench', brow=-0.7, gx=1.0), {'sq': [1.1, 0.84, 1.1]}), toonDur=0.07, toonEase='in'),     # ...the notes drop, he squashes (4 frames)...
            k(TAK14, toon=FREE(A(lid=0.0, eye=0.5, pop=1.0, popLen=0.42, stalkYaw=-0.55, stalkPitch=-0.3, stalkRed=0.5, stalkBow=0.04, jaw=0.85, jawLen=0.55, mouth='scream', brow=1.0), {'sq': [0.9, 1.16, 0.9]}), toonDur=0.05, toonEase='out'),   # ...THE take
            *[k(r(TAK14 + 0.07 + 0.08 * j), toon=FREE(A(lid=0.0, eye=0.5, pop=1.0, popLen=r(0.42 - 0.1 * (-0.5) ** (j + 1)), stalkYaw=r(-0.55 + 0.22 * (-0.6) ** j), stalkPitch=r(-0.3 + 0.12 * (-0.6) ** j), stalkRed=0.5, stalkBow=0.04,
                jaw=0.85, jawLen=0.55, mouth='scream', brow=1.0), {'sq': [1.0, 1.0, 1.0] if j else [1.03, 0.97, 1.03]}), toonDur=0.07, toonEase='inOut') for j in range(4)],   # the stalks overshoot and wobble back
            k(r(TAK14 + 0.62), toon=FREE(A(lid=0.0, eye=0.5, pop=1.0, popLen=0.4, stalkYaw=-0.5, stalkPitch=-0.25, stalkRed=0.5, stalkBow=0.04, jaw=0.8, jawLen=0.55, mouth='scream', brow=1.0, pupilShake=0.8)), toonDur=0.2)])],   # held, the pupils shivering
        props=[TEL('tel14', OLD), NOTES('mus14', OLD, t0=-2.0, rate=3.5, size=0.14, stopAt=CLK14, hang=HANG14, drop=11)],
        cams=[SITCAM([0.4, 1.5, 0.3], [[0.85, 2.35, SIT[2]]], top=0.16, bottom=0.74)])
st.cue('sfx:click', 'S14', CLK14, 0.35); st.cue('sfx:boing', 'S14', TAK14, 0.3); st.cue('sfx:gasp', 'S14', r(TAK14 + 0.05), 0.25)

# 15: he cried for joy... Close: his face crumples, tears jetting out sideways, his hands clasped, his shoulders heaving, the phone still on his ear
D15 = st.dur('S15')
JOY = {'touch': {'R': ['torso', -0.04, 0.45, 0.28, 1, 0.02], 'L': ['torso', 0.04, 0.45, 0.28, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
SOB = lambda j: {**JOY, 'face': A(tears=1.0, mouth='scream' if j % 2 else 'sob', brow=0.9, lid=0.85), 'sq': [r(1.0 + (0.04 if j % 2 else 0.0)), r(1.0 - (0.05 if j % 2 else -0.02)), r(1.0 + (0.04 if j % 2 else 0.0))], 'bend': {'spine': [r(0.14 if j % 2 else -0.04), 0, 0, 1, None]}}
TEARS = lambda pid, r_=0.026, rate=24, sp=1.9: P(pid, 'tearFountain', on={'actor': OLD, 'joint': 'head', 'offset': [0.0, 0.24, 0.17]}, opts={'at': 0.0, 'dx': 0.09, 'rate': rate, 'speed': sp, 'r': r_})
st.shot('S15', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SOB(0), toonDur=0.0), *[k(r(0.08 + 0.17 * j), toon=SOB(j + 1), toonDur=0.09, toonEase='inOut') for j in range(8)]])],
        props=[TEL('tel15', OLD), TEARS('larmes15')],
        cams=[SITCAM([0.45, 1.2, -1.2], [[0.66, 1.75, SIT[2]], [-0.62, 1.75, SIT[2]]], top=0.16, bottom=0.74)])   # low, from the phone side: the tears against the wall
st.cue('sfx:sniff', 'S15', 0.2, 0.25); st.cue('sfx:sniff', 'S15', 0.7, 0.2)

# 16: ...live on television. Wider: two light grey TV cameras on tripods, three quarters to us (lens, viewfinder, TV plate, red light), push in on
#     him from either side; he sobs in the middle, a reporter's INFO mic comes in from the right (only her sleeve shows); over him a red EN DIRECT sign
D16 = st.dur('S16'); MIC16 = [0.4, 1.4, r(SIT[2] + 0.32)]; ZC16 = r(SIT[2] + 1.3)   # (stills 2) no operators (a back filled a quarter of the frame): two low cameras in the lower corners, the mic from the right
MICK = lambda p, b, f: {'reach': {'R': [*p, 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [b, 0, 0, 1, None]}, 'face': f}
st.shot('S16', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SOB(0), toonDur=0.0), *[k(r(0.06 + 0.17 * j), toon=SOB(j + 1), toonDur=0.09, toonEase='inOut') for j in range(8)]]),
        act('repo', [1.55, 0, r(SIT[2] + 0.45)], -100, 'stand', 'neutral',   # (pass 3) further right: her head out of frame (a sliver of it read as a fault)
            keys=[k(0.0, look=[0.0, 1.6, SIT[2]]), k(0.0, toon=MICK([0.8, 1.5, r(SIT[2] + 0.4)], 0.0, {'lid': 0.2, 'mouth': 'open'}), toonDur=0.0),
            k(0.08, toon=MICK(MIC16, 0.3, {'lid': 0.1, 'mouth': 'open', 'brow': 0.5}), toonDur=0.3, toonEase='out'),                                  # she leans in with the mic...
            k(0.6, toon=MICK([r(MIC16[0] - 0.05), r(MIC16[1] - 0.06), MIC16[2]], 0.36, {'lid': 0.1, 'mouth': 'o', 'brow': 0.6}), toonDur=0.25, toonEase='inOut'),   # ...and it follows his sobs
            k(0.95, toon=MICK([r(MIC16[0] + 0.02), r(MIC16[1] + 0.04), MIC16[2]], 0.3, {'lid': 0.1, 'mouth': 'open', 'brow': 0.6}), toonDur=0.25, toonEase='inOut')])],
        props=[TEL('tel16', OLD), TEARS('larmes16', 0.024, 22, 1.7),
               P('mic16', 'pressMic', on={'actor': 'repo', 'hand': 'R', 'offset': [0.0, -0.02, 0.04]}, scale=1.5, opts={'text': 'INFO', 'color': '#C8322A'}),
               *[P(f'tv16{j}', 'newsCamera', pos=[x, 0, -2.45], ry=r(-70 if x > 0 else 70), opts={'h': 0.85, 'logo': 'TV', 'blink': 0.7 + 0.1 * j},
                   keys=[k(0.0, to=[r(x * 0.88), 0, -2.5], dur=D16, ease='inOut'), k(r(0.2 + 0.3 * j), rotTo=[0, r(math.radians(-82 if x > 0 else 82), 4), 0], dur=0.5, ease='inOut')]) for j, x in enumerate((-0.95, 0.95))],   # (pass 3) at his sides, three quarters to us (lens, plate, red light): they push in and pan on him
               P('direct16', 'signBoard', pos=[0.0, 0, -3.45], opts={'text': 'EN DIRECT', 'bg': '#D22B2B', 'fg': '#FFFFFF', 'w': 1.15, 'h': 0.32, 'height': 2.02})],
        cams=[FC(0.0, [0.0, 1.45, -0.5], [[SIT[0], 1.92, SIT[2]], [SIT[0], 0.95, SIT[2]], [0.0, 2.44, -3.45], [-0.95, 1.4, -2.45], [0.95, 1.4, -2.45]], top=0.12, bottom=0.76)])   # (pass 2) between the two cameras; (pass 3) wide enough for the two TV cameras at his sides
st.cue('sfx:click', 'S16', 0.2, 0.15)

# 17: the voice said... Close on the phone on his ear: a flat electronic voice, a jagged little bubble with its tail on the phone; his eyes slide to it
D17 = st.dur('S17')
st.shot('S17', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(A(lid=0.0, eye=0.3, mouth='o', brow=0.6)), toonDur=0.0),
            FK(0.22, A(lid=0.0, eye=0.35, mouth='o', brow=0.9, gx=1.0), 0.1), FK(0.75, A(lid=0.0, eye=0.35, mouth='o', brow=0.9, gx=1.0, pupilShake=0.6), 0.1)])],   # his eyes slide to the voice
        props=[TEL('tel17', OLD), P('bulle17', 'voiceBubble', on={'actor': OLD, 'joint': 'head', 'offset': [0.3, 0.44, 0.02], 'face': 'camera'}, opts={'at': 0.1, 'text': 'BIP', 'w': 0.46})],
        cams=[FC(0.0, [0.85, 1.7, -1.35], [[SIT[0], 1.3, SIT[2]], [0.8, 2.22, SIT[2]], [-0.2, 1.6, SIT[2]], [0.85, 1.9, SIT[2]], [SIT[0], 1.9, SIT[2]]], top=0.18, bottom=0.7)])   # (pass 2) the ear and the phone above the middle, the chin above the captions
st.cue('sfx:ding', 'S17', 0.1, 0.15)

# 18: ...for an adviser, press one. His hand goes up to the phone and pulls: the ear and the head stretch after it like taffy, further than when he
#     first pulled, and hold there trembling; POP, it comes free, the head springs back in three smaller and smaller bounces; he holds the phone in
#     front of him, the keypad to us, and his eyes drop to it
D18 = st.dur('S18'); POP18 = 0.58; CAR18 = 0.24   # (pass 3) the pop later: the stretch has time to grow and hold
def OFF18(u, s, sy, f, lay=0.0): return {'touch': {'L': MIX(GRIP, FGRIP, eio(min(1.0, max(0.0, u))))}, 'hands': {'L': 'grip'}, 'scl': {'head': [s, sy, 1.0]}, 'lay': [0, lay], 'face': f}
st.shot('S18', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=FREE(A(lid=0.0, eye=0.3, mouth='o')), toonDur=0.0),
            k(0.03, toon=HOLD(A(lid=0.2, mouth='clench', brow=-0.4)), toonDur=0.14, toonEase='inOut'),                                    # the hand goes up to the phone
            k(0.19, toon=OFF18(0, 0.9, 1.05, A(lid=0.3, mouth='clench', brow=-0.6, gx=0.8)), toonDur=0.06),                              # an anticipation...
            k(0.25, toon=OFF18(0, 1.5, 0.94, A(lid=0.15, mouth='grimace', brow=-0.8, gx=0.8, sweat=1.0), -0.03), toonDur=0.08, toonEase='in'),     # ...he pulls: the head is dragged after the phone...
            k(0.36, toon=OFF18(0, 2.6, 0.8, A(lid=0.1, mouth='grimace', brow=-0.9, gx=0.8, sweat=1.0, tremble=1.0), -0.1), toonDur=0.1, toonEase='out'),   # ...to 2.6 times its width (2.25 in S07)
            *[k(r(0.46 + 0.04 * j), toon=OFF18(0, 2.68 if j % 2 else 2.52, 0.8, A(lid=0.1, mouth='grimace', brow=-0.9, gx=0.8, sweat=1.0, tremble=1.0, pupilShake=1.0), -0.1), toonDur=0.035, toonEase='linear') for j in range(3)],   # held, trembling
            *[k(r(POP18 + 0.06 * j), toon=OFF18((0.06 * (j + 1)) / CAR18, s_, sy_, A(lid=0.0, eye=0.5, mouth='O', brow=1.0), l_), toonDur=0.06, toonEase='linear')
              for j, (s_, sy_, l_) in enumerate([(0.66, 1.24, 0.05), (1.26, 0.9, -0.02), (0.85, 1.08, 0.01), (1.1, 0.95, 0.0), (0.96, 1.02, 0.0), (1.0, 1.0, 0.0)])],   # POP: it comes free, the head springs back: three smaller and smaller bounces
            FK(r(POP18 + 0.4), A(lid=0.3, mouth='line', gy=0.85), 0.1),                                                                  # his eyes drop to the screen
            *BL(1.28, A(lid=0.3, mouth='line', gy=0.85)),
            k(1.42, toon=SHOW(A(lid=0.3, mouth='line', gy=0.85), TAP0), toonDur=0.25, toonEase='inOut')])],                              # the other index comes up over the keypad
        props=[TEL('tel18', OLD, keys=CARRY(OLD, POP18, CAR18, EAR, FRONT), keypad=1), BURST('pop18', [0.55, 1.85, r(SIT[2] + 0.1)], POP18, 'POP !', 0.42, 0.4)],
        cams=[SITCAM([0.25, 1.1, -0.5], [[0.75, 2.05, SIT[2]], [0.15, 0.78, r(SIT[2] + 0.45)]], top=0.16, bottom=0.74)])   # lower and closer than S14
st.cue('sfx:stretch', 'S18', 0.25, 0.3); st.cue('pop', 'S18', POP18, 0.3); st.cue('sfx:boing', 'S18', r(POP18 + 0.06), 0.2)

# 19: he pressed one. Insert, from below: the red phone big in his hand, its keypad square to us; one finger comes in from the lower right, presses the
#     1 and lifts: the 1 stays green, in the clear (UN)
D19 = st.dur('S19'); PRESS19 = 0.55; PAD19 = [0.0, 1.45, -1.2]
st.shot('S19', 'livingRoom', setOpts=LR, actors=[],
        props=[P('pad19', 'phoneKeypad', pos=PAD19, face='camera', scale=0.3, opts={'label': 'SERVICE CLIENT', 'pressAt': PRESS19, 'case': '#E3241B', 'hold': 1, 'finger': 1})],
        cams=[FC(0.0, [0.04, 1.0, -0.5], [[-0.09, 1.62, PAD19[2]], [0.09, 1.62, PAD19[2]], [-0.09, 1.28, PAD19[2]], [0.12, 1.28, PAD19[2]]], top=0.22, bottom=0.72, lenses=range(16, 60))])   # (pass 2) no face behind it: the wall over the sofa
st.cue('sfx:click', 'S19', PRESS19, 0.35)

# 20: the music started again. The notes pour out of the phone in his hand; his face falls and he flattens into the sofa; he re-inflates as he puts
#     it back on his ear, and looks at us, deadpan; a long slow blink
D20 = st.dur('S20'); BACK20 = 0.5
st.shot('S20', 'livingRoom', setOpts=LR, actors=[act(OLD, SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SHOW(A(lid=0.3, mouth='line', gy=0.85)), toonDur=0.0),
            FK(0.16, A(lid=0.1, mouth='o', gy=0.85, brow=0.7)),                                                                          # the notes: his brows go up...
            k(0.3, toon=SHOW(A(lid=0.6, mouth='line', gy=0.85, brow=-0.3, shadow=0.9), None, {'sq': [1.2, 0.66, 1.2]}), toonDur=0.14, toonEase='in'),   # (pass 3) ...and he flattens into the sofa, the gloom over his eyes
            k(BACK20, toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9), {'sq': [1.12, 0.8, 1.12]}), toonDur=0.2, toonEase='inOut'),        # back on the ear, re-inflating...
            k(r(BACK20 + 0.24), toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9), {'sq': [0.95, 1.07, 0.95]}), toonDur=0.1, toonEase='out'), # ...overshoot...
            k(r(BACK20 + 0.36), toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9), {'sq': [1.02, 0.98, 1.02]}), toonDur=0.08), k(r(BACK20 + 0.46), toon=HOLD(A(lid=0.5, mouth='line', shadow=0.9)), toonDur=0.1),   # ...and settles
            *BL(1.3, A(lid=0.5, mouth='line', shadow=0.9)), k(1.72, toon=HOLD(A(lid=1.0, mouth='line', shadow=0.9)), toonDur=0.18, toonEase='inOut'), k(1.98, toon=HOLD(A(lid=0.55, mouth='line', shadow=0.9)), toonDur=0.16)])],   # a long, slow blink
        props=[TEL('tel20', OLD, start=FRONT, keys=CARRY(OLD, BACK20, 0.3, FRONT, EAR), keypad=1), NOTES('mus20a', OLD, t0=0.08, t1=r(BACK20 - 0.05), rate=5.0, size=0.14, off=[0.2, -0.2, 0.46]),
               NOTES('mus20b', OLD, t0=r(BACK20 + 0.28), rate=4.0, size=0.14)],
        cams=[SITCAM([0.8, 1.55, -1.0], [[0.72, 2.3, SIT[2]]], top=0.14, bottom=0.76)])   # three quarters from the phone side   # wider, from the phone side: the end hold
st.cue('sfx:ding', 'S20', 0.1, 0.12)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
FIRE = {'preset': 'pompier', 'suit': '#23304E', 'pants': '#23304E', 'hatColor': '#E9EDF3', 'bandColor': '#F2D23C', 'bandH': 0.06,   # (pass 3) chrome helmets, yellow reflective bands (red ones read as nothing)
        'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
st.write("Le service client", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec', OLD], extra_cast={
    'mec': MEC, OLD: {**MEC, 'hairColor': '#80868F'},   # (pass 3) mid-grey: the pale grey read as a white bandage
    'pomp1': {**FIRE, 'seed': 731}, 'pomp2': {**FIRE, 'seed': 732},
    'femme': {'preset': 'femme', 'seed': 733, 'suit': '#F7F5EF', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 734, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'suit': '#26365F', 'lapel': '#26365F', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off1': {'preset': 'politique', 'seed': 735, 'suit': '#33363D', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold1': {'preset': 'cop', 'seed': 737, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold2': {'preset': 'cop2', 'seed': 738, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{mid: {'preset': 'officiel', 'seed': 740 + j, 'suit': '#8E2B2B', 'hat': 'copcap', 'hatColor': '#8E2B2B', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j, (mid, _, _, _) in enumerate(BAND)},
    **{eid: {'preset': 'gamin', 'seed': 750 + j, 'suit': c_, 'glasses': False, 'build': {'headScale': 1.25}, 'toon': EX} for j, ((eid, _), c_) in enumerate(zip(KIDS, ['#E0413A', '#3A9BDC', '#E8A33C']))},
    'prof': {'preset': 'madame', 'seed': 755, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'repo': {'preset': 'journaliste', 'seed': 756, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
