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
GUARD = lambda pid, who, **o: P(pid, 'guardHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, scale=1.1, opts={'gold': True, **o})   # (stills 1) on top of the head (at 0.26 it sat on his chin); (pass 3) gold, a tall red plume
EPAU = lambda pid, who: P(pid, 'epaulettes', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.635, 0.0]}, opts={'w': 0.58})   # (pass 3) red epaulettes with a gold fringe
SABRE = lambda pid, who: P(pid, 'sabre', on={'actor': who, 'joint': 'torso', 'offset': [0.26, 0.02, 0.15]})   # (pass 3) a sabre at the left shoulder (the right hand salutes)
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
        cams=[FC(0.0, [-3.9, 1.6, 1.4], [[-4.6, 1.95, -2.15], [-3.75, 2.45, -1.05], [-3.4, 2.3, -1.05], [-3.4, 1.0, -1.05], [-4.95, 0.85, -1.45], [-3.75, 0.5, -1.05], [-4.6, 2.2, -3.55], [-5.6, 1.65, -1.6]], top=0.12, bottom=0.78, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])   # (pass 3) room on his right: his head was cut by the frame edge
st.cue('sfx:click', 'S01', 0.1, 0.1); st.cue('sfx:click', 'S01', 0.34, 0.1); st.cue('sfx:siren', 'S01', AL1, 0.35)

