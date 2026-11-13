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
Natural look; cycle 16 tools: the near-blocker probe (st.gag(..., joint=...)), the hung camera without its tripod, the new props of props_valise.js.
(pass 3) the floppy stocking, the painted eye band, the oversized dummy, the champagne bottle and the filling flute, the two-sided desk sign."""
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
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)} (stopped at a wall: frame tighter or move the camera)')   # (pass 2) S09 went out at 77 degrees, S10 at 68
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def FWDV(ry): return (math.sin(math.radians(ry)), math.cos(math.radians(ry)))
def OFF(p, ry, fwd=0.0, rgt=0.0, y=0.0):                           # a point in front of / to the right of someone facing ry
    f = FWDV(ry); rr = (-f[1], f[0]); return [r(p[0] + fwd * f[0] + rgt * rr[0]), y, r(p[2] + fwd * f[1] + rgt * rr[1])]

RED = '#C0392B'                                                       # his suitcase
VAL = lambda pid, **kw: P(pid, 'suitcase', **kw)
HALL = lambda pid, **o: P(pid, 'terminalHall', pos=[0, 0, 0], opts={'w': 14, 'back': -4.2, 'front': 6, 'h': 5, **o})
CAR = [0.0, 0, -1.3]; CR = 1.0; CL = 4.4                              # the carousel: centre, end radius, straight length
CAROPTS = {'len': CL, 'r': CR, 'speed': 0.55, 'number': 3, 'hatchX': 0.6, 'hatchH': 1.4}   # (check stills 2) at 1.9 the lifted flaps swept across him
BELT = r(0.44 + 0.02)                                                 # the top of the belt
BACKZ = r(CAR[2] - CR)                                                # the back straight: the belt runs -X there, out of the tunnel's flaps
EXITX = r(CAROPTS['hatchX'] - 1.3 / 2 - 0.16)                         # the flap curtain at the tunnel's exit (its -X face)
MEB = [-1.05, 0, -3.0]                                                # his place at the carousel: behind the back straight, facing us across the belt

# 1: the hook. The baggage hall: the carousel turning, empty; he waits behind it, deadpan, facing us across the belt; a single sock rides out of
#    the tunnel and past him; his eyes follow it; a slow blink. A passenger walks off with his bag at the back
# (pass 3) the belt twice as fast and the sock already out at the cut: it rides in front of him by 0.6 s (it crept 28 % of the frame and reached him
# at the cut); a stocking stood up on the belt, its top flopping and wobbling, the toe ahead (the straight striped tube read as a block); the
# passenger crosses behind him, inside the frame (he walked off out of it)
D1 = st.dur('S01')
ME1 = MEB
SPD1 = 1.1
SOCK0 = [r(EXITX - 0.3), r(BELT + 0.35), BACKZ]
SOCKX = lambda t: r(SOCK0[0] - SPD1 * t)
st.shot('S01', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME1, 12, 'stand', 'unimpressed', keys=[k(0.0, look=[r(SOCKX(0.1)), 0.85, BACKZ]), k(0.3, look=[r(SOCKX(0.4)), 0.8, BACKZ]), k(0.6, look=[r(SOCKX(0.7)), 0.8, BACKZ]), k(0.9, look=[r(SOCKX(1.0)), 0.8, BACKZ]),   # his eyes ride with the sock, a beat ahead
            k(0.0, toon={'face': {'lid': 0.45, 'gy': 0.3}, 'hands': {'L': 'rest', 'R': 'rest'}}, toonDur=0.0),
            k(0.66, toon={'face': {'lid': 1.0, 'gy': 0.3}}, toonDur=0.08), k(0.86, toon={'face': {'lid': 0.45, 'gy': 0.3}}, toonDur=0.12)]),   # a slow blink at the sock
        act('passager', [0.45, 0, -3.75], -95, 'stand', 'neutral', keys=[k(0.0, look=[-6.0, 1.5, -3.9]), k(0.0, to=[-1.6, 0, -3.85], dur=round(D1 + 0.5, 3), clip='walk', then='walk', ease='linear', face='move'),
            k(0.0, toon={'hands': {'L': 'grip'}}, toonDur=0.0)])],   # a passenger walks off with his bag, behind him
        props=[HALL('hall1'), P('car1', 'carousel', pos=CAR, opts={**CAROPTS, 'speed': SPD1, 'flap': [[0.0, 0.3], [0.2, 0.12], [0.45, 0.0]]}),
               P('sock1', 'sockL', pos=SOCK0, rot=[0, r(-PI / 2), 0], scale=2.0, opts={'color': '#F4F1E8', 'stripe': '#D7262E', 'flop': -0.55, 'wob': 0.16}, keys=[k(0.0, to=[SOCKX(D1 + 0.1), SOCK0[1], BACKZ], dur=round(D1 + 0.1, 3), ease='linear')]),
               P('bag1p', 'briefcase', on={'actor': 'passager', 'hand': 'L'}, scale=1.3)],
        cams=[FC(0.0, [-0.9, 1.95, 0.4], [[ME1[0], 2.42, ME1[2]], [ME1[0], 1.0, ME1[2]], [r(EXITX + 0.35), 1.6, BACKZ], [SOCKX(1.0), BELT, BACKZ], [r(ME1[0] - 0.5), 1.6, ME1[2]]], top=0.1, bottom=0.74, drift=(0.05, 0.0, -0.1))])
        # (pass 2) closer: his head a fifth of the frame (from the hip up, the tunnel's mouth and the sock beside him)
        # (first look) higher: from 1.5 m the island hid the far belt and the sock on it
st.cue('sfx:beep', 'S01', 0.05, 0.2); st.cue('engine', 'S01', 0.0, 0.08, round(D1, 3))

# 2: his suitcase. He steps to the tunnel's mouth and leans in sideways through the rubber flaps, his neck stretching, to look for it; he pulls out,
#    turns back to us, and a flap swings out and slaps him across the head (the head squashed, the eyes crossed); deadpan, a blink
# (pass 2) bent double at the tunnel's mouth, his head goes in through the flaps (the pin channel puts it there); out again, still bent, a flap swings
# out at his head height: SLAP, the head squashed, the eyes crossed, held, then he straightens up to us
# (pass 3) the head squashed along its own height, half of it (squashed front to back, toward the lens, it did not change size), held clear of the
# flaps; the whole gag 0.06 s earlier: ten frames of deadpan after it (two)
D2 = st.dur('S02'); IN2 = 0.3; OUT2 = 0.5; HIT2 = round(OUT2 + 0.06, 3)
TW2 = -1.2                                                                # (pass 2b) the neck twisted toward the lens as he comes out: the slap lands on his face (it faced away, 105 degrees)
ME2 = [r(EXITX - 0.88), 0, r(BACKZ - 0.42)]
INTUN = [r(EXITX + 0.14), 1.0, r(BACKZ - 0.05)]                            # his head through the flaps, inside the mouth of the tunnel
OUTH = [r(EXITX - 0.22), 1.08, r(BACKZ - 0.12)]                           # his head just out of the flaps, still bent: where the flap swings
BENT = lambda bx, st_=1.0, tw=0.0: {'bend': {'spine': [r(bx), 0, 0, 1, None], 'neck': [r(0.35 * bx), 0, r(tw), r(st_), None]}, 'hands': {'L': 'rest', 'R': 'rest'}}
HD = [0.0, 0.25, 0.0]                                                     # the middle of his head, in the frame of the head
st.shot('S02', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME2, 75, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BENT(0.0), 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.05, toon={**BENT(-0.15), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.35}}, toonDur=0.09, toonEase='inOut'),                    # a little lean back first...
            k(0.14, toon={**BENT(1.25, 1.9), 'pin': {'joint': 'head', 'off': HD, 'at': INTUN, 'w': 1}, 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.16, toonEase='inOut'),   # ...then in he goes, bent double, the neck stretching...
            k(IN2, toon={**BENT(1.3, 2.0), 'pin': {'joint': 'head', 'off': HD, 'at': [r(INTUN[0] + 0.06), INTUN[1], INTUN[2]], 'w': 1}, 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.14),   # ...the head inside, looking
            k(round(OUT2 - 0.06, 3), toon={**BENT(1.2, 1.6, TW2), 'pin': {'joint': 'head', 'off': HD, 'at': OUTH, 'w': 1}, 'face': {'lid': 0.45}}, toonDur=0.06, toonEase='out'),   # out again, still bent...
            k(HIT2, toon={**BENT(1.15, 1.3, TW2), 'pin': {'joint': 'head', 'off': HD, 'at': [r(OUTH[0] - 0.12), OUTH[1], OUTH[2]], 'w': 1}, 'scl': {'head': [1.35, 0.5, 1.3]}, 'lay': [0.0, 0.08], 'face': {'cross': 1.0, 'lid': 0.15, 'brow': 0.9}}, toonDur=0.033, toonEase='out'),   # ...SLAP: squashed to half its height
            k(round(HIT2 + 0.22, 3), toon={**BENT(1.1, 1.2, TW2), 'pin': {'joint': 'head', 'off': HD, 'at': [r(OUTH[0] - 0.26), OUTH[1], OUTH[2]], 'w': 1}, 'scl': {'head': [1.3, 0.55, 1.25]}, 'face': {'cross': 1.0, 'lid': 0.2, 'brow': 0.8}}, toonDur=0.2),   # held, cross-eyed, out of the flaps...
            k(round(HIT2 + 0.28, 3), toon={**BENT(0.0), 'scl': {'head': [0.94, 1.08, 0.98]}, 'face': {'cross': 0.6, 'lid': 0.35}}, toonDur=0.12, toonEase='out'),   # ...he straightens up, the head popping back...
            k(round(HIT2 + 0.28, 3), face=10, turn=0.14), k(round(HIT2 + 0.3, 3), look='camera'),
            k(round(HIT2 + 0.42, 3), toon={**BENT(0.0), 'face': {'cross': 0.0, 'lid': 0.45}}, toonDur=0.1),
            k(round(D2 - 0.16, 3), toon={**BENT(0.0), 'face': {'lid': 1.0}}, toonDur=0.05), k(round(D2 - 0.07, 3), toon={**BENT(0.0), 'face': {'lid': 0.45}}, toonDur=0.06)])],   # ...deadpan, a blink
        props=[HALL('hall2'), P('car2', 'carousel', pos=CAR, opts={**CAROPTS, 'flap': [[0.0, 0.0], [0.14, 0.0], [IN2, -0.5], [round(OUT2 - 0.06, 3), -0.45], [round(OUT2, 3), 0.0], [HIT2, 0.62], [round(HIT2 + 0.1, 3), -0.2], [round(HIT2 + 0.22, 3), 0.1], [round(HIT2 + 0.34, 3), 0.0]]})],
        cams=[FC(0.0, [r(EXITX - 1.45), 1.65, 0.45], [[ME2[0], 2.45, ME2[2]], [ME2[0], 0.4, ME2[2]], [r(EXITX + 0.25), 1.45, BACKZ], [r(EXITX + 0.25), BELT, BACKZ], [r(ME2[0] - 0.45), 1.6, ME2[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:stretch', 'S02', 0.14, 0.2); st.cue('sfx:splat', 'S02', HIT2, 0.45); st.cue('sfx:boing', 'S02', round(HIT2 + 0.3, 3), 0.2)

# 3: it went round the world without him. Paris: his red suitcase in sunglasses on the pavement, the Eiffel tower at the end of the street, a selfie
#    stick up from its handle; it hops for the photo; the first sticker pops on: PARIS
D3 = st.dur('S03')
V3 = [0.0, 0, -2.0]
st.shot('S03', 'parisStreet', setOpts={'eiffelStyle': 'v2', 'eiffelX': -3.0, 'eiffelZ': -120}, actors=[],
        props=[VAL('val3', pos=V3, ry=8, scale=1.4, opts={'color': RED, 'shades': True, 'selfie': 0.45, 'stickers': 1, 'stickerTimes': [0.42], 'seed': 0},
                   keys=[k(0.1, squash=[1.12, 0.86, 1.12], dur=0.1), k(0.16, to=[V3[0], 0.16, V3[2]], dur=0.11, ease='out'), k(0.27, to=[V3[0], 0.0, V3[2]], dur=0.1, ease='in'), k(0.37, squash=[1.16, 0.84, 1.16], dur=0.28)])],
               # (pass 2) a real hop for the photo: a crouch, air under the wheels, a squash on landing (it rose 3 px)
        fx=[{'type': 'flash', 'at': 0.38, 'dur': 0.08}],   # (pass 3) the selfie's flash (the click had no picture)
        cams=[FC(0.0, [0.7, 0.55, 1.6], [[V3[0], 1.95, V3[2]], [V3[0], 0.0, V3[2]], [-3.0, 46.0, -120.0], [r(V3[0] + 0.7), 1.6, V3[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.12))])
st.cue('sfx:click', 'S03', 0.38, 0.3); st.cue('pop', 'S03', 0.42, 0.25)

# 4: the world. Before the pyramids: it sunbathes on its back on a striped towel under a parasol, in sunglasses; LE CAIRE pops on
# (pass 3) a blue towel under the red case (red on red, 1.8 to 1) and the case whole in the frame; it sighs: the lid lifts a little, its sunglasses
# with it, and settles back with a squash (it lay inert for 1.1 s)
D4 = st.dur('S04')
V4 = [0.0, 0.03, -1.8]
SIGH4 = [[0.0, 0.0], [0.15, 0.0], [0.45, 0.3], [0.62, 0.3], [0.82, 0.0]]
st.shot('S04', 'savannah', setOpts={'seed': 8}, actors=[],
        props=[P('towel4', 'carpet', pos=[0.0, 0, -1.65], ry=90, opts={'w': 1.5, 'd': 0.75, 'color': '#2E86C1', 'inner': '#FFFFFF'}),
               VAL('val4', pos=[0.0, 0.18, -1.3], rot=[r(-PI / 2 + 0.25), 0, 0], scale=1.3, opts={'color': RED, 'shades': True, 'stickers': 2, 'stickerTimes': [-1.0, 0.35], 'seed': 0, 'open': SIGH4},
                   keys=[k(0.82, squash=[1.06, 0.93, 1.06], dur=0.25)]),
               P('parasol4', 'parasol', pos=[0.75, 0, -2.2], opts={'openAt': -1.0}),
               P('pyr4a', 'pyramid', pos=[-6.0, 0, -26.0], opts={'base': 13, 'h': 9}), P('pyr4b', 'pyramid', pos=[7.5, 0, -36.0], opts={'base': 18, 'h': 12}), P('pyr4c', 'pyramid', pos=[20.0, 0, -50.0], opts={'base': 10, 'h': 7})],
        cams=[FC(0.0, [0.8, 0.95, 0.15], [[0.0, 0.5, -1.3], [-0.45, 0.15, -1.25], [0.45, 0.15, -1.0], [0.0, 0.0, -2.3], [0.75, 1.9, -2.2], [-6.0, 9.0, -26.0]], top=0.1, bottom=0.74, drift=(-0.08, 0.0, -0.08))])
        # (first look) closer: the suitcase was a corner of the frame
st.cue('pop', 'S04', 0.35, 0.25); st.cue('sfx:slideDownSlow', 'S04', 0.6, 0.15)

# 5: forty countries. In space: the Earth turning, the suitcase in sunglasses orbiting it like a satellite, a white streak behind it
D5 = st.dur('S05')
ORB = 2.15; EC = [0.0, 0.0, -5.0]   # (pass 2) clear of the globe (at 1.75 its wheels ran on the Earth: it walked)
def orbit_keys(t0, dur, a0, a1, n=8):
    ks = []
    for i in range(n):
        a = a0 + (a1 - a0) * (i + 1) / n
        ks.append(k(r(t0 + dur * i / n), to=[r(EC[0] + ORB * math.cos(a)), r(EC[1] + 1.6 + ORB * 0.35 * math.sin(a)), r(EC[2] + ORB * math.sin(a))], dur=r(dur / n), ease='linear'))
    return ks
st.shot('S05', 'spaceDark', actors=[],
        props=[P('earth5', 'earthGlobe', pos=EC, opts={'radius': 1.6, 'spin': 0.5}),
               P('trail5', 'orbitTrail', pos=[EC[0], r(EC[1] + 1.6), EC[2]], opts={'r': ORB, 'tilt': -0.33, 'speed': 0.55}),
               VAL('val5', pos=[r(EC[0] + ORB * math.cos(0.32)), r(EC[1] + 1.6 + ORB * 0.35 * math.sin(0.32)), r(EC[2] + ORB * math.sin(0.32))], scale=1.15, opts={'color': RED, 'shades': True, 'stickers': 4, 'seed': 0},
                   keys=[*orbit_keys(0.0, round(D5 + 0.1, 3), 0.32, 2.82), k(0.0, rotTo=[0.4, 2.4, 0.3], dur=round(D5 + 0.1, 3))])],   # (check stills 2) across the front of the Earth mid-shot
        cams=[cam(0.0, [0.0, 2.6, 3.5], [0.0, 2.55, 3.2], [0.0, 1.55, -5.0], [0.0, 1.55, -5.0], lens=44)])
st.cue('whoosh', 'S05', 0.1, 0.3, 0.9, 300, 1400)

# 6: three hundred flights. The departures hall: the board's VOLS counter runs up to 300 while the stickers pop onto the suitcase one after another
# (pass 3) the suitcase jumps a little at each sticker (it did not react to any of them); its handle down (the bar crossed the V of VOLS); the hall's
# sign out (cut at the top left, it read RTS)
D6 = st.dur('S06')
V6 = [0.0, 0, -1.2]; NST6 = 11; ST6 = [round(0.08 + i * (D6 - 0.3) / NST6, 3) for i in range(NST6)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[],
        props=[HALL('hall6', sign=False),
               P('board6', 'flightBoard', pos=[0.35, 1.9, -2.6], scale=1.25, opts={'from': 37, 'to': 300, 't0': 0.0, 't1': round(D6 - 0.2, 3)}),
               VAL('val6', pos=V6, ry=-10, scale=1.35, opts={'color': RED, 'stickers': NST6 + 4, 'stickerTimes': [-1.0] * 4 + ST6, 'seed': 0, 'handle': 0.0},
                   keys=[k(t_, squash=[1.07, 0.92, 1.07], dur=0.1) for t_ in ST6])],
        cams=[FC(0.0, [0.9, 1.25, 1.6], [[V6[0], 1.05, V6[2]], [V6[0], 0.0, V6[2]], [-0.9, 2.65, -2.6], [1.6, 1.2, -2.6]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.15))])
for i_, t_ in enumerate(ST6): st.cue('pop', 'S06', t_, 0.12 + 0.01 * (i_ % 3))
st.cue('sfx:ticks', 'S06', 0.0, 0.2)

# 7: the airline gave a loyalty card. The check-in desk (ENREGISTREMENT), from behind the agent's shoulder: she holds out the gold card with a smile;
#    his arm shoots out for it and stretches across the desk; she draws it back a little; his suitcase stands beside him
# (pass 3) the card twice the size and turned to the lens (edge-on in her fingers, 40 x 19 px); she holds it in her left hand, on our side, and
# draws it back, then waggles it; he stays upright, so his arm alone stretches across the desk after it (he leaned in: it read as a normal reach); the
# sign's words on its back too, higher in the frame; a breath in her holds
D7 = st.dur('S07')
DZ7 = 1.2   # (pass 2) the whole desk 1.2 m forward from the hall's back wall: room behind it for the cameras (against the wall the lenses opened to 77-85 degrees)
AG = [-0.45, 0, r(-2.95 + DZ7)]; ME7 = [-0.2, 0, r(-1.2 + DZ7)]; CARD7 = [-0.3, 1.45, r(-2.2 + DZ7)]; VS7 = [-1.75, 0.235, r(-1.85 + DZ7)]   # (first look) the suitcase on the check-in scale beside the desk (on the floor behind it, it was hidden)
CARD7B = [r(CARD7[0] + 0.12), r(CARD7[1] + 0.06), r(CARD7[2] - 0.32)]   # where she draws it back to
SCALE = lambda n: P(f'scale{n}', 'bagScale', pos=[VS7[0], 0, VS7[2]])
REACH7 = lambda x, y, z, s=1.0: {'reach': {'R': [r(x), r(y), r(z), 1, 0.05]}, 'hands': {'R': 'spread'}, 'hose': 0.12}   # (pass 2) the weight always 1 (at 1.4-1.6 the hand overshot its point and the arm hung)
DESK = lambda n: P(f'desk{n}', 'serviceDesk', pos=[-0.1, 0, r(-2.05 + DZ7)], opts={'w': 2.4, 'text': 'ENREGISTREMENT', 'sub': False, 'band': '#1F3A6E', 'color': '#E4E0D6', 'signY': 2.75, 'twoSided': True})
GOLD = {'tag': 'gold', 'tagScale': 2.4, 'tagGlint': 0.12}                   # (pass 2) the gold card hung down the front of the suitcase, oversized, twinkling
HOLD7 = lambda c, sq=None: {'reach': {'L': [r(c[0] + 0.16), r(c[1] - 0.02), r(c[2] - 0.02), 1, 0.05]}, 'hands': {'L': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}, **({'sq': sq} if sq else {})}
st.shot('S07', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('agent', AG, 0, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec', 'cheat': 0.2}), k(0.0, toon=HOLD7(CARD7), toonDur=0.0),
            k(0.3, toon=HOLD7(CARD7, [1.0, 1.02, 1.0]), toonDur=0.25, toonEase='inOut'),                                    # a breath...
            k(0.62, toon=HOLD7(CARD7B), toonDur=0.18, toonEase='inOut'),                                                   # ...she draws it back a little...
            k(0.95, toon=HOLD7([r(CARD7B[0] + 0.04), r(CARD7B[1] + 0.03), CARD7B[2]]), toonDur=0.12, toonEase='inOut'), k(1.07, toon=HOLD7(CARD7B, [1.0, 0.99, 1.0]), toonDur=0.12, toonEase='inOut')]),   # ...and waggles it
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[CARD7[0], CARD7[1], CARD7[2]]), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.25, toon={**REACH7(ME7[0] - 0.1, 1.2, ME7[2] + 0.15), 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.35}}, toonDur=0.1, toonEase='in'),   # the hand back first...
            k(0.4, toon={**REACH7(CARD7[0] - 0.02, CARD7[1] - 0.02, CARD7[2] + 0.12), 'sq': [0.98, 1.03, 0.98], 'face': {'lid': 0.25, 'brow': 0.4}}, toonDur=0.08, toonEase='out'),   # ...then shot out across the desk, stretching
            k(0.62, toon={**REACH7(CARD7B[0] - 0.02, CARD7B[1] - 0.03, CARD7B[2] + 0.14), 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.18, toonEase='inOut'),   # after it...
            k(0.95, toon={**REACH7(CARD7B[0] + 0.02, CARD7B[1], CARD7B[2] + 0.1), 'face': {'lid': 0.3, 'brow': 0.5}}, toonDur=0.12, toonEase='inOut'),            # ...and after it again
            k(1.1, toon={**REACH7(CARD7B[0] - 0.01, CARD7B[1] - 0.03, CARD7B[2] + 0.13), 'face': {'lid': 0.4, 'brow': 0.4}}, toonDur=0.14, toonEase='inOut'),
            k(0.62, look=[CARD7B[0], CARD7B[1], CARD7B[2]])])],
        props=[HALL('hall7', sign=False), DESK('7'), SCALE('7'),
               P('card7', 'loyaltyCard', pos=CARD7, face='camera', opts={'s': 2.2, 'bright': True},
                 keys=[k(0.62, to=CARD7B, dur=0.18, ease='inOut'), k(0.95, to=[r(CARD7B[0] + 0.04), r(CARD7B[1] + 0.03), CARD7B[2]], dur=0.12, ease='inOut'), k(1.07, to=CARD7B, dur=0.12, ease='inOut')]),
               VAL('val7', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0})],
        cams=[FC(0.0, [1.75, 2.3, -3.85], [[ME7[0], 2.45, ME7[2]], [ME7[0], 0.9, ME7[2]], [VS7[0], 1.2, VS7[2]], [CARD7[0], CARD7[1], CARD7[2]], [-0.1, 3.02, -1.3], [-0.85, 2.8, -1.3], [0.65, 2.8, -1.3], [r(AG[0] - 0.05), 2.2, AG[2]]], top=0.1, bottom=0.74, inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8))])
        # over the agent's shoulder: his face to us across the desk (from his side we saw his back)
st.cue('sfx:stretch', 'S07', 0.4, 0.3)

# 8: a loyalty card. Close on the desk top from the side: the gold card in her fingers, his stretched hand an inch short of it; the card glides away
#    over his fingers toward the suitcase; his hand closes on air
# (pass 2) low on the desk top from behind it, the suitcase beyond on the left: she flicks the card, it arcs over his fingers and drops into the tag on
# the front of the suitcase, which swings; his hand closes on air (S08 repeated S07's angle, the card vanished behind her)
# (pass 3) the agent further off to her right and her hand away after the flick: his empty grab in the clear (a hand under her sleeve at the edge)
D8 = st.dur('S08'); FL8 = 0.14; LAND8 = 0.62
TAG8 = [r(VS7[0] + 0.03), 0.76, r(VS7[2] - 0.17)]                          # the card's place in the tag, on the front of the suitcase (it faces -Z, the desk's side)
APEX8 = [-0.95, 1.85, r(-2.05 + DZ7)]
AG8 = [0.6, 0, AG[2]]
st.shot('S08', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('agent', AG8, 0, 'stand', 'happy', keys=[k(0.0, look=[CARD7[0], 1.6, CARD7[2]]), k(0.0, toon={'reach': {'R': [r(CARD7[0] + 0.05), CARD7[1], r(CARD7[2] - 0.2), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.0),
            k(round(FL8 - 0.06, 3), toon={'reach': {'R': [r(CARD7[0] + 0.1), r(CARD7[1] - 0.06), r(CARD7[2] - 0.28), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.06, toonEase='in'),
            k(FL8, toon={'reach': {'R': [r(CARD7[0] - 0.12), r(CARD7[1] + 0.12), r(CARD7[2] - 0.18), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0}}, toonDur=0.05, toonEase='out'),   # a flick of the wrist...
            k(0.3, toon={'reach': {'R': [0.3, 1.2, r(AG8[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.15}}, toonDur=0.16, toonEase='inOut'),   # ...and her hand away
            k(round(FL8 + 0.1, 3), look=[TAG8[0], TAG8[1], TAG8[2]])]),
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[CARD7[0], CARD7[1], CARD7[2]]), k(0.0, toon={**REACH7(CARD7[0] + 0.05, CARD7[1] - 0.02, CARD7[2] + 0.05), 'face': {'lid': 0.25, 'brow': 0.5}}, toonDur=0.0),
            k(0.22, look=[APEX8[0], APEX8[1], APEX8[2]]), k(0.42, look=[TAG8[0], TAG8[1], TAG8[2]]),   # his eyes follow it over his hand...
            k(0.36, toon={**REACH7(CARD7[0] + 0.02, CARD7[1] - 0.02, CARD7[2] + 0.02), 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'brow': 0.6}}, toonDur=0.06)])],   # ...the hand closes on air
        props=[HALL('hall8', sign=False), DESK('8'), SCALE('8'),
               P('card8', 'loyaltyCard', pos=[r(CARD7[0] + 0.05), r(CARD7[1] - 0.06), r(CARD7[2] - 0.12)], face='camera', opts={'s': 1.5, 'bright': True},
                 keys=[k(FL8, path=[APEX8, TAG8], dur=round(LAND8 - FL8, 3), ease='inOut'), k(LAND8, visible=False)]),   # it arcs over his fingers into the tag
               VAL('val8', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0}, keys=[k(LAND8, visible=False)]),
               VAL('val8g', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0, **GOLD, 'tagSwing': 0.6}, keys=[k(0.0, visible=False), k(LAND8, visible=True), k(LAND8, squash=[1.06, 0.95, 1.06], dur=0.3)])],
        cams=[FC(0.0, [-1.05, 1.45, -3.6], [[r(CARD7[0] + 0.05), CARD7[1], CARD7[2]], APEX8, TAG8, [VS7[0], 0.55, VS7[2]], [ME7[0], 1.95, ME7[2]], [r(ME7[0] + 0.2), 1.35, ME7[2]]], top=0.1, bottom=0.72, lenses=range(30, 57), inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8))])
st.cue('sfx:slideUp', 'S08', FL8, 0.2); st.cue('sfx:ding', 'S08', LAND8, 0.3)

# 9: to the suitcase. The gold card swinging in the suitcase's luggage tag; his hand still out in the air, deadpan, a slow blink at us
# (pass 3) low from the suitcase's front: the gold card big and whole in the foreground, his face and his hand out behind it on the diagonal (S09
# repeated S08's framing, the card small at the edge, a blank desk front a quarter of the frame: the desk is left out of this one); then a cut in on
# his face for the slow blink, his head a third of the frame (every deadpan of the draft was in a medium-wide shot)
D9 = st.dur('S09'); CUT9 = 0.5
HAND9 = [-1.0, 1.25, -0.45]                                                 # his hand out toward the suitcase
st.shot('S09', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[TAG8[0], TAG8[1], TAG8[2]]), k(0.0, toon={**REACH7(*HAND9), 'hands': {'R': 'grip'}, 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.3, look='camera'), k(0.3, face=165, turn=0.2),   # (pass 2) his hand still out, his face to us
            k(round(CUT9 + 0.12, 3), toon={**REACH7(*HAND9), 'hands': {'R': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.1),
            k(round(CUT9 + 0.36, 3), toon={**REACH7(*HAND9), 'hands': {'R': 'grip'}, 'face': {'lid': 0.45}}, toonDur=0.14)])],   # a slow blink at us
        props=[HALL('hall9', sign=False), SCALE('9'),
               VAL('val9g', pos=VS7, ry=170, scale=1.2, opts={'color': RED, 'stickers': 15, 'seed': 0, 'handle': 1.0, **GOLD, 'tagSwing': 0.45})],   # the gold card swinging on the front of the suitcase
        cams=[FC(0.0, [-2.1, 0.5, -1.85], [TAG8, [VS7[0], 0.28, VS7[2]], [r(VS7[0] - 0.3), 0.9, VS7[2]], [ME7[0], 2.45, ME7[2]], [ME7[0], 1.3, ME7[2]], HAND9], top=0.1, bottom=0.74, inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8)),
              FC(CUT9, [r(ME7[0] - 0.35), 2.0, r(ME7[2] - 1.55)], [[ME7[0], 2.42, ME7[2]], [ME7[0], 1.8, ME7[2]]], top=0.2, bottom=0.62, inside=(-6.8, 6.8, 0.2, 4.8, -4.0, 5.8))])
st.cue('sfx:ding', 'S09', 0.05, 0.15)

# 10: it flies first class. The cabin: the suitcase lounges in a wide leather seat, a sleep mask pushed up on its brow, the gold tag hanging, a flute of
#     champagne on the armrest; the hostess bows and tops up its glass
# (pass 3) a bottle in her hand and a pour you can see, the glass filling (her hand hovered over the flute with nothing in it); a breath in her bow
# (frozen 0.8 s); the suitcase sinks back into the leather with a sigh; the sleep mask one pink band with closed eyes painted on (two lobes read as a
# bra or a bow)
D10 = st.dur('S10')
SEAT = [-0.85, 0, 0.4]; HOST = [0.25, 0, 0.7]   # (first look) beside the seat: in front of it her back filled half the frame
BOT10 = [-0.27, 1.21, 0.65]                      # the bottle's grip: tipped 100 degrees its mouth is over the flute
POUR10 = [[0.0, 0.5], [0.22, 1.75], [1.2, 1.95], [1.45, 0.7]]
HOLDB = lambda bend, sq=None, lid=0.6: {'reach': {'R': [*BOT10, 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [bend, 0, 0, 1, None]}, 'face': {'mouth': 'smile', 'lid': lid}, **({'sq': sq} if sq else {})}
st.shot('S10', 'whiteVoid', setOpts={'color': '#DCD6C8'}, actors=[
        act('hotesse', HOST, -100, 'stand', 'happy', keys=[k(0.0, look={'point': [SEAT[0], 1.0, SEAT[2]], 'cheat': 0.45}),   # (probe) her face cheated to us (76 degrees: a profile)
            k(0.0, toon=HOLDB(0.1, lid=0.25), toonDur=0.0),
            k(0.15, toon=HOLDB(0.45), toonDur=0.25, toonEase='inOut'),                                   # a bow as she pours...
            k(0.6, toon=HOLDB(0.5, [1.0, 1.015, 1.0]), toonDur=0.3, toonEase='inOut'), k(0.95, toon=HOLDB(0.43), toonDur=0.3, toonEase='inOut'),   # ...a breath...
            k(round(D10 - 0.5, 3), toon=HOLDB(0.15, lid=0.25), toonDur=0.25, toonEase='inOut')])],      # ...and up
        props=[P('cabin10', 'cabinShell', pos=[0, 0, 0], opts={'len': 8, 'half': 1.9}),
               P('seat10', 'firstSeat', pos=SEAT, ry=0), P('seat10b', 'firstSeat', pos=[-0.85, 0, -1.4], ry=0), P('seat10c', 'firstSeat', pos=[0.95, 0, -1.4], ry=0),
               VAL('val10', pos=[SEAT[0], 0.47, r(SEAT[2] - 0.05)], rot=[-0.22, 0, 0], scale=1.0, opts={'color': RED, 'stickers': 15, 'seed': 0, 'shades': 'band', **GOLD, 'tagScale': 2.0, 'tagSwing': 0.15},
                   keys=[k(0.85, rotTo=[-0.42, 0, 0], dur=0.3, ease='inOut'), k(0.85, squash=[1.05, 0.95, 1.05], dur=0.35), k(1.25, rotTo=[-0.3, 0, 0], dur=0.3, ease='inOut')]),   # it sinks back into the leather
               P('flute10', 'flute', pos=[-0.42, 0.59, 0.5], scale=1.6, opts={'level': 0.85, 'fill': [[0.0, 0.2], [0.3, 0.2], [1.2, 0.85]]}),
               P('bot10', 'champagneBottle', pos=BOT10, ry=-45, opts={'tilt': POUR10}),
               P('pour10', 'beerStream', pos=[-0.425, 1.155, 0.495], opts={'length': 0.2, 'r': 0.007, 'color': '#F3CF5A'}, keys=[k(0.0, visible=False), k(0.26, visible=True), k(1.2, visible=False)])],
        cams=[FC(0.0, [-1.35, 1.55, 2.5], [[SEAT[0], 1.6, SEAT[2]], [SEAT[0], 0.45, SEAT[2]], [HOST[0], 1.85, HOST[2]], [-0.42, 0.75, 0.5]], top=0.34, bottom=0.74, drift=(0.08, 0.0, -0.05), inside=(-1.75, 1.75, 0.3, 2.2, -3.8, 3.9))])   # (pass 2) tighter (the lens opened to 68 degrees)
st.cue('sfx:pour', 'S10', 0.24, 0.3); st.cue('sfx:jet', 'S10', 0.0, 0.06)

# 11: he flies in the hold. Dark, between the bags: he sits folded with his knees up, FRAGILE stuck on his forehead, under a swinging bulb; the plane
#     banks: a big bag slides in and squashes him flat, then it slides off and he springs back into shape; deadpan
# (pass 2) the frame banks with the plane; FRAGILE on his forehead
# (pass 3) the bag crosses in front of him and slams him back against the big purple case behind him, then slides off: he is left flattened like a
# pancake facing us, FRAGILE stretched wide on his brow, held nine frames, and springs back past his shape twice (pressed sideways he became an
# edge-on slice in front of the bag, the layering flipping: a pile of navy limbs); FRAGILE higher, off his eye; the burst beside the impact
D11 = st.dur('S11'); HIT11 = 0.56; OFF11 = round(HIT11 + 0.1, 3); BACK11 = round(HIT11 + 0.48, 3)
ME11 = [-0.45, 0, -0.6]
FLAT11 = [ME11[0], 0, -0.98]                                          # pressed back against the case behind him
SPLAT11 = {'reach': {'L': [r(ME11[0] - 0.62), 0.95, -0.95, 1, 0.05], 'R': [r(ME11[0] + 0.62), 0.95, -0.95, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}   # arms and hands splayed on the case
st.shot('S11', 'whiteVoid', setOpts={'color': '#20242C'}, actors=[
        act('mec', ME11, 0, 'sitFloor', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'sq': [1.0, 0.92, 1.0], 'face': {'lid': 0.45}}, toonDur=0.0),
            k(round(HIT11 - 0.14, 3), toon={'sq': [1.0, 0.94, 1.0], 'face': {'lid': 0.3, 'brow': 0.5, 'gx': 0.6}}, toonDur=0.08),   # he sees it coming...
            k(round(HIT11 - 0.02, 3), toon={**SPLAT11, 'sq': [1.45, 1.15, 0.2], 'face': {'lid': 0.5, 'cross': 0.7, 'brow': 0.6}}, toonDur=0.03, toonEase='out'),   # ...SCHLAC: flat as a pancake, splayed...
            k(round(HIT11 - 0.04, 3), to=FLAT11, dur=0.04, glide=True, face='keep'),   # (check stills) pushed back with the bag, not after it
            k(round(BACK11 - 0.1, 3), toon={**SPLAT11, 'sq': [1.42, 1.13, 0.22], 'face': {'lid': 0.5, 'cross': 0.7, 'brow': 0.5}}, toonDur=0.2),   # ...held, facing us...
            k(BACK11, toon={'sq': [0.86, 0.97, 1.3], 'face': {'lid': 0.45}}, toonDur=0.06, toonEase='outBack'),                    # ...and back, past his shape...
            k(BACK11, to=ME11, dur=0.1, glide=True, face='keep'),
            k(round(BACK11 + 0.1, 3), toon={'sq': [1.1, 0.9, 0.92], 'face': {'lid': 0.45}}, toonDur=0.07), k(round(BACK11 + 0.19, 3), toon={'sq': [0.96, 0.95, 1.05], 'face': {'lid': 0.45}}, toonDur=0.07),   # ...twice...
            k(round(BACK11 + 0.28, 3), toon={'sq': [1.0, 0.92, 1.0], 'face': {'lid': 0.45}}, toonDur=0.08),
            k(round(D11 - 0.2, 3), toon={'sq': [1.0, 0.92, 1.0], 'face': {'lid': 1.0}}, toonDur=0.05), k(round(D11 - 0.1, 3), toon={'sq': [1.0, 0.92, 1.0], 'face': {'lid': 0.45}}, toonDur=0.06)])],   # ...deadpan, a blink
        props=[P('hold11', 'cargoHold', pos=[0, 0, 0], opts={'len': 6, 'half': 1.6, 'h': 1.7, 'lampX': -0.3, 'lampZ': 0.15, 'swing': 0.35}),   # (pass 2b) the bulb in front of him: his face lit
               P('frag11', 'fragileTag', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.43, 0.092]}, scale=1.0, opts={'w': 0.22, 'bright': True}),
               VAL('b11a', pos=[-0.95, 0, -0.8], ry=80, scale=1.1, opts={'color': '#2E6FB5', 'stickers': 2, 'seed': 3}), VAL('b11b', pos=[-0.95, 0.75, -0.8], ry=75, scale=1.0, opts={'color': '#3CB371', 'seed': 4}),
               VAL('b11c', pos=[0.8, 0, -1.3], ry=-20, scale=1.15, opts={'color': '#7A7F87', 'seed': 5}), VAL('b11d', pos=[-0.45, 0, -1.25], ry=0, scale=1.25, opts={'color': '#9B59B6', 'seed': 6}),   # the big case right behind him
               P('sch11', 'hicBurst', pos=[0.4, 1.35, -0.4], face='camera', opts={'at': [HIT11], 'w': 0.42, 'text': 'SCHLAC !', 'inner': 0.78, 'fit': 0.56}),
               VAL('b11e', pos=[1.7, 0, 0.1], ry=5, scale=1.3, opts={'color': '#F28C28', 'stickers': 3, 'seed': 7},
                   keys=[k(0.12, to=[-0.42, 0, 0.1], dur=round(HIT11 - 0.16, 3), ease='in'), k(round(HIT11 - 0.04, 3), to=[-0.42, 0, -0.77], dur=0.04, ease='in'),   # across in front of him, then into him
                         k(OFF11, to=[1.8, 0, -0.2], dur=0.2, ease='inOut')])],   # ...and off again
        cams=[FC(0.0, [0.4, 1.1, 0.75], [[ME11[0], 1.6, ME11[2]], [ME11[0], 0.4, ME11[2]], [-0.95, 1.0, -0.8], [0.25, 0.9, -0.55]], top=0.16, bottom=0.74, drift=(0.0, 0.0, -0.1)),
              {**glide([FC(round(HIT11 - 0.1, 3), [0.4, 1.1, 0.75], [[ME11[0], 1.6, ME11[2]], [ME11[0], 0.4, ME11[2]], [-0.95, 1.0, -0.8], [0.25, 0.9, -0.55]], top=0.16, bottom=0.74)], 0.2), 'roll': 0.12}])   # (check stills) from 35 degrees off his front: the pancake reads thin (from the front, only wider)
        # (pass 2) the frame banks with the plane as the bag comes in
st.cue('sfx:splat', 'S11', HIT11, 0.45); st.cue('whoosh', 'S11', OFF11, 0.2, 0.25, 300, 1200); st.cue('sfx:boing', 'S11', BACK11, 0.25); st.cue('sfx:jet', 'S11', 0.0, 0.1)

# 12: yesterday it came back. At the carousel, he behind the belt as before: the flaps lift and his red suitcase rides out of the tunnel covered in
#     stickers, the gold card on its tag; he jumps for joy: a crouch, up, held at the top with his arms out, deadpan
# (pass 3) the suitcase rides out standing up and facing us, in its sunglasses, already pushing through the lifted flaps at the cut and clear of them
# by 0.45 s (lying flat it was a red sliver of 40 x 50 px at the mouth of the tunnel); he jumps once it is out, and lands on bent knees (he landed
# stiff-legged in a T); he stands further left, under the sign
D12 = st.dur('S12'); JMP = 0.72; SPD12 = 0.8
ME12 = [-1.5, 0, -3.0]
VR12 = [EXITX, BELT, BACKZ]
VX12 = lambda t: r(VR12[0] - SPD12 * t)
st.shot('S12', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME12, 15, 'stand', 'unimpressed', keys=[k(0.0, look=[VX12(0.15), 1.1, BACKZ]), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.3, look={'point': [VX12(0.45), 1.0, BACKZ], 'cheat': 0.3}),
            k(round(JMP - 0.18, 3), toon={'sq': [1.12, 0.85, 1.12], 'face': {'lid': 0.3}, 'autoSq': 0}, toonDur=0.12, toonEase='in'),     # a crouch...
            k(JMP, toon={'sq': [0.9, 1.15, 0.9], 'reach': {'L': [r(ME12[0] + 0.7), 2.55, ME12[2], 1, 0.05], 'R': [r(ME12[0] - 0.7), 2.55, ME12[2], 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'lid': 0.2, 'mouth': 'smile'}, 'autoSq': 0}, toonDur=0.08, toonEase='out'),
            k(round(JMP + 0.37, 3), toon={'sq': [1.15, 0.82, 1.15], 'bend': {'legL': [0.45, 0, 0, 1, None], 'legR': [0.45, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'smile'}, 'autoSq': 0}, toonDur=0.05, toonEase='in'),   # ...down on bent knees...
            k(round(JMP + 0.6, 3), toon={'face': {'lid': 0.45, 'mouth': 'smile'}}, toonDur=0.12),
            k(JMP, to=[ME12[0], 0.62, ME12[2]], dur=0.16, glide=True, ease='out', face='keep'), k(round(JMP + 0.16, 3), to=[ME12[0], 0.66, ME12[2]], dur=0.12, glide=True, ease='inOut', face='keep'),   # up, a hang at the top...
            k(round(JMP + 0.28, 3), to=[ME12[0], 0.0, ME12[2]], dur=0.12, glide=True, ease='in', face='keep')])],   # ...and down
        props=[HALL('hall12', signX=-1.5), P('car12', 'carousel', pos=CAR, opts={**CAROPTS, 'speed': SPD12, 'flap': [[0.0, 0.4], [0.25, 0.5], [0.5, 0.2], [0.75, 0.0]]}),
               VAL('val12', pos=VR12, ry=0, scale=1.4, opts={'color': RED, 'stickers': 15, 'seed': 0, 'shades': True, **GOLD, 'tagScale': 2.0, 'tagSwing': 0.3},
                   keys=[k(0.0, to=[VX12(D12), BELT, BACKZ], dur=round(D12, 3), ease='linear')])],   # rides out at the belt's speed
        cams=[FC(0.0, [-1.6, 2.05, 1.6], [[ME12[0], 3.3, ME12[2]], [ME12[0], 0.7, ME12[2]], [r(ME12[0] - 0.9), 3.0, ME12[2]], [r(ME12[0] + 0.9), 3.0, ME12[2]], [r(EXITX + 0.6), 2.0, BACKZ], [VX12(D12), BELT, BACKZ], [VX12(0.5), 1.55, BACKZ]], top=0.08, bottom=0.74)])
st.cue('sfx:slideDown', 'S12', 0.05, 0.2); st.cue('sfx:boing', 'S12', JMP, 0.3); st.cue('sfx:fanfare', 'S12', round(JMP + 0.05, 3), 0.15); st.cue('thud', 'S12', round(JMP + 0.4, 3), 0.2)

# 13: with a little suitcase. Behind it a little pink suitcase with a baby's dummy pops out through the flaps and bumps into the big one; his double
#     take, the jaw dropping
# (pass 3) low on the belt by the mouth of the tunnel: both suitcases standing up and facing us in the lower middle of the frame, the little one a
# fifth of the frame wide with a dummy three times the size, out with a hop and a bump (hidden behind the big one and the wall); then a cut to him for
# the take: the look back at the big one, the snap, the eyes on stalks and the jaw down to his belt, hit at 0.72 s and held to the cut (the jaw came at
# 1.60 s of 1.63: the take helper's keys and the shot's own fought each other)
D13 = st.dur('S13'); OUT13 = 0.06; BUMP13 = 0.34; CUT13 = 0.55; SNAP13 = 0.72; SPD13 = 0.25
ME13 = [-1.55, 0, -3.0]
VB13 = [-1.0, BELT, BACKZ]; VBX = lambda t: r(VB13[0] - SPD13 * t)   # (check stills) clear of the tunnel's wall, which cut the little one
LS0 = [r(EXITX + 0.22), BELT, BACKZ]; LSB = [r(VBX(BUMP13) + 0.7 / 2 + 0.375 / 2), BELT, BACKZ]   # the little one against the big one's side
TAKEF = {'pop': 0.8, 'popLen': 0.35, 'brow': 1.0, 'jaw': 1.0, 'jawLen': 1.0, 'mouth': 'O'}
st.shot('S13', 'whiteVoid', setOpts={'color': '#E3E8EC'}, actors=[
        act('mec', ME13, 15, 'stand', 'unimpressed', keys=[k(0.0, look=[VBX(0.0), 1.0, BACKZ]), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.4, look=[LSB[0], 0.7, BACKZ]),                                       # a glance at the little one...
            k(0.56, look={'point': [r(VBX(0.56) - 0.1), 1.0, BACKZ], 'cheat': 0.45}),                          # ...back to the big one, blank...
            k(SNAP13, look={'point': [r(LSB[0] - SPD13 * (SNAP13 - BUMP13)), 0.7, BACKZ], 'cheat': 0.5}),     # ...and the snap back to the little one, cheated to the lens (a 67-degree profile)
            k(round(SNAP13 - 0.05, 3), toon={'sq': [1.1, 0.88, 1.1], 'face': {'lid': 0.6, 'brow': -0.3, 'mouth': 'smile'}}, toonDur=0.04, toonEase='in'),   # the anticipation squash...
            k(SNAP13, toon={'sq': [0.88, 1.18, 0.88], 'face': TAKEF}, toonDur=0.05, toonEase='outBack'),                                                   # ...the stretch, eyes out, jaw to his belt...
            k(0.95, toon={'sq': [0.9, 1.15, 0.9], 'face': TAKEF}, toonDur=0.1), k(1.15, toon={'sq': [0.89, 1.16, 0.89], 'face': TAKEF}, toonDur=0.1), k(1.35, toon={'sq': [0.91, 1.14, 0.91], 'face': TAKEF}, toonDur=0.1),   # ...held, a shiver...
            k(round(D13 - 0.1, 3), toon={'sq': [0.95, 1.06, 0.95], 'face': {'pop': 0.55, 'popLen': 0.28, 'brow': 0.8, 'jaw': 0.9, 'jawLen': 0.9, 'mouth': 'O'}}, toonDur=0.1)])],
        props=[HALL('hall13'), P('car13', 'carousel', pos=CAR, opts={**CAROPTS, 'speed': SPD13, 'flap': [[0.0, 0.0], [round(OUT13 - 0.03, 3), 0.0], [round(OUT13 + 0.06, 3), 0.5], [round(OUT13 + 0.24, 3), 0.25], [round(OUT13 + 0.4, 3), 0.0]]}),
               VAL('val13', pos=VB13, ry=0, scale=1.4, opts={'color': RED, 'stickers': 15, 'seed': 0, 'shades': True, **GOLD, 'tagScale': 2.0, 'tagSwing': 0.2},
                   keys=[k(0.0, to=[VBX(D13), BELT, BACKZ], dur=round(D13, 3), ease='linear'), k(BUMP13, squash=[1.08, 0.94, 1.08], dur=0.3)]),
               VAL('val13s', pos=LS0, ry=0, scale=0.75, opts={'color': '#F5A3C0', 'pacifier': True, 'pacScale': 3.0, 'stickers': 1, 'seed': 9},
                   keys=[k(OUT13, path=[[r((LS0[0] + LSB[0]) / 2), r(BELT + 0.42), BACKZ], LSB], dur=round(BUMP13 - OUT13, 3), ease='out'),   # out with a hop...
                         k(BUMP13, squash=[1.25, 0.78, 1.25], dur=0.3),                                                                       # ...a bump into the big one...
                         k(BUMP13, to=[r(LSB[0] + 0.05 - SPD13 * (D13 - BUMP13)), BELT, BACKZ], dur=round(D13 - BUMP13, 3), ease='linear')])],   # ...and on with it
        cams=[FC(0.0, [-1.25, 1.05, 0.7], [[r(EXITX + 0.1), 1.85, BACKZ], [VBX(0.0), 1.55, BACKZ], [VBX(CUT13), BELT, BACKZ], [r((LS0[0] + LSB[0]) / 2), r(BELT + 0.85), BACKZ], [LS0[0], BELT, BACKZ], [ME13[0], 2.45, ME13[2]]], top=0.1, bottom=0.72),
              FC(CUT13, [r(ME13[0] + 0.2), 1.95, -1.25], [[ME13[0], 2.7, ME13[2]], [ME13[0], 1.15, ME13[2]]], top=0.1, bottom=0.66)])
st.cue('sfx:squeak', 'S13', OUT13, 0.25); st.cue('clack', 'S13', BUMP13, 0.25); st.cue('sfx:gasp', 'S13', SNAP13, 0.25)

# 14: he pays the maintenance. At home on the rug: he kneels before the little suitcase lying open like a mouth and feeds it a banknote; the lid snaps
#     shut on his hand; he pulls, his arm stretches like elastic, the little suitcase sliding after it, and lets go: the arm snaps back, the hand empty;
#     deadpan, a blink; the big suitcase stands by with its gold card
# (pass 2) his hand stays in the lid all through the pull while his body falls back; it lets go: the arm snaps back past rest with two wobbles, the lid
# clacks shut on air; a big green banknote
# (pass 3) a higher three-quarter view looking down on the rug: his arm a line of its own across it, his head in the frame, the open mouth turned
# halfway to the lens with its dark inside showing (a pink slab seen from behind); the little suitcase further off, lying on the rug (half sunk in
# the floor), skidding less: the arm stretches about three times its length and thins; the big case whole beside them; a cut in on his face for the
# last blink, his head a third of the frame
D14 = st.dur('S14'); SNAP = 0.56; PULL = 0.86; PEAK = 1.3; LET = 1.6; CUT14 = 1.95
ME14 = [-0.55, 0, -0.55]; SM14 = [0.5, 0.1, -0.05]; CAM14 = [1.3, 1.8, 1.45]
YAWM = round((math.atan2(ME14[0] - SM14[0], ME14[2] - SM14[2]) + math.atan2(CAM14[0] - SM14[0], CAM14[2] - SM14[2])) / 2, 3)   # its mouth halfway between him and the lens
MD14 = (math.sin(YAWM), math.cos(YAWM))
LIDO = [[0.0, 1.1], [round(SNAP - 0.05, 3), 1.1], [SNAP, 0.0], [round(PEAK + 0.02, 3), 0.0], [round(PEAK + 0.06, 3), 0.14], [round(PEAK + 0.1, 3), 0.0], [round(PEAK + 0.16, 3), 0.12], [round(PEAK + 0.2, 3), 0.0],
        [round(LET - 0.02, 3), 0.0], [round(LET + 0.04, 3), 0.4], [round(LET + 0.14, 3), 0.0], [round(LET + 0.2, 3), 0.1], [round(LET + 0.26, 3), 0.0]]   # (pass 2) it chomps at the peak, opens to let go, clacks shut on air
TOWARD = lambda d: [r(SM14[0] + (ME14[0] - SM14[0]) * d), SM14[1], r(SM14[2] + (ME14[2] - SM14[2]) * d)]
INLID = lambda d: [r(TOWARD(d)[0] - 0.12 * MD14[0]), 0.13, r(TOWARD(d)[2] - 0.12 * MD14[1])]   # the hand inside its mouth, wherever it has skidded to
GRIP14 = lambda d: {'reach': {'R': [*INLID(d), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.15}
st.shot('S14', 'livingRoom', setOpts={'carpet': False, 'picture': False}, actors=[
        act('mec', ME14, 60, 'kneel', 'unimpressed', keys=[k(0.0, look=[SM14[0], 0.15, SM14[2]]), k(0.0, toon={'reach': {'R': [r(ME14[0] + 0.45), 0.6, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.25, toon={**GRIP14(0.0), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.25, toonEase='inOut'),   # the banknote into its mouth
            k(SNAP, toon={**GRIP14(0.0), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.0, 'brow': 0.6}}, toonDur=0.033, toonEase='out'),   # CHOMP
            k(round(SNAP + 0.15, 3), toon={**GRIP14(0.0), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.1), k(round(SNAP + 0.17, 3), look='camera'),   # deadpan, at us
            k(PULL, toon={**GRIP14(0.0), 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'lay': [-0.15, 0], 'face': {'lid': 0.3, 'brow': 0.3}}, toonDur=0.12, toonEase='in'),
            k(round(PULL + 0.12, 3), toon={**GRIP14(0.12), 'bend': {'spine': [-0.75, 0, 0, 1, None]}, 'lay': [-0.6, 0], 'face': {'lid': 0.3, 'brow': 0.5, 'mouth': 'clench'}}, toonDur=round(PEAK - PULL - 0.12, 3), toonEase='inOut'),   # he falls back, the hand still in its mouth: the arm like elastic
            k(round(PULL + 0.05, 3), look=[SM14[0], 0.15, SM14[2]]),
            k(LET, toon={'reach': {'R': [r(ME14[0] - 0.15), 1.25, r(ME14[2] + 0.1), 1, 0.05]}, 'hands': {'R': 'spread'}, 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'lay': [-0.2, 0], 'sq': [0.96, 1.04, 0.96], 'face': {'lid': 0.2, 'brow': 0.8}}, toonDur=0.05, toonEase='out'),   # it lets go: the arm snaps back past rest...
            k(round(LET + 0.1, 3), toon={'reach': {'R': [r(ME14[0] + 0.32), 0.75, r(ME14[2] + 0.38), 1, 0.05]}, 'hands': {'R': 'open'}, 'lay': [0.04, 0], 'face': {'lid': 0.35}}, toonDur=0.08),   # ...wobbles once...
            k(round(LET + 0.2, 3), toon={'reach': {'R': [r(ME14[0] + 0.18), 0.95, r(ME14[2] + 0.3), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45}}, toonDur=0.08),   # ...twice
            k(round(LET + 0.3, 3), toon={'reach': {'R': [r(ME14[0] + 0.25), 0.85, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45}}, toonDur=0.1),   # the hand empty
            k(round(LET + 0.32, 3), look='camera'), k(round(D14 - 0.42, 3), toon={'reach': {'R': [r(ME14[0] + 0.25), 0.85, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0}}, toonDur=0.07),
            k(round(D14 - 0.25, 3), toon={'reach': {'R': [r(ME14[0] + 0.25), 0.85, r(ME14[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45}}, toonDur=0.1)])],
        props=[P('rug14', 'carpet', pos=[-0.05, 0, -0.35], opts={'w': 2.4, 'd': 1.7, 'color': '#C9D3C2', 'inner': '#DCE3D6'}),   # (check stills) a pale sage rug: the navy arm a line across it (on the blue-grey rug it vanished); (pass 2) pink on the orange floor was 1.3 to 1
               VAL('val14s', pos=SM14, rot=[r(-PI / 2), 0, YAWM], scale=0.75, opts={'color': '#F5A3C0', 'pacifier': True, 'pacScale': 2.0, 'stickers': 1, 'seed': 9, 'open': LIDO},
                   keys=[k(round(PULL + 0.12, 3), to=TOWARD(0.12), dur=round(PEAK - PULL - 0.12, 3), ease='inOut'), k(LET, to=TOWARD(0.06), dur=0.18, ease='out')]),   # it skids after him on its back, a little
               VAL('val14', pos=[0.95, 0, -0.85], ry=-35, scale=1.15, opts={'color': RED, 'stickers': 15, 'seed': 0, **GOLD, 'tagScale': 2.0, 'tagSwing': 0.12}),
               P('note14', 'banknote', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.1, 0.02]}, scale=1.5, keys=[k(SNAP, visible=False)])],   # (pass 2) a big banknote
        cams=[FC(0.0, CAM14, [[ME14[0], 1.7, ME14[2]], [r(ME14[0] - 0.65), 0.9, ME14[2]], [SM14[0], 0.45, SM14[2]], [0.95, 1.05, -0.85], [0.95, 0.0, -0.85], [ME14[0], 0.0, ME14[2]]], top=0.12, bottom=0.74, drift=(-0.05, 0.0, -0.08)),
              FC(CUT14, [r(ME14[0] + 0.95), 1.45, r(ME14[2] + 1.15)], [[ME14[0], 1.65, ME14[2]], [ME14[0], 1.05, ME14[2]]], top=0.18, bottom=0.62)])
st.cue('sfx:zip', 'S14', 0.25, 0.2); st.cue('clack', 'S14', SNAP, 0.45); st.cue('sfx:stretch', 'S14', round(PULL + 0.12, 3), 0.3); st.cue('clack', 'S14', round(PEAK + 0.06, 3), 0.2); st.cue('sfx:twang', 'S14', LET, 0.35); st.cue('clack', 'S14', round(LET + 0.14, 3), 0.3); st.cue('sfx:cash', 'S14', round(LET + 0.3, 3), 0.15)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe; (cycle 16) the near-blocker test in front of each
for g_ in [('S01', 0.7, 'mec', 'sock', None), ('S02', round(OUT2 + 0.1, 3), 'mec', 'slap', None), ('S07', 0.55, 'mec', 'reach', None), ('S08', 0.4, 'mec', 'hand', 'handR'),
           ('S09', 0.66, 'mec', 'blink', None), ('S10', 0.6, 'hotesse', 'bow', None), ('S11', round(HIT11 + 0.3, 3), 'mec', 'flat', None), ('S12', round(JMP + 0.2, 3), 'mec', 'jump', None),
           ('S13', round(SNAP13 + 0.3, 3), 'mec', 'jaw', None), ('S14', round(PULL + 0.3, 3), 'mec', 'elastic', None), ('S14', round(D14 - 0.3, 3), 'mec', 'end', None)]:
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
