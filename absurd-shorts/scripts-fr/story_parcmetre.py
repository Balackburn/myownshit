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
HOME = lambda pid, **kw: P(pid, 'carHome', pos=CAR, ry=90, opts=kw)
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
CROSS = {'touch': {'R': ['torso', 0.13, 0.45, 0.2, 1, 0.02], 'L': ['torso', -0.13, 0.42, 0.21, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}   # arms folded

for g_ in [('S02', 0.86, 'mec', 'screen'), ('S04', 0.3, 'mec', 'ticket'), ('S08', 0.5, 'mec', 'home'), ('S15', 0.3, 'mec', 'snip'), ('S20', 0.3, 'mec', 'squash'), ('S23', 0.5, 'mec', 'end')]:
    st.gag(*g_)
st.card('S06', 'REFUSÉ', at=0.95)
st.card('S19', 'DOUBLE FILE', at=0.35)

# 1: the hook. At the machine, from the pavement side (review 1: from its blank back it read as a black lectern): the screen, the coin slot and the
#    two big buttons face us; a coin in, then he looks round at us and presses the red button without a look
D1 = st.dur('S01'); FACE1 = -121                  # facing the machine's front: his right profile to us
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', MP, FACE1, 'stand', 'neutral', keys=[k(0.0, look=CARD),
            k(0.06, toon=REACH('R', CARD, 'pinch'), toonDur=0.2, toonEase='out'), k(0.36, look='camera', lookDur=0.16), k(0.36, toon={**REACH('R', [RED[0] + 0.04, RED[1], RED[2]]), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.14, toonEase='inOut'),
            k(0.62, toon={**REACH('R', [RED[0] - 0.005, RED[1], RED[2]]), 'sq': [1.0, 0.985, 1.0], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.05), k(0.85, toon={**REACH('R', [RED[0] + 0.02, RED[1], RED[2]]), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.15)])],
        props=[MTR('pm1', pressAt=[0.62], litAfter=0.62, screens=[[0.62, '1 H']]), CARP('car1'), BAY('bay1'),
               P('piece1', 'coin', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=0.8, keys=[k(0.26, visible=False)])],
        cams=[FC(0.0, [7.45, 1.45, 1.6], [[MP[0], 2.45, MP[2]], [MP[0], 0.0, MP[2]], [METER[0], 2.15, METER[2]], [METER[0], 0.0, METER[2]], [SCREEN[0], SCREEN[1], r(SCREEN[2] - 0.25)]], top=0.12, bottom=0.76, drift=(-0.1, 0.0, 0.1))])
st.cue('sfx:kaching', 'S01', 0.26, 0.2); st.cue('sfx:beep', 'S01', 0.62, 0.25)

# 2: ...his parking for four hundred years. Over his right shoulder (review 1: no shoulder showed), the screen rolls up faster and faster and slams
#    on 400 ANS on « quatre »; his head jolts back; then he leans in on it, a slow blink
D2 = st.dur('S02'); SLAM2 = 0.72
ROLL = [[0.0, '1 H'], [0.2, '1 JOUR'], [0.36, '1 MOIS'], [0.48, '1 AN'], [0.57, '10 ANS'], [0.64, '100 ANS'], [SLAM2, '400 ANS']]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', MP, FACE1, 'stand', 'neutral', keys=[k(0.0, look=SCREEN),
            k(0.0, toon={**REACH('R', [RED[0] + 0.05, RED[1] - 0.03, RED[2]]), 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(SLAM2, toon={**REACH('R', [RED[0] + 0.12, RED[1] - 0.06, RED[2]]), 'lay': [-0.12, 0.0], 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out'),   # the jolt
            k(r(SLAM2 + 0.3), toon={**REACH('R', [RED[0] + 0.12, RED[1] - 0.06, RED[2]]), 'lay': [0.08, 0.0], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.5, toonEase='inOut'),
            k(1.45, toon={**REACH('R', [RED[0] + 0.12, RED[1] - 0.06, RED[2]]), 'lay': [0.08, 0.0], 'face': {'lid': 1.0, 'mouth': 'O'}}, toonDur=0.1), k(1.58, toon={**REACH('R', [RED[0] + 0.12, RED[1] - 0.06, RED[2]]), 'lay': [0.08, 0.0], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.12)])],
        props=[MTR('pm2', litAfter=0.0, screens=ROLL)],
        cams=[FC(0.0, [7.0, 2.2, 3.4], [[SCREEN[0], 1.4, 2.72], [SCREEN[0], 1.4, 3.08], [RED[0], 0.98, 2.72], [GREEN[0], 0.98, 3.08], [6.48, 1.75, 3.14]], top=0.22, bottom=0.86, lenses=range(16, 70), drift=(-0.1, -0.03, -0.04))])
for t_ in [0.2, 0.36, 0.48, 0.57, 0.64]: st.cue('sfx:tick', 'S02', t_, 0.15)
st.cue('sfx:ding', 'S02', SLAM2, 0.4)

# 3: he pressed the wrong button. Close on the two big buttons: his finger still on the lit red 400 ANS beside the green 1 H; it lifts away slowly,
#    hangs, then jerks back (review 1: no finger showed, and the machine's side was black: a warm bounce light on it now)
D3 = st.dur('S03')
F3 = lambda out, y=0.0: REACH('R', [r(RED[0] + out), r(RED[1] + y), RED[2]])
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', MP, FACE1, 'stand', 'neutral', keys=[k(0.0, look=RED), k(0.0, toon=F3(-0.005), toonDur=0.0),
            k(0.25, toon=F3(0.02), toonDur=0.15, toonEase='out'), k(0.95, toon=F3(0.09, 0.02), toonDur=0.65, toonEase='inOut'), k(1.15, toon=F3(0.3, 0.12), toonDur=0.08, toonEase='in')])],   # off the button, slowly... then away
        props=[MTR('pm3', litAfter=0.0, screens=[[0.0, '400 ANS']]), P('rebond3', 'glowLight', pos=[6.25, 1.35, 2.25], opts={'color': '#FFE7C2', 'k': 3.5, 'dist': 2.5})],
        cams=[FC(0.0, [6.25, 0.85, 2.45], [[RED[0], 1.14, RED[2] - 0.1], [GREEN[0], 1.14, GREEN[2] + 0.1], [RED[0], 0.98, RED[2] - 0.1], [GREEN[0], 0.98, GREEN[2] + 0.1], [r(RED[0] + 0.12), 1.06, RED[2]]], top=0.34, bottom=0.62, lenses=range(14, 60), drift=(-0.1, 0.03, -0.05))])

