#!/usr/bin/env python3
"""Le centime (story 77, cycle 39; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man paid his taxes one cent too much. The tax office decided to refund him. But the stamp cost more than the cent. So the minister came in
person. With the republican guard. The street was closed. A brass band played. Helicopters flew over the neighbourhood. The cent arrived on a velvet
cushion. The minister gave a one-hour speech. The neighbours wept. Television filmed it live. He put the cent in his piggy bank. The next day, he
got a bill. Two million euros. Travel expenses.
Staging: at the tax office desk a red police light starts turning over the clerk's screen (+0,01 €); a meeting at the ministry, the chief bangs the
table, everyone nods; a stamp of 3 € slapped beside a cheque for 0,01 €; a black car stops in his Paris street, the minister steps out; the guards
in plumed helmets salute as one; barriers, a closed street, a jam; a trumpet, a tuba, a drum; two helicopters over the roofs; a guard carries the
coin on a red velvet cushion; the speech at a lectern, a guard nodding off; neighbours crying at their windows; TV cameras, EN DIRECT; in his
kitchen the coin drops into the pink piggy bank, which jiggles; the next morning a letter; the bill unrolls to the floor, 2 000 000 €; FRAIS DE
DÉPLACEMENT; a look at us.
Natural look; cycle 39: piggyBank, velvetCushion, guardHelmet, beacon (props_centime), brass, helicopter, billScroll, tvCamera, crowdBarrier reused."""
from story_kit import *
import math

