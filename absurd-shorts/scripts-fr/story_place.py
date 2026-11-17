#!/usr/bin/env python3
"""La place (story 85, cycle 47; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man had his parking space taken at the supermarket. The army confirmed the invasion. The navy imposed a blockade on the roundabout.
Ultimatum: ten minutes to surrender. The invader was in the cheese aisle. Six planes bombed his car. And the two hundred spaces round it. The
supermarket too. It was badly parked. The invader was put under witness protection. The space was retaken. Three thousand soldiers paraded on
it. The other countries called a summit. The summit lasted forty laps. The treaty declared the space a neutral zone. Every country parked a
tank in it. This man pays the war reparations. The blockade was never lifted. He parks in the neighbouring country.
Staging: from behind his blue car, indicator blinking, a small red car zips in from the far end and swerves into the last free bay one second
before him; he brakes hard (nose dip); through his windscreen, eyes wide, then a deadpan glare. In a war room a general stabs a red flag-pin
into the red toy car on a map of the car park while he stands beside him pointing at it. A grey warship sits on the roundabout's grassy island;
striped booms slam down across every exit and its gun turret swings to check each car as it goes round. A giant red countdown clock on the
supermarket roof flips to 10:00 and starts ticking while soldiers march the shoppers out with their full trolleys; a tank aims at the doors.
Alone in the emptied cheese aisle, the red car's driver sniffs a big plain cheese wheel while a red laser dot wanders over his shoulder. Six
fighter jets roar over the car park and six bombs fall on the little red car. Aerial: every car flat as a pancake in its bay, smoking in neat
rows, a hubcap rolling, his blue car untouched in the lane with its indicator still blinking, the shoppers safe behind a barrier watching. The
empty supermarket folds flat like a cardboard box, its sign and clock tipping onto the pile, the dust greying the invader standing outside with
his cheese (PLIÉ). Two masked special forces walk the grey invader, a blanket over his head, to a black car while he points in outrage beside
his blinking car. In the swept, empty bay a soldier drives a flagpole straight down and he salutes proudly (REPRISE). Soldiers and a band march
in a tight loop inside that one bay round the flag while he salutes at its edge. A queue of black official cars with little flags waits at a
striped boom while the warship's gun checks them one by one. The black cars circle the warship nose to tail, leaders in sashes leaning out of
their windows to pass the treaty pages back, and a lap counter on the bridge clicks to 40. Back at the bay, the leaders run striped tape round
its white lines while he slowly lowers his salute (NEUTRE). A tower of tanks, each with its own little flag, stands in the taped bay beside his
blinking car. He shakes his empty wallet over a general's upturned helmet while a line of soldiers holding out their helmets stretches across
the flattened car park to the horizon. Months later: tall grass round the booms, the warship still on its island; his car waits at the give-way
line, indicator blinking, and the gun swings round and stops on him. At a border post he ducks under the striped barrier toward us with a
shopping bag in each hand while, far behind, his car sits tiny in a lone painted bay under another flag, its indicator still blinking.
Natural look; cycle 47: props_place.js (parkLot, bayCar, flatRows, parkedRows, superStore, countdownClock, warMap, flagPin, warship, ringRoad,
plainCheese, cheeseShelf, laserDot, bombDrop, hubcap, tankTower, bayFlag, borderPost, bayTape, fullTrolley, emptyWallet, helmetLine);
battleTank (props_bocal), fighterJet, timedBurst (props_flaque), softDust, softWisp (props_barbecue), armyHelmet, treatySheet (props_guepe),
balaclava, rifle (props_rambarde), blanketDrape (props_porte), bandInstr, epaulettes (props_centime), kepi (props_conseiller), shoppingBag,
crowdBarrier (props_news) reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.86) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; flat
grounds raised (the asphalt top at 0.06); horizontal actions staged in depth (the 9:16 frame is only ~2 m wide at 4-5 m); two faces in a V;
nobody shown hurt (the shoppers evacuated and safe, the invader outside before the store folds); no English, no real flags or brands."""
from story_kit import *
import math

st = Story('place', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 19)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
def loc(p, ry, lx, lz, y=0.0):
    """a point in the frame of a prop at p turned ry degrees (local +X, +Z), y up"""
    a = math.radians(ry); return [r(p[0] + lx * math.cos(a) + lz * math.sin(a)), r(p[1] + y), r(p[2] - lx * math.sin(a) + lz * math.cos(a))]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
GY = 0.06                                              # the asphalt's top
CS = 1.25                                              # the size of the cars (the cast is 2.3 m tall)

# ---- the car park (world A): the asphalt x -32..32, z -19..33; the supermarket's front wall at z -15.5 (x -14..14); rows of bays 2.5 m wide:
#      A (z -13..-8, noses to the store), lane A (z -8..-2), B and C back to back, lane B, D and E; the KEY bay is A's 11th (x 0..2.5)
STORE_Z = -15.5
ROWS = [(-10.5, -23.75, 20, -1), (0.5, -23.75, 20, 1), (5.5, -23.75, 20, -1), (16.5, -23.75, 20, 1), (21.5, -23.75, 20, -1)]
KEY = [1.25, GY, -10.6]; KEYC = [1.25, GY, -10.5]
LANE_A = -5.4
BLUE = '#5E8FD0'; BLUE_PLATE = 'GH-485-PL'
HERO_CAR = [5.7, GY, LANE_A]                           # where his car stops, nose -X, its right side to row A
LOT = lambda: P('parking', 'parkLot', pos=[0, 0, 7.0], opts={'w': 64, 'd': 52, 'rows': [[z, x0, n, 5] for (z, x0, n, _) in ROWS], 'lamps': [[-12.5, -5.0], [12.5, -5.0], [-12.5, 11.0], [12.5, 11.0], [-12.5, 27.0], [12.5, 27.0]],
                                                         'zebra': [0.0, -14.4, 5.0], 'arrows': [[-8, LANE_A + 0.2, -PI / 2], [9, 11.2, PI / 2]]})
def ROWS_INTACT(skip=()): return P('rangees', 'parkedRows', pos=[0, 0, 0], opts={'rows': [list(x) for x in ROWS], 'skip': list(skip), 's': CS, 'y': GY})
def ROWS_FLAT(skip=(), wisps=10): return P('epaves', 'flatRows', pos=[0, 0, 0], opts={'rows': [list(x) for x in ROWS], 'skip': list(skip), 'y': GY, 'wisps': wisps})
def STORE(**o): return P('magasin', 'superStore', pos=[0, 0, STORE_Z], opts={'w': 28, 'd': 14, 'h': 6.5, **o})
def CAR(pid, pos, ry, **o):
    keys = o.pop('keys', None); d = P(pid, 'bayCar', pos=pos, ry=ry, scale=o.pop('scale', CS), opts=o)
    if keys: d['keys'] = keys
    return d
HEROCAR = lambda pid='voiture', pos=None, ry=-90, **o: CAR(pid, pos or HERO_CAR, ry, **{'color': BLUE, 'plate': BLUE_PLATE, 'blink': 'R', 'indS': 1.6, 'glow': 0.75, 'blinkP': 0.55, **o})   # (round 1) bigger lamps, 1.8 Hz
LOT_SET = {'clouds': 34, 'grass': '#86BE5C'}
CLOCK0 = 600.0                                         # ten minutes, from the flip in S04
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'bald',
        'gloves': '#2E3320', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.2, 'shift': 2.0, 'breathe': 2.0}}
SPEC = {'outfit': 'suit', 'suit': '#4A5160', 'pants': '#3C424E', 'shirt': '#4A5160', 'lapel': '#2C3038', 'tie': '#2C3038', 'cuff': '#4A5160', 'hat': 'none', 'hair': 'bald', 'gloves': '#16171A',
        'facial': 'none', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
HELMET = lambda pid, who, **o: P(pid, 'armyHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95, **o})
KEPI = lambda pid, who: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5730', 'band': '#2E3320'})
BALA = lambda pid, who: P(pid, 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
SALUTE = lambda p, ry: [*off(p, ry, 0.08, 0.2, 2.02), 1, 0.03]   # the flat right hand at the temple, standing
def stand_blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]

for g_ in [('S01', 1.9, 'mec', 'glare'), ('S02', 1.05, 'general', 'stab'), ('S05', 0.9, 'envahisseur', 'sniff'), ('S09', 1.2, 'mec', 'point'), ('S10', 0.9, 'mec', 'salute'), ('S14', 1.9, 'mec', 'lower')]:
    st.gag(*g_)

# 1: the hook. Two angles. (a) Low behind his blue car, its right indicator blinking: far down the lane a small red car zips toward us and swerves
#    left into the last free bay, one second before him; his car brakes hard, its tail kicking up. (b) Through his windscreen: he grips the wheel,
#    eyes wide, his head turns to the bay, then back to us, a deadpan glare; the indicator still blinking at the corner of the frame
D1 = st.dur('S01'); CUT1 = 1.12; STOP1 = 1.0; BRAKE1 = 0.82
START1 = [12.0, GY, LANE_A]
RED_PATH = [[-3.0, GY, -4.6], [-0.4, GY, -5.2], [0.9, GY, -7.4], [1.25, GY, -9.6], KEY]
SEAT = lambda p, ry: loc(p, ry, 0.36 * CS, 0.06, 0.0)   # the driver's seat (the car's left, +X local), at the floor
HERO_SIT1 = SEAT(HERO_CAR, -90)
CA1 = cam(0.0, [13.2, 4.0, -3.3], [12.95, 3.9, -3.4], [1.6, 0.4, -9.6], [1.6, 0.35, -9.6], lens=50)
CB1 = cam(CUT1, [0.6, 1.85, -4.9], [0.75, 1.84, -4.85], [HERO_SIT1[0], 1.55, HERO_SIT1[2]], [HERO_SIT1[0], 1.55, HERO_SIT1[2]], lens=58)   # (round 1) wider: his near front indicator blinks at the lower right
chk('S01a', CA1['from'], CA1['lookAt'], 40, {'heroCarRear': loc(START1, -90, 0, -2.3, 0.8), 'heroCarStop': loc(HERO_CAR, -90, -0.9, -2.3, 0.8), 'bay': [1.25, 0.6, -10.6], 'redStart': [-14, 0.8, -4.7]})
chk('S01b', CB1['from'], CB1['lookAt'], 58, {'face': [HERO_SIT1[0], 1.75, HERO_SIT1[2]], 'blinkFR': loc(HERO_CAR, -90, -0.74 * CS, 1.85 * CS, 0.76 * CS), 'blinkFL': loc(HERO_CAR, -90, 0.74 * CS, 1.85 * CS, 0.76 * CS), 'sideL': loc(HERO_CAR, -90, 0.85 * CS, 1.3 * CS, 0.8 * CS)})
st.shot('S01', 'grassland', setOpts=LOT_SET, actors=[
        act('mec', SEAT(START1, -90), -90, 'drive', 'neutral', keys=[k(0.0, to=HERO_SIT1, dur=STOP1, ease='out', glide=True, face='keep', clip='drive'), k(0.0, look=[1.25, 1.0, -10.6]),
            k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(r(CUT1 + 0.05), toon={'face': {'lid': 0.0, 'pop': 0.45, 'mouth': 'O', 'brow': 0.7}, 'sq': [1.06, 0.95, 1.06]}, toonDur=0.05),   # (round 1) a squash, not a stretch: the stretch put his hair through the roof
            k(r(CUT1 + 0.3), look=[1.0, 1.2, -9.5], lookDur=0.12), k(r(CUT1 + 0.3), toon={'face': {'lid': 0.15, 'pop': 0.1, 'mouth': 'O', 'brow': 0.4}, 'sq': [1, 1, 1]}, toonDur=0.12),
            k(r(CUT1 + 0.72), look='camera', lookDur=0.1), k(r(CUT1 + 0.72), toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.35}}, toonDur=0.1),
            *stand_blink(r(CUT1 + 1.0), {'lid': 0.45, 'mouth': 'line', 'brow': -0.35})]),
        act('voleur', add(RED_PATH[0], [-12.0, 0, 0]), 90, 'drive', 'smug', visible=False)],
        props=[LOT(), ROWS_INTACT(skip=['0:10']), STORE(clock=None),
               HEROCAR('voiture', START1, clear=True, blink='both', brake=[BRAKE1, 0.45], keys=[k(0.0, to=HERO_CAR, dur=STOP1, ease='out')]),
               CAR('rouge', [-9.0, GY, -4.6], 90, color='#D8392B', plate='RX-001-ZZ', scale=1.0, hop=[[1.0, 0.07]],
                   keys=[k(0.0, path=RED_PATH, dur=1.0, ease='inOut', faceMove=True)])],
        cams=[CA1, CB1])
