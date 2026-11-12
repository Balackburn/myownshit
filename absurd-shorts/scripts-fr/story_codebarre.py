#!/usr/bin/env python3
"""Le code-barres (story 48, cycle 10 of the cartoon staging): this man fell asleep in a supermarket. An employee stuck a label on him. At the
checkout he beeped. One man: two euros forty-nine. He protested; the manager scanned his barcode: he was indeed in stock. He was put on promotion:
minus fifty per cent. Then vacuum-packed, for freshness. A lady bought him. She brought him back the next day: a manufacturing defect. The
manufacturer recalled him. He went back to his mother's. She asked for a refund.
Staging: every gag treats him as a product: the price gun's clack on his sleeping forehead, the anti-theft gate that flashes red as he walks out,
lying stiff on the conveyor belt under the scanner, the manager's laser on his forehead, the -50 % sticker that shrinks him to half his size with a
bounce, the vacuum pack that sucks in round him and flattens his face against the plastic, carried off under a lady's arm, the returns desk's stamp,
the recall notice on the shop's screen, delivered back to his mother in a cardboard box. Natural look; cycle 10 tools: the audit's occlusion check,
react() for the bystanders, a real contrapposto (idleShift 1.6)."""
from story_kit import *
import math

st = Story('codebarre', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L05', 3), ('S07', 'L06', 0), ('S08', 'L07', 0),
         ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0), ('S14', 'L13', 0)])

def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
SM = {'fr': True}
def FWDV(ry): return (math.sin(math.radians(ry)), math.cos(math.radians(ry)))
def OFF(p, ry, fwd=0.0, rgt=0.0, y=0.0):                           # (pass 2) a point in front of / to the right of someone facing ry
    f = FWDV(ry); r = (-f[1], f[0]); return [round(p[0] + fwd * f[0] + rgt * r[0], 3), y, round(p[2] + fwd * f[1] + rgt * r[1], 3)]
def FOLD(p, ry, extra=None):                                        # (pass 2) arms folded across the chest
    return {'reach': {'L': [*OFF(p, ry, 0.26, 0.13, 1.33), 1, 0.05], 'R': [*OFF(p, ry, 0.24, -0.13, 1.3), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}, **(extra or {})}
LABEL = lambda small=False: P('label', 'barcodeLabel', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.44 if small else 0.36, 0.2]}, opts={'w': 0.1 if small else 0.2, 'h': 0.06 if small else 0.12, 'price': '2,49 €', 'bright': True})   # (pass 2) small=True once he is half size: an attached prop keeps its size, so at half size the full label covered both eyes   # on his forehead from S02 on
HALF = 0.5                                                          # minus fifty per cent: half his size from S08 on
SMALL = {'sq': [HALF, HALF, HALF]}

# 1: the hook. At the foot of the back shelf he sleeps, sitting on the floor against the packets, head on his shoulder; Zs rise
SIT = [0.6, 0, -3.05]
D1 = st.dur('S01')
SLEEP = {'bend': {'neck': [0.25, 0, 0.38, 1, None]}, 'face': {'lid': 1, 'jaw': 0.25}}
st.shot('S01', 'supermarket', setOpts=SM, actors=[
        act('mec', SIT, 0, 'sitFloor', 'neutral', keys=[k(0.0, look=None), k(0.0, toon=SLEEP, toonDur=0.0),
            *[k(round(0.35 + 0.6 * i, 3), toon={**SLEEP, 'sq': [1.03, 0.98, 1.03] if i % 2 == 0 else [0.99, 1.01, 0.99]}, toonDur=0.3, toonEase='inOut') for i in range(3)]])],   # snoring: the chest swells and falls
        props=[P('zz', 'zzz', pos=[SIT[0] + 0.25, 1.55, SIT[2] + 0.1])],
        cams=[FC(0.0, [1.3, 0.75, -0.7], [[SIT[0], 1.75, SIT[2]], [SIT[0], 0.0, SIT[2] + 0.9], [SIT[0] - 0.9, 1.6, -3.65], [SIT[0] + 1.0, 0.5, -3.65]], top=0.14, bottom=0.74, drift=(-0.05, 0, -0.1))])
st.cue('sfx:grunt', 'S01', 0.3, 0.15); st.cue('sfx:sniff', 'S01', 1.0, 0.2)   # a snore

