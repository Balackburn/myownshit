#!/usr/bin/env python3
"""La cravate (story 43, cycle 7 of the cartoon staging): this man caught his tie in the lift door. The lift went up. Not him. The tie did. To the
sixth floor. He called the managing agent. The agent replied: "In the lift shaft, it is a common part." Since then the lady on the third hangs her
washing on it. The kid on the fifth plays it. He is making progress. To unhook it, a vote of the general meeting is needed. Yesterday they voted. One
vote was missing. His. He was downstairs. They voted the repainting all the same. His tie is beige. He pays the service charges.
Tone: he stays on the ground floor, his feet on the floor; it is the tie that stretches; he is annoyed, never choked: the tie leaves the back of his
collar level with the floor and runs back to the seam of the lift door (a leash), never upward.
Second staging (the first had the leash hidden behind him: seen from in front, a line that runs straight back from a man's nape is behind his head):
in the hall he stands a pace in front of the door and well to its right, so the red line crosses the frame beside his head to the seam. Every gag of
the film is the leash pulling him or him straining at it: the rubber neck, the poster on the wall, the drag on his heels, the yank of each peg, the
plucked string, the six-floor arm, the zip-line bill. The cut-away block (the shaft at the right, the landings at the left) is the map."""
from story_kit import *
import math

st = Story('cravate', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L01', 11), ('S04', 'L02', 0), ('S05', 'L02', 2), ('S06', 'L02', 5), ('S07', 'L03', 0),
         ('S08', 'L04', 0), ('S09', 'L05', 0), ('S10', 'L05', 4), ('S11', 'L06', 0), ('S12', 'L06', 5), ('S13', 'L07', 0), ('S14', 'L07', 6),
         ('S15', 'L08', 0), ('S16', 'L08', 3), ('S17', 'L09', 0), ('S18', 'L09', 4), ('S19', 'L10', 0), ('S20', 'L10', 2), ('S21', 'L11', 0),
         ('S22', 'L11', 5), ('S23', 'L12', 0), ('S24', 'L13', 0), ('S25', 29.0, 0)])

RED, BEIGE = '#D0202A', '#D9C7A3'
FH = 2.8                                             # a floor of the block
NAPE = {'actor': 'mec', 'joint': 'neck', 'offset': [0, 0.05, -0.1]}   # where the tie leaves his collar: at the back (the knot stays in front: cast tieKnot)
HEAD = 2.28                                          # the top of his tuft (a man of the series is 2.2 m and some)


def hcam(t, frm, pts, top=0.2, bottom=0.8, drift=(0.0, 0.0, -0.12), lenses=range(26, 66), ease='linear', margin=0.07):
    """a camera at frm that holds every point of pts between top and bottom of the frame (story_kit.fit), dollying by drift over the shot"""
    look, lens, _ = fit(list(frm), pts, margin=margin, top=top, bottom=bottom, lenses=lenses)
    if lens is None: raise SystemExit(f'no lens fits from {frm}: {pts}')
    return cam(t, list(frm), [round(frm[i] + drift[i], 3) for i in range(3)], look, [round(look[i] + drift[i], 3) for i in range(3)], lens=lens, ease=ease)


# ---- the hall: the lift door in the middle of the back wall (z = -3), its seam at x = 0; the floor display over it (y 2.4); the notice board at x 2.3
BACK = -3.0
SEAM = [0.0, 1.56, -2.93]                            # where the tie goes into the door: at the height of his collar
ME = [1.3, 0, -2.05]; MERY = -8                      # where he stands for the rest of the film: on his leash, a pace from the wall, well right of the door
HALL = lambda doors=None, floor=None: {'doors': doors or [[0, 0]], 'floor': floor or [[0, '6']]}
ROPE = lambda pid='rope', **o: P(pid, 'tieRope', on=NAPE, opts={'color': RED, 'w': 0.085, 'to': SEAM, **o})
HEADME = [ME[0], HEAD, ME[2]]; FEETME = [ME[0], 0.0, ME[2]]; CHEST = [ME[0], 1.2, ME[2]]
DISP = [0.0, 2.55, -2.92]                            # the floor display
STAND = lambda **kw: k(0.0, look=None, **kw)

# 1: the hook. He comes out of the lift, pleased with himself, and turns right toward the street door; the end of his tie flies behind him; the doors
#    shut on it: clack. Two more steps: the tie is taut: his head stays; the rest of him goes on: his neck is two heads long
D1 = st.dur('S01'); C1, T1 = 0.42, 0.92                # the doors meet; the tie is taut
A1, B1, F1 = [0.0, 0, -2.5], [1.2, 0, -1.85], 60     # out of the cabin; where the tie stops him; his heading (out and to the right)
BK1 = (-math.sin(math.radians(F1)), -math.cos(math.radians(F1)))   # behind him
def pos1(t): u = min(t, T1) / T1; return [A1[0] + (B1[0] - A1[0]) * u, 0.0, A1[2] + (B1[2] - A1[2]) * u]
def trail1(t, L):                                     # the free end of the tie, flying behind him
    p = pos1(t); return [round(p[0] + (0.1 + L) * BK1[0], 3), round(1.52 + 0.07 * math.sin(t * 31), 3), round(p[2] + (0.1 + L) * BK1[1], 3)]