st.cue('sfx:sting', 'S03', 0.3, 0.2)

# 4: the ticket... Low on the pavement: the ticket bursts out of the slot and races along the ground past the lens; he follows it, does a double
#    take back at the machine, and his eyes pop (review 1: it pooled at his feet)
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[act('mec', MP, -160, 'stand', 'neutral', keys=[k(0.0, look=SLOT), k(0.1, look=[6.6, 0.0, 0.6], lookDur=0.1), k(0.32, look=SLOT, lookDur=0.06),
            k(0.1, toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.06, toonEase='out'),
            k(0.4, toon={'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.22, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.93, 1.09, 0.93]}, toonDur=0.05, toonEase='out')])],   # the double take: eyes out
        props=[MTR('pm4', litAfter=0.0, screens=[[0.0, '400 ANS']]), RIB('rib4', **{'from': 0.0, 'rate': 12.0, 'accel': 0.1, 'w': 0.2})],
        cams=[FC(0.0, [7.3, 1.45, 0.9], [[SLOT[0], 0.75, SLOT[2]], [METER[0], 1.6, METER[2]], [6.5, 0.0, 1.2], [6.5, 0.0, 2.4], [MP[0], 2.45, MP[2]]], top=0.12, bottom=0.8, lenses=range(26, 70))])
st.cue('sfx:paper', 'S04', 0.0, 0.5); st.cue('sfx:zip', 'S04', 0.05, 0.3); st.cue('pop', 'S04', 0.4, 0.2)

# 5: ...is three kilometres long. High over the street: the white ticket runs down the pavement to the vanishing point, the man a dot at the machine
D5 = st.dur('S05')
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[act('mec', MP, 180, 'stand', 'neutral', keys=[k(0.0, look=[6.5, 0.0, -30.0])])],
        props=[MTR('pm5', litAfter=0.0, screens=[[0.0, '400 ANS']]), CARP('car5'), BAY('bay5'), RIB('rib5', **{'from': 0.0, 'len0': 8.0, 'rate': 70.0, 'accel': 0.02, 'w': 0.22})],
        cams=[FC(0.0, [8.6, 11.0, 9.0], [[MP[0], 0.0, MP[2]], [MP[0], 2.4, MP[2]], [6.55, 0.0, -45.0], [3.85, 0.0, 2.0]], top=0.1, bottom=0.72, lenses=range(30, 72), drift=(0.0, 0.3, 0.4))])
st.cue('whoosh', 'S05', 0.0, 1.0)

# 6: the town hall refuses to refund him. Over the clerk's shoulder: him at the counter beside the paper roll, taller than he is; the big stamp
#    comes down on his claim (REFUSÉ)
D6 = st.dur('S06'); HIT6 = 0.9; ME6 = [0.3, 0, 1.05]
st.shot('S06', 'mairie', setOpts={'front': 3.6, 'frontSign': {'text': 'ÉTAT CIVIL', 'x': -1.15, 'y': 2.15, 'w': 1.5, 'h': 0.36}, 'map': False}, actors=[   # (review 1) the sign out from under the REFUSÉ card
        act('mec', ME6, 180, 'stand', 'neutral', keys=[k(0.0, look=[-0.3, 1.9, -0.7]), k(r(HIT6 + 0.02), toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [0.94, 1.06, 0.94], 'lay': [-0.08, 0.0]}, toonDur=0.04, toonEase='out'),   # (review 1) a real flinch at the stamp
            k(r(HIT6 + 0.14), toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1), k(1.45, look='camera', lookDur=0.25), k(1.6, toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.3)]),
        act('guichet', [-0.4, 0, -0.75], 10, 'sitWrite', 'neutral', keys=[k(0.0, look=[-0.25, 0.8, -0.15]),
            k(0.45, toon={'reach': {'R': [-0.22, 1.55, -0.3, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'brow': -0.5}}, toonDur=0.3, toonEase='out'),
            k(r(HIT6 - 0.06), toon={'reach': {'R': [-0.22, 0.92, -0.18, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.2, 'brow': -0.7}}, toonDur=0.06, toonEase='in'),
            k(r(HIT6 + 0.35), look=ME6, lookDur=0.2), k(r(HIT6 + 0.45), clip='shakeHead')])],
        props=[P('desk6', 'desk', pos=[0.0, 0, 0.0], opts={'w': 1.6}), P('chaise6', 'chair', pos=[-0.4, 0, -0.75]), P('rouleau6', 'paperRoll', pos=[0.62, 0.76, 0.1], opts={'r': 0.62, 'w': 0.15, 'tail': 0.0}),
               P('tampon6', 'bigStamp', on={'actor': 'guichet', 'hand': 'R', 'offset': [0.0, -0.04, 0.05]}, scale=0.55),
               P('formulaire6', 'paperSheet', pos=[-0.3, 0.77, -0.15], rot=[-PI / 2, 0, 0], opts={'w': 0.3, 'h': 0.4, 'lines': ['REMBOURSEMENT']})],
        cams=[FC(0.0, [0.8, 2.6, -2.3], [[ME6[0], 2.45, ME6[2]], [ME6[0], 1.1, ME6[2]], [0.62, 2.05, 0.1], [-0.22, 0.9, -0.18], [-0.22, 0.55, -0.18]], top=0.14, bottom=0.76, inside=(-4.8, 4.8, 0.3, 3.4, -2.5, 3.4))])
st.cue('thud', 'S06', HIT6, 0.6)

# 7: so he stays parked. Through the windscreen: he sits back in the driver's seat, folds his arms, settles, and looks at us; the ticket on the dash
D7 = st.dur('S07')
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[3.45, 1.8, -6.0]), k(0.2, toon=CROSS, toonDur=0.25, toonEase='out'),
            k(0.55, toon={**CROSS, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.12, toonEase='out'), k(0.75, toon={**CROSS, 'sq': [1.0, 1.0, 1.0], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2),
            k(0.95, look='camera', lookDur=0.3), k(1.3, toon={**CROSS, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.42, toon={**CROSS, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1)])],
        props=[CARP('car7'), BAY('bay7'), MTR('pm7', litAfter=0.0, screens=[[0.0, '400 ANS']]),
               P('tk7', 'signBoard', pos=cw(0.98, 1.0, 0.32), ry=180, opts={'text': '400 ANS', 'bg': '#FFFFFF', 'fg': '#2A4FA0', 'w': 0.34, 'h': 0.13, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [2.7, 1.8, -4.6], [[SEAT[0], 2.15, SEAT[2]], [SEAT[0], 0.9, SEAT[2]], [4.25, 1.0, -0.98], [2.95, 0.9, -1.6]], top=0.16, bottom=0.74, drift=(0.0, 0.0, 0.15))])
st.cue('sfx:carDoor', 'S07', 0.05, 0.4)

# 8: he lives in his car. Three-quarter front: gingham curtains, a stove pipe puffing smoke, a geranium on the roof, an aerial, the BIENVENUE mat,
#    washing strung to the machine; him inside with a cup of coffee; a slow push in
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=[3.45, 1.9, -5.0]),
            k(0.0, toon={'reach': {'R': [3.55, 1.55, -0.55, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.5, toon={'reach': {'R': [3.5, 1.95, -0.35, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.6, 'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'),
            k(0.95, toon={'reach': {'R': [3.55, 1.55, -0.55, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'), k(1.1, look='camera')])],
        props=[CARP('car8'), BAY('bay8'), HOME('home8'), MTR('pm8', screens=[[0.0, '400 ANS']]), P('linge8', 'clothesline', pos=[4.62, 2.0, 1.75], opts={'to': [0.95, -0.15, 1.1], 'n': 4}),
               P('tasse8', 'hotMug', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, scale=0.8)],
        cams=[FC(0.0, [0.3, 2.45, -2.6], [[CAR[0], 3.0, -1.5], [CAR[0], 3.0, 1.6], [2.6, 0.0, -0.05], [5.6, 1.85, 2.9], [SEAT[0], 2.1, SEAT[2]]], top=0.14, bottom=0.78, drift=(0.2, -0.05, 0.15))])

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

# 10: his children grew up... A chalk hopscotch in the bay ahead of the car: one kid hops along it, the other cheers; him at the wheel, proud
D10 = st.dur('S10'); HZ = -2.75; HOPS = [(0.15, 3.05), (0.42, 3.45), (0.69, 3.85), (0.96, 4.25), (1.2, 4.6)]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=[3.8, 1.0, HZ]), k(0.2, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.2)]),
        act('gamin1', [2.65, 0, HZ], 90, 'stand', 'happy', scale=0.72, keys=[k(0.0, look=[4.6, 0.0, HZ]), *[k(r(t0 - 0.12), to=[x, 0, HZ], dur=0.24, arc=0.32, ease='inOut', clip='jump', face='keep') for t0, x in HOPS]]),
        act('gamin2', [2.2, 0, -3.7], 40, 'celebrate', 'happy', scale=0.72, keys=[k(0.0, look=[3.4, 1.2, HZ])])],
        props=[CARP('car10'), BAY('bay10', num=''), HOME('home10', smoke=False), P('marelle10', 'hopscotch', pos=[2.8, 0, HZ], opts={'len': 2.1, 'w': 0.72})],
        cams=[FC(0.0, [3.6, 3.6, -7.0], [[2.65, 1.9, HZ], [4.6, 1.9, HZ], [2.2, 1.9, -3.7], [CAR[0], 2.1, -1.0], [2.2, 0.0, -3.7], [2.8, 0.0, HZ + 0.4]], top=0.14, bottom=0.78, drift=(0.0, -0.1, 0.2))])   # high: the chalk squares read on the ground
for t0, _ in HOPS: st.cue('sfx:stepSoft', 'S10', t0, 0.15)

# 11: ...between two white lines. The kid stands against the machine's side, pencilled heights above earlier ones; his father levels a hand on his head
D11 = st.dur('S11'); KID = [5.52, 0, 2.42]; MARKS = [[0.82, 'LÉO 4 ANS'], [0.94, 'LÉO 5 ANS'], [1.06, 'LÉO 6 ANS'], [1.18, 'LÉO 7 ANS']]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[act('gamin1', KID, 180, 'stand', 'happy', scale=0.72, keys=[k(0.0, look='camera'), k(0.45, toon={'sq': [0.98, 1.03, 0.98]}, toonDur=0.15), k(0.8, toon={'face': {'lid': 0.2, 'mouth': 'grin'}}, toonDur=0.15)]),
        act('mec', [6.2, 0, 2.8], -140, 'stand', 'happy', keys=[k(0.0, look=[5.52, 1.1, 2.42]), k(0.0, toon=REACH('R', [5.55, 1.2, 2.45], 'open'), toonDur=0.0),
            k(0.55, toon=REACH('R', [5.75, 1.22, 2.64], 'pinch'), toonDur=0.15), k(0.8, look='camera', lookDur=0.25)])],
        props=[MTR('pm11', marks=MARKS, screens=[[0.0, '400 ANS']], plaque='PLACE N° 12/DEPUIS 2026'), CARP('car11'), BAY('bay11'), HOME('home11'),
               P('crayon11', 'pen', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, opts={'len': 0.12})],
        cams=[FC(0.0, [5.75, 1.3, -0.3], [[KID[0], 1.45, KID[2]], [KID[0], 0.0, KID[2]], [6.2, 2.45, 2.8], [6.2, 0.0, 2.8], [METER[0], 1.5, 2.66]], top=0.16, bottom=0.74)])

# 12: the postman slips his mail... The postman walks up to the windscreen with a letter and tucks it under the wiper; him inside, watching
D12 = st.dur('S12'); WIPE = cw(1.56, 1.05, -0.38); LETAT = 1.1
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[2.4, 1.9, -2.8]), k(0.9, look=WIPE, lookDur=0.2)]),
        act('facteur', [2.45, 0, 1.0], 180, 'walk', 'happy', keys=[k(0.0, to=[2.6, 0, -1.72], dur=0.8, clip='walk', then='stand', ease='out'), k(0.0, look='camera'), k(0.82, turn=75), k(0.8, look=WIPE),
            k(0.85, toon=REACH('R', [WIPE[0], WIPE[1] + 0.08, WIPE[2] - 0.05], 'pinch'), toonDur=0.2, toonEase='out'), k(1.3, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.1)])],
        props=[CARP('car12'), BAY('bay12'), HOME('home12', letterAt=LETAT), P('lettre12', 'envelope', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, keys=[k(LETAT, visible=False)]),
               P('sac12', 'cardboardBox', on={'actor': 'facteur', 'joint': 'torso', 'offset': [0.24, 0.1, 0.0]}, scale=0.35)],
        cams=[FC(0.0, [2.5, 1.7, -6.2], [[2.45, 2.45, 1.0], [2.6, 2.45, -1.72], [2.6, 0.0, -1.72], [SEAT[0], 2.15, SEAT[2]], [4.75, 0.5, -2.0]], top=0.14, bottom=0.74, drift=(0.15, 0.0, 0.2))])
st.cue('sfx:stepSoft', 'S12', 0.2, 0.15); st.cue('sfx:stepSoft', 'S12', 0.55, 0.15); st.cue('sfx:paper', 'S12', LETAT, 0.3)

# 13: ...under the wiper. Close on the windscreen: the envelope flutters under the wiper; behind the glass he leans in, squints at the address, nods
D13 = st.dur('S13')
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=WIPE), k(0.2, to=[SEAT[0], SEAT[1], r(SEAT[2] - 0.12)], dur=0.3, ease='out', face='keep'),
            k(0.25, toon={'face': {'lid': 0.65, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.15), k(0.8, toon={'face': {'lid': 0.3, 'mouth': 'smile'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.1),
            k(0.95, toon={'face': {'lid': 0.3, 'mouth': 'smile'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.12), k(1.0, look='camera', lookDur=0.2)])],
        props=[CARP('car13'), HOME('home13', letter=True)],
        cams=[FC(0.0, [3.55, 1.5, -2.95], [[WIPE[0], 0.95, WIPE[2]], [WIPE[0], 1.2, WIPE[2]], [SEAT[0], 2.15, SEAT[2] - 0.12], [SEAT[0], 1.6, SEAT[2]]], top=0.18, bottom=0.72, lenses=range(20, 56))])

# 14: every year the mayor... In his sash, the mayor strides to the tricolour ribbon across the front of the bay, the giant scissors up, posing for us
D14 = st.dur('S14'); MAY = [2.35, 0, -3.15]; RIBZ = -3.0
SCI = lambda pid, snip: P(pid, 'bigScissors', on={'actor': 'maire', 'hand': 'R', 'offset': [0, 0, 0.04]}, scale=2.2, opts={'handle': '#D23B32', 'open': 0.5, 'snip': snip})   # (review 1) red rings: black ones read as a blob
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look=MAY), k(0.7, look='camera')]),
        act('maire', [1.45, 0, -1.6], 150, 'walk', 'smug', keys=[k(0.0, to=MAY, dur=0.75, clip='walk', then='stand', ease='out'), k(0.0, look=[3.4, 1.0, RIBZ]), k(0.8, look='camera', lookDur=0.2),
            k(0.85, toon={'reach': {'R': [2.95, 2.75, -3.0, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.2, toonEase='out'),   # (review 1) raised beside his head, not over his face
            k(1.4, toon={'reach': {'R': [2.95, 2.75, -3.0, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=0.06), k(1.52, toon={'reach': {'R': [2.95, 2.75, -3.0, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.08)])],
        props=[CARP('car14'), BAY('bay14'), HOME('home14', smoke=False), P('ruban14', 'ribbonCut', pos=[CAR[0], 0, RIBZ], opts={'w': 2.3, 'h': 0.95, 'tricolor': True}), SCI('sci14', [[0.0, 0.0]]),
               P('sash14', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8})],
        cams=[FC(0.0, [1.9, 1.6, -7.6], [[1.45, 2.45, -1.6], [MAY[0], 2.45, MAY[2]], [5.0, 1.05, RIBZ], [CAR[0], 2.1, -1.2], [MAY[0], 0.0, MAY[2]]], top=0.14, bottom=0.78)])
st.cue('sfx:fanfare', 'S14', 0.2, 0.3)

# 15: ...opens his bay. The snip: the ribbon halves drop, confetti bursts, the mayor beams at us, the man at the wheel waves
D15 = st.dur('S15'); SNIP = 0.3
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'happy', keys=[k(0.0, look='camera'), k(r(SNIP + 0.1), clip='royalWave', params={'freq': 2.2})]),
        act('maire', MAY, 150, 'stand', 'smug', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [2.92, 0.98, RIBZ, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(SNIP, toon={'reach': {'R': [2.92, 0.98, RIBZ, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.2, 'mouth': 'grin'}}, toonDur=0.05)])],
        props=[CARP('car15'), BAY('bay15'), HOME('home15', smoke=False), P('ruban15', 'ribbonCut', pos=[CAR[0], 0, RIBZ], opts={'w': 2.3, 'h': 0.95, 'cutAt': SNIP, 'tricolor': True}),
               SCI('sci15', [[0.0, 1.0], [r(SNIP - 0.04), 1.0], [SNIP, 0.0], [r(SNIP + 0.4), 0.0], [r(SNIP + 0.6), 1.0]]),
               P('sash15', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8}),
               P('conf15', 'confettiRain', pos=[CAR[0], 0.0, -2.6], opts={'w': 3.4, 'h': 3.4, 'd': 1.8, 'n': 170, 'at': SNIP})],
        cams=[FC(0.0, [3.4, 1.05, -5.9], [[2.92, 0.98, RIBZ], [MAY[0], 2.45, MAY[2]], [r(MAY[0] - 0.45), 2.0, MAY[2]], [SEAT[0], 2.15, SEAT[2]], [4.9, 0.98, RIBZ], [MAY[0], 0.0, MAY[2]]], top=0.16, bottom=0.74)])
st.cue('sfx:twang', 'S15', SNIP, 0.4); st.cue('pop', 'S15', r(SNIP + 0.05), 0.3)

# 16: tourists photograph it. A tourist takes a selfie in front of the car, the man waving behind the windscreen; two more flash cameras
D16 = st.dur('S16'); SELF = [4.5, 0, -3.35]
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[4.8, 2.3, -4.1]), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),   # (review 1) no second wave: he poses for the selfie
            k(0.45, toon={'reach': {'R': [r(SEAT[0] + 0.15), 1.95, r(SEAT[2] - 0.45), 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'face': {**DEAD, 'mouth': 'smirk'}}, toonDur=0.15, toonEase='out'), k(1.05, look='camera', lookDur=0.15),
            k(1.25, toon={'reach': {'R': [r(SEAT[0] + 0.15), 1.95, r(SEAT[2] - 0.45), 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'face': {'lid': 1.0, 'mouth': 'smirk'}}, toonDur=0.06), k(1.37, toon={'reach': {'R': [r(SEAT[0] + 0.15), 1.95, r(SEAT[2] - 0.45), 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'face': {**DEAD, 'mouth': 'smirk'}}, toonDur=0.08)]),
        act('touriste1', SELF, 180, 'stand', 'happy', keys=[k(0.0, look=[4.75, 2.25, -4.1]), k(0.0, toon={'reach': {'R': [4.8, 2.3, -4.1, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'grin'}}, toonDur=0.0),
            k(0.9, toon={'reach': {'R': [4.8, 2.3, -4.1, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [0.98, 1.03, 0.98], 'face': {'lid': 0.0, 'mouth': 'grin', 'brow': 0.6}}, toonDur=0.08)]),
        *[act(tid, [tx, 0, tz], try_, 'stand', 'happy', keys=[k(0.0, look=[3.6, 1.8, -0.5]), k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            k(r(fl + 0.02), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.06),
            k(r(fl + 0.2), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15)])
          for tid, tx, tz, try_, fl in [('touriste2', 2.15, -4.5, 25, 0.35), ('touriste3', 5.35, -4.7, -20, 1.0)]]],
        props=[CARP('car16'), BAY('bay16'), HOME('home16', smoke=False), P('tel16', 'handset', on={'actor': 'touriste1', 'hand': 'R', 'offset': [0.0, 0.05, 0.04], 'face': 'camera'}, scale=2.4, opts={'screen': '#8FD3F2'}),   # (review 1) no phone showed
               *[P(f'app16{j}', 'pressCamera', on={'actor': tid, 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': [fl], 'burst': 0.5}) for j, (tid, fl) in enumerate([('touriste2', 0.35), ('touriste3', 1.0)])]],
        cams=[FC(0.0, [3.0, 1.6, -11.5], [[SELF[0], 2.45, SELF[2]], [SELF[0], 0.0, SELF[2]], [SEAT[0], 2.15, SEAT[2]], [CAR[0], 2.1, -0.6], [2.15, 2.4, -4.5], [5.35, 2.4, -4.7]], top=0.14, bottom=0.78, lenses=range(14, 34))])
st.cue('sfx:shutter', 'S16', 0.35, 0.3); st.cue('sfx:shutter', 'S16', 0.9, 0.3); st.cue('sfx:shutter', 'S16', 1.0, 0.3)

# 17: yesterday a delivery van... Down the road the van comes on fast and stops dead alongside his car (review 1: it eased to a stop): the nose
#     pitches down hard, the rear lifts, two rocks to rest; the driver lurches; its hazard lights start blinking
D17 = st.dur('S17'); STOP17 = 1.3; V0 = [VAN[0], 0, 16.0]; VNEAR = [VAN[0], 0, r(VAN[2] + 1.0)]
VKEYS = lambda a, b: [k(0.0, to=a, dur=r(STOP17 - 0.1), ease='linear'), k(r(STOP17 - 0.1), to=b, dur=0.1, ease='out')]
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[1.6, 1.8, 8.0]), k(0.8, look=[1.6, 1.8, 2.0], lookDur=0.3), k(1.35, look=[2.3, 1.9, 0.0], lookDur=0.1),
            k(1.35, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.06, toonEase='out')]),
        act('livreur', vw(1.15, 0.5, -0.45, V0), 180, 'drive', 'neutral', keys=[*VKEYS(vw(1.15, 0.5, -0.45, VNEAR), VSEAT), k(0.0, look=[1.15, 1.8, -8.0]),
            k(STOP17, toon={'lay': [0.35, 0.0], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O'}}, toonDur=0.06, toonEase='out'), k(r(STOP17 + 0.22), toon={'lay': [-0.06, 0.0], 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.15)])],   # the lurch
        props=[CARP('car17'), BAY('bay17'), HOME('home17', smoke=False), VANP('van17', V0, brakeAt=r(STOP17 - 0.04), brakeAmp=2.6, hazardFrom=r(STOP17 + 0.15), keys=VKEYS(VNEAR, VAN))],
        cams=[FC(0.0, [-1.6, 1.7, -7.8], [[VAN[0], 2.8, VAN[2]], [VAN[0], 0.0, VAN[2] + 2.6], [CAR[0], 2.1, -2.0], [CAR[0], 0.0, -2.0], [VAN[0], 2.8, 9.0]], top=0.14, bottom=0.78)])
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
#     the top, the van alongside, hazards blinking slowly, two cars stuck behind it, each hopping on its honk (TÛT !)
D19 = st.dur('S19'); C19A, C19B = 5.8, 10.0; Z19 = 5.15
HOP = lambda x, z, t0: [k(t0, to=[x, 0.22, z], dur=0.06, ease='out'), k(r(t0 + 0.06), to=[x, 0.0, z], dur=0.09, ease='in')]
st.shot('S19', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[3.45, 1.8, -5.0])]), act('livreur', VSEAT, 180, 'drive', 'neutral', keys=[k(0.0, look=[1.15, 1.8, -5.0])])],
        props=[CARP('car19'), BAY('bay19'), HOME('home19', mat=False), VANP('van19', hazardFrom=0.0, hazardRate=1.0),
               P('bouchon19a', 'car', pos=[1.6, 0, C19A], ry=90, opts={'color': '#3A7BC8', 'plate': 'GH-123-JK'}, keys=[*HOP(1.6, C19A, 0.15), *HOP(1.6, C19A, 0.75)]),
               P('bouchon19b', 'car', pos=[1.6, 0, C19B], ry=90, opts={'color': '#E8C547', 'plate': 'LM-456-NP'}, keys=[*HOP(1.6, C19B, 0.45), *HOP(1.6, C19B, 0.95)]),
               P('tut19a', 'hicBurst', pos=[3.0, 2.5, C19A], face='camera', opts={'at': [0.15, 0.75], 'w': 1.7, 'text': 'TÛT !', 'inner': 0.76, 'fit': 0.6, 'hold': 0.25, 'bold': True}),
               P('tut19b', 'hicBurst', pos=[0.2, 2.5, C19B], face='camera', opts={'at': [0.45, 0.95], 'w': 1.7, 'text': 'TÛT !', 'inner': 0.76, 'fit': 0.6, 'hold': 0.25, 'bold': True})],
        cams=[cam(0.0, [2.6, 32.0, r(Z19 + 0.3)], [2.6, 31.5, r(Z19 + 0.1)], [2.6, 0.0, Z19], [2.6, 0.0, r(Z19 - 0.1)], lens=48)])
st.cue('sfx:honkLong', 'S19', 0.15, 0.4); st.cue('sfx:honk', 'S19', 0.45, 0.3); st.cue('sfx:honk', 'S19', 0.75, 0.3); st.cue('sfx:honkLong', 'S19', 0.95, 0.3)

# 20: he can't get out. From inside the van's cab, across the gap: his face mashed flat against his window (wide and shallow), then dragged slowly
#     down the glass, squeaking, the face stretching up it, his hands sliding after; at the sill it pops back up, hair on end (review 1: the head bobbed
#     instead of sliding: no more root move, the slide is a squash of the body)
D20 = st.dur('S20'); SLIDE0, SLIDE1 = 0.25, 1.05
FLAT = lambda w=1.5, h=1.05: {'scl': {'head': [w, h, 0.35]}}
GLASS = lambda y, f, sq=None, w=1.5, h=1.05: {**FLAT(w, h), 'reach': {'R': [3.0, r(y), -0.38, 1, 0.04], 'L': [3.0, r(y + 0.05), 0.28, 1, 0.04]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'face': f, **({'sq': sq} if sq else {})}
st.shot('S20', 'parisStreet', setOpts=STREET, actors=[act('mec', [r(SEAT[0] - 0.1), SEAT[1], SEAT[2]], -90, 'drive', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon=GLASS(2.1, {'lid': 0.6, 'mouth': 'O'}, [1.04, 0.97, 1.04]), toonDur=0.0),
            k(0.08, toon=GLASS(2.1, {'lid': 0.75, 'mouth': 'O'}, [1.06, 0.95, 1.06], 1.6, 1.0), toonDur=0.06, toonEase='out'),   # mashed on the glass
            k(SLIDE1, toon=GLASS(1.72, {'lid': 0.8, 'mouth': 'O'}, [1.08, 0.8, 1.08], 1.4, 1.25), toonDur=r(SLIDE1 - SLIDE0), toonEase='in'),   # dragged down, the face stretching up
            k(r(SLIDE1 + 0.12), toon={'reach': {'R': [3.0, 2.0, -0.38, 1, 0.04], 'L': [3.0, 2.05, 0.28, 1, 0.04]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'sq': [0.93, 1.1, 0.93], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.06, toonEase='out'),   # pops back
            k(r(SLIDE1 + 0.3), toon={'reach': {'R': [3.0, 2.0, -0.38, 1, 0.04], 'L': [3.0, 2.05, 0.28, 1, 0.04]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'hairUp': 1.0, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.1)])],
        props=[CARP('car20'), VANP('van20', hazardFrom=0.0, hazardRate=1.0), P('vitre20', 'slab', pos=[2.975, 1.85, -0.05], opts={'w': 0.012, 'h': 0.95, 'd': 1.3, 'color': '#D8EEF8', 'opacity': 0.24}),
               P('reflet20', 'slab', pos=[2.965, 2.05, 0.3], rot=[0.6, 0, 0], opts={'w': 0.004, 'h': 0.55, 'd': 0.05, 'color': '#FFFFFF', 'opacity': 0.55})],
        cams=[FC(0.0, [2.3, 1.95, 0.05], [[3.05, 2.25, -0.05], [3.05, 1.45, -0.05], [3.0, 2.0, 0.35], [3.0, 2.0, -0.45]], top=0.22, bottom=0.74, lenses=range(24, 64))])
st.cue('sfx:bonk', 'S20', 0.08, 0.3); st.cue('sfx:squeak', 'S20', SLIDE0, r(SLIDE1 - SLIDE0)); st.cue('pop', 'S20', r(SLIDE1 + 0.12), 0.2)

# 21: the delivery man paid... At the machine, from the pavement side like 1 (review 1: from its back), the button reading 500 ANS now: with a smug
#     look at us he winds up, and presses the red button on purpose, hard
D21 = st.dur('S21'); LP = [6.3, 0, 3.45]; MTR5 = lambda pid, **kw: P(pid, 'horodateur', pos=METER, ry=90, opts={'labels': ['1 H', '500 ANS'], **kw})
st.shot('S21', 'parisStreet', setOpts=STREET, actors=[act('livreur', LP, -121, 'stand', 'smug', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.35, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.25, toon={**REACH('R', [RED[0] + 0.22, RED[1] + 0.12, RED[2]]), 'lay': [-0.06, 0.0], 'face': {'lid': 0.35, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.18, toonEase='out'),   # the wind-up
            k(0.6, toon={**REACH('R', [RED[0] - 0.005, RED[1], RED[2]]), 'lay': [0.06, 0.0], 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.3, 'mouth': 'grin', 'brow': 0.6}}, toonDur=0.05, toonEase='in'), k(0.95, look=SCREEN, lookDur=0.2)])],
        props=[MTR5('pm21', pressAt=[0.6], litAfter=0.6, screens=[[0.6, '1 H']], marks=MARKS, plaque='PLACE N° 12/DEPUIS 2026'), CARP('car21'), VANP('van21', hazardFrom=0.0, hazardRate=1.0)],
        cams=[FC(0.0, [7.45, 1.45, 1.6], [[LP[0], 2.45, LP[2]], [LP[0], 0.0, LP[2]], [METER[0], 2.15, METER[2]], [METER[0], 0.0, METER[2]], [SCREEN[0], SCREEN[1], r(SCREEN[2] - 0.25)]], top=0.12, bottom=0.76, drift=(-0.1, 0.0, 0.1))])
st.cue('sfx:beep', 'S21', 0.6, 0.3)

# 22: ...for five hundred years. Wider on the machine: the screen jumps straight to 500 ANS and the second ticket whips out twice as fast as his,
#     past the delivery man's legs and out of the frame
D22 = st.dur('S22')
st.shot('S22', 'parisStreet', setOpts=STREET, actors=[act('livreur', LP, -121, 'stand', 'smug', keys=[k(0.0, look=SCREEN), k(0.3, look=[6.6, 0.0, 0.8], lookDur=0.1), k(0.4, toon={'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.3, 'mouth': 'grin'}}, toonDur=0.1), k(0.75, look='camera', lookDur=0.15)])],
        props=[MTR5('pm22', litAfter=0.0, screens=[[0.0, '1 H'], [0.12, '50 ANS'], [0.22, '500 ANS']], marks=MARKS, plaque='PLACE N° 12/DEPUIS 2026'),
               RIB('rib22', **{'from': 0.18, 'rate': 24.0, 'accel': 0.06, 'w': 0.2, 'text': '500 ANS', 'color': '#B8322A'})],
        cams=[FC(0.0, [7.05, 1.15, 2.05], [[SCREEN[0], 1.4, 2.7], [SCREEN[0], 1.4, 3.1], [SLOT[0], 0.5, SLOT[2]], [6.5, 0.0, 1.6]], top=0.2, bottom=0.72, lenses=range(20, 60))])
st.cue('sfx:ding', 'S22', 0.22, 0.35); st.cue('sfx:paper', 'S22', 0.2, 0.6); st.cue('whoosh', 'S22', 0.2, 0.3, 0.4, 3000, 800)

# 23: they play cards on Sundays. Front on at window height across the gap (review 1: high, the heads tipped to the tray, a sliver of card): the two
#     of them at their windows, faces up and three-quarter to us, each with a fan of big cards; they slap three cards on a light tray between the
#     windows, looking at each other, a glance down at each slap; then both look at us (a Sunday: no hazards)
D23 = st.dur('S23'); TRAY = [2.79, 1.37, 0.0]; SLAPS = [0.5, 1.1, 1.55]
ME23, LV23 = [SEAT[0], 1.95, SEAT[2]], [VSEAT2[0], 1.9, VSEAT2[2]]
def GLANCES(other, t_end):
    out = [k(0.0, look=other)]
    for t_ in SLAPS: out += [k(r(t_ - 0.05), look=[TRAY[0], 1.4, TRAY[2]], lookDur=0.06), k(r(t_ + 0.22), look=other, lookDur=0.1)]
    return out + [k(t_end, look='camera', lookDur=0.25)]
st.shot('S23', 'parisStreet', setOpts=STREET, actors=[act('mec', SEAT, -158, 'drive', 'neutral', keys=[*GLANCES(LV23, 1.75),   # (stills 5) turned more to us: his face read in profile
            k(0.0, toon={'reach': {'R': [3.05, 1.62, 0.02, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.42, toon={'reach': {'R': [2.9, 1.52, 0.02, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'sq': [1.0, 0.97, 1.0], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08, toonEase='in'),   # slap
            k(0.62, toon={'reach': {'R': [3.1, 1.66, -0.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2),
            k(1.47, toon={'reach': {'R': [2.92, 1.5, 0.0, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'sq': [1.0, 0.97, 1.0], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08, toonEase='in'),   # slap
            k(1.7, toon={'reach': {'R': [3.1, 1.66, -0.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2),
            k(2.1, toon={'reach': {'R': [3.1, 1.66, -0.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(2.24, toon={'reach': {'R': [3.1, 1.66, -0.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12)]),
        act('livreur', VSEAT2, 152, 'drive', 'happy', keys=[*GLANCES(ME23, 1.85),
            k(0.0, toon={'reach': {'R': [2.5, 1.62, 0.0, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(1.02, toon={'reach': {'R': [2.66, 1.52, 0.0, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'sq': [1.0, 0.96, 1.0], 'face': {'lid': 0.2, 'mouth': 'grin'}}, toonDur=0.08, toonEase='in'),   # slap
            k(1.25, toon={'reach': {'R': [2.45, 1.66, -0.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.2),
            k(1.9, toon={'reach': {'R': [2.45, 1.66, -0.05, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.15)])],
        props=[CARP('car23'), BAY('bay23'), HOME('home23'), VANP('van23'), P('fill23', 'glowLight', pos=[3.15, 2.3, -0.75], opts={'color': '#FFF1DC', 'k': 2.5, 'dist': 2.2}), P('cartes23', 'cardTray', pos=TRAY, opts={'w': 0.7, 'd': 0.4, 'slapAt': SLAPS, 'cardScale': 2.0, 'top': '#EADCBE'}),
               P('main23a', 'cardFan', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, 0.02, 0.03], 'face': 'camera'}, opts={'s': 1.1}),
               P('main23b', 'cardFan', on={'actor': 'livreur', 'hand': 'L', 'offset': [0.0, 0.02, 0.03], 'face': 'camera'}, opts={'s': 1.1})],
        cams=[FC(0.0, [2.75, 2.45, -2.6], [[SEAT[0], 2.45, SEAT[2]], [VSEAT2[0], 2.4, VSEAT2[2]], [r(SEAT[0] + 0.2), 1.9, SEAT[2]], [r(VSEAT2[0] - 0.2), 1.9, VSEAT2[2]], [TRAY[0], 1.2, TRAY[2]]], top=0.2, bottom=0.66, drift=(0.0, -0.05, 0.15))])   # (stills 5) higher: the tray's top and the cards on it
st.cue('sfx:clink', 'S23', 0.5, 0.25); st.cue('sfx:clink', 'S23', 1.1, 0.25); st.cue('sfx:clink', 'S23', 1.55, 0.25); st.cue('sfx:bell', 'S23', 0.0, 0.25)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le parcmètre", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
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