# 2: the tax office decided to refund him. A meeting room at the ministry: four officials round a table, a board TROP-PERÇU 0,01 €; the chief bangs the
#    table and all four nod at once
D2 = st.dur('S02'); BANG2 = 0.55
OFF2 = [('chef', [-4.6, 0, -2.15], 0, 'boss'), ('off1', [-5.45, 0, -1.35], 90, 'politique'), ('off2', [-3.75, 0, -1.35], -90, 'avocat'), ('off3', [-4.6, 0, -0.55], 180, 'officiel')]
NOD = lambda t: [k(t, toon={'bend': {'neck': [0.5, 0, 0, 1, None]}, 'sq': [1.05, 0.93, 1.05], 'face': {'lid': 0.3}}, toonDur=0.06, toonEase='out'), k(r(t + 0.14), toon={'bend': {'neck': [-0.08, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': DEAD}, toonDur=0.1),
                 k(r(t + 0.26), toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.1)]   # (review 1) a deep nod, an overshoot back, settle
st.shot('S02', 'office', actors=[
        *[act(n_, p_, ry_, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 1.2, -1.35]), *(NOD(r(BANG2 + 0.12)) + NOD(r(BANG2 + 0.42)) + [k(1.28, look=[-4.6, 1.9, -2.15], lookDur=0.1), k(1.55, look='camera', lookDur=0.12)] + NOD(1.78) if n_ != 'chef' else   # (pass 3) the hold lives: a look at the chief, at us, a last nod
            [k(r(BANG2 - 0.28), toon={'reach': {'R': [-4.45, 1.85, -1.8, 1, 0.03]}, 'hands': {'R': 'fist'}, 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.2, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.2, toonEase='out'),
             k(BANG2, toon={'reach': {'R': [-4.45, 0.8, -1.65, 1, 0.03]}, 'hands': {'R': 'fist'}, 'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.1, 'brow': -0.9, 'mouth': 'open'}}, toonDur=0.05, toonEase='in'), k(r(BANG2 + 0.4), look='camera'), k(1.3, toon={'reach': {'R': [-4.45, 0.8, -1.65, 1, 0.03]}, 'hands': {'R': 'fist'}, 'face': {'lid': 1.0, 'brow': -0.6, 'mouth': 'line'}}, toonDur=0.07), k(1.42, toon={'reach': {'R': [-4.45, 0.8, -1.65, 1, 0.03]}, 'hands': {'R': 'fist'}, 'face': {'lid': 0.2, 'brow': -0.6, 'mouth': 'line'}}, toonDur=0.08),
             k(1.78, toon={'reach': {'R': [-4.45, 0.8, -1.65, 1, 0.03]}, 'hands': {'R': 'fist'}, 'bend': {'neck': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'brow': -0.6, 'mouth': 'line'}}, toonDur=0.08), k(1.95, toon={'reach': {'R': [-4.45, 0.8, -1.65, 1, 0.03]}, 'hands': {'R': 'fist'}, 'face': {'lid': 0.2, 'brow': -0.6, 'mouth': 'line'}}, toonDur=0.1)])]) for n_, p_, ry_, _ in OFF2]],
        props=[P('table2', 'desk', pos=[-4.6, 0, -1.35], opts={'w': 1.4}, keys=[k(BANG2, squash=[1.04, 0.84, 1.04], dur=0.35)]),   # (review 1) the slam flattens the table...
               *[P(f'pap2{j}', 'slab', pos=[r(-5.0 + 0.4 * j), 0.79, r(-1.25 - 0.08 * j)], opts={'w': 0.22, 'h': 0.012, 'd': 0.28, 'color': '#FBF8EE'}, keys=[k(BANG2, to=[r(-5.0 + 0.4 * j), r(0.98 + 0.04 * j), r(-1.25 - 0.08 * j)], dur=0.08, ease='out'), k(r(BANG2 + 0.08), to=[r(-5.0 + 0.4 * j), 0.79, r(-1.25 - 0.08 * j)], dur=0.12, ease='in')]) for j in range(3)],
               P('tab2', 'signBoard', pos=[-4.6, 1.5, -3.55], opts={'text': 'TROP-PERÇU\n0,01 €', 'bg': '#F6F1E3', 'fg': '#C8322A', 'frame': '#26365F', 'w': 1.5, 'h': 0.8, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [-3.6, 2.75, 1.2], [[-4.6, 1.9, -2.15], [-5.45, 1.9, -1.35], [-3.75, 1.9, -1.35], [-4.6, 2.35, -3.55], [-5.4, 1.5, -3.55], [-3.8, 1.5, -3.55], [-4.6, 0.7, -0.6]], top=0.1, bottom=0.8, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])   # (stills 1) high over the near officials' heads (their backs filled the frame), the board whole
st.cue('thud', 'S02', BANG2, 0.35)

# 3: but the stamp cost more than the cent. (pass 3) A true top-down macro on a green desk pad: the envelope above, the cheque below, both as wide as
#    the frame; the rubber stamp hovers over the envelope's corner, rises toward the lens, slams (the desk shakes, the cheque flips): a postage stamp
#    3,00 € beside the cheque's 0,01 €; then head and shoulders on the official, sweating, his eyes darting
D3 = st.dur('S03'); SLAP3 = 0.6
ENV3 = [-4.6, 0.772, -1.6]; CHQ3 = [-4.6, 0.772, -1.32]; STP3 = [-4.47, 0.79, -1.645]   # (stills 1) the cheque above the caption band
SW3 = {'lid': 0.2, 'mouth': 'zigzag', 'sweat': 1.0, 'brow': 0.6}
st.shot('S03', 'office', fx=[{'type': 'shake', 'at': SLAP3, 'dur': 0.3, 'amount': 0.012}], actors=[act('agent2', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.5, 0.77, -1.6]),
            k(0.0, toon={'reach': {'R': [STP3[0], 1.02, STP3[2], 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.0),
            k(0.28, toon={'reach': {'R': [-4.5, 1.2, -1.6, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [0.97, 1.05, 0.97], 'face': {'lid': 0.2, 'brow': -0.6}}, toonDur=0.26, toonEase='out'),   # the wind-up, toward the lens (stills 1: lower and nearer the middle, it left the frame by the corner)
            k(SLAP3, toon={'reach': {'R': [STP3[0], 0.9, STP3[2], 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.05, 0.94, 1.05], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.05, toonEase='in'),   # thump
            k(r(SLAP3 + 0.16), toon={'reach': {'R': [-4.28, 1.12, -2.0, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': SW3}, toonDur=0.14, toonEase='out'),   # the hand lifts away: the stamp shows
            k(r(SLAP3 + 0.4), look='camera'), *BLINK(1.3, SW3), k(1.5, look=[-6.2, 1.7, 0.5], lookDur=0.08), k(1.72, look=[-3.0, 1.7, 0.5], lookDur=0.08), k(1.95, look='camera', lookDur=0.08),   # his eyes dart: left, right, us
            k(2.08, toon={'reach': {'R': [-4.28, 1.12, -2.0, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.94, 1.04], 'face': {**SW3, 'mouth': 'clench'}}, toonDur=0.08),   # a gulp
            k(2.22, toon={'reach': {'R': [-4.28, 1.12, -2.0, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.0, 1.0, 1.0], 'face': SW3}, toonDur=0.1), *BLINK(2.36, SW3)])],
        props=[P('pc3', 'laptop', pos=[-5.05, 0.76, -1.75], ry=200),
               P('sous3', 'slab', pos=[-4.6, 0.764, -1.42], opts={'w': 0.5, 'h': 0.008, 'd': 0.86, 'color': '#2F5D50', 'outline': 0.004}, keys=[k(1.02, visible=False)]),   # a desk pad: one calm ground under the two papers
               P('env3', 'slab', pos=ENV3, opts={'w': 0.4, 'h': 0.006, 'd': 0.25, 'color': '#FDFBF3', 'outline': 0.004}, keys=[k(SLAP3, squash=[1.06, 0.6, 1.06], dur=0.3)]),
               *[P(f'adr3{j}', 'slab', pos=[-4.68, 0.777, r(ENV3[2] + 0.045 * j)], opts={'w': 0.17 - 0.03 * j, 'h': 0.003, 'd': 0.012, 'color': '#8A8F98'}) for j in range(3)],
               P('timbre3', 'postStamp', pos=STP3, rot=[-PI / 2, 0, -0.08], opts={'w': 0.145, 'h': 0.18, 'text': '3,00 €', 'at': SLAP3}),
               P('chq3', 'taxCheque', pos=CHQ3, rot=[-PI / 2, 0, 0.06], opts={'w': 0.4, 'h': 0.185, 'amount': '0,01 €'},
                 keys=[k(SLAP3, to=[CHQ3[0], 0.96, CHQ3[2]], dur=0.12, ease='out'), k(SLAP3, rotTo=[r(-PI / 2 - 2 * PI, 4), 0.0, 0.06], dur=0.3, ease='inOut'), k(r(SLAP3 + 0.12), to=CHQ3, dur=0.18, ease='in')]),   # it hops and turns right over at the thump
               P('tampon3', 'rubberStamp', on={'actor': 'agent2', 'hand': 'R', 'offset': [0.0, -0.08, 0.03]}, scale=2.2)],
        cams=[cam(0.0, [-4.6, 3.05, -1.325], [-4.6, 2.95, -1.325], [-4.6, 0.77, -1.405], lens=20),   # straight down: 0.45 m wide, the desk pad edge to edge
              FC(1.05, [-4.2, 1.8, -0.45], [[-4.6, 2.15, -2.15], [-4.6, 1.25, -2.15], [-4.97, 1.7, -2.15], [-4.23, 1.7, -2.15]], top=0.14, bottom=0.72, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])   # then head and shoulders, sweating, at us
st.cue('thud', 'S03', SLAP3, 0.4); st.cue('sfx:gasp', 'S03', r(SLAP3 + 0.4), 0.2)

# 4: so the minister came in person. (pass 3) From the pavement by his door, over his shoulder: a navy official car (chrome, a flag on each wing)
#    sweeps in past us and stops with a dip of its springs; its rear door swings open on our side and the minister shoots out of it, squeezed thin,
#    lands in a squash three-quarters to us, and snaps his jacket straight; he watches, deadpan, then turns his head to us
D4 = st.dur('S04'); STOP4 = 0.55; DOOR4 = 0.6; OUT4 = 0.78
CAR4 = [3.9, 0, -2.84]; GAP4 = [4.78, 0, -1.9]; MIN4 = [5.55, 0, -0.75]; ME4 = [6.9, 0, 0.3]
TUG4 = lambda y, sq, f: {'touch': {'R': ['torso', 0.11, y, 0.2, 1, 0.02], 'L': ['torso', -0.11, y, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': sq, 'face': f}
st.shot('S04', 'parisStreet', setOpts={**STREET, 'clear': [-9.0, 6.0]}, fx=[{'type': 'shake', 'at': STOP4, 'dur': 0.25, 'amount': 0.02}], actors=[
        act('ministre', GAP4, 50, 'stand', 'neutral', keys=[k(0.0, look=[ME4[0], 2.0, ME4[2]]), k(0.0, visible=False), k(r(OUT4 - 0.02), visible=True), k(0.0, toon={'sq': [0.6, 1.2, 0.6]}, toonDur=0.0),   # squeezed thin in the doorway (stills 1: at 1.5 his head left the frame)...
            k(OUT4, to=MIN4, dur=0.3, clip='walk', then='stand', ease='out', face='keep'),
            k(r(OUT4 + 0.28), toon={'sq': [1.24, 0.78, 1.24]}, toonDur=0.06, toonEase='out'), k(r(OUT4 + 0.42), toon={'sq': [0.95, 1.06, 0.95]}, toonDur=0.1), k(r(OUT4 + 0.54), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.08),   # ...he lands in a squash, re-inflates
            k(r(OUT4 + 0.62), toon=TUG4(0.42, [0.98, 1.05, 0.98], {'lid': 0.3, 'brow': -0.4, 'mouth': 'line'}), toonDur=0.14, toonEase='out'),   # both hands to his lapels, a breath in...
            k(r(OUT4 + 0.84), toon=TUG4(0.2, [1.06, 0.93, 1.06], {'lid': 0.2, 'brow': 0.5, 'mouth': 'line'}), toonDur=0.05, toonEase='in'),      # ...the snap
            k(r(OUT4 + 0.98), toon=TUG4(0.24, [1.0, 1.0, 1.0], {'lid': 0.25, 'mouth': 'line'}), toonDur=0.1), k(r(OUT4 + 1.2), toon={'face': {'lid': 0.2, 'mouth': 'open', 'brow': 0.5}}, toonDur=0.15)]),
        act('mec', ME4, -95, 'stand', 'neutral', keys=[k(0.0, look=[3.9, 1.2, 2.5]), k(0.0, toon=LIP, toonDur=0.0), k(0.3, look=[GAP4[0], 1.5, GAP4[2]], lookDur=0.2), k(r(OUT4 + 0.3), look=[MIN4[0], 2.2, MIN4[2]], lookDur=0.1), *BLINK(1.3, {'mouth': 'line'}),
            k(r(D4 - 0.55), face=[6.95, 0, 2.9], turn=0.24), k(r(D4 - 0.5), look='camera', lookDur=0.16), *BLINK(r(D4 - 0.18), {'mouth': 'line'})])],   # his back to us, his head following the car, the minister; then he turns round to us
        props=[P('auto4', 'ministerCar', pos=[3.9, 0, 6.6], ry=90, opts={'doorSide': 1, 'hingeFront': True, 'doorAt': DOOR4}, keys=[k(0.0, to=CAR4, dur=STOP4, ease='out'), k(STOP4, squash=[1.05, 0.8, 1.05], dur=0.5)]), COCK('ck4', 'ministre')],
        cams=[FC(0.0, [6.95, 1.55, 2.9], [[ME4[0], 2.5, ME4[2]], [ME4[0], 1.0, ME4[2]], [r(ME4[0] + 0.3), 1.8, ME4[2]], [MIN4[0], 2.5, MIN4[2]], [MIN4[0], 0.3, MIN4[2]], [5.05, 1.5, -0.6], [4.83, 2.05, -1.9], [4.68, 1.5, -4.59]], top=0.12, bottom=0.8, lenses=range(26, 72))])
st.cue('sfx:brake', 'S04', r(STOP4 - 0.1), 0.25); st.cue('sfx:carDoor', 'S04', r(DOOR4), 0.25); st.cue('whoosh', 'S04', OUT4, 0.2)

# 5: with the republican guard. A line of guards along the kerb; (pass 3) gold helmets with a tall red plume and a black tail, red epaulettes, white
#    gloves, a sabre at the shoulder; on a beat three snap a salute together; the last one glances at his neighbour, eyes wide, and over-snaps his
#    half a second late: his helmet tips over his eyes; the neighbour's eyes slide to him
D5 = st.dur('S05'); SAL5 = 0.4; LATE5 = 0.45
G5 = [[r(3.6 - 0.0 * j), 0, r(-2.6 + 1.3 * j)] for j in range(4)]
GF5 = {'lid': 0.3, 'mouth': 'line'}
def G5KEYS(j):
    d = LATE5 if j == 3 else 0.0
    ks = [k(0.0, look=[G5[j][0], 1.9, 8.0]), k(0.0, toon={'face': GF5}, toonDur=0.0), k(r(SAL5 + d), clip='salute'),
          k(r(SAL5 + d), toon={'sq': [0.9, 1.16, 0.9] if j == 3 else [0.95, 1.08, 0.95], 'face': {'lid': 0.2, 'mouth': 'line'}}, toonDur=0.05, toonEase='out'),
          k(r(SAL5 + d + 0.12), toon={'sq': [1.04, 0.96, 1.04], 'face': GF5}, toonDur=0.08), k(r(SAL5 + d + 0.24), toon={'sq': [1.0, 1.0, 1.0], 'face': GF5}, toonDur=0.08)]
    if j == 3: ks += [k(r(SAL5 + 0.1), look=[G5[2][0], 1.9, G5[2][2]], lookDur=0.08), k(r(SAL5 + 0.16), toon={'sq': [1.0, 1.03, 1.0], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.06),
                      k(r(SAL5 + d - 0.04), look=[G5[3][0], 1.9, 8.0], lookDur=0.05)]   # the late one: a glance at his neighbour, the eyes wide, then he snaps
    if j == 2: ks += [k(r(SAL5 + LATE5 + 0.3), look=[G5[3][0], 1.9, G5[3][2]], lookDur=0.12), k(r(SAL5 + LATE5 + 0.3), toon={'face': {'lid': 0.45, 'brow': -0.8, 'mouth': 'line'}}, toonDur=0.1, keepPose=True)]   # the neighbour's eyes slide to him
    return ks
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[*[act(f'garde{j + 1}', G5[j], 0, 'stand', 'determined', keys=G5KEYS(j)) for j in range(4)]],
        props=[*[GUARD(f'casque5{j}', f'garde{j + 1}', **({'knockAt': [r(SAL5 + LATE5 + 0.05)], 'knock': 0.6, 'stay': 0.55} if j == 3 else {})) for j in range(4)],
               *[EPAU(f'epau5{j}', f'garde{j + 1}') for j in range(4)], *[SABRE(f'sabre5{j}', f'garde{j + 1}') for j in range(4)]],
        cams=[FC(0.0, [0.8, 0.7, 3.9], [[G5[0][0], 3.05, G5[0][2]], [G5[3][0], 3.05, G5[3][2]], [G5[3][0], 0.0, G5[3][2]], [G5[1][0], 1.2, G5[1][2]]], top=0.1, bottom=0.8)])   # (review 1) further round: four silhouettes, not one mass   # low, down the line of guards in perspective
st.cue('clack', 'S05', SAL5, 0.35); st.cue('clack', 'S05', r(SAL5 + LATE5), 0.3); st.cue('sfx:boing', 'S05', r(SAL5 + LATE5 + 0.06), 0.15)

# 6: the street was closed. (pass 3) Low and close: the policeman in front of the barriers, an arm up, his cheeks ballooning on the whistle; the sign
#    RUE FERMÉE beside him; behind the barriers the jam, nose to tail, facing us: one car hops and squashes as it honks, then the next
D6 = st.dur('S06'); FL6 = [0.7, 0, 1.5]
WH6 = lambda t, puff, dx: k(t, toon={'reach': {'R': [r(FL6[0] + 0.5 + dx), 2.32, r(FL6[2] - 0.12), 1, 0.03]}, 'hands': {'R': 'open'}, 'scl': {'head': [1.2, 0.9, 1.14] if puff else [1.0, 1.0, 1.0]}, 'sq': [1.04, 0.95, 1.04] if puff else [0.98, 1.03, 0.98],
                                        'face': {'lid': 0.2, 'mouth': 'whistle', 'puff': 1.0 if puff else 0.2, 'brow': -0.5}}, toonDur=0.07)
HONK6 = lambda p_, t: [k(t, to=[p_[0], 0.2, p_[2]], dur=0.06, ease='out'), k(r(t + 0.06), to=p_, dur=0.08, ease='in'), k(r(t + 0.14), squash=[1.08, 0.82, 1.08], dur=0.3)]
CARS6 = [[-1.0, 0, 5.4], [1.3, 0, 5.9], [-1.0, 0, 9.3], [1.3, 0, 9.8], [-1.0, 0, 13.2], [1.3, 0, 13.7]]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[act('flic', FL6, 180, 'stand', 'neutral', keys=[k(0.0, look='camera'), WH6(0.0, False, 0.0), WH6(0.1, True, -0.12), WH6(0.3, True, 0.12), WH6(0.5, False, -0.12), WH6(0.7, False, 0.12),
            k(0.62, look=[CARS6[0][0], 1.2, CARS6[0][2]], lookDur=0.1), WH6(0.9, True, -0.12), WH6(1.1, True, 0.12), k(1.05, look='camera', lookDur=0.1), WH6(1.3, False, -0.12), WH6(1.48, False, 0.0)])],   # two blasts, a glance over his shoulder at the honk
        props=[*[P(f'barr6{j}', 'crowdBarrier', pos=[r(-3.0 + 2.0 * j), 0, 2.9], opts={'w': 1.9}) for j in range(4)],
               P('ferme6', 'signBoard', pos=[-0.78, 0, 2.5], ry=180, opts={'text': 'RUE FERMÉE', 'bg': '#C8322A', 'fg': '#FFFFFF', 'w': 1.15, 'h': 0.4, 'height': 1.05, 'posts': True}),
               *[P(f'voit6{j}', 'car', pos=CARS6[j], ry=90, opts={'color': ['#E2B53C', '#4A8C5A', '#C8322A', '#2F62B5', '#8A5AA8', '#D9734E'][j], 'glass': 0.8, 'glassColor': '#33404A'},
                   keys=(HONK6(CARS6[0], 0.6) if j == 0 else HONK6(CARS6[1], 1.12) if j == 1 else [])) for j in range(6)]],   # (pass 3) the cars face us (ry 180 laid them across the street)
        cams=[FC(0.0, [0.25, 0.95, -3.1], [[FL6[0], 2.5, FL6[2]], [FL6[0], 0.75, FL6[2]], [r(FL6[0] + 0.7), 2.4, FL6[2]], [-1.42, 1.5, 2.5]], top=0.12, bottom=0.78, lenses=range(26, 68))])   # a portrait frame is 2.5 m wide at him: the sign half behind him, the cars straight behind
st.cue('sfx:whistle', 'S06', 0.1, 0.25); st.cue('sfx:honkLong', 'S06', 0.6, 0.2); st.cue('sfx:whistle', 'S06', 0.9, 0.2); st.cue('sfx:honkLong', 'S06', 1.12, 0.18)

# 7: a brass band played. Three bandsmen in red; (pass 3) a trumpet at the mouth, a sousaphone whose bell rises over the head, a drum on the belly
#    with two sticks; all three pump on the beat (down, up), cheeks ballooning, the bells swelling, the sticks falling in turn
D7 = st.dur('S07'); BEATS7 = [r(0.12 + 0.24 * j) for j in range(int(D7 / 0.24))]
BAND = [('musi1', [3.0, 0, -0.6], 'trumpet'), ('musi2', [3.2, 0, 0.3], 'sousa'), ('musi3', [3.0, 0, 1.2], 'drum')]   # (pass 3) closer together and further from the house fronts: the camera backed into the wall
F7 = [0.985, 0.174]                                 # they face ry 80: forward (x, z); their right hand is toward +Z
def PLAY7(p_, kd, i):
    dn = i % 2 == 0
    if kd == 'trumpet': rc = {'R': [r(p_[0] + 0.34), 1.92, r(p_[2] + 0.13), 1, 0.03], 'L': [r(p_[0] + 0.3), 1.9, r(p_[2] - 0.02), 1, 0.03]}
    elif kd == 'sousa': rc = {'R': [r(p_[0] + 0.3), 1.42, r(p_[2] + 0.3), 1, 0.03], 'L': [r(p_[0] + 0.34), 1.3, r(p_[2] - 0.22), 1, 0.03]}
    else: rc = {'R': [r(p_[0] + 0.36), 1.36 if dn else 1.66, r(p_[2] + 0.2), 1, 0.03], 'L': [r(p_[0] + 0.36), 1.66 if dn else 1.36, r(p_[2] - 0.1), 1, 0.03]}   # the sticks fall in turn
    return {'reach': rc, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.09, 0.89, 1.09] if dn else [0.94, 1.1, 0.94],
            'scl': {'head': [1.16, 0.92, 1.12] if (dn and kd != 'drum') else [1.0, 1.0, 1.0]}, 'face': {'puff': (1.0 if dn else 0.5) if kd != 'drum' else 0.0, 'lid': 0.3, 'mouth': 'line' if kd == 'drum' else 'whistle'}}
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[*[act(n_, p_, 80, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=PLAY7(p_, kd, 1), toonDur=0.0),
            *[k(b_, toon=PLAY7(p_, kd, i), toonDur=0.07, toonEase='out') for i, b_ in enumerate(BEATS7)]]) for n_, p_, kd in BAND]],
        props=[P('instr70', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11]}, opts={'kind': 'trumpet', 'beat': BEATS7[::2], 's': 1.15}),
               P('instr71', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.3, 0.0]}, opts={'kind': 'sousa', 'beat': BEATS7[::2]}),
               P('instr72', 'bandInstr', on={'actor': 'musi3', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': BEATS7}),
               P('bag7R', 'bandInstr', on={'actor': 'musi3', 'hand': 'R', 'offset': [0.0, -0.06, 0.03], 'face': 'camera', 'faceRoll': 2.5}, opts={'kind': 'stick'}),
               P('bag7L', 'bandInstr', on={'actor': 'musi3', 'hand': 'L', 'offset': [0.0, -0.06, 0.03], 'face': 'camera', 'faceRoll': -2.5}, opts={'kind': 'stick'}),
               *[P(f'kepi7{j}', 'copCap', on={'actor': n_, 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}, opts={'color': '#B5302A'}) for j, (n_, p_, kd) in enumerate(BAND)]],
        cams=[FC(0.0, [5.9, 1.7, 0.35], [[3.0, 2.75, -0.6], [3.0, 2.75, 1.2], [3.2, 2.95, 0.3], [3.2, 0.9, 0.3], [3.0, 0.9, -0.85], [3.0, 0.9, 1.72]], top=0.08, bottom=0.8, lenses=range(26, 72))])   # (review 1) the drum inside the frame; (pass 3) the sousaphone's bell too
for b_ in BEATS7[::2]: st.cue('thud', 'S07', b_, 0.2)
st.cue('sfx:fanfare', 'S07', 0.05, 0.3)

# 8: helicopters flew over the neighbourhood. Low on the pavement looking up past the roofs: two helicopters sweep over, rotors blurring; he looks up;
#    (pass 3) their wash pulls at his tie and hair; his chest is clear of the caption band
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET, fx=[{'type': 'wind', 'at': 0.35, 'dur': 1.5, 'v': [-1.5, -2.0, 6.0]}], actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[9.0, 12.0, -4.0]), k(0.0, toon=LIP, toonDur=0.0), *BLINK(0.7, {'mouth': 'line'}),
            k(r(D8 * 0.6), look=[9.0, 12.0, 4.0], lookDur=0.4), *BLINK(1.9, {'mouth': 'line'})])],
        props=[P('heli8a', 'helicopter', pos=[8.6, 9.6, -9.0], ry=0, scale=1.5, keys=[k(0.0, to=[8.6, 9.2, 9.0], dur=D8, ease='linear')]),
               P('heli8b', 'helicopter', pos=[10.5, 11.0, -15.0], ry=0, scale=1.5, keys=[k(0.0, to=[10.5, 10.6, 5.0], dur=D8, ease='linear')])],   # (stills 1) lower and nearer: they were cut off at the top
        cams=[FC(0.0, [3.0, 0.6, 1.3], [[ME[0], 2.45, ME[2]], [ME[0], 1.15, ME[2]], [8.6, 10.2, 0.0], [10.5, 11.6, -4.0], [8.6, 8.8, 0.0], [7.6, 13.5, 0.0]], top=0.06, bottom=0.745, lenses=range(26, 80))])   # (pass 3) his waist above the caption band (his chest sat in it)
st.cue('engine', 'S08', 0.0, 0.3)

# 9: the cent arrived on a velvet cushion. (pass 3) A macro first: the copper cent standing on the red velvet, 1 CENT on its face, a star flashing
#    beside it; then the camera pulls back to the guard who carries it, gold helmet against the sky, and he walks it slowly toward us down the boulevard
D9 = st.dur('S09'); G9 = [3.0, 0, -1.6]; WALK9 = 1.05
CUSH9 = {'touch': {'R': ['torso', -0.12, 0.08, 0.32, 1, 0.02], 'L': ['torso', 0.12, 0.08, 0.32, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'hip': 0.0, 'face': {'lid': 0.35, 'mouth': 'line'}}   # hip 0: no idle weight shift (it slid the pelvis, and the cushion, 17 cm out of the macro)
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('garde3', G9, 0, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.0, toon=CUSH9, toonDur=0.0),
            k(WALK9, to=[3.0, 0, -0.6], dur=r(D9 - WALK9), clip='walk', ease='linear'), k(WALK9, clip='walk', speed=0.55), k(1.7, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07, keepPose=True), k(1.82, toon={'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.08, keepPose=True)])],
        props=[GUARD('casque9', 'garde3'), EPAU('epau9', 'garde3'), P('coussin9', 'velvetCushion', on={'actor': 'garde3', 'joint': 'torso', 'offset': [0.0, 0.12, 0.36]}, opts={'w': 0.36}),
               P('piece9', 'centCoin', on={'actor': 'garde3', 'joint': 'torso', 'offset': [0.0, 0.283, 0.36], 'rot': [-0.3, 0, 0]}, opts={'r': 0.055, 'glint': [0.2, 0.75, 1.9], 'glintAt': [0.095, 0.07]})],   # a coin of eleven centimetres: a cartoon cent
        cams=[FC(0.0, [3.3, 1.62, -0.2], [[2.78, 1.2, -1.24], [3.22, 1.2, -1.24], [3.0, 1.43, -1.24], [3.0, 1.1, -1.24]], top=0.3, bottom=0.68, lenses=range(16, 60)),
              glide([FC(WALK9, [3.95, 1.75, 2.6], [[3.0, 3.05, -0.8], [3.0, 1.2, -0.8], [2.6, 1.6, -0.8], [3.4, 1.6, -0.8]], top=0.12, bottom=0.78, drift=(0.0, 0.0, 0.2))], 0.5)])   # from the side of the road: the tower beside his helmet, not out of it
st.cue('sfx:choir', 'S09', 0.1, 0.25); st.cue('sfx:ding', 'S09', 0.2, 0.2); st.cue('sfx:ding', 'S09', 0.75, 0.15)

# 10: the minister gave a one-hour speech. (pass 3) Three-quarter front, from the road: the minister orates at a lectern with a tricolour panel, arms
#     going, and over his head a big street clock whose minute hand goes all the way round; behind his shoulder a guard nods off, a snore bubble
#     swelling at his nose, and jerks awake, his helmet over his eyes; in the foreground, facing us, the man: deadpan, one slow blink
D10 = st.dur('S10'); NOD10 = 1.1; LEC10 = [5.9, 0, 0.2]; MIN10 = [6.5, 0, 0.2]; GD10 = [7.05, 0, -0.6]; ME10 = [4.6, 0, 1.2]
def ORA10(j):
    up, dn = ('R', 'L') if j % 2 else ('L', 'R')
    return {'reach': {up: [r(MIN10[0] - 0.25), r(2.35 + 0.12 * (j % 3)), r(MIN10[2] + (-0.45 if up == 'R' else 0.45)), 1, 0.03], dn: [r(LEC10[0] + 0.1), 1.24, r(LEC10[2] + (-0.2 if dn == 'R' else 0.2)), 1, 0.03]},
            'hands': {up: 'point', dn: 'open'}, 'sq': [0.96, 1.06, 0.96] if j % 2 else [1.03, 0.97, 1.03], 'face': {'mouth': 'open' if j % 2 else 'O', 'lid': 0.2, 'brow': 0.7}}
SLEEP10 = {'bend': {'neck': [0.7, 0, 0, 1, None]}, 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 1.0, 'mouth': 'line'}}
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('ministre', MIN10, -90, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=ORA10(0), toonDur=0.0), *[k(r(0.12 + 0.26 * j), toon=ORA10(j + 1), toonDur=0.1, toonEase='out') for j in range(int(D10 / 0.26))]]),
        act('garde1', GD10, -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.9, GD10[2]]), k(0.0, toon={'face': {'lid': 0.6, 'mouth': 'line'}}, toonDur=0.0), k(0.12, toon=SLEEP10, toonDur=0.45, toonEase='inOut'),   # the head drops...
            k(NOD10, toon={'bend': {'neck': [-0.15, 0, 0, 1, None]}, 'sq': [0.88, 1.18, 0.88], 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...awake with a jerk
            k(r(NOD10 + 0.2), toon={'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.1, 'brow': 0.6, 'mouth': 'line'}}, toonDur=0.1), k(r(NOD10 + 0.36), toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.1),
            k(r(NOD10 + 0.5), look=[MIN10[0], 2.0, 3.0], lookDur=0.1), k(r(NOD10 + 0.8), look=[0.0, 1.9, GD10[2]], lookDur=0.1)]),   # a guilty glance at the minister
        act('mec', ME10, -90, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=LIP, toonDur=0.0), k(0.55, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.16, toonEase='inOut'), k(0.95, toon=LIP, toonDur=0.16, toonEase='inOut'),   # one slow blink
            k(r(NOD10 + 0.12), look=[4.6, 1.9, -4.0], lookDur=0.12), k(r(NOD10 + 0.55), look='camera', lookDur=0.14), *BLINK(2.0, {'mouth': 'line'})])],   # his eyes go to the pop behind him, and back to us
        props=[P('pupitre10', 'podium', pos=LEC10, ry=-90, opts={'text': 'RÉPUBLIQUE'}), *[P(f'tri10{j}', 'slab', pos=[r(LEC10[0] - 0.262), 0.3, r(LEC10[2] - 0.17 + 0.17 * j)], opts={'w': 0.012, 'h': 0.3, 'd': 0.17, 'color': TRI[j]}) for j in range(3)],
               COCK('ck10', 'ministre'), GUARD('casque10', 'garde1', knockAt=[r(NOD10 + 0.02)], knock=0.6, stay=0.5), EPAU('epau10', 'garde1'),
               P('bulle10', 'snoreBubble', on={'actor': 'garde1', 'joint': 'head', 'offset': [0.0, 0.2, 0.12]}, opts={'from': 0.3, 'popAt': NOD10, 'r': 0.13, 'period': 0.5}),
               P('horloge10', 'streetClock', pos=[7.3, 0, 0.2], ry=-90, opts={'r': 0.5, 'h': 3.35, 'from': 0.1, 'to': r(D10 - 0.1), 'turns': 1, 'hour': 3})],   # the hour passes: the minute hand goes once round
        cams=[FC(0.0, [1.9, 1.5, 0.55], [[ME10[0], 2.5, ME10[2]], [ME10[0], 1.15, ME10[2]], [ME10[0], 1.8, r(ME10[2] + 0.35)], [MIN10[0], 2.5, MIN10[2]], [LEC10[0], 0.7, LEC10[2]], [GD10[0], 3.1, GD10[2]], [GD10[0], 1.5, r(GD10[2] - 0.35)],
                             [7.3, 3.9, 0.2], [7.3, 3.35, -0.35]], top=0.1, bottom=0.78, lenses=range(26, 72))])
st.cue('sfx:ticks', 'S10', 0.1, 0.2); st.cue('sfx:boing', 'S10', NOD10, 0.15)

# 11: the neighbours wept. Up the facade, the neighbours at their windows, handkerchiefs out, tears spurting in arcs
D11 = st.dur('S11')
NB11 = [('voisin1', [9.8, 3.25, -1.6], 'mamie'), ('voisin2', [9.8, 3.25, 1.8], 'madame'), ('voisin3', [9.8, 6.3, 0.1], 'boss')]   # (stills 1) on the balconies (in front of the facade they floated); (pass 3) the house fronts are at x 10.2: the balconies hung three metres out from them
HANKY = {'touch': {'R': ['face', -0.14, 0.6, 0.12, 1, 0.02]}, 'hands': {'R': 'pinch'}}
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[*[act(n_, p_, -90, 'stand', 'sad', keys=[k(0.0, look=[4.4, 1.0, 0.3]), k(0.0, toon={**HANKY, 'face': {'lid': 0.7, 'mouth': 'cry', 'brow': 1.0}}, toonDur=0.0),
            *[k(r(0.12 + 0.22 * i + 0.07 * j), toon={**HANKY, 'sq': [1.04, 0.95, 1.04] if i % 2 else [0.98, 1.03, 0.98], 'face': {'lid': 0.75, 'mouth': 'cry', 'brow': 1.0}}, toonDur=0.08) for i in range(int(D11 / 0.22))]]) for j, (n_, p_, _) in enumerate(NB11)]],   # (review 1) the handkerchief held at the eye on every sob
        props=[*[P(f'larmes11{j}', 'tearFountain', on={'actor': n_, 'joint': 'head'}, opts={'at': r(0.05 + 0.1 * j), 'r': 0.036, 'speed': 1.8, 'rate': 10}) for j, (n_, p_, _) in enumerate(NB11)],   # (review 1) tears twice as big
               *[P(f'mouch11{j}', 'slab', on={'actor': n_, 'hand': 'R', 'offset': [0.0, -0.06, 0.03], 'face': 'camera'}, opts={'w': 0.27, 'h': 0.27, 'd': 0.006, 'color': '#FFFFFF', 'outline': 0.006}) for j, (n_, p_, _) in enumerate(NB11)],   # a white handkerchief; (pass 3) nearly twice the size
               *[P(f'balc11{j}', 'balcony', pos=[9.77, p_[1], p_[2]], ry=-90, opts={'w': 1.3, 'd': 0.85, 'rail': 'front'}) for j, (n_, p_, _) in enumerate(NB11)]],   # (review 1) a stone balcony with an iron rail under each (black slabs read as voids)
        cams=[FC(0.0, [5.6, 2.2, 2.6], [[9.8, 5.75, -1.6], [9.8, 5.75, 1.8], [9.8, 8.8, 0.1], [9.8, 3.4, -1.6], [9.8, 3.4, 1.8]], top=0.12, bottom=0.8, lenses=range(26, 64))])
st.cue('sfx:gasp', 'S11', 0.1, 0.15)

# 12: television filmed it live. (pass 3) The reporter faces us, a microphone with a red ball at her chin, her free hand going; beside her a pale grey
#     camera on its tripod, in profile, its lens on her and its red light blinking; EN DIRECT on a red board over it; behind the barriers, small, the
#     man on his doorstep, facing the cameras, deadpan
D12 = st.dur('S12'); REP12 = [3.98, 0, 1.35]; ME12 = [6.3, 0, -1.87]; NC12 = [4.28, 0, 2.37]; MIC12 = [3.688, 1.95, 1.407]
TALK12 = lambda j: {'reach': {'R': [*MIC12, 1, 0.03], 'L': [r(3.875 + (0.1 if j % 2 else -0.06)), r(1.5 + (0.3 if j % 2 else 0.0)), r(1.761 + (0.05 if j % 2 else 0.0)), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'},
                    'sq': [1.03, 0.97, 1.03] if j % 2 else [0.98, 1.03, 0.98], 'face': {'mouth': 'open' if j % 2 else 'O', 'lid': 0.1, 'brow': 0.8}}
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        act('reporter', REP12, -59, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=TALK12(0), toonDur=0.0), *[k(r(0.1 + 0.22 * j), toon=TALK12(j + 1), toonDur=0.09, toonEase='out') for j in range(int(D12 / 0.22))],
            k(1.0, look=[ME12[0], 1.9, ME12[2]], lookDur=0.12), k(1.3, look='camera', lookDur=0.12)]),   # a glance back at him, and to us
        act('mec', ME12, -46, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=LIP, toonDur=0.0), *BLINK(0.8, {'mouth': 'line'}), *BLINK(1.5, {'mouth': 'line'})])],
        props=[P('cam12', 'newsCam', pos=NC12, ry=-164, opts={'h': 1.3}),
               P('direct12', 'signBoard', pos=[5.75, 3.0, 1.3], face='camera', opts={'text': 'EN DIRECT', 'bg': '#C8322A', 'fg': '#FFFFFF', 'w': 1.15, 'h': 0.34, 'posts': False, 'height': 0}),
               P('micro12', 'handMic', on={'actor': 'reporter', 'hand': 'R', 'offset': [0.0, -0.02, 0.03], 'face': 'camera'}, opts={'s': 1.3}),
               *[P(f'barr12{j}', 'crowdBarrier', pos=p_, ry=-57, opts={'w': 1.9}) for j, p_ in enumerate([[4.765, 0, -0.756], [5.791, 0, 0.84]])]],
        cams=[FC(0.0, [1.6, 1.45, 3.0], [[REP12[0], 2.5, REP12[2]], [REP12[0], 0.9, REP12[2]], [3.6, 1.8, 1.1], [NC12[0], 1.75, NC12[2]], [4.45, 1.2, 2.6], [ME12[0], 2.5, ME12[2]], [5.75, 3.45, 1.3], [6.25, 3.2, 1.6]], top=0.1, bottom=0.78, lenses=range(26, 72))])