E1 = [round(B1[0] + 0.3 * math.sin(math.radians(F1)), 3), 0, round(B1[2] + 0.3 * math.cos(math.radians(F1)), 3)]   # where his feet end: past the point where his head stopped
NECK1 = {'neck': [-0.85, 0, 0, 2.5, None], 'spine': [0.35, 0, 0, 1, None]}
st.shot('S01', 'immeubleHall', setOpts=HALL([[0.0, 1], [round(C1 - 0.22, 3), 1], [C1, 0]], [[0, 'RC']]), actors=[
        act('mec', A1, F1, 'walk', 'smug', keys=[STAND(), k(0.0, to=B1, dur=T1, clip='walk', then='stand', ease='linear', face=F1, cruise=True),
            k(0.3, look=[3.2, 1.7, 0.4]), k(0.62, toon={'face': {'lid': 0.35, 'browL': 0.5}}, toonDur=0.1),                       # pleased with himself, eyes half shut
            k(T1 - 0.03, look=None), k(T1 - 0.03, toon={'bend': {'neck': [-0.7, 0, 0, 2.1, None], 'spine': [0.25, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'brow': 1, 'eye': 0.55, 'jaw': 0.5, 'pop': 0.5}}, toonDur=0.07, toonEase='out'),
            k(T1, expr='surprised'), k(T1, to=E1, dur=0.12, clip='stand', then='stand', glide=True, ease='out', face=F1),            # his feet go on, his head stays
            k(T1 + 0.16, toon={'bend': NECK1, 'tremble': 1, 'face': {'brow': 1, 'eye': 0.55, 'jaw': 0.55, 'pop': 0.75, 'pupilShake': 1}}, toonDur=0.1)])],   # and hangs there
        props=[P('rope', 'tieRope', on=NAPE, opts={'color': RED, 'w': 0.085, 'toKeys': [[t, *trail1(t, 0.42 + 0.3 * t / C1)] for t in (0.0, 0.1, 0.2, 0.3)] + [[C1, *SEAM]], 'pluck': [[T1, 0.05, 9, 14, 5]]}),
               P('clack', 'impactStars', pos=[0.0, 1.56, -2.86], opts={'at': C1, 'n': 6, 'r': 0.3, 'r0': 0.1, 'dur': 0.26, 'size': 0.06})],
        fx=[{'type': 'shake', 'at': C1, 'dur': 0.1, 'amount': 0.01}, {'type': 'shake', 'at': T1, 'dur': 0.14, 'amount': 0.016}],
        cams=[hcam(0.0, [-0.2, 1.5, 3.4], [[-0.62, 2.6, -2.9], [-0.62, 0.05, -2.9], [E1[0] + 0.3, HEAD + 0.1, E1[2]], [E1[0] + 0.3, 0.0, E1[2]], [0.0, 0.0, -2.5]], top=0.12, bottom=0.86)])
st.cue('clack', 'S01', C1, 0.6); st.cue('sfx:twang', 'S01', T1, 0.45); st.cue('sfx:stretch', 'S01', T1 + 0.05, 0.35)

# 2: from the right. The neck snaps back, then all of him: he flies backwards and lands flat on the wall beside the lift, a poster; slides; peels off,
#    fills out; and digs in: he runs on the spot, leaning away, his heels squeaking on the tiles: the leash does not give
D2 = st.dur('S02'); N2, H2, PL2, SC2 = 0.06, 0.18, 0.6, 0.78
WALL2 = [0.98, 0, -2.86]                              # his back on the wall right of the lift door
DIG2 = [1.25, 0, -2.25]                               # where he digs in
st.shot('S02', 'immeubleHall', setOpts=HALL([[0, 0]], [[0, 'RC']]), actors=[
        act('mec', E1, F1, 'stand', 'surprised', keys=[STAND(), k(0.0, toon={'bend': NECK1, 'tremble': 1, 'face': {'brow': 1, 'eye': 0.55, 'jaw': 0.55, 'pop': 0.75}}, toonDur=0.0),
            k(N2 - 0.05, toon={'sq': [0.88, 1.14, 0.88], 'bend': {'neck': [0.3, 0, 0, 0.8, None]}, 'face': {'brow': 1, 'eye': 0.5, 'jaw': 0.6}}, toonDur=0.05, toonEase='in'),   # the neck comes back first: boing
            k(N2, to=WALL2, dur=round(H2 - N2, 3), clip='stand', then='stand', glide=True, ease='in', face=0),                   # then all of him, backwards
            k(H2, clip='poster', params={'slideAt': 0.2, 'slide': 0.35, 'high': 0.12, 'flat': 0.08, 'expr': 'dizzy', 'stars': 1}),
            k(PL2 - 0.06, to=DIG2, dur=0.12, clip='stand', then='stand', glide=True, ease='out', face=70), k(PL2 - 0.06, toon={'sq': [1.14, 0.88, 1.2]}, toonDur=0.06, toonEase='out'),   # off the wall: a pop
            k(PL2 + 0.04, toon={'sq': [0.95, 1.06, 0.95], 'settle': 0.6}, toonDur=0.08), k(PL2 + 0.06, expr='angry'),
            k(SC2, clip='scramble', params={'dur': 0.4, 'freq': 9, 'expr': 'determined'})])],                                       # he runs on the spot
        props=[ROPE(pluck=[[H2, 0.05, 10, 14, 5], [SC2 + 0.1, 0.03, 12, 14, 6]]),
               P('splat', 'impactStars', pos=[WALL2[0], 1.8, -2.8], opts={'at': H2, 'n': 7, 'r': 0.55, 'r0': 0.25, 'dur': 0.3, 'size': 0.08}),
               P('dust', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[SC2, DIG2[0] - 0.15, DIG2[2] - 0.1], [D2, DIG2[0] - 0.15, DIG2[2] - 0.1]], 'from': SC2, 'to': D2, 'every': 0.05})],
        fx=[{'type': 'shake', 'at': H2, 'dur': 0.16, 'amount': 0.02}],
        cams=[hcam(0.0, [3.1, 1.45, 0.4], [[WALL2[0], HEAD + 0.15, -2.9], [WALL2[0], 0.0, -2.86], [DIG2[0], HEAD, DIG2[2]], [DIG2[0] + 0.3, 0.0, DIG2[2]], SEAM, [-0.3, 1.5, -2.9]], top=0.14, bottom=0.86)])
st.cue('sfx:spring', 'S02', N2 - 0.04, 0.4); st.cue('sfx:splat', 'S02', H2, 0.6); st.cue('pop', 'S02', PL2 - 0.05, 0.35); [st.cue('sfx:squeak', 'S02', round(SC2 + 0.12 * i, 3), 0.18) for i in range(5)]

# 3: the lift went up. From the front: he is running on the spot; a bell: the display says 1; the leash takes him backwards on his heels, smoke at
#    his heels, across the tiles to the door; he slams flat on it; 2, 3: each floor flattens him a little more
D3 = st.dur('S03'); G3, DR3, HT3 = 0.1, 0.16, 0.42
ONDOOR = [0.28, 0, -2.84]                             # his back on the right leaf, his nape at the seam
FLAT3 = lambda k_=0.0: {'sq': [1.24 + 0.05 * k_, 1.02, 0.13 - 0.02 * k_], 'hands': {'L': 'spread', 'R': 'spread'}, 'reach': {'L': [ONDOOR[0] + 0.8, 1.55 - 0.05 * k_, -2.8, 1, 0.08], 'R': [ONDOOR[0] - 0.6, 1.6 - 0.05 * k_, -2.8, 1, 0.08]},
                        'scl': {'head': [1.18 + 0.06 * k_, 0.95 - 0.03 * k_, 0.7]}, 'face': {'brow': 1, 'eye': 0.5, 'cheeks': 1, 'mouth': 'wavy', 'pupilShake': 1 if k_ else 0}}
st.shot('S03', 'immeubleHall', setOpts=HALL([[0, 0]], [[0, 'RC'], [G3, '1'], [0.62, '2'], [1.0, '3']]), actors=[
        act('mec', DIG2, 70, 'stand', 'determined', keys=[STAND(), k(0.0, clip='scramble', params={'dur': 0.05, 'freq': 9, 'expr': 'determined'}),
            k(G3, look=DISP), k(G3 + 0.02, expr='surprised'),                                                                         # the bell: his eyes go up to it
            k(DR3, clip='heelBrake', to=ONDOOR, dur=round(HT3 - DR3, 3), glide=True, ease='in', face=20),                          # dragged backwards on his heels
            k(HT3, clip='stand'), k(HT3, toon=FLAT3(0), toonDur=0.03), k(HT3 + 0.02, look=[0.6, 1.6, 1.8]),                       # flat on the door
            k(0.62, toon=FLAT3(1), toonDur=0.06), k(1.0, toon=FLAT3(2), toonDur=0.06)])],                                            # a floor more: flatter
        props=[ROPE(pluck=[[G3, 0.04, 12, 14, 4], [HT3, 0.05, 10, 14, 5]]), P('bell', 'impactStars', pos=[0, 2.6, -2.86], opts={'at': G3, 'n': 5, 'r': 0.3, 'r0': 0.15, 'dur': 0.24, 'size': 0.05}),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[DR3, DIG2[0] - 0.1, DIG2[2] + 0.1], [HT3, ONDOOR[0], ONDOOR[2] + 0.15]], 'from': DR3, 'to': HT3, 'every': 0.03, 'marks': True}),
               P('slam', 'impactStars', pos=[ONDOOR[0], 1.7, -2.78], opts={'at': HT3, 'n': 7, 'r': 0.5, 'r0': 0.2, 'dur': 0.28, 'size': 0.07})],
        fx=[{'type': 'shake', 'at': HT3, 'dur': 0.14, 'amount': 0.02}],
        cams=[hcam(0.0, [0.75, 1.5, 1.7], [[0, 2.68, -2.92], [-0.62, 0.05, -2.9], [1.0, 0.05, -2.9], [DIG2[0] + 0.2, HEAD, DIG2[2]], [DIG2[0] + 0.3, 0.0, DIG2[2]]], top=0.12, bottom=0.88)])