st.cue('engine', 'S01', 0.0, 0.25, 1.0); st.cue('sfx:brake', 'S01', BRAKE1, 0.5); st.cue('sfx:tick', 'S01', 0.1, 0.15); st.cue('sfx:tick', 'S01', 0.8, 0.15); st.cue('sfx:tick', 'S01', 1.5, 0.15); st.cue('sfx:gasp', 'S01', r(CUT1 + 0.05), 0.2)

# 2: the army confirmed the invasion. The war room: across a dark map table printed with the car park, the general (kepi, epaulettes), three
#    quarters to us on the left, winds up and stabs a red flag-pin into the red toy car in its bay; he stands stiffly on the right, three quarters
#    to us, pointing at it; the general straightens, satisfied
D2 = st.dur('S02'); STAB2 = 1.0
TAB2 = [0.0, 0, -1.2]; RED2 = [0.16, -0.14]            # the red toy car on the table (table frame)
TOY2 = [r(TAB2[0] + RED2[0]), 0.92, r(TAB2[2] + RED2[1])]
GEN2 = [-0.55, 0, -1.9]; RYG2 = 24; HERO2 = [0.6, 0, -2.0]; RYH2 = -22
C2 = cam(0.0, [0.3, 2.45, 3.9], [0.29, 2.43, 3.7], [-0.165, 0.62, -5.914], [-0.165, 0.63, -5.914], lens=29)   # (round 1) tilted down: the toy car sat in the caption band
chk('S02', C2['from'], C2['lookAt'], 46, {'genFace': [GEN2[0], 1.95, GEN2[2]], 'heroFace': [HERO2[0], 1.95, HERO2[2]], 'toy': TOY2})
def PT2(d):
    """(round 1) a point d metres from his right shoulder along the line to the toy car: his arm straight out, pointing down at it"""
    sh = off(HERO2, RYH2, 0.0, 0.25, 1.72); v = [TOY2[i] - sh[i] for i in range(3)]; n = math.sqrt(sum(x * x for x in v)); return [r(sh[i] + v[i] / n * d) for i in range(3)]
def GK(t, hp, sq=(1, 1, 1), face=None, d=0.12, e='inOut', hand='grip', bend=0.0):
    return k(t, toon={'reach': {'R': [*hp, 1, 0.03]}, 'hands': {'R': hand}, 'sq': list(sq), 'bend': {'spine': [bend, 0, 0, 1, None]}, 'face': face or {'lid': 0.3, 'mouth': 'clench', 'brow': -0.6}}, toonDur=d, toonEase=e)