st = Story('centime', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 17)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
LIP = {'face': {'lid': 0.45, 'mouth': 'line'}}
BLINK = lambda t, f=None: [k(t, toon={'face': {'lid': 1.0, **(f or {})}}, toonDur=0.07, keepPose=True), k(r(t + 0.12), toon={'face': {**DEAD, **(f or {})}}, toonDur=0.08, keepPose=True)]   # (cycle 40) keepPose: a blink keeps what the hands hold
STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 6.0], 'clearL': [-6.0, 6.0]}   # no tree or lamp of the set in front of his door
ME = [5.6, 0, 0.0]                                   # on the right-hand pavement at his door, facing the road (-X)
MIN = [4.35, 0, 0.35]                                # the minister in front of him
TRI = ['#2F62B5', '#F4F4F0', '#E0413A']
GUARD = lambda pid, who: P(pid, 'guardHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, scale=1.1)   # (stills 1) on top of the head (at 0.26 it sat on his chin)
COCK = lambda pid, who: P(pid, 'slab', on={'actor': who, 'joint': 'torso', 'offset': [0.1, 0.48, 0.13]}, opts={'w': 0.05, 'h': 0.05, 'd': 0.01, 'color': '#E0413A'})   # a tricolour pin

for g_ in [('S01', 0.8, 'agent', 'alarm'), ('S03', 0.6, 'agent2', 'stamp'), ('S05', 0.5, 'garde1', 'salute'), ('S09', 0.9, 'garde3', 'cushion'), ('S13', 0.9, 'mec', 'piggy'), ('S15', 0.6, 'mec', 'bill')]:
    st.gag(*g_)
st.card('S01', '0,01 €', at=0.85)
st.card('S09', 'REMBOURSÉ', at=0.7)
st.card('S15', '2 000 000 €', at=0.45)

# 1: the hook. The tax office desk: he hands over his payment; the clerk types, freezes; a red police light on the desk starts turning, a siren; the
#    clerk's eyes pop at the screen (+0,01 €); he stands there, deadpan
D1 = st.dur('S01'); AL1 = 0.75
st.shot('S01', 'office', actors=[
        act('agent', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 0.95, -1.55]), *[k(r(0.08 + 0.12 * j), toon={'reach': {('L' if j % 2 else 'R'): [r(-4.7 if j % 2 else -4.5), 0.84, -1.62, 1, 0.03]}, 'hands': {'L': 'point', 'R': 'point'}, 'face': {'lid': 0.5}}, toonDur=0.05) for j in range(5)],
            k(r(AL1 - 0.22), look=[-3.75, 1.9, -1.05], lookDur=0.08), k(r(AL1 - 0.06), look=[-4.6, 0.95, -1.55], lookDur=0.05),   # (review 1) a double take: up at him, back down at the screen...
            k(AL1, toon={'sq': [0.86, 1.2, 0.86], 'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.14, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...eyes out on stalks...
            k(r(AL1 + 0.42), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.14, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.1), k(r(AL1 + 0.55), toon={'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.06, toonEase='in'),   # ...a hang, then they snap back
            k(r(AL1 + 0.45), look=[-3.75, 1.9, -1.05]), *BLINK(1.7, {'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}), k(2.2, look=[-4.6, 0.95, -1.55], lookDur=0.12)]),   # types... freezes, eyes popping at the screen, then looks up at him
        act('mec', [-3.75, 0, -1.05], 15, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=LIP, toonDur=0.0), k(r(AL1 + 0.1), look=[-4.95, 0.9, -1.45], lookDur=0.12), k(r(AL1 + 0.6), look='camera', lookDur=0.15), *BLINK(r(AL1 + 0.95), {'mouth': 'line'})])],   # facing us at the corner of the desk, deadpan, a glance at the light
        props=[P('pc1', 'laptop', pos=[-4.6, 0.76, -1.6], ry=180), P('gyro1', 'beacon', pos=[-4.95, 0.76, -1.45], scale=2.4, opts={'from': AL1, 'rps': 2.2, 'len': 0.75, 'opacity': 0.3}),   # (review 1) two and a half times bigger, its beam sweeping the wall
               P('imp1', 'signBoard', pos=[-4.6, 1.95, -3.55], opts={'text': 'CENTRE DES IMPÔTS', 'bg': '#26365F', 'fg': '#FFFFFF', 'frame': '#E0413A', 'w': 1.9, 'h': 0.38, 'posts': False, 'height': 0}),
               BURST('b1', [-5.3, 1.65, -1.6], r(AL1 + 0.05), '+0,01 €', 0.5, 0.5)],   # (review 1) clear of his shoulder (it read +0,0)
        cams=[FC(0.0, [-3.9, 1.6, 1.4], [[-4.6, 1.95, -2.15], [-3.75, 2.45, -1.05], [-4.95, 0.85, -1.45], [-3.75, 0.5, -1.05], [-4.6, 2.2, -3.55], [-5.6, 1.65, -1.6]], top=0.12, bottom=0.78, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])
st.cue('sfx:click', 'S01', 0.1, 0.1); st.cue('sfx:click', 'S01', 0.34, 0.1); st.cue('sfx:siren', 'S01', AL1, 0.35)

# 2: the tax office decided to refund him. A meeting room at the ministry: four officials round a table, a board TROP-PERÇU 0,01 €; the chief bangs the
#    table and all four nod at once
D2 = st.dur('S02'); BANG2 = 0.55
OFF2 = [('chef', [-4.6, 0, -2.15], 0, 'boss'), ('off1', [-5.45, 0, -1.35], 90, 'politique'), ('off2', [-3.75, 0, -1.35], -90, 'avocat'), ('off3', [-4.6, 0, -0.55], 180, 'officiel')]
NOD = lambda t: [k(t, toon={'bend': {'neck': [0.5, 0, 0, 1, None]}, 'sq': [1.05, 0.93, 1.05], 'face': {'lid': 0.3}}, toonDur=0.06, toonEase='out'), k(r(t + 0.14), toon={'bend': {'neck': [-0.08, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': DEAD}, toonDur=0.1),
                 k(r(t + 0.26), toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.1)]   # (review 1) a deep nod, an overshoot back, settle
st.shot('S02', 'office', actors=[
        *[act(n_, p_, ry_, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 1.2, -1.35]), *(NOD(r(BANG2 + 0.12)) + NOD(r(BANG2 + 0.42)) if n_ != 'chef' else
            [k(r(BANG2 - 0.28), toon={'reach': {'R': [-4.45, 1.85, -1.8, 1, 0.03]}, 'hands': {'R': 'fist'}, 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.2, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.2, toonEase='out'),
             k(BANG2, toon={'reach': {'R': [-4.45, 0.8, -1.65, 1, 0.03]}, 'hands': {'R': 'fist'}, 'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.1, 'brow': -0.9, 'mouth': 'open'}}, toonDur=0.05, toonEase='in'), k(r(BANG2 + 0.4), look='camera')])]) for n_, p_, ry_, _ in OFF2]],
        props=[P('table2', 'desk', pos=[-4.6, 0, -1.35], opts={'w': 1.4}, keys=[k(BANG2, squash=[1.04, 0.84, 1.04], dur=0.35)]),   # (review 1) the slam flattens the table...
               *[P(f'pap2{j}', 'slab', pos=[r(-5.0 + 0.4 * j), 0.79, r(-1.25 - 0.08 * j)], opts={'w': 0.22, 'h': 0.012, 'd': 0.28, 'color': '#FBF8EE'}, keys=[k(BANG2, to=[r(-5.0 + 0.4 * j), r(0.98 + 0.04 * j), r(-1.25 - 0.08 * j)], dur=0.08, ease='out'), k(r(BANG2 + 0.08), to=[r(-5.0 + 0.4 * j), 0.79, r(-1.25 - 0.08 * j)], dur=0.12, ease='in')]) for j in range(3)],
               P('tab2', 'signBoard', pos=[-4.6, 1.5, -3.55], opts={'text': 'TROP-PERÇU\n0,01 €', 'bg': '#F6F1E3', 'fg': '#C8322A', 'frame': '#26365F', 'w': 1.5, 'h': 0.8, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [-3.6, 2.75, 1.2], [[-4.6, 1.9, -2.15], [-5.45, 1.9, -1.35], [-3.75, 1.9, -1.35], [-4.6, 2.35, -3.55], [-5.4, 1.5, -3.55], [-3.8, 1.5, -3.55], [-4.6, 0.7, -0.6]], top=0.1, bottom=0.8, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])   # (stills 1) high over the near officials' heads (their backs filled the frame), the board whole
st.cue('thud', 'S02', BANG2, 0.35)

# 3: but the stamp cost more than the cent. Close on the desk from above: a cheque for 0,01 € and its envelope; a hand slaps a big stamp 3,00 € on the
#    envelope (thump), the cheque jumps; the official looks at us, sweating
D3 = st.dur('S03'); SLAP3 = 0.55
st.shot('S03', 'office', actors=[act('agent2', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 0.77, -1.5]), k(0.0, toon={'reach': {'R': [-4.4, 1.15, -1.5, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.0), k(0.22, toon={'reach': {'R': [-4.42, 1.42, -1.5, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'brow': -0.6}}, toonDur=0.2, toonEase='out'),   # (review 1) the stamp up, a hang...
            k(SLAP3, toon={'reach': {'R': [-4.4, 0.9, -1.47, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.05, toonEase='in'),   # ...thump
            k(r(SLAP3 + 0.35), look='camera'), k(r(SLAP3 + 0.4), toon={'reach': {'R': [-4.4, 1.0, -1.47, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'zigzag', 'sweat': 1.0, 'brow': 0.6}}, toonDur=0.12), *BLINK(1.5, {'mouth': 'zigzag', 'sweat': 1.0}), k(1.8, turn=-12, turnDur=0.12), k(2.0, turn=10, turnDur=0.12), k(2.2, turn=0, turnDur=0.12)])],
        props=[P('pc3', 'laptop', pos=[-5.05, 0.76, -1.75], ry=200), P('chq3', 'cheque', pos=[-4.78, 0.775, -1.4], rot=[-PI / 2, 0, 0.15], scale=1.3, opts={'amount': '0,01 €', 'text': 'TRÉSOR PUBLIC'}, keys=[k(SLAP3, to=[-4.8, 0.9, -1.38], dur=0.08, ease='out'), k(r(SLAP3 + 0.08), to=[-4.82, 0.775, -1.36], dur=0.12, ease='in')]),   # (review 1) it hops at the thump
               P('env3', 'envelope', pos=[-4.4, 0.775, -1.45], rot=[-PI / 2, 0, -0.1], scale=1.6, keys=[k(SLAP3, squash=[1.08, 0.8, 1.08], dur=0.3)]),
               P('tampon3', 'rubberStamp', on={'actor': 'agent2', 'hand': 'R', 'offset': [0.0, -0.08, 0.03]}, scale=2.2),   # (review 1) the big stamp in his hand
               P('timbre3', 'stampMark', pos=[-4.35, 0.79, -1.47], rot=[-PI / 2, 0, -0.1], opts={'text': '3,00 €', 'w': 0.17, 'h': 0.09}, keys=[k(0.0, visible=False), k(SLAP3, visible=True)])],
        cams=[FC(0.0, [-4.6, 1.6, -1.05], [[-4.9, 0.775, -1.4], [-4.25, 0.775, -1.45], [-4.6, 0.775, -1.58], [-4.6, 0.775, -1.26]], top=0.15, bottom=0.72, lenses=range(20, 60), inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0)),   # (review 1) from above: the two prices fill the frame
              FC(1.05, [-4.15, 1.85, -0.35], [[-4.6, 2.08, -2.15], [-4.6, 1.3, -2.15], [-4.85, 0.78, -1.3], [-4.3, 0.78, -1.3]], top=0.12, bottom=0.72, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])   # then him, sweating, at us
st.cue('thud', 'S03', SLAP3, 0.4); st.cue('sfx:gasp', 'S03', r(SLAP3 + 0.3), 0.2)

# 4: so the minister came in person. His street: a black car pulls up at his door with a bounce; the door opens and the minister steps out, tugging his
#    jacket straight; he waits on his doorstep, deadpan
D4 = st.dur('S04'); STOP4 = 0.55; OUT4 = 0.75
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('ministre', [2.9, 0, 0.6], 90, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]), k(0.0, visible=False), k(r(OUT4 - 0.02), visible=True), k(0.0, toon={'sq': [0.5, 0.5, 0.5]}, toonDur=0.0),
            k(r(OUT4 - 0.02), toon={'sq': [0.62, 1.45, 0.62]}, toonDur=0.0), k(r(OUT4 + 0.1), toon={'sq': [1.18, 0.84, 1.18]}, toonDur=0.08, toonEase='out'), k(r(OUT4 + 0.24), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.1),   # (review 1) squeezed thin out of the door, he re-inflates
            k(OUT4, to=MIN, dur=0.35, clip='walk', then='stand', ease='out', face='keep'), k(r(OUT4 + 0.45), toon={'touch': {'R': ['torso', 0.1, 0.25, 0.2, 1, 0.02], 'L': ['torso', -0.1, 0.25, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 1.04, 1.0]}, toonDur=0.1),
            k(r(OUT4 + 0.62), toon={}, toonDur=0.15)]),   # out of the car, a tug at the jacket
        act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[2.9, 1.2, 0.6]), k(0.0, toon=LIP, toonDur=0.0), k(r(OUT4 + 0.3), look=[MIN[0], 2.2, MIN[2]]), *BLINK(1.3)])],
        props=[P('auto4', 'car', pos=[2.6, 0, -8.0], ry=0, opts={'color': '#1A1C22', 'glass': 0.85, 'glassColor': '#2A3040'}, keys=[k(0.0, to=[2.6, 0, 0.0], dur=STOP4, ease='out'), k(STOP4, squash=[1.03, 0.88, 1.03], dur=0.45)]), COCK('ck4', 'ministre')],   # (review 1) tinted windows (he showed standing inside), a bounce as it stops
        cams=[FC(0.0, [2.2, 1.5, 4.4], [[ME[0], 2.45, ME[2]], [ME[0], 0.35, ME[2]], [2.6, 1.5, -1.6], [2.6, 0.5, 1.6], [MIN[0], 2.45, MIN[2]]], top=0.14, bottom=0.8)])   # (review 1) less empty road under them   # three-quarter on him from the road side (side on, his box head read as its back)
st.cue('sfx:brake', 'S04', r(STOP4 - 0.1), 0.25); st.cue('sfx:carDoor', 'S04', r(OUT4 - 0.05), 0.25)

# 5: with the republican guard. A line of guards in plumed helmets along the kerb, swords at the shoulder; on a beat all four snap a salute together,
#    the plumes bouncing; one beat late, the last one
D5 = st.dur('S05'); SAL5 = 0.4
G5 = [[r(3.6 - 0.0 * j), 0, r(-2.6 + 1.3 * j)] for j in range(4)]
SALUTE = lambda: {'reach': {'R': [0.0, 0.0, 0.0, 0, 0.0]}}
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[*[act(f'garde{j + 1}', G5[j], 0, 'stand', 'determined', keys=[k(0.0, look=[G5[j][0], 1.9, 8.0]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(r(SAL5 + (0.18 if j == 3 else 0.0)), clip='salute'), k(r(SAL5 + (0.18 if j == 3 else 0.0)), toon={'sq': [0.97, 1.05, 0.97], 'face': {'lid': 0.2, 'mouth': 'line'}}, toonDur=0.05, toonEase='out'),
            k(r(SAL5 + 0.12 + (0.18 if j == 3 else 0.0)), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.1)] + ([k(r(SAL5 + 0.5), look=[G5[2][0], 1.9, G5[2][2]], lookDur=0.1)] if j == 3 else [])) for j in range(4)]],   # the last one late, then a glance at his neighbour
        props=[*[GUARD(f'casque5{j}', f'garde{j + 1}') for j in range(4)]],
        cams=[FC(0.0, [0.8, 0.7, 3.9], [[G5[0][0], 2.75, G5[0][2]], [G5[3][0], 2.75, G5[3][2]], [G5[3][0], 0.0, G5[3][2]], [G5[1][0], 1.2, G5[1][2]]], top=0.1, bottom=0.8)])   # (review 1) further round: four silhouettes, not one mass   # low, down the line of guards in perspective (the same set-up as S04)
st.cue('sfx:clack' if False else 'clack', 'S05', SAL5, 0.35); st.cue('clack', 'S05', r(SAL5 + 0.18), 0.25)

# 6: the street was closed. Barriers across the road, a sign RUE FERMÉE; behind them a jam of cars, one honking, a policeman whistling
D6 = st.dur('S06')
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[act('flic', [1.2, 0, 3.4], 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, 8.0]), k(0.0, toon={'reach': {'R': [1.3, 2.35, 3.6, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.2, 'mouth': 'whistle'}}, toonDur=0.0),
            *[k(r(0.15 + 0.25 * j), toon={'reach': {'R': [r(1.3 + (0.15 if j % 2 else -0.15)), 2.35, 3.6, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.2, 'mouth': 'whistle'}}, toonDur=0.08) for j in range(5)]])],
        props=[*[P(f'barr6{j}', 'crowdBarrier', pos=[r(-3.0 + 2.0 * j), 0, 2.6], opts={'w': 1.9}) for j in range(4)],
               P('ferme6', 'signBoard', pos=[0.0, 0, 2.3], ry=180, opts={'text': 'RUE FERMÉE', 'bg': '#C8322A', 'fg': '#FFFFFF', 'w': 1.4, 'h': 0.42, 'height': 1.05, 'posts': True}),
               *[P(f'voit6{j}', 'car', pos=[r(-2.2 + 2.6 * (j % 2)), 0, r(5.6 + 3.4 * (j // 2))], ry=180, opts={'color': ['#C8322A', '#2F62B5', '#E2B53C', '#4A8C5A', '#8A5AA8', '#D9734E'][j], 'glass': 0.8, 'glassColor': '#33404A'},
                   keys=([k(0.58, to=[-2.2, 0.16, 5.6], dur=0.06, ease='out'), k(0.64, to=[-2.2, 0.0, 5.6], dur=0.08, ease='in'), k(0.72, squash=[1.05, 0.88, 1.05], dur=0.3)] if j == 0 else [])) for j in range(6)]],   # (review 1) six cars, the first one hops as it honks
        cams=[FC(0.0, [3.0, 1.25, -2.2], [[0.0, 1.6, 2.3], [-2.6, 0.5, 2.6], [2.6, 0.5, 2.6], [1.2, 2.45, 3.4], [-2.2, 1.4, 12.0]], top=0.14, bottom=0.8)])   # (review 1) nearer the policeman, less road
st.cue('sfx:whistle', 'S06', 0.1, 0.25); st.cue('sfx:honkLong', 'S06', 0.6, 0.2)

# 7: a brass band played. Three bandsmen in red: trumpet, tuba, drum; cheeks puffed, the drum skin jumping on the beat, the tuba player swaying
D7 = st.dur('S07'); BEATS7 = [r(0.12 + 0.24 * j) for j in range(int(D7 / 0.24))]
BAND = [('musi1', [3.4, 0, -0.9], 'trumpet'), ('musi2', [3.6, 0, 0.3], 'tuba'), ('musi3', [3.4, 0, 1.5], 'drum')]
PLAY7 = lambda p_, kd, i: {'reach': {'R': [r(p_[0] + (0.42 if kd == 'trumpet' else 0.4)), 1.86 if kd == 'trumpet' else 1.3, r(p_[2] + 0.04), 1, 0.03], 'L': [r(p_[0] + (0.36 if kd == 'trumpet' else 0.35)), 1.84 if kd == 'trumpet' else 1.3, r(p_[2] + 0.14), 1, 0.03]},
                             'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.03, 0.97, 1.03] if i % 2 == 0 else [0.98, 1.03, 0.98],
                             'scl': {'head': [1.12, 0.94, 1.1] if (i % 2 == 0 and kd != 'drum') else [1.0, 1.0, 1.0]}, 'face': {'puff': (1.0 if i % 2 == 0 else 0.6) if kd != 'drum' else 0.0, 'lid': 0.3}}   # (review 1) every beat keeps the pose
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[*[act(n_, p_, 80, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=PLAY7(p_, kd, 0), toonDur=0.0),
            *[k(b_, toon=PLAY7(p_, kd, i), toonDur=0.08) for i, b_ in enumerate(BEATS7)]]) for n_, p_, kd in BAND]],
        props=[*[P(f'instr7{j}', 'brass', on={'actor': n_, 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'kind': kd, 's': 1.2, **({'beat': BEATS7} if kd == 'drum' else {})}) for j, (n_, p_, kd) in enumerate(BAND)],
               *[P(f'kepi7{j}', 'copCap', on={'actor': n_, 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}, opts={'color': '#B5302A'}) for j, (n_, p_, kd) in enumerate(BAND)]],
        cams=[FC(0.0, [5.9, 1.7, 0.4], [[3.4, 2.75, -0.9], [3.4, 2.75, 1.5], [3.6, 0.9, 0.3], [3.4, 0.9, -1.1], [3.4, 0.9, 2.05]], top=0.1, bottom=0.8)])   # (review 1) the drum inside the frame
for b_ in BEATS7[::2]: st.cue('thud', 'S07', b_, 0.2)
st.cue('sfx:fanfare', 'S07', 0.05, 0.3)

# 8: helicopters flew over the neighbourhood. Low on the pavement looking up past the roofs: two helicopters sweep over, rotors blurring; he looks up
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[9.0, 12.0, -4.0]), k(0.0, toon=LIP, toonDur=0.0), *BLINK(0.7), k(r(D8 * 0.6), look=[9.0, 12.0, 4.0], lookDur=0.4)])],
        props=[P('heli8a', 'helicopter', pos=[8.6, 9.6, -9.0], ry=0, scale=1.5, keys=[k(0.0, to=[8.6, 9.2, 9.0], dur=D8, ease='linear')]),
               P('heli8b', 'helicopter', pos=[10.5, 11.0, -15.0], ry=0, scale=1.5, keys=[k(0.0, to=[10.5, 10.6, 5.0], dur=D8, ease='linear')])],   # (stills 1) lower and nearer: they were cut off at the top
        cams=[FC(0.0, [3.0, 0.6, 1.3], [[ME[0], 2.45, ME[2]], [ME[0], 1.2, ME[2]], [8.6, 10.2, 0.0], [10.5, 11.6, -4.0], [8.6, 8.8, 0.0], [7.6, 13.5, 0.0]], top=0.06, bottom=0.8, lenses=range(26, 72))])   # (review 1) up past the roofs into the sky   # low in front of him, the helicopters over the roofs behind him
st.cue('sfx:chainsaw' if False else 'engine', 'S08', 0.0, 0.3)

# 9: the cent arrived on a velvet cushion. A guard walks slowly toward us carrying the red cushion on both palms; on it, tiny and gleaming, the cent;
#    a glint (REMBOURSÉ)
D9 = st.dur('S09'); G9 = [3.0, 0, -2.4]
CUSH = {'reach': {'R': [0.0, 0.0, 0.0, 0, 0.0]}}
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('garde3', G9, 0, 'walk', 'determined', keys=[k(0.0, to=[3.0, 0, -0.6], dur=D9, clip='walk', ease='linear'), k(0.0, clip='walk', speed=0.55), k(0.0, look='camera'),
            k(0.0, toon={'touch': {'R': ['torso', -0.12, 0.08, 0.32, 1, 0.02], 'L': ['torso', 0.12, 0.08, 0.32, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[GUARD('casque9', 'garde3'), P('coussin9', 'velvetCushion', on={'actor': 'garde3', 'joint': 'torso', 'offset': [0.0, 0.12, 0.36]}, opts={'w': 0.34}),
               P('piece9', 'glintCoin', on={'actor': 'garde3', 'joint': 'torso', 'offset': [0.0, 0.235, 0.36]}, rot=[-0.35, 0, 0], opts={'r': 0.038, 'glint': 0.3})],   # (review 1) a glint two and a half times bigger
        cams=[FC(0.0, [3.15, 1.75, 2.4], [[G9[0], 2.75, -0.8], [G9[0], 1.2, -0.8], [r(G9[0] - 0.35), 1.6, -0.8], [r(G9[0] + 0.35), 1.6, -0.8]], top=0.12, bottom=0.78, drift=(0.0, 0.0, 0.3))])
st.cue('sfx:choir', 'S09', 0.1, 0.25); st.cue('sfx:ding', 'S09', 0.6, 0.2)

# 10: the minister gave a one-hour speech. At a lectern at his door: the minister orates, hands going; behind, a guard nods off and jerks awake; the
#     shadows swing round as the hour passes; he stands deadpan
D10 = st.dur('S10'); NOD10 = 0.9
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('ministre', MIN, 90, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 2.0, ME[2]]), *[k(r(0.1 + 0.3 * j), toon={'reach': {('R' if j % 2 else 'L'): [r(MIN[0] + 0.35), r(2.0 + 0.15 * (j % 3)), r(MIN[2] + (-0.35 if j % 2 else 0.45)), 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'open' if j % 2 else 'O', 'lid': 0.2, 'brow': 0.6}}, toonDur=0.12) for j in range(int(D10 / 0.3))]]),
        act('garde1', [3.55, 0, -1.3], 90, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.9, -1.3]), k(0.3, toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': {'lid': 1.0}}, toonDur=0.4, toonEase='inOut'),
            k(NOD10, toon={'bend': {'neck': [-0.1, 0, 0, 1, None]}, 'sq': [0.95, 1.08, 0.95], 'face': {'lid': 0.0, 'eye': 0.5}}, toonDur=0.05, toonEase='out'), k(r(NOD10 + 0.15), toon={'face': {'lid': 0.3}}, toonDur=0.1)]),   # asleep... awake with a jerk
        act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[MIN[0], 2.2, MIN[2]]), k(0.0, toon=LIP, toonDur=0.0), *BLINK(0.6), *BLINK(1.4), k(1.6, look='camera')])],
        props=[P('pupitre10', 'podium', pos=[r(MIN[0] + 0.3), 0, MIN[2]], ry=90, opts={'text': 'RÉPUBLIQUE'}), COCK('ck10', 'ministre'), GUARD('casque10', 'garde1'),
               P('horloge10', 'wallClock', pos=[7.45, 2.8, -0.85], ry=-90, scale=1.3, opts={'rate': 2.5})],   # (review 1) the hour passing: the clock's hands whirl round
        cams=[FC(0.0, [4.9, 1.55, 4.2], [[ME[0], 2.45, ME[2]], [MIN[0], 2.45, MIN[2]], [3.55, 2.95, -1.3], [3.25, 1.0, -1.3], [MIN[0], 0.9, MIN[2]], [ME[0], 0.9, ME[2]], [7.45, 3.25, -0.85]], top=0.12, bottom=0.78)])   # (review 1) in front of them both: two faces, the clock, the dozing guard whole   # three-quarter on him from the road side (stills 1: the guard is behind the minister now, he filled the foreground)
st.cue('sfx:ticks', 'S10', 0.1, 0.2); st.cue('sfx:boing', 'S10', NOD10, 0.15)

# 11: the neighbours wept. Up the facade, the neighbours at their windows, handkerchiefs out, tears spurting in arcs
D11 = st.dur('S11')
NB11 = [('voisin1', [7.25, 3.25, -1.6], 'mamie'), ('voisin2', [7.25, 3.25, 1.8], 'madame'), ('voisin3', [7.25, 6.3, 0.1], 'boss')]   # (stills 1) on the balconies (in front of the facade they floated)
HANKY = {'touch': {'R': ['face', -0.14, 0.6, 0.12, 1, 0.02]}, 'hands': {'R': 'pinch'}}
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[*[act(n_, p_, -90, 'stand', 'sad', keys=[k(0.0, look=[4.4, 1.0, 0.3]), k(0.0, toon={**HANKY, 'face': {'lid': 0.7, 'mouth': 'cry', 'brow': 1.0}}, toonDur=0.0),
            *[k(r(0.12 + 0.22 * i + 0.07 * j), toon={**HANKY, 'sq': [1.04, 0.95, 1.04] if i % 2 else [0.98, 1.03, 0.98], 'face': {'lid': 0.75, 'mouth': 'cry', 'brow': 1.0}}, toonDur=0.08) for i in range(int(D11 / 0.22))]]) for j, (n_, p_, _) in enumerate(NB11)]],   # (review 1) the handkerchief held at the eye on every sob
        props=[*[P(f'larmes11{j}', 'tearFountain', on={'actor': n_, 'joint': 'head'}, opts={'at': r(0.05 + 0.1 * j), 'r': 0.036, 'speed': 1.8, 'rate': 10}) for j, (n_, p_, _) in enumerate(NB11)],   # (review 1) tears twice as big
               *[P(f'mouch11{j}', 'slab', on={'actor': n_, 'hand': 'R', 'offset': [0.0, -0.06, 0.03], 'face': 'camera'}, opts={'w': 0.15, 'h': 0.15, 'd': 0.006, 'color': '#F8F6F0', 'outline': 0.004}) for j, (n_, p_, _) in enumerate(NB11)],   # a white handkerchief
               *[P(f'balc11{j}', 'balcony', pos=[7.2, p_[1], p_[2]], ry=-90, opts={'w': 1.3, 'd': 0.85, 'rail': 'front'}) for j, (n_, p_, _) in enumerate(NB11)]],   # (review 1) a stone balcony with an iron rail under each (black slabs read as voids)
        cams=[FC(0.0, [3.6, 2.6, 2.4], [[7.25, 5.75, -1.6], [7.25, 5.75, 1.8], [7.25, 8.8, 0.1], [7.25, 3.4, -1.6], [7.25, 3.4, 1.8]], top=0.12, bottom=0.8, lenses=range(26, 64))])
st.cue('sfx:gasp', 'S11', 0.1, 0.15)

# 12: television filmed it live. Behind the barriers, TV cameras on tripods, a reporter with a microphone, EN DIRECT; the red lights on
D12 = st.dur('S12')
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[act('reporter', [2.2, 0, -1.2], 60, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [2.45, 1.95, -0.9, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'open', 'lid': 0.1, 'brow': 0.8}}, toonDur=0.0),
            *[k(r(0.1 + 0.25 * j), toon={'reach': {'R': [2.45, 1.95, -0.9, 1, 0.03], 'L': [r(2.55 + (0.12 if j % 2 else -0.05)), r(1.5 + (0.25 if j % 2 else 0.0)), -0.85, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': [1.02, 0.98, 1.02] if j % 2 else [0.99, 1.02, 0.99], 'face': {'mouth': 'open' if j % 2 else 'O', 'lid': 0.1, 'brow': 0.8}}, toonDur=0.1) for j in range(int(D12 / 0.25))]])],   # (review 1) the free hand gesturing
        props=[*[P(f'tv12{j}', 'tvCamera', pos=[r(1.0 + 1.1 * j), 0, r(1.2 + 0.5 * j)], ry=r(-60 + 25 * j)) for j in range(3)],
               P('direct12', 'signBoard', pos=[2.4, 2.5, -2.2], ry=40, opts={'text': 'EN DIRECT', 'bg': '#C8322A', 'fg': '#FFFFFF', 'w': 1.1, 'h': 0.32, 'posts': False, 'height': 0}),
               P('micro12', 'megaphone', on={'actor': 'reporter', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, scale=0.35),
               *[P(f'barr12{j}', 'crowdBarrier', pos=[r(0.6 + 1.9 * j), 0, 2.5], opts={'w': 1.8}) for j in range(2)]],
        cams=[FC(0.0, [1.3, 1.5, 2.9], [[2.2, 2.45, -1.2], [1.9, 2.95, -2.2], [2.9, 2.95, -2.2], [1.0, 0.6, 1.2], [2.2, 0.6, -1.2]], top=0.1, bottom=0.8)])   # (review 1) from the other side of the cameras   # (stills 1) nearer the reporter, the sign whole
st.cue('sfx:shutter', 'S12', 0.3, 0.15); st.cue('sfx:shutter', 'S12', 0.9, 0.15)

# 13: he put the cent in his piggy bank. His kitchen table, close: his fingers hold the cent over the pink pig; he lets go; it drops into the slot
#     (clink) and the pig jiggles; a look at us
D13 = st.dur('S13'); DROP13 = 0.65; PIG = [0.15, 0.76, -1.3]
st.shot('S13', 'kitchenDay', actors=[act('mec', [0.15, 0, -1.95], 0, 'stand', 'neutral', keys=[k(0.0, look=PIG), k(0.0, toon={'reach': {'R': [0.2, 1.15, -1.32, 1, 0.03]}, 'hands': {'R': 'pinch'}, **LIP}, toonDur=0.0),
            k(r(DROP13 - 0.1), toon={'reach': {'R': [0.2, 1.17, -1.3, 1, 0.03]}, 'hands': {'R': 'open'}, **LIP}, toonDur=0.06), k(r(DROP13 + 0.45), look='camera'), *BLINK(r(DROP13 + 0.8), {'mouth': 'line'})])],
        props=[P('table13', 'table', pos=[0.15, 0, -1.3], opts={'w': 1.0, 'd': 0.7, 'h': 0.76}), P('cochon13', 'piggyBank', pos=PIG, ry=20, opts={'s': 1.25, 'dropAt': [DROP13], 'jig': 3.0})],   # (review 1) a jiggle three times bigger
        cams=[FC(0.0, [0.42, 1.12, -0.82], [[0.18, 1.24, -1.3], [PIG[0], 0.78, PIG[2]], [r(PIG[0] - 0.2), 0.95, PIG[2]], [r(PIG[0] + 0.2), 0.95, PIG[2]]], top=0.18, bottom=0.72, lenses=range(20, 60)),   # (review 1) a macro: fingers, cent, slot
              FC(r(DROP13 + 0.42), [0.7, 1.5, 0.3], [[0.15, 2.45, -1.95], [PIG[0], 0.75, PIG[2]], [r(PIG[0] - 0.3), 1.0, PIG[2]], [r(PIG[0] + 0.3), 1.0, PIG[2]]], top=0.12, bottom=0.78)])   # then him and the pig at us
st.cue('sfx:clink', 'S13', r(DROP13 + 0.2), 0.35)

# 14: the next day he got a bill. His front door from inside: a fat envelope slides in under the door (swish), he picks it up and tears it open
D14 = st.dur('S14'); IN14 = 0.25
st.shot('S14', 'kitchenDay', actors=[act('mec', [0.6, 0, -1.6], 0, 'stand', 'neutral', keys=[k(0.0, look=[1.6, 0.05, -1.0]), k(0.35, look=[0.9, 0.05, -1.05], lookDur=0.2), k(0.0, toon=LIP, toonDur=0.0),
            k(0.7, toon={'bend': {'spine': [0.6, 0, 0, 1, None]}, 'reach': {'R': [0.88, 0.12, -1.08, 1, 0.03]}, 'hands': {'R': 'pinch'}, **LIP}, toonDur=0.2, toonEase='inOut'),
            k(1.15, toon={'reach': {'R': [0.5, 1.6, -1.25, 1, 0.03], 'L': [0.7, 1.6, -1.25, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.2, toonEase='inOut'), k(1.4, look=[0.6, 1.6, -1.25])])],
        props=[P('lettre14', 'envelope', pos=[2.6, 0.012, -0.9], rot=[-PI / 2, 0, 0.2], scale=2.0, keys=[k(IN14, to=[0.9, 0.012, -1.05], dur=0.25, ease='out'), k(0.9, attach='mec', hand='R', offset=[0.0, -0.06, 0.03])])],   # (review 1) picked up (with a dict for attach it stayed on the floor)
        cams=[FC(0.0, [1.4, 1.35, 1.1], [[0.6, 2.45, -1.6], [0.9, 0.0, -1.05], [0.6, 0.0, -1.6], [2.1, 0.1, -0.9], [0.8, 1.95, -1.0]], top=0.12, bottom=0.74)])   # (review 1) his head in frame when he bends, the envelope above the captions
st.cue('sfx:paper', 'S14', IN14, 0.25); st.cue('sfx:zip', 'S14', 1.2, 0.2)

# 15: two million euros. The bill unrolls out of his hands down to the floor and on across it toward us, line after line; at the bottom, huge,
#     2 000 000 € (the card)
D15 = st.dur('S15')
st.shot('S15', 'kitchenDay', actors=[act('mec', [0.3, 0, -1.3], 0, 'stand', 'neutral', keys=[k(0.0, look=[0.3, 1.0, -0.4]), k(0.0, toon={'reach': {'R': [0.2, 1.55, -0.95, 1, 0.03], 'L': [0.42, 1.55, -0.95, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.0),
            k(0.7, look='camera'), k(1.0, toon={'reach': {'R': [0.2, 1.55, -0.95, 1, 0.03], 'L': [0.42, 1.55, -0.95, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07),
            k(1.12, toon={'reach': {'R': [0.2, 1.55, -0.95, 1, 0.03], 'L': [0.42, 1.55, -0.95, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.08)])],   # (review 1) the blink keeps his hands on the bill (they dropped)
        props=[P('facture15', 'billScroll', pos=[0.31, 1.55, -0.92], opts={'w': 0.36, 'top': 1.55, 'head': 'FACTURE', 'items': ['VOITURE 480 000 €', 'GARDE 620 000 €', 'FANFARE 230 000 €', 'HÉLICOPTÈRES 540 000 €', 'COUSSIN 129 999,99 €', 'CENTIME 0,01 €', 'TOTAL : 2 000 000 €'], 'len': [[0.0, 0.2], [0.2, 1.55], [r(D15 - 0.1), 3.4]]})],
        cams=[FC(0.0, [0.7, 1.45, 1.1], [[0.3, 2.45, -1.3], [0.3, 0.0, -0.4], [0.3, 0.0, 0.6], [0.05, 1.0, -0.6], [0.55, 1.0, -0.6]], top=0.22, bottom=0.82)])   # (review 1) his head below the 2 000 000 € card
st.cue('sfx:paper', 'S15', 0.1, 0.2); st.cue('sfx:slideDown', 'S15', 0.25, 0.25)

# 16: travel expenses. Close on the bill's last line, FRAIS DE DÉPLACEMENT, then up to him: deadpan, a slow blink, a look at us; beside him on the
#     table, the pink pig
D16 = st.dur('S16')
st.shot('S16', 'kitchenDay', actors=[act('mec', [0.3, 0, -1.3], 0, 'stand', 'neutral', keys=[k(0.0, look=[0.3, 1.2, -0.9]), k(0.0, toon={'reach': {'R': [0.2, 1.3, -0.95, 1, 0.03], 'L': [0.42, 1.3, -0.95, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.0),
            k(0.45, look='camera'), k(0.75, toon={'reach': {'R': [0.2, 1.3, -0.95, 1, 0.03], 'L': [0.42, 1.3, -0.95, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.14, toonEase='inOut'),
            k(0.95, toon={'reach': {'R': [0.2, 1.3, -0.95, 1, 0.03], 'L': [0.42, 1.3, -0.95, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.14, toonEase='inOut')])],
        props=[P('frais16', 'paperSheet', on={'actor': 'mec', 'hand': 'R', 'offset': [0.11, 0.02, 0.03], 'face': 'camera'}, opts={'w': 0.5, 'h': 0.3, 'head': 'FRAIS DE', 'big': 'DÉPLACEMENT', 'bright': True}),   # (review 1) face to the camera (edge-on it read as a wire), the words in large type
               P('table16', 'table', pos=[-0.75, 0, -1.4], opts={'w': 0.8, 'd': 0.6, 'h': 0.76}), P('cochon16', 'piggyBank', pos=[-0.6, 0.76, -1.3], ry=40, opts={'s': 1.25})],
        cams=[FC(0.0, [0.25, 1.35, -0.25], [[0.31, 1.47, -0.92], [0.31, 1.13, -0.92], [0.04, 1.3, -0.92], [0.58, 1.3, -0.92]], top=0.25, bottom=0.66),   # (review 1) the last line first, filling the width...
              glide([FC(0.5, [-0.35, 1.45, 0.5], [[0.3, 2.45, -1.3], [0.3, 1.15, -1.3], [-0.6, 0.85, -1.3], [0.5, 1.3, -0.95]], top=0.12, bottom=0.78)], 0.35)])   # ...then up to his face, the pig beside him

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le centime", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'agent': {'preset': 'officiel', 'seed': 771, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'agent2': {'preset': 'avocat', 'seed': 772, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef': {'preset': 'boss', 'seed': 773, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'off1': {'preset': 'politique', 'seed': 774, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off2': {'preset': 'avocat', 'seed': 775, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off3': {'preset': 'officiel', 'seed': 776, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 777, 'suit': '#34405A', 'lapel': '#34405A', 'tie': '#2F62B5', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'garde{j + 1}': {'preset': 'boss', 'seed': 778 + j, 'suit': '#2B3A66', 'lapel': '#2B3A66', 'tie': '#C8322A', 'pants': '#F2F2EE', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},
    'flic': {'preset': 'cop', 'seed': 782, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'musi{j + 1}': {'preset': 'serveur', 'seed': 783 + j, 'suit': '#B5302A', 'pants': '#1C1F2A', 'build': {'width': 1.0 + 0.1 * (j == 1), 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    'voisin1': {'preset': 'mamie', 'seed': 786, 'build': {'width': 1.0, 'headWidth': 1.25}, 'toon': EX},
    'voisin2': {'preset': 'madame', 'seed': 787, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'voisin3': {'preset': 'boss', 'seed': 788, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'reporter': {'preset': 'journaliste', 'seed': 789, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