st.cue('sfx:bell', 'S03', G3, 0.5); st.cue('sfx:squeak', 'S03', DR3, 0.35); st.cue('whoosh', 'S03', DR3, 0.25, 0.25, 400, 1500); st.cue('sfx:splat', 'S03', HT3, 0.55)
st.cue('sfx:tick', 'S03', 0.62, 0.3); st.cue('sfx:tick', 'S03', 1.0, 0.3)

# 4: not him. The tie gives: he springs off the door, a pop, whole again, on his feet a pace away; the tie is a red line from his collar to the seam,
#    taut, humming; he looks along it to the door; at us
D4 = st.dur('S04'); P4 = 0.08
st.shot('S04', 'immeubleHall', setOpts=HALL([[0, 0]], [[0, '3'], [0.2, '4'], [0.5, '5']]), actors=[
        act('mec', ONDOOR, 20, 'stand', 'surprised', keys=[STAND(), k(0.0, toon=FLAT3(2), toonDur=0.0),
            k(P4, to=ME, dur=0.16, clip='stand', then='stand', glide=True, ease='out', face=MERY), k(P4, toon={'sq': [1.12, 0.9, 1.22]}, toonDur=0.06, toonEase='out'),   # off the door: a pop
            k(P4 + 0.1, toon={'sq': [0.95, 1.06, 0.95], 'settle': 0.6}, toonDur=0.08), k(P4 + 0.12, expr='unimpressed'),
            k(P4 + 0.2, look=SEAM), k(P4 + 0.22, toon={'face': {'gx': -0.8, 'browL': 0.7}}, toonDur=0.08),                           # his eyes go along the tie to the door
            k(0.56, look=[1.8, 1.65, 1.2]), k(0.58, toon={'face': {'lid': 0.45, 'browL': 0.6}}, toonDur=0.08)])],                     # then to us
        props=[ROPE(pluck=[[P4 + 0.1, 0.05, 9, 14, 3]])],
        cams=[hcam(0.0, [2.25, 1.6, 0.9], [[ME[0] + 0.25, HEAD + 0.05, ME[2]], [ME[0], 0.7, ME[2]], SEAM, DISP, [-0.3, 2.62, -2.92]], top=0.16, bottom=0.74)])
st.cue('pop', 'S04', P4, 0.45); st.cue('sfx:twang', 'S04', P4 + 0.1, 0.4)

# ---- the block cut open (the camera looks toward -Z): landings at the left, the lift shaft at the right; he stands on the ground-floor landing by its
#      partition, his back to the lift's landing door; the tie goes from his nape through the door and straight up the shaft to the cabin
SX = 6.4 / 2 - 1.7 / 2 - 0.12; SW = 1.7                # the middle of the shaft, its width
PART = round(SX - SW / 2 - 0.06, 3)                   # the partition between the landings and the shaft
MEC = [round(PART - 0.72, 3), 0, 0.35]                 # he, on the ground floor, a pace from the partition
DOORC = [round(PART - 0.06, 3), 1.56, 0.3]             # where the tie goes through the landing door
LINEX = round(SX - 0.52, 3)                            # the tie in the shaft: a red line beside the cabin's cables
CABTOP = lambda lv: round(lv * FH + 0.5, 2)            # where the tie ends, under the cabin floor
LEN = 0.75 + 0.46 + (CABTOP(6) - 1.56)                 # the length of the tie when the cabin is at the sixth
AT = lambda y: round((CABTOP(6) - y) / LEN, 4)         # where a point of the shaft at height y is along the tie, from its far end
def ROPEC(cab=None, **o):   # the tie in the cut-away: from his collar, through the door, round the sill, and straight up to the cabin (cab: [[t, level], ...])
    end = {'toKeys': [[t, LINEX, CABTOP(lv), 0.2] for t, lv in cab]} if cab else {'to': [LINEX, CABTOP(6), 0.2]}
    return P('rope', 'tieRope', on=NAPE, opts={'color': RED, 'w': 0.16, 'via': [DOORC, [LINEX, 1.56, 0.2]], 'face': [0, 0, 1], **end, **o})
def coupecam(t, y0, y1, d=13.0, lens=44, x=0.7, **kw):  # square to the cut, travelling up or down
    return cam(t, [x, y0, d], [x, y1, d], [x, y0, 0], [x, y1, 0], lens=lens, **kw)
HIM = lambda **kw: act('mec', MEC, -35, 'stand', 'unimpressed', keys=[STAND()], **kw)
WASH = lambda t1, t2, t3: [{'at': AT(10.0), 'kind': 'shirt', 'color': '#F4F1E8', 'from': t1}, {'at': AT(9.55), 'kind': 'sock', 'color': '#E8A33A', 'from': t2},
                           {'at': AT(9.35), 'kind': 'sock', 'color': '#3A6EA5', 'from': round(t2 + 0.1, 3)}, {'at': AT(9.05), 'kind': 'towel', 'color': '#E77A9A', 'from': t3}]
COUPE = lambda cab=None: {'cabin': cab or [[0.0, 6.0]]}

# 5: the tie did. The block cut open: the cabin goes up the dark shaft, floor after floor, and under it the tie: a red line that gets longer; the
#    frame goes up with it; he stays at the bottom of the picture, then leaves it
D5 = st.dur('S05')
st.shot('S05', 'immeubleCoupe', setOpts=COUPE([[0.0, 3.0], [D5, 5.2]]), actors=[HIM()],
        props=[ROPEC([[0.0, 3.0], [D5, 5.2]])],
        cams=[coupecam(0.0, 3.4, 11.0, d=14.0, ease='inOut')])
st.cue('whoosh', 'S05', 0.0, 0.2, D5, 200, 600)

# 6: to the sixth. The top of the block: the cabin stops: a bell: a neighbour comes out on the landing without a look; then the frame drops the whole
#    height of the block, down the red line, to him
D6 = st.dur('S06'); A6 = 0.2
st.shot('S06', 'immeubleCoupe', setOpts=COUPE([[0.0, 5.2], [A6, 6.0]]), actors=[HIM(),
        act('voisin', [round(PART - 0.5, 3), 6 * FH, 0.35], -90, 'stand', 'neutral', keys=[k(0.0, visible=False), k(A6 + 0.12, visible=True), k(A6 + 0.14, to=[-1.6, 6 * FH, 0.35], dur=0.7, clip='walk', ease='linear', face=-90)])],
        props=[ROPEC([[0.0, 5.2], [A6, 6.0]], pluck=[[A6, 0.12, 5, 30, 3]])],
        cams=[coupecam(0.0, 16.6, 17.2, d=9.0), glide([coupecam(A6 + 0.36, 9.5, 9.0, d=22.5, lens=50)], 0.45)])
st.cue('sfx:bell', 'S06', A6, 0.5)

