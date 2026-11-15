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
tearFountain, tvCamera, pressMic, hicBurst, flag, signBoard)."""
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
ME = [0.0, 0, -0.6]                                  # him in his living room, facing us
EAR = {'touch': {'R': ['face', 0.2, 0.08, 0.02, 1, 0.02]}, 'hands': {'R': 'grip'}}   # the phone held to his right ear
PH = lambda pid, who='mec', hand='R': P(pid, 'smartPhone', on={'actor': who, 'hand': hand, 'offset': [0.0, 0.0, 0.03]}, opts={'case': '#E0413A'})   # a red phone (a dark one melted into his suit)
NOTES = lambda pid, actor='mec', t0=0.0, t1=99.0, rate=3.0, size=0.1, side=1: P(pid, 'holdNotes', on={'actor': actor, 'joint': 'head', 'offset': [0.32, 0.12, 0.0]}, face='camera', opts={'from': t0, 'until': t1, 'rate': rate, 'size': size, 'side': side})
HOLD = lambda f=None, extra=None: {**EAR, 'face': f or {**DEAD, 'mouth': 'line'}, **(extra or {})}

for g_ in [('S07', 0.8, 'mec', 'stuck'), ('S10', 1.0, 'femme', 'oui'), ('S11', 1.2, 'mec', 'anthem'), ('S14', 0.7, 'mec', 'click'), ('S15', 0.6, 'mec', 'tears'), ('S19', 0.7, 'mec', 'press'), ('S20', 0.9, 'mec', 'end')]:
    st.gag(*g_)
st.card('S04', 'DIX ANS', at=0.3)
st.card('S11', 'HYMNE', at=0.6)
st.card('S19', 'UN', at=0.55)

# 1: the hook. His living room: he lifts his red phone to his ear, deadpan
D1 = st.dur('S01')
st.shot('S01', 'livingRoom', actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.25, 1.4, -0.2]), k(0.0, toon={'touch': {'R': ['torso', 0.12, 0.35, 0.3, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.0),
            k(0.6, toon=HOLD({'lid': 0.3, 'mouth': 'line'}), toonDur=0.25, toonEase='inOut'), k(0.7, look='camera'), k(1.4, toon=HOLD({'lid': 1.0, 'mouth': 'line'}), toonDur=0.06), k(1.5, toon=HOLD(), toonDur=0.08)])],
        props=[PH('tel1')],
        cams=[FC(0.0, [0.5, 1.6, 2.4], [[ME[0], 2.5, ME[2]], [ME[0], 1.1, ME[2]], [0.45, 2.0, ME[2]], [-0.4, 2.0, ME[2]]], top=0.14, bottom=0.74)])
st.cue('sfx:click', 'S01', 0.2, 0.15); st.cue('sfx:ring', 'S01', 0.9, 0.12)

# 2: they put him on hold. Close: a click, and the hold music pours out of the phone, notes floating up past his head; his eyes go up to the ceiling
D2 = st.dur('S02')
st.shot('S02', 'livingRoom', actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0), k(0.45, toon=HOLD({'lid': 0.4, 'mouth': 'line', 'gy': -0.6}), toonDur=0.15), k(0.45, look=[0.0, 3.4, 0.0])])],
        props=[PH('tel2'), NOTES('mus2', t0=0.3)],
        cams=[FC(0.0, [0.3, 2.0, 1.2], [[ME[0], 2.55, ME[2]], [ME[0], 1.55, ME[2]], [0.6, 2.4, ME[2]], [-0.35, 2.0, ME[2]]], top=0.14, bottom=0.74)])
st.cue('sfx:click', 'S02', 0.2, 0.2); st.cue('sfx:ding', 'S02', 0.32, 0.12)

# 3: the hold music... Wider: he stands by the wall, the phone at his ear, notes rising; a calendar on the wall beside him
D3 = st.dur('S03'); CAL = [0.75, 1.75, -2.08]
st.shot('S03', 'livingRoom', actors=[act('mec', [0.1, 0, -1.4], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0), k(0.8, toon=HOLD({'lid': 1.0, 'mouth': 'line'}), toonDur=0.07), k(0.92, toon=HOLD(), toonDur=0.08)])],
        props=[PH('tel3'), NOTES('mus3', rate=3.5), P('cal3', 'yearCalendar', pos=CAL, opts={'years': [2016, 2016]})],
        cams=[FC(0.0, [0.6, 1.5, 2.6], [[0.1, 2.5, -1.4], [0.1, 0.0, -1.4], [CAL[0], 2.1, CAL[2]], [CAL[0], 1.4, CAL[2]]], top=0.14, bottom=0.78)])

# 4: ...has been playing for ten years. Close on the calendar: its pages fly off year after year, 2016 to 2026 (DIX ANS)
D4 = st.dur('S04')
st.shot('S04', 'livingRoom', actors=[],
        props=[P('cal4', 'yearCalendar', pos=CAL, opts={'years': [2016, 2026], 'flipAt': 0.05, 'dur': r(D4 - 0.25)}), NOTES('mus4', 'mec', 0.0, 99.0)],
        cams=[FC(0.0, [0.8, 1.75, -0.9], [[CAL[0], 2.15, CAL[2]], [CAL[0], 1.35, CAL[2]], [r(CAL[0] - 0.35), 1.75, CAL[2]], [r(CAL[0] + 0.35), 1.75, CAL[2]]], top=0.2, bottom=0.76)])
st.cue('sfx:paper', 'S04', 0.1, 0.2); st.cue('sfx:paper', 'S04', 0.45, 0.2); st.cue('sfx:paper', 'S04', 0.8, 0.2)

# 5: he knows every note by heart. Eyes shut, swaying, he conducts along with one finger of his free hand, mouthing the tune
D5 = st.dur('S05')
CND = lambda j: HOLD({'lid': 1.0, 'mouth': 'O' if j % 2 else 'line'}, {'reach': {'L': [r(-0.45 + 0.1 * math.sin(j * 1.7)), r(1.95 + (0.12 if j % 2 else -0.05)), -0.3, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'point'}, 'bend': {'neck': [0, 0, r(0.12 if j % 2 else -0.12), 1, None]}})
st.shot('S05', 'livingRoom', actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=CND(0), toonDur=0.0), *[k(r(0.15 + 0.28 * j), toon=CND(j), toonDur=0.2, toonEase='inOut') for j in range(6)]])],
        props=[PH('tel5'), NOTES('mus5', rate=4.0, size=0.12)],
        cams=[FC(0.0, [-0.4, 1.7, 2.0], [[ME[0], 2.55, ME[2]], [ME[0], 1.2, ME[2]], [-0.65, 2.3, -0.3], [0.6, 2.4, ME[2]]], top=0.14, bottom=0.74)])

# 6: the phone ended up... He goes to put the phone down: his arm comes away from his ear and the phone stays on it; he looks at his empty hand
D6 = st.dur('S06')
st.shot('S06', 'livingRoom', actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0),
            k(0.4, toon={'reach': {'R': [0.35, 1.25, -0.2, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2, toonEase='inOut'), k(0.65, look=[0.35, 1.25, -0.2]), k(1.0, look='camera')])],
        props=[P('tel6', 'smartPhone', on={'actor': 'mec', 'joint': 'head', 'offset': [0.2, 0.08, 0.02]}, rot=[0, PI / 2, 0], opts={'case': '#E0413A'}), NOTES('mus6')],   # stuck to his head now, not to his hand
        cams=[FC(0.0, [-1.0, 1.55, 1.9], [[ME[0], 2.55, ME[2]], [ME[0], 0.9, ME[2]], [0.45, 1.25, -0.2], [-0.4, 2.0, ME[2]]], top=0.14, bottom=0.76)])   # from his left, wider: the empty hand and the phone left on his head

# 7: ...stuck to his ear. Close: he pulls at the phone with both hands; his head stretches sideways after it and springs back; it stays on
D7 = st.dur('S07'); PULL = lambda f, s: {'touch': {'R': ['face', 0.27, 0.08, 0.02, 1, 0.02], 'L': ['face', 0.27, 0.1, 0.06, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'scl': {'head': [r(1 + 0.25 * s), r(1 - 0.08 * s), 1.0]}, 'face': f}
st.shot('S07', 'livingRoom', actors=[act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=PULL({'lid': 0.3, 'mouth': 'clench', 'brow': -0.6}, 0), toonDur=0.0),
            k(0.25, toon=PULL({'lid': 0.2, 'mouth': 'clench', 'brow': -0.8, 'sweat': 1.0}, 1), toonDur=0.15, toonEase='out'), k(0.5, toon=PULL({'lid': 0.2, 'mouth': 'clench', 'brow': -0.8, 'sweat': 1.0}, 0.6), toonDur=0.1),
            k(0.7, toon=PULL({'lid': 0.2, 'mouth': 'clench', 'brow': -0.9, 'sweat': 1.0}, 1.2), toonDur=0.12, toonEase='out'),
            k(0.9, toon={'reach': {'R': [0.4, 1.3, -0.2, 1, 0.03], 'L': [-0.4, 1.3, -0.2, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'scl': {'head': [0.9, 1.08, 1.0]}, 'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.06, toonEase='out'),   # his grip slips: the head springs back...
            k(1.05, toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.15)])],   # ...deadpan
        props=[P('tel7', 'smartPhone', on={'actor': 'mec', 'joint': 'head', 'offset': [0.2, 0.08, 0.02]}, rot=[0, PI / 2, 0], opts={'case': '#E0413A'}), NOTES('mus7')],
        cams=[FC(0.0, [0.55, 1.45, 1.0], [[ME[0], 2.6, ME[2]], [ME[0], 1.5, ME[2]], [0.5, 2.1, ME[2]], [-0.45, 2.1, ME[2]]], top=0.14, bottom=0.74)])   # low on the pull: not the frame of S02
st.cue('sfx:stretch', 'S07', 0.25, 0.25); st.cue('sfx:stretch', 'S07', 0.7, 0.25); st.cue('sfx:boing', 'S07', 0.9, 0.25)

# 8: the firemen moved house with him. Down the street: two firemen carry his sofa like a sedan chair, him sitting on it, the phone at his ear,
#    notes trailing behind
D8 = st.dur('S08'); Z8 = 3.0; V8 = 1.4
SOFA8 = lambda z: [3.6, 0.55, z]
st.shot('S08', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', [3.6, 0.65, Z8], 180, 'sit', 'neutral', keys=[k(0.0, to=[3.6, 0.65, r(Z8 - V8 * D8)], dur=D8, ease='linear'), k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0)]),
        *[act(fid, [r(3.6 + dx), 0, r(Z8 + dz)], 180, 'walk', 'determined', keys=[k(0.0, to=[r(3.6 + dx), 0, r(Z8 + dz - V8 * D8)], dur=D8, clip='walk', ease='linear'), k(0.0, toon={'reach': {'R': [r(3.6 + dx * 0.6), 1.05, r(Z8 + dz * 0.5), 1, 0.04], 'L': [r(3.6 + dx * 0.6), 1.05, r(Z8 + dz * 0.5 + 0.3), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)])
          for fid, dx, dz in [('pomp1', 0.0, -1.05), ('pomp2', 0.0, 1.05)]]],
        props=[P('canape8', 'sofaProp', pos=SOFA8(Z8), ry=0, scale=0.85, keys=[k(0.0, to=SOFA8(r(Z8 - V8 * D8)), dur=D8, ease='linear')]), PH('tel8'), NOTES('mus8', side=1)],
        cams=[FC(0.0, [5.9, 1.5, -0.6], [[3.6, 2.5, Z8], [3.6, 0.0, r(Z8 - 1.05)], [3.6, 2.6, r(Z8 + 1.05)], [3.6, 0.0, r(Z8 - V8 * D8 - 1.0)]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S08', 0.3, 0.15); st.cue('sfx:stepSoft', 'S08', 0.8, 0.15); st.cue('sfx:stepSoft', 'S08', 1.3, 0.15)

# 9: he got married on hold. The town hall: the mayor in his sash reads from the register; the bride in her veil beside him; the phone at his ear,
#    notes rising over the wedding
D9 = st.dur('S09'); BR = [0.45, 0, 0.2]; GR = [-0.45, 0, 0.2]; MA = [0.0, 0, -1.5]
st.shot('S09', 'mairie', setOpts={'map': False, 'bannerY': 3.9}, actors=[
        act('mec', GR, 10, 'stand', 'neutral', keys=[k(0.0, look=[MA[0], 2.0, MA[2]]), k(0.0, toon=HOLD(), toonDur=0.0), k(1.0, look='camera')]),
        act('femme', BR, -10, 'stand', 'happy', keys=[k(0.0, look=[MA[0], 2.0, MA[2]]), k(0.6, look=[GR[0], 2.1, GR[2]]), k(1.1, look=[MA[0], 2.0, MA[2]]), k(0.9, toon={'touch': {'R': ['torso', 0.05, 0.4, 0.3, 1, 0.02], 'L': ['torso', -0.05, 0.4, 0.3, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=0.06), k(1.0, toon={'touch': {'R': ['torso', 0.05, 0.4, 0.3, 1, 0.02], 'L': ['torso', -0.05, 0.4, 0.3, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.08), k(0.0, toon={'touch': {'R': ['torso', 0.05, 0.4, 0.3, 1, 0.02], 'L': ['torso', -0.05, 0.4, 0.3, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.0)]),
        act('maire', MA, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.9, 0.2]), k(0.0, toon={'reach': {'R': [0.15, 1.35, -1.1, 1, 0.04], 'L': [-0.15, 1.35, -1.1, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'open'}}, toonDur=0.0),
            k(0.5, look=[0.15, 1.35, -1.1]), k(1.05, look=[GR[0], 2.1, GR[2]]), *[k(r(0.2 + 0.3 * j), toon={'reach': {'R': [0.15, 1.35, -1.1, 1, 0.04], 'L': [-0.15, 1.35, -1.1, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'open' if j % 2 else 'line'}}, toonDur=0.1) for j in range(5)]])],   # reading out the register
        props=[PH('tel9'), NOTES('mus9'), P('voile9', 'bridalVeil', on={'actor': 'femme', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}), P('bouq9', 'bouquet', on={'actor': 'femme', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}),
               P('reg9', 'paperSheet', on={'actor': 'maire', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, face='camera', opts={'w': 0.3, 'h': 0.22, 'lines': ['REGISTRE']})],
        cams=[FC(0.0, [0.3, 1.6, 2.6], [[GR[0], 2.5, GR[2]], [BR[0], 2.45, BR[2]], [MA[0], 2.5, MA[2]], [GR[0], 0.9, GR[2]], [BR[0], 0.9, BR[2]]], top=0.14, bottom=0.76)])
st.cue('sfx:bell', 'S09', 0.2, 0.2)

# 10: his wife said yes on the speaker. She leans to the phone on his ear and says it into it: OUI !; the mayor claps, he does not move
D10 = st.dur('S10'); OUI10 = 0.7
st.shot('S10', 'mairie', setOpts={'map': False, 'bannerY': 3.9}, actors=[
        act('mec', GR, 10, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0), k(r(OUI10 + 0.05), toon=HOLD(extra={'sq': [0.97, 1.03, 0.97]}), toonDur=0.05), k(r(OUI10 + 0.2), toon=HOLD(), toonDur=0.08), k(1.55, toon=HOLD({'lid': 1.0, 'mouth': 'line'}), toonDur=0.07), k(1.67, toon=HOLD(), toonDur=0.08)]),
        act('femme', BR, -60, 'stand', 'happy', keys=[k(0.0, look=[GR[0], 2.0, GR[2]]), k(0.2, toon={'bend': {'spine': [0.25, 0, -0.2, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'),
            k(OUI10, toon={'bend': {'spine': [0.3, 0, -0.25, 1, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'mouth': 'open'}}, toonDur=0.06, toonEase='out'), k(r(OUI10 + 0.5), toon={'bend': {'spine': [0.05, 0, 0, 1, None]}, 'face': {'lid': 0.1, 'mouth': 'bigsmile'}}, toonDur=0.25)]),
        act('maire', MA, 0, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.9, 0.2]), *[k(r(OUI10 + 0.15 + 0.16 * j), toon={'reach': {'R': [r(0.08 if j % 2 else 0.12), 1.55, -1.1, 1, 0.04], 'L': [r(-0.08 if j % 2 else -0.12), 1.55, -1.1, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.06) for j in range(6)]])],
        props=[PH('tel10'), NOTES('mus10'), P('voile10', 'bridalVeil', on={'actor': 'femme', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}), BURST('oui10', [-0.05, 2.45, 0.5], OUI10, 'OUI !', 0.42, 0.4)],
        cams=[FC(0.0, [1.6, 1.8, 1.5], [[GR[0], 2.55, GR[2]], [BR[0], 2.45, BR[2]], [GR[0], 1.3, GR[2]], [BR[0], 1.3, BR[2]]], top=0.18, bottom=0.74)])   # from her side: her yes into his phone
st.cue('sfx:pop', 'S10', OUI10, 0.2); st.cue('sfx:fanfare', 'S10', r(OUI10 + 0.2), 0.15)

# 11: the music became the national anthem. A ceremony in the street: the flag climbs its pole; officials and soldiers salute, hand on heart; in the
#     front row him, the phone at his ear: the anthem is coming out of it (HYMNE)
D11 = st.dur('S11'); POLE = [2.0, 0, -2.2]
st.shot('S11', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', [0.0, 0, 0.6], 0, 'stand', 'neutral', keys=[k(0.0, look=[POLE[0], 4.0, POLE[2]]), k(0.0, toon=HOLD(), toonDur=0.0), k(0.9, toon=HOLD({'lid': 1.0, 'mouth': 'line'}), toonDur=0.07), k(1.02, toon=HOLD(), toonDur=0.08), k(1.4, look='camera')]),
        *[act(oid, [x, 0, z], ry, 'salute' if pre in ('cop', 'cop2') else 'stand', 'determined', keys=[k(0.0, look=[POLE[0], 4.0, POLE[2]]),
            *([k(0.0, toon={'touch': {'R': ['torso', -0.08, 0.45, 0.25, 1, 0.02]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0), k(r(0.7 + 0.5 * (x > 0)), toon={'touch': {'R': ['torso', -0.08, 0.45, 0.25, 1, 0.02]}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07),
               k(r(0.82 + 0.5 * (x > 0)), toon={'touch': {'R': ['torso', -0.08, 0.45, 0.25, 1, 0.02]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.08), k(1.6, look=[0.0, 1.9, 0.6])] if pre not in ('cop', 'cop2') else [])])   # a blink, then a glance at him: the anthem is his phone
          for oid, x, z, ry, pre in [('off1', -1.1, -0.2, 15, 'politique'), ('sold1', 1.0, -0.4, -10, 'cop'), ('sold2', -0.4, -1.0, 5, 'cop2'), ('off2', 0.7, -1.3, -5, 'politique')]]],
        props=[PH('tel11'), NOTES('mus11', rate=4.0, size=0.13), P('mat11', 'flagPole', pos=POLE, opts={'h': 6.0, 'raise': [0.1, r(D11 - 0.1)]})],
        cams=[FC(0.0, [-1.6, 1.3, 4.2], [[0.0, 2.5, 0.6], [0.0, 0.0, 0.6], [POLE[0], 6.2, POLE[2]], [-1.1, 2.4, -0.2], [1.0, 2.4, -0.4]], top=0.14, bottom=0.78)])
st.cue('sfx:fanfare', 'S11', 0.2, 0.25)

# 12: the band played it at the parade. The street with flags: a marching band, trumpets, a tuba and a drum, in step, playing it
D12 = st.dur('S12'); Z12 = 2.0; V12 = 1.2
BAND = [('mus1', -0.6, 0.0, 'trumpet'), ('mus2', 0.6, 0.0, 'trumpet'), ('mus3', -0.6, 1.2, 'tuba'), ('mus4', 0.6, 1.2, 'drum')]
st.shot('S12', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act(mid, [r(3.5 + dx), 0, r(Z12 + dz)], 180, 'walk', 'determined', keys=[k(0.0, to=[r(3.5 + dx), 0, r(Z12 + dz - V12 * D12)], dur=D12, clip='walk', ease='linear'),
            k(0.0, toon={'reach': {'R': [r(3.5 + dx + 0.05), 2.0 if kind == 'trumpet' else 1.4, r(Z12 + dz - 0.35), 1, 0.04], 'L': [r(3.5 + dx - 0.05), 2.0 if kind == 'trumpet' else 1.3, r(Z12 + dz - 0.3), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'kiss', 'cheeks': 0.8 if kind != 'drum' else 0.0}}, toonDur=0.0)])
        for mid, dx, dz, kind in BAND],
        props=[*[P(f'ins12{j}', 'brass', on={'actor': mid, 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, opts={'kind': kind, 'beat': [0.1, 0.5, 0.9, 1.3, 1.7] if kind == 'drum' else []}) for j, (mid, dx, dz, kind) in enumerate(BAND)],
               *[P(f'n12{j}', 'holdNotes', on={'actor': BAND[j][0], 'joint': 'head', 'offset': [0.0, 0.4, -0.3]}, face='camera', opts={'rate': 2.5, 'size': 0.12, 'side': -1 if j % 2 else 1}) for j in range(2)],
               *[P(f'dr12{j}', 'flag', pos=[r(6.2 if j % 2 else 0.8), 2.2, r(-2.0 + 2.6 * j)], scale=0.5, opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A']}) for j in range(3)]],
        cams=[FC(0.0, [1.6, 1.2, -2.6], [[3.5, 2.5, r(Z12 - 0.6)], [2.9, 0.0, r(Z12 - V12 * D12)], [4.1, 2.6, r(Z12 + 1.2)], [2.9, 0.3, r(Z12 + 1.2)]], top=0.14, bottom=0.78)])
st.cue('sfx:fanfare', 'S12', 0.05, 0.3); st.cue('thud', 'S12', 0.1, 0.15); st.cue('thud', 'S12', 0.5, 0.15); st.cue('thud', 'S12', 0.9, 0.15); st.cue('thud', 'S12', 1.3, 0.15)

# 13: the children whistle it at school. A classroom: the kids at their desks whistle it, notes over their heads; the teacher conducts with a ruler
D13 = st.dur('S13'); KIDS = [('el1', -0.7, 0.0), ('el2', 0.7, 0.0), ('el3', -0.7, 1.2), ('el4', 0.7, 1.2)]
st.shot('S13', 'classroom', actors=[
        *[act(eid, [x, 0, z], 180, 'sit', 'happy', keys=[k(0.0, look=[0.0, 1.8, -1.6]), *[k(r(0.1 + 0.3 * j + 0.07 * i), toon={'face': {'lid': 0.3, 'mouth': 'whistle', 'cheeks': 0.5}, 'sq': [1.0, 1.03 if j % 2 else 0.98, 1.0]}, toonDur=0.12) for j in range(6)]])
          for i, (eid, x, z) in enumerate(KIDS)],
        act('prof', [0.0, 0, -1.6], 0, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.4, 0.6]), *[k(r(0.1 + 0.25 * j), toon={'reach': {'R': [r(0.25 + (0.15 if j % 2 else -0.1)), r(2.1 + (0.15 if j % 2 else 0.0)), -1.3, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smile'}}, toonDur=0.12) for j in range(7)]])],
        props=[*[P(f'n13{i}', 'holdNotes', on={'actor': eid, 'joint': 'head', 'offset': [0.0, 0.5, 0.2]}, face='camera', opts={'rate': 2.0, 'size': 0.09, 'from': r(0.05 * i)}) for i, (eid, x, z) in enumerate(KIDS)],
               P('regle13', 'slab', on={'actor': 'prof', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, opts={'w': 0.03, 'h': 0.4, 'd': 0.01, 'color': '#E2B53C'})],
        cams=[FC(0.0, [0.0, 2.2, -2.9], [[-0.7, 1.9, 0.0], [0.7, 1.9, 1.2], [0.0, 2.5, -1.6], [-0.7, 0.5, 1.2], [0.7, 0.5, 0.0]], top=0.14, bottom=0.78, inside=(-4.0, 4.0, 0.5, 3.0, -3.3, 6.0))])
st.cue('sfx:whistle', 'S13', 0.1, 0.25)

# 14: yesterday someone picked up. Back on his sofa, older, the phone at his ear: click: the notes stop dead; his eyes pop
D14 = st.dur('S14'); CLK14 = 0.45
st.shot('S14', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD(), toonDur=0.0),
            k(r(CLK14 + 0.05), toon=HOLD({'lid': 0.0, 'eye': 0.6, 'pop': 0.7, 'popLen': 0.22, 'mouth': 'O', 'brow': 1.0}, {'sq': [0.95, 1.08, 0.95]}), toonDur=0.05, toonEase='out'),
            k(r(CLK14 + 0.5), toon=HOLD({'lid': 0.0, 'eye': 0.5, 'pop': 0.3, 'popLen': 0.12, 'mouth': 'O', 'brow': 0.9}), toonDur=0.15)])],   # a take: eyes out on stalks
        props=[PH('tel14'), NOTES('mus14', t0=-2.0, t1=CLK14), P('sofa14', 'sofaProp', pos=[0.0, 0, -2.05], ry=0)],
        cams=[FC(0.0, [0.35, 1.5, 1.2], [[0.0, 2.1, -1.6], [0.0, 1.0, -1.6], [0.45, 1.75, -1.6], [-0.4, 1.75, -1.6]], top=0.16, bottom=0.74)])
st.cue('sfx:click', 'S14', CLK14, 0.35); st.cue('sfx:gasp', 'S14', r(CLK14 + 0.08), 0.25)

# 15: he cried for joy... Close: his face crumples, tears jetting out sideways, the phone still at his ear
D15 = st.dur('S15')
st.shot('S15', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD({'tears': 1.0, 'mouth': 'sob', 'brow': 0.9, 'lid': 0.8}), toonDur=0.0),
            *[k(r(0.1 + 0.16 * j), toon=HOLD({'tears': 1.0, 'mouth': 'scream' if j % 2 else 'sob', 'brow': 0.9, 'lid': 0.85}, {'sq': [r(1.0 + (0.03 if j % 2 else 0.0)), r(1.0 - (0.04 if j % 2 else 0.0)), r(1.0 + (0.03 if j % 2 else 0.0))]}), toonDur=0.08) for j in range(8)]])],
        props=[PH('tel15'), P('larmes15', 'tearFountain', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.24, 0.17]}, opts={'at': 0.05, 'dx': 0.09, 'rate': 24, 'speed': 1.9, 'r': 0.026}), P('sofa15', 'sofaProp', pos=[0.0, 0, -2.05], ry=0)],
        cams=[FC(0.0, [-0.5, 1.45, -0.45], [[0.0, 2.15, -1.6], [0.0, 1.3, -1.6], [0.55, 1.9, -1.6], [-0.55, 1.9, -1.6]], top=0.16, bottom=0.74)])   # low from his left: the tears against the wall
st.cue('sfx:sniff', 'S15', 0.2, 0.25); st.cue('sfx:sniff', 'S15', 0.7, 0.2)

# 16: ...live on television. Wider: TV cameras crowd his living room, a reporter thrusts a mic at him; a red EN DIRECT sign
D16 = st.dur('S16')
st.shot('S16', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD({'tears': 1.0, 'mouth': 'sob', 'brow': 0.9, 'lid': 0.8}), toonDur=0.0)]),
        act('repo', [0.9, 0, -0.9], -130, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, -1.6]), k(0.0, toon={'reach': {'R': [0.4, 1.55, -1.3, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'open'}}, toonDur=0.0)])],
        props=[PH('tel16'), P('larmes16', 'tearFountain', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.24, 0.17]}, opts={'at': 0.0, 'dx': 0.09, 'rate': 20, 'speed': 1.6, 'r': 0.022}), P('sofa16', 'sofaProp', pos=[0.0, 0, -2.05], ry=0),
               P('mic16', 'pressMic', on={'actor': 'repo', 'hand': 'R', 'offset': [0.0, -0.02, 0.04]}, opts={'text': 'INFO', 'color': '#C8322A'}),
               *[P(f'tv16{j}', 'tvCamera', pos=[r(-1.4 + 0.9 * j), 0, r(0.4 + 0.2 * (j % 2))], ry=r(180 + 15 * (j - 1))) for j in range(3)],
               P('direct16', 'signBoard', pos=[-1.3, 0, -0.4], ry=20, opts={'text': 'EN DIRECT', 'bg': '#D22B2B', 'fg': '#FFFFFF', 'w': 1.0, 'h': 0.3, 'height': 1.8})],
        cams=[FC(0.0, [0.4, 1.7, 2.6], [[0.0, 2.1, -1.6], [0.0, 0.6, -1.6], [0.9, 2.45, -0.9], [-1.4, 1.8, 0.4], [-1.3, 2.15, -0.4]], top=0.14, bottom=0.78)])
st.cue('sfx:click', 'S16', 0.2, 0.15)

# 17: the voice said... Close on the phone at his ear: a flat electronic voice, a little speech bubble out of the phone; his eyes go to it
D17 = st.dur('S17')
st.shot('S17', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD({'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'gx': 0.6}), toonDur=0.0)])],
        props=[PH('tel17'), BURST('bip17', [0.55, 2.2, -1.4], 0.1, 'BIP', 0.28, 0.6)],
        cams=[FC(0.0, [0.5, 1.95, -0.6], [[0.0, 2.2, -1.6], [0.0, 1.6, -1.6], [0.6, 2.4, -1.4], [-0.3, 1.9, -1.6]], top=0.18, bottom=0.74)])
st.cue('sfx:ding', 'S17', 0.1, 0.15)

# 18: ...for an adviser, press one. He takes the phone off his ear (it comes free with a pop) and holds it in front of him: the keypad
D18 = st.dur('S18'); OFF18 = 0.35
st.shot('S18', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD({'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}), toonDur=0.0),
            k(OFF18, toon={'reach': {'R': [0.1, 1.18, -1.05, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'line'}}, toonDur=0.15, toonEase='out'), k(r(OFF18 + 0.1), look=[0.1, 1.18, -1.05])])],   # (stills 1) held at chest height: in front of his face it hid it
        props=[P('pad18', 'phoneKeypad', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, face='camera', scale=0.3, opts={'label': 'SERVICE CLIENT'})],
        cams=[FC(0.0, [0.3, 1.6, 0.4], [[0.0, 2.15, -1.6], [0.0, 1.0, -1.6], [0.25, 1.2, -1.05], [-0.2, 1.2, -1.05]], top=0.16, bottom=0.74)])
st.cue('pop', 'S18', OFF18, 0.25)

# 19: he pressed one. Insert: the keypad big in his hand; his finger comes in and presses 1: it lights up green (UN)
D19 = st.dur('S19'); PRESS19 = 0.55; PAD19 = [0.05, 1.25, -0.95]   # (stills 1) the keypad as its own prop, square to the lens (held in the hand it turned edge-on and his face filled the insert)
st.shot('S19', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look=PAD19), k(0.0, toon={'reach': {'R': [0.14, 1.12, -0.97, 1, 0.03], 'L': [-0.2, 1.3, -1.0, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'point'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(r(PRESS19 - 0.18), toon={'reach': {'R': [0.14, 1.12, -0.97, 1, 0.03], 'L': [0.01, 1.31, -0.91, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'point'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.18, toonEase='inOut')])],   # the finger comes in to the 1
        props=[P('pad19', 'phoneKeypad', pos=PAD19, face='camera', scale=0.3, opts={'label': 'SERVICE CLIENT', 'pressAt': PRESS19})],
        cams=[FC(0.0, [0.12, 1.3, -0.45], [[-0.04, 1.42, -0.95], [0.14, 1.42, -0.95], [-0.04, 1.08, -0.95], [0.14, 1.08, -0.95]], top=0.18, bottom=0.74, lenses=range(16, 60))])   # (stills 1) the keypad fills the frame
st.cue('sfx:click', 'S19', PRESS19, 0.35)

# 20: the music started again. The notes pour out of the phone again; he puts it back to his ear and looks at us, deadpan
D20 = st.dur('S20')
st.shot('S20', 'livingRoom', actors=[act('mec', [0.0, 0, -1.6], 0, 'sit', 'neutral', keys=[k(0.0, look=[0.05, 1.45, -1.15]), k(0.0, toon={'reach': {'R': [0.05, 1.45, -1.15, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon=HOLD(), toonDur=0.25, toonEase='inOut'), k(0.55, look='camera'), k(0.95, toon=HOLD({'lid': 1.0, 'mouth': 'line'}), toonDur=0.1), k(1.1, toon=HOLD(), toonDur=0.1)])],
        props=[PH('tel20'), NOTES('mus20', t0=0.1, rate=3.5), P('sofa20', 'sofaProp', pos=[0.0, 0, -2.05], ry=0)],
        cams=[FC(0.0, [-0.7, 1.75, 0.9], [[0.0, 2.15, -1.6], [0.0, 1.0, -1.6], [0.55, 2.3, -1.6], [-0.4, 1.8, -1.6]], top=0.16, bottom=0.74)])   # wider, from his left: the end hold
st.cue('sfx:ding', 'S20', 0.1, 0.12)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le service client", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'pomp1': {'preset': 'pompier', 'seed': 731, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'pomp2': {'preset': 'pompier', 'seed': 732, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'femme': {'preset': 'femme', 'seed': 733, 'suit': '#F7F5EF', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 734, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'suit': '#26365F', 'lapel': '#26365F', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off1': {'preset': 'politique', 'seed': 735, 'suit': '#33363D', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off2': {'preset': 'politique', 'seed': 736, 'suit': '#4A4D55', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold1': {'preset': 'cop', 'seed': 737, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold2': {'preset': 'cop2', 'seed': 738, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{mid: {'preset': 'officiel', 'seed': 740 + j, 'suit': '#8E2B2B', 'hat': 'copcap', 'hatColor': '#8E2B2B', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j, (mid, _, _, _) in enumerate(BAND)},
    **{eid: {'preset': 'gamin', 'seed': 750 + j, 'suit': c_, 'build': {'headScale': 1.25}, 'toon': EX} for j, ((eid, _, _), c_) in enumerate(zip(KIDS, ['#E0413A', '#3A9BDC', '#7CC25A', '#E8A33C']))},
    'prof': {'preset': 'madame', 'seed': 755, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'repo': {'preset': 'journaliste', 'seed': 756, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
