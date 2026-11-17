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
HEROCAR = lambda pid='voiture', pos=None, ry=-90, **o: CAR(pid, pos or HERO_CAR, ry, **{'color': BLUE, 'plate': BLUE_PLATE, 'blink': 'R', **o})
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
RED_PATH = [[-2.0, GY, -4.7], [0.2, GY, -5.9], [1.1, GY, -8.2], [1.25, GY, -10.0], KEY]
SEAT = lambda p, ry: loc(p, ry, 0.36 * CS, 0.06, 0.0)   # the driver's seat (the car's left, +X local), at the floor
HERO_SIT1 = SEAT(HERO_CAR, -90)
CA1 = cam(0.0, [17.6, 1.0, -6.4], [17.3, 0.98, -6.45], [7.6, 0.8, -7.3], [7.6, 0.78, -7.2], lens=56)
CB1 = cam(CUT1, [1.7, 2.05, -6.6], [1.85, 2.03, -6.45], [HERO_SIT1[0], 1.62, HERO_SIT1[2]], [HERO_SIT1[0], 1.62, HERO_SIT1[2]], lens=40)
chk('S01a', CA1['from'], CA1['lookAt'], 40, {'heroCarRear': loc(START1, -90, 0, -2.3, 0.8), 'heroCarStop': loc(HERO_CAR, -90, -0.9, -2.3, 0.8), 'bay': [1.25, 0.6, -10.6], 'redStart': [-14, 0.8, -4.7]})
chk('S01b', CB1['from'], CB1['lookAt'], 40, {'face': [HERO_SIT1[0], 1.75, HERO_SIT1[2]], 'blinkFR': loc(HERO_CAR, -90, -0.74 * CS, 1.85 * CS, 0.76 * CS)})
st.shot('S01', 'grassland', setOpts=LOT_SET, actors=[
        act('mec', SEAT(START1, -90), -90, 'drive', 'neutral', keys=[k(0.0, to=HERO_SIT1, dur=STOP1, ease='out', glide=True, face='keep', clip='drive'), k(0.0, look=[1.25, 1.0, -10.6]),
            k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(r(CUT1 + 0.05), toon={'face': {'lid': 0.0, 'pop': 0.45, 'mouth': 'O', 'brow': 0.7}, 'sq': [0.94, 1.08, 0.94]}, toonDur=0.05),
            k(r(CUT1 + 0.3), look=[1.0, 1.2, -9.5], lookDur=0.12), k(r(CUT1 + 0.3), toon={'face': {'lid': 0.15, 'pop': 0.1, 'mouth': 'O', 'brow': 0.4}, 'sq': [1, 1, 1]}, toonDur=0.12),
            k(r(CUT1 + 0.72), look='camera', lookDur=0.1), k(r(CUT1 + 0.72), toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.35}}, toonDur=0.1),
            *stand_blink(r(CUT1 + 1.0), {'lid': 0.45, 'mouth': 'line', 'brow': -0.35})]),
        act('voleur', add(RED_PATH[0], [-12.0, 0, 0]), 90, 'drive', 'smug', visible=False)],
        props=[LOT(), ROWS_INTACT(skip=['0:10']), STORE(clock=None),
               HEROCAR('voiture', START1, clear=True, brake=[BRAKE1, 0.45], keys=[k(0.0, to=HERO_CAR, dur=STOP1, ease='out')]),
               CAR('rouge', add(RED_PATH[0], [-12.0, 0, 0]), 90, color='#D8392B', plate='RX-001-ZZ', scale=1.0, hop=[[1.0, 0.07]],
                   keys=[k(0.0, path=RED_PATH, dur=1.0, ease='out', faceMove=True)])],
        cams=[CA1, CB1])
st.cue('engine', 'S01', 0.0, 0.25, 1.0); st.cue('sfx:brake', 'S01', BRAKE1, 0.5); st.cue('sfx:tick', 'S01', 0.1, 0.15); st.cue('sfx:tick', 'S01', 0.8, 0.15); st.cue('sfx:tick', 'S01', 1.5, 0.15); st.cue('sfx:gasp', 'S01', r(CUT1 + 0.05), 0.2)

