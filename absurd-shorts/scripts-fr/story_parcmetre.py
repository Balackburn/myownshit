#!/usr/bin/env python3
"""Le parcmètre (story 75, cycle 37; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man paid for his parking for four hundred years. He pressed the wrong button. The ticket is three kilometres long. The town hall refuses to
refund him. So he stays parked. He lives in his car. He got married on his bay. His children grew up between two white lines. The postman slips his
mail under the wiper. Every year the mayor opens his bay. Tourists photograph it. Yesterday a delivery van parked beside him. Double-parked. He can't
get out. The delivery man paid for five hundred years. They play cards on Sundays.
Staging: a big pay-and-display machine on the pavement beside his red car; he presses the red 400 ANS button next to the green 1 H without looking;
the screen rolls up from one hour to four hundred years; the ticket gushes out of the slot and runs down the pavement to the vanishing point; at the
town hall the paper roll is taller than the clerk, who stamps REFUSÉ; he sits in his car, arms crossed; the car becomes a house (gingham curtains, a
smoking stove pipe, a geranium, an aerial, a BIENVENUE mat, washing hung to the machine); a wedding through the car window; children on a chalk
hopscotch between the lines, heights pencilled on the machine; the postman tucks a letter under the wiper; the mayor cuts a ribbon across the bay
under confetti; a tourist's selfie with him waving behind the windscreen; a delivery van brakes alongside, hazard lights on, cars stuck behind it;
his face squashed flat against his window; the delivery man presses 500 ANS on purpose; a card game on a tray across the gap between the windows.
Natural look; cycle 37: props_parcmetre.js (horodateur, ticketRibbon, carHome, deliveryVan, clothesline, hopscotch, paperRoll, cardTray)."""
from story_kit import *
import math

st = Story('parcmetre', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 3), ('S06', 'L04', 0), ('S07', 'L05', 0),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L08', 5), ('S12', 'L09', 0), ('S13', 'L09', 5), ('S14', 'L10', 0),
         ('S15', 'L10', 4), ('S16', 'L11', 0), ('S17', 'L12', 0), ('S18', 'L12', 5), ('S19', 'L13', 0), ('S20', 'L14', 0), ('S21', 'L15', 0),
         ('S22', 'L15', 5), ('S23', 'L16', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
DEAD = {'lid': 0.45}
STREET = {'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}

# The car: parked along the right-hand kerb (x = 5), facing -Z; the car prop faces +X, so ry 90 and car-local (x, y, z) -> world (CX + z, y, CZ - x)
CAR = [3.85, 0, 0.0]
def cw(lx, ly, lz): return [r(CAR[0] + lz), ly, r(CAR[2] - lx)]
SEAT, SEAT2 = cw(0.05, 0.12, -0.4), cw(0.05, 0.12, 0.4)   # driver (road side), passenger (kerb side)
CARP = lambda pid, **kw: P(pid, 'car', pos=CAR, ry=90, opts={'color': '#C9473A', 'plate': 'AB-400-AN', **kw})
BAY = lambda pid, num='12': P(pid, 'parkingBay', pos=[CAR[0], 0, -0.4], ry=90, opts={'w': 2.4, 'l': 6.0, 'num': num})
HOME = lambda pid, **kw: P(pid, 'carHome', pos=CAR, ry=90, opts={'matRot': PI, **kw})   # (pass 3) matRot: BIENVENUE reads from the road side (review 2: upside down)
# The machine: on the pavement behind the car, facing the buildings (+X); prop front +Z, so ry 90 and local (x, y, z) -> world (MX + z, y, MZ - x)
METER = [5.6, 0, 2.9]
def mw(lx, ly, lz): return [r(METER[0] + lz), ly, r(METER[2] - lx)]
RED, GREEN, SLOT, SCREEN, CARD = mw(0.09, 1.06, 0.22), mw(-0.09, 1.06, 0.22), mw(0.0, 0.64, 0.2), mw(0.0, 1.25, 0.18), mw(0.12, 0.8, 0.19)
MTR = lambda pid, **kw: P(pid, 'horodateur', pos=METER, ry=90, opts={'labels': ['1 H', '400 ANS'], **kw})
RIBP = [[0.0, 0.6], [0.6, 0.72], [1.6, 0.75], [220.0, 0.8]]   # the ticket's run: out of the slot onto the pavement, then down it toward -Z
RIB = lambda pid, **kw: P(pid, 'ticketRibbon', pos=SLOT, ry=90, opts={'path': RIBP, 'text': '400 ANS', **kw})
MP = [6.35, 0, 3.35]   # where he stands to pay
VAN = [1.6, 0, 1.15]   # the van double-parked alongside: its cab level with his driver's seat (van-local (x, y, z) -> world (VX + z, y, VZ - x))
def vw(lx, ly, lz, v=VAN): return [r(v[0] + lz), ly, r(v[2] - lx)]
VSEAT, VSEAT2 = vw(1.15, 0.5, -0.45), vw(1.15, 0.5, 0.45)
VANP = lambda pid, pos=VAN, keys=None, **kw: P(pid, 'deliveryVan', pos=pos, ry=90, opts=kw, **({'keys': keys} if keys else {}))   # (stills 1) keys passed in opts: the van never moved
REACH = lambda hand, pt, pose='point', w=1: {'reach': {hand: [pt[0], pt[1], pt[2], w, 0.04]}, 'hands': {hand: pose}}
def LIFE(t0, t1, face, amp=0.022, per=0.42, blink=None):
    """(final pass) a hold that lives: the chest breathes in and out every `per` s from t0 to t1 and the eyes blink once (at `blink`), on top of the
    pose held (keepPose keeps its reach, touch, hands and bends); `face` is the face held (review 3: six holds read as freezes)"""
    ks, t, i = [], t0, 0
    while t < t1 - 0.08:
        sq_ = [r(1 - amp * 0.4), r(1 + amp), r(1 - amp * 0.4)] if i % 2 == 0 else [1.0, 1.0, 1.0]
        ks.append(k(r(t), toon={'sq': sq_, 'face': face}, toonDur=r(per * 0.9), toonEase='inOut', keepPose=True)); t += per; i += 1
    if blink is not None:
        ks += [k(r(blink), toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(blink + 0.1), toon={'face': face}, toonDur=0.07, keepPose=True)]
    return ks
CROSS = {'touch': {'R': ['torso', 0.13, 0.45, 0.2, 1, 0.02], 'L': ['torso', -0.13, 0.42, 0.21, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}   # arms folded

for g_ in [('S02', 0.86, 'mec', 'screen'), ('S04', 0.3, 'mec', 'ticket'), ('S08', 0.5, 'mec', 'home'), ('S15', 0.3, 'mec', 'snip'), ('S20', 0.3, 'mec', 'squash'), ('S23', 0.5, 'mec', 'end')]:
    st.gag(*g_)
st.card('S06', 'REFUSÉ', at=0.95)
st.card('S19', 'DOUBLE FILE', at=0.35)

# 1: the hook. (pass 3) He stands beside the machine, three-quarters to us, from the sunny side of the pavement with his car behind (review 2: a
#    blank profile and a black suit against the sun): a coin in, then he looks at us, deadpan, and his far hand finds the red 400 ANS button
#    without a look
D1 = st.dur('S01'); P1 = [6.05, 0, 2.3]; FACE1 = 12; PRESS = [RED[0], r(RED[1] - 0.025), r(RED[2] - 0.04)]
PR = lambda out=0.0, up=0.0: REACH('R', [r(PRESS[0] + 0.6 * out), r(PRESS[1] + 0.15 * out + up), r(PRESS[2] - 0.75 * out)])   # his finger on the red button, or `out` metres back toward his shoulder
FILL = lambda pid, pos=(6.75, 1.35, 3.0), kk=3.5: P(pid, 'glowLight', pos=list(pos), opts={'color': '#FFE7C2', 'k': kk, 'dist': 3.0, 'at': -1})   # a warm bounce on the machine's shaded front
CAM1 = lambda who=P1, hd=2.1: FC(0.0, [7.45, 1.45, 4.2], [[who[0], hd, who[2]], [who[0], 0.45, who[2]], [METER[0], 2.12, METER[2]], [METER[0], 0.45, METER[2]], [SCREEN[0], SCREEN[1], r(SCREEN[2] + 0.25)]], top=0.12, bottom=0.8, drift=(-0.1, 0.0, -0.1))
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', P1, FACE1, 'stand', 'neutral', keys=[k(0.0, look=CARD), k(0.0, toon={**REACH('R', CARD, 'pinch'), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.2, look='camera', lookDur=0.14), k(0.28, toon={**PR(0.1, 0.02), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2, toonEase='inOut'),
            k(0.58, toon={**PR(0.0), 'sq': [1.02, 0.97, 1.02], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.05, toonEase='in'),   # the press, a little weight into it
            k(0.72, toon={**PR(0.0), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12),
            k(0.9, toon={**PR(0.0), 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06), k(1.0, toon={**PR(0.0), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08)])],
        props=[MTR('pm1', pressAt=[0.62], litAfter=0.62, screens=[[0.62, '1 H']]), CARP('car1'), BAY('bay1'), FILL('fill1'),
               P('piece1', 'coin', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=0.8, keys=[k(0.26, visible=False)])],
        cams=[CAM1()])
st.cue('sfx:kaching', 'S01', 0.26, 0.2); st.cue('sfx:beep', 'S01', 0.62, 0.25)

# 2: ...his parking for four hundred years. (pass 3) Two set-ups (review 2: his head and sleeve covered the number while the narrator said it). Face
#    on to the machine, the screen big: it rolls up faster and faster and slams on 400 ANS on « quatre », his finger flinching on the button, the
#    number in the clear. Then the frame of 1, closer: the number still there, and beside it his take, three-quarters to us; his eyes come to us
D2 = st.dur('S02'); SLAM2 = 0.72; CUT2 = 1.05; LK2 = [6.1, 1.35, 3.3]   # LK2: between the screen and us (his head three-quarters to the lens, his eyes on the screen)
ROLL = [[0.0, '1 H'], [0.2, '1 JOUR'], [0.36, '1 MOIS'], [0.48, '1 AN'], [0.57, '10 ANS'], [0.64, '100 ANS'], [SLAM2, '400 ANS']]
WIDE2 = {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0, 'gx': -0.9}
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', P1, FACE1, 'stand', 'neutral', keys=[k(0.0, look=LK2),
            k(0.0, toon={**PR(0.0), 'face': {**DEAD, 'mouth': 'line', 'gx': -0.9}}, toonDur=0.0),
            k(SLAM2, toon={**PR(0.03, 0.012), 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'line', 'gx': -0.9}}, toonDur=0.04, toonEase='out'),   # the finger flinches on the button
            k(r(SLAM2 + 0.1), toon={**PR(0.0), 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'line', 'gx': -0.9}}, toonDur=0.1),
            k(r(CUT2 + 0.03), toon={**PR(0.0), 'sq': [0.94, 1.09, 0.94], 'hairUp': 0.9, 'face': WIDE2}, toonDur=0.05, toonEase='out'),   # the take, on the cut to his face
            k(r(CUT2 + 0.25), toon={**PR(0.0), 'hairUp': 0.3, 'face': WIDE2}, toonDur=0.15),
            k(1.45, look='camera', lookDur=0.14), k(1.45, toon={**PR(0.0), 'sq': [1.02, 0.96, 1.02], 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.15),   # ...and his eyes come to us
            k(1.66, toon={**PR(0.0), 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.05), k(1.74, toon={**PR(0.0), 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.05)])],
        props=[MTR('pm2', litAfter=0.0, screens=ROLL), FILL('fill2', (6.6, 1.4, 3.0), 3.2)],
        cams=[FC(0.0, [6.95, 1.5, 2.96], [[SCREEN[0], 1.36, 2.7], [SCREEN[0], 1.36, 3.1], [RED[0], 1.0, 2.72], [GREEN[0], 1.0, 3.08]], top=0.3, bottom=0.66, lenses=range(14, 60), drift=(-0.1, 0.0, 0.0)),
              FC(CUT2, [7.3, 1.55, 4.0], [[SCREEN[0], 1.38, 2.72], [SCREEN[0], 1.1, 3.08], [P1[0], 2.08, P1[2]], [r(P1[0] + 0.2), 1.3, P1[2]]], top=0.18, bottom=0.74, drift=(-0.05, 0.0, -0.05))])
for t_ in [0.2, 0.36, 0.48, 0.57, 0.64]: st.cue('sfx:tick', 'S02', t_, 0.15)
st.cue('sfx:ding', 'S02', SLAM2, 0.4)

# 3: he pressed the wrong button. Close on the two big buttons, face on: his finger still on the lit red 400 ANS beside the green 1 H. (pass 3) It
#    peels off slowly, hangs, jerks away, and by 0.6 s the two labels are in the clear to the cut (review 2: the hand hid them until the last 0.2 s)
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', P1, FACE1, 'stand', 'neutral', keys=[k(0.0, look=RED), k(0.0, toon=PR(0.0), toonDur=0.0),
            k(0.1, toon=PR(0.035, 0.004), toonDur=0.3, toonEase='inOut'),   # off the button, slowly...
            k(0.42, toon=PR(0.042, 0.014), toonDur=0.03), k(0.47, toon=PR(0.04, 0.002), toonDur=0.03), k(0.52, toon=PR(0.045, 0.012), toonDur=0.03),   # ...it hangs, trembling...
            k(0.55, toon=PR(0.7, 0.1), toonDur=0.07, toonEase='in')])],   # ...and jerks away, out of the frame
        props=[MTR('pm3', litAfter=0.0, screens=[[0.0, '400 ANS']]), FILL('rebond3', (6.3, 1.2, 3.2), 3.5)],
        cams=[FC(0.0, [6.55, 0.98, 3.05], [[RED[0], 1.15, RED[2] - 0.1], [GREEN[0], 1.15, GREEN[2] + 0.1], [RED[0], 0.97, RED[2] - 0.1], [GREEN[0], 0.97, GREEN[2] + 0.1], [r(RED[0] + 0.1), 1.06, r(RED[2] - 0.12)]], top=0.34, bottom=0.62, lenses=range(14, 60), drift=(-0.12, 0.02, -0.03))])