st.shot('S02', 'office', setOpts={'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#4A5866', 'band': '#2E3A46', 'trim': '#1E262E'}, actors=[
        act('general', GEN2, RYG2, 'stand', 'angry', keys=[k(0.0, look=add(TOY2, [0, 0.1, 0])),
            GK(0.0, add(TOY2, [-0.25, 0.75, 0.05]), d=0.0), GK(0.45, add(TOY2, [-0.2, 1.05, 0.1]), (0.95, 1.06, 0.95), d=0.3, e='out'),
            GK(r(STAB2 - 0.07), add(TOY2, [-0.02, 0.45, 0.0]), (0.97, 1.03, 0.97), d=0.05, e='in', bend=0.15),
            GK(STAB2, add(TOY2, [0.0, 0.27, 0.0]), (1.08, 0.92, 1.08), {'lid': 0.1, 'mouth': 'clench', 'brow': -0.8}, d=0.04, e='out', bend=0.25),
            GK(r(STAB2 + 0.35), add(TOY2, [-0.3, 0.6, 0.15]), face={'lid': 0.4, 'mouth': 'smile', 'brow': 0.1}, d=0.25, hand='rest', bend=0.0),
            k(r(STAB2 + 0.5), look='camera', lookDur=0.15), k(r(STAB2 + 0.6), toon={'face': {'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}, 'bend': {'neck': [0.15, 0, 0, 1, None]}}, toonDur=0.15, keepPose=True),
            k(r(STAB2 + 0.8), toon={'face': {'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}, 'bend': {'neck': [0.0, 0, 0, 1, None]}}, toonDur=0.15, keepPose=True)]),
        act('mec', HERO2, RYH2, 'stand', 'unimpressed', keys=[k(0.0, look=TOY2), k(0.0, toon={'reach': {'R': [*PT2(0.62), 1, 0.12]}, 'hands': {'R': 'point'}, 'face': DEAD, 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(STAB2 + 0.02), toon={'reach': {'R': [*PT2(0.68), 1, 0.12]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, 'sq': [0.98, 1.02, 0.98], 'bend': {'spine': [0.15, 0, 0, 1, None]}}, toonDur=0.06),
            k(r(STAB2 + 0.3), look='camera', lookDur=0.2), *stand_blink(1.45)])],
        props=[P('table2', 'warMap', pos=TAB2, opts={'red': RED2, 'blue': [0.42, 0.02]}),
               P('epingle2a', 'flagPin', on={'actor': 'general', 'hand': 'R', 'offset': [0.0, -0.06, 0.02], 'rot': [3.1416, 0, 0]}, keys=[k(0.0, visible=True), k(r(STAB2 - 0.02), visible=False)]),
               P('epingle2', 'flagPin', pos=add(TOY2, [0, 0.03, 0]), keys=[k(0.0, visible=False), k(r(STAB2 - 0.02), visible=True)], opts={'s': 1.3}),
               KEPI('kepi2', 'general'), P('epaul2', 'epaulettes', on={'actor': 'general', 'joint': 'torso', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.52})],
        fx=[{'type': 'shake', 'at': STAB2, 'dur': 0.12, 'amount': 0.01}],
        cams=[C2])
st.cue('whoosh', 'S02', r(STAB2 - 0.15), 0.18); st.cue('thud', 'S02', STAB2, 0.45)

# 3: the navy imposed a blockade on the roundabout. Low on the approach road: a grey warship sits on the roundabout's grassy island, bow to us;
#    cars go round it; the striped boom across our exit slams down in the foreground (and on every exit), and the ship's gun turret swings to
#    follow each car that passes
RING = [48.0, 0, 36.5]; RI, RO = 6.5, 13.0
SHIP = [RING[0], 0.23, RING[2]]; SHIP_RY = -90          # bow to the west (-X), toward the car park's road
D3 = st.dur('S03'); SLAM3 = 0.95
def ring_pos(a_deg, rad=10.95): a = math.radians(a_deg); return [r(RING[0] + rad * math.sin(a)), GY, r(RING[2] + rad * math.cos(a))]
def turret_yaw(p):
    """the yaw of the ship's turret (0 ahead, + to its left) that points at p"""
    tp = loc(SHIP, SHIP_RY, 0, 2.4); dx, dz = p[0] - tp[0], p[2] - tp[2]; F = fwd(SHIP_RY); L = [-right(SHIP_RY)[0], 0, -right(SHIP_RY)[2]]
    return r(math.atan2(dx * L[0] + dz * L[2], dx * F[0] + dz * F[2]), 3)
CARS3 = [{'color': '#F2C94C', 'a0': 200}, {'color': '#E8E4DA', 'a0': 255}, {'color': '#7FB069', 'a0': 320}, {'color': '#D98AA8', 'a0': 40}]
SP3 = 30.0
AIM3 = [[0.0, turret_yaw(ring_pos(255 + SP3 * 0.0))]] + [[r(t), turret_yaw(ring_pos(255 + SP3 * t))] for t in (0.4, 0.8, 1.2)] + [[1.5, turret_yaw(ring_pos(320 + SP3 * 1.6))], [1.9, turret_yaw(ring_pos(320 + SP3 * 2.0))]]
C3 = cam(0.0, [30.4, 1.1, 36.8], [30.7, 1.12, 36.78], [48.0, 3.9, 36.5], [48.0, 3.95, 36.5], lens=40)   # (round 1) on the ship's axis: bow-on, whole, little sky
chk('S03', C3['from'], C3['lookAt'], 40, {'mast': loc(SHIP, SHIP_RY, 0, -1.4, 6.4), 'bow': loc(SHIP, SHIP_RY, 0, 5.9, 1.5), 'boom': [35.0, 1.0, 36.5], 'boomR': [35.0, 1.0, 39.5], 'island': [RING[0] - RI, 0.2, RING[2]]})
st.shot('S03', 'grassland', setOpts=LOT_SET, actors=[],
        props=[P('rondpoint3', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': SLAM3, 'cars': CARS3, 'speed': SP3}),
               P('navire3', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': AIM3, 'aimBlend': 0.22, 'gunS': 1.7}),
               P('route3', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}), LOT()],
        fx=[{'type': 'shake', 'at': SLAM3, 'dur': 0.15, 'amount': 0.012}],
        cams=[C3])
st.cue('sfx:honk', 'S03', 0.2, 0.15); st.cue('clang', 'S03', SLAM3, 0.5); st.cue('sfx:rattleShort', 'S03', r(SLAM3 + 0.05), 0.25); st.cue('engine', 'S03', 1.1, 0.18, 0.8)

# 4: ultimatum, ten minutes to surrender. The supermarket front seen low from the car park: a giant red countdown clock on the roof flips on to
#    10:00 and starts ticking; soldiers march the shoppers out, each pushing a full trolley, toward us; a tank in the foreground aims its gun at
#    the doors
D4 = st.dur('S04'); FLIP4 = 0.25
CLK = {'x': 0.0, 'base': CLOCK0, 'flipAt': FLIP4}
SHOP4 = [('client1', [-1.8, GY, -13.6], [-3.0, GY, -9.8]), ('client2', [-0.6, GY, -14.6], [-1.7, GY, -11.0]), ('client3', [-3.1, GY, -14.9], [-4.2, GY, -11.3])]
SOL4 = [('soldat1', [-0.2, GY, -15.3], [-0.9, GY, -12.4]), ('soldat2', [-4.4, GY, -15.4], [-5.3, GY, -12.6])]
C4 = cam(0.0, [-2.4, 1.6, -4.9], [-2.38, 1.62, -5.15], [-0.6, 3.8, -15.5], [-0.6, 3.85, -15.5], lens=58)   # (round 1) a little less tilt: the tank's gun above the captions
TANK4 = [0.6, GY, -12.0]; TANK4_RY = yaw(TANK4, [0.0, 0, -15.5])
chk('S04', C4['from'], C4['lookAt'], 58, {'clock': [0.0, 10.4, STORE_Z - 1.0], 'sign': [0, 8.0, STORE_Z - 0.4], 'door': [0, 1.5, STORE_Z], 'shopNear': [-3.0, 2.3, -9.8], 'shopNearFeet': [-3.0, 0.0, -9.8], 'tank': [0.6, 1.2, -12.0], 'gunTip': [0.3, 1.2, -13.8], 'redcar': [1.25, 1.3, -10.6]})
def TROLLEY(pid, a, b, dur):
    """a full trolley rolling ahead of a shopper from a to b (0.95 m in front of him), its handle toward him"""
    h = math.atan2(b[0] - a[0], b[2] - a[2]); f = [math.sin(h) * 0.95, 0, math.cos(h) * 0.95]
    return P(pid, 'fullTrolley', pos=add(a, f), keys=[k(0.0, path=[add(b, f)], dur=dur, ease='linear', faceMove=True, yawOffset=-90)])
st.shot('S04', 'grassland', setOpts=LOT_SET, actors=[
        *[act(w, a, yaw(a, b), 'stand', 'scared', keys=[k(0.0, to=b, dur=D4, clip='pushCartWalk'), k(0.0, look=[9.6, 1.8, -2.4])]) for w, a, b in SHOP4],
        *[act(w, a, yaw(a, b), 'stand', 'angry', keys=[k(0.0, to=b, dur=D4, clip='walk'), k(0.0, toon={'reach': {'R': [*off(b, yaw(a, b), 0.45, 0.05, 1.45), 1, 0.04], 'L': [*off(b, yaw(a, b), 0.35, -0.2, 1.35), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)])
          for w, a, b in SOL4]],
        props=[LOT(), ROWS_INTACT(skip=['0:7', '0:8', '0:9', '0:10', '0:11', '0:12', '0:13']), STORE(clock=CLK), CAR('rouge4', KEY, 180, color='#D8392B', plate='RX-001-ZZ', scale=1.0),
               P('char4', 'plainTank', pos=TANK4, ry=TANK4_RY, scale=0.6, opts={'turret': [[0, 0.06], [0.9, -0.05], [1.5, 0.04]], 'rumble': [[0.0, 2.4, 0.01]]}),   # (round 1) the tank aiming at the doors
               *[TROLLEY(f'chariot4{i}', a, b, D4) for i, (w, a, b) in enumerate(SHOP4)],
               *[HELMET(f'casque4{i}', w) for i, (w, a, b) in enumerate(SOL4)], *[P(f'fusil4{i}', 'rifle', on={'actor': w, 'hand': 'R', 'offset': [0, -0.05, 0.05]}) for i, (w, a, b) in enumerate(SOL4)],
               ],
        cams=[C4])
st.cue('sfx:tick', 'S04', r(FLIP4 + 0.02), 0.35); st.cue('sfx:ticks', 'S04', r(FLIP4 + 0.4), 0.2); st.cue('sfx:stepHeavy', 'S04', 0.5, 0.15); st.cue('sfx:rattle', 'S04', 0.2, 0.12)

# 5: the invader was in the cheese aisle. Inside the emptied supermarket, alone in front of the cheese fridge, the red car's driver (red blazer)
#    holds a big plain cheese wheel to his nose with both hands and sniffs it, eyes closed in bliss, three quarters to us; a thin red laser beam
#    comes in from the right and its dot wanders over his shoulder and up the side of his head
D5 = st.dur('S05'); SNIFF5 = 0.55
INV5 = [-0.15, 0, -1.65]; RY5 = -6
# (round 1) turned a little away from the lens (a three-quarter face, his left temple to us); the wheel held up at his nose (it sat at his belly), his head tilted down into it on the inhale, the laser dot on his visible (left) temple
NOSE5 = off(INV5, RY5, 0.42, 0.0, 1.95)
CH5A = off(INV5, RY5, 0.46, 0.0, 1.62); CH5B = off(INV5, RY5, 0.33, 0.0, 1.74)          # the middle of the wheel's back face (its pivot), before and on the sniff: its top edge at his nose
C5 = cam(0.0, [0.95, 1.85, 1.25], [0.88, 1.85, 1.1], [-0.15, 1.88, -1.6], [-0.15, 1.9, -1.6], lens=44)
chk('S05', C5['from'], C5['lookAt'], 44, {'face': [INV5[0], 1.98, INV5[2]], 'cheese': CH5B, 'templeL': off(INV5, RY5, 0.0, -0.21, 2.02), 'sign': [0, 2.35, -3.4]})
TL5 = lambda f, s_, y: off(INV5, RY5, f, s_, y)
DOT5 = [[0.0, *TL5(0.04, -0.36, 1.5)], [0.45, *TL5(0.1, -0.34, 1.7)], [0.85, *TL5(0.04, -0.27, 1.92)], [1.15, *TL5(0.0, -0.215, 2.02)], [2.1, *TL5(0.0, -0.215, 2.05)]]
HOLD5 = lambda f, y, sq=0.25: {'R': [*off(INV5, RY5, f, sq, y), 1, 0.03], 'L': [*off(INV5, RY5, f, -sq, y), 1, 0.03]}
st.shot('S05', 'supermarket', setOpts={'fr': True, 'signs': [['FROMAGES', '#2E6FB5', '#FFFFFF', -2.6, -3.2]]}, actors=[
        act('envahisseur', INV5, RY5, 'stand', 'happy', keys=[k(0.0, look=NOSE5),
            k(0.0, toon={'reach': HOLD5(0.46, 1.62), 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.0),
            k(r(SNIFF5 - 0.15), toon={'reach': HOLD5(0.44, 1.64), 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.6, 'mouth': 'O', 'brow': 0.2}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.12),
            k(SNIFF5, toon={'reach': HOLD5(0.33, 1.74), 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'smile', 'brow': 0.6, 'cheeks': 0.5}, 'sq': [0.93, 1.09, 0.93], 'bend': {'spine': [0.08, 0, 0, 1, None], 'neck': [0.32, 0, 0, 1, None]}}, toonDur=0.2, toonEase='out'),
            k(r(SNIFF5 + 0.5), toon={'reach': HOLD5(0.33, 1.74), 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'bigsmile', 'brow': 0.6, 'cheeks': 0.6}, 'sq': [0.96, 1.05, 0.96], 'bend': {'spine': [0.06, 0, 0, 1, None], 'neck': [0.28, 0, 0, 1, None]}}, toonDur=0.3),
            k(1.45, toon={'reach': HOLD5(0.35, 1.72), 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.9, 'mouth': 'smile', 'brow': 0.4, 'cheeks': 0.4}, 'sq': [0.97, 1.04, 0.97], 'bend': {'spine': [0.08, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}}, toonDur=0.2)])],
        props=[P('frigo5', 'cheeseShelf', pos=[-0.2, 0, -2.75], opts={'w': 3.2}),
               P('fromage5', 'plainCheese', pos=CH5A, rot=[1.5708, 0, 0], ry=RY5, opts={'r': 0.24, 'h': 0.14}, keys=[k(r(SNIFF5 - 0.15), to=CH5B, dur=0.32, ease='out')]),
               P('laser5', 'laserDot', pos=[0, 0, 0], opts={'pts': DOT5, 'src': [4.5, 2.7, 2.2], 'r': 0.03})],
        cams=[C5])
st.cue('sfx:sniff', 'S05', SNIFF5, 0.3); st.cue('sfx:sniff', 'S05', r(SNIFF5 + 0.32), 0.2); st.cue('sfx:tense', 'S05', 0.05, 0.12)

# 6: six planes bombed his car. Low on the car park beside the little red car in its bay: six fighter jets in a V roar in over our heads and away
#    toward the store; six fat bombs drop from them and fall, slow then fast, all on the red car; it bursts and squashes flat
D6 = st.dur('S06'); REL6 = 0.2; HIT6 = 1.72
# (round 1) low in the lane on the bay's axis, the red car centred low and clear: the jets are in frame from 0.2 s (looking up), the six bombs hang a
# moment then drop fast, the camera glides down with them onto the car, which squashes to a pancake with a bounce; stars, no white-out
JETS6 = [(0.0, 0.0), (-4.0, 5.0), (4.0, 5.0), (-8.0, 10.0), (8.0, 10.0), (0.0, 15.0)]   # (x offset, behind)
JZ0, JZ1, JY = -3.5, -97.5, 22.0
def jet_pos(dx, back, t): return [r(KEY[0] + dx), JY, r(JZ0 + back + (JZ1 - JZ0) * t / D6)]
C6 = cam(0.0, [1.25, 0.55, -3.4], [1.25, 0.57, -3.6], [1.25, 13.0, -15.4], [1.25, 12.8, -15.6], lens=66)
C6b = cam(1.02, [1.25, 0.7, -3.6], [1.25, 0.72, -3.7], [1.25, 1.6, -10.6], [1.25, 1.58, -10.6], lens=56)
chk('S06', C6['from'], C6['lookAt'], 66, {'jetLead02': jet_pos(0, 0, 0.2), 'jetLast06': jet_pos(0, 15, 0.6), 'jetLeadRel': jet_pos(0, 0, REL6)})
chk('S06b', C6b['from'], C6b['lookAt'], 56, {'carTop': [1.25, 1.45, -10.6], 'carFoot': [1.25, 0.0, -9.0], 'bomb15': [1.25, 9.0, -10.6], 'bomb16': [1.25, 5.0, -10.6]})
DROPS6 = [{'from': add(jet_pos(dx, back, REL6 + 0.04 * i), [0, -1.0, 0]), 'to': [r(KEY[0] + 0.12 * (i - 2.5)), 0.9, r(KEY[2] + 0.1 * (i % 3 - 1))], 't0': r(REL6 + 0.04 * i), 'dur': r(HIT6 - REL6 - 0.04 * i)} for i, (dx, back) in enumerate(JETS6)]
st.shot('S06', 'grassland', setOpts=LOT_SET, actors=[],
        props=[LOT(), ROWS_INTACT(skip=['0:10']), STORE(clock={**CLK, 'base': r(CLOCK0 - (st.SH['S06'][0] - st.SH['S04'][0] - FLIP4), 2), 'flipAt': -1}),
               CAR('rouge6', KEY, 180, color='#D8392B', plate='RX-001-ZZ', scale=1.0, flatAt=HIT6),
               *[P(f'avion6{i}', 'fighterJet', pos=jet_pos(dx, back, 0), ry=180, opts={'burner': 0.8, 'glow': 2.2}, keys=[k(0.0, to=jet_pos(dx, back, D6), dur=D6, ease='linear')]) for i, (dx, back) in enumerate(JETS6)],
               P('bombes6', 'bombDrop', pos=[0, 0, 0], opts={'drops': DROPS6, 's': 1.2, 'hang': 0.18}),
               P('boum6', 'timedBurst', pos=[KEY[0], 0.8, r(KEY[2] - 1.8)], opts={'at': HIT6, 'size': 1.5, 'seed': 6, 'life': 0.45}),
               P('etoiles6', 'impactStars', pos=[KEY[0], 1.3, r(KEY[2] + 0.4)], opts={'at': HIT6, 'n': 7, 'r': 1.15, 'size': 0.22, 'dur': 0.55, 'r0': 0.3}),
               P('fumee6', 'softDust', pos=[KEY[0], 0.5, r(KEY[2] - 0.6)], opts={'at': r(HIT6 + 0.14), 'n': 8, 'size': 1.0, 'life': 1.2, 'rise': 1.6, 'spread': 2.6, 'color': '#9A958D', 'opacity': 0.55})],
        fx=[{'type': 'shake', 'at': HIT6, 'dur': 0.3, 'amount': 0.03}],
        cams=[C6, glide([C6b], 0.42)])
st.cue('sfx:jet', 'S06', 0.0, 0.55); st.cue('whoosh', 'S06', REL6, 0.3, 0.9); st.cue('thunder', 'S06', HIT6, 0.7); st.cue('sfx:crunch', 'S06', r(HIT6 + 0.04), 0.35)

# 7: and the two hundred spaces round it. High over the car park: every car squashed flat in its bay, smoking in neat rows, a lone hubcap rolling
#    across the lane; his blue car untouched in lane A, indicator blinking; the supermarket and its clock beyond; in the foreground the shoppers,
#    safe behind a crowd barrier, watch with their full trolleys
D7 = st.dur('S07')
CLK7 = {**CLK, 'base': r(CLOCK0 - (st.SH['S07'][0] - st.SH['S04'][0] - FLIP4), 2), 'flipAt': -1}
C7 = cam(0.0, [3.5, 11.5, 42.0], [3.4, 11.7, 41.7], [2.745, 7.425, 32.899], [2.745, 7.35, 32.8], lens=55)
SAFE7 = [('client1', [-1.5, GY, 29.3]), ('client2', [1.0, GY, 29.5]), ('client3', [3.6, GY, 29.2]), ('client4', [6.2, GY, 29.6])]
chk('S07', C7['from'], C7['lookAt'], 55, {'heroCar': HERO_CAR, 'store': [0, 6.5, STORE_Z], 'clock': [0.0, 10.4, STORE_Z], 'shopperHead': [1.0, 2.3, 29.5], 'barrier': [1.0, 1.0, 28.5], 'rowE': [0, 0.2, 21.5]})
# (round 1) the shoppers come alive: heads turn from the wrecks to each other, client2 does a double take, client4's trolley drifts off on its own;
#            the hubcap twice as big and nearer; his car's lamps big and bright enough to blink at this distance
LK7 = [1.25, 1.0, -10.5]
SHOPK7 = {'client1': [k(0.0, look=LK7), k(0.7, look=[1.0, 2.0, 29.5], lookDur=0.15), k(1.1, look=LK7, lookDur=0.2)],
          'client2': [k(0.0, look=LK7), k(0.35, look=[-1.5, 2.0, 29.3], lookDur=0.08), k(0.5, look=LK7, lookDur=0.08), k(0.62, look=[-1.5, 2.0, 29.3], lookDur=0.06),
                      k(0.62, toon={'face': {'lid': 0.0, 'pop': 0.4, 'mouth': 'O', 'brow': 0.8}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.06), k(1.0, look=LK7, lookDur=0.2)],
          'client3': [k(0.0, look=LK7), k(0.9, look=[3.6, 1.0, 22.0], lookDur=0.2)],
          'client4': [k(0.0, look=LK7), k(0.8, look=[8.4, 1.0, 27.4], lookDur=0.15), k(0.8, toon={'face': {'lid': 0.1, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.1)]}
st.shot('S07', 'grassland', setOpts=LOT_SET, actors=[act(w, p, 180, 'stand', 'surprised', keys=SHOPK7[w] + stand_blink(0.25 + 0.3 * i, {'lid': 0.1, 'mouth': 'O'})) for i, (w, p) in enumerate(SAFE7)],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=14), CAR('rougeplat7', KEY, 180, color='#D8392B', plate='RX-001-ZZ', scale=1.0, flat=True), HEROCAR('voiture7', blink='both', indS=3.2, glow=2.8),
               STORE(clock=CLK7), P('roue7', 'hubcap', pos=[-4.0, 0.52, 21.0], ry=90, opts={'r': 0.5, 'spin': 7}, keys=[k(0.0, to=[3.0, 0.52, 21.4], dur=D7, ease='linear')]),
               P('barriere7', 'crowdBarrier', pos=[2.2, GY, 28.5], opts={'length': 10.0}),
               *[P(f'chariot7{i}', 'fullTrolley', pos=add(p, [0.95, 0, 0.1]), ry=180, **({'keys': [k(0.75, to=add(p, [2.6, 0, -0.5]), dur=0.85, ease='in')]} if w == 'client4' else {})) for i, (w, p) in enumerate(SAFE7)]],
        cams=[C7])
st.cue('sfx:wind', 'S07', 0.0, 0.25); st.cue('sfx:rattle', 'S07', 0.3, 0.12)

# 8: the supermarket too; it was badly parked. Low in front of the store: the invader stands outside the doors, cheese wheel under his arm, facing
#    us, untouched; behind him the empty supermarket folds flat like a cardboard box, front in, sides in, roof down, the sign and the clock tipping
#    onto the pile; a wall of dust rolls over him and leaves him grey (PLIÉ); (staging) the dust round him kept light: at 0.95 it hid him for a second
D8 = st.dur('S08'); FOLD8 = 0.3; GREY8 = r(FOLD8 + 0.72)
# (round 1) the fold in stages (front, sides, back, roof, then the sign and the clock tipping onto the pile) seen from higher up, so the flattened box
#           lies in the middle of the frame behind him with its sign and clock readable on top; he stands to the right, the wheel face-on
INV8 = [3.4, GY, -11.6]; RY8 = -8
CLK8 = {**CLK, 'base': r(CLOCK0 - (st.SH['S08'][0] - st.SH['S04'][0] - FLIP4), 2), 'flipAt': -1}
C8 = cam(0.0, [4.4, 3.3, -3.6], [4.38, 3.32, -3.75], [0.6, 3.6, -16.0], [0.6, 3.55, -16.0], lens=52)
C8b = cam(r(FOLD8 + 0.3), [4.6, 4.5, -3.9], [4.58, 4.52, -4.05], [0.2, 0.2, -20.5], [0.2, 0.25, -20.5], lens=50)
chk('S08b', C8b['from'], C8b['lookAt'], 50, {'face': [INV8[0], 1.98, INV8[2]], 'feet': INV8, 'pileFront': [0, 0.9, STORE_Z], 'pileBack': [0, 0.9, STORE_Z - 14], 'sign': [0, 1.2, STORE_Z - 3.6], 'clock': [0, 1.4, STORE_Z - 2.4]})
CHEESE_ARM = lambda pid, who: P(pid, 'plainCheese', on={'actor': who, 'joint': 'torso', 'offset': [-0.36, 0.1, 0.12]}, rot=[1.5708, 0, 0], opts={'r': 0.24, 'h': 0.14})   # (round 1) face-on
st.card('S08', 'PLIÉ', at=r(FOLD8 + 1.12))
INVK8 = lambda grey: [k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [*off(INV8, RY8, 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': 0.2}}, toonDur=0.0),
                      k(r(FOLD8 + 0.1), look=[0.3, 3.0, -16.0], lookDur=0.2),
                      k(r(FOLD8 + 0.62), toon={'reach': {'R': [*off(INV8, RY8, 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.7}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.06)] + \
                     ([k(r(GREY8 + 0.25), look='camera', lookDur=0.15), k(r(GREY8 + 0.25), toon={'reach': {'R': [*off(INV8, RY8, 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}, 'sq': [1, 1, 1]}, toonDur=0.15)] + stand_blink(r(GREY8 + 0.7), {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}) if grey else [])
st.shot('S08', 'grassland', setOpts=LOT_SET, actors=[
        act('envahisseur', INV8, RY8, 'stand', 'happy', keys=INVK8(False) + [k(0.0, visible=True), k(GREY8, visible=False)]),
        act('gris', INV8, RY8, 'stand', 'neutral', keys=INVK8(True) + [k(0.0, visible=False), k(GREY8, visible=True)])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=6), STORE(clock=CLK8, foldAt=FOLD8, staged=True), CHEESE_ARM('fromage8a', 'envahisseur'), CHEESE_ARM('fromage8b', 'gris'),
               P('nuage8', 'softDust', pos=add(INV8, [0, 0.8, -0.9]), opts={'at': r(FOLD8 + 0.62), 'n': 9, 'size': 1.0, 'life': 1.0, 'rise': 1.2, 'spread': 2.0, 'color': '#D8D2C4', 'opacity': 0.6})],
        fx=[{'type': 'shake', 'at': r(FOLD8 + 0.64), 'dur': 0.3, 'amount': 0.025}],
        cams=[C8, glide([C8b], 0.7)])
st.cue('sfx:crunch', 'S08', r(FOLD8 + 0.05), 0.3); st.cue('sfx:crunch', 'S08', r(FOLD8 + 0.25), 0.3); st.cue('thud', 'S08', r(FOLD8 + 0.64), 0.7); st.cue('sfx:poof', 'S08', r(FOLD8 + 0.66), 0.4); st.cue('clack', 'S08', r(FOLD8 + 0.96), 0.4)

# 9: the invader was put under witness protection. In the lane, the folded store behind: two masked special forces walk the grey invader, a grey
#    blanket over his head, the cheese under his arm, to a black car; in the foreground he stands by his blue car (indicator blinking) and points
#    at them, outraged, mouth open
D9 = st.dur('S09')
# (round 1) tighter and lower: he stands three quarters to us by his blinking car; a double take (us, the invader, us, the invader) then his arm shoots
#           out half as long again at the invader, jaw dropped, eyes popping; the invader, blanket hanging over his head front and back, cheese face-on
INV9a, INV9b = [0.1, GY, -13.0], [-2.2, GY, -12.6]
BLACK9 = [-3.7, GY, -13.6]
HERO9 = [3.4, GY, -8.9]; RYH9 = -20
C9 = cam(0.0, [5.5, 1.62, -4.4], [5.42, 1.63, -4.55], [0.9, 1.55, -11.6], [0.88, 1.56, -11.6], lens=46)
HCAR9 = [5.2, GY, -10.7]
chk('S09', C9['from'], C9['lookAt'], 46, {'heroFace': [HERO9[0], 1.98, HERO9[2]], 'invStart': [INV9a[0], 2.0, INV9a[2]], 'invEnd': [INV9b[0], 2.0, INV9b[2]], 'blackCar': BLACK9, 'heroCarFR': loc(HCAR9, -90, -0.74 * CS, 1.85 * CS, 0.76 * CS), 'heroCarFL': loc(HCAR9, -90, 0.74 * CS, 1.85 * CS, 0.76 * CS)})
FORCE9 = [('forces1', -0.62), ('forces2', 0.62)]
def PT9(d, h, tgt=None):
    """a point d metres from his right shoulder toward the invader (where he is at that moment), at height h"""
    tg = tgt or INV9a; sh = off(HERO9, RYH9, 0.0, -0.25, 0.0); dx, dz = tg[0] - sh[0], tg[2] - sh[2]; n = math.hypot(dx, dz); return [r(sh[0] + dx / n * d), h, r(sh[2] + dz / n * d)]
INVM9 = [r((INV9a[0] + INV9b[0]) / 2), GY, r((INV9a[2] + INV9b[2]) / 2)]
OUT9 = {'lid': 0.0, 'pop': 0.5, 'mouth': 'scream', 'brow': 0.8}
st.shot('S09', 'grassland', setOpts=LOT_SET, actors=[
        act('gris', INV9a, yaw(INV9a, INV9b), 'stand', 'neutral', keys=[k(0.0, to=INV9b, dur=D9, clip='walk'), k(0.0, toon={'reach': {'R': [*off(INV9b, yaw(INV9a, INV9b), 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0)]),
        *[act(w, off(INV9a, yaw(INV9a, INV9b), -0.1, s), yaw(INV9a, INV9b), 'stand', 'neutral', keys=[k(0.0, to=off(INV9b, yaw(INV9a, INV9b), -0.1, s), dur=D9, clip='walk'),
            k(0.0, toon={'reach': {('L' if s > 0 else 'R'): [*off(INV9b, yaw(INV9a, INV9b), 0.05, s * 0.45, 1.45), 1, 0.04]}, 'hands': {('L' if s > 0 else 'R'): 'grip'}}, toonDur=0.0)]) for w, s in FORCE9],
        act('mec', HERO9, RYH9, 'stand', 'angry', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            k(0.22, look=[INV9a[0], 2.0, INV9a[2]], lookDur=0.06), k(0.42, look='camera', lookDur=0.06),
            k(0.42, toon={'face': {'lid': 0.1, 'pop': 0.2, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.06),
            k(0.62, look=[INVM9[0], 2.0, INVM9[2]], lookDur=0.06),
            k(0.56, toon={'reach': {'L': [*PT9(0.3, 1.5), 1, 0.04]}, 'hands': {'L': 'fist'}, 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.6}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.06),
            k(0.66, toon={'reach': {'L': [*PT9(1.2, 1.95, INVM9), 1, 0.1]}, 'hands': {'L': 'point'}, 'face': OUT9, 'sq': [0.94, 1.08, 0.94]}, toonDur=0.07, toonEase='out'),
            k(0.85, toon={'reach': {'L': [*PT9(1.12, 1.9, INVM9), 1, 0.1]}, 'hands': {'L': 'point'}, 'face': OUT9, 'sq': [1, 1, 1]}, toonDur=0.12),
            *[k(r(1.0 + 0.24 * i), toon={'reach': {'L': [*PT9(1.12 + 0.05 * (i % 2), 1.9 + 0.06 * (i % 2), INVM9 if i < 3 else INV9b), 1, 0.1]}, 'hands': {'L': 'point'}, 'face': {**OUT9, 'mouth': 'scream' if i % 2 == 0 else 'O'}}, toonDur=0.07) for i in range(6)],
            k(1.4, look=[INV9b[0], 2.0, INV9b[2]], lookDur=0.5)])],
        props=[LOT(), ROWS_FLAT(skip=['0:10', '0:11', '0:12', '0:13'], wisps=6), STORE(folded=True, clock=CLK8), HEROCAR('voiture9', HCAR9, blink='both'), CAR('noire9', BLACK9, -90, dark=True, plate='AA-000-AA'),
               CHEESE_ARM('fromage9', 'gris'),
               P('couverture9', 'blanketDrape', on={'actor': 'gris', 'joint': 'head', 'offset': [0.0, 0.56, 0.21]}, opts={'w': 0.66, 'h': 0.95, 'color': '#4E5668', 'band': '#3E4452'}),
               P('couverture9b', 'blanketDrape', on={'actor': 'gris', 'joint': 'head', 'offset': [0.0, 0.56, -0.21]}, opts={'w': 0.66, 'h': 0.95, 'color': '#4E5668', 'band': '#3E4452'}),
               P('couverture9c', 'blanketDrape', on={'actor': 'gris', 'joint': 'head', 'offset': [0.0, 0.56, 0.0]}, rot=[-1.5708, 0, 0], opts={'w': 0.66, 'h': 0.42, 'color': '#4E5668', 'band': '#4E5668'}),
               *[BALA(f'cagoule9{i}', w) for i, (w, s) in enumerate(FORCE9)]],
        cams=[C9])
st.cue('sfx:boing', 'S09', 0.66, 0.2)
st.cue('sfx:stepHeavy', 'S09', 0.3, 0.2); st.cue('sfx:stepHeavy', 'S09', 0.9, 0.2); st.cue('sfx:stepHeavy', 'S09', 1.5, 0.2); st.cue('sfx:carDoor', 'S09', 2.2, 0.3)

# 10: the space was retaken. Low in the lane on the swept, empty bay between the flattened wrecks: a soldier drives a flagpole straight down into
#     the middle of it (thud, shudder), and he, at the bay's edge, snaps a proud salute (REPRISE)
D10 = st.dur('S10'); PLANT10 = 0.42; SAL10 = 0.62
POLE = [1.25, GY, -11.0]
SOLD10 = [0.55, GY, -10.2]; RYS10 = yaw(SOLD10, POLE)
HERO10 = [3.2, GY, -8.3]; RYH10 = -22
C10 = cam(0.0, [4.4, 0.95, -4.4], [4.35, 0.98, -4.55], [1.4, 2.1, -10.6], [1.4, 2.15, -10.6], lens=50)
chk('S10', C10['from'], C10['lookAt'], 50, {'heroFace': [HERO10[0], 1.98, HERO10[2]], 'flagTop': [POLE[0], 3.5, POLE[2]], 'soldFace': [SOLD10[0], 1.98, SOLD10[2]], 'bayFront': [1.25, 0.06, -8.0]})
st.card('S10', 'REPRISE', at=r(SAL10 + 0.15))
FLAG_ARMY = {'h': 3.4, 'fw': 1.2, 'colors': ['#3E5A2E', '#3E5A2E'], 'mark': 'star', 'markColor': '#E2B53C'}
st.shot('S10', 'grassland', setOpts=LOT_SET, actors=[
        act('soldat1', SOLD10, RYS10, 'stand', 'angry', keys=[k(0.0, look=add(POLE, [0, 1.0, 0])),
            k(0.0, toon={'reach': {'R': [*add(POLE, [-0.05, 1.95, 0.05]), 1, 0.03], 'L': [*add(POLE, [-0.05, 1.55, 0.05]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.0),
            k(PLANT10, toon={'reach': {'R': [*add(POLE, [-0.05, 1.05, 0.05]), 1, 0.03], 'L': [*add(POLE, [-0.05, 0.65, 0.05]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.1, 0.88, 1.1], 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.1, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.12, toonEase='in'),
            k(r(PLANT10 + 0.25), toon={'reach': {'R': SALUTE(SOLD10, RYS10)}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.1, toonEase='out')]),
        act('mec', HERO10, RYH10, 'stand', 'neutral', keys=[k(0.0, look=add(POLE, [0, 2.6, 0])), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(r(SAL10 - 0.1), toon={'reach': {'R': [*off(HERO10, RYH10, 0.3, 0.25, 1.4), 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [1.02, 0.97, 1.02], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.08),
            k(SAL10, toon={'reach': {'R': SALUTE(HERO10, RYH10)}, 'hands': {'R': 'open'}, 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.25, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.06, toonEase='out'),
            k(r(SAL10 + 0.12), toon={'reach': {'R': SALUTE(HERO10, RYH10)}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1], 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.08)])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=6), STORE(folded=True, clock=CLK8), P('drapeau10', 'bayFlag', pos=POLE, opts={**FLAG_ARMY, 'plantAt': PLANT10, 'drop': 0.9}), HELMET('casque10', 'soldat1'),
               P('poussiere10', 'softDust', pos=add(POLE, [0, 0.1, 0]), opts={'at': r(PLANT10 + 0.12), 'n': 6, 'size': 0.35, 'life': 0.7, 'rise': 0.3, 'spread': 0.7, 'color': '#C9C3B5', 'opacity': 0.8})],
        fx=[{'type': 'shake', 'at': r(PLANT10 + 0.12), 'dur': 0.12, 'amount': 0.012}],
        cams=[C10])
st.cue('thud', 'S10', r(PLANT10 + 0.12), 0.55); st.cue('sfx:fanfare', 'S10', r(SAL10 + 0.1), 0.25)

# 11: three thousand soldiers paraded on it. Low at the corner of the same bay: soldiers and a band (drum, trumpet) march nose to tail in a tight
#     loop inside its white lines, round the flag; he salutes at the edge
D11 = st.dur('S11')
LOOP = [[0.55, -12.35], [1.95, -12.35], [1.95, -8.75], [0.55, -8.75]]
def loop_pt(s):
    per = 2 * (1.4 + 3.6); s = s % per
    for i in range(4):
        a, b = LOOP[i], LOOP[(i + 1) % 4]; L = math.dist(a, b)
        if s <= L: w = s / L; return [r(a[0] + (b[0] - a[0]) * w), GY, r(a[1] + (b[1] - a[1]) * w)]
        s -= L
    return [LOOP[0][0], GY, LOOP[0][1]]
def loop_path(s0, d, n=10): return [loop_pt(s0 + d * j / n) for j in range(1, n + 1)]
# (round 1) lower and wider, single file nose to tail round the flag, the drummer and the trumpeter leading (it was a tangled scrum seen from above)
MARCH11 = [('musi1', 6.0), ('musi2', 4.35), ('soldat1', 2.7), ('soldat2', 1.05), ('soldat3', 9.4), ('soldat4', 7.75)]
SPD11 = 1.2
HERO11 = [3.3, GY, -9.9]; RYH11 = 5
C11 = cam(0.0, [5.9, 3.3, -5.4], [5.85, 3.28, -5.55], [1.3, 0.85, -10.6], [1.3, 0.87, -10.6], lens=50)
chk('S11', C11['from'], C11['lookAt'], 46, {'heroFace': [HERO11[0], 1.98, HERO11[2]], 'loopNear': [1.95, 2.0, -8.75], 'loopFar': [0.55, 2.0, -12.35], 'flagTop': [POLE[0], 3.5, POLE[2]]})
def marcher(w, s0):
    p0 = loop_pt(s0); p1 = loop_pt(s0 + 0.05); ks = [k(0.0, path=loop_path(s0, SPD11 * D11), dur=D11, clip='marchPomp', face='move')]
    if w.startswith('soldat'): ks.append(k(0.0, toon={'reach': {'R': [*add(p0, [0, 2.0, 0]), 0, 0.03]}}, toonDur=0.0))
    return act(w, p0, yaw(p0, p1), 'stand', 'neutral', keys=ks)
st.shot('S11', 'grassland', setOpts=LOT_SET, actors=[*[marcher(w, s0) for w, s0 in MARCH11],
        act('mec', HERO11, RYH11, 'stand', 'happy', keys=[k(0.0, look=[1.25, 2.0, -10.5]), k(0.0, toon={'reach': {'R': SALUTE(HERO11, RYH11)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.0),
            *stand_blink(0.9, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4})])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=4), STORE(folded=True, clock=CLK8), P('drapeau11', 'bayFlag', pos=POLE, opts=FLAG_ARMY),
               *[HELMET(f'casque11{i}', w) for i, (w, s0) in enumerate(MARCH11) if w.startswith('soldat')],
               P('tambour11', 'bandInstr', on={'actor': 'musi1', 'joint': 'torso', 'offset': [0.0, 0.1, 0.22]}, opts={'kind': 'drum', 'beat': [r(0.3 * i) for i in range(7)]}),
               P('trompette11', 'bandInstr', on={'actor': 'musi2', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'kind': 'trumpet'}),
               KEPI('kepi11a', 'musi1'), KEPI('kepi11b', 'musi2')],
        cams=[C11])
st.cue('sfx:fanfare', 'S11', 0.0, 0.35); st.cue('sfx:stepHeavy', 'S11', 0.2, 0.2); st.cue('sfx:stepHeavy', 'S11', 0.75, 0.2); st.cue('sfx:stepHeavy', 'S11', 1.3, 0.2)

# 12: the other countries called a summit. Low beside the approach road: a queue of black official cars with little flags on their wings waits
#     nose to tail at the closed striped boom; beyond it the warship's gun swings from one car to the next to check it
D12 = st.dur('S12')
QUEUE = [[30.7, GY, 38.3], [27.4, GY, 34.7], [23.9, GY, 38.3], [20.4, GY, 34.7]]
FLAGS = [['#6A3FA0', '#F2C94C'], ['#1E7A8C', '#E88AA8'], ['#E07A1F', '#1F2E5C'], ['#9CC43A', '#7A2333']]
# (round 1) seen from behind the queue: the cars inch toward the closed boom, the warship beyond it; its (bigger) gun swings from car to car, a little
#           past each one and back (a settle), front car to back car
INCH12 = 0.9
AIMS12 = [turret_yaw(add(q, [INCH12, 0, 0])) for q in QUEUE]
AIM12 = []
for i, (t0, q) in enumerate(zip((0.05, 0.5, 0.95, 1.4), (0, 1, 2, 3))):
    v = AIMS12[q] * 1.5; AIM12 += [[t0, r(v * 1.14, 3)], [r(t0 + 0.16), r(v, 3)]]
FRM12 = [10.0, 3.4, 36.5]
LK12, LN12 = [40.0, 2.6, 36.5], 44
C12 = cam(0.0, FRM12, add(FRM12, [0.2, 0.0, -0.02]), LK12, add(LK12, [0, 0.05, 0]), lens=LN12)
chk('S12', C12['from'], C12['lookAt'], C12['lens'], {'car0': QUEUE[0], 'car3': QUEUE[3], 'boom': [33.8, 1.0, 36.0], 'ship': loc(SHIP, SHIP_RY, 0, 0, 4.0), 'turret': loc(SHIP, SHIP_RY, 0, 2.4, 2.2)})
st.shot('S12', 'grassland', setOpts=LOT_SET, actors=[],
        props=[P('rondpoint12', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': 'down'}),
               P('navire12', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': AIM12, 'aimBlend': 0.13, 'counter': True, 'laps': [[0, 0]], 'gunS': 1.8}),
               P('route12', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}),
               *[CAR(f'officielle12{i}', p, 90, dark=True, flag=FLAGS[i], plate='CD-%03d-XX' % (12 + i), phase=0.2 * i,
                     keys=[k(r(0.1 + 0.12 * i), to=add(p, [r(INCH12 * 0.5), 0, 0]), dur=0.35, ease='inOut'), k(r(1.0 + 0.12 * i), to=add(p, [INCH12, 0, 0]), dur=0.35, ease='inOut')]) for i, p in enumerate(QUEUE)]],
        cams=[C12])
st.cue('engine', 'S12', 0.0, 0.15, 1.8); st.cue('sfx:honk', 'S12', 0.6, 0.12); st.cue('sfx:squeak', 'S12', 0.45, 0.15); st.cue('sfx:squeak', 'S12', 0.95, 0.15); st.cue('sfx:squeak', 'S12', 1.45, 0.15)

# 13: the summit lasted forty laps. On the roundabout's west side: the black cars drive round the warship nose to tail; in each a leader in a sash
#     leans out of his window and passes the treaty pages back to the car behind; on the bridge the lap counter clicks 38, 39, 40
D13 = st.dur('S13')
A13 = (252.0, 292.0)
def arc_path(a0, a1, rad, lx=0.0, lz=0.0, n=12):
    pts = []
    for j in range(n + 1):
        a = a0 + (a1 - a0) * j / n; c = ring_pos(a, rad); h = a + 90.0
        pts.append(loc(c, h, lx, lz))
    return pts
# (round 1) the cars a car length apart; each leader stands in his car with his chest out of its right window (only the upper body shows above the
#           door), leaning out; the front one holds a treaty page back, the one behind stretches out and takes it; lower camera, all above the captions
LEAD13 = [('chef1', 24.5, FLAGS[0], 'R'), ('chef2', 0.0, FLAGS[1], 'R')]   # (who, angle lead, flag, the open window: the car's right faces us on the west side)
RAD13 = 10.95
# (round 1) from the west, level with the cars' right sides (the open windows), panning with them as they go round; the lap counter on the bridge
#           behind them
LEAD13A = 24.5
def mid13(t):
    a_ = A13[0] + (A13[1] - A13[0]) * t / D13; p1, p2 = ring_pos(a_ + LEAD13A, RAD13), ring_pos(a_, RAD13); return [r((p1[0] + p2[0]) / 2), 2.4, r((p1[2] + p2[2]) / 2)]
M0, M1 = mid13(0.0), mid13(1.15)   # (round 1) a partial pan: the lap counter stays in frame until it reads 40
C13 = cam(0.0, add(M0, [-14.5, 1.3, 0.4]), add(M0, [-14.3, 1.29, 0.4]), M0, add(M0, [0.1, 0, 0]), lens=46)
C13b = cam(0.05, add(M1, [-14.5, 1.3, 0.4]), add(M1, [-14.3, 1.29, 0.4]), M1, add(M1, [0.1, 0, 0]), lens=46)
for tt, cc in ((0.0, C13), (D13, C13b)):
    a_ = A13[0] + (A13[1] - A13[0]) * tt / D13
    chk(f'S13@{tt:.1f}', cc['from'], cc['lookAt'], 46, {'car1': add(ring_pos(a_ + 24.5, RAD13), [0, 1.0, 0]), 'car2': add(ring_pos(a_, RAD13), [0, 1.0, 0]), 'chef1head': add(loc(ring_pos(a_ + 24.5, RAD13), a_ + 24.5 + 90, -0.72 * CS, -0.25 * CS), [0, 2.0, 0]), 'counter': loc(SHIP, SHIP_RY, 0, -0.65, 4.5)})
WX13 = -0.72 * CS                                      # the window side (the car's right, -X local), the leader's middle just inside the door
def leader(w, lead, side, lz, extra=()):
    """a leader standing in the car, his chest out of its right window, turned toward us"""
    pts = arc_path(A13[0] + lead, A13[1] + lead, RAD13, WX13, lz)
    p0 = [pts[0][0], 0.02, pts[0][2]]
    return act(w, p0, -90, 'stand', 'neutral', keys=[k(0.0, path=[[q[0], 0.02, q[2]] for q in pts[1:]], dur=D13, glide=True, face='keep'), k(0.0, look=[32.2, 4.6, 45.6]),
        k(0.0, toon={'bend': {'spine': [0.0, 0, (0.22 if w == 'chef1' else -0.22), 1, None]}, 'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0), *extra])
CARS13 = [P(f'officielle13{i}', 'bayCar', pos=arc_path(A13[0] + lead, A13[1] + lead, RAD13)[0], ry=r(A13[0] + lead + 90, 2), scale=CS,
            opts={'dark': True, 'flag': fl, 'open': side, 'plate': 'CD-%03d-XX' % (12 + i)}, keys=[k(0.0, path=arc_path(A13[0] + lead, A13[1] + lead, RAD13)[1:], dur=D13, ease='linear', faceMove=True)])
          for i, (w, lead, fl, side) in enumerate(LEAD13)]
SASHES = [['#6A3FA0', '#F2C94C'], ['#1E7A8C', '#E88AA8'], ['#E07A1F', '#1F2E5C']]
PASS13 = 0.95
def handoff(t):
    """the point between the two leaders' windows where the page changes hands (moving with the cars)"""
    a = A13[0] + (A13[1] - A13[0]) * t / D13
    p1 = loc(ring_pos(a + 12.25, RAD13), a + 12.25 + 90.0, WX13 * 1.35, 0.0); return [p1[0], 2.15, p1[2]]
REACH13 = lambda w, t, hand: k(t, toon={'reach': {hand: [*handoff(t), 1, 0.1]}, 'hands': {hand: 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}, 'bend': {'spine': [0.0, 0, (0.3 if w == 'chef1' else -0.3), 1, None]}}, toonDur=0.25)
st.shot('S13', 'grassland', setOpts=LOT_SET, actors=[
        leader('chef1', 24.5, 'R', -0.25 * CS, [REACH13('chef1', 0.35, 'R'), REACH13('chef1', 0.7, 'R'), REACH13('chef1', PASS13, 'R'),
                                                k(r(PASS13 + 0.3), toon={'face': {'lid': 0.4, 'mouth': 'smile'}, 'bend': {'spine': [0.0, 0, 0.18, 1, None]}}, toonDur=0.3)]),
        leader('chef2', 0.0, 'R', 0.55 * CS, [REACH13('chef2', 0.55, 'L'), REACH13('chef2', 0.8, 'L'), REACH13('chef2', PASS13, 'L'),
                                              k(r(PASS13 + 0.35), toon={'reach': {'L': [*add(handoff(PASS13 + 0.35), [0.0, -0.2, 0.0]), 0.0, 0.05]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}, 'bend': {'spine': [0.0, 0, -0.18, 1, None]}}, toonDur=0.3)])],
        props=[P('rondpoint13', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': 'down'}),
               P('navire13', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': [[0, 0.0]], 'counter': True, 'laps': [[0, 38], [0.55, 39], [1.25, 40]]}),
               P('route13', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}), *CARS13,
               P('page13a', 'treatySheet', on={'actor': 'chef1', 'hand': 'R', 'offset': [0.0, -0.04, 0.05], 'face': 'camera'}, opts={'w': 0.34, 'text': True}, keys=[k(0.0, visible=True), k(PASS13, visible=False)]),
               P('page13b', 'treatySheet', on={'actor': 'chef2', 'hand': 'L', 'offset': [0.0, -0.04, 0.05], 'face': 'camera'}, opts={'w': 0.34, 'text': True}, keys=[k(0.0, visible=False), k(PASS13, visible=True)])],
        cams=[C13, glide([C13b], r(D13 - 0.1))])
st.cue('engine', 'S13', 0.0, 0.2, 1.8); st.cue('sfx:ding', 'S13', 0.55, 0.25); st.cue('sfx:ding', 'S13', 1.25, 0.35); st.cue('sfx:paper', 'S13', PASS13, 0.25)

# 14: the treaty declared the space a neutral zone. Back at the bay round the flag: three leaders in sashes run a red-and-white tape round its
#     white lines, post to post; he, at the edge, still saluting, slowly lowers his hand (NEUTRE)
D14 = st.dur('S14'); LOWER14 = 1.2
LEAD14 = [('chef1', [-0.05, GY, -8.15]), ('chef2', [2.6, GY, -12.9]), ('chef3', [-0.05, GY, -12.9])]
HERO14 = [3.0, GY, -8.0]; RYH14 = -35
C14 = cam(0.0, [-0.9, 1.75, -1.6], [-0.85, 1.75, -1.75], [2.412, 2.307, -11.019], [2.412, 2.3, -11.019], lens=48)
chk('S14', C14['from'], C14['lookAt'], 48, {'heroFace': [HERO14[0], 1.98, HERO14[2]], 'chef1': [LEAD14[0][1][0], 1.98, LEAD14[0][1][2]], 'chef2': [2.6, 1.98, -12.9], 'flagTop': [POLE[0], 3.5, POLE[2]]})
st.card('S14', 'NEUTRE', at=1.6)
st.shot('S14', 'grassland', setOpts=LOT_SET, actors=[
        *[act(w, p, yaw(p, KEYC), 'stand', 'neutral', keys=[k(0.0, look=add(KEYC, [0, 0.9, 0])), k(0.0, toon={'reach': {'R': [*off(p, yaw(p, KEYC), 0.35, 0.15, 0.95), 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(r(0.4 + 0.3 * i), look='camera', lookDur=0.3), *stand_blink(r(1.0 + 0.25 * i), {'lid': 0.35, 'mouth': 'line'})]) for i, (w, p) in enumerate(LEAD14)],
        act('mec', HERO14, RYH14, 'stand', 'happy', keys=[k(0.0, look=[1.25, 2.6, -10.8]), k(0.0, toon={'reach': {'R': SALUTE(HERO14, RYH14)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.0),
            k(0.6, toon={'reach': {'R': SALUTE(HERO14, RYH14)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}}, toonDur=0.3),
            k(LOWER14, toon={'reach': {'R': [*off(HERO14, RYH14, 0.15, 0.3, 1.0), 1, 0.04]}, 'hands': {'R': 'rest'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.9, toonEase='inOut'),
            k(r(LOWER14 + 0.5), look='camera', lookDur=0.4), *stand_blink(2.1, {'lid': 0.5, 'mouth': 'line', 'brow': -0.2})])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=4), STORE(folded=True, clock=CLK8), P('drapeau14', 'bayFlag', pos=POLE, opts=FLAG_ARMY),
               P('ruban14', 'bayTape', pos=KEYC, opts={'w': 2.5, 'l': 5.0, 'stretch': [0.15, 1.3]})],
        cams=[C14])
st.cue('sfx:stretch', 'S14', 0.2, 0.2); st.cue('sfx:stretch', 'S14', 0.75, 0.2); st.cue('sfx:sting', 'S14', 1.6, 0.25)

# 15: every country parked a tank in it. Low in the lane, looking up: a tall tower of tanks, each with its own little flag, stacked inside the taped
#     bay; at its foot he stands by his blue car, indicator still blinking, and looks up at it
D15 = st.dur('S15')
TFLAGS = [['#6A3FA0', '#F2C94C'], ['#1E7A8C', '#E88AA8'], ['#E07A1F', '#1F2E5C'], ['#9CC43A', '#7A2333'], ['#7EC8E3', '#7A4A2A']]   # (round 1) invented pairs only
HERO15 = [2.0, GY, -6.2]; RYH15 = -25
C15 = cam(0.0, [-2.6, 1.15, 0.2], [-2.5, 1.15, -0.05], [2.0, 4.0, -9.6], [2.0, 4.1, -9.6], lens=52)   # (round 1) tighter: less empty sky
chk('S15', C15['from'], C15['lookAt'], 58, {'towerTop': [1.25, 8.4, -10.5], 'towerFoot': [1.25, 0.3, -10.5], 'heroFace': [HERO15[0], 1.98, HERO15[2]], 'heroCarFR': loc([5.6, GY, -5.9], -90, -0.74 * CS, 1.85 * CS, 0.76 * CS)})
st.shot('S15', 'grassland', setOpts=LOT_SET, actors=[
        # (round 1) the eyes go up first, then the head tips back on a stretched neck; the tower sways once and settles
        act('mec', HERO15, RYH15, 'stand', 'unimpressed', keys=[k(0.0, look=[1.25, 2.0, -10.5]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.25, toon={'face': {'lid': 0.15, 'mouth': 'line', 'brow': 0.5, 'pop': 0.15}}, toonDur=0.08), k(0.25, look=[1.25, 3.4, -10.5], lookDur=0.12),
            k(0.5, look=[1.25, 8.0, -10.5], lookDur=0.35), k(0.5, toon={'face': {'lid': 0.1, 'mouth': 'O', 'brow': 0.6, 'pop': 0.2}, 'sq': [0.95, 1.07, 0.95], 'bend': {'neck': [-0.45, 0, 0, 1, None], 'spine': [-0.12, 0, 0, 1, None]}}, toonDur=0.35, toonEase='out'),
            k(1.15, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}, 'sq': [1, 1, 1], 'bend': {'neck': [-0.4, 0, 0, 1, None], 'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.3),
            *stand_blink(1.6, {'lid': 0.3, 'mouth': 'line', 'brow': 0.3})])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=4), STORE(folded=True, clock=CLK8), P('ruban15', 'bayTape', pos=KEYC, opts={'w': 2.5, 'l': 5.0}),
               P('tours15', 'tankTower', pos=KEYC, opts={'n': 5, 's': 0.62, 'flags': TFLAGS, 'marks': ['chevron', None, 'disc', None, 'chevron'], 'sway': 0.85, 'swayAmp': 0.06}),
               HEROCAR('voiture15', [5.6, GY, -5.9], blink='both')],
        cams=[C15])
st.cue('sfx:rattle', 'S15', 0.1, 0.2); st.cue('sfx:squeak', 'S15', 0.88, 0.3); st.cue('sfx:honkTiny', 'S15', 1.2, 0.15)

# 16: this man pays the war reparations. In lane B, the flattened rows round them: he shakes his empty open wallet upside down over the general's
#     upturned helmet, held out like a bowl; behind them a line of soldiers holding out their helmets runs across the car park to the horizon
D16 = st.dur('S16')
HERO16 = [0.6, GY, 10.4]; RYH16 = 150; GEN16 = [-0.5, GY, 10.9]; RYG16 = -150
# (round 1) the helmet held up at chest height and the wallet upside down right over it (one silhouette); three hard shakes, a single coin drops into
#           the helmet; the line of helmets starts behind his right shoulder (no blank head between the two men); all above the captions
BOWL16 = [0.05, 1.46, 10.62]
C16 = cam(0.0, [0.15, 2.0, 5.3], [0.13, 2.0, 5.5], [0.05, 1.35, 15.6], [0.05, 1.36, 15.6], lens=30)
chk('S16', C16['from'], C16['lookAt'], 30, {'heroFace': [HERO16[0], 1.98, HERO16[2]], 'genFace': [GEN16[0], 1.98, GEN16[2]], 'bowl': BOWL16, 'wallet': add(BOWL16, [0, 0.3, 0]), 'lineStart': [2.1, 1.8, 13.6]})
WAL16 = lambda dy, dx=0.0: [*add(BOWL16, [r(-0.02 + dx), r(0.3 + dy), -0.02]), 1, 0.03]
SH16 = [(0.3, 0.0, 0.0), (0.42, 0.14, 0.03), (0.52, -0.04, -0.03), (0.62, 0.15, 0.03), (0.72, -0.04, -0.03), (0.82, 0.15, 0.03), (0.93, -0.03, 0.0)]
COIN16 = 0.95
st.shot('S16', 'grassland', setOpts=LOT_SET, actors=[
        act('mec', HERO16, RYH16, 'stand', 'unimpressed', keys=[k(0.0, look=BOWL16), k(0.0, toon={'reach': {'R': WAL16(0.0)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            *[k(t, toon={'reach': {'R': WAL16(dy, dx)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.45, 'mouth': 'clench' if dy > 0 else 'line', 'brow': -0.3}, 'sq': [1.03, 0.97, 1.03] if dy > 0 else [0.98, 1.02, 0.98]}, toonDur=0.05, toonEase='out') for t, dy, dx in SH16],
            k(r(COIN16 + 0.15), look=add(BOWL16, [0, -0.05, 0]), lookDur=0.1),
            k(1.4, look='camera', lookDur=0.15), *stand_blink(1.65, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})]),
        act('general', GEN16, RYG16, 'stand', 'neutral', keys=[k(0.0, look=add(BOWL16, [-0.1, 0.4, 0])),
            k(0.0, toon={'reach': {'R': [*add(BOWL16, [0.18, -0.03, 0.0]), 1, 0.03], 'L': [*add(BOWL16, [-0.16, -0.04, 0.0]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(r(COIN16 + 0.36), toon={'reach': {'R': [*add(BOWL16, [0.18, -0.06, 0.0]), 1, 0.03], 'L': [*add(BOWL16, [-0.16, -0.07, 0.0]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.08),
            k(r(COIN16 + 0.5), look='camera', lookDur=0.2), *stand_blink(1.2, {'lid': 0.35, 'mouth': 'line', 'brow': 0.4})])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=4), STORE(folded=True, clock=CLK8), KEPI('kepi16', 'general'),
               P('bol16', 'armyHelmet', pos=add(BOWL16, [0, -0.06, 0]), rot=[3.1416, 0, 0], opts={'s': 0.95}, keys=[k(r(COIN16 + 0.36), to=add(BOWL16, [0, -0.09, 0]), dur=0.08)]),
               P('portefeuille16', 'emptyWallet', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.07, 0.03], 'face': 'camera'}, rot=[3.1416, 0, 0], opts={'open': 0.7}),
               P('piece16', 'coinDrop', pos=[0, 0, 0], opts={'from': add(BOWL16, [-0.02, 0.22, -0.02]), 'to': add(BOWL16, [0.0, 0.02, 0.0]), 'at': COIN16, 'dur': 0.3}),
               P('file16', 'helmetLine', pos=[0, 0, 0], opts={'path': [[2.1, 13.6], [3.6, 33.0], [6.0, 120.0]], 'gap': 1.1, 'y': GY, 'face': r(PI, 4)})],
        cams=[C16])
st.cue('sfx:rattleShort', 'S16', 0.42, 0.2); st.cue('sfx:rattleShort', 'S16', 0.62, 0.2); st.cue('sfx:rattleShort', 'S16', 0.82, 0.2); st.cue('sfx:clink', 'S16', r(COIN16 + 0.3), 0.3)

# 17: the blockade was never lifted. Months later at the roundabout: tall grass round the striped booms, the warship still on its island; low
#     behind his blue car waiting at the give-way line, its indicator blinking; the ship's gun swings round and stops on him
D17 = st.dur('S17'); AIMED17 = 1.12
CAR17 = [30.9, GY, 38.3]
# (round 1) three quarters from the side, the car on the left and the ship on the right, so the barrel's swing across to him and its stop read (a
#           little past, back, then a 0.6 s hold on him)
C17 = cam(0.0, [22.0, 3.3, 51.0], [22.1, 3.3, 50.8], [35.6, 2.3, 36.4], [35.62, 2.32, 36.4], lens=62)
AIMC17 = turret_yaw(CAR17)
chk('S17', C17['from'], C17['lookAt'], 62, {'carRear': loc(CAR17, 90, 0, -2.3, 0.8), 'turret': loc(SHIP, SHIP_RY, 0, 2.4, 2.2), 'mast': loc(SHIP, SHIP_RY, 0, -1.4, 6.4), 'boom': [33.8, 1.0, 37.0]})
st.shot('S17', 'grassland', setOpts={**LOT_SET, 'sky': ['#9FC4D8', '#DCE6E4']}, actors=[],
        props=[P('rondpoint17', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': 'down', 'grass': True}),
               P('navire17', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': [[0, -1.0], [0.3, -1.0], [0.62, r(AIMC17 + 0.32, 3)], [0.98, r(AIMC17 - 0.07, 3)], [AIMED17, AIMC17]], 'aimBlend': 0.3, 'counter': True, 'laps': [[0, 40]], 'gunS': 1.6}),
               P('route17', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}),
               HEROCAR('voiture17', CAR17, 90, blink='both'),
               P('herbe17', 'tallGrass', pos=[29.0, 0, 41.6], opts={'w': 8, 'd': 1.6, 'h': 1.0, 'count': 260, 'seed': 77, 'thin': 0.03})],
        cams=[C17])
st.cue('sfx:wind', 'S17', 0.0, 0.3); st.cue('sfx:tick', 'S17', 0.2, 0.12); st.cue('sfx:tick', 'S17', 0.9, 0.12); st.cue('sfx:squeak', 'S17', 0.45, 0.25); st.cue('clack', 'S17', AIMED17, 0.4)

# 18: he parks in the neighbouring country. A border post on a country road: he ducks under the striped barrier toward us, a shopping bag in each
#     hand, and straightens up; far behind him his blue car sits tiny in a lone painted bay under another country's flag, indicator blinking
D18 = st.dur('S18'); DUCK18 = (0.55, 1.25)
HA18, HB18 = [0.4, GY, -2.6], [0.4, GY, 2.0]
FAR18 = [1.6, GY, -30.0]
C18 = cam(0.0, [1.15, 1.25, 6.4], [1.13, 1.27, 6.2], [0.4, 1.6, -4.0], [0.4, 1.6, -4.0], lens=44)
chk('S18', C18['from'], C18['lookAt'], 44, {'heroStart': [HA18[0], 2.0, HA18[2]], 'heroEnd': [HB18[0], 2.0, HB18[2]], 'farCar': FAR18, 'farFlag': [FAR18[0] - 2.6, 4.0, FAR18[2]], 'booth': [-1.7, 2.8, -1.2]})
def HB(t, sq=(1, 1, 1), bend=0.0, face=None, d=0.12):
    return k(t, toon={'sq': list(sq), 'bend': {'spine': [bend, 0, 0, 1, None]}, 'face': face or {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=d)
st.shot('S18', 'grassland', setOpts={'clouds': 30, 'grass': '#8CC260'}, actors=[
        act('mec', HA18, 0, 'holdBags', 'unimpressed', keys=[k(0.0, to=HB18, dur=1.75, clip='carryBags'), k(0.0, look='camera'),
            HB(0.0, d=0.0), HB(DUCK18[0], (1.12, 0.62, 1.12), 0.55, {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}, 0.14), HB(DUCK18[1], (1.12, 0.62, 1.12), 0.55, {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}, 0.3),
            # (round 1) the rise in steps (it happened between two draft frames): half up, overshoot, settle
            HB(r(DUCK18[1] + 0.16), (1.05, 0.84, 1.05), 0.28, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}, 0.16), HB(r(DUCK18[1] + 0.32), (0.95, 1.06, 0.95), 0.0, None, 0.16),
            HB(r(DUCK18[1] + 0.5), (1, 1, 1), 0.0, None, 0.16), *stand_blink(2.3, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})])],
        props=[P('route18', 'parkLot', pos=[0, 0, -20.0], opts={'w': 7, 'd': 70, 'rows': []}),
               P('frontiere18', 'borderPost', pos=[-3.6, GY, 0.0], opts={'length': 7.0, 'gantry': True}),
               P('baie18', 'parkLot', pos=[FAR18[0], GY, FAR18[2]], opts={'w': 3.4, 'd': 5.8, 'y': 0.02, 'color': '#6E7178', 'rows': [[0, 0, 1, 5]]}),
               HEROCAR('voiture18', [FAR18[0], r(GY + 0.02), FAR18[2]], 180, blink='both'),
               P('drapeau18', 'bayFlag', pos=[r(FAR18[0] - 2.4), GY, FAR18[2]], opts={'h': 4.6, 'fw': 1.6, 'colors': ['#7EC8E3', '#7A4A2A'], 'mark': 'star', 'markColor': '#F2C94C'}),
               P('sac18a', 'shoppingBag', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.4, 0.0]}), P('sac18b', 'shoppingBag', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.4, 0.0]})],
        cams=[C18])
st.cue('sfx:stepSoft', 'S18', 0.3, 0.2); st.cue('sfx:paper', 'S18', 0.8, 0.15); st.cue('sfx:stepSoft', 'S18', 1.6, 0.2); st.cue('sfx:tick', 'S18', 2.0, 0.1); st.cue('sfx:tick', 'S18', 2.7, 0.1)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
INV = {'preset': 'boss', 'suit': '#B8332B', 'lapel': '#8E2420', 'tie': '#F2C94C', 'facial': 'mustache', 'glasses': False, 'build': {'width': 0.92, 'headWidth': 1.25, 'belly': 0.08}, 'toon': EX}
st.write("La place", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'voleur': {**INV, 'seed': 900},
    'envahisseur': {**INV, 'seed': 901}, 'gris': {**INV, 'seed': 901, 'suit': '#9C9790', 'lapel': '#8A857E', 'tie': '#B8B2A6', 'hairColor': '#A8A399'},
    'general': {**SOLD, 'preset': 'commissaire', 'seed': 902, 'suit': '#4E5A34', 'lapel': '#3E4828', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}},
    **{f'soldat{i}': {**SOLD, 'preset': 'cop' if i % 2 else 'cop2', 'seed': 910 + i} for i in range(1, 7)},
    'musi1': {**SOLD, 'preset': 'cop', 'seed': 920}, 'musi2': {**SOLD, 'preset': 'cop2', 'seed': 921},
    'forces1': {**SPEC, 'preset': 'cop', 'seed': 930}, 'forces2': {**SPEC, 'preset': 'cop2', 'seed': 931},
    'client1': {'preset': 'madame', 'seed': 940, 'suit': '#2E7D4F', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'client2': {'preset': 'worker', 'seed': 941, 'hat': 'none', 'suit': '#1F4E8C', 'pants': '#22324A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'client3': {'preset': 'mamie', 'seed': 942, 'suit': '#7A2E4E', 'lapel': '#5A1E38', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'client4': {'preset': 'femme', 'seed': 943, 'suit': '#E0A030', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'chef1': {'preset': 'politique', 'seed': 950, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'sash': SASHES[0], 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef2': {'preset': 'politique', 'seed': 951, 'suit': '#3A4F6E', 'lapel': '#3A4F6E', 'tie': '#C8A030', 'sash': SASHES[1], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chef3': {'preset': 'politique', 'seed': 952, 'suit': '#4A3F5E', 'lapel': '#4A3F5E', 'tie': '#2E6B8C', 'sash': SASHES[2], 'sashW': 0.12, 'facial': 'mustache', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
})