# 7: he called the managing agent. The hall, closer: his phone at his ear, a foot that taps, his eyes to the ceiling; the leash runs from behind his
#    head to the door; over the door, 6
D7 = st.dur('S07')
st.shot('S07', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'phoneEar', 'unimpressed', keys=[STAND(), k(0.0, toon={'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.0),
            *[x for i in range(4) for x in (k(round(0.1 + 0.28 * i, 3), toon={'bend': {'shinR': [0.45, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.07), k(round(0.2 + 0.28 * i, 3), toon={'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.06))],   # a foot taps
            k(0.45, look=[ME[0] - 0.2, 3.6, ME[2] + 0.4]), k(0.95, look=[1.8, 1.7, 1.0])])],                                               # eyes to the ceiling, then to us
        props=[ROPE(), P('phone', 'smartPhone', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.02, 0.03]})],
        cams=[hcam(0.0, [2.0, 1.75, 0.15], [[ME[0] + 0.2, HEAD + 0.06, ME[2]], [ME[0], 1.05, ME[2]], SEAM, DISP], top=0.18, bottom=0.72)])
[st.cue('sfx:tick', 'S07', round(0.17 + 0.28 * i, 3), 0.2) for i in range(4)]; st.cue('sfx:ring', 'S07', 0.05, 0.15)

# ---- the managing agent's office: the agent (a bald man with a beard, charcoal suit) behind a desk, piles of files, SYNDIC on the wall behind him
OFF = {'door': False, 'printer': False}
DESKZ = -1.55; SYN = [0.0, 0, -2.25]
DESK = lambda: [P('desk', 'desk', pos=[0.0, 0, DESKZ], opts={'w': 1.6, 'd': 0.75, 'color': '#7A5A3C'}),
                P('pile1', 'paperPile', pos=[0.5, 0.76, DESKZ - 0.05], opts={'count': 70, 'seed': 4}), P('pile2', 'paperPile', pos=[0.62, 0.76, DESKZ + 0.15], opts={'count': 45, 'seed': 7}),
                P('pile3', 'paperPile', pos=[-0.55, 0.76, DESKZ + 0.05], opts={'count': 55, 'seed': 9}),
                P('sign', 'paperSheet', pos=[0.0, 2.45, -3.45], opts={'w': 1.15, 'h': 0.32, 'big': 'SYNDIC', 'bigSize': 0.62, 'top': 0.18, 'paper': '#1B2A4A', 'ink': '#F4F1E8', 'bigInk': '#F4F1E8'})]

# 8: the managing agent answered. He picks up without looking up: the phone wedged between ear and shoulder (his head on one side, his neck folded),
#    the other hand stamping papers like a machine
D8 = st.dur('S08')
STAMPS8 = [0.12, 0.42, 0.72, 1.02, 1.3]
st.shot('S08', 'office', setOpts=OFF, actors=[
        act('syndic', SYN, 0, 'phoneEar', 'unimpressed', keys=[STAND(), k(0.0, look=[0.0, 0.8, DESKZ]),
            k(0.0, toon={'bend': {'neck': [0, 0, 0.35, 0.75, None]}, 'face': {'lid': 0.55}}, toonDur=0.0),                                  # the phone in the fold of his neck
            *[x for t in STAMPS8 for x in (k(round(t - 0.12, 3), toon={'bend': {'neck': [0, 0, 0.35, 0.75, None]}, 'reach': {'L': [-0.3, 1.25, DESKZ, 1, 0.06]}, 'face': {'lid': 0.55}}, toonDur=0.1, toonEase='out'),
                                           k(t, toon={'bend': {'neck': [0, 0, 0.35, 0.75, None]}, 'reach': {'L': [-0.3, 0.86, DESKZ + 0.05, 1, 0.04]}, 'face': {'lid': 0.55}}, toonDur=0.04, toonEase='in'))]])],
        props=[*DESK(), P('stamp', 'rubberStamp', on={'actor': 'syndic', 'hand': 'L', 'offset': [0, -0.04, 0.02]}), P('phone', 'smartPhone', on={'actor': 'syndic', 'hand': 'R', 'offset': [0, 0.02, 0.03]})],
        cams=[hcam(0.0, [0.5, 1.7, 2.3], [[0.0, 2.32, SYN[2]], [-0.75, 0.76, DESKZ + 0.38], [0.75, 0.76, DESKZ + 0.38], [0.0, 2.62, -3.45]], top=0.14, bottom=0.74)])
[st.cue('sfx:cuff', 'S08', t, 0.35) for t in STAMPS8]

# 9: "In the lift shaft," — close on him: his finger up, his eyebrows up over his glasses, he says it (the narrator's line, his mouth)
D9 = st.dur('S09')
st.shot('S09', 'office', setOpts=OFF, actors=[
        act('syndic', SYN, 0, 'stand', 'neutral', keys=[STAND(), k(0.0, look=[0.4, 1.95, 1.0]), *st.talk('L05', 'S09', 'neutral'),
            k(0.0, toon={'hands': {'R': 'point'}, 'reach': {'R': [round(SYN[0] - 0.3, 3), 2.42, round(SYN[2] + 0.3, 3), 1, 0.06]}, 'face': {'brow': 0.8, 'lid': 0.3}}, toonDur=0.0),   # one finger up: the rule
            *[k(t, toon={'hands': {'R': 'point'}, 'reach': {'R': [round(SYN[0] - 0.3, 3), 2.42 + dy, round(SYN[2] + 0.3, 3), 1, 0.06]}, 'face': {'brow': 0.8, 'lid': 0.3}}, toonDur=0.08) for t, dy in ((0.3, -0.06), (0.62, 0.02), (0.95, -0.05))]])],   # it beats the words
        props=[*DESK()],
        cams=[hcam(0.0, [0.4, 1.95, -0.1], [[0.0, 2.35, SYN[2]], [0.0, 1.45, SYN[2]], [-0.3, 2.55, SYN[2] + 0.3]], top=0.18, bottom=0.66, drift=(-0.02, 0, -0.1))])

# 10: "it is a common part." From above, his desk: the rules of the block; the big stamp comes down: PARTIE COMMUNE (the title card: one per film)
D10 = st.dur('S10'); HIT10 = 0.3
SHEET10 = [0.0, 0.775, DESKZ + 0.02]
st.shot('S10', 'office', setOpts=OFF, actors=[],
        props=[*DESK(), P('rules', 'paperSheet', pos=SHEET10, rot=[-math.pi / 2, 0, 0], opts={'w': 0.46, 'h': 0.6, 'head': 'RÈGLEMENT DE COPROPRIÉTÉ', 'lines': ['Article 4', "La cage d'ascenseur", "et ce qu'elle contient"], 'rules': True, 'bright': True,
                                                                                         'stamp': {'text': 'PARTIE COMMUNE', 'at': HIT10, 'rot': 0.22, 'y': -0.12}}),
               P('bigstamp', 'bigStamp', pos=[0.12, 1.45, SHEET10[2] - 0.42], ry=-13, keys=[k(HIT10 - 0.14, to=[0.0, 0.775 + 0.39, SHEET10[2] + 0.12], dur=0.14, ease='in'), k(HIT10, squash=[1.25, 0.7, 1.25], dur=0.25),
                                                                                   k(HIT10 + 0.22, to=[0.14, 1.45, SHEET10[2] - 0.45], dur=0.25, ease='out')])],   # it comes down from beyond the top of the frame onto its mark (the foot of the page is toward us) and goes back up there (lifted straight up it filled the lens)
        fx=[{'type': 'shake', 'at': HIT10, 'dur': 0.14, 'amount': 0.018}],
        cams=[cam(0.0, [0.0, 2.05, DESKZ + 0.32], [0.0, 1.95, DESKZ + 0.3], [0.0, 0.77, DESKZ - 0.02], [0.0, 0.77, DESKZ - 0.01], lens=40)])
st.cue('sfx:cuff', 'S10', HIT10, 0.7); st.cue('thud', 'S10', HIT10, 0.5)
st.card('S10', 'PARTIE COMMUNE')

# 11: since then the lady on the third. The cut-away, the third floor: a lady in curlers leans into the shaft from her landing and pegs her washing on
#    the red line: a shirt, two socks, a towel, each with a little pop
D11 = st.dur('S11'); W11 = (0.22, 0.62, 1.05)
DAME = [round(PART - 0.42, 3), 3 * FH, 0.45]
PEG = lambda y: [round(LINEX - 0.06, 3), round(y - 0.02, 3), 0.28]
st.shot('S11', 'immeubleCoupe', setOpts=COUPE(), actors=[
        act('mamie', DAME, 90, 'stand', 'happy', keys=[STAND(), k(0.0, look=[LINEX, 3 * FH + 1.4, 0.2]),
            *[x for t, y in zip(W11, (10.0, 9.55, 9.05)) for x in (k(round(t - 0.18, 3), toon={'reach': {'R': [*PEG(y), 1, 0.08]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}}, toonDur=0.14, toonEase='out'),
                                                                 k(round(t + 0.12, 3), toon={'reach': {'R': [LINEX - 0.5, 3 * FH + 1.0, 0.45, 0, 0.1]}, 'bend': {'spine': [0.1, 0, 0, 1, None]}}, toonDur=0.16))],
            k(1.35, look=[1.0, 3 * FH + 1.6, 6.0])])],                                                                                      # pleased: to us
        props=[ROPEC(items=WASH(*W11), pluck=[[t, 0.03, 6, 14, 4] for t in W11], pluckAt=AT(9.6))],
        cams=[coupecam(0.0, 9.75, 9.68, d=3.9, x=1.2)])
[st.cue('pop', 'S11', t, 0.3) for t in W11]

# 12: on it, her washing. The hall: each peg up there tugs him down here: a jerk back, a bigger one; the towel: he is pulled back on his heels, leaning
#    at forty degrees, his arms windmilling
D12 = st.dur('S12'); J12 = (0.06, 0.34, 0.66)
LEAN12 = [round(ME[0] - 0.42, 3), 0, round(ME[2] - 0.32, 3)]
st.shot('S12', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[1.8, 1.7, 1.0]),
            k(J12[0], toon={'bend': {'neck': [-0.35, 0, 0, 1.2, None]}, 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.05, toonEase='out'), k(J12[0] + 0.12, toon={'face': {'lid': 0.4}}, toonDur=0.1),   # a jerk
            k(J12[1], to=[round(ME[0] - 0.12, 3), 0, round(ME[2] - 0.09, 3)], dur=0.1, clip='stand', then='stand', glide=True, ease='out', face=MERY),
            k(J12[1], toon={'bend': {'neck': [-0.5, 0, 0, 1.4, None], 'spine': [-0.25, 0, 0, 1, None]}, 'face': {'brow': 1, 'eye': 0.45}}, toonDur=0.05, toonEase='out'), k(J12[1] + 0.14, toon={'face': {'lid': 0.3}}, toonDur=0.1),
            k(J12[2], to=LEAN12, dur=0.14, clip='teeter', then='teeter', glide=True, ease='out', face=MERY), k(J12[2], expr='worried'),                         # the towel: on his heels
            k(J12[2] + 0.02, toon={'bend': {'spine': [-0.6, 0, 0, 1, None], 'neck': [-0.3, 0, 0, 1.3, None]}, 'face': {'brow': 1, 'eye': 0.5, 'pupilShake': 1}}, toonDur=0.08)])],
        props=[ROPE(pluck=[[t, 0.04 + 0.02 * i, 9, 14, 4] for i, t in enumerate(J12)])],
        cams=[hcam(0.0, [2.35, 1.5, 1.0], [HEADME, FEETME, [LEAN12[0] - 0.5, 2.0, LEAN12[2]], SEAM, DISP], top=0.15, bottom=0.88)])
[st.cue('sfx:twang', 'S12', t, 0.25 + 0.1 * i) for i, t in enumerate(J12)]; st.cue('sfx:squeak', 'S12', J12[2], 0.35)

# 13: the kid on the fifth plays it. The cut-away, the fifth floor: a boy leans into the shaft and plucks the red line like a double bass, his tongue
#    out; notes rise; the washing two floors down jumps
D13 = st.dur('S13'); PL13 = (0.18, 0.46, 0.74, 1.02, 1.28)
KID = [round(PART - 0.4, 3), 5 * FH, 0.45]
st.shot('S13', 'immeubleCoupe', setOpts=COUPE(), actors=[
        act('gamin', KID, 90, 'stand', 'happy', keys=[STAND(), k(0.0, look=[LINEX, 5 * FH + 1.2, 0.2]),
            *[x for t in PL13 for x in (k(round(t - 0.1, 3), toon={'reach': {'R': [LINEX - 0.02, 5 * FH + 1.15, 0.3, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'tongue': 1}}, toonDur=0.08),
                                        k(t, toon={'reach': {'R': [LINEX + 0.14, 5 * FH + 1.05, 0.3, 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {'tongue': 1}}, toonDur=0.05, toonEase='in'))],
            k(1.4, look=[1.0, 5 * FH + 1.4, 6.0])])],
        props=[ROPEC(items=WASH(0, 0, 0), pluck=[[t, 0.07, 7, 14, 3] for t in PL13], pluckAt=AT(5 * FH + 1.1)),
               P('notes', 'whistleNotes', pos=[LINEX + 0.15, 5 * FH + 1.5, 0.45], opts={'n': 5, 'from': PL13[0], 'every': 0.27, 'size': 0.2, 'dx': -0.25, 'dy': 0.7, 'life': 0.7, 'color': '#1B1B1E'})],
        cams=[coupecam(0.0, 14.95, 14.88, d=3.7, x=1.2)])
[st.cue('sfx:twang', 'S13', t, 0.35) for t in PL13]

# 14: he is making progress. The hall: the waves arrive down the leash: he shakes like a jelly; then the tune takes him: he dances, deadpan
D14 = st.dur('S14'); JE14, DA14 = 0.02, 0.5
st.shot('S14', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[1.8, 1.7, 1.0]), k(0.0, clip='jelly', params={'amp': 0.5, 'freq': 9, 'decay': 0.8}),   # (slower and bigger: at 22 Hz the shake did not show)
            k(DA14, clip='dance'), k(DA14, toon={'face': {'lid': 0.5, 'browL': 0.6}}, toonDur=0.08)])],
        props=[ROPE(pluck=[[t, 0.12, 4.5, 10, 2.5] for t in (-0.3, -0.02, 0.26, 0.54, 0.82)]),   # waves you can see run down the leash
               P('notes', 'whistleNotes', pos=[ME[0] + 0.25, 2.25, ME[2] + 0.3], opts={'n': 4, 'from': 0.1, 'every': 0.22, 'size': 0.16, 'dx': 0.3, 'dy': 0.5, 'life': 0.6, 'color': '#1B1B1E'})],
        cams=[hcam(0.0, [2.1, 1.7, 0.6], [[ME[0] + 0.25, HEAD + 0.1, ME[2]], [ME[0], 0.35, ME[2]], SEAM], top=0.16, bottom=0.8)])

# ---- the notice board of the hall (x 2.3): the agent's notice of the general meeting, pinned on it
CONVOC = lambda: P('convoc', 'paperSheet', pos=[2.3, 1.42, -2.925], opts={'w': 0.5, 'h': 0.64, 'head': 'CONVOCATION', 'big': 'ASSEMBLÉE GÉNÉRALE', 'bigSize': 0.075,
                                                                        'lines': ['Ordre du jour :', '1. Décrocher la cravate', 'du rez-de-chaussée', '2. Ravalement de la façade'], 'lineSize': 0.055})
READ = [1.62, 0, -2.42]; READRY = 128                 # as near the board as the leash lets him, turned to it

# 15: to unhook it — he turns to the notice board as far as the leash lets him, and his neck stretches the rest of the way, his eyes on stalks
D15 = st.dur('S15'); TU15, NK15 = 0.08, 0.3
st.shot('S15', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'unimpressed', keys=[STAND(), k(0.04, look=[2.3, 1.5, -2.95]),
            k(TU15, to=READ, dur=0.2, clip='walk', then='stand', ease='inOut', face=READRY),
            k(NK15, toon={'bend': {'neck': [0.35, 0, 0, 2.4, None], 'spine': [0.3, 0, 0, 1, None]}, 'face': {'pop': 0.6, 'brow': 0.8}}, toonDur=0.16, toonEase='outBack')])],
        props=[ROPE(), CONVOC()],
        cams=[hcam(0.0, [3.25, 1.6, 1.2], [[2.05, 1.85, -2.95], [2.75, 1.1, -2.95], [ME[0], HEAD, ME[2]], [READ[0], 0.0, READ[2]], [ME[0] - 0.3, 1.56, ME[2] - 0.3]], top=0.14, bottom=0.86)])   # from the right-hand wall: his neck stretches across the frame to the board