st.cue('sfx:sting', 'S03', 0.3, 0.2)

# 4: the ticket... Low on the pavement, the lens dropped onto the ticket's path (review 3: the ribbon a strip by the machine, the lower 40 % bare
#    pavement): it gulps out of the slot in four spurts, the machine kicking back at each, a ribbon wider than the man, and comes straight down
#    the pavement at us, filling the lower half by 0.15 s and gone under the lens by 0.45 s; beside the machine his eyes follow its head to us and
#    pop, with a stretch up
D4 = st.dur('S04'); RIBZ4 = [[-0.1, 0.62], [-0.3, 0.72], [-0.6, 0.75], [-220.0, 0.75]]   # the ticket's run turned toward +Z, down the pavement under the lens
SPIT4 = [0.0, 0.18, 0.36, 0.54]   # the machine's kicks, and the paper's spurts with them
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[act('mec', P1, FACE1, 'stand', 'neutral', keys=[k(0.0, look=SLOT), k(0.1, look=[6.55, 0.2, 4.0], lookDur=0.12), k(0.26, look='camera', lookDur=0.08),
            k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.0),
            k(0.22, toon={'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, 'sq': [1.05, 0.93, 1.05]}, toonDur=0.05, toonEase='out'),   # the anticipation
            k(0.3, toon={'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.24, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.9, 1.13, 0.9], 'hairUp': 1.0}, toonDur=0.05, toonEase='out'),   # the take: eyes out on stalks, a stretch up
            k(0.5, toon={'face': {'lid': 0.0, 'pop': 0.9, 'popLen': 0.22, 'mouth': 'O', 'brow': 1.0, 'pupilShake': 1.0}, 'sq': [0.95, 1.06, 0.95], 'hairUp': 0.8}, toonDur=0.12)])],
        props=[MTR('pm4', litAfter=0.0, screens=[[0.0, '400 ANS']], kickAt=SPIT4, kickAmp=0.1), FILL('fill4', (6.7, 1.3, 3.4), 3.0),
               P('rib4', 'ticketRibbon', pos=SLOT, ry=90, opts={'path': RIBZ4, 'text': '400 ANS', 'from': 0.0, 'len0': 1.27, 'rate': 2.0, 'accel': 0.02, 'spurts': SPIT4, 'spurtLen': 0.45, 'w': 0.55, 'rep': 0.4, 'across': True, 'edge': '#2A4FA0'})],
        cams=[FC(0.0, [6.55, 0.42, 5.1], [[METER[0], 2.15, METER[2]], [P1[0], 2.62, P1[2]], [METER[0], 0.0, METER[2]], [6.55, 0.0, 4.25]], top=0.07, bottom=0.97, lenses=range(40, 80))])   # (final pass) on the paper's path, 42 cm up
st.cue('sfx:paper', 'S04', 0.0, 0.5); st.cue('sfx:zip', 'S04', 0.05, 0.3); st.cue('pop', 'S04', 0.3, 0.2)

# 5: ...is three kilometres long. High over the street: the ticket runs down the pavement, swerves onto the road and snakes away to the vanishing
#    point, the man a dot at the machine. (pass 3) Three times wider, red print, a blue edge, on the grey road (review 2: a 10 px dotted line on a
#    cream pavement)
D5 = st.dur('S05'); SNAKE5 = [[r(SLOT[2] - z_), r(3.2 + 0.9 * math.sin(z_ * 0.33) - SLOT[0])] for z_ in range(14, 232, 3)]
RIB5P = [[0.0, 0.6], [-0.6, 0.72], [-2.6, 0.75], [-5.5, -0.4], [-8.5, -1.9], *SNAKE5]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[act('mec', P1, 0, 'stand', 'neutral', keys=[k(0.0, look=[5.0, 0.0, 40.0]), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O'}}, toonDur=0.0)])],
        props=[MTR('pm5', litAfter=0.0, screens=[[0.0, '400 ANS']]), CARP('car5'), BAY('bay5'),
               P('rib5', 'ticketRibbon', pos=SLOT, ry=90, opts={'path': RIB5P, 'text': '400 ANS', 'from': 0.0, 'len0': 60.0, 'rate': 70.0, 'accel': 0.02, 'w': 0.7, 'rep': 3.0, 'textH': 0.55, 'edge': '#2A4FA0', 'color': '#C8322A'})],
        cams=[FC(0.0, [9.0, 12.0, -9.0], [[P1[0], 0.0, P1[2]], [P1[0], 2.4, P1[2]], [3.2, 0.0, 50.0], [3.85, 0.0, -1.2]], top=0.1, bottom=0.74, lenses=range(30, 72), drift=(0.0, 0.3, -0.4), inside=(-9.4, 9.2, 0.2, 40.0, -200.0, 200.0))])
st.cue('whoosh', 'S05', 0.0, 1.0)

# 6: the town hall refuses to refund him. Over the clerk's shoulder: him at the counter, the paper roll standing behind him a head taller than he is,
#    400 ANS printed on its side and down its loose end (review 3: chin-high, unprinted); the big stamp raised high in her left hand, the right way
#    up, knob in her fist and red rubber down (review 3: upside down, a gavel), comes down square on his claim and leaves REFUSÉ in red ink on it
D6 = st.dur('S06'); HIT6 = 0.9; ME6 = [0.3, 0, 1.05]; ST6 = [0.12, 1.16, -0.14]; ROLL6 = [0.75, 0, 1.95]   # the roll stands behind him, to his left, turned to the lens
st.shot('S06', 'mairie', setOpts={'front': 3.6, 'frontSign': {'text': 'ÉTAT CIVIL', 'x': -1.15, 'y': 1.78, 'w': 1.5, 'h': 0.36}, 'map': False}, actors=[
        act('mec', ME6, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.12, 1.9, -0.3]), k(r(HIT6 + 0.02), toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [0.94, 1.06, 0.94], 'lay': [-0.08, 0.0]}, toonDur=0.04, toonEase='out'),   # (review 1) a real flinch at the stamp
            k(r(HIT6 + 0.14), toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1), k(1.45, look='camera', lookDur=0.25), k(1.6, toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.3)]),
        act('guichet', [-0.4, 0, -0.75], 10, 'sitWrite', 'neutral', keys=[k(0.0, look=[0.1, 0.8, -0.15]),
            k(0.3, toon={'reach': {'L': [0.12, 1.9, -0.32, 1, 0.04]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'brow': -0.5}}, toonDur=0.35, toonEase='out'),
            k(r(HIT6 - 0.06), toon={'reach': {'L': [*ST6, 1, 0.04]}, 'hands': {'L': 'grip'}, 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.2, 'brow': -0.7}}, toonDur=0.06, toonEase='in'),
            k(r(HIT6 + 0.35), look=ME6, lookDur=0.2), k(r(HIT6 + 0.45), clip='shakeHead')])],
        props=[P('desk6', 'desk', pos=[0.0, 0, 0.0], opts={'w': 1.6}), P('chaise6', 'chair', pos=[-0.4, 0, -0.75]),
               P('rouleau6', 'paperRoll', pos=ROLL6, ry=155, opts={'r': 1.25, 'w': 0.34, 'tail': 0.6, 'text': '400 ANS', 'tailText': '400 ANS'}),
               P('tampon6', 'bigStamp', on={'actor': 'guichet', 'hand': 'L', 'offset': [0.0, -0.06, 0.0], 'hang': True}, scale=1.0),   # hangs from her fist: rubber down whatever her wrist does
               P('formulaire6', 'paperSheet', pos=[ST6[0], 0.775, ST6[2]], rot=[-PI / 2, 0, 0], opts={'w': 0.3, 'h': 0.4, 'lines': ['REMBOURSEMENT'], 'stamp': {'text': 'REFUSÉ', 'at': HIT6, 'rot': 0.18, 'w': 0.86}})],
        cams=[FC(0.0, [0.8, 2.6, -2.3], [[ME6[0], 2.45, ME6[2]], [ME6[0], 1.1, ME6[2]], [ROLL6[0], 2.52, ROLL6[2]], [1.3, 0.35, 0.8], [ST6[0], 0.9, ST6[2]], [ST6[0], 0.55, ST6[2]], [0.12, 2.0, -0.32]], top=0.18, lenses=range(26, 70), bottom=0.76, inside=(-4.8, 4.8, 0.3, 3.4, -2.5, 3.4))])
