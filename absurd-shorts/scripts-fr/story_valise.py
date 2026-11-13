#!/usr/bin/env python3
"""La valise (story 54, cycle 16 of the cartoon staging): this man lost his suitcase at the airport. It went round the world without him. Forty
countries, three hundred flights. The airline gave a loyalty card. To the suitcase. It flies first class. He flies in the hold. Yesterday it came back.
With a little suitcase. He pays the maintenance.
Staging: at the empty carousel a single sock rides past him; he leans in to peek through the rubber flaps, his neck stretching, and a flap slaps him
in the face on the way out; the suitcase takes a selfie under the Eiffel tower, sunbathes on a towel before the pyramids, orbits the Earth; in front of
a departures board running up to 300 its stickers pop on one after another; at the check-in counter his arm stretches out for the gold card the agent
holds out, and she slips it past his hand into the suitcase's luggage tag; the suitcase lounges in a first-class seat with a flute of champagne while
the hostess bows; he sits folded in the hold between the bags, FRAGILE on his forehead, and a bag sliding in on the bank flattens him like a sandwich;
the suitcase rides out through the flaps covered in stickers and he jumps for joy; behind it a little suitcase with a dummy; at home he feeds banknotes
into the little suitcase, its lid snaps shut on his hand and his arm stretches like elastic before it lets go.
Natural look; cycle 16 tools: the near-blocker probe (st.gag(..., joint=...)), the hung camera without its tripod, the new props of props_valise.js."""
from story_kit import *
import math

st = Story('valise', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L02', 6), ('S05', 'L02b', 0), ('S06', 'L02b', 2), ('S07', 'L03', 0),
         ('S08', 'L03', 6), ('S09', 'L04', 0), ('S10', 'L05', 0), ('S11', 'L06', 0), ('S12', 'L07', 0), ('S13', 'L08', 0), ('S14', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(30, 57), **kw):
    # (cycle 16) lenses at most 56 degrees by default: wider, the top of an outdoor frame reached the dark top of the sky (52, S01-S02)
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def FWDV(ry): return (math.sin(math.radians(ry)), math.cos(math.radians(ry)))
def OFF(p, ry, fwd=0.0, rgt=0.0, y=0.0):                           # a point in front of / to the right of someone facing ry
    f = FWDV(ry); rr = (-f[1], f[0]); return [r(p[0] + fwd * f[0] + rgt * rr[0]), y, r(p[2] + fwd * f[1] + rgt * rr[1])]

RED = '#C0392B'                                                       # his suitcase
VAL = lambda pid, **kw: P(pid, 'suitcase', **kw)
HALL = lambda pid, **o: P(pid, 'terminalHall', pos=[0, 0, 0], opts={'w': 14, 'back': -4.2, 'front': 6, 'h': 5, **o})
CAR = [0.0, 0, -1.3]; CR = 1.0; CL = 4.4                              # the carousel: centre, end radius, straight length
CAROPTS = {'len': CL, 'r': CR, 'speed': 0.55, 'number': 3, 'hatchX': 0.6, 'hatchH': 1.9}
BELT = r(0.44 + 0.02)                                                 # the top of the belt
BACKZ = r(CAR[2] - CR)                                                # the back straight: the belt runs -X there, out of the tunnel's flaps
EXITX = r(CAROPTS['hatchX'] - 1.3 / 2 - 0.16)                         # the flap curtain at the tunnel's exit (its -X face)
MEB = [-1.05, 0, -3.0]                                                # his place at the carousel: behind the back straight, facing us across the belt

# 1: the hook. The baggage hall: the carousel turning, empty; he waits behind it, deadpan, facing us across the belt; the flaps lift and a single sock
#    rides out of the tunnel and past him; his eyes follow it; a slow blink. A passenger walks off with his bag at the back
D1 = st.dur('S01')
ME1 = MEB
SOCK0 = [r(EXITX + 0.15), r(BELT + 0.07), BACKZ]
st.shot('S01', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME1, 12, 'stand', 'unimpressed', keys=[k(0.0, look=[EXITX, 0.7, BACKZ]), k(0.35, look=[r(EXITX - 0.25), 0.5, BACKZ]), k(0.75, look=[r(EXITX - 0.55), 0.5, BACKZ]),   # his eyes ride with the sock
            k(0.0, toon={'face': {'lid': 0.45, 'gy': 0.3}, 'hands': {'L': 'rest', 'R': 'rest'}}, toonDur=0.0),
            k(0.66, toon={'face': {'lid': 1.0, 'gy': 0.3}}, toonDur=0.08), k(0.86, toon={'face': {'lid': 0.45, 'gy': 0.3}}, toonDur=0.12)]),   # a slow blink at the sock
        act('passager', [2.6, 0, -3.25], 95, 'stand', 'neutral', keys=[k(0.0, look=[6.0, 1.5, -3.3]), k(0.0, to=[5.2, 0, -3.3], dur=round(D1 + 0.5, 3), clip='walk', then='walk', ease='linear', face='move'),
            k(0.0, toon={'hands': {'L': 'grip'}}, toonDur=0.0)])],   # a passenger walks off with his bag
        props=[HALL('hall1'), P('car1', 'carousel', pos=CAR, opts={**CAROPTS, 'flap': [[0.0, 0.0], [0.05, 0.0], [0.12, 0.3], [0.35, 0.12], [0.6, 0.0]]}),
               P('sock1', 'sockSingle', pos=SOCK0, rot=[r(PI / 2), 0, r(-PI / 2)], scale=1.8, keys=[k(0.0, to=[r(SOCK0[0] - 0.55 * (D1 + 0.4)), SOCK0[1], BACKZ], dur=round(D1 + 0.4, 3), ease='linear')]),   # one sock
               P('bag1p', 'briefcase', on={'actor': 'passager', 'hand': 'L'}, scale=1.3)],
        cams=[FC(0.0, [-1.3, 1.5, 1.2], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.9, ME1[2]], [r(EXITX + 0.5), 2.55, BACKZ], [r(EXITX - 0.75), BELT, BACKZ], [-1.9, 0.5, -0.3]], top=0.1, bottom=0.74, drift=(0.06, 0.0, -0.12))])