st.cue('sfx:shutter', 'S12', 0.3, 0.15); st.cue('sfx:shutter', 'S12', 0.9, 0.15)

# 13: he put the cent in his piggy bank. His kitchen table, close: his fingers hold the cent over the pink pig; (pass 3) a dark copper cent with a
#     light rim, hanging clear under his fingertips; a small dip, he lets go and lifts his hand away; it drops into the slot (clink) and the pig
#     jiggles; a look at us
D13 = st.dur('S13'); DROP13 = 0.65; PIG = [0.15, 0.76, -1.3]
PIN13 = lambda y, h='pinch', z=-1.31: {'reach': {'R': [0.16, y, z, 1, 0.03]}, 'hands': {'R': h}, **LIP}
st.shot('S13', 'kitchenDay', actors=[act('mec', [0.15, 0, -1.95], 0, 'stand', 'neutral', keys=[k(0.0, look=PIG), k(0.0, toon=PIN13(1.235), toonDur=0.0),
            k(0.2, toon=PIN13(1.222), toonDur=0.12, toonEase='inOut'), k(0.38, toon=PIN13(1.24), toonDur=0.12, toonEase='inOut'),   # a small dip: he lines it up with the slot
            k(r(DROP13 - 0.08), toon=PIN13(1.44, 'open', -1.4), toonDur=0.1, toonEase='out'), k(r(DROP13 + 0.45), look='camera'), *BLINK(r(DROP13 + 0.8), {'mouth': 'line'}), *BLINK(1.95, {'mouth': 'line'})])],
        props=[P('table13', 'table', pos=[0.15, 0, -1.3], opts={'w': 1.0, 'd': 0.7, 'h': 0.76}),
               P('cochon13', 'piggyBank', pos=PIG, ry=20, opts={'s': 1.25, 'dropAt': [DROP13], 'jig': 3.0, 'coin': {'r': 0.032, 'color': '#A85A2C', 'rim': '#E3A070', 'pre': 0.64, 'hover': 0.35, 'ry': 0.9}})],   # (review 1) a jiggle three times bigger
        cams=[FC(0.0, [0.42, 1.12, -0.82], [[0.18, 1.3, -1.3], [PIG[0], 0.78, PIG[2]], [r(PIG[0] - 0.2), 0.95, PIG[2]], [r(PIG[0] + 0.2), 0.95, PIG[2]]], top=0.18, bottom=0.72, lenses=range(20, 60)),   # (review 1) a macro: fingers, cent, slot
              FC(r(DROP13 + 0.42), [0.7, 1.5, 0.3], [[0.15, 2.45, -1.95], [PIG[0], 0.75, PIG[2]], [r(PIG[0] - 0.3), 1.0, PIG[2]], [r(PIG[0] + 0.3), 1.0, PIG[2]]], top=0.12, bottom=0.78)])   # then him and the pig at us