st.cue('thud', 'S06', HIT6, 0.6)

# 7: so he stays parked. Through the windscreen: he sits back in the driver's seat, folds his arms, settles, and looks at us; the ticket on the dash;
#    (final pass) the hold breathes, a smug eyebrow, a blink (review 3: a freeze from 0.87 s)
D7 = st.dur('S07')
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[3.45, 1.8, -6.0]), k(0.2, toon=CROSS, toonDur=0.25, toonEase='out'),
            k(0.55, toon={**CROSS, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.12, toonEase='out'), k(0.75, toon={**CROSS, 'sq': [1.0, 1.0, 1.0], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2),
            k(0.95, look='camera', lookDur=0.3), k(1.3, toon={**CROSS, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.42, toon={**CROSS, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1),
            *LIFE(0.88, 1.28, {**DEAD, 'mouth': 'line'}, per=0.2), k(1.1, toon={'face': {**DEAD, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.12, keepPose=True),   # (final pass) the hold breathes, a smug eyebrow
            *LIFE(1.48, D7, {**DEAD, 'mouth': 'line'}, per=0.2)])],
        props=[CARP('car7'), BAY('bay7'), MTR('pm7', litAfter=0.0, screens=[[0.0, '400 ANS']]),
               P('tk7', 'signBoard', pos=cw(0.98, 1.0, 0.32), ry=180, opts={'text': '400 ANS', 'bg': '#FFFFFF', 'fg': '#2A4FA0', 'w': 0.34, 'h': 0.13, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [2.7, 1.8, -4.6], [[SEAT[0], 2.15, SEAT[2]], [SEAT[0], 0.9, SEAT[2]], [4.25, 1.0, -0.98], [2.95, 0.9, -1.6]], top=0.16, bottom=0.74, drift=(0.0, 0.0, 0.15))])
st.cue('sfx:carDoor', 'S07', 0.05, 0.4)

# 8: he lives in his car. Three-quarter front, closer (review 3: his face 8 % of the width): gingham curtains, a stove pipe puffing white smoke
#    rimmed in ink, a geranium on the roof, an aerial, the BIENVENUE mat, washing strung from the aerial to the machine's P sign (review 3: never in
#    the frame); him inside with a big cup of coffee, a sip, a breath, a blink; a slow push in
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=[3.45, 1.9, -5.0]),
            k(0.0, toon={'reach': {'R': [3.55, 1.55, -0.55, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.5, toon={'reach': {'R': [3.5, 1.95, -0.35, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.6, 'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'),
            k(0.95, toon={'reach': {'R': [3.55, 1.55, -0.55, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'), k(1.1, look='camera'),
            *LIFE(0.14, 0.46, {'lid': 0.3, 'mouth': 'smile'}, per=0.16), *LIFE(1.2, D8, {'lid': 0.3, 'mouth': 'smile'}, per=0.12, blink=1.26)])],   # (final pass) the holds breathe
        props=[CARP('car8'), BAY('bay8'), HOME('home8', smokeBig=True), MTR('pm8', screens=[[0.0, '400 ANS']]),
               P('linge8', 'clothesline', pos=[3.35, 2.62, 0.45], opts={'to': [2.25, -0.54, 2.45], 'n': 3, 'sag': 0.12, 'u0': 0.58, 'u1': 0.9}),   # from the aerial to the top of the P sign
               P('tasse8', 'hotMug', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, scale=1.5)],
        cams=[FC(0.0, [1.4, 2.75, -4.4], [[SEAT[0], 2.2, SEAT[2]], [METER[0], 2.15, METER[2]], [METER[0], 0.0, METER[2]], [4.27, 3.4, 1.15], [2.6, 0.0, -0.05]], top=0.12, bottom=0.72, drift=(0.15, -0.05, 0.2))])   # (final pass) closer, from higher: the washing clears the roof

# 9: he got married on his bay. Through the windscreen: him at the wheel, the bride beside him in her veil; the mayor in his sash reads at the driver's
#    window; confetti rains on the roof
D9 = st.dur('S09')
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=[2.6, 2.1, -0.6]), k(0.7, look='camera', lookDur=0.25), k(0.75, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.2)]),
        act('mariee', SEAT2, 180, 'drive', 'happy', keys=[k(0.0, look=[3.45, 2.1, -0.05]), k(0.85, look='camera', lookDur=0.3), k(0.9, toon={'face': {'lid': 0.2, 'mouth': 'smile'}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.15)]),
        act('maire', [2.35, 0, -0.55], 140, 'holdUp', 'neutral', keys=[k(0.0, look=[3.45, 2.0, -0.05]), k(0.9, look='camera', lookDur=0.3)])],
        props=[CARP('car9'), BAY('bay9'), HOME('home9', smoke=False), P('voile9', 'brideVeil', on={'actor': 'mariee', 'joint': 'head', 'offset': [0, 0.42, 0]}),
               P('sash9', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8}),
               P('acte9', 'paperSheet', on={'actor': 'maire', 'hand': 'R', 'offset': [0.0, 0.05, 0.06]}, opts={'w': 0.26, 'h': 0.34, 'lines': ['MARIAGE']}),
               P('conf9', 'confettiRain', pos=[CAR[0], 0.0, -0.3], opts={'w': 3.4, 'h': 3.6, 'd': 4.2, 'n': 170})],
        cams=[FC(0.0, [3.3, 2.05, -4.9], [[SEAT[0], 2.15, SEAT[2]], [SEAT2[0], 2.2, SEAT2[2]], [2.35, 2.45, -0.55], [CAR[0], 0.8, -1.9], [2.35, 0.0, -0.55]], top=0.14, bottom=0.76)])
st.cue('sfx:bell', 'S09', 0.1, 0.4)

# 10: his children grew up... A chalk hopscotch in the bay ahead of the car: one kid hops along it, the other cheers by the bonnet; him at the wheel,
#     proud; (final pass) lower and pushing in on him
D10 = st.dur('S10'); HZ = -2.75; HOPS = [(0.15, 3.05), (0.42, 3.45), (0.69, 3.85), (0.96, 4.25), (1.2, 4.6)]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=[3.8, 1.0, HZ]), k(0.2, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.2)]),
        act('gamin1', [2.65, 0, HZ], 90, 'stand', 'happy', scale=0.72, keys=[k(0.0, look=[4.6, 0.0, HZ]), *[k(r(t0 - 0.12), to=[x, 0, HZ], dur=0.24, arc=0.32, ease='inOut', clip='jump', face='keep') for t0, x in HOPS]]),
        act('gamin2', [2.3, 0, -2.1], 40, 'celebrate', 'happy', scale=0.72, keys=[k(0.0, look=[3.4, 1.2, HZ])])],
        props=[CARP('car10'), BAY('bay10', num=''), HOME('home10', smoke=False), P('marelle10', 'hopscotch', pos=[2.8, 0, HZ], opts={'len': 2.1, 'w': 0.72})],
        cams=[FC(0.0, [3.5, 2.8, -6.0], [[2.65, 1.9, HZ], [4.6, 1.9, HZ], [2.3, 1.9, -2.1], [CAR[0], 2.1, -1.0], [2.8, 0.0, HZ + 0.4]], top=0.12, bottom=0.78, drift=(0.0, -0.25, 0.9))])   # (final pass) lower, the other kid by the bonnet, a push in of 0.9 m (review 3: his face 4 % of the width)