# 2: the army confirmed the invasion. The war room: across a dark map table printed with the car park, the general (kepi, epaulettes), three
#    quarters to us on the left, winds up and stabs a red flag-pin into the red toy car in its bay; he stands stiffly on the right, three quarters
#    to us, pointing at it; the general straightens, satisfied
D2 = st.dur('S02'); STAB2 = 1.0
TAB2 = [0.0, 0, -1.2]; RED2 = [0.16, -0.14]            # the red toy car on the table (table frame)
TOY2 = [r(TAB2[0] + RED2[0]), 0.92, r(TAB2[2] + RED2[1])]
GEN2 = [-0.55, 0, -1.9]; RYG2 = 24; HERO2 = [0.6, 0, -2.0]; RYH2 = -22
C2 = cam(0.0, [0.3, 2.45, 3.9], [0.29, 2.43, 3.7], [-0.165, 0.95, -5.914], [-0.165, 0.96, -5.914], lens=29)
chk('S02', C2['from'], C2['lookAt'], 46, {'genFace': [GEN2[0], 1.95, GEN2[2]], 'heroFace': [HERO2[0], 1.95, HERO2[2]], 'toy': TOY2})
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
        act('mec', HERO2, RYH2, 'stand', 'unimpressed', keys=[k(0.0, look=TOY2), k(0.0, toon={'reach': {'R': [*add(TOY2, [0.35, 0.55, 0.15]), 1, 0.04]}, 'hands': {'R': 'point'}, 'face': DEAD}, toonDur=0.0),
            k(r(STAB2 + 0.02), toon={'reach': {'R': [*add(TOY2, [0.33, 0.52, 0.15]), 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, 'sq': [0.98, 1.02, 0.98]}, toonDur=0.06),
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
C3 = cam(0.0, [31.5, 1.5, 38.6], [31.9, 1.52, 38.5], [41.138, 1.75, 35.935], [41.3, 1.7, 35.935], lens=42)
chk('S03', C3['from'], C3['lookAt'], 36, {'mast': loc(SHIP, SHIP_RY, 0, -1.4, 6.4), 'bow': loc(SHIP, SHIP_RY, 0, 5.9, 1.5), 'boom': [33.8, 1.0, 36.5], 'island': [RING[0] - RI, 0.2, RING[2]]})
st.shot('S03', 'grassland', setOpts=LOT_SET, actors=[],
        props=[P('rondpoint3', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': SLAM3, 'cars': CARS3, 'speed': SP3}),
               P('navire3', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': AIM3, 'aimBlend': 0.28}),
               P('route3', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}), LOT()],
        fx=[{'type': 'shake', 'at': SLAM3, 'dur': 0.15, 'amount': 0.012}],
        cams=[C3])
st.cue('sfx:honk', 'S03', 0.2, 0.15); st.cue('clang', 'S03', SLAM3, 0.5); st.cue('sfx:rattleShort', 'S03', r(SLAM3 + 0.05), 0.25); st.cue('engine', 'S03', 1.1, 0.18, 0.8)

# 4: ultimatum, ten minutes to surrender. The supermarket front seen low from the car park: a giant red countdown clock on the roof flips on to
#    10:00 and starts ticking; soldiers march the shoppers out, each pushing a full trolley, toward us; a tank in the foreground aims its gun at
#    the doors
D4 = st.dur('S04'); FLIP4 = 0.25
CLK = {'x': 0.0, 'base': CLOCK0, 'flipAt': FLIP4}
SHOP4 = [('client1', [-1.0, GY, -13.6], [-2.2, GY, -10.2]), ('client2', [0.3, GY, -14.6], [-0.9, GY, -11.4]), ('client3', [-2.3, GY, -14.9], [-3.4, GY, -11.7])]
SOL4 = [('soldat1', [0.9, GY, -15.3], [-0.1, GY, -12.6]), ('soldat2', [-3.6, GY, -15.4], [-4.5, GY, -12.8])]
C4 = cam(0.0, [-2.4, 1.6, -4.9], [-2.38, 1.62, -5.15], [-0.6, 4.4, -15.5], [-0.6, 4.45, -15.5], lens=58)
chk('S04', C4['from'], C4['lookAt'], 58, {'clock': [0.0, 10.4, STORE_Z - 1.0], 'sign': [0, 8.0, STORE_Z - 0.4], 'door': [0, 1.5, STORE_Z], 'shopNear': [-2.2, 2.3, -10.2], 'shopNearFeet': [-2.2, 0.0, -10.2], 'tank': [3.9, 1.7, -9.9], 'redcar': [1.25, 1.3, -10.6]})
def TROLLEY(pid, a, b, dur):
    """a full trolley rolling ahead of a shopper from a to b (0.95 m in front of him), its handle toward him"""
    h = math.atan2(b[0] - a[0], b[2] - a[2]); f = [math.sin(h) * 0.95, 0, math.cos(h) * 0.95]
    return P(pid, 'fullTrolley', pos=add(a, f), keys=[k(0.0, path=[add(b, f)], dur=dur, ease='linear', faceMove=True, yawOffset=-90)])
st.shot('S04', 'grassland', setOpts=LOT_SET, actors=[
        *[act(w, a, yaw(a, b), 'stand', 'scared', keys=[k(0.0, to=b, dur=D4, clip='pushCartWalk'), k(0.0, look=[9.6, 1.8, -2.4])]) for w, a, b in SHOP4],
        *[act(w, a, yaw(a, b), 'stand', 'angry', keys=[k(0.0, to=b, dur=D4, clip='walk'), k(0.0, toon={'reach': {'R': [*off(b, yaw(a, b), 0.45, 0.05, 1.45), 1, 0.04], 'L': [*off(b, yaw(a, b), 0.35, -0.2, 1.35), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)])
          for w, a, b in SOL4]],
        props=[LOT(), ROWS_INTACT(skip=['0:7', '0:8', '0:9', '0:10', '0:11']), STORE(clock=CLK), CAR('rouge4', KEY, 180, color='#D8392B', plate='RX-001-ZZ', scale=1.0),
               *[TROLLEY(f'chariot4{i}', a, b, D4) for i, (w, a, b) in enumerate(SHOP4)],
               *[HELMET(f'casque4{i}', w) for i, (w, a, b) in enumerate(SOL4)], *[P(f'fusil4{i}', 'rifle', on={'actor': w, 'hand': 'R', 'offset': [0, -0.05, 0.05]}) for i, (w, a, b) in enumerate(SOL4)],
               ],
        cams=[C4])
st.cue('sfx:tick', 'S04', r(FLIP4 + 0.02), 0.35); st.cue('sfx:ticks', 'S04', r(FLIP4 + 0.4), 0.2); st.cue('sfx:stepHeavy', 'S04', 0.5, 0.15); st.cue('sfx:rattle', 'S04', 0.2, 0.12)

# 5: the invader was in the cheese aisle. Inside the emptied supermarket, alone in front of the cheese fridge, the red car's driver (red blazer)
#    holds a big plain cheese wheel to his nose with both hands and sniffs it, eyes closed in bliss, three quarters to us; a thin red laser beam
#    comes in from the right and its dot wanders over his shoulder and up the side of his head
D5 = st.dur('S05'); SNIFF5 = 0.55
INV5 = [-0.15, 0, -1.65]; RY5 = 26
NOSE5 = off(INV5, RY5, 0.42, 0.0, 1.5)
CHEESE5 = off(INV5, RY5, 0.4, 0.0, 1.3)
C5 = cam(0.0, [0.95, 1.8, 1.25], [0.88, 1.8, 1.1], [-0.15, 1.72, -1.6], [-0.15, 1.75, -1.6], lens=44)
chk('S05', C5['from'], C5['lookAt'], 44, {'face': [INV5[0], 1.98, INV5[2]], 'cheese': CHEESE5, 'shoulderR': off(INV5, RY5, 0.0, 0.3, 1.5), 'sign': [0, 2.35, -3.4]})
DOT5 = [[0.0, *off(INV5, RY5, 0.05, 0.36, 1.25)], [0.6, *off(INV5, RY5, 0.12, 0.38, 1.52)], [1.1, *off(INV5, RY5, 0.0, 0.33, 1.6)], [1.5, *off(INV5, RY5, 0.06, 0.24, 1.98)], [2.1, *off(INV5, RY5, 0.04, 0.2, 2.12)]]
st.shot('S05', 'supermarket', setOpts={'fr': True, 'signs': [['FROMAGES', '#2E6FB5', '#FFFFFF', -2.6, -3.2]]}, actors=[
        act('envahisseur', INV5, RY5, 'stand', 'happy', keys=[k(0.0, look=NOSE5),
            k(0.0, toon={'reach': {'R': [*off(INV5, RY5, 0.38, 0.25, 1.42), 1, 0.03], 'L': [*off(INV5, RY5, 0.38, -0.25, 1.42), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.0),
            k(SNIFF5, toon={'reach': {'R': [*off(INV5, RY5, 0.36, 0.25, 1.48), 1, 0.03], 'L': [*off(INV5, RY5, 0.36, -0.25, 1.48), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'smile', 'brow': 0.6, 'cheeks': 0.5}, 'sq': [0.96, 1.06, 0.96], 'bend': {'spine': [0.12, 0, 0, 1, None], 'neck': [0.22, 0, 0, 1, None]}}, toonDur=0.18, toonEase='out'),
            k(r(SNIFF5 + 0.5), toon={'reach': {'R': [*off(INV5, RY5, 0.36, 0.25, 1.45), 1, 0.03], 'L': [*off(INV5, RY5, 0.36, -0.25, 1.45), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'bigsmile', 'brow': 0.6, 'cheeks': 0.6}, 'sq': [1.02, 0.98, 1.02], 'bend': {'spine': [0.06, 0, 0, 1, None], 'neck': [0.1, 0, 0, 1, None]}}, toonDur=0.3),
            k(1.45, toon={'reach': {'R': [*off(INV5, RY5, 0.38, 0.25, 1.42), 1, 0.03], 'L': [*off(INV5, RY5, 0.38, -0.25, 1.42), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.9, 'mouth': 'smile', 'brow': 0.4, 'cheeks': 0.4}, 'sq': [0.97, 1.04, 0.97], 'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}}, toonDur=0.2)])],
        props=[P('frigo5', 'cheeseShelf', pos=[-0.2, 0, -2.75], opts={'w': 3.2}), P('fromage5', 'plainCheese', pos=CHEESE5, rot=[1.15, 0, 0], ry=RY5, opts={'r': 0.24, 'h': 0.14}),
               P('laser5', 'laserDot', pos=[0, 0, 0], opts={'pts': DOT5, 'src': [4.5, 2.7, 2.2], 'r': 0.03})],
        cams=[C5])
st.cue('sfx:sniff', 'S05', SNIFF5, 0.3); st.cue('sfx:sniff', 'S05', r(SNIFF5 + 0.32), 0.2); st.cue('sfx:tense', 'S05', 0.05, 0.12)

# 6: six planes bombed his car. Low on the car park beside the little red car in its bay: six fighter jets in a V roar in over our heads and away
#    toward the store; six fat bombs drop from them and fall, slow then fast, all on the red car; it bursts and squashes flat
D6 = st.dur('S06'); REL6 = 0.75; HIT6 = 1.72
JETS6 = [(0.0, 0.0), (-7.0, 7.0), (7.0, 7.0), (-14.0, 14.0), (14.0, 14.0), (0.0, 21.0)]   # (x offset, behind)
JZ0, JZ1, JY = 34.0, -60.0, 22.0
def jet_pos(dx, back, t): return [r(KEY[0] + dx), JY, r(JZ0 + back + (JZ1 - JZ0) * t / D6)]
C6 = cam(0.0, [5.8, 0.45, -2.2], [5.76, 0.46, -2.3], [2.2, 12.5, -15.0], [2.2, 12.0, -15.5], lens=66)
C6b = cam(1.0, [5.76, 0.5, -2.3], [5.72, 0.52, -2.4], [2.832, 2.606, -11.525], [2.832, 2.7, -11.525], lens=62)
chk('S06', C6['from'], C6['lookAt'], 66, {'redcar': [1.25, 0.6, -10.6], 'jetLeadRel': jet_pos(0, 0, REL6), 'jetLeadEnd': jet_pos(0, 0, D6 - 0.1), 'bombMid': [1.25, 12.0, -10.6]})
DROPS6 = [{'from': add(jet_pos(dx, back, REL6 + 0.03 * i), [0, -1.0, 0]), 'to': [r(KEY[0] + 0.12 * (i - 2.5)), 0.9, r(KEY[2] + 0.1 * (i % 3 - 1))], 't0': r(REL6 + 0.03 * i), 'dur': r(HIT6 - REL6 - 0.03 * i)} for i, (dx, back) in enumerate(JETS6)]
st.shot('S06', 'grassland', setOpts=LOT_SET, actors=[],
        props=[LOT(), ROWS_INTACT(skip=['0:10']), STORE(clock={**CLK, 'base': r(CLOCK0 - (st.SH['S06'][0] - st.SH['S04'][0] - FLIP4), 2), 'flipAt': -1}),
               CAR('rouge6', KEY, 180, color='#D8392B', plate='RX-001-ZZ', scale=1.0, flatAt=HIT6),
               *[P(f'avion6{i}', 'fighterJet', pos=jet_pos(dx, back, 0), ry=180, opts={'burner': 0.8, 'glow': 2.2}, keys=[k(0.0, to=jet_pos(dx, back, D6), dur=D6, ease='linear')]) for i, (dx, back) in enumerate(JETS6)],
               P('bombes6', 'bombDrop', pos=[0, 0, 0], opts={'drops': DROPS6, 's': 1.0}),
               P('boum6', 'timedBurst', pos=[KEY[0], 0.8, KEY[2]], opts={'at': HIT6, 'size': 2.2, 'seed': 6, 'life': 0.5}),
               P('fumee6', 'softDust', pos=[KEY[0], 0.6, KEY[2]], opts={'at': r(HIT6 + 0.05), 'n': 10, 'size': 1.4, 'life': 1.4, 'rise': 2.0, 'spread': 3.0, 'color': '#8E8982', 'opacity': 0.8})],
        fx=[{'type': 'shake', 'at': HIT6, 'dur': 0.3, 'amount': 0.03}, {'type': 'flash', 'at': HIT6, 'dur': 0.12}],
        cams=[C6, glide([C6b], 0.38)])
st.cue('sfx:jet', 'S06', 0.0, 0.55); st.cue('whoosh', 'S06', REL6, 0.3, 0.9); st.cue('thunder', 'S06', HIT6, 0.7); st.cue('sfx:crunch', 'S06', r(HIT6 + 0.04), 0.35)

# 7: and the two hundred spaces round it. High over the car park: every car squashed flat in its bay, smoking in neat rows, a lone hubcap rolling
#    across the lane; his blue car untouched in lane A, indicator blinking; the supermarket and its clock beyond; in the foreground the shoppers,
#    safe behind a crowd barrier, watch with their full trolleys
D7 = st.dur('S07')
CLK7 = {**CLK, 'base': r(CLOCK0 - (st.SH['S07'][0] - st.SH['S04'][0] - FLIP4), 2), 'flipAt': -1}
C7 = cam(0.0, [3.5, 11.5, 42.0], [3.4, 11.7, 41.7], [2.745, 7.425, 32.899], [2.745, 7.35, 32.8], lens=55)
SAFE7 = [('client1', [-1.5, GY, 29.3]), ('client2', [1.0, GY, 29.5]), ('client3', [3.6, GY, 29.2]), ('client4', [6.2, GY, 29.6])]
chk('S07', C7['from'], C7['lookAt'], 55, {'heroCar': HERO_CAR, 'store': [0, 6.5, STORE_Z], 'clock': [0.0, 10.4, STORE_Z], 'shopperHead': [1.0, 2.3, 29.5], 'barrier': [1.0, 1.0, 28.5], 'rowE': [0, 0.2, 21.5]})
st.shot('S07', 'grassland', setOpts=LOT_SET, actors=[act(w, p, 180, 'stand', 'surprised', keys=[k(0.0, look=[1.25, 1.0, -10.5])] + stand_blink(0.5 + 0.2 * i, {'lid': 0.1, 'mouth': 'O'})) for i, (w, p) in enumerate(SAFE7)],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=14), CAR('rougeplat7', KEY, 180, color='#D8392B', plate='RX-001-ZZ', scale=1.0, flat=True), HEROCAR('voiture7'),
               STORE(clock=CLK7), P('roue7', 'hubcap', pos=[-6.0, 0.28, 11.0], ry=90, opts={'r': 0.26, 'spin': 10}, keys=[k(0.0, to=[0.5, 0.28, 11.2], dur=D7, ease='linear')]),
               P('barriere7', 'crowdBarrier', pos=[2.2, GY, 28.5], opts={'length': 10.0}),
               *[P(f'chariot7{i}', 'fullTrolley', pos=add(p, [0.95, 0, 0.1]), ry=180) for i, (w, p) in enumerate(SAFE7)]],
        cams=[C7])
st.cue('sfx:wind', 'S07', 0.0, 0.25); st.cue('sfx:rattle', 'S07', 0.3, 0.12)

# 8: the supermarket too; it was badly parked. Low in front of the store: the invader stands outside the doors, cheese wheel under his arm, facing
#    us, untouched; behind him the empty supermarket folds flat like a cardboard box, front in, sides in, roof down, the sign and the clock tipping
#    onto the pile; a wall of dust rolls over him and leaves him grey (PLIÉ)
D8 = st.dur('S08'); FOLD8 = 0.55; GREY8 = r(FOLD8 + 0.5)
INV8 = [0.6, GY, -12.2]; RY8 = 18
CLK8 = {**CLK, 'base': r(CLOCK0 - (st.SH['S08'][0] - st.SH['S04'][0] - FLIP4), 2), 'flipAt': -1}
C8 = cam(0.0, [2.3, 1.35, -6.9], [2.25, 1.38, -7.05], [0.3, 3.3, -15.5], [0.3, 3.0, -15.5], lens=58)
chk('S08', C8['from'], C8['lookAt'], 58, {'face': [INV8[0], 1.98, INV8[2]], 'feet': INV8, 'roof': [0, 6.6, STORE_Z], 'pile': [0, 1.0, STORE_Z - 3]})
CHEESE_ARM = lambda pid, who: P(pid, 'plainCheese', on={'actor': who, 'joint': 'torso', 'offset': [-0.33, 0.12, 0.05]}, rot=[0, 0, 1.5708], opts={'r': 0.24, 'h': 0.14})
st.card('S08', 'PLIÉ', at=r(FOLD8 + 0.75))
INVK8 = lambda grey: [k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [*off(INV8, RY8, 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': 0.2}}, toonDur=0.0),
                      k(r(FOLD8 + 0.1), look=[0.3, 3.0, -16.0], lookDur=0.2),
                      k(r(FOLD8 + 0.42), toon={'reach': {'R': [*off(INV8, RY8, 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.7}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.06)] + \
                     ([k(r(GREY8 + 0.25), look='camera', lookDur=0.15), k(r(GREY8 + 0.25), toon={'reach': {'R': [*off(INV8, RY8, 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}, 'sq': [1, 1, 1]}, toonDur=0.15)] + stand_blink(r(GREY8 + 0.7), {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}) if grey else [])
st.shot('S08', 'grassland', setOpts=LOT_SET, actors=[
        act('envahisseur', INV8, RY8, 'stand', 'happy', keys=INVK8(False) + [k(0.0, visible=True), k(GREY8, visible=False)]),
        act('gris', INV8, RY8, 'stand', 'neutral', keys=INVK8(True) + [k(0.0, visible=False), k(GREY8, visible=True)])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=6), STORE(clock=CLK8, foldAt=FOLD8), CHEESE_ARM('fromage8a', 'envahisseur'), CHEESE_ARM('fromage8b', 'gris'),
               P('nuage8', 'softDust', pos=add(INV8, [0, 1.0, -0.6]), opts={'at': r(FOLD8 + 0.36), 'n': 12, 'size': 1.6, 'life': 1.3, 'rise': 1.6, 'spread': 2.4, 'color': '#D8D2C4', 'opacity': 0.95})],
        fx=[{'type': 'shake', 'at': r(FOLD8 + 0.38), 'dur': 0.3, 'amount': 0.025}],
        cams=[C8])
st.cue('sfx:crunch', 'S08', r(FOLD8 + 0.1), 0.35); st.cue('thud', 'S08', r(FOLD8 + 0.38), 0.7); st.cue('sfx:poof', 'S08', r(FOLD8 + 0.4), 0.4)

# 9: the invader was put under witness protection. In the lane, the folded store behind: two masked special forces walk the grey invader, a grey
#    blanket over his head, the cheese under his arm, to a black car; in the foreground he stands by his blue car (indicator blinking) and points
#    at them, outraged, mouth open
D9 = st.dur('S09')
INV9a, INV9b = [0.6, GY, -13.4], [-2.0, GY, -12.9]
BLACK9 = [-3.4, GY, -13.9]
HERO9 = [4.2, GY, -10.4]; RYH9 = -12
C9 = cam(0.0, [7.5, 2.0, -3.0], [7.4, 1.99, -3.15], [1.934, 0.62, -11.175], [1.9, 0.64, -11.175], lens=44)
chk('S09', C9['from'], C9['lookAt'], 44, {'heroFace': [HERO9[0], 1.98, HERO9[2]], 'invStart': [INV9a[0], 2.0, INV9a[2]], 'invEnd': [INV9b[0], 2.0, INV9b[2]], 'blackCar': BLACK9, 'heroCarFR': loc([7.0, GY, -9.4], -90, -0.74 * CS, 1.85 * CS, 0.76 * CS)})
FORCE9 = [('forces1', -0.62), ('forces2', 0.62)]
def PT9(d, h):
    """a point d metres from his right shoulder toward the invader, at height h"""
    sh = off(HERO9, RYH9, 0.0, 0.25, 0.0); dx, dz = INV9a[0] - sh[0], INV9a[2] - sh[2]; n = math.hypot(dx, dz); return [r(sh[0] + dx / n * d), h, r(sh[2] + dz / n * d)]
st.shot('S09', 'grassland', setOpts=LOT_SET, actors=[
        act('gris', INV9a, yaw(INV9a, INV9b), 'stand', 'neutral', keys=[k(0.0, to=INV9b, dur=D9, clip='walk'), k(0.0, toon={'reach': {'R': [*off(INV9b, yaw(INV9a, INV9b), 0.12, 0.42, 1.3), 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0)]),
        *[act(w, off(INV9a, yaw(INV9a, INV9b), -0.1, s), yaw(INV9a, INV9b), 'stand', 'neutral', keys=[k(0.0, to=off(INV9b, yaw(INV9a, INV9b), -0.1, s), dur=D9, clip='walk'),
            k(0.0, toon={'reach': {('L' if s > 0 else 'R'): [*off(INV9b, yaw(INV9a, INV9b), 0.05, s * 0.45, 1.45), 1, 0.04]}, 'hands': {('L' if s > 0 else 'R'): 'grip'}}, toonDur=0.0)]) for w, s in FORCE9],
        act('mec', HERO9, RYH9, 'stand', 'angry', keys=[k(0.0, look=[INV9a[0], 2.0, INV9a[2]]), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.0),
            k(0.35, toon={'reach': {'R': [*PT9(0.68, 1.78), 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.05, 'mouth': 'scream', 'brow': -0.9}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.08, toonEase='out'),
            k(0.55, toon={'reach': {'R': [*PT9(0.72, 1.82), 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.05, 'mouth': 'scream', 'brow': -0.9}, 'sq': [1, 1, 1]}, toonDur=0.1),
            k(1.0, look=[INV9b[0], 2.0, INV9b[2]], lookDur=0.8),
            *[k(r(0.8 + 0.22 * i), toon={'reach': {'R': [*PT9(0.72, 1.82 + 0.06 * (i % 2)), 1, 0.04]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.05, 'mouth': 'scream' if i % 2 == 0 else 'clench', 'brow': -0.9}}, toonDur=0.06) for i in range(7)]])],
        props=[LOT(), ROWS_FLAT(skip=['0:10', '0:11', '0:12', '0:13'], wisps=6), STORE(folded=True, clock=CLK8), HEROCAR('voiture9', [7.0, GY, -9.4]), CAR('noire9', BLACK9, -90, dark=True, plate='AA-000-AA'),
               CHEESE_ARM('fromage9', 'gris'), P('couverture9', 'blanketDrape', on={'actor': 'gris', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, rot=[-1.5708, 0, 0], opts={'w': 0.62, 'h': 0.9, 'color': '#8E9196'}),
               *[BALA(f'cagoule9{i}', w) for i, (w, s) in enumerate(FORCE9)]],
        cams=[C9])
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
MARCH11 = [('soldat1', 0.0), ('soldat2', 1.25), ('soldat3', 2.5), ('soldat4', 3.75), ('musi1', 5.0), ('soldat5', 6.25), ('musi2', 7.5), ('soldat6', 8.75)]
SPD11 = 1.15
HERO11 = [3.0, GY, -8.0]; RYH11 = 15
C11 = cam(0.0, [4.6, 6.2, -4.6], [4.55, 6.15, -4.75], [1.162, -0.25, -10.945], [1.162, -0.25, -10.945], lens=56)
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
AIM12 = [[0.0, turret_yaw(QUEUE[3])], [0.45, turret_yaw(QUEUE[2])], [0.95, turret_yaw(QUEUE[1])], [1.45, turret_yaw(QUEUE[0])]]
AIM12 = [[t, r(v * 1.6, 3)] for t, v in AIM12]           # a little more swing than the true bearing, so it reads
FRM12 = [36.4, 1.3, 37.6]
LK12, LN12 = [27.0, 1.25, 37.2], 46
C12 = cam(0.0, FRM12, add(FRM12, [-0.25, 0.0, 0.0]), LK12, LK12, lens=LN12)
print('S12 lens', LN12)
chk('S12', C12['from'], C12['lookAt'], C12['lens'], {'car0': QUEUE[0], 'car3': QUEUE[3], 'boom': [33.8, 1.0, 36.0], 'ship': loc(SHIP, SHIP_RY, 0, 0, 4.0), 'turret': loc(SHIP, SHIP_RY, 0, 2.4, 2.2)})
st.shot('S12', 'grassland', setOpts=LOT_SET, actors=[],
        props=[P('rondpoint12', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': 'down'}),
               P('navire12', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': AIM12, 'aimBlend': 0.3, 'counter': True, 'laps': [[0, 0]]}),
               P('route12', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}),
               *[CAR(f'officielle12{i}', p, 90, dark=True, flag=FLAGS[i], plate='CD-%03d-XX' % (12 + i), phase=0.2 * i) for i, p in enumerate(QUEUE)]],
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
LEAD13 = [('chef1', 14.0, FLAGS[0], 'R'), ('chef2', 0.0, FLAGS[1], 'R')]   # (who, angle lead, flag, the open window: the car's right faces us on the west side)
RAD13 = 10.95
C13 = cam(0.0, [31.0, 9.0, 47.0], [31.2, 8.9, 46.8], [41.6, 3.6, 37.2], [41.7, 3.55, 37.15], lens=58)
chk('S13', C13['from'], C13['lookAt'], 46, {'car1mid': ring_pos(sum(A13) / 2 + 12, RAD13), 'car2mid': ring_pos(sum(A13) / 2, RAD13), 'counter': loc(SHIP, SHIP_RY, 0, -0.65, 4.5), 'bow': loc(SHIP, SHIP_RY, 0, 5.9, 1.5)})
def leader(w, lead, side):
    """a leader standing in the car with his chest out of its left window (the car's left faces us on the west side), turned toward us"""
    lx = 0.95 * CS if side == 'L' else -0.95 * CS
    pts = arc_path(A13[0] + lead, A13[1] + lead, RAD13, lx, 0.05)
    p0 = [pts[0][0], -0.42, pts[0][2]]
    return act(w, p0, -90, 'stand', 'neutral', keys=[k(0.0, path=[[q[0], -0.42, q[2]] for q in pts[1:]], dur=D13, glide=True, face='keep'), k(0.0, look=[31.0, 9.0, 47.0])])
CARS13 = [P(f'officielle13{i}', 'bayCar', pos=arc_path(A13[0] + lead, A13[1] + lead, RAD13)[0], ry=r(A13[0] + lead + 90, 2), scale=CS,
            opts={'dark': True, 'flag': fl, 'open': side, 'plate': 'CD-%03d-XX' % (12 + i)}, keys=[k(0.0, path=arc_path(A13[0] + lead, A13[1] + lead, RAD13)[1:], dur=D13, ease='linear', faceMove=True)])
          for i, (w, lead, fl, side) in enumerate(LEAD13)]
SASHES = [['#6A3FA0', '#F2C94C'], ['#1E7A8C', '#E88AA8'], ['#E07A1F', '#1F2E5C']]
PASS13 = 0.9
st.shot('S13', 'grassland', setOpts=LOT_SET, actors=[
        leader('chef1', 14.0, 'R'), leader('chef2', 0.0, 'R')],
        props=[P('rondpoint13', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': 'down'}),
               P('navire13', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': [[0, 0.0]], 'counter': True, 'laps': [[0, 38], [0.55, 39], [1.25, 40]]}),
               P('route13', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}), *CARS13,
               P('page13a', 'treatySheet', on={'actor': 'chef1', 'hand': 'R', 'offset': [0.0, -0.04, 0.05], 'face': 'camera'}, opts={'w': 0.34, 'text': True}, keys=[k(0.0, visible=True), k(PASS13, visible=False)]),
               P('page13b', 'treatySheet', on={'actor': 'chef2', 'hand': 'L', 'offset': [0.0, -0.04, 0.05], 'face': 'camera'}, opts={'w': 0.34, 'text': True}, keys=[k(0.0, visible=False), k(PASS13, visible=True)])],
        cams=[C13])
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
HERO15 = [2.0, GY, -6.2]; RYH15 = -25
C15 = cam(0.0, [-3.2, 1.1, 1.0], [-3.1, 1.1, 0.75], [2.2, 3.4, -9.4], [2.2, 3.55, -9.4], lens=58)
chk('S15', C15['from'], C15['lookAt'], 58, {'towerTop': [1.25, 8.4, -10.5], 'towerFoot': [1.25, 0.3, -10.5], 'heroFace': [HERO15[0], 1.98, HERO15[2]], 'heroCarFR': loc([5.6, GY, -5.9], -90, -0.74 * CS, 1.85 * CS, 0.76 * CS)})
st.shot('S15', 'grassland', setOpts=LOT_SET, actors=[
        act('mec', HERO15, RYH15, 'stand', 'unimpressed', keys=[k(0.0, look=[1.25, 2.0, -10.5]), k(0.0, toon={'face': DEAD}, toonDur=0.0), k(0.3, look=[1.25, 8.0, -10.5], lookDur=0.9),
            k(1.25, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}, 'bend': {'neck': [-0.25, 0, 0, 1, None]}}, toonDur=0.4), *stand_blink(1.6, {'lid': 0.3, 'mouth': 'line', 'brow': 0.2})])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=4), STORE(folded=True, clock=CLK8), P('ruban15', 'bayTape', pos=KEYC, opts={'w': 2.5, 'l': 5.0}),
               P('tours15', 'tankTower', pos=KEYC, opts={'n': 5, 's': 0.62}), HEROCAR('voiture15', [5.6, GY, -5.9])],
        cams=[C15])
st.cue('sfx:rattle', 'S15', 0.1, 0.2); st.cue('sfx:honkTiny', 'S15', 1.2, 0.15)

# 16: this man pays the war reparations. In lane B, the flattened rows round them: he shakes his empty open wallet upside down over the general's
#     upturned helmet, held out like a bowl; behind them a line of soldiers holding out their helmets runs across the car park to the horizon
D16 = st.dur('S16')
HERO16 = [0.55, GY, 10.4]; RYH16 = 150; GEN16 = [-0.45, GY, 10.9]; RYG16 = -150
BOWL16 = [0.05, 1.32, 10.65]
C16 = cam(0.0, [0.1, 2.55, 5.3], [0.08, 2.54, 5.5], [0.05, 1.55, 15.6], [0.05, 1.56, 15.6], lens=30)
chk('S16', C16['from'], C16['lookAt'], 46, {'heroFace': [HERO16[0], 1.98, HERO16[2]], 'genFace': [GEN16[0], 1.98, GEN16[2]], 'bowl': BOWL16, 'lineFar': [16.0, 1.8, -40.0]})
st.shot('S16', 'grassland', setOpts=LOT_SET, actors=[
        act('mec', HERO16, RYH16, 'stand', 'unimpressed', keys=[k(0.0, look=BOWL16), *[k(r(0.15 + 0.17 * i), toon={'reach': {'R': [*add(BOWL16, [-0.12, 0.42 + (0.07 if i % 2 else 0.0), 0.05]), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.07) for i in range(8)],
            k(1.5, look='camera', lookDur=0.15), *stand_blink(1.7, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})]),
        act('general', GEN16, RYG16, 'stand', 'neutral', keys=[k(0.0, look=add(BOWL16, [-0.1, 0.4, 0])),
            k(0.0, toon={'reach': {'R': [*add(BOWL16, [0.17, -0.02, 0.0]), 1, 0.03], 'L': [*add(BOWL16, [0.02, -0.04, -0.12]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            *stand_blink(1.1, {'lid': 0.3, 'mouth': 'line'})])],
        props=[LOT(), ROWS_FLAT(skip=['0:10'], wisps=4), STORE(folded=True, clock=CLK8), KEPI('kepi16', 'general'),
               P('bol16', 'armyHelmet', pos=add(BOWL16, [0, -0.06, 0]), rot=[3.1416, 0, 0], opts={'s': 0.95}),
               P('portefeuille16', 'emptyWallet', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.06, 0.03], 'face': 'camera'}, rot=[3.1416, 0, 0], opts={'open': 0.55}),
               P('file16', 'helmetLine', pos=[0, 0, 0], opts={'path': [[0.0, 12.6], [0.4, 33.0], [2.0, 120.0]], 'gap': 1.1, 'y': GY, 'face': r(PI, 4)})],
        cams=[C16])
st.cue('sfx:rattleShort', 'S16', 0.2, 0.2); st.cue('sfx:rattleShort', 'S16', 0.75, 0.2); st.cue('sfx:cash', 'S16', 1.3, 0.12)

# 17: the blockade was never lifted. Months later at the roundabout: tall grass round the striped booms, the warship still on its island; low
#     behind his blue car waiting at the give-way line, its indicator blinking; the ship's gun swings round and stops on him
D17 = st.dur('S17'); AIMED17 = 1.05
CAR17 = [30.9, GY, 38.3]
C17 = cam(0.0, [24.4, 1.95, 40.2], [24.55, 1.96, 40.15], [33.983, 1.479, 37.383], [33.983, 1.5, 37.383], lens=37)
chk('S17', C17['from'], C17['lookAt'], 40, {'carRear': loc(CAR17, 90, 0, -2.3, 0.8), 'turret': loc(SHIP, SHIP_RY, 0, 2.4, 2.2), 'mast': loc(SHIP, SHIP_RY, 0, -1.4, 6.4), 'boom': [33.8, 1.0, 37.0]})
st.shot('S17', 'grassland', setOpts={**LOT_SET, 'sky': ['#9FC4D8', '#DCE6E4']}, actors=[],
        props=[P('rondpoint17', 'ringRoad', pos=[RING[0], 0, RING[2]], opts={'ri': RI, 'ro': RO, 'exitLen': 44, 'booms': 'down', 'grass': True}),
               P('navire17', 'warship', pos=SHIP, ry=SHIP_RY, opts={'aim': [[0, 1.2], [0.35, 1.2], [AIMED17, turret_yaw(CAR17)]], 'aimBlend': 0.6, 'counter': True, 'laps': [[0, 40]]}),
               P('route17', 'parkLot', pos=[-22.0, 0, 36.5], opts={'w': 59, 'd': 7, 'rows': []}),
               HEROCAR('voiture17', CAR17, 90, blink='L'),
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
            HB(0.0, d=0.0), HB(DUCK18[0], (1.12, 0.62, 1.12), 0.55, {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}, 0.12), HB(DUCK18[1], (1.12, 0.62, 1.12), 0.55, {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}, 0.3),
            HB(r(DUCK18[1] + 0.2), (0.96, 1.05, 0.96), 0.0, None, 0.12), HB(r(DUCK18[1] + 0.35), (1, 1, 1), 0.0, None, 0.1), *stand_blink(2.3, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})])],
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