# 2: an employee stuck a label on him. The employee in his red tabard crouches beside him with a price gun: clack, on his forehead; his head squashes; he
#    sleeps on. Then close: the label on his forehead, 2,49 €
D2 = st.dur('S02'); CL2 = round(st.at('S02', 'L02', 4) - 0.04, 3)
FORE = [SIT[0], 1.38, round(SIT[2] + 0.22, 3)]
st.shot('S02', 'supermarket', setOpts=SM, actors=[
        act('mec', SIT, 0, 'sitFloor', 'neutral', keys=[k(0.0, look=None), k(0.0, toon=SLEEP, toonDur=0.0),
            k(CL2, toon={**SLEEP, 'scl': {'head': [1.18, 0.78, 1.18]}, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.02, toonEase='out'),   # clack: the head squashed
            k(round(CL2 + 0.07, 3), toon={**SLEEP, 'scl': {'head': [0.94, 1.08, 0.94]}}, toonDur=0.05), k(round(CL2 + 0.16, 3), toon={**SLEEP, 'face': {'lid': 1, 'jaw': 0.3, 'brow': 0.2}}, toonDur=0.1)]),   # back, and he sleeps on
        act('employe', [round(SIT[0] + 0.85, 3), 0, round(SIT[2] + 0.55, 3)], -120, 'kneel', 'neutral', keys=[k(0.0, look=FORE),
            k(round(CL2 - 0.3, 3), toon={'reach': {'R': [round(FORE[0] + 0.25, 3), 1.45, round(FORE[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.15),
            k(round(CL2 - 0.04, 3), toon={'reach': {'R': [round(FORE[0] + 0.12, 3), 1.4, round(FORE[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.04, toonEase='in'),
            k(round(CL2 + 0.12, 3), toon={'reach': {'R': [round(FORE[0] + 0.32, 3), 1.42, round(FORE[2] + 0.3, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1), k(round(CL2 + 0.3, 3), look='camera')])],
        props=[P('zz', 'zzz', pos=[SIT[0] + 0.25, 1.75, SIT[2] + 0.1]), P('gun', 'priceGun', on={'actor': 'employe', 'hand': 'R', 'offset': [0, 0, 0.04], 'rot': [math.pi, 0, 0]}, scale=1.4, opts={'clackAt': [CL2]}),
               P('label', 'barcodeLabel', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.36, 0.2]}, opts={'w': 0.2, 'h': 0.12, 'price': '2,49 €', 'bright': True}, keys=[k(0.0, visible=False), k(CL2, visible=True)])],
        cams=[FC(0.0, [1.9, 1.1, -0.9], [[SIT[0], 1.8, SIT[2]], [SIT[0], 0.0, SIT[2] + 0.9], [SIT[0] + 0.85, 1.7, SIT[2] + 0.55], [SIT[0] + 0.85, 0.0, SIT[2] + 0.55]], top=0.14, bottom=0.74),
              FC(round(CL2 + 0.3, 3), [round(SIT[0] + 0.15, 3), 1.45, round(SIT[2] + 1.6, 3)], [[SIT[0], 1.72, SIT[2]], [SIT[0], 1.05, SIT[2]], [SIT[0] - 0.35, 1.4, SIT[2]], [SIT[0] + 0.35, 1.4, SIT[2]]], top=0.2, bottom=0.66)])   # close: the label on his forehead
st.cue('clack', 'S02', CL2, 0.45)

# 3: at the checkout he beeped. Waking, he walks out through the anti-theft gate: it flashes red and beeps; he freezes in mid-stride, eyes out on stalks
D3 = st.dur('S03'); BIP3 = round(st.at('S03', 'L03', 5) - 0.03, 3)
GATE = [2.2, 0, 2.0]
st.shot('S03', 'supermarket', setOpts=SM, actors=[
        act('mec', [GATE[0], 0, 0.3], 0, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, to=[GATE[0], 0, round(GATE[2] + 0.1, 3)], dur=BIP3, clip='walk', then='stand', ease='linear', face=0),
            k(round(BIP3 - 0.1, 3), toon={'sq': [1.07, 0.9, 1.07], 'face': {'brow': -0.3, 'lid': 0.4}}, toonDur=0.06, toonEase='in'),   # (pass 2) a squash first...
            k(BIP3, to=[GATE[0], 0.32, round(GATE[2] + 0.16, 3)], dur=0.07, glide=True, ease='out', face=0), k(round(BIP3 + 0.36, 3), to=[GATE[0], 0, round(GATE[2] + 0.2, 3)], dur=0.1, glide=True, ease='in', face=0),   # ...up off the floor, hung there, then down
            k(BIP3, toon={'sq': [0.9, 1.14, 0.9], 'hairUp': 1, 'wind': [0.0, 0.3, -1.0], 'face': {'pop': 0.75, 'popLen': 0.32, 'brow': 1, 'jaw': 0.3}, 'bend': {'legR': [-0.75, 0, 0, 1, None], 'shinR': [0.95, 0, 0, 1, None], 'legL': [0.55, 0, 0, 1, None]},
                          'reach': {'R': [round(GATE[0] - 0.25, 3), 2.2, round(GATE[2] + 0.6, 3), 1, 0.05], 'L': [round(GATE[0] + 0.3, 3), 1.15, round(GATE[2] - 0.25, 3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.03, toonEase='out'),   # frozen in a full stride, arms mid-swing, the tie flying
            k(round(BIP3 + 0.3, 3), toon={'sq': [0.94, 1.08, 0.94], 'hairUp': 0.8, 'wind': [0.0, 0.3, -1.0], 'face': {'pop': 0.7, 'popLen': 0.3, 'brow': 1}, 'bend': {'legR': [-0.75, 0, 0, 1, None], 'shinR': [0.95, 0, 0, 1, None], 'legL': [0.55, 0, 0, 1, None]},
                          'reach': {'R': [round(GATE[0] - 0.25, 3), 2.2, round(GATE[2] + 0.6, 3), 1, 0.05], 'L': [round(GATE[0] + 0.3, 3), 1.15, round(GATE[2] - 0.25, 3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.05),
            k(round(BIP3 + 0.46, 3), toon={'sq': [1.06, 0.93, 1.06], 'face': {'pop': 0.3, 'brow': 0.8}}, toonDur=0.05)]),   # landed
        act('caissiere', [4.45, 0, -0.2], -90, 'stand', 'neutral', keys=[k(0.0, look=[GATE[0], 1.8, GATE[2]]), *react(BIP3, 0.8, look=[GATE[0], 1.8, GATE[2]])])],
        props=[LABEL(), P('gate', 'securityGate', pos=GATE, opts={'gap': 1.15, 'beepAt': [BIP3], 'flash': 0.6, 'glowPosts': True})],
        cams=[FC(0.0, [2.7, 1.2, 6.4], [[GATE[0], 2.5, GATE[2]], [GATE[0], 0.0, round(GATE[2] + 0.1, 3)], [GATE[0] - 0.7, 1.75, GATE[2]], [GATE[0] + 0.7, 1.75, GATE[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.2))])
st.cue('sfx:beep', 'S03', BIP3, 0.45); st.cue('sfx:beep', 'S03', BIP3 + 0.18, 0.4); st.cue('sfx:beep', 'S03', BIP3 + 0.36, 0.35)

# 4: one man: 2,49 €. He lies stiff on the conveyor belt; it carries him to the cashier; she scans his forehead: beep; the customer display: UN HOMME 2,49 €
D4 = st.dur('S04'); SC4 = round(st.at('S04', 'L04', 1) - 0.12, 3)
BELT = [3.6, 0.95, -1.15]
st.shot('S04', 'supermarket', setOpts=SM, actors=[
        act('mec', BELT, 180, 'lieBack', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[BELT[0], BELT[1], round(BELT[2] + 0.45, 3)], dur=round(SC4 + 0.05, 3), glide=True, ease='linear', face='keep'),
            k(0.0, toon={'face': {'lid': 0.35}}, toonDur=0.0), k(SC4, toon={'face': {'lid': 0.0, 'pop': 0.35, 'brow': 0.8}, 'sq': [0.98, 1.02, 0.98]}, toonDur=0.04), k(round(SC4 + 0.2, 3), toon={'face': {'lid': 0.3, 'gy': -0.6, 'brow': 0.5}}, toonDur=0.1), k(round(SC4 + 0.9, 3), toon={'face': {'lid': 1}}, toonDur=0.06), k(round(SC4 + 1.0, 3), toon={'face': {'lid': 0.35}}, toonDur=0.08)]),   # (pass 2) the beep pops his eyes; he looks up at the display; a blink
        act('caissiere', [4.45, 0, -0.1], -90, 'stand', 'neutral', keys=[k(0.0, look=[BELT[0], 1.2, round(BELT[2] + 0.5, 3)]),
            k(round(SC4 - 0.2, 3), toon={'reach': {'R': [4.0, 1.34, round(BELT[2] + 1.25, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.12),   # (pass 2) the scanner swept across his forehead
            k(SC4, toon={'reach': {'R': [3.62, 1.3, round(BELT[2] + 1.38, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.08), k(round(SC4 + 0.14, 3), toon={'reach': {'R': [3.3, 1.34, round(BELT[2] + 1.35, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.08),
            k(round(SC4 + 0.45, 3), toon={'reach': {'R': [4.0, 1.25, round(BELT[2] + 1.3, 3), 1, 0.06]}, 'hands': {'R': 'grip'}, 'face': {'browL': 0.6}}, toonDur=0.15)])],
        props=[LABEL(), P('scanner', 'priceGun', on={'actor': 'caissiere', 'hand': 'R', 'offset': [0, 0, 0.04], 'rot': [math.pi, 0, 0]}, scale=1.3, opts={'color': '#3A3D44', 'clackAt': [SC4]}),
               P('disp', 'lcdScreen', pos=[2.85, 0.93, 0.15], ry=-20, opts={'w': 0.62, 'h': 0.4, 'stand': 0.32, 'pages': [[0.0, ['0,00 €']], [round(SC4 + 0.06, 3), ['UN HOMME', '2,49 €'], {'big': 0.9}]]})],
        cams=[FC(0.0, [3.2, 1.8, 1.9], [[BELT[0], 1.3, round(BELT[2] - 0.2, 3)], [BELT[0], 1.3, round(BELT[2] + 1.45, 3)], [round(BELT[0] - 0.4, 3), 0.95, round(BELT[2] + 0.9, 3)], [round(BELT[0] + 0.45, 3), 1.7, round(BELT[2] + 1.2, 3)], [2.85, 1.55, 0.15]], top=0.18, bottom=0.74)])   # (pass 2) down the belt from the cashier's end: his head and label toward us under the scanner
st.cue('sfx:beep', 'S04', SC4, 0.5)

# 5: he protested. Up beside the till, he rants: arms flailing, red in the face, steam out of his ears
D5 = st.dur('S05'); ME5 = [2.75, 0, -0.5]; RY5 = -12                  # (pass 2) three-quarters to the camera (from behind his ear nothing read)
st.shot('S05', 'supermarket', setOpts=SM, actors=[
        act('mec', ME5, RY5, 'stand', 'angry', keys=[k(0.0, look='camera'), k(0.0, expr='angry'),
            *[k(round(0.0 + 0.13 * i, 3), toon={'reach': {'R': [*OFF(ME5, RY5, 0.15, 0.5 if i % 2 == 0 else 0.35, 2.4 if i % 2 == 0 else 1.95), 1, 0.05], 'L': [*OFF(ME5, RY5, 0.15, -0.38 if i % 2 == 0 else -0.55, 1.9 if i % 2 == 0 else 2.45), 1, 0.05]},
                                                     'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [1.04, 0.97, 1.04] if i % 2 else [0.97, 1.04, 0.97], 'face': {'red': min(1.0, 0.35 + 0.18 * i), 'steam': 1, 'steamInk': 1, 'brow': -0.9, 'jaw': 0.65 if i % 2 else 0.4}}, toonDur=0.07, toonEase='inOut') for i in range(8)]]),   # (pass 2) windmilling, the face ramping to red, inked steam
        act('caissiere', [4.45, 0, -0.1], -90, 'stand', 'neutral', keys=[k(0.0, look=[ME5[0], 1.9, ME5[2]]), *react(0.05, 0.6, kind='wince')])],
        props=[LABEL()],
        cams=[FC(0.0, [round(ME5[0] - 0.4, 3), 1.65, round(ME5[2] + 2.6, 3)], [[ME5[0], 2.7, ME5[2]], [ME5[0], 1.15, ME5[2]], [round(ME5[0] - 0.75, 3), 2.2, ME5[2]], [round(ME5[0] + 0.75, 3), 2.2, ME5[2]]], top=0.12, bottom=0.74, drift=(0.04, 0, -0.08))])   # (pass 2) a medium shot, face to us
st.cue('sfx:jet', 'S05', 0.1, 0.18)   # steam out of his ears

# 6: the manager scanned his barcode. The manager in his tie raises a hand scanner: a red beam on the label: beep; he freezes mid-rant, eyes crossed on it
D6 = st.dur('S06'); SC6 = round(st.at('S06', 'L05', 6) - 0.04, 3)
GER = [round(ME5[0] + 1.25, 3), 0, round(ME5[2] + 0.95, 3)]
FOREH = [round(ME5[0] + 0.2 * 0.866, 3), 2.08, round(ME5[2] + 0.2 * 0.5, 3)]   # (pass 2) on the label at the front of his head (he faces 60)
BEAM0 = [round(GER[0] - 0.62, 3), 1.78, round(GER[2] - 0.45, 3)]          # the scanner's nose in his raised hand
st.shot('S06', 'supermarket', setOpts=SM, actors=[
        act('mec', ME5, 60, 'stand', 'angry', keys=[k(0.0, look=GER), k(0.0, toon={'face': {'red': 1, 'steam': 1, 'steamInk': 1, 'brow': -0.8, 'jaw': 0.5}}, toonDur=0.0),
            k(SC6, toon={'sq': [0.96, 1.05, 0.96], 'face': {'red': 0.6, 'cross': 1, 'tremble': 1, 'brow': 0.9, 'jaw': 0.2}}, toonDur=0.03, toonEase='out'), k(SC6, look=None),   # (pass 2) the eyes cross on the dot, a trembling freeze
            k(round(SC6 + 0.5, 3), toon={'sq': [0.97, 1.04, 0.97], 'face': {'red': 0.4, 'cross': 1, 'tremble': 1, 'brow': 0.9, 'jaw': 0.25}}, toonDur=0.2)]),
        act('gerant', GER, -125, 'stand', 'determined', keys=[k(0.0, look=FOREH),
            k(round(SC6 - 0.25, 3), toon={'reach': {'R': [round(GER[0] - 0.45, 3), 1.7, round(GER[2] - 0.32, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.15, toonEase='out')])],
        props=[LABEL(), P('scan6', 'priceGun', on={'actor': 'gerant', 'hand': 'R', 'offset': [0, 0, 0.04], 'rot': [math.pi, 0, 0]}, scale=1.3, opts={'color': '#3A3D44', 'clackAt': [SC6]}),
               P('beam', 'laserBeam', pos=BEAM0, opts={'vec': [round(FOREH[i] - BEAM0[i], 3) for i in range(3)], 'r': 0.012}, keys=[k(0.0, visible=False), k(SC6, visible=True), k(round(SC6 + 0.3, 3), visible=False)])],
        cams=[FC(0.0, [4.75, 1.95, 1.0], [[ME5[0], 2.65, ME5[2]], [ME5[0], 1.35, ME5[2]], [round(GER[0] - 0.2, 3), 1.9, round(GER[2] - 0.1, 3)], [round(ME5[0] - 0.5, 3), 2.0, ME5[2]]], top=0.12, bottom=0.74, drift=(-0.04, 0, -0.04))])   # (pass 2) over the manager's shoulder: his face, the dot on the label
st.cue('sfx:beep', 'S06', SC6, 0.5)

# 7: he was indeed in stock. The manager shows us his tablet: EN STOCK : 1, the pictogram of a man; he nods, satisfied
D7 = st.dur('S07')
st.shot('S07', 'supermarket', setOpts=SM, actors=[
        act('gerant', GER, -30, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [*OFF(GER, -30, 0.32, 0.36, 1.95), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.0),   # (pass 2) turned to us, the tablet up beside his face
            *[k(round(0.3 + 0.18 * i, 3), toon={'reach': {'R': [*OFF(GER, -30, 0.32, 0.36, 1.95), 1, 0.06]}, 'hands': {'R': 'grip'}, 'bend': {'neck': [0.22 if i % 2 == 0 else -0.05, 0, 0, 1, None]}}, toonDur=0.08) for i in range(4)]]),   # two nods
        act('mec', ME5, 60, 'stand', 'worried', keys=[k(0.0, look=GER)])],
        props=[LABEL(), P('tab', 'lcdScreen', on={'actor': 'gerant', 'hand': 'R', 'offset': [0, 0.02, 0.06], 'face': 'camera'}, opts={'w': 0.46, 'h': 0.32, 'stand': 0, 'dark': False, 'pages': [[0.0, ['EN STOCK : 1', '1 homme', 'rayon 3'], {'face': True, 'big': 0.8}]]})],
        cams=[FC(0.0, [round(GER[0] - 1.2, 3), 1.8, round(GER[2] + 2.0, 3)], [[GER[0], 2.45, GER[2]], [GER[0], 1.35, GER[2]], [*OFF(GER, -30, 0.32, 0.62, 2.15)], [*OFF(GER, -30, 0.32, 0.1, 1.75)]], top=0.14, bottom=0.72)])

# 8: he was put on promotion: minus fifty per cent. The manager slaps a -50 % sticker on his chest; on « cinquante » he shrinks to half his size, a bounce
D8 = st.dur('S08'); SL8 = round(st.at('S08', 'L07', 4) - 0.06, 3); SH8 = round(st.at('S08', 'L07', 6) - 0.04, 3)
CHEST8 = [round(ME5[0] + 0.12, 3), 1.55, round(ME5[2] + 0.2, 3)]
st.shot('S08', 'supermarket', setOpts=SM, actors=[
        act('mec', ME5, 60, 'stand', 'worried', keys=[k(0.0, look=GER), k(SL8, toon={'sq': [1.04, 0.96, 1.04]}, toonDur=0.03), k(round(SL8 + 0.1, 3), toon={}, toonDur=0.08), k(round(SL8 + 0.2, 3), look=[ME5[0], 1.0, ME5[2] + 0.5]), k(round(SL8 + 0.45, 3), to=[ME5[0], 0, round(ME5[2] + 0.01, 3)], dur=0.15, clip='stand', then='stand', face=-28), k(round(SL8 + 0.62, 3), look='camera'),   # (pass 1b) he turns to us: the sticker to the camera
            k(round(SH8 - 0.08, 3), toon={'sq': [1.06, 0.94, 1.06], 'face': {'pop': 0.4, 'brow': 1}}, toonDur=0.06),   # it takes him: a gather
            k(SH8, toon={'sq': [HALF * 0.86, HALF * 1.14, HALF * 0.86], 'face': {'pop': 0.5, 'brow': 1}}, toonDur=0.07, toonEase='in'),   # down to half, stretched by the speed
            k(round(SH8 + 0.07, 3), toon={'sq': [HALF * 1.12, HALF * 0.88, HALF * 1.12], 'face': {'brow': 0.8}}, toonDur=0.05), k(round(SH8 + 0.14, 3), toon={'sq': [HALF * 0.97, HALF * 1.03, HALF * 0.97], 'face': {'brow': 0.6}}, toonDur=0.06),
            k(round(SH8 + 0.24, 3), toon={**SMALL, 'face': {'brow': 0.5, 'lid': 0.3}}, toonDur=0.08), k(round(SH8 + 0.3, 3), look='camera')]),
        act('gerant', GER, -125, 'stand', 'determined', keys=[k(0.0, look=CHEST8), k(round(SL8 - 0.22, 3), toon={'reach': {'R': [round(CHEST8[0] + 0.5, 3), 1.95, round(CHEST8[2] + 0.3, 3), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.15),
            k(round(SL8 - 0.05, 3), toon={'reach': {'R': [round(CHEST8[0] + 0.1, 3), CHEST8[1], round(CHEST8[2] + 0.1, 3), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.05, toonEase='in'),   # slap
            k(round(SL8 + 0.15, 3), toon={}, toonDur=0.15), k(round(SH8 + 0.05, 3), look=[ME5[0], 0.7, ME5[2]]),
            k(round(SH8 + 0.05, 3), toon={'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': {'jaw': 0.75, 'brow': 0.8, 'eye': 0.25}}, toonDur=0.4, toonEase='inOut')])],   # (pass 2) a slow lean over him, the jaw dropping (the eyes-out take was the hero's)
        props=[LABEL(), P('promo', 'starSticker', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.02, 0.12, 0.2]}, opts={'r': 0.2, 'text': '-50 %', 'bright': True}, keys=[k(0.0, visible=False), k(SL8, visible=True), k(SH8, scale=0.55, dur=0.07)])],   # (pass 2) it shrinks with him
        cams=[FC(0.0, [1.3, 1.45, 2.3], [[ME5[0], 2.55, ME5[2]], [ME5[0], 0.0, ME5[2]], [round(GER[0] + 0.15, 3), 2.35, GER[2]], [round(ME5[0] - 0.4, 3), 1.5, ME5[2]]], top=0.2, bottom=0.76, drift=(0.03, -0.06, -0.05)),
              FC(round(SH8 + 0.3, 3), [round(ME5[0] - 0.7, 3), 0.75, round(ME5[2] + 1.8, 3)], [[ME5[0], 1.35, ME5[2]], [ME5[0], 0.0, ME5[2]], [round(ME5[0] - 0.35, 3), 0.7, ME5[2]], [round(ME5[0] + 0.35, 3), 0.7, ME5[2]]], top=0.18, bottom=0.74)])   # (pass 1b) then low and close on the half-size man and his -50 %   # (pass 1b) on him, the manager at the edge: he drops from the top of the frame to the bottom half (the two-shot made him a speck)
st.cue('thud', 'S08', SL8, 0.35); st.cue('sfx:slideDown', 'S08', SH8 - 0.05, 0.4); st.cue('sfx:boing', 'S08', SH8 + 0.07, 0.3)

# 9: then vacuum-packed, for freshness. Half his size in a clear pack: on « vide » the air goes: the plastic sucks in round him, his face squashed flat on it
D9 = st.dur('S09'); VAC9 = round(st.at('S09', 'L08', 2) - 0.08, 3); ME9 = [0.4, 0.45, -2.6]   # (pass 2) on a promo table (on the floor it read as a display case)
PARTS = [[0.24, 0.22, 0.48, 0.16], [0.7, 0.36, 0.44, 0.2], [1.03, 0.2, 0.28, 0.2]]   # (pass 2) the film clings to his legs, his torso with the arms pinned, his head
FLAT9 = {**SMALL, 'scl': {'head': [1.3, 0.95, 0.5]}, 'face': {'puff': 1, 'cheeks': 1, 'lid': 0.0, 'pop': 0.45, 'brow': 0.9}}   # (pass 2) the face pressed on the film: wide, flat, the eyes bulging
st.shot('S09', 'supermarket', setOpts=SM, actors=[
        act('mec', ME9, 0, 'stiffStand', 'worried', keys=[k(0.0, look='camera'), k(0.0, toon={**SMALL, 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.0),
            k(VAC9, toon={**FLAT9, 'sq': [HALF * 0.9, HALF * 1.02, HALF * 0.82]}, toonDur=0.12, toonEase='in'), k(round(VAC9 + 0.45, 3), toon={**FLAT9, 'sq': [HALF * 0.9, HALF * 1.02, HALF * 0.82], 'face': {'puff': 1, 'cheeks': 1, 'lid': 0.8, 'brow': 0.9, 'gx': 0.5}}, toonDur=0.1)])],
        props=[LABEL(True), P('promo', 'starSticker', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.02, 0.12, 0.2]}, opts={'r': 0.11, 'text': '-50 %', 'bright': True}),
               P('podium', 'table', pos=[ME9[0], 0, ME9[2]], opts={'color': '#C8322A', 'legs': '#8E2A22', 'w': 0.8, 'd': 0.6, 'h': 0.45}),
               P('pack', 'vacuumBag', pos=ME9, opts={'w': 0.62, 'h': 1.26, 'd': 0.42, 'labelY': 0.3, 'tray': True, 'parts': PARTS, 'tight': [[0.0, 1.35], [VAC9, 1.35], [round(VAC9 + 0.12, 3), 0.8], [round(VAC9 + 0.2, 3), 0.86]]})],
        cams=[FC(0.0, [round(ME9[0] + 0.45, 3), round(ME9[1] + 0.8, 3), round(ME9[2] + 1.9, 3)], [[ME9[0], round(ME9[1] + 1.32, 3), ME9[2]], [ME9[0], round(ME9[1] - 0.15, 3), ME9[2]], [round(ME9[0] - 0.42, 3), round(ME9[1] + 0.7, 3), ME9[2]], [round(ME9[0] + 0.42, 3), round(ME9[1] + 0.7, 3), ME9[2]]], top=0.14, bottom=0.74, drift=(-0.03, 0, -0.06))])   # (pass 2) closer
st.cue('whoosh', 'S09', VAC9, 0.4, 0.15, 3000, 800); st.cue('sfx:squeak', 'S09', VAC9 + 0.12, 0.3)

# 10: a lady bought him. On the shelf among the products, the lady picks up his pack and tucks it under her arm; she walks off
D10 = st.dur('S10'); TK10 = 0.35; ME10 = [-0.6, 0.9, -3.3]
DAME = [-1.35, 0, -2.45]; PK10 = OFF(DAME, 145, 0.42, 0.0, 0.42)   # (pass 2) the pack held in front of her by its sides (it floated beside her)
st.shot('S10', 'supermarket', setOpts=SM, actors=[
        act('mec', ME10, 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=FLAT9, toonDur=0.0),
            k(TK10, to=PK10, dur=0.3, glide=True, ease='inOut', face='keep')]),
        act('dame', DAME, 145, 'stand', 'neutral', keys=[k(0.0, look=[ME10[0], 1.4, ME10[2]]),
            k(0.1, toon={'reach': {'L': [round(ME10[0] - 0.3, 3), 1.35, round(ME10[2] + 0.2, 3), 1, 0.06], 'R': [round(ME10[0] + 0.3, 3), 1.35, round(ME10[2] + 0.2, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}}, toonDur=0.2),
            k(round(TK10 + 0.3, 3), toon={'reach': {'L': [*OFF(DAME, 145, 0.4, -0.25, 1.1), 1, 0.06], 'R': [*OFF(DAME, 145, 0.4, 0.25, 1.1), 1, 0.06]}, 'hands': {'L': 'flat', 'R': 'flat'}}, toonDur=0.12), k(round(TK10 + 0.4, 3), look='camera')])],
        props=[LABEL(True), P('pack', 'vacuumBag', pos=ME10, opts={'w': 0.62, 'h': 1.26, 'd': 0.42, 'labelY': 0.3, 'parts': PARTS, 'tight': [[0.0, 0.86]]}, keys=[k(TK10, to=PK10, dur=0.3, ease='inOut')])],
        cams=[FC(0.0, [0.9, 1.45, 0.6], [[DAME[0], 2.25, DAME[2]], [DAME[0], 0.0, DAME[2]], [ME10[0], 2.2, ME10[2]], [ME10[0] + 0.5, 0.9, ME10[2]]], top=0.12, bottom=0.74)])   # (first look) the lady at the side of the pack, not in front of it

# 11: she brought him back the next day: a manufacturing defect. The returns desk: she plants the pack on the counter; the clerk stamps it: DÉFAUT
D11 = st.dur('S11'); ST11 = round(st.at('S11', 'L10', 5) - 0.05, 3); DESK = [-1.6, 0, 1.4]; DAME11 = [round(-1.6 + 1.25, 3), 0, round(1.4 + 0.15, 3)]; CLERC11 = [-1.0, 0, 0.65]
TOP11 = [DESK[0], 1.07, round(DESK[2] - 0.3, 3)]
st.shot('S11', 'supermarket', setOpts=SM, actors=[
        act('mec', TOP11, 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=FLAT9, toonDur=0.0), k(ST11, toon={**FLAT9, 'sq': [HALF * 1.12, HALF * 0.72, HALF * 1.12]}, toonDur=0.03),   # (pass 2) squashed like an accordion...
            k(round(ST11 + 0.12, 3), toon={'sq': [HALF * 0.94, HALF * 1.12, HALF * 0.94], 'scl': {'head': [0.92, 1.1, 1.08]}, 'face': {'pop': 0.5, 'brow': 1, 'jaw': 0.3}}, toonDur=0.06, toonEase='out'),   # ...then he pops back up, re-inflated
            k(round(ST11 + 0.24, 3), toon={'sq': [HALF * 1.03, HALF * 0.98, HALF * 1.03], 'face': {'brow': 0.6}}, toonDur=0.06), k(round(ST11 + 0.34, 3), toon={**SMALL, 'face': {'lid': 0.35, 'brow': 0.3}}, toonDur=0.08)]),
        act('dame', DAME11, -110, 'stand', 'unimpressed', keys=[k(0.0, look=[DESK[0], 1.6, DESK[2]]), k(0.0, toon={'reach': {'L': [round(DESK[0] + 0.45, 3), 1.45, round(DESK[2] - 0.2, 3), 1, 0.06]}, 'hands': {'L': 'flat'}}, toonDur=0.0),   # (first look) at the end of the counter, not in front of it
            k(0.35, toon={'face': {'brow': 0.3}}, toonDur=0.14, toonEase='outBack'), k(0.62, toon=FOLD(DAME11, -110, {'sq': [1.0, 1.0, 1.0]}), toonDur=0.2), k(0.62, look='camera'), k(1.4, toon=FOLD(DAME11, -110, {'lay': [0.0, 0.05]}), toonDur=0.4, toonEase='inOut')]),   # (pass 2) she lets go and folds her arms; her weight shifts
        act('clerc', CLERC11, -25, 'stand', 'neutral', keys=[k(0.0, look=[TOP11[0], 1.4, TOP11[2]]),   # (pass 2) beside the pack, facing us (behind it only a sleeve showed)
            k(round(ST11 - 0.3, 3), toon={'reach': {'R': [round(TOP11[0] + 0.3, 3), 2.15, round(TOP11[2] + 0.3, 3), 1, 0.06]}, 'hands': {'R': 'grip'}, 'face': {'brow': -0.4}}, toonDur=0.15),   # the stamp raised high...
            k(round(ST11 - 0.03, 3), toon={'reach': {'R': [round(TOP11[0] + 0.08, 3), 1.42, round(TOP11[2] + 0.3, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.03, toonEase='in'),   # ...slammed
            k(round(ST11 + 0.12, 3), toon={'reach': {'R': [round(TOP11[0] + 0.35, 3), 1.75, round(TOP11[2] + 0.35, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.08), k(round(ST11 + 0.4, 3), toon={}, toonDur=0.2), k(round(ST11 + 0.3, 3), look='camera')])],
        props=[LABEL(True), P('desk', 'serviceDesk', pos=DESK, opts={'text': 'RETOURS', 'sub': 'SERVICE CLIENTS', 'w': 1.8}),
               P('pack', 'vacuumBag', pos=TOP11, opts={'w': 0.62, 'h': 1.26, 'd': 0.42, 'labelY': 0.3, 'parts': PARTS, 'tight': [[0.0, 0.86], [ST11, 0.86], [round(ST11 + 0.03, 3), 0.8], [round(ST11 + 0.12, 3), 1.55], [round(ST11 + 0.24, 3), 1.3], [round(ST11 + 0.36, 3), 1.42]]}),   # (pass 2) the stamp squashes it, then it puffs up loose: the defect
               P('stamp11', 'paperSheet', pos=[TOP11[0], 1.62, round(TOP11[2] + 0.34, 3)], face='camera', opts={'w': 0.66, 'h': 0.36, 'paper': '#FFFFFF', 'bright': True, 'stamp': {'text': 'DÉFAUT DE FABRICATION', 'at': ST11, 'rot': -0.12, 'y': 0.0, 'w': 0.97}},   # (pass 2) a bigger sheet turned to us
                 keys=[k(0.0, visible=False), k(ST11, visible=True)])],
        cams=[FC(0.0, [-2.6, 1.6, 4.0], [[DESK[0], 2.75, round(DESK[2] - 0.45, 3)], [DESK[0], 0.3, DESK[2]], [round(DESK[0] + 1.25, 3), 0.4, round(DESK[2] + 0.15, 3)], [round(DESK[0] - 0.9, 3), 1.6, DESK[2]], [CLERC11[0], 2.3, CLERC11[2]]], top=0.12, bottom=0.74)])   # (first look) from the other end: the pack on the counter, the stamp, the clerk, the lady beyond
st.cue('thud', 'S11', 0.05, 0.3); st.cue('sfx:cuff', 'S11', ST11, 0.45)

# 12: the manufacturer recalled him. The big screen over the aisle: RAPPEL PRODUIT, his pictogram, « retour au fabricant »; the lady looks up, arms folded
D12 = st.dur('S12'); SCR12 = [0.0, 2.95, -3.85]   # (first look) over the shelf, not behind its top
st.shot('S12', 'supermarket', setOpts={**SM, 'signs': []}, actors=[act('dame', [0.9, 0, -2.2], -165, 'stand', 'unimpressed', keys=[k(0.0, look=[SCR12[0], SCR12[1] + 0.3, SCR12[2]]), k(0.32, look='camera'), k(0.32, toon={'face': {'lid': 0.35}}, toonDur=0.08),
            k(0.52, look=[SCR12[0], SCR12[1] + 0.3, SCR12[2]]), k(0.52, toon={'sq': [0.95, 1.06, 0.95], 'face': {'pop': 0.4, 'brow': 1, 'jaw': 0.3}}, toonDur=0.04, toonEase='out'),   # (pass 2) a double take at the screen...
            k(0.75, toon=FOLD([0.9, 0, -2.2], -165, {'face': {'brow': -0.4, 'lid': 0.3}}), toonDur=0.2)])],   # ...and the arms fold
        props=[P('recall', 'lcdScreen', pos=[SCR12[0], 2.3, SCR12[2]], opts={'w': 2.3, 'h': 1.35, 'stand': 0, 'dark': False, 'pages': [[0.0, ['RAPPEL PRODUIT', 'homme, lot unique', 'retour au fabricant'], {'face': True, 'big': 0.9, 'accent': '#C8202A'}]]})],
        cams=[FC(0.0, [0.15, 1.7, 1.2], [[SCR12[0] - 1.2, 3.7, SCR12[2]], [SCR12[0] + 1.2, 3.7, SCR12[2]], [SCR12[0] - 1.2, 2.25, SCR12[2]], [SCR12[0] + 1.2, 2.25, SCR12[2]], [0.9, 0.4, -2.2]], top=0.1, bottom=0.74, drift=(0.0, 0.02, -0.06))])   # (pass 1b) centred on the screen, the lady below it looking up (at the edge the screen was cut and overlapped the PROMOTIONS sign)
st.cue('sfx:ding', 'S12', 0.05, 0.3)

# 13: he went back to his mother's. Her landing: a cardboard box on the mat (RETOUR FABRICANT); the door opens; his mother looks down; he pops up out of it
D13 = st.dur('S13'); OP13 = 0.35; UP13 = 0.75; DOOR = [0.0, 0, -2.9]; BOX = [0.05, 0, round(DOOR[2] + 0.95, 3)]
st.shot('S13', 'whiteVoid', actors=[
        act('mere', [DOOR[0], 0, round(DOOR[2] - 0.4, 3)], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(OP13, to=[DOOR[0], 0, round(DOOR[2] + 0.25, 3)], dur=0.3, clip='walk', then='stand', ease='out', face=0),
            k(round(UP13 - 0.06, 3), toon={'face': {'gy': 0.8, 'lid': 0.3}}, toonDur=0.05), k(round(UP13 + 0.04, 3), look=[BOX[0], 1.1, BOX[2]]), k(round(UP13 + 0.04, 3), toon={'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.1)]),   # (pass 2) her eyes lead her head down to him
        act('mec', [BOX[0], -0.4, BOX[2]], 0, 'stand', 'unimpressed', keys=[k(0.0, toon=SMALL, toonDur=0.0), k(0.0, look='camera'),
            k(UP13, to=[BOX[0], 0.16, BOX[2]], dur=0.06, glide=True, ease='out', face='keep'), k(round(UP13 + 0.1, 3), to=[BOX[0], 0.0, BOX[2]], dur=0.1, glide=True, ease='inOut', face='keep'),   # (pass 2) out like a jack-in-the-box
            k(UP13, toon={'sq': [HALF * 0.78, HALF * 1.4, HALF * 0.78], 'reach': {'L': [round(BOX[0] + 0.36, 3), 1.35, round(BOX[2] + 0.1, 3), 1, 0.05], 'R': [round(BOX[0] - 0.36, 3), 1.35, round(BOX[2] + 0.1, 3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'pop': 0.5, 'brow': 1, 'jaw': 0.4}, 'hairUp': 1}, toonDur=0.06, toonEase='out'),
            k(round(UP13 + 0.1, 3), toon={'sq': [HALF * 1.15, HALF * 0.86, HALF * 1.15], 'reach': {'L': [round(BOX[0] + 0.36, 3), 1.15, round(BOX[2] + 0.1, 3), 1, 0.05], 'R': [round(BOX[0] - 0.36, 3), 1.15, round(BOX[2] + 0.1, 3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'pop': 0.3, 'brow': 1}}, toonDur=0.06),
            k(round(UP13 + 0.18, 3), toon={'sq': [HALF * 0.94, HALF * 1.08, HALF * 0.94], 'reach': {'L': [round(BOX[0] + 0.36, 3), 1.2, round(BOX[2] + 0.1, 3), 1, 0.05], 'R': [round(BOX[0] - 0.36, 3), 1.2, round(BOX[2] + 0.1, 3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'brow': 0.8}}, toonDur=0.06),
            k(round(UP13 + 0.27, 3), toon={'sq': [HALF * 1.03, HALF * 0.98, HALF * 1.03], 'face': {'brow': 0.6}}, toonDur=0.06), k(round(UP13 + 0.36, 3), toon={**SMALL, 'face': {'lid': 0.35}}, toonDur=0.1),
            k(round(UP13 + 0.3, 3), look=[DOOR[0], 1.6, round(DOOR[2] + 0.3, 3)])])],
        props=[P('wall13', 'plainWall', pos=[0.0, 0, round(DOOR[2] - 0.05, 3)], opts={'w': 8.0, 'h': 3.2, 'color': '#E9DCCB'}), P('door13', 'door', pos=[DOOR[0], 0, round(DOOR[2] + 0.02, 3)], opts={'w': 0.95, 'h': 2.15, 'openAt': OP13}),
               P('mat13', 'doormat', pos=[DOOR[0], 0.01, round(DOOR[2] + 0.62, 3)], opts={'text': 'BIENVENUE', 'w': 0.85, 'd': 0.5}),
               P('box13', 'cardboardBox', pos=BOX, scale=1.6, opts={'text': 'RETOUR FABRICANT', 'flapsAt': round(UP13 - 0.02, 3)}), LABEL(True)],
        cams=[FC(0.0, [1.1, 1.0, 1.4], [[DOOR[0] - 0.45, 2.3, DOOR[2]], [BOX[0], 0.05, round(BOX[2] + 0.45, 3)], [DOOR[0] + 0.5, 1.0, DOOR[2]], [BOX[0], 1.3, BOX[2]]], top=0.12, bottom=0.74, drift=(-0.04, 0, -0.06))])
st.cue('sfx:carDoor', 'S13', OP13, 0.25); st.cue('pop', 'S13', UP13 + 0.1, 0.35)

# 14: she asked for a refund. His mother holds the till receipt out to us at arm's length; at her feet, in the box, he looks at us
D14 = st.dur('S14'); RF14 = round(st.at('S14', 'L13', 4) - 0.1, 3)
MERE = [DOOR[0], 0, round(DOOR[2] + 0.25, 3)]
st.shot('S14', 'whiteVoid', actors=[
        act('mere', MERE, 15, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(round(RF14 - 0.2, 3), toon={'reach': {'R': [round(MERE[0] + 0.5, 3), 1.35, round(MERE[2] + 0.55, 3), 1, 0.06]}, 'hands': {'R': 'pinch'}, 'face': {'browL': 0.6}}, toonDur=0.15, toonEase='outBack'),
            k(round(RF14 + 0.6, 3), toon={'reach': {'R': [round(MERE[0] + 0.5, 3), 1.35, round(MERE[2] + 0.55, 3), 1, 0.06]}, 'hands': {'R': 'pinch'}, 'face': {'browL': 0.7, 'lid': 0.3}}, toonDur=0.1)]),
        act('mec', BOX, 0, 'stand', 'unimpressed', keys=[k(0.0, toon=SMALL, toonDur=0.0), k(0.0, look='camera'), k(1.3, toon={**SMALL, 'face': {'lid': 0.4}}, toonDur=0.1), k(1.75, toon={**SMALL, 'face': {'lid': 1}}, toonDur=0.12), k(1.95, toon={**SMALL, 'face': {'lid': 0.4}}, toonDur=0.14)])],   # (pass 2) a slow blink at us
        props=[P('wall14', 'plainWall', pos=[0.0, 0, round(DOOR[2] - 0.05, 3)], opts={'w': 8.0, 'h': 3.2, 'color': '#E9DCCB'}), P('door14', 'door', pos=[DOOR[0], 0, round(DOOR[2] + 0.02, 3)], opts={'w': 0.95, 'h': 2.15, 'open': 1}),   # (pass 2) open from the first frame (it shut across the cut)
               P('mat14', 'doormat', pos=[DOOR[0], 0.01, round(DOOR[2] + 0.62, 3)], opts={'text': 'BIENVENUE', 'w': 0.85, 'd': 0.5}), P('box14', 'cardboardBox', pos=BOX, scale=1.6, opts={'text': 'RETOUR FABRICANT'}), LABEL(True),
               P('ticket', 'paperSheet', on={'actor': 'mere', 'hand': 'R', 'offset': [0, -0.26, 0.05], 'face': 'camera'}, opts={'w': 0.5, 'h': 0.66, 'head': 'TICKET', 'lines': ['1 homme', '2,49 €'], 'lineSize': 0.08, 'lineGap': 0.1, 'lineBold': True, 'paper': '#FFFFFF', 'bright': True, 'stamp': {'text': 'REMBOURSEMENT', 'at': 0.0, 'rot': -0.06, 'y': -0.2, 'w': 0.98}},   # (pass 2) REMBOURSEMENT the biggest line, below her hand
                 keys=[k(0.0, scale=0.01, dur=0.0), k(round(RF14 - 0.1, 3), scale=1.0, dur=0.1, ease='outBack')])],
        cams=[FC(0.0, [0.9, 1.45, 0.95], [[MERE[0], 2.25, MERE[2]], [BOX[0], 0.75, BOX[2]], [round(MERE[0] + 0.5, 3), 1.9, round(MERE[2] + 0.55, 3)], [round(MERE[0] + 0.5, 3), 0.95, round(MERE[2] + 0.55, 3)], [BOX[0], 1.25, BOX[2]]], top=0.12, bottom=0.8, drift=(-0.03, 0, -0.05))])   # (pass 2) closer: the receipt and the faces lead, the box rim cropped
st.cue('sfx:paper', 'S14', RF14 - 0.1, 0.3)
st.card('S08', '-50 %', at=round(SH8, 3))

st.write("Le code-barres", rig='toon', fingers=True, cloth=True, idleShift=1.6, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'employe': {'preset': 'worker', 'seed': 481, 'hat': None, 'facial': 'none', 'suit': '#C8322A', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'caissiere': {'preset': 'madame', 'seed': 482, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'gerant': {'preset': 'fringant', 'seed': 483, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'dame': {'preset': 'madame', 'seed': 484, 'suit': '#4F7F3A', 'hair': 'curly', 'hairColor': '#8A4B2A', 'build': {'width': 0.92, 'headWidth': 1.25}},
    'clerc': {'preset': 'worker', 'seed': 485, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'mere': {'preset': 'mamie', 'seed': 486, 'build': {'width': 0.95, 'headWidth': 1.25}},
})