for t0, _ in HOPS: st.cue('sfx:stepSoft', 'S10', t0, 0.15)

# 11: ...between two white lines. The kid stands against the machine's side, pencilled heights above earlier ones. (pass 3) He is on tiptoes, his
#     neck stretched for the next mark (review 2: a stiff pose for the whole shot); his father's flat hand squashes him back down to his height,
#     then the pencil marks it
D11 = st.dur('S11'); KID = [5.52, 0, 2.42]; MARKS = [[0.82, 'LÉO 4 ANS'], [0.94, 'LÉO 5 ANS'], [1.06, 'LÉO 6 ANS'], [1.18, 'LÉO 7 ANS']]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[act('gamin1', KID, 180, 'stand', 'happy', scale=0.72, keys=[k(0.0, look='camera'),
            k(0.0, toon={'sq': [0.92, 1.14, 0.92], 'bend': {'neck': [-0.15, 0, 0, 1.5, None]}, 'buzz': 0.004, 'face': {'lid': 0.1, 'mouth': 'clench', 'brow': 0.7, 'gy': -0.6}}, toonDur=0.0),
            k(0.42, toon={'sq': [1.08, 0.88, 1.08], 'face': {'lid': 0.3, 'mouth': 'pout', 'brow': -0.4}}, toonDur=0.07, toonEase='in'),   # squashed back down
            k(0.6, toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'mouth': 'pout', 'brow': -0.3}}, toonDur=0.14),
            k(0.95, toon={'face': {'lid': 0.2, 'mouth': 'grin'}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.12)]),
        act('mec', [6.2, 0, 2.8], -140, 'stand', 'happy', keys=[k(0.0, look=[5.52, 1.3, 2.42]), k(0.0, toon=REACH('R', [5.56, 1.5, 2.46], 'open'), toonDur=0.0),
            k(0.3, toon=REACH('R', [5.56, 1.2, 2.46], 'open'), toonDur=0.16, toonEase='in'),   # the hand comes down flat on the boy's head
            k(0.7, toon=REACH('R', [5.75, 1.22, 2.64], 'pinch'), toonDur=0.15), k(0.98, look='camera', lookDur=0.22)])],
        props=[MTR('pm11', marks=MARKS, screens=[[0.0, '400 ANS']], plaque='PLACE N° 12/DEPUIS 2026'), CARP('car11'), BAY('bay11'), HOME('home11'),
               P('crayon11', 'pen', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, opts={'len': 0.12})],
        cams=[FC(0.0, [5.75, 1.3, -0.3], [[KID[0], 1.6, KID[2]], [KID[0], 0.0, KID[2]], [6.2, 2.45, 2.8], [6.2, 0.0, 2.8], [METER[0], 1.5, 2.66]], top=0.16, bottom=0.74)])

# 12: the postman slips his mail... The postman walks up to the windscreen with a letter and tucks it under the wiper; him inside, watching
D12 = st.dur('S12'); WIPE = cw(1.56, 1.05, -0.38); LETAT = 1.1
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[2.4, 1.9, -2.8]), k(0.9, look=WIPE, lookDur=0.2)]),
        act('facteur', [2.45, 0, 1.0], 180, 'walk', 'happy', keys=[k(0.0, to=[2.6, 0, -1.72], dur=0.8, clip='walk', then='stand', ease='out'), k(0.0, look='camera'), k(0.82, turn=75), k(0.8, look=WIPE),
            k(0.85, toon=REACH('R', [WIPE[0], WIPE[1] + 0.08, WIPE[2] - 0.05], 'pinch'), toonDur=0.2, toonEase='out'), k(1.3, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.1)])],
        props=[CARP('car12'), BAY('bay12'), HOME('home12', letterAt=LETAT), P('lettre12', 'envelope', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, keys=[k(LETAT, visible=False)]),
               P('sac12', 'cardboardBox', on={'actor': 'facteur', 'joint': 'torso', 'offset': [0.24, 0.1, 0.0]}, scale=0.35)],
        cams=[FC(0.0, [2.5, 1.7, -6.2], [[2.45, 2.45, 1.0], [2.6, 2.45, -1.72], [2.6, 0.0, -1.72], [SEAT[0], 2.15, SEAT[2]], [4.75, 0.5, -2.0]], top=0.14, bottom=0.74, drift=(0.15, 0.0, 0.2))])
st.cue('sfx:stepSoft', 'S12', 0.2, 0.15); st.cue('sfx:stepSoft', 'S12', 0.55, 0.15); st.cue('sfx:paper', 'S12', LETAT, 0.3)