st.cue('sfx:clink', 'S13', r(DROP13 + 0.2), 0.35)

# 14: the next day he got a bill. (pass 3) His kitchen, the front door behind him: the brass flap of its letter slot swings in and a fat envelope
#     shoots through, lands and slides to his feet (swish); his head turns to it, then he bends like a plank, picks it up and tears it open: a strip
#     of paper drops out of it
D14 = st.dur('S14'); IN14 = 0.2; H14 = [1.2, 0, -1.75]; DOOR14 = [2.8, 0, -3.55]; E14 = [1.05, 0.012, -1.2]; TEAR14 = 1.5; BILL14 = 1.72
HOLD14 = lambda dx=0.0, f=None: {'reach': {'R': [r(1.1 - dx), 1.6, -1.38, 1, 0.03], 'L': [r(1.3 + dx), 1.6, -1.38, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **(f or LIP)}
BILLO = {'w': 0.5, 'top': 1.55, 'max': 4.4, 'totalAt': 0.95, 'totalLen': 0.85, 'oneLine': True}   # (stills 1) the rows on one line each, the total 0.95 m down the strip
st.shot('S14', 'kitchenDay', actors=[act('mec', H14, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=LIP, toonDur=0.0), k(r(IN14 + 0.05), look=[2.6, 0.9, -3.4], lookDur=0.1), k(0.5, look=E14, lookDur=0.15),
            k(0.7, toon={'bend': {'spine': [0.6, 0, 0, 1, None]}, 'reach': {'R': [r(E14[0] - 0.02), 0.12, r(E14[2] - 0.03), 1, 0.03]}, 'hands': {'R': 'pinch'}, **LIP}, toonDur=0.2, toonEase='inOut'),
            k(1.15, toon=HOLD14(), toonDur=0.2, toonEase='inOut'), k(1.38, look=[1.2, 1.6, -1.38]),
            k(r(TEAR14 - 0.1), toon=HOLD14(-0.03, {'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.4}}), toonDur=0.08), k(TEAR14, toon=HOLD14(0.16, {'face': {'lid': 0.2, 'mouth': 'line'}}), toonDur=0.06, toonEase='out'),   # he tears it open: the hands jerk apart
            k(r(TEAR14 + 0.16), toon=HOLD14(0.05), toonDur=0.1), k(r(BILL14 + 0.15), look=[1.2, 0.3, -1.0], lookDur=0.25), *BLINK(2.2, {'mouth': 'line'})])],   # his eyes follow the paper down
        props=[P('porte14', 'mailDoor', pos=DOOR14, opts={'flapAt': IN14}),
               P('lettre14', 'envelope', pos=[2.8, 0.95, -3.5], rot=[-PI / 2, 0, 0.2], scale=2.0, keys=[k(0.0, visible=False), k(IN14, visible=True), k(IN14, to=[2.3, 0.012, -2.7], dur=0.14, ease='in'), k(r(IN14 + 0.14), to=E14, dur=0.22, ease='out'),
                   k(0.9, attach='mec', hand='R', offset=[0.0, -0.06, 0.03]), k(TEAR14, squash=[1.25, 0.8, 1.0], dur=0.25), k(r(BILL14 + 0.1), visible=False)]),
               P('facture14', 'expenseBill', pos=[1.2, 1.55, -1.37], opts={**BILLO, 'len': [[BILL14, 0.03], [D14, 1.3]]}, keys=[k(0.0, visible=False), k(BILL14, visible=True)])],
        cams=[FC(0.0, [1.0, 1.3, 1.5], [[H14[0], 2.5, H14[2]], [0.55, 1.2, H14[2]], [E14[0], 0.0, E14[2]], [DOOR14[0], 2.5, DOOR14[2]], [3.3, 1.0, DOOR14[2]], [DOOR14[0], 0.95, DOOR14[2]]], top=0.12, bottom=0.74)])   # him in the middle, the door behind his shoulder
st.cue('clack', 'S14', IN14, 0.2); st.cue('sfx:paper', 'S14', r(IN14 + 0.1), 0.25); st.cue('sfx:zip', 'S14', TEAR14, 0.2); st.cue('sfx:slideDown', 'S14', BILL14, 0.2)

# 15: two million euros. (pass 3) The bill runs out of his hands to the floor and on across it toward us, past the lens, its roll hopping; in the
#     middle of the floor, as wide as the paper, a red block: TOTAL 2 000 000 €; his eyes follow the roll, come up to us, snap back down to the
#     total, out on stalks (a closer camera for the take), then up to us
D15 = st.dur('S15'); HP15 = [0.95, 0, -1.75]; BP15 = [0.95, 1.55, -1.37]; TILT15 = 1.03   # HP15: a quarter of a metre nearer the pig's table than in S14 (the end hold frames him and the pig: the nearer they are, the larger the sheet)
# (stills 1) the strip shoots out at 59 degrees from the vertical: its total faces the lens (flat on the floor it was a red dash)
BLK15 = lambda s_: [BP15[0], r(BP15[1] - s_ * math.cos(TILT15)), r(BP15[2] + s_ * math.sin(TILT15))]   # the point s_ metres down the strip
H15 = {'reach': {'R': [r(BP15[0] - 0.1), 1.55, -1.4, 1, 0.03], 'L': [r(BP15[0] + 0.1), 1.55, -1.4, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}
st.shot('S15', 'kitchenDay', actors=[act('mec', HP15, 0, 'stand', 'neutral', keys=[k(0.0, look=[BP15[0], 0.3, -1.0]), k(0.0, toon=H15, toonDur=0.0),
            *doubleTake(0.26, BLK15(1.4), keep=H15, back='camera', pop=0.85, blank=0.2, hold=0.42), k(1.12, look='camera', lookDur=0.12)])],
        props=[P('facture15', 'expenseBill', pos=BP15, opts={**BILLO, 'len': [[0.0, 1.3], [0.5, 4.4]], 'tilt': [[0.0, 0.0], [0.22, TILT15]]})],
        cams=[FC(0.0, [1.3, 1.25, 2.3], [[HP15[0], 2.5, HP15[2]], [r(BP15[0] - 0.27), BLK15(1.8)[1], BLK15(1.8)[2]], [r(BP15[0] + 0.27), BLK15(1.8)[1], BLK15(1.8)[2]], [r(HP15[0] - 0.35), 1.4, HP15[2]], [r(HP15[0] + 0.35), 1.4, HP15[2]]], top=0.2, bottom=0.74, lenses=range(26, 70)),   # the total above the captions, his head below the card
              FC(0.8, [1.2, 1.8, 0.1], [[HP15[0], 2.5, HP15[2]], [HP15[0], 1.42, -1.4], [r(HP15[0] - 0.35), 1.9, HP15[2]], [r(HP15[0] + 0.35), 1.9, HP15[2]]], top=0.22, bottom=0.72)])   # closer: the eyes out on stalks, the top of the bill in his hands
st.cue('sfx:paper', 'S15', 0.02, 0.2); st.cue('sfx:slideDown', 'S15', 0.05, 0.25); st.cue('sfx:boing', 'S15', 0.64, 0.12)

# 16: travel expenses. (pass 3) Close on the sheet he holds by its side edges, his hands out of the words: FRAIS DE DÉPLACEMENT, clear for the whole
#     insert; then up to him: his eyes come to us, a breath, one slow blink in the middle of the hold; beside him on the table, the pink pig
D16 = st.dur('S16'); SH16 = [HP15[0], 1.32, -1.3]; SW16 = 0.62
H16 = lambda sq=None, f=None: {'reach': {'R': [r(SH16[0] - SW16 / 2 - 0.025), 1.32, -1.36, 1, 0.03], 'L': [r(SH16[0] + SW16 / 2 + 0.025), 1.32, -1.36, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, **({'sq': sq} if sq else {}), 'face': f or DEAD | {'mouth': 'line'}}
st.shot('S16', 'kitchenDay', actors=[act('mec', HP15, 0, 'stand', 'neutral', keys=[k(0.0, look=SH16), k(0.0, toon=H16(), toonDur=0.0), k(0.98, look='camera', lookDur=0.14),
            k(1.1, toon=H16([0.99, 1.035, 0.99]), toonDur=0.25, toonEase='inOut'),                                                    # a breath in...
            k(1.36, toon=H16([0.99, 1.035, 0.99], {'lid': 1.0, 'mouth': 'line'}), toonDur=0.14, toonEase='inOut'),                    # ...the slow blink...
            k(1.62, toon=H16([1.0, 1.0, 1.0]), toonDur=0.2, toonEase='inOut')])],                                                      # ...and out
        props=[P('frais16', 'paperSheet', pos=SH16, face='camera', opts={'w': SW16, 'h': 0.27, 'head': 'FRAIS DE', 'big': 'DÉPLACEMENT', 'bright': True}),   # (pass 3) a free sheet turned to the lens, in front of both hands (in his hand, his palms covered the words)
               P('table16', 'table', pos=[0.15, 0, -1.3], opts={'w': 1.0, 'd': 0.7, 'h': 0.76}), P('cochon16', 'piggyBank', pos=PIG, ry=20, opts={'s': 1.25})],
        cams=[FC(0.0, [SH16[0], 1.38, -0.3], [[SH16[0], 1.48, SH16[2]], [SH16[0], 1.16, SH16[2]], [r(SH16[0] - 0.38), 1.32, SH16[2]], [r(SH16[0] + 0.38), 1.32, SH16[2]]], top=0.25, bottom=0.66),   # the two lines, as wide as the frame
              glide([FC(0.6, [0.25, 1.45, 0.45], [[HP15[0], 2.5, HP15[2]], [HP15[0], 1.1, HP15[2]], [PIG[0], 0.85, PIG[2]], [r(PIG[0] - 0.22), 1.0, PIG[2]], [r(SH16[0] + 0.44), 1.32, r(SH16[2] + 0.14)]], top=0.12, bottom=0.78, lenses=range(26, 68))], 0.35)])   # ...then up to his face, the pig beside him

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le centime", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}},   # (pass 3) he breathes in the holds
    'agent': {'preset': 'officiel', 'seed': 771, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'agent2': {'preset': 'avocat', 'seed': 772, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef': {'preset': 'boss', 'seed': 773, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'off1': {'preset': 'politique', 'seed': 774, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off2': {'preset': 'avocat', 'seed': 775, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'off3': {'preset': 'officiel', 'seed': 776, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 777, 'suit': '#34405A', 'lapel': '#34405A', 'tie': '#2F62B5', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'garde{j + 1}': {'preset': 'boss', 'seed': 778 + j, 'suit': '#1E2A52', 'lapel': '#1E2A52', 'tie': '#1E2A52', 'shirt': '#1E2A52', 'gloves': '#FFFFFF', 'pants': '#F2F2EE', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},
    'flic': {'preset': 'cop', 'seed': 782, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'musi{j + 1}': {'preset': 'serveur', 'seed': 783 + j, 'suit': '#B5302A', 'pants': '#1C1F2A', 'build': {'width': 1.0 + 0.1 * (j == 1), 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    'voisin1': {'preset': 'mamie', 'seed': 786, 'build': {'width': 1.0, 'headWidth': 1.25}, 'toon': EX},
    'voisin2': {'preset': 'madame', 'seed': 787, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'voisin3': {'preset': 'boss', 'seed': 788, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'reporter': {'preset': 'journaliste', 'seed': 789, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