st.cue('sfx:beep', 'S01', 0.05, 0.2); st.cue('engine', 'S01', 0.0, 0.08, round(D1, 3))

# 2: his suitcase. He steps to the tunnel's mouth and leans in sideways through the rubber flaps, his neck stretching, to look for it; he pulls out,
#    turns back to us, and a flap swings out and slaps him across the head (the head squashed, the eyes crossed); deadpan, a blink
D2 = st.dur('S02'); IN2 = 0.4; OUT2 = 0.76
ME2 = [r(EXITX - 0.7), 0, r(BACKZ - 0.5)]
PEEK = lambda k_, tw=0.0: {'bend': {'spine': [r(0.15 * k_), 0, r(-0.55 * k_), 1, None], 'neck': [0, r(tw), r(-0.45 * k_), r(1 + 0.45 * k_), None]}, 'hands': {'L': 'rest', 'R': 'rest'}}
st.shot('S02', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME2, 15, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**PEEK(0.0), 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.06, toon={**PEEK(-0.15, -0.3), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.35}}, toonDur=0.1, toonEase='inOut'),           # a little lean the other way first...
            k(0.18, toon={**PEEK(1.0, 1.35), 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.2, toonEase='inOut'),                           # ...then in he goes, sideways, the neck stretching...
            k(IN2, toon={**PEEK(1.08, 1.45), 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.1),                                             # ...the head through the flaps
            k(OUT2, toon={**PEEK(0.2, 0.15), 'sq': [1.0, 1.03, 1.0], 'face': {'lid': 0.45}}, toonDur=0.07, toonEase='out'),               # out again, back to us...
            k(round(OUT2 + 0.07, 3), toon={**PEEK(0.05, -0.25), 'scl': {'head': [0.72, 1.06, 1.12]}, 'lay': [0, -0.1], 'face': {'cross': 0.9, 'lid': 0.2, 'brow': 0.8}}, toonDur=0.033, toonEase='out'),   # ...SLAP
            k(round(OUT2 + 0.17, 3), toon={**PEEK(0.0, 0.08), 'scl': {'head': [1.06, 0.97, 0.98]}, 'face': {'cross': 0.5, 'lid': 0.3}}, toonDur=0.06),
            k(round(OUT2 + 0.27, 3), toon={**PEEK(0.0), 'face': {'lid': 0.45}}, toonDur=0.08), k(round(OUT2 + 0.3, 3), look='camera'),
            k(round(D2 - 0.18, 3), toon={**PEEK(0.0), 'face': {'lid': 1.0}}, toonDur=0.05), k(round(D2 - 0.08, 3), toon={**PEEK(0.0), 'face': {'lid': 0.45}}, toonDur=0.06)])],
        props=[HALL('hall2'), P('car2', 'carousel', pos=CAR, opts={**CAROPTS, 'flap': [[0.0, 0.0], [round(IN2 - 0.1, 3), 0.0], [IN2, -0.5], [round(OUT2 - 0.02, 3), -0.45], [round(OUT2 + 0.06, 3), 0.5], [round(OUT2 + 0.14, 3), -0.18], [round(OUT2 + 0.24, 3), 0.0]]})],
        cams=[FC(0.0, [r(EXITX - 1.2), 1.6, 0.6], [[ME2[0], 2.6, ME2[2]], [ME2[0], 0.8, ME2[2]], [r(EXITX + 0.2), 2.6, BACKZ], [r(EXITX + 0.2), BELT, BACKZ], [r(ME2[0] - 0.5), 1.6, ME2[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:stretch', 'S02', 0.18, 0.2); st.cue('sfx:splat', 'S02', round(OUT2 + 0.07, 3), 0.4); st.cue('sfx:boing', 'S02', round(OUT2 + 0.08, 3), 0.15)

# 3: it went round the world without him. Paris: his red suitcase in sunglasses on the pavement, the Eiffel tower at the end of the street, a selfie
#    stick up from its handle; it hops for the photo; the first sticker pops on: PARIS
D3 = st.dur('S03')
V3 = [0.0, 0, -2.0]
st.shot('S03', 'parisStreet', setOpts={'eiffelStyle': 'v2', 'eiffelX': -3.0, 'eiffelZ': -120}, actors=[],
        props=[VAL('val3', pos=V3, ry=8, scale=1.4, opts={'color': RED, 'shades': True, 'selfie': 0.45, 'stickers': 1, 'stickerTimes': [0.42], 'seed': 0, 'bob': [[0.0, 0.06], [0.3, 0.0]]})],
        cams=[FC(0.0, [0.7, 0.55, 1.6], [[V3[0], 1.95, V3[2]], [V3[0], 0.0, V3[2]], [-3.0, 46.0, -120.0], [r(V3[0] + 0.7), 1.6, V3[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.12))])
st.cue('sfx:click', 'S03', 0.4, 0.3); st.cue('pop', 'S03', 0.42, 0.25)

# 4: the world. Before the pyramids: it sunbathes on its back on a striped towel under a parasol, in sunglasses; LE CAIRE pops on
D4 = st.dur('S04')
V4 = [0.0, 0.03, -1.8]
st.shot('S04', 'savannah', setOpts={'seed': 8}, actors=[],
        props=[P('towel4', 'carpet', pos=[0.0, 0, -1.65], ry=90, opts={'w': 1.5, 'd': 0.75, 'color': '#E8463A', 'inner': '#FFFFFF'}),
               VAL('val4', pos=[0.0, 0.18, -1.3], rot=[r(-PI / 2 + 0.25), 0, 0], scale=1.3, opts={'color': RED, 'shades': True, 'stickers': 2, 'stickerTimes': [-1.0, 0.35], 'seed': 0}),
               P('parasol4', 'parasol', pos=[0.75, 0, -2.2], opts={'openAt': -1.0}),
               P('pyr4a', 'pyramid', pos=[-6.0, 0, -26.0], opts={'base': 13, 'h': 9}), P('pyr4b', 'pyramid', pos=[7.5, 0, -36.0], opts={'base': 18, 'h': 12}), P('pyr4c', 'pyramid', pos=[20.0, 0, -50.0], opts={'base': 10, 'h': 7})],
        cams=[FC(0.0, [1.1, 1.25, 1.2], [[0.0, 0.55, -1.3], [0.0, 0.0, -1.5], [-6.0, 9.0, -26.0], [7.5, 12.0, -36.0], [0.8, 1.9, -2.2]], top=0.1, bottom=0.74, drift=(-0.1, 0.0, -0.1))])
st.cue('pop', 'S04', 0.35, 0.25)

# 5: forty countries. In space: the Earth turning, the suitcase in sunglasses orbiting it like a satellite, a white streak behind it
D5 = st.dur('S05')
ORB = 1.75; EC = [0.0, 0.0, -5.0]
def orbit_keys(t0, dur, a0, a1, n=8):
    ks = []
    for i in range(n):
        a = a0 + (a1 - a0) * (i + 1) / n
        ks.append(k(r(t0 + dur * i / n), to=[r(EC[0] + ORB * math.cos(a)), r(EC[1] + 1.6 + ORB * 0.35 * math.sin(a)), r(EC[2] + ORB * math.sin(a))], dur=r(dur / n), ease='linear'))
    return ks
st.shot('S05', 'spaceDark', actors=[],
        props=[P('earth5', 'earthGlobe', pos=EC, opts={'radius': 1.6, 'spin': 0.5}),
               P('trail5', 'orbitTrail', pos=[EC[0], r(EC[1] + 1.6), EC[2]], opts={'r': ORB, 'tilt': -0.33, 'speed': 0.55}),
               VAL('val5', pos=[r(EC[0] + ORB * math.cos(-0.6)), r(EC[1] + 1.6 + ORB * 0.35 * math.sin(-0.6)), r(EC[2] + ORB * math.sin(-0.6))], scale=0.8, opts={'color': RED, 'shades': True, 'stickers': 4, 'seed': 0},
                   keys=[*orbit_keys(0.0, round(D5 + 0.1, 3), -0.6, 1.9), k(0.0, rotTo=[0.4, 2.4, 0.3], dur=round(D5 + 0.1, 3))])],
        cams=[cam(0.0, [0.0, 2.6, 3.5], [0.0, 2.55, 3.2], [0.0, 1.55, -5.0], [0.0, 1.55, -5.0], lens=44)])
st.cue('whoosh', 'S05', 0.1, 0.3, 0.9, 300, 1400)

# 6: three hundred flights. The departures hall: the board's VOLS counter runs up to 300 while the stickers pop onto the suitcase one after another
D6 = st.dur('S06')
V6 = [0.0, 0, -1.2]; NST6 = 11; ST6 = [round(0.08 + i * (D6 - 0.3) / NST6, 3) for i in range(NST6)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[],
        props=[HALL('hall6', sign='DÉPARTS', signX=-1.9, signY=3.4, signZ=-3.0),
               P('board6', 'flightBoard', pos=[0.35, 1.9, -2.6], scale=1.25, opts={'from': 37, 'to': 300, 't0': 0.0, 't1': round(D6 - 0.2, 3)}),
               VAL('val6', pos=V6, ry=-10, scale=1.35, opts={'color': RED, 'stickers': NST6 + 4, 'stickerTimes': [-1.0] * 4 + ST6, 'seed': 0, 'handle': 1.0})],
        cams=[FC(0.0, [0.9, 1.25, 1.6], [[V6[0], 1.05, V6[2]], [V6[0], 0.0, V6[2]], [-0.9, 2.65, -2.6], [1.6, 1.2, -2.6]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.15))])
for i_, t_ in enumerate(ST6): st.cue('pop', 'S06', t_, 0.12 + 0.01 * (i_ % 3))
st.cue('sfx:ticks', 'S06', 0.0, 0.2)

# 7: the airline gave a loyalty card. The check-in desk (ENREGISTREMENT), from behind the agent's shoulder: she holds out the gold card with a smile;
#    his arm shoots out for it and stretches across the desk; she draws it back a little; his suitcase stands beside him
D7 = st.dur('S07')
AG = [0.15, 0, -2.95]; ME7 = [-0.2, 0, -1.2]; CARD7 = [0.0, 1.45, -2.2]; VS7 = [-0.95, 0.0, -1.35]
REACH7 = lambda x, y, z, s=1.0: {'reach': {'R': [r(x), r(y), r(z), s, 0.05]}, 'hands': {'R': 'spread'}, 'hose': 0.12}
DESK = lambda n: P(f'desk{n}', 'serviceDesk', pos=[-0.1, 0, -2.05], opts={'w': 2.4, 'text': 'ENREGISTREMENT', 'sub': False, 'band': '#1F3A6E', 'color': '#E4E0D6', 'signY': 2.75})
st.shot('S07', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('agent', AG, 0, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec', 'cheat': 0.2}), k(0.0, toon={'reach': {'R': [CARD7[0], CARD7[1], r(CARD7[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.0),
            k(0.62, toon={'reach': {'R': [r(CARD7[0] + 0.12), r(CARD7[1] + 0.06), r(CARD7[2] - 0.32), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.18, toonEase='inOut')]),   # she draws it back a little
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[CARD7[0], CARD7[1], CARD7[2]]), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.25, toon={**REACH7(ME7[0] - 0.1, 1.2, ME7[2] + 0.15), 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.35}}, toonDur=0.1, toonEase='in'),   # the hand back first...
            k(0.4, toon={**REACH7(CARD7[0] - 0.05, CARD7[1], CARD7[2] + 0.12, 1.4), 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.5}}, toonDur=0.08, toonEase='out'),   # ...then shot out, stretching
            k(0.62, toon={**REACH7(CARD7[0] + 0.05, CARD7[1] + 0.04, CARD7[2] - 0.18, 1.6), 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.6}}, toonDur=0.18, toonEase='inOut')])],   # after it
        props=[HALL('hall7', sign=False), DESK('7'), P('card7', 'loyaltyCard', on={'actor': 'agent', 'hand': 'R', 'offset': [0, -0.06, 0.04]}, scale=1.0, opts={'s': 1.1, 'bright': True}),
               VAL('val7', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0})],
        cams=[FC(0.0, [0.9, 1.95, -3.75], [[ME7[0], 2.45, ME7[2]], [ME7[0], 0.9, ME7[2]], [VS7[0], 0.9, VS7[2]], [CARD7[0], CARD7[1], CARD7[2]], [r(AG[0] + 0.3), 2.1, AG[2]]], top=0.1, bottom=0.74, inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8))])
        # over the agent's right shoulder: his face to us across the desk (from his side we saw his back)