st.cue('sfx:stretch', 'S15', NK15, 0.35)

# 16: you need a vote of the general meeting. The notice, close: his stretched head comes into the frame at the left, his eyes go down the lines
D16 = st.dur('S16')
st.shot('S16', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', READ, READRY, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[2.3, 1.62, -2.95]),
            k(0.0, toon={'bend': {'neck': [0.35, 0, 0, 2.4, None], 'spine': [0.3, 0, 0, 1, None]}, 'face': {'pop': 0.6, 'brow': 0.8}}, toonDur=0.0),
            k(0.45, look=[2.3, 1.42, -2.95]), k(0.9, look=[2.3, 1.3, -2.95]), k(1.3, look=[2.3, 1.2, -2.95]), k(1.55, toon={'bend': {'neck': [0.35, 0, 0, 2.4, None], 'spine': [0.3, 0, 0, 1, None]}, 'face': {'pop': 0.0, 'lid': 0.45}}, toonDur=0.1)])],
        props=[ROPE(), CONVOC()],
        cams=[cam(0.0, [2.05, 1.55, -1.2], [2.08, 1.53, -1.32], [2.28, 1.5, -2.95], [2.28, 1.49, -2.95], lens=40)])   # the whole notice, its heading under the SYNDIC label; his stretched head comes in at the left