# 13: ...under the wiper. Close on the windscreen: the envelope flutters under the wiper. Behind the glass he tips forward out of his seat right up to
#     the windscreen (review 3: he never came to the glass; a seat move made him hop behind the roof bar in review 2, so the whole body tips about
#     the seat, the neck bent back to keep his face on the glass), nose on the glass, the near eye twice its size on the address, his eyes reading
#     along it; then he pulls back and nods: it is for him
D13 = st.dur('S13')
LEAN13 = lambda lay, a: {'lay': [lay, 0.0], 'bend': {'spine': [a, 0, 0, 1.0, None], 'neck': [r(-(lay + a)), 0, 0, 1.0, None]}}   # tipped `lay` about the seat and bowed `a`, the face kept upright
EYE13 = {'eyeL': 1.0, 'lidR': 0.75, 'lid': 0.05, 'mouth': 'line', 'browL': 0.9, 'browR': -0.6}   # the near eye at the glass, magnified
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=WIPE),
            k(0.0, toon={**LEAN13(0.0, 0.0), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.08, toon={**LEAN13(0.08, 0.06), 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.1, toonEase='inOut'),   # a squint at the envelope
            k(0.2, toon={**LEAN13(0.6, 0.3), 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.22, toonEase='in'),   # he comes to the glass
            k(0.42, toon={**LEAN13(0.64, 0.32), 'scl': {'head': [1.22, 1.08, 0.62]}, 'face': EYE13}, toonDur=0.05, toonEase='out'),   # nose on the glass: the near eye twice its size
            k(0.52, toon={'sq': [0.99, 1.02, 0.99], 'face': {**EYE13, 'gx': -0.5}}, toonDur=0.1, keepPose=True), k(0.66, toon={'sq': [1.0, 1.0, 1.0], 'face': {**EYE13, 'gx': 0.5}}, toonDur=0.12, keepPose=True),   # reading the address
            k(0.78, toon={'face': {**EYE13, 'gx': 0.0, 'eyeL': 1.1}}, toonDur=0.05, keepPose=True),
            k(0.84, toon={**LEAN13(0.46, 0.24), 'scl': {'head': [1.08, 1.04, 0.9]}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.08),   # pulls back: it is for him
            k(0.93, toon={**LEAN13(0.56, 0.28), 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.06), k(1.02, toon={**LEAN13(0.44, 0.24), 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.08), k(1.05, look='camera', lookDur=0.12),
            k(1.12, toon={'sq': [0.99, 1.02, 0.99], 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.08, keepPose=True)])],
        props=[CARP('car13'), HOME('home13', letter=True)],
        cams=[FC(0.0, [3.55, 1.45, -3.0], [[WIPE[0], 0.92, WIPE[2]], [3.47, 2.0, -0.7], [3.0, 1.4, -1.0], [3.95, 1.4, -1.0]], top=0.16, bottom=0.74, lenses=range(20, 60))])

# 14: every year the mayor... (pass 3) Close and low: in his sash the mayor strides in three-quarters to us, the giant gold scissors already going
#     up, and is in his pose by 0.5 s (review 2: a distant wide, his face turned away until the last frames); he snips the air twice; a wide
#     blue-white-red ribbon with a rosette across the front of the bay
D14 = st.dur('S14'); MAY = [3.15, 0, -3.6]; MAY0 = [2.2, 0, -2.85]; RIBZ = -3.0
SCI = lambda pid, snip: P(pid, 'goldScissors', on={'actor': 'maire', 'hand': 'R', 'offset': [0, 0, 0.04]}, scale=2.0, opts={'open': 0.5, 'snip': snip})
RUB = lambda pid, **kw: P(pid, 'bayRibbon', pos=[CAR[0], 0, RIBZ], opts={'w': 2.3, 'h': 0.95, **kw})
SASH = lambda pid: P(pid, 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8})
UP14 = {'touch': {'R': ['torso', -0.4, 0.98, 0.12, 1, 0.02]}, 'hands': {'R': 'grip'}}   # the scissors held high, on the ribbon's side
GRIN14 = {'lid': 0.2, 'mouth': 'grin', 'brow': 0.5}
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=MAY), k(0.75, look='camera')]),
        act('maire', MAY0, 128, 'walk', 'smug', keys=[k(0.0, to=MAY, dur=0.42, clip='walk', then='stand', ease='out'), k(0.0, look='camera'),
            k(0.0, toon={'touch': {'R': ['torso', -0.3, 0.55, 0.3, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.12, toon={**UP14, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.3, toonEase='out'), k(0.44, turn=162),
            k(0.46, toon={**UP14, 'sq': [0.96, 1.06, 0.96], 'face': GRIN14}, toonDur=0.06, toonEase='out'),   # the pose: chest out
            k(0.62, toon={**UP14, 'face': GRIN14}, toonDur=0.12),
            k(1.0, toon={**UP14, 'face': {'lid': 1.0, 'mouth': 'grin'}}, toonDur=0.05), k(1.08, toon={**UP14, 'face': GRIN14}, toonDur=0.06)])],
        props=[CARP('car14'), BAY('bay14'), HOME('home14', smoke=False), RUB('ruban14'), SCI('sci14', [[0.0, 1.0], [0.64, 1.0], [0.7, 0.0], [0.78, 1.0], [0.88, 1.0], [0.94, 0.0], [1.02, 1.0]]), SASH('sash14')],
        cams=[FC(0.0, [3.9, 1.25, -6.9], [[MAY[0], 2.15, MAY[2]], [r(MAY[0] + 1.0), 2.6, MAY[2]], [r(MAY[0] - 0.4), 1.3, MAY[2]], [MAY[0], 0.72, MAY[2]], [SEAT[0], 2.0, SEAT[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:fanfare', 'S14', 0.2, 0.3); st.cue('sfx:tick', 'S14', 0.7, 0.2); st.cue('sfx:tick', 'S14', 0.94, 0.2)

# 15: ...opens his bay. The snip: the ribbon halves drop, the rosette falls, confetti bursts, the mayor beams at us with the scissors back up, the
#     man at the wheel waves. (pass 3) Close and low, the ribbon across the lower third. (final pass) Sunk 18 cm in his seat: his face under the
#     windscreen's top bar while he waves (review 3: hidden behind it)
D15 = st.dur('S15'); SNIP = 0.3; CUT15 = [3.55, 1.0, -3.1]
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('mec', [SEAT[0], -0.06, SEAT[2]], 180, 'drive', 'happy', keys=[k(0.0, look='camera'), k(r(SNIP + 0.1), clip='royalWave', params={'freq': 2.2})]),
        act('maire', MAY, 162, 'stand', 'smug', keys=[k(0.0, look=CUT15), k(0.0, toon={'reach': {'R': [*CUT15, 1, 0.04]}, 'hands': {'R': 'grip'}, 'lay': [0.12, 0.0], 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(SNIP, toon={'reach': {'R': [*CUT15, 1, 0.04]}, 'hands': {'R': 'grip'}, 'lay': [0.12, 0.0], 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.2, 'mouth': 'grin'}}, toonDur=0.05),
            k(r(SNIP + 0.25), look='camera', lookDur=0.15), k(r(SNIP + 0.3), toon={**UP14, 'sq': [0.97, 1.05, 0.97], 'face': {'lid': 0.2, 'mouth': 'grin', 'brow': 0.6}}, toonDur=0.18, toonEase='out'),
            k(1.05, toon={**UP14, 'face': {'lid': 1.0, 'mouth': 'grin'}}, toonDur=0.05), k(1.13, toon={**UP14, 'face': {'lid': 0.2, 'mouth': 'grin', 'brow': 0.6}}, toonDur=0.06)])],
        props=[CARP('car15'), BAY('bay15'), HOME('home15', smoke=False), RUB('ruban15', cutAt=SNIP),
               SCI('sci15', [[0.0, 1.0], [r(SNIP - 0.04), 1.0], [SNIP, 0.0], [r(SNIP + 0.4), 0.0], [r(SNIP + 0.6), 1.0]]), SASH('sash15'),
               P('conf15', 'confettiRain', pos=[CAR[0], 0.0, -2.6], opts={'w': 3.4, 'h': 3.4, 'd': 1.8, 'n': 170, 'at': SNIP})],
        cams=[FC(0.0, [4.4, 0.9, -6.1], [[MAY[0], 2.15, MAY[2]], [r(MAY[0] - 0.4), 1.3, MAY[2]], [4.7, 1.0, RIBZ], [MAY[0], 0.62, MAY[2]], [SEAT[0], 2.0, SEAT[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:twang', 'S15', SNIP, 0.4); st.cue('pop', 'S15', r(SNIP + 0.05), 0.3)

# 16: tourists photograph it. A real selfie (review 3: she stood square in the middle ground, the phone a black slab): the lens at her phone's side,
#     close, her head big on the left, grinning at the phone she holds out toward us, leaning back and aside so the windscreen sits in the clear gap
#     on the right with him behind it, thumb up; the second tourist down on one knee at the bumper with a flash; click; she checks the picture while
#     he wiggles his thumb hard
D16 = st.dur('S16'); SELF = [4.41, 0, -2.98]; PH16 = [4.66, 1.72, -3.62]; T2 = [3.72, 0, -2.3]; C16 = [4.4, 1.95, -4.4]; LK16 = [3.85, 1.35, 0.0]
TH16 = lambda y=1.85, x=3.78: {'reach': {'R': [x, y, -0.9, 1, 0.04]}, 'hands': {'R': 'thumbUp'}}   # his right hand, in the middle of the windscreen
EYE16 = {'touch': {'R': ['face', -0.05, 0.6, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.58, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
ARM16 = lambda p=PH16: {'reach': {'R': [*p, 1, 0.04]}, 'hands': {'R': 'grip'}, 'lay': [-0.08, 0.12]}   # arm out toward the lens, leaning back and aside
SM16 = lambda b=0.6: {'face': {'lid': 0.15, 'mouth': 'grin', 'brow': b}}
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=C16), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.3, toon={**TH16(1.7), 'face': {**DEAD, 'mouth': 'smirk'}}, toonDur=0.12, toonEase='out'), k(0.44, toon={**TH16(1.9), 'face': {**DEAD, 'mouth': 'smirk'}}, toonDur=0.08),   # the thumb shoots up
            *LIFE(0.6, 1.12, {**DEAD, 'mouth': 'smirk'}, per=0.18, blink=0.8),
            *[k(r(1.15 + 0.08 * i), toon={**TH16(1.98 if i % 2 == 0 else 1.8, 3.92 if i % 2 == 0 else 3.66), 'face': {**DEAD, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.07, toonEase='inOut') for i in range(6)],   # the wiggle
            k(1.66, toon={**TH16(), 'face': {**DEAD, 'mouth': 'smirk'}}, toonDur=0.1)]),
        act('touriste1', SELF, 180, 'stand', 'happy', keys=[k(0.0, look=PH16), k(0.0, toon={**ARM16([4.62, 1.6, -3.4]), **SM16(0.4)}, toonDur=0.0),
            k(0.12, toon={**ARM16(), **SM16()}, toonDur=0.3, toonEase='out'),   # the arm goes out, she leans back
            k(0.6, toon={**ARM16(), **SM16(0.8)}, toonDur=0.1), k(0.84, toon={**ARM16(), 'sq': [1.03, 0.95, 1.03], **SM16(0.8)}, toonDur=0.05, toonEase='in'),   # the pose, then the click
            k(0.92, toon={**ARM16(), 'sq': [0.98, 1.03, 0.98], 'face': {'lid': 0.0, 'mouth': 'grin', 'brow': 1.0}}, toonDur=0.06),
            k(1.15, toon={**ARM16([4.5, 1.55, -3.45]), 'face': {'lid': 0.45, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.22, toonEase='inOut'), k(1.15, look=[4.5, 1.55, -3.45], lookDur=0.15),   # she checks the picture
            k(1.55, toon={**ARM16([4.5, 1.55, -3.45]), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.15, 'mouth': 'grin', 'brow': 0.7}}, toonDur=0.08), k(1.6, look=C16, lookDur=0.12)]),
        act('touriste2', T2, 25, 'kneel', 'happy', keys=[k(0.0, look=[3.45, 1.75, -0.4]), k(0.0, toon=EYE16, toonDur=0.0), k(0.37, toon={**EYE16, 'sq': [1.0, 0.96, 1.0]}, toonDur=0.05), k(0.55, toon=EYE16, toonDur=0.12),
            k(1.32, toon={**EYE16, 'sq': [1.0, 0.96, 1.0]}, toonDur=0.05), k(1.5, toon=EYE16, toonDur=0.12)])],
        props=[CARP('car16'), BAY('bay16'), HOME('home16', smoke=False), P('tel16', 'handset', on={'actor': 'touriste1', 'hand': 'R', 'offset': [0.0, 0.05, 0.04], 'face': 'camera', 'faceBack': True}, scale=1.5, opts={'screen': '#8FD3F2'}),
               P('app16', 'pressCamera', on={'actor': 'touriste2', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': [0.35, 1.3], 'burst': 0.5})],
        cams=[cam(0.0, C16, r3([C16[0] - 0.04, C16[1], C16[2] + 0.12]), LK16, r3([LK16[0] - 0.04, LK16[1], LK16[2] + 0.12]), lens=50)])   # (final pass) at her phone's side
st.cue('sfx:shutter', 'S16', 0.35, 0.3); st.cue('sfx:shutter', 'S16', 0.88, 0.3); st.cue('sfx:shutter', 'S16', 1.3, 0.3)

# 17: yesterday a delivery van... Down the road the van comes on fast from the first frame (review 3: it came in at 0.73 s) and stops dead alongside
#     his car (review 1: it eased to a stop): the nose pitches down hard, the rear lifts, two rocks to rest; the driver lurches, sunk in his seat so his
#     head stays under the cab roof as it dips (review 3: it popped up through it); its hazard lights start blinking; he blinks at it
D17 = st.dur('S17'); STOP17 = 1.3; V0 = [VAN[0], 0, 13.3]; VNEAR = [VAN[0], 0, r(VAN[2] + 1.0)]
VKEYS = lambda a, b: [k(0.0, to=a, dur=r(STOP17 - 0.1), ease='linear'), k(r(STOP17 - 0.1), to=b, dur=0.1, ease='out')]
DRV17 = lambda v: vw(1.15, 0.38, -0.45, v)   # the driver 12 cm lower than the seat's mark
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[1.6, 1.8, 8.0]), k(0.8, look=[1.6, 1.8, 2.0], lookDur=0.3), k(1.35, look=[2.3, 1.9, 0.0], lookDur=0.1),
            k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0), *LIFE(0.2, 1.3, {**DEAD, 'mouth': 'line'}, per=0.25, blink=0.6),
            k(1.35, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.06, toonEase='out')]),
        act('livreur', DRV17(V0), 180, 'drive', 'neutral', keys=[*VKEYS(DRV17(VNEAR), DRV17(VAN)), k(0.0, look=[1.15, 1.8, -8.0]),
            k(STOP17, toon={'lay': [0.35, 0.0], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O'}}, toonDur=0.06, toonEase='out'), k(r(STOP17 + 0.22), toon={'lay': [-0.06, 0.0], 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.15)])],   # the lurch
        props=[CARP('car17'), BAY('bay17'), HOME('home17', smoke=False), VANP('van17', V0, brakeAt=r(STOP17 - 0.04), brakeAmp=2.0, hazardFrom=r(STOP17 + 0.15), keys=VKEYS(VNEAR, VAN))],
        cams=[FC(0.0, [0.4, 4.0, -9.5], [[r(CAR[0] + 0.95), 0.0, -2.1], [r(VAN[0] - 1.05), 0.0, r(VAN[2] - 2.7)], [VAN[0], 2.85, r(VAN[2] + 2.6)], [CAR[0], 1.2, 2.1], [0.6, 2.5, 11.0], [2.6, 2.5, 11.0]], top=0.22, bottom=0.84, lenses=range(30, 70))])   # (final pass) down the road: the van in the frame from its start
st.cue('engine', 'S17', 0.0, 1.3); st.cue('sfx:brake', 'S17', r(STOP17 - 0.2), 0.4)

# 18: ...parked beside him. Close through his windscreen (review 1: faces 20 px tall): the wall of van a hand's width from his window, hazards
#     blinking; his eyes go to the van wall first, then his head; then at us; a slow blink
D18 = st.dur('S18')
st.shot('S18', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[2.3, 1.9, -0.05]), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'gx': -0.8}}, toonDur=0.0),
            k(0.6, look='camera', lookDur=0.25), k(0.55, toon={'face': {**DEAD, 'mouth': 'line', 'gx': 0.0}}, toonDur=0.1),
            k(0.95, toon={'face': {**DEAD, 'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.08, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12)]),
        act('livreur', VSEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[1.15, 1.8, -8.0]), k(0.7, look=[1.15, 1.6, -0.8], lookDur=0.2),
            k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0), k(0.85, toon={'face': {'lid': 0.15, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.12), k(1.0, toon={'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=0.06), k(1.1, toon={'face': {'lid': 0.15, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.08)])],
        props=[CARP('car18'), BAY('bay18'), HOME('home18', smoke=False), VANP('van18', brakeAt=-0.25, hazardFrom=0.0, hazardRate=1.0)],
        cams=[FC(0.0, [3.55, 1.85, -2.2], [[SEAT[0], 2.3, SEAT[2]], [SEAT[0], 1.25, SEAT[2]], [2.5, 2.1, -0.05], [2.5, 1.3, -0.05], [4.05, 1.8, -0.05]], top=0.14, bottom=0.74, drift=(0.0, 0.0, 0.2))])
st.cue('sfx:honkTiny', 'S18', 0.4, 0.2)

# 19: double-parked. Straight down from above, higher (review 1: one car, cut by the bottom; the card over the bay's number): the car in its bay at
#     the top, the van alongside, hazards blinking slowly, two cars stuck behind it, each hopping on its honk (TÛT !); (final pass) each hop a metre
#     up, more than a wheel, nose first, squashed on landing (review 3: the hops did not register from above)
D19 = st.dur('S19'); C19A, C19B = 5.8, 10.0; Z19 = 3.4
HOP = lambda x, z, t0: [k(t0, to=[x, 1.0, z], dur=0.1, ease='out'), k(t0, rotTo=[0, r(PI / 2), 0.2], dur=0.08, ease='out'),   # (final pass) a metre up, more than a wheel (review 3: the hops did not register), nose first
                        k(r(t0 + 0.1), to=[x, 0.0, z], dur=0.11, ease='in'), k(r(t0 + 0.12), rotTo=[0, r(PI / 2), 0.0], dur=0.09, ease='in'), k(r(t0 + 0.21), squash=[1.1, 0.78, 1.1], dur=0.22)]   # and a squash on landing
st.shot('S19', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[3.45, 1.8, -5.0])]), act('livreur', VSEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[1.15, 1.8, -5.0])])],
        props=[CARP('car19'), BAY('bay19'), HOME('home19', mat=False), VANP('van19', hazardFrom=0.0, hazardRate=1.0),
               P('bouchon19a', 'car', pos=[1.6, 0, C19A], ry=90, opts={'color': '#3A7BC8', 'plate': 'GH-123-JK'}, keys=[*HOP(1.6, C19A, 0.15), *HOP(1.6, C19A, 0.75)]),
               P('bouchon19b', 'car', pos=[1.6, 0, C19B], ry=90, opts={'color': '#E8C547', 'plate': 'LM-456-NP'}, keys=[*HOP(1.6, C19B, 0.45), *HOP(1.6, C19B, 0.95)]),
               P('tut19a', 'hicBurst', pos=[3.0, 2.5, C19A], face='camera', opts={'at': [0.15, 0.75], 'w': 1.7, 'text': 'TÛT !', 'inner': 0.76, 'fit': 0.6, 'hold': 0.25, 'bold': True}),
               P('tut19b', 'hicBurst', pos=[0.2, 2.5, C19B], face='camera', opts={'at': [0.45, 0.95], 'w': 1.7, 'text': 'TÛT !', 'inner': 0.76, 'fit': 0.6, 'hold': 0.25, 'bold': True})],
        cams=[cam(0.0, [2.6, 29.0, r(Z19 - 7.5)], [2.6, 28.6, r(Z19 - 7.3)], [2.6, 0.0, Z19], [2.6, 0.0, r(Z19 + 0.1)], lens=48)])   # (pass 3) from the other end (review 2: TÛT ! and 12 upside down), 15 degrees off the vertical
st.cue('sfx:honkLong', 'S19', 0.15, 0.4); st.cue('sfx:honk', 'S19', 0.45, 0.3); st.cue('sfx:honk', 'S19', 0.75, 0.3); st.cue('sfx:honkLong', 'S19', 0.95, 0.3)

# 20: he can't get out. From inside the van's cab, from higher and tilted down (review 3: the face slid into the caption band): his face hits his
#     window and splats, 1.4 wide by 0.7 tall, held; then it is dragged down the glass in three stick-slips, squeaking: on each stick his body sinks
#     while the face stays stuck and stretches up, on each slip it drops, leaving a greasy smear on the glass, his hands sliding after; it stops on
#     the van's sill line just above the captions (its lowest point above 74 % of the height), hangs, blinks, then pops back up, hair on end, under
#     his roof rail (he sits 20 cm lower in his seat for it)
D20 = st.dur('S20'); SL0, POP20 = 0.33, 1.0
SEAT20 = [r(SEAT[0] - 0.1), -0.08, SEAT[2]]
FLAT = lambda w=1.4, h=0.7: {'scl': {'head': [w, h, 0.35]}}
HG = lambda hy: {'reach': {'R': [3.0, r(hy), -0.38, 1, 0.04], 'L': [3.0, r(hy + 0.04), 0.28, 1, 0.04]}, 'hands': {'R': 'spread', 'L': 'spread'}}
GL = lambda hy, sy, f, w=1.4, h=0.7, sx=1.04: {**FLAT(w, h), **HG(hy), 'face': f, 'sq': [sx, sy, sx]}   # hands at hy on the glass, the body squashed to sy about the seat, the head w x h
SM20 = {'lid': 0.8, 'mouth': 'O', 'mouthH': 0.5}; UP20 = {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}
GLY = 1.46   # the pane's middle
st.shot('S20', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT20, -90, 'drive', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon=GL(1.62, 1.0, {'lid': 0.6, 'mouth': 'O'}, 1.15, 1.05, 1.0), toonDur=0.0),
            k(0.03, toon=GL(1.56, 1.02, {'lid': 0.9, 'mouth': 'O', 'mouthH': 0.6}, 1.42, 0.68), toonDur=0.04, toonEase='out'),   # SPLAT on the glass
            k(0.18, toon=GL(1.56, 1.02, {'lid': 0.85, 'mouth': 'O', 'mouthH': 0.6}, 1.38, 0.71), toonDur=0.08), k(0.26, toon=GL(1.56, 1.02, {'lid': 0.9, 'mouth': 'O', 'mouthH': 0.6}, 1.42, 0.69), toonDur=0.06),   # held, quivering
            k(SL0, toon=GL(1.56, 0.975, SM20, 1.32, 0.83), toonDur=0.12, toonEase='in'),   # stick: the body sinks, the face stays put and stretches up
            k(0.45, toon=GL(1.5, 0.965, SM20, 1.4, 0.72), toonDur=0.04, toonEase='out'),   # slip
            k(0.49, toon=GL(1.5, 0.92, SM20, 1.32, 0.845), toonDur=0.12, toonEase='in'),
            k(0.61, toon=GL(1.43, 0.91, SM20, 1.4, 0.73), toonDur=0.04, toonEase='out'),
            k(0.65, toon=GL(1.43, 0.865, SM20, 1.32, 0.855), toonDur=0.13, toonEase='in'),
            k(0.78, toon=GL(1.37, 0.86, {'lid': 0.9, 'mouth': 'O', 'mouthH': 0.5}, 1.4, 0.76), toonDur=0.05, toonEase='out'),   # on the sill line
            k(0.88, toon=GL(1.37, 0.855, {'lid': 1.0, 'mouth': 'O', 'mouthH': 0.5}, 1.4, 0.75), toonDur=0.05), k(0.95, toon=GL(1.37, 0.86, {'lid': 0.9, 'mouth': 'O', 'mouthH': 0.5}, 1.4, 0.76), toonDur=0.04),   # it hangs there; a blink
            k(POP20, toon={**HG(1.64), 'scl': {'head': [0.95, 1.05, 0.95]}, 'sq': [0.96, 1.0, 0.96], 'hairUp': 1.0, 'face': UP20}, toonDur=0.06, toonEase='out'),   # pops back up, hair on end, under the rail
            k(1.12, toon={**HG(1.64), 'sq': [1.03, 0.96, 1.03], 'hairUp': 1.0, 'face': UP20}, toonDur=0.08),
            k(1.24, toon={**HG(1.64), 'hairUp': 0.9, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.1),
            k(1.36, toon={**HG(1.64), 'hairUp': 0.9, 'sq': [0.99, 1.02, 0.99], 'face': {'lid': 1.0, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.05), k(1.42, toon={**HG(1.64), 'hairUp': 0.9, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.05)])],
        props=[CARP('car20'), VANP('van20', hazardFrom=0.0, hazardRate=1.0),
               P('vitre20', 'glassPane', pos=[2.965, GLY, 0.2], ry=-90, opts={'w': 2.2, 'h': 1.05, 'opacity': 0.2,   # his window, and the smear the face leaves on it
                   'smear': {'x': -0.25, 'w': 0.5, 'top': 0.15, 'keys': [[SL0, 0.15], [0.45, 0.15], [0.49, 0.115], [0.61, 0.115], [0.65, 0.047], [0.78, 0.047], [0.83, -0.005]]}})],
        cams=[cam(0.0, [1.557, 2.2, 0.152], [1.557, 2.2, 0.152], [11.438, -2.66, -1.134], lens=52)])   # (final pass) up under the cab roof, tilted down: y 2.0 at 16 %, the sill line at 73 % of the height
st.cue('sfx:bonk', 'S20', 0.05, 0.3); st.cue('sfx:squeak', 'S20', 0.45, 0.14); st.cue('sfx:squeak', 'S20', 0.61, 0.14); st.cue('sfx:squeak', 'S20', 0.78, 0.16); st.cue('pop', 'S20', POP20, 0.2)

# 21: the delivery man paid... The frame of 1 again, the button reading 500 ANS: he grins at us, his finger hovering over the green 1 H, nearly
#     pressing; it slides to the red, his eyes still on us; a small pull-back, then a jab: the button sinks, his finger recoils two frames, and the
#     screen flips to 500 ANS on contact (review 3: no wind-up, the arm locked, the screen still on 1 H); then he breathes, grins and blinks at us
D21 = st.dur('S21'); MTR5 = lambda pid, **kw: P(pid, 'horodateur', pos=METER, ry=90, opts={'labels': ['1 H', '500 ANS'], **kw})
GR = lambda out=0.06, up=0.03: REACH('R', [r(GREEN[0] + out), r(GREEN[1] + up), GREEN[2]])
GRIN21 = {'lid': 0.3, 'mouth': 'grin', 'brow': 0.6}; JAB21 = 0.64
st.shot('S21', 'parisStreet', setOpts=STREET, actors=[act('livreur', P1, FACE1, 'stand', 'smug', keys=[k(0.0, look='camera'),
            k(0.0, toon={**GR(), 'face': GRIN21}, toonDur=0.0),
            k(0.12, toon={**GR(0.02, 0.0), 'face': GRIN21}, toonDur=0.08), k(0.24, toon={**GR(0.07, 0.04), 'face': GRIN21}, toonDur=0.08),   # it hovers over the green, nearly presses
            k(0.34, toon={**PR(0.07, 0.03), 'face': {'lid': 0.35, 'mouth': 'smirk', 'brow': 0.8}}, toonDur=0.16, toonEase='inOut'),   # ...and slides to the red, his eyes still on us
            k(0.52, toon={**PR(0.17, 0.05), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': 1.0}}, toonDur=0.1, toonEase='out'),   # the pull-back
            k(r(JAB21 - 0.04), toon={**PR(-0.012), 'sq': [1.05, 0.94, 1.05], 'face': {'lid': 0.2, 'mouth': 'grin', 'brow': 0.8}}, toonDur=0.04, toonEase='in'),   # JAB: the button sinks
            k(r(JAB21 + 0.03), toon={**PR(0.04, 0.012), 'sq': [0.99, 1.02, 0.99], 'face': {'lid': 0.25, 'mouth': 'grin', 'brow': 0.8}}, toonDur=0.03, toonEase='out'),   # the recoil, two frames
            k(r(JAB21 + 0.1), toon={**PR(0.01), 'face': {'lid': 0.3, 'mouth': 'grin', 'brow': 0.8}}, toonDur=0.08),
            *LIFE(0.82, D21, {'lid': 0.3, 'mouth': 'grin', 'brow': 0.8}, per=0.16, blink=0.98), k(1.12, toon={'face': {'lid': 0.3, 'mouth': 'grin', 'brow': 1.0}}, toonDur=0.06, keepPose=True)])],
        props=[MTR5('pm21', pressAt=[JAB21], litAfter=JAB21, screens=[[JAB21, '500 ANS']], marks=MARKS, plaque='PLACE N° 12/DEPUIS 2026'), CARP('car21'), HOME('home21', smoke=False), VANP('van21', hazardFrom=0.0, hazardRate=1.0), FILL('fill21')],
        cams=[CAM1(P1, 2.3)])
st.cue('sfx:beep', 'S21', JAB21, 0.3)

# 22: ...for five hundred years. (pass 3) Low, face on to the machine: the screen on 500 ANS (final pass: it flips in 21) and the second ticket fires out level, like water
#     from a hose, and lands at our feet; the machine kicks back at each spit; the delivery man ducks, his helmet left hanging in the air where his
#     head was (review 2: the same ticket, only faster)
D22 = st.dur('S22'); FIRE22 = 0.2
st.shot('S22', 'parisStreet', setOpts=STREET, actors=[act('livreur', P1, FACE1, 'stand', 'smug', keys=[k(0.0, look=SCREEN), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'grin'}}, toonDur=0.0),
            k(r(FIRE22 + 0.04), look=[7.2, 0.4, 3.1], lookDur=0.08),
            k(r(FIRE22 + 0.03), toon={'sq': [1.14, 0.8, 1.14], 'hat': [0.38, 0.5, 2.6], 'face': {'lid': 0.0, 'pop': 0.8, 'popLen': 0.2, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.07, toonEase='out'),   # the take: he ducks, his helmet left hanging in the air where his head was
            k(0.5, toon={'sq': [1.1, 0.84, 1.1], 'hat': [0.3, 0.7, 5.0], 'face': {'lid': 0.0, 'pop': 0.7, 'popLen': 0.18, 'mouth': 'O', 'brow': 1.0, 'pupilShake': 1.0}}, toonDur=0.2),
            k(0.64, toon={'sq': [0.97, 1.04, 0.97], 'hat': [0.03, 0.3, 6.5], 'face': {'lid': 0.1, 'eye': 0.3, 'mouth': 'grin', 'brow': 0.8}}, toonDur=0.14, toonEase='in'),   # he comes back up under it: askew
            k(0.86, toon={'hat': [0.0, 0.28, 6.5], 'face': {'lid': 0.2, 'mouth': 'grin', 'brow': 0.8}}, toonDur=0.1),
            k(0.8, look='camera', lookDur=0.15)])],
        props=[MTR5('pm22', litAfter=0.0, screens=[[0.0, '500 ANS']], marks=MARKS, plaque='PLACE N° 12/DEPUIS 2026', kickAt=[FIRE22, 0.42, 0.64, 0.86], kickAmp=0.1), FILL('fill22', (6.8, 1.2, 2.9), 3.2),
               P('rib22', 'ticketRibbon', pos=SLOT, ry=90, opts={'path': [[0.0, 1.5], [-0.6, 1.8], [-4.0, 1.9]], 'jet': 0.95, 'jetDrop': 0.1, 'wave': 0.035, 'text': '500 ANS', 'from': FIRE22, 'rate': 24.0, 'accel': 0.05, 'w': 0.3, 'rep': 1.0, 'textH': 0.5, 'color': '#B8322A', 'edge': '#B8322A', 'turn': True})],
        cams=[FC(0.0, [7.5, 0.55, 3.45], [[SCREEN[0], 1.45, 2.9], [METER[0], 0.1, 2.9], [P1[0], 2.3, P1[2]], [7.1, 0.0, 3.1]], top=0.08, bottom=0.86, lenses=range(26, 76))])
st.cue('sfx:ding', 'S22', 0.17, 0.35); st.cue('sfx:paper', 'S22', FIRE22, 0.6); st.cue('whoosh', 'S22', FIRE22, 0.3, 0.4, 3000, 800); st.cue('pop', 'S22', r(FIRE22 + 0.1), 0.2)

# 23: they play cards on Sundays. (final pass) Front on, down the gap between the two windows, the tray in the middle tipped up to us. (pass 3) At window height across the gap (review 2: from above his head sat under the roof, in profile):
#     he sits up at his window, seen past the pillar, his head in the clear, three-quarters to us like the delivery man's; their eyes go to each other and down to the
#     cards; each winds up and slaps a card on the tray, tipped to us, which bounces; then the delivery man looks at us, and he does, a beat later
D23 = st.dur('S23'); TRAY = [2.79, 1.37, 0.0]; SLAPS = [0.5, 1.1, 1.55]; M23 = [3.15, 0.12, -0.05]; PILE = [2.79, 1.48, -0.03]
def HAND23(pt, f, sq=None): return {'reach': {'R': [*pt, 1, 0.04], 'L': [3.1, 1.28, -0.35, 1, 0.04]}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}
UP23, REST23 = [2.98, 1.95, -0.15], [2.98, 1.62, -0.12]
F23 = lambda gx=0.7, gy=0.0, lid=0.45: {'lid': lid, 'mouth': 'line', 'gx': gx, 'gy': gy}
def HANDV(pt, f, sq=None): return {'reach': {'R': [*pt, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': f, **({'sq': sq} if sq else {})}
LV_REST, LV_UP = [2.5, 1.7, -0.08], [2.55, 2.02, -0.12]
V23 = lambda gx=-0.7, gy=0.0, lid=0.3, m='smile': {'lid': lid, 'mouth': m, 'gx': gx, 'gy': gy}
st.shot('S23', 'parisStreet', setOpts=STREET, actors=[act('mec', M23, -165, 'drive', 'neutral', keys=[k(0.0, look=[2.5, 1.7, -3.0]),
            k(0.0, toon=HAND23(REST23, F23()), toonDur=0.0),
            k(0.24, toon=HAND23(UP23, F23(0.3, 0.5)), toonDur=0.16, toonEase='out'),   # the wind-up, a glance down
            k(0.44, toon=HAND23(PILE, F23(0.3, 0.6), [1.03, 0.95, 1.03]), toonDur=0.06, toonEase='in'),   # slap
            k(0.62, toon=HAND23(REST23, F23()), toonDur=0.2),
            k(1.05, toon=HAND23(REST23, F23(0.5, 0.6)), toonDur=0.06), k(1.25, toon=HAND23(REST23, F23()), toonDur=0.1),   # his eyes on the delivery man's card
            k(1.3, toon=HAND23(UP23, F23(0.3, 0.5)), toonDur=0.15, toonEase='out'),
            k(1.49, toon=HAND23(PILE, F23(0.3, 0.6), [1.03, 0.95, 1.03]), toonDur=0.06, toonEase='in'),   # slap
            k(1.68, toon=HAND23(REST23, F23()), toonDur=0.2),
            k(2.0, look='camera', lookDur=0.22), k(2.0, toon=HAND23(REST23, F23(0.0, 0.0)), toonDur=0.15),   # then he too looks at us
            k(2.32, toon=HAND23(REST23, F23(0.0, 0.0, 1.0)), toonDur=0.08), k(2.44, toon=HAND23(REST23, F23(0.0, 0.0)), toonDur=0.1)]),
        act('livreur', VSEAT2, 152, 'drive', 'happy', keys=[k(0.0, look=[2.6, 1.85, -2.4]), k(0.0, toon=HANDV(LV_REST, V23()), toonDur=0.0),
            k(0.46, toon=HANDV(LV_REST, V23(-0.4, 0.6)), toonDur=0.06), k(0.66, toon=HANDV(LV_REST, V23()), toonDur=0.1),   # he watches the first card land
            k(0.84, toon=HANDV(LV_UP, V23(-0.3, 0.5, 0.2, 'grin')), toonDur=0.16, toonEase='out'),
            k(1.04, toon=HANDV([2.77, 1.48, -0.03], V23(-0.3, 0.6, 0.2, 'grin'), [1.03, 0.95, 1.03]), toonDur=0.06, toonEase='in'),   # slap
            k(1.25, toon=HANDV(LV_REST, V23()), toonDur=0.2),
            k(1.5, toon=HANDV(LV_REST, V23(-0.4, 0.6)), toonDur=0.06), k(1.68, toon=HANDV(LV_REST, V23()), toonDur=0.1),
            k(1.8, look='camera', lookDur=0.22), k(1.8, toon=HANDV(LV_REST, V23(0.0, 0.0)), toonDur=0.15),
            k(2.5, toon=HANDV(LV_REST, V23(0.0, 0.0, 0.3, 'grin')), toonDur=0.1)])],
        props=[CARP('car23'), BAY('bay23'), HOME('home23'), VANP('van23'), P('fill23', 'glowLight', pos=[3.15, 2.3, -0.75], opts={'color': '#FFF1DC', 'k': 2.5, 'dist': 2.2, 'at': -1}),
               P('cartes23', 'cardTray', pos=TRAY, rot=[-0.75, 0, 0], opts={'w': 0.7, 'd': 0.4, 'slapAt': SLAPS, 'cardScale': 2.0, 'top': '#2E7D5B', 'bounce': 0.035}),
               P('main23a', 'cardFan', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, 0.02, 0.03], 'face': 'camera'}, opts={'s': 1.1}),
               P('main23b', 'cardFan', on={'actor': 'livreur', 'hand': 'L', 'offset': [0.0, 0.02, 0.03], 'face': 'camera'}, opts={'s': 1.1})],
        cams=[FC(0.0, [2.72, 1.62, -2.6], [[3.15, 2.1, -0.05], [2.05, 2.45, 0.0], [3.5, 1.75, -0.05], [1.75, 1.6, 0.0], [TRAY[0], 1.22, -0.1]], top=0.16, bottom=0.66, drift=(0.0, 0.0, 0.15))])   # (final pass) down the gap between the two windows: the tray in the middle (review 3: behind the van's pillar, the bottom 40 % grille)
st.cue('sfx:clink', 'S23', 0.5, 0.25); st.cue('sfx:clink', 'S23', 1.1, 0.25); st.cue('sfx:clink', 'S23', 1.55, 0.25); st.cue('sfx:bell', 'S23', 0.0, 0.25)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le parcmètre", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'guichet': {'preset': 'madame', 'seed': 801, 'suit': '#5B7FA8', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'mariee': {'preset': 'femme', 'seed': 802, 'suit': '#F4F1EA', 'build': {'width': 0.85, 'headWidth': 1.22}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 803, 'suit': '#26365F', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
    'gamin1': {'preset': 'gamin', 'seed': 804, 'suit': '#E8A33C', 'toon': EX},
    'gamin2': {'preset': 'gamin', 'seed': 805, 'suit': '#5BB5A8', 'toon': EX},
    'facteur': {'preset': 'worker', 'seed': 806, 'suit': '#F2C230', 'pants': '#2F4A8A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'touriste1': {'preset': 'tourist', 'seed': 807, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'touriste2': {'preset': 'tourist', 'seed': 808, 'suit': '#E25C7A', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'touriste3': {'preset': 'madame', 'seed': 809, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'livreur': {'preset': 'worker', 'seed': 810, 'suit': '#7A5230', 'pants': '#3A3A3A', 'build': {'width': 1.05, 'headWidth': 1.22}, 'toon': EX},
})