st.cue('sfx:stretch', 'S07', 0.4, 0.3)

# 8: a loyalty card. Close on the desk top from the side: the gold card in her fingers, his stretched hand an inch short of it; the card glides away
#    over his fingers toward the suitcase; his hand closes on air
D8 = st.dur('S08')
st.shot('S08', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('agent', AG, 0, 'stand', 'happy', keys=[k(0.0, look=[VS7[0], 1.2, VS7[2]]), k(0.0, toon={'reach': {'R': [r(CARD7[0] + 0.12), r(CARD7[1] + 0.06), r(CARD7[2] - 0.32), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': [r(VS7[0] + 0.3), 1.4, -1.75, 1.35, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0.25, 1, None]}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.5, toonEase='inOut')]),   # over to the suitcase
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[CARD7[0], CARD7[1], CARD7[2]]), k(0.0, toon={**REACH7(CARD7[0] + 0.05, CARD7[1] + 0.04, CARD7[2] - 0.18, 1.6), 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.6}}, toonDur=0.0),
            k(0.32, look=[VS7[0], 1.3, VS7[2]]), k(0.55, toon={**REACH7(CARD7[0] + 0.02, CARD7[1] + 0.03, CARD7[2] - 0.22, 1.6), 'hands': {'R': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.06)])],   # it closes on air
        props=[HALL('hall8', sign=False), DESK('8'), P('card8', 'loyaltyCard', on={'actor': 'agent', 'hand': 'R', 'offset': [0, -0.06, 0.04]}, scale=1.0, opts={'s': 1.1, 'bright': True}),
               VAL('val8', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0})],
        cams=[FC(0.0, [1.35, 1.8, -2.75], [[r(CARD7[0] - 0.35), r(CARD7[1] + 0.3), CARD7[2]], [r(CARD7[0] + 0.25), r(CARD7[1] - 0.25), CARD7[2]], [VS7[0], 1.4, VS7[2]], [ME7[0], 2.35, ME7[2]], [ME7[0], 1.2, ME7[2]]], top=0.12, bottom=0.72, drift=(-0.1, 0.0, 0.0), inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8))])
        # (first look) from behind the desk on the right: the card and his hand over the desk top, his face in three-quarters (from the side it was a profile)
st.cue('sfx:slideUp', 'S08', 0.3, 0.2)

# 9: to the suitcase. Over the agent's shoulder again: she has slipped the card into the suitcase's luggage tag, the gold card swinging on it; his hand
#    still out in the air, deadpan, a slow blink at us
D9 = st.dur('S09'); IN9 = 0.18
st.shot('S09', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('agent', AG, 0, 'stand', 'happy', keys=[k(0.0, look=[VS7[0], 1.2, VS7[2]]), k(0.0, toon={'reach': {'R': [r(VS7[0] + 0.3), 1.4, -1.75, 1.35, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0.25, 1, None]}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.0),
            k(round(IN9 + 0.1, 3), toon={'hands': {'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0}}, toonDur=0.25), k(round(IN9 + 0.2, 3), look={'actor': 'mec', 'cheat': 0.2})]),
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[VS7[0], 1.3, VS7[2]]), k(0.0, toon={**REACH7(CARD7[0] + 0.02, CARD7[1] + 0.03, CARD7[2] - 0.22, 1.6), 'hands': {'R': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.4, look='camera'), k(0.55, toon={**REACH7(CARD7[0] + 0.02, CARD7[1] + 0.03, CARD7[2] - 0.22, 1.6), 'hands': {'R': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 1.0}}, toonDur=0.08),
            k(0.75, toon={**REACH7(CARD7[0] + 0.02, CARD7[1] + 0.03, CARD7[2] - 0.22, 1.6), 'hands': {'R': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.12)])],   # the hand left out, a slow blink at us
        props=[HALL('hall9', sign=False), DESK('9'),
               VAL('val9', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0}, keys=[k(IN9, visible=False)]),
               VAL('val9g', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0, 'tag': 'gold', 'tagSwing': 0.5}, keys=[k(0.0, visible=False), k(IN9, visible=True)]),
               P('card9', 'loyaltyCard', on={'actor': 'agent', 'hand': 'R', 'offset': [0, -0.06, 0.04]}, scale=1.0, opts={'s': 1.1, 'bright': True}, keys=[k(IN9, visible=False)])],
        cams=[FC(0.0, [-0.3, 1.85, -3.7], [[VS7[0], 1.5, VS7[2]], [VS7[0], 0.6, VS7[2]], [ME7[0], 2.4, ME7[2]], [ME7[0], 1.1, ME7[2]], [CARD7[0], 1.5, -2.0]], top=0.12, bottom=0.72, inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8))])
st.cue('sfx:ding', 'S09', IN9, 0.3)

# 10: it flies first class. The cabin: the suitcase lounges in a wide leather seat, a sleep mask pushed up on its brow, the gold tag hanging, a flute of
#     champagne on the armrest; the hostess bows and tops up its glass
D10 = st.dur('S10')
SEAT = [-0.85, 0, 0.4]; HOST = [0.15, 0, 1.05]
st.shot('S10', 'whiteVoid', setOpts={'color': '#DCD6C8'}, actors=[
        act('hotesse', HOST, -120, 'stand', 'happy', keys=[k(0.0, look=[SEAT[0], 1.0, SEAT[2]]), k(0.0, toon={'reach': {'R': [-0.38, 1.0, 0.72, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'smile', 'lid': 0.25}}, toonDur=0.0),
            k(0.15, toon={'reach': {'R': [-0.42, 0.95, 0.68, 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {'mouth': 'smile', 'lid': 0.6}}, toonDur=0.25, toonEase='inOut'),   # a bow as she pours
            k(round(D10 - 0.5, 3), toon={'reach': {'R': [-0.2, 1.05, 0.8, 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': {'mouth': 'smile', 'lid': 0.25}}, toonDur=0.25, toonEase='inOut')])],
        props=[P('cabin10', 'cabinShell', pos=[0, 0, 0], opts={'len': 8, 'half': 1.9}),
               P('seat10', 'firstSeat', pos=SEAT, ry=0), P('seat10b', 'firstSeat', pos=[-0.85, 0, -1.4], ry=0), P('seat10c', 'firstSeat', pos=[0.95, 0, -1.4], ry=0),
               VAL('val10', pos=[SEAT[0], 0.47, r(SEAT[2] - 0.05)], rot=[-0.22, 0, 0], scale=1.0, opts={'color': RED, 'stickers': 15, 'seed': 0, 'shades': 'mask', 'tag': 'gold', 'tagSwing': 0.15}),
               P('flute10', 'flute', pos=[-0.42, 0.59, 0.5], scale=1.6, opts={'level': 0.8})],
        cams=[FC(0.0, [0.75, 1.45, 2.6], [[SEAT[0], 1.75, SEAT[2]], [SEAT[0], 0.3, SEAT[2]], [HOST[0], 2.35, HOST[2]], [-0.42, 0.75, 0.5]], top=0.12, bottom=0.74, drift=(-0.1, 0.0, -0.15))])
st.cue('sfx:pour', 'S10', 0.2, 0.25); st.cue('sfx:jet', 'S10', 0.0, 0.06)

# 11: he flies in the hold. Dark, between the bags: he sits folded with his knees up, FRAGILE stuck on his forehead, under a swinging bulb; the plane
#     banks: a big bag slides in and squashes him flat against the stack, then it slides off and he springs back into shape; deadpan
D11 = st.dur('S11'); HIT11 = 0.62
ME11 = [0.0, 0, -0.6]
st.shot('S11', 'whiteVoid', setOpts={'color': '#20242C'}, actors=[
        act('mec', ME11, 15, 'sitFloor', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'sq': [1.0, 0.92, 1.0], 'face': {'lid': 0.45}}, toonDur=0.0),
            k(round(HIT11 - 0.03, 3), toon={'sq': [1.0, 0.94, 1.0], 'face': {'lid': 0.3, 'brow': 0.3}}, toonDur=0.08),
            k(HIT11, toon={'sq': [0.42, 1.08, 1.25], 'face': {'lid': 0.5, 'cross': 0.4}}, toonDur=0.033, toonEase='out'),                # flattened like a sandwich...
            k(round(HIT11 + 0.32, 3), toon={'sq': [0.45, 1.06, 1.22], 'face': {'lid': 0.5}}, toonDur=0.1),                                 # ...held...
            k(round(HIT11 + 0.45, 3), toon={'sq': [1.15, 0.9, 0.95], 'face': {'lid': 0.45}}, toonDur=0.06, toonEase='outBack'),            # ...and back, past his shape...
            k(round(HIT11 + 0.56, 3), toon={'sq': [0.97, 0.95, 1.0], 'face': {'lid': 0.45}}, toonDur=0.06), k(round(HIT11 + 0.66, 3), toon={'sq': [1.0, 0.92, 1.0], 'face': {'lid': 0.45}}, toonDur=0.08)])],
        props=[P('hold11', 'cargoHold', pos=[0, 0, 0], opts={'len': 6, 'half': 1.6, 'h': 1.7, 'lampX': 0.2, 'lampZ': -0.3, 'swing': 0.35}),
               P('frag11', 'fragileTag', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.07, 0.17]}, scale=0.8, opts={'w': 0.3}),
               VAL('b11a', pos=[-0.95, 0, -0.8], ry=80, scale=1.1, opts={'color': '#2E6FB5', 'stickers': 2, 'seed': 3}), VAL('b11b', pos=[-0.95, 0.75, -0.8], ry=75, scale=1.0, opts={'color': '#3CB371', 'seed': 4}),
               VAL('b11c', pos=[0.8, 0, -1.3], ry=-20, scale=1.15, opts={'color': '#7A7F87', 'seed': 5}), VAL('b11d', pos=[-0.3, 0, -1.6], ry=10, scale=1.25, opts={'color': '#9B59B6', 'seed': 6}),
               VAL('b11e', pos=[1.6, 0, -0.55], ry=-95, scale=1.3, opts={'color': '#F28C28', 'stickers': 3, 'seed': 7},
                   keys=[k(0.25, to=[0.6, 0, -0.55], dur=round(HIT11 - 0.25, 3), ease='in'), k(round(HIT11 + 0.38, 3), to=[1.5, 0, -0.5], dur=0.3, ease='inOut')])],   # the bag that slides in on the bank
        cams=[FC(0.0, [0.55, 1.15, 1.55], [[ME11[0], 1.55, ME11[2]], [ME11[0], 0.0, ME11[2]], [-1.2, 1.2, -0.8], [1.0, 0.9, -0.55]], top=0.14, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:splat', 'S11', HIT11, 0.4); st.cue('sfx:boing', 'S11', round(HIT11 + 0.45, 3), 0.25); st.cue('sfx:jet', 'S11', 0.0, 0.1)

# 12: yesterday it came back. At the carousel, he behind the belt as before: the flaps lift and his red suitcase rides out of the tunnel covered in
#     stickers, the gold card on its tag; he jumps for joy: a crouch, up, held at the top with his arms out, deadpan
D12 = st.dur('S12'); OUT12 = 0.12; JMP = 0.6
ME12 = [-1.15, 0, -3.0]
VR12 = [r(EXITX + 0.25), BELT, BACKZ]
st.shot('S12', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME12, 15, 'stand', 'unimpressed', keys=[k(0.0, look=[EXITX, 1.1, BACKZ]), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            k(round(OUT12 + 0.12, 3), look={'point': [r(EXITX - 0.4), 0.7, BACKZ], 'cheat': 0.3}),
            k(round(JMP - 0.18, 3), toon={'sq': [1.12, 0.85, 1.12], 'face': {'lid': 0.3}, 'autoSq': 0}, toonDur=0.12, toonEase='in'),     # a crouch...
            k(JMP, toon={'sq': [0.9, 1.15, 0.9], 'reach': {'L': [r(ME12[0] + 0.7), 2.55, ME12[2], 1, 0.05], 'R': [r(ME12[0] - 0.7), 2.55, ME12[2], 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'lid': 0.2, 'mouth': 'smile'}, 'autoSq': 0}, toonDur=0.08, toonEase='out'),
            k(round(JMP + 0.42, 3), toon={'sq': [1.08, 0.92, 1.08], 'face': {'lid': 0.4}, 'autoSq': 0}, toonDur=0.06, toonEase='in'),
            k(round(JMP + 0.55, 3), toon={'face': {'lid': 0.45}}, toonDur=0.1),
            k(JMP, to=[ME12[0], 0.62, ME12[2]], dur=0.16, glide=True, ease='out', face='keep'), k(round(JMP + 0.16, 3), to=[ME12[0], 0.66, ME12[2]], dur=0.14, glide=True, ease='inOut', face='keep'),   # up, a hang at the top...
            k(round(JMP + 0.3, 3), to=[ME12[0], 0.0, ME12[2]], dur=0.13, glide=True, ease='in', face='keep')])],   # ...and down
        props=[HALL('hall12'), P('car12', 'carousel', pos=CAR, opts={**CAROPTS, 'flap': [[0.0, 0.0], [round(OUT12 - 0.05, 3), 0.0], [round(OUT12 + 0.1, 3), 0.85], [round(OUT12 + 0.35, 3), 0.7], [round(OUT12 + 0.5, 3), 0.0]]}),
               VAL('val12', pos=VR12, rot=[r(-PI / 2), 0, r(-PI / 2)], scale=1.05, opts={'color': RED, 'stickers': 15, 'seed': 0, 'tag': 'gold', 'tagSwing': 0.3},
                   keys=[k(OUT12, to=[r(VR12[0] - 0.55 * (D12 - OUT12)), BELT, BACKZ], dur=round(D12 - OUT12, 3), ease='linear')])],   # rides out at the belt's speed
        cams=[FC(0.0, [-1.8, 1.25, 2.0], [[ME12[0], 3.25, ME12[2]], [ME12[0], 0.7, ME12[2]], [r(EXITX + 1.0), 2.5, BACKZ], [r(EXITX - 0.5), BELT, BACKZ]], top=0.08, bottom=0.74)])
st.cue('sfx:slideDown', 'S12', OUT12, 0.2); st.cue('sfx:boing', 'S12', JMP, 0.3); st.cue('sfx:fanfare', 'S12', round(JMP + 0.05, 3), 0.15)

# 13: with a little suitcase. Behind it a little pink suitcase with a baby's dummy pops out through the flaps and bumps into the big one; his double
#     take, the jaw dropping
D13 = st.dur('S13'); OUT13 = 0.25
VB13 = [r(VR12[0] - 0.55 * (D12 - OUT12)), BELT, BACKZ]
st.shot('S13', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME12, 15, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [VB13[0], 0.7, BACKZ], 'cheat': 0.3}), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'smile'}}, toonDur=0.0),
            *doubleTake(round(OUT13 + 0.25, 3), [r(EXITX - 0.1), 0.55, BACKZ], back=[VB13[0], 0.7, BACKZ], pop=0.0),
            k(round(OUT13 + 0.82, 3), toon={'face': {'jaw': 1.0, 'lid': 0.0, 'brow': 1.0}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.05, toonEase='out')])],   # the jaw drops
        props=[HALL('hall13'), P('car13', 'carousel', pos=CAR, opts={**CAROPTS, 'flap': [[0.0, 0.0], [round(OUT13 - 0.05, 3), 0.0], [round(OUT13 + 0.06, 3), 0.45], [round(OUT13 + 0.25, 3), 0.3], [round(OUT13 + 0.4, 3), 0.0]]}),
               VAL('val13', pos=VB13, rot=[r(-PI / 2), 0, r(-PI / 2)], scale=1.05, opts={'color': RED, 'stickers': 15, 'seed': 0, 'tag': 'gold', 'tagSwing': 0.2},
                   keys=[k(0.0, to=[r(VB13[0] - 0.55 * D13), BELT, BACKZ], dur=round(D13, 3), ease='linear')]),
               VAL('val13s', pos=[r(EXITX + 0.2), BELT, BACKZ], rot=[r(-PI / 2), 0, r(-PI / 2)], scale=0.42, opts={'color': '#F5A3C0', 'pacifier': True, 'stickers': 1, 'seed': 9},
                   keys=[k(OUT13, to=[r(VB13[0] - 0.55 * (OUT13 + 0.45) + 0.62), BELT, BACKZ], dur=0.45, ease='out'), k(round(OUT13 + 0.45, 3), to=[r(VB13[0] - 0.55 * D13 + 0.6), BELT, BACKZ], dur=round(D13 - OUT13 - 0.45, 3), ease='linear')])],   # out fast, it bumps into the big one
        cams=[FC(0.0, [-1.6, 1.2, 1.4], [[ME12[0], 2.45, ME12[2]], [ME12[0], 1.0, ME12[2]], [r(EXITX + 0.2), 1.5, BACKZ], [r(VB13[0] - 0.4), BELT, BACKZ]], top=0.12, bottom=0.74)])
st.cue('sfx:squeak', 'S13', OUT13, 0.25); st.cue('clack', 'S13', round(OUT13 + 0.45, 3), 0.2); st.cue('sfx:gasp', 'S13', round(OUT13 + 0.82, 3), 0.2)

# 14: he pays the maintenance. At home on the rug: he kneels before the little suitcase lying open like a mouth and feeds it a banknote; the lid snaps
#     shut on his hand; he pulls, his arm stretches like elastic, the little suitcase sliding after it, and lets go: the arm snaps back, the hand empty;
#     deadpan, a blink; the big suitcase stands by with its gold card
D14 = st.dur('S14'); SNAP = 0.62; PULL = 1.0; LET = 1.55
ME14 = [-0.55, 0, -0.55]; SM14 = [0.25, 0.0, -0.15]; YAWM = round(math.atan2(ME14[0] - SM14[0], ME14[2] - SM14[2]), 3)   # its mouth turned to him
LIDO = [[0.0, 1.1], [round(SNAP - 0.05, 3), 1.1], [SNAP, 0.0], [round(PULL + 0.55, 3), 0.0], [round(LET + 0.05, 3), 0.35], [round(LET + 0.25, 3), 0.0]]
HANDIN = [r(SM14[0] - 0.02), 0.13, r(SM14[2] - 0.02)]
TOWARD = lambda d: [r(SM14[0] + (ME14[0] - SM14[0]) * d), 0.0, r(SM14[2] + (ME14[2] - SM14[2]) * d)]
st.shot('S14', 'livingRoom', setOpts={'carpet': False, 'picture': False}, actors=[
        act('mec', ME14, 60, 'kneel', 'unimpressed', keys=[k(0.0, look=[SM14[0], 0.15, SM14[2]]), k(0.0, toon={'reach': {'R': [r(ME14[0] + 0.45), 0.6, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': [*HANDIN, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.25, toonEase='inOut'),   # the banknote into its mouth
            k(SNAP, toon={'reach': {'R': [*HANDIN, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.0, 'brow': 0.6}}, toonDur=0.033, toonEase='out'),   # CHOMP
            k(round(SNAP + 0.18, 3), toon={'reach': {'R': [*HANDIN, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.1), k(round(SNAP + 0.2, 3), look='camera'),   # deadpan, at us
            k(PULL, toon={'reach': {'R': [*TOWARD(0.35)[:1], 0.13, TOWARD(0.35)[2], 1.9, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [-0.35, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'brow': 0.3}}, toonDur=0.4, toonEase='inOut'),   # he pulls back, the arm like elastic
            k(round(PULL + 0.05, 3), look=[SM14[0], 0.15, SM14[2]]),
            k(LET, toon={'reach': {'R': [r(ME14[0] + 0.1), 1.1, r(ME14[2] + 0.3), 1, 0.05]}, 'hands': {'R': 'spread'}, 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'sq': [0.96, 1.04, 0.96], 'face': {'lid': 0.2, 'brow': 0.7}}, toonDur=0.05, toonEase='out'),   # it lets go: snap
            k(round(LET + 0.2, 3), toon={'reach': {'R': [r(ME14[0] + 0.25), 0.85, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45}}, toonDur=0.15),   # the hand empty
            k(round(LET + 0.25, 3), look='camera'), k(round(D14 - 0.42, 3), toon={'reach': {'R': [r(ME14[0] + 0.25), 0.85, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0}}, toonDur=0.07),
            k(round(D14 - 0.25, 3), toon={'reach': {'R': [r(ME14[0] + 0.25), 0.85, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45}}, toonDur=0.1)])],
        props=[VAL('val14s', pos=SM14, rot=[r(-PI / 2), 0, YAWM], scale=0.55, opts={'color': '#F5A3C0', 'pacifier': True, 'stickers': 1, 'seed': 9, 'open': LIDO},
                   keys=[k(PULL, to=TOWARD(0.35), dur=0.4, ease='inOut'), k(LET, to=TOWARD(0.05), dur=0.15, ease='out')]),   # dragged along by the hand it holds
               VAL('val14', pos=[1.0, 0, -0.95], ry=-35, scale=1.15, opts={'color': RED, 'stickers': 15, 'seed': 0, 'tag': 'gold', 'tagSwing': 0.12}),
               P('note14', 'banknote', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.08, 0.02]}, scale=0.7, keys=[k(SNAP, visible=False)])],
        cams=[FC(0.0, [0.35, 1.4, 2.3], [[ME14[0], 2.05, ME14[2]], [ME14[0], 0.0, ME14[2]], [SM14[0], 0.4, SM14[2]], [1.0, 1.2, -0.95], [1.35, 0.2, -0.95]], top=0.12, bottom=0.74, drift=(-0.08, 0.0, -0.12))])
st.cue('sfx:zip', 'S14', 0.3, 0.2); st.cue('clack', 'S14', SNAP, 0.45); st.cue('sfx:stretch', 'S14', PULL, 0.3); st.cue('sfx:twang', 'S14', LET, 0.35); st.cue('sfx:cash', 'S14', round(LET + 0.1, 3), 0.15)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe; (cycle 16) the near-blocker test in front of each
for g_ in [('S01', 0.7, 'mec', 'sock', None), ('S02', round(OUT2 + 0.1, 3), 'mec', 'slap', None), ('S07', 0.55, 'mec', 'reach', None), ('S08', 0.4, 'mec', 'hand', 'handR'),
           ('S09', 0.6, 'mec', 'blink', None), ('S10', 0.6, 'hotesse', 'bow', None), ('S11', round(HIT11 + 0.15, 3), 'mec', 'flat', None), ('S12', round(JMP + 0.2, 3), 'mec', 'jump', None),
           ('S13', round(OUT13 + 0.9, 3), 'mec', 'jaw', None), ('S14', round(PULL + 0.3, 3), 'mec', 'elastic', None), ('S14', round(D14 - 0.3, 3), 'mec', 'end', None)]:
    st.gag(g_[0], g_[1], g_[2], g_[3], joint=g_[4])
for t_ in [('S06', 0.9, 'board6', 'vols'), ('S07', 0.5, 'card7', 'card'), ('S11', 0.4, 'frag11', 'fragile')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S04', 'MONDE')
st.card('S10', 'PREMIÈRE')

st.write("La valise", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'passager': {'preset': 'worker', 'seed': 541, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'agent': {'preset': 'madame', 'seed': 542, 'suit': '#1F3A6E', 'hairColor': '#6B3A1E', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'hotesse': {'preset': 'madame', 'seed': 543, 'suit': '#1F3A6E', 'hair': 'bun', 'hairColor': '#2A2A2E', 'build': {'width': 0.9, 'headWidth': 1.25}},
})