st.cue('sfx:paper', 'S16', 0.1, 0.3)

# ---- the general meeting: a common room (a town-hall office repainted grey-green), the agent's table at the back, the neighbours on chairs facing it.
#      The camera stands behind the agent's table and looks at them; the chair of the ground floor, in the front row, is empty
AG = {'wall': '#E2E6DC', 'band': '#8C9A7A', 'trim': '#5E6B50', 'floor': '#B79B74', 'joint': '#A2865F', 'banner': False, 'map': False, 'deskZ': -1.25, 'plate': 'SYNDIC',
      'front': 3.6, 'frontSign': {'text': 'SALLE COMMUNE', 'x': 0.0, 'y': 2.45, 'w': 1.7}}
ROW1, ROW2 = 1.0, 1.95                                # the two rows of chairs (the neighbours face -Z, toward the agent)
SEATS = {'mamie': [-0.62, ROW1], 'vide': [0.0, ROW1], 'gamin': [0.62, ROW1], 'voisin': [-0.93, ROW2], 'femme': [-0.31, ROW2], 'madame': [0.31, ROW2], 'retraite': [0.93, ROW2]}
CHAIRS = lambda: [P(f'ch_{n}', 'chair', pos=[x, 0, z + 0.05], ry=180, opts={'color': '#6B4F3A'}) for n, (x, z) in SEATS.items()]
NAMECARD = lambda: P('card', 'nameCard', pos=[0.0, 0.47, ROW1 + 0.02], ry=180, opts={'text': 'REZ-DE-CHAUSSÉE', 'w': 0.44, 'h': 0.17, 'bright': True})
def VOTER(n, up=None, hi=2.25, expr='neutral', reach_k=1.0):   # a neighbour on a chair; up: when the hand goes up
    x, z = SEATS[n]; ks = [STAND(), k(0.0, look=[0.0, 1.6, -2.0])]
    if up is not None: ks += [k(up, toon={'reach': {'R': [round(x - 0.12, 3), hi, round(z - 0.05, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.1, toonEase='outBack')]
    return act(n, [x, 0, z], 180, 'sit', expr, keys=ks)
AGCAM = lambda t=0.0: hcam(t, [0.0, 1.75, -2.4], [[-1.15, 1.9, ROW2], [1.15, 1.9, ROW2], [-0.8, 0.4, ROW1], [0.8, 0.4, ROW1], [0.5, 3.05, ROW1]], top=0.12, bottom=0.82, drift=(0, 0, 0.1))

# 17: yesterday, they voted. The neighbours, on their chairs: hands go up one after another (the lady's, the yellow neighbour's...); the boy's arm
#     stretches up over all of them; in the front row the empty chair
D17 = st.dur('S17')
st.shot('S17', 'mairie', setOpts=AG, actors=[VOTER('mamie', 0.2, expr='happy'), VOTER('voisin', 0.32), VOTER('femme', 0.42), VOTER('madame', 0.5, expr='happy'), VOTER('retraite', 0.58),
        act('gamin', [SEATS['gamin'][0], 0, SEATS['gamin'][1]], 180, 'sit', 'happy', keys=[STAND(), k(0.0, look=[0.0, 1.6, -2.0]),
            k(0.66, toon={'reach': {'R': [0.5, 2.3, ROW1 - 0.05, 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.1, toonEase='outBack'),
            k(0.95, toon={'reach': {'R': [0.5, 3.05, ROW1 - 0.05, 1, 0.06]}, 'hands': {'R': 'spread'}, 'face': {'tongue': 1}}, toonDur=0.14, toonEase='outBack')])],   # higher than everybody
        props=[*CHAIRS(), NAMECARD()],
        cams=[AGCAM()])
[st.cue('whoosh', 'S17', t, 0.12, 0.12, 700, 2200) for t in (0.2, 0.32, 0.42, 0.5, 0.58, 0.66)]; st.cue('sfx:stretch', 'S17', 0.95, 0.3)

# 18: one vote was missing. The agent at his table, the count pinned on the wall behind him: POUR : 5, MAJORITÉ : 6; he taps the 5 with his pen, then
#     his eyes go to the front row
D18 = st.dur('S18')
COUNT = P('count', 'paperSheet', pos=[-0.62, 1.72, -2.56], opts={'w': 0.86, 'h': 0.78, 'head': 'DÉCROCHAGE', 'big': 'POUR : 5', 'bigSize': 0.2, 'lines': ['MAJORITÉ : 6'], 'lineSize': 0.1, 'bright': True})
st.shot('S18', 'mairie', setOpts=AG, actors=[
        act('syndic', [0.25, 0, -1.95], 0, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[-0.62, 1.8, -2.56]),
            k(0.05, toon={'reach': {'R': [-0.42, 1.8, -2.45, 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.12), k(0.3, toon={'reach': {'R': [-0.42, 1.74, -2.48, 1, 0.04]}, 'hands': {'R': 'point'}}, toonDur=0.05),
            k(0.4, toon={'reach': {'R': [-0.42, 1.8, -2.45, 1, 0.04]}, 'hands': {'R': 'point'}}, toonDur=0.05), k(0.5, toon={'reach': {'R': [-0.42, 1.74, -2.48, 1, 0.04]}, 'hands': {'R': 'point'}}, toonDur=0.05),
            k(0.72, look=[0.0, 0.6, ROW1]), k(0.76, toon={'face': {'lid': 0.4, 'browL': 0.7}}, toonDur=0.08)])],
        props=[COUNT, P('pen', 'marker', on={'actor': 'syndic', 'hand': 'R', 'offset': [0, -0.02, 0.06]})],
        cams=[hcam(0.0, [-0.15, 1.75, 1.3], [[-1.05, 2.11, -2.56], [-0.19, 1.33, -2.56], [0.65, 2.42, -1.95], [-0.1, 2.42, -1.95], [0.25, 1.2, -1.95]], top=0.16, bottom=0.7)])
st.cue('sfx:tick', 'S18', 0.3, 0.3); st.cue('sfx:tick', 'S18', 0.5, 0.3)

# 19: his. The empty chair, low and close: the name card REZ-DE-CHAUSSÉE; a tumbleweed rolls across the meeting room
D19 = st.dur('S19')
st.shot('S19', 'mairie', setOpts=AG, actors=[VOTER('mamie', 0.0, expr='neutral'), VOTER('gamin', 0.0, expr='neutral')],
        props=[*CHAIRS(), NAMECARD(), P('weed', 'tumbleweed', pos=[-1.6, 0, ROW1 - 0.62], scale=1.3, keys=[k(0.05, to=[1.6, 0, ROW1 - 0.66], dur=0.85, ease='linear')])],
        cams=[cam(0.0, [0.05, 0.9, -0.55], [0.05, 0.88, -0.48], [0.0, 0.38, ROW1], [0.0, 0.38, ROW1], lens=56)])
st.cue('gust', 'S19', 0.0, 0.25, 0.9)

# 20: he was downstairs. The hall: alone, he votes: his hand goes up, his arm stretches to the ceiling and his hand flattens against it; nobody up there
#     sees it
D20 = st.dur('S20'); UP20 = 0.12
st.shot('S20', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'determined', keys=[STAND(), k(0.0, look=[1.0, 3.6, -2.0]),
            k(UP20, toon={'reach': {'R': [round(ME[0] - 0.22, 3), 3.55, ME[2], 1, 0.06]}, 'hands': {'R': 'spread'}, 'scl': {'handR': [1.35, 0.55, 1.35]}, 'face': {'brow': 0.6}}, toonDur=0.16, toonEase='outBack'),
            k(0.6, look=[1.8, 1.7, 1.0]), k(0.62, expr='unimpressed'), k(0.64, toon={'reach': {'R': [round(ME[0] - 0.22, 3), 3.55, ME[2], 1, 0.06]}, 'hands': {'R': 'spread'}, 'scl': {'handR': [1.35, 0.55, 1.35]}, 'face': {'lid': 0.45}}, toonDur=0.08)])],
        props=[ROPE()],
        cams=[hcam(0.0, [2.1, 1.3, 2.7], [[ME[0] - 0.2, 3.6, ME[2]], FEETME, SEAM, [ME[0] + 0.3, HEAD, ME[2]]], top=0.06, bottom=0.88)])
st.cue('sfx:stretch', 'S20', UP20, 0.35); st.cue('sfx:splat', 'S20', UP20 + 0.16, 0.25)

# 21: they voted the repainting all the same: every hand shoots up at once, the boy's to the ceiling
D21 = st.dur('S21')
st.shot('S21', 'mairie', setOpts=AG, actors=[VOTER('mamie', 0.08, expr='happy'), VOTER('voisin', 0.08), VOTER('femme', 0.08, expr='happy'), VOTER('madame', 0.08, expr='happy'), VOTER('retraite', 0.08),
        act('gamin', [SEATS['gamin'][0], 0, SEATS['gamin'][1]], 180, 'sit', 'happy', keys=[STAND(), k(0.0, look=[0.0, 1.6, -2.0]),
            k(0.08, toon={'reach': {'R': [0.5, 3.05, ROW1 - 0.05, 1, 0.06]}, 'hands': {'R': 'spread'}, 'face': {'tongue': 1}}, toonDur=0.12, toonEase='outBack')])],
        props=[*CHAIRS(), NAMECARD()],
        cams=[AGCAM()])
st.cue('whoosh', 'S21', 0.08, 0.35, 0.15, 500, 2000)

# 22: the repainting. The cut-away, the fourth floor: a house painter on the landing rolls his walls beige and, without a look, the red line with them:
#     the beige runs down it
D22 = st.dur('S22'); RL22 = 0.22
PAINTER = [round(PART - 0.45, 3), 4 * FH, 0.5]
PFRONT = lambda t_hit, y_hit, v=8.0: [round(t_hit - (CABTOP(6) - y_hit) / v, 3), round(t_hit - (CABTOP(6) - y_hit) / v + LEN / v, 3)]   # paint [t0, t1] whose front passes y_hit at t_hit
GRIP22 = lambda y: [round(LINEX - 0.45, 3), round(y, 3), 0.34]   # the grip of his roller; its head rests on the line 0.55 m higher (the roller tilted 39 degrees)
ROLL22 = [(0.0, 4 * FH + 1.2), (RL22, 4 * FH + 0.62), (0.5, 4 * FH + 1.12), (0.78, 4 * FH + 0.66)]   # (t, y of the grip): up and down the line
st.shot('S22', 'immeubleCoupe', setOpts=COUPE(), actors=[
        act('peintre', PAINTER, 90, 'stand', 'happy', keys=[STAND(), k(0.0, look=[LINEX, 4 * FH + 1.6, 0.2]),
            *[k(t, toon={'reach': {'R': [*GRIP22(y), 1, 0.06]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.15, 0, 0, 1, None]}}, toonDur=(0.0 if t == 0.0 else 0.2), toonEase='inOut') for t, y in ROLL22]])],
        props=[ROPEC(items=WASH(0, 0, 0), paint=PFRONT(RL22 + 0.05, 4 * FH + 1.17), color2=BEIGE),
               P('roller', 'paintRoller', pos=GRIP22(ROLL22[0][1]), rot=[0, 0, -0.68], opts={'color': BEIGE, 'len': 0.8},
                 keys=[k(round(t0, 3), to=GRIP22(y1), dur=round(t1 - t0, 3), ease='inOut') for (t0, _), (t1, y1) in zip(ROLL22, ROLL22[1:])]),   # free, its head on the line, his hand on its grip (in his hand it pointed into the wall)
               P('notes', 'whistleNotes', pos=[PAINTER[0] + 0.1, 4 * FH + 2.25, 0.6], opts={'n': 3, 'from': 0.0, 'every': 0.25, 'size': 0.16, 'dx': -0.3, 'dy': 0.6, 'life': 0.6, 'color': '#1B1B1E'})],
        cams=[coupecam(0.0, 12.45, 12.38, d=4.4, x=1.25)])
st.cue('sfx:whistle', 'S22', 0.0, 0.3)

# 23: his tie is beige. The hall: the beige comes out of the seam along the leash to his collar; his knot goes beige; he looks down at it, cross-eyed;
#     a double take; at us
D23 = st.dur('S23'); AR23 = 0.36
KB = {'knot': BEIGE}                                  # his knot, beige from now on (toon channel `knot`: every key after it carries it)
st.shot('S23', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[1.8, 1.7, 1.0]),
            k(AR23 + 0.04, look=[ME[0], 1.1, ME[2] + 0.4]), k(AR23, toon={**KB}, toonDur=0.0), k(AR23 + 0.06, toon={**KB, 'face': {'gx': 0.0, 'gy': 0.8, 'brow': 0.4}}, toonDur=0.08),           # down at his knot
            k(0.78, look=[1.8, 1.7, 1.0]), k(0.78, toon={**KB, 'face': {'pop': 0.75, 'brow': 1, 'eye': 0.5}}, toonDur=0.06, toonEase='outBack'),           # the take
            k(1.02, toon={**KB, 'face': {'pop': 0.0, 'lid': 0.45, 'browL': 0.6}}, toonDur=0.1)])],
        props=[ROPE(paint=[0.0, AR23], color2=BEIGE)],
        cams=[hcam(0.0, [2.0, 1.75, 0.2], [[ME[0] + 0.2, HEAD + 0.06, ME[2]], [ME[0], 1.05, ME[2]], SEAM, DISP], top=0.18, bottom=0.72)])
st.cue('sfx:pour', 'S23', 0.0, 0.25); st.cue('pop', 'S23', AR23, 0.3); st.cue('sfx:spring', 'S23', 0.78, 0.3)

# 24: he pays the service charges. An envelope comes out of the seam and zips down the leash; it smacks the back of his head; he reaches back for it
D24 = st.dur('S24'); OUT24, HIT24, GRAB24 = 0.06, 0.5, 0.76   # (the envelope faces us and flies longer: edge-on and in 0.3 s it did not show)
NAPEW = [round(ME[0] - 0.08, 3), 1.66, round(ME[2] - 0.2, 3)]
st.shot('S24', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[1.8, 1.7, 1.0]), k(0.0, toon={**KB, 'face': {'lid': 0.45, 'browL': 0.6}}, toonDur=0.0),
            k(HIT24, toon={**KB, 'bend': {'neck': [0.45, 0, 0, 1, None]}, 'scl': {'head': [1.12, 0.86, 1.12]}, 'face': {'pop': 0.6, 'brow': 1, 'eye': 0.5}}, toonDur=0.04, toonEase='out'),   # thwack
            k(HIT24 + 0.12, toon={**KB, 'face': {'pop': 0.0, 'lid': 0.45, 'browL': 0.7}}, toonDur=0.1),
            k(GRAB24 - 0.12, toon={**KB, 'reach': {'L': [NAPEW[0] - 0.05, 1.75, NAPEW[2] - 0.05, 1, 0.08]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.45}}, toonDur=0.12),
            k(GRAB24 + 0.18, toon={**KB, 'reach': {'L': [ME[0] - 0.1, 1.45, ME[2] + 0.35, 1, 0.08]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.45}}, toonDur=0.16), k(GRAB24 + 0.2, look=[ME[0] - 0.1, 1.45, ME[2] + 0.45])])],
        props=[ROPE(color=BEIGE, pluck=[[HIT24, 0.03, 10, 14, 6]]),
               P('bill', 'paperSheet', pos=[0.05, 1.6, -2.86], ry=30, scale=0.01, opts={'w': 0.3, 'h': 0.19, 'head': 'CHARGES', 'headSize': 0.32, 'top': 0.42, 'paper': '#F1E6CC'},
                 keys=[k(OUT24 - 0.04, scale=1.25, dur=0.06, ease='out'), k(OUT24, to=[NAPEW[0] - 0.02, NAPEW[1] + 0.04, NAPEW[2] - 0.06], dur=round(HIT24 - OUT24, 3), ease='in'), k(HIT24, squash=[1.3, 0.7, 1.0], dur=0.2),
                       k(GRAB24, attach='mec', hand='L', offset=[0, 0, 0.05])])],
        cams=[hcam(0.0, [2.05, 1.7, 0.5], [[ME[0] + 0.25, HEAD + 0.06, ME[2]], [ME[0], 0.95, ME[2]], SEAM, DISP], top=0.18, bottom=0.74)])
st.cue('sfx:zip', 'S24', OUT24, 0.4); st.cue('sfx:bonk', 'S24', HIT24, 0.5); st.cue('sfx:paper', 'S24', GRAB24, 0.3)

# 25: close: he reads it: CHARGES DU RDC, 1 240 €: le ravalement, le séchage du linge; his eye twitches; down the leash, the boy's last note shakes
#     him one more time
D25 = st.dur('S25'); TW25, WB25 = 0.62, 1.05
st.shot('S25', 'immeubleHall', setOpts=HALL(), actors=[
        act('mec', ME, MERY, 'stand', 'unimpressed', keys=[STAND(), k(0.0, look=[ME[0] - 0.05, 1.4, ME[2] + 0.5]),
            k(0.0, toon={**KB, 'reach': {'L': [ME[0] - 0.2, 1.42, ME[2] + 0.38, 1, 0.08], 'R': [ME[0] + 0.16, 1.42, ME[2] + 0.38, 1, 0.08]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(TW25, toon={**KB, 'reach': {'L': [ME[0] - 0.2, 1.42, ME[2] + 0.38, 1, 0.08], 'R': [ME[0] + 0.16, 1.42, ME[2] + 0.38, 1, 0.08]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lidL': 0.9, 'lidR': 0.4, 'browL': 0.8}}, toonDur=0.03),
            k(TW25 + 0.06, toon={**KB, 'reach': {'L': [ME[0] - 0.2, 1.42, ME[2] + 0.38, 1, 0.08], 'R': [ME[0] + 0.16, 1.42, ME[2] + 0.38, 1, 0.08]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.03),
            k(TW25 + 0.12, toon={**KB, 'reach': {'L': [ME[0] - 0.2, 1.42, ME[2] + 0.38, 1, 0.08], 'R': [ME[0] + 0.16, 1.42, ME[2] + 0.38, 1, 0.08]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lidL': 0.9, 'lidR': 0.4, 'browL': 0.8}}, toonDur=0.03),
            k(TW25 + 0.18, toon={**KB, 'reach': {'L': [ME[0] - 0.2, 1.42, ME[2] + 0.38, 1, 0.08], 'R': [ME[0] + 0.16, 1.42, ME[2] + 0.38, 1, 0.08]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.03),
            k(WB25, clip='jelly', params={'amp': 0.18, 'freq': 20, 'decay': 6}), k(1.4, look=[1.8, 1.72, 1.0])])],
        props=[ROPE(color=BEIGE, pluck=[[WB25 - 0.15, 0.05, 7, 14, 4]]),
               P('billopen', 'paperSheet', pos=[round(ME[0] - 0.02, 3), 1.42, round(ME[2] + 0.4, 3)], ry=11, rot=[-0.12, 0, 0], opts={'w': 0.36, 'h': 0.46, 'head': 'CHARGES DU RDC', 'big': '1 240 €', 'bigSize': 0.15,
                                                                                                                 'lines': ['Ravalement', 'Séchage du linge'], 'lineSize': 0.07, 'bright': True})],   # free, facing us, his hands at its edges (held in a hand it was seen edge-on)
        cams=[hcam(0.0, [1.8, 1.72, 0.3], [[ME[0] + 0.15, HEAD + 0.05, ME[2]], [ME[0], 1.18, ME[2] + 0.4], [ME[0] - 0.45, 1.58, ME[2] - 0.3]], top=0.16, bottom=0.74, drift=(-0.02, 0, -0.08))])
st.cue('sfx:cash', 'S25', 0.1, 0.35); st.cue('sfx:twang', 'S25', WB25 - 0.15, 0.3)

st.write("La cravate", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'tieKnot': True, 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'voisin': {'preset': 'fringant', 'seed': 161, 'build': {'width': 0.85, 'headWidth': 1.25}},
    'syndic': {'preset': 'boss', 'seed': 37, 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'mamie': {'preset': 'mamie', 'seed': 52, 'build': {'headWidth': 1.2}},
    'gamin': {'preset': 'gamin', 'seed': 18, 'build': {'height': 0.68, 'headWidth': 1.3}},
    'peintre': {'preset': 'worker', 'seed': 77, 'build': {'width': 0.9, 'headWidth': 1.2}},
    'femme': {'preset': 'femme', 'seed': 23},
    'madame': {'preset': 'madame', 'seed': 31},
    'retraite': {'preset': 'lemec_beige', 'seed': 64, 'build': {'width': 0.9, 'headWidth': 1.2}}})
