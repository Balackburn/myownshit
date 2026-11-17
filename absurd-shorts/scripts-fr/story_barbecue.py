#!/usr/bin/env python3
"""Le barbecue (story 83, cycle 45; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man was smoked out by his neighbour's barbecue. He cried chemical attack. The president set off the nuclear alert. The whole country put on
a gas mask. The army dropped a whole regiment. Only one landed on the grill. The others, on this man's house. Six sausages were taken prisoner.
A chipolata refused to talk. It was swapped for a spy. The army put the barbecue out with a flamethrower. The neighbourhood caught fire. The
paratrooper did not move. To reassure everyone, the minister ate a sausage. He was put in quarantine. The president decreed a national barbecue.
On the embers of the neighbourhood. Oh, and he was not invited.
Staging: over a low fence the neighbour's garden party laughs and clinks glasses round a small red kettle grill while he stands alone on his side
and a thick grey ribbon of smoke flows straight into his face; phone at his ear, a curl of smoke slipping into the receiver; the president winds
his fist up and slams a big red button flat, red sirens spin; a street crowd all in gas masks turns its heads as one to follow a single wisp; the
sky over the little garden fills with parachutes, the guests looking up with sausages on their forks; one paratrooper comes down sitting and lands
bottom-first on the grill, smoke from his trousers, and snaps a rigid salute; his house, the roof caved in under a heap of white canopies, boots
kicking out of the chimney, him in front in a gas mask; six sausages upright in a cell, a soldier slams the barred door (CAPTURÉES); in the
interrogation room a chipolata on a chair under the lamp, an officer slams the table, it hops and lands, silent; on a foggy bridge two soldiers
carry it away on a stretcher while a spy in a trench coat walks the other way; a gas-masked soldier blasts the grill with a flamethrower, the
paratrooper still saluting on it; the whole neighbourhood in flames, the grill a black lump in front (ÉTEINT); the paratrooper still saluting on
the charred grill, sooty, smoke rising; the minister bites a sausage under the flashes; a glass bubble drops over him mid-bite (QUARANTAINE); the
president raises a sausage on a fork like a toast before a giant smoking grill, a band, invented flags; soldiers and neighbours roast sausages on
sticks over the embers round the paratrooper, one holds a sausage out to him; framed like the first shot, he stands alone behind the charred stump
of his fence, gas mask on, an empty paper plate, the smoke drifting into his mask, while the neighbour clinks glasses with a general.
Natural look; cycle 45: props_barbecue.js (sausage, forkSausage, sausageStick, kettleGrill, smokeRibbon, bigRedButton, alarmSiren, parachuteSky,
parachute, cavedHouse, cellDoor, fogBridge, stretcher, flameThrower, fuelTanks, emberBed, sootPatches, paperPlate, partyGlass, gardenBunting,
bbqFlag, charredFence); gasMask (props_table), armyHelmet (props_guepe), smartPhone, cottage, fence, slab (props_cafe), table, flameField,
smokeField, burntTree, glassDome, cheekPuff (props_news), flashBursts (props_moustache), bandInstr (props_centime), fedoraHat (props_trou), shades
(props_feu), kepi, toonPuff (props_bocal), impactStars reused.
Lessons applied from the start: `lens` is the vertical field; faces and main props above the caption band (0.77-0.86); the man's right hand is at
-X when he faces +Z; every camera checked with project() before stills; flat grounds raised 5 cm or more on grassland; soot in charcoal-grey
patches, never a uniform face colour; the last shot is framed like the first."""
from story_kit import *
import math, os

st = Story('barbecue', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 19)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none',
        'gloves': '#2E3320', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 1.2, 'shift': 0.8, 'breathe': 1.4}}

# ---- the gardens (grassland): the low fence along Z at x 0; his lawn at -X, the neighbour's patio, grill and party at +X; their two cottages behind
GR = [0.9, 0, -1.3]                                    # the neighbour's red kettle grill, by the fence
H1 = [-0.9, 0, 1.6]; RY1 = -13                         # where he stands, on his side, facing us
FACE1 = off(H1, RY1, 0.12, 0.0, 1.76)                  # the front of his face
NB = [1.55, 0.06, -1.95]                               # the neighbour (chef's whites) beside the grill
G1, G2, G3 = [1.35, 0.06, -3.4], [1.95, 0.06, -2.75], [2.3, 0.06, -4.4]
HOUSE_H, HOUSE_N = [-6.8, 0, -9.5], [6.8, 0, -9.5]
BACK = [(-13.0, -22.0, '#EFC7C7', '#6A3A30'), (-1.5, -22.0, '#C9DDF0', '#B5402F'), (10.0, -22.0, '#F2B49A', '#4E5E7E'), (-7.0, -34.0, '#F4F2EC', '#B5402F'), (5.5, -34.0, '#E6CDE6', '#5E83C6'), (3.8, -15.5, '#F2E2A0', '#6A3A30'), (-4.5, -28.0, '#B9DDB0', '#B5402F')]
GARDEN_SET = {'clouds': 30, 'grass': '#86BE5C'}

def GARDEN(state='party', grill=True, para_char=False):
    """state: 'party' (summer, the party set), 'fire' (everything burning), 'burnt' (charred shells and embers)"""
    burnt, fire = state == 'burnt', state == 'fire'
    ps = []
    for (pid, p, col, roof) in [('maison', HOUSE_H, '#F2D58A', '#B5402F'), ('voisins', HOUSE_N, '#B9DDB0', '#4E5E7E')]:
        ps.append(P(pid, 'cottage', pos=p, opts={'w': 6.4, 'd': 7.0, 'h': 2.9, 'color': col, 'roof': roof, 'door': '#2F7F8C', 'burnt': burnt, 'seed': 3 if pid == 'maison' else 8}))
    for j, (x, z, col, roof) in enumerate(BACK):
        ps.append(P(f'arriere{j}', 'cottage', pos=[x, 0, z], opts={'w': 6.4, 'd': 7.0, 'h': 2.9, 'color': col, 'roof': roof, 'burnt': burnt, 'seed': 11 + j}))
    if burnt:
        ps.append(P('cloture', 'charredFence', pos=[0.0, 0, 0.0], ry=90, opts={'L': 9.0, 'seed': 5}))
        ps += [P(f'arbremort{j}', 'burntTree', pos=[x, 0, z], opts={'h': 4.5 + j * 0.4, 'seed': 30 + j}) for j, (x, z) in enumerate([(-5.2, -4.8), (8.2, -7.6), (-9.5, -15.0), (9.5, -16.5)])]
        ps.append(P('fumees', 'smokeField', pos=[0, 0, 0], opts={'points': [[-6.8, -9.5, 9], [6.8, -9.5, 8], [-1.5, -22, 10], [10, -22, 9]], 'size': 1.4, 'color': '#5A5450'}))
    else:
        ps.append(P('cloture', 'fence', pos=[0.0, 0, 0.0], ry=90, opts={'length': 9.0, 'height': 0.85, 'color': '#F6F4EE', 'rail': '#F6F4EE'}))
        ps.append(P('patio', 'slab', pos=[2.5, 0.03, -2.9], opts={'w': 4.6, 'h': 0.06, 'd': 4.6, 'color': '#D8C9AA'}))
        ps.append(P('nappe', 'table', pos=[3.4, 0.06, -3.9], ry=-20, opts={'w': 1.4, 'd': 0.8, 'h': 0.76, 'color': '#F2EEE4', 'legs': '#8A6A44'}))
        ps += [P(f'assiette{j}', 'paperPlate', pos=[r(3.4 + dx), 0.83, r(-3.9 + dz)]) for j, (dx, dz) in enumerate([(-0.45, 0.1), (0.0, 0.18), (0.42, 0.05)])]
        ps += [P('mat1', 'slab', pos=[0.55, 1.2, -5.0], opts={'w': 0.06, 'h': 2.4, 'd': 0.06, 'color': '#8A6A44'}),
               P('mat2', 'slab', pos=[4.3, 1.2, -5.0], opts={'w': 0.06, 'h': 2.4, 'd': 0.06, 'color': '#8A6A44'}),
               P('guirlande', 'gardenBunting', pos=[0, 0, 0], opts={'a': [0.55, 2.35, -5.0], 'b': [4.3, 2.35, -5.0], 'n': 14, 'sag': 0.35})]
    if fire:
        pts = []
        for (x, z) in [HOUSE_H[::2], HOUSE_N[::2]] + [(b[0], b[1]) for b in BACK]:
            pts += [[x - 1.6, 3.6, z + 0.5, 2.2], [x + 1.4, 3.9, z - 0.4, 2.4], [x, 4.8, z, 2.6], [x - 2.4, 1.0, z + 3.6, 1.4], [x + 2.2, 1.2, z + 3.6, 1.3]]
        pts += [[0.0, 0.3, z, 0.55] for z in (-3.8, -2.4, -0.4, 1.0, 2.6)] + [[3.4, 0.9, -3.9, 0.7], [2.4, 0.4, -5.0, 0.5]]
        ps.append(P('flammes', 'flameField', pos=[0, 0, 0], opts={'points': pts, 'seed': 7}))
        ps.append(P('fumees', 'smokeField', pos=[0, 0, 0], opts={'points': [[-6.8, -9.5, 14], [6.8, -9.5, 13], [-13, -22, 12], [-1.5, -22, 15], [10, -22, 12], [-7, -34, 12], [5.5, -34, 12]], 'size': 2.0}))
    if grill:
        ps.append(P('gril', 'kettleGrill', pos=GR, opts={'char': burnt or fire or para_char, 'smokeH': 0.9, 'smokeN': 8, 'smokeSize': 0.8, 'wind': [-0.3, 0.3]}))
    return ps

MASK = lambda pid, who: P(pid, 'gasMask', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
HELMET = lambda pid, who, **o: P(pid, 'armyHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95, **o})
KEPI = lambda pid, who, **o: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5730', 'band': '#2E3320', **o})
FORK = lambda pid, who, hand='R', roll=0.0, **o: P(pid, 'forkSausage', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.04, 0.03], 'face': 'camera', 'faceRoll': roll}, opts=o)
GLASS = lambda pid, who, hand='R', **o: P(pid, 'partyGlass', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.05, 0.03], 'face': 'camera'}, opts=o)
SOOT = lambda pid, who, at=None: P(pid, 'sootPatches', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, keys=([k(0.0, visible=False), k(at, visible=True)] if at is not None else []))

for g_ in [('S03', 0.98, 'president', 'button'), ('S06', 0.72, 'para', 'land'), ('S09', 0.86, 'officier', 'slam'), ('S15', 0.35, 'ministre', 'dome')]:
    st.gag(*g_)

# 1: the hook. Medium shot, him in the foreground on his lawn, facing us; over the low fence behind him the neighbour's garden party laughs and
#    clinks glasses round the little red kettle grill; a thick grey ribbon of smoke rises from the grill, rolls over the fence and flows straight
#    into his face; he does not move; a slow blink, then a little cough puff
D1 = st.dur('S01'); CLINK1 = 0.95; COUGH1 = 1.95
C1 = cam(0.0, [-1.75, 1.7, 5.4], [-1.67, 1.69, 5.15], [0.85, 1.35, -2.6], [0.82, 1.36, -2.6], lens=44)
MID12 = [r((G1[0] + G2[0]) / 2), 1.42, r((G1[2] + G2[2]) / 2)]
def CLINK(t0, who_p, other_p, hand='R'):
    mid = [r((who_p[0] + other_p[0]) / 2), 1.42, r((who_p[2] + other_p[2]) / 2)]
    return [k(r(t0 - 0.25), toon={'reach': {hand: [*add(who_p, [0, 1.25, 0.25]), 1, 0.04]}, 'hands': {hand: 'grip'}}, toonDur=0.0),
            k(r(t0 - 0.2), toon={'reach': {hand: [*mid, 1, 0.04]}, 'hands': {hand: 'grip'}}, toonDur=0.2, toonEase='out'),
            k(r(t0 + 0.15), toon={'reach': {hand: [*add(who_p, [0, 1.5, 0.25]), 1, 0.04]}, 'hands': {hand: 'grip'}}, toonDur=0.3)]
SMOKE1 = P('fumee1', 'smokeRibbon', pos=[0, 0, 0], opts={'pts': [add(GR, [0, 1.0, 0]), add(GR, [-0.2, 2.7, 0.7]), [-0.2, 2.45, 2.0], FACE1], 'n': 48, 's0': 0.05, 's1': 0.11, 'speed': 0.42, 'wob': 0.04, 'curl': 0.04})
st.shot('S01', 'grassland', setOpts=GARDEN_SET, actors=[
        act('mec', H1, RY1, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(1.3, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.12), k(1.5, toon={'face': DEAD}, toonDur=0.12),
            k(COUGH1, toon={'face': {'lid': 0.7, 'mouth': 'O', 'cheeks': 0.4}, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.05), k(r(COUGH1 + 0.15), toon={'face': DEAD, 'sq': [1, 1, 1]}, toonDur=0.15)]),
        act('voisin', NB, yaw(NB, [-1.6, 0, 4.6]), 'laugh', 'happy'),
        act('invite1', G1, yaw(G1, G2), 'stand', 'happy', keys=[k(0.0, look=add(G2, [0, 1.7, 0])), *CLINK(CLINK1, G1, G2), k(r(CLINK1 + 0.3), clip='laugh')]),
        act('invite2', G2, yaw(G2, G1), 'stand', 'happy', keys=[k(0.0, look=add(G1, [0, 1.7, 0])), *CLINK(CLINK1, G2, G1), k(r(CLINK1 + 0.35), clip='laugh')]),
        act('invite3', G3, yaw(G3, [-1.6, 0, 4.6]), 'laugh', 'happy')],
        props=[*GARDEN('party'), SMOKE1, FORK('fourchette1', 'voisin'), GLASS('verre1a', 'invite1'), GLASS('verre1b', 'invite2', color='#E8B84A'), GLASS('verre1c', 'invite3', hand='L'),
               P('toux1', 'toonPuff', pos=add(FACE1, [0, -0.08, 0.06]), opts={'at': COUGH1, 'n': 3, 'size': 0.07, 'life': 0.5, 'rise': 0.25, 'spread': 0.12, 'color': '#8E8A84'})],
        cams=[C1])
st.cue('sfx:clink', 'S01', CLINK1, 0.35); st.cue('sfx:grunt', 'S01', COUGH1, 0.2)

# 2: he cried chemical attack. Closer, still on his lawn: phone at his right ear, dead serious, he talks; a curl of the smoke slips over the fence
#    and into the receiver; the party carries on behind
D2 = st.dur('S02')
PHONE2 = off(H1, RY1, 0.1, 0.15, 1.66)
st.shot('S02', 'grassland', setOpts=GARDEN_SET, actors=[
        act('mec', H1, RY1, 'phoneEar', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.0), *st.talk('L02', 'S02', base='unimpressed')]),
        act('voisin', NB, yaw(NB, [-1.6, 0, 4.6]), 'laugh', 'happy'), act('invite2', G2, yaw(G2, G1), 'laugh', 'happy')],
        props=[*GARDEN('party'), P('tel2', 'smartPhone', on={'actor': 'mec', 'hand': 'R'}, opts={'call': True}), FORK('fourchette2', 'voisin'), GLASS('verre2b', 'invite2'),
               P('fumee2', 'smokeRibbon', pos=[0, 0, 0], opts={'pts': [add(GR, [0, 1.0, 0]), [0.3, 2.4, 0.3], [-0.5, 2.05, 2.1], PHONE2], 'n': 36, 's0': 0.04, 's1': 0.085, 'speed': 0.42, 'curl': 0.04})],
        cams=[cam(0.0, [-1.55, 1.8, 3.35], [-1.5, 1.79, 3.2], [-0.92, 1.66, 1.5], [-0.92, 1.66, 1.5], lens=40)])
st.cue('sfx:beep', 'S02', 0.05, 0.12)

# 3: the president set off the nuclear alert. His office: behind the desk, he winds his right fist up over his head (stretching tall) and slams it
#    down on the big red button: the dome squashes flat, he squashes with it, the desk jumps; two red sirens on the back wall start spinning and the
#    room turns red; he looks at us, satisfied
D3 = st.dur('S03'); HIT3 = 0.98
DESK3 = [0.0, 0, -1.2]; DH = 0.76; BTN3 = [-0.22, DH, -1.0]
PRES3 = [0.05, 0, -1.85]
LH3 = [0.35, r(DH + 0.04), -1.25, 1, 0.04]
def PK(t, pR, sq=(1, 1, 1), face=None, dur=0.12, ease='inOut', hand='fist', bend=0.0):
    return k(t, toon={'reach': {'R': [*pR, 1, 0.03], 'L': LH3}, 'hands': {'R': hand, 'L': 'open'}, 'sq': list(sq), 'bend': {'spine': [bend, 0, 0, 1, None]},
                      'face': face or {'lid': 0.25, 'mouth': 'line', 'brow': -0.6}}, toonDur=dur, toonEase=ease)
st.shot('S03', 'office', setOpts={'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#E9E1CF', 'band': '#2E4563', 'trim': '#1E2E44'}, actors=[
        act('president', PRES3, 0, 'stand', 'angry', keys=[k(0.0, look=[BTN3[0], 1.0, BTN3[2]]),
            PK(0.0, [-0.3, 1.1, -1.55], dur=0.0), PK(0.3, [-0.34, 1.3, -1.6], dur=0.15),
            PK(0.5, [-0.34, 2.4, -1.7], (0.93, 1.12, 0.93), {'lid': 0.1, 'mouth': 'clench', 'brow': -0.8}, 0.28, 'out'),
            PK(r(HIT3 - 0.1), [BTN3[0], 1.08, BTN3[2]], (1.02, 0.98, 1.02), dur=0.1, ease='in', bend=0.25),
            PK(HIT3, [BTN3[0], 1.0, BTN3[2]], (1.2, 0.78, 1.2), {'lid': 0.0, 'pop': 0.4, 'mouth': 'clench', 'brow': -0.9}, 0.04, 'out', bend=0.35),
            PK(r(HIT3 + 0.16), [BTN3[0], 1.02, BTN3[2]], (0.95, 1.07, 0.95), {'lid': 0.2, 'mouth': 'line', 'brow': -0.5}, 0.12, bend=0.2),
            PK(r(HIT3 + 0.34), [-0.32, 1.1, -1.5], (1, 1, 1), {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}, 0.25, hand='rest'),
            k(r(HIT3 + 0.45), look='camera', lookDur=0.15)])],
        props=[P('bureau3', 'table', pos=DESK3, opts={'w': 1.6, 'd': 0.9, 'h': DH, 'color': '#5A3E2B', 'legs': '#3E2A1C'},
                 keys=[k(HIT3, to=[0.0, 0.025, -1.2], dur=0.04), k(r(HIT3 + 0.05), to=DESK3, dur=0.1)]),
               P('bouton3', 'bigRedButton', pos=BTN3, opts={'pressAt': HIT3}),
               P('sirene3a', 'alarmSiren', pos=[-1.7, 2.65, -3.58], opts={'from': r(HIT3 + 0.04), 's': 1.6, 'power': 6, 'reach': 8}),
               P('sirene3b', 'alarmSiren', pos=[1.7, 2.65, -3.58], opts={'from': r(HIT3 + 0.04), 's': 1.6, 'power': 6, 'reach': 8}),
               P('etoiles3', 'impactStars', pos=[BTN3[0], r(DH + 0.18), BTN3[2]], opts={'at': HIT3, 'n': 5})],
        fx=[{'type': 'shake', 'at': HIT3, 'dur': 0.18, 'amount': 0.014}],
        cams=[cam(0.0, [0.45, 1.3, 1.3], [0.42, 1.3, 1.12], [-0.05, 1.38, -1.6], [-0.05, 1.38, -1.6], lens=50)])
st.cue('whoosh', 'S03', 0.5, 0.2); st.cue('thud', 'S03', HIT3, 0.55); st.cue('sfx:siren', 'S03', r(HIT3 + 0.05), 0.45)

# 4: the whole country put on a gas mask. A street of pastel cottages: a crowd standing in the road, every one of them in a gas mask (him in front
#    in his suit); a single wisp of smoke drifts across in front of them and every head turns together to follow it
D4 = st.dur('S04')
CROWD4 = [('mec', 0.0, 3.6), ('invite1', -0.85, 2.85), ('invite2', 0.9, 2.75), ('invite3', -0.35, 2.0), ('foule3', 0.45, 1.85), ('foule1', -1.25, 1.2), ('foule2', 1.3, 1.1)]
WISP0, WISP1 = [-3.6, 2.15, 5.0], [3.6, 2.35, 5.0]
def wisp_at(t): u = max(0.0, min(1.0, t / D4)); return [r(WISP0[i] + (WISP1[i] - WISP0[i]) * u) for i in range(3)]
LOOKS4 = [k(0.0, look=wisp_at(0.0))] + [k(r(t), look=wisp_at(t + 0.3), lookDur=0.3) for t in [0.15 + 0.3 * j for j in range(7)] if t < D4]
st.shot('S04', 'cottageStreet', actors=[act(who, [x, 0, z], 0, 'stand', 'neutral', keys=list(LOOKS4)) for (who, x, z) in CROWD4],
        props=[*[MASK(f'masque4{j}', who) for j, (who, _, _) in enumerate(CROWD4)],
               P('volute4', 'smokeRibbon', pos=WISP0, opts={'pts': [[0, 0, 0], [0.25, 0.1, 0], [0.5, 0.0, 0]], 'n': 10, 's0': 0.07, 's1': 0.11, 'speed': 0.9, 'shrink': False, 'wob': 0.03},
                 keys=[k(0.0, to=WISP1, dur=D4, ease='linear')])],
        cams=[cam(0.0, [0.4, 2.55, 10.5], [0.38, 2.5, 10.2], [0.0, 1.55, 2.2], [0.0, 1.55, 2.2], lens=38)])
st.cue('sfx:wind', 'S04', 0.0, 0.25); st.cue('sfx:sniff', 'S04', 0.6, 0.15)

# 5: the army dropped a whole regiment. Low in the little garden, looking up: the sky fills with parachutes coming down; in front, the guests and the
#    neighbour look up, sausages still on their forks
D5 = st.dur('S05')
SKY5 = [1.4, 12.0, -12.0]
G5 = [('voisin', [1.25, 0.06, -1.15]), ('invite1', [2.35, 0.06, -1.45]), ('invite2', [1.75, 0.06, -2.2]), ('invite3', [3.0, 0.06, -2.4])]
st.shot('S05', 'grassland', setOpts=GARDEN_SET, actors=[act(who, p, yaw(p, [2.0, 0, 1.6]), 'stand', 'surprised', keys=[k(0.0, look=add(SKY5, [j * 1.5 - 2, 0, 0])), k(r(0.6 + 0.1 * j), look=add(SKY5, [j * 1.5 - 2, -3.0, 2.0]), lookDur=0.8),
            k(0.0, toon={'reach': {'R': [*off(p, yaw(p, [2.0, 0, 1.6]), 0.3, 0.18, 1.15), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.0),
            k(r(1.2 + 0.12 * j), toon={'face': {'lid': 1.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.08, keepPose=True), k(r(1.32 + 0.12 * j), toon={'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.08, keepPose=True),
            k(r(1.6 + 0.05 * j), look=add(SKY5, [j * 1.5 - 1.2, -5.0, 4.0]), lookDur=0.35)])
            for j, (who, p) in enumerate(G5)],
        props=[*GARDEN('party'), *[FORK(f'fourchette5{j}', who) for j, (who, _) in enumerate(G5)],
               P('ciel5', 'parachuteSky', pos=[1.5, 0, -13.0], opts={'n': 34, 'w': 24, 'd': 22, 'y0': 7, 'y1': 30, 'v': 2.6})],
        cams=[cam(0.0, [2.05, 0.6, 1.55], [2.05, 0.62, 1.45], [1.4, 8.5, -9.0], [1.4, 9.2, -9.0], lens=62)])
st.cue('sfx:wind', 'S05', 0.0, 0.3); st.cue('whoosh', 'S05', 0.4, 0.3)

# 6: only one landed on the grill. Medium on the grill: a paratrooper comes down sitting, his canopy over him, and lands bottom-first on the
#    sausages: he squashes, the grill squashes, smoke puffs from his trousers; he snaps a rigid salute and holds it; his canopy collapses behind
#    him; the neighbour beside the grill freezes, eyes popping
D6 = st.dur('S06'); LAND6 = 0.72
PARA_P = [GR[0], 0.39, GR[2]]; PARA_RY = -8
SAL = lambda p, ry: [*off([p[0], 0, p[2]], ry, 0.12, 0.15, p[1] + 1.6), 1, 0.03]
def SALUTE(t, sq=(1, 1, 1), dur=0.1, face=None):
    return k(t, toon={'reach': {'R': SAL(PARA_P, PARA_RY), 'L': [*off([PARA_P[0], 0, PARA_P[2]], PARA_RY, 0.25, -0.22, PARA_P[1] + 0.55), 1, 0.04]}, 'hands': {'R': 'open', 'L': 'rest'},
                      'sq': list(sq), 'face': face or {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=dur, toonEase='out')
st.shot('S06', 'grassland', setOpts=GARDEN_SET, actors=[
        act('para', [GR[0], 2.5, GR[2]], PARA_RY, 'armsUp', 'neutral', keys=[k(0.0, look='camera'), k(0.0, to=PARA_P, dur=LAND6, ease='in'), k(r(LAND6 - 0.1), clip='sit'),
            k(LAND6, toon={'sq': [1.22, 0.74, 1.22], 'face': {'lid': 0.0, 'pop': 0.5, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.04, toonEase='out'),
            k(r(LAND6 + 0.1), toon={'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.1, 'pop': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.1),
            SALUTE(r(LAND6 + 0.25), (1.0, 1.02, 1.0), 0.08), SALUTE(r(LAND6 + 0.4))]),
        act('voisin', [1.75, 0.06, -1.75], yaw([1.75, 0, -1.75], [0.4, 0, 2.4]), 'stand', 'happy', keys=[k(0.0, look=[GR[0], 2.4, GR[2]]), k(0.4, look=[GR[0], 1.4, GR[2]], lookDur=0.25),
            k(LAND6, toon={'face': {'lid': 0.0, 'pop': 0.6, 'mouth': 'O', 'brow': 0.8}, 'sq': [0.94, 1.08, 0.94], 'reach': {'R': [*off([1.75, 0, -1.75], yaw([1.75, 0, -1.75], [0.4, 0, 2.4]), 0.3, 0.2, 1.2), 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.05),
            k(r(LAND6 + 0.12), toon={'face': {'lid': 0.1, 'pop': 0.3, 'mouth': 'O', 'brow': 0.6}, 'sq': [1, 1, 1], 'reach': {'R': [*off([1.75, 0, -1.75], yaw([1.75, 0, -1.75], [0.4, 0, 2.4]), 0.3, 0.2, 1.2), 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.15)])],
        props=[*GARDEN('party', grill=False),
               P('gril', 'kettleGrill', pos=GR, opts={'smokeH': 0.9, 'smokeN': 8, 'smokeSize': 0.8}, keys=[k(LAND6, squash=[1.18, 0.78, 1.18], dur=0.3)]),
               P('voile6', 'parachute', on={'actor': 'para', 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]}, opts={'collapseAt': r(LAND6 + 0.08), 'backSign': -1}),
               HELMET('casque6', 'para'), FORK('fourchette6', 'voisin'),
               P('fumee6', 'toonPuff', pos=add(GR, [0.05, 0.8, -0.32]), opts={'at': r(LAND6 + 0.02), 'n': 6, 'size': 0.09, 'life': 0.9, 'rise': 0.9, 'spread': 0.35, 'color': '#7A766F'}),
               P('fumee6b', 'smokeRibbon', pos=[0, 0, 0], keys=[k(0.0, visible=False), k(r(LAND6 + 0.15), visible=True)],
                 opts={'pts': [add(GR, [0.05, 0.85, -0.18]), add(GR, [0.1, 1.5, -0.25]), add(GR, [-0.05, 2.3, -0.2])], 'n': 14, 's0': 0.05, 's1': 0.13, 'speed': 0.5, 'shrink': False, 'color': '#A7A29A'})],
        fx=[{'type': 'shake', 'at': LAND6, 'dur': 0.15, 'amount': 0.012}],
        cams=[cam(0.0, [0.35, 1.5, 2.45], [0.36, 1.5, 2.3], [0.95, 1.75, -1.3], [0.95, 1.3, -1.3], lens=44, ease='out')])
st.cue('whoosh', 'S06', 0.15, 0.3); st.cue('thud', 'S06', LAND6, 0.5); st.cue('sfx:splat', 'S06', LAND6, 0.3); st.cue('sfx:poof', 'S06', r(LAND6 + 0.05), 0.25)

# 7: the others, on this man's house. His cottage: the roof caved in under a heap of white canopies, lines trailing down the front, a pair of boots
#    kicking out of the chimney; in front, him in his gas mask, facing us, motionless
D7 = st.dur('S07')
H7 = [-5.3, 0, -2.2]
st.shot('S07', 'grassland', setOpts=GARDEN_SET, actors=[act('mec', H7, yaw(H7, [-4.3, 0, 2.6]), 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.9, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(1.08, toon={'face': DEAD}, toonDur=0.1)])],
        props=[*[p_ for p_ in GARDEN('party', grill=False) if p_['id'] != 'maison'], MASK('masque7', 'mec'),
               P('maison7', 'cavedHouse', pos=HOUSE_H, opts={'color': '#F2D58A', 'roof': '#B5402F', 'kick': [0.0, 9.0]}),
               P('poussiere7', 'toonPuff', pos=add(HOUSE_H, [0.0, 3.6, 3.0]), opts={'at': 0.02, 'n': 8, 'size': 0.6, 'life': 0.9, 'rise': 1.0, 'spread': 2.4, 'color': '#E2DCCF'})],
        cams=[cam(0.0, [-4.0, 1.6, 3.4], [-4.05, 1.62, 3.2], [-6.0, 3.2, -8.0], [-6.0, 3.25, -8.0], lens=50)])
st.cue('sfx:crunch', 'S07', 0.02, 0.35); st.cue('sfx:stepHeavy', 'S07', 0.4, 0.15)

# 8: six sausages were taken prisoner. The cell: six sausages stand upright in a row on the floor behind the bars; a soldier slams the barred
#    door on them (CAPTURÉES): they flinch with the clang
D8 = st.dur('S08'); SLAM8 = 0.95
SAUS8 = [[r(-0.5 + 0.2 * i), 0.0, 1.35] for i in range(6)]
SOL8 = [0.72, 0, 3.25]; RY8 = yaw(SOL8, [-0.1, 0, 3.0])
DOOR_E = lambda a, x=0.8: [r(-0.55 + x * math.cos(a)), 1.15, r(2.65 - x * math.sin(a))]
st.card('S08', 'CAPTURÉES', at=r(SLAM8 + 0.12))
st.shot('S08', 'prisonCell', setOpts={'bars': False}, actors=[
        act('soldat', SOL8, RY8, 'stand', 'angry', keys=[k(0.0, look=[-0.2, 0.3, 1.35]),
            k(0.0, toon={'reach': {'R': [*DOOR_E(-1.1), 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(r(SLAM8 - 0.35), toon={'reach': {'R': [*DOOR_E(-1.15), 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.2),
            k(r(SLAM8 - 0.12), toon={'reach': {'R': [*DOOR_E(0.0), 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.12, toonEase='in'),
            k(r(SLAM8 + 0.25), toon={'reach': {'R': [*off(SOL8, RY8, 0.2, 0.25, 0.9), 1, 0.04]}, 'hands': {'R': 'rest'}, 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'sq': [1, 1, 1]}, toonDur=0.3),
            k(r(SLAM8 + 0.5), look='camera', lookDur=0.2)])],
        props=[P('grille8', 'cellDoor', pos=[0.0, 0, 2.6], opts={'w': 6.4, 'dx': -0.05, 'dw': 1.0, 'open': 1.1, 'slamAt': SLAM8}), HELMET('casque8', 'soldat'),
               *[P(f'saucisse8{i}', 'sausage', pos=p_, opts={'len': 0.36, 'r': 0.05, 'hop': [[r(SLAM8 + 0.02 + 0.015 * i), 0.05, 0.25]]}) for i, p_ in enumerate(SAUS8)]],
        fx=[{'type': 'shake', 'at': SLAM8, 'dur': 0.15, 'amount': 0.012}],
        cams=[cam(0.0, [0.3, 1.25, 8.4], [0.29, 1.23, 8.1], [0.15, 0.9, 2.0], [0.15, 0.88, 2.0], lens=34)])
st.cue('whoosh', 'S08', r(SLAM8 - 0.2), 0.2); st.cue('clang', 'S08', SLAM8, 0.6)

# 9: a chipolata refused to talk. The interrogation room: a single chipolata stands on the suspect's chair under the hanging lamp; an officer leans
#    over the table, winds up and slams both fists on it: the chipolata hops and lands back on the chair, silent
D9 = st.dur('S09'); SLAM9 = 0.86
OFF9 = [0.95, 0, -1.05]; RY9 = -90
FIST9 = lambda t, pr, pl, sq=(1, 1, 1), face=None, d=0.12, e='inOut', b=0.35: k(t, toon={'reach': {'R': [*pr, 1, 0.03], 'L': [*pl, 1, 0.03]}, 'hands': {'R': 'fist', 'L': 'fist'}, 'sq': list(sq),
                                                                                      'bend': {'spine': [b, 0, 0, 1, None]}, 'face': face or {'lid': 0.2, 'mouth': 'line', 'brow': -0.8}}, toonDur=d, toonEase=e)
st.shot('S09', 'interrogation', actors=[
        act('officier', OFF9, RY9, 'stand', 'angry', keys=[k(0.0, look=[0.0, 1.05, -1.45]),
            FIST9(0.0, [0.7, 1.15, -1.25], [0.7, 1.15, -0.8], d=0.0), FIST9(0.45, [0.78, 1.6, -1.25], [0.78, 1.6, -0.8], (0.95, 1.08, 0.95), {'lid': 0.1, 'mouth': 'clench', 'brow': -0.9}, 0.25, 'out', 0.05),
            FIST9(r(SLAM9 - 0.08), [0.5, 0.86, -1.2], [0.5, 0.86, -0.85], (1.02, 0.98, 1.02), d=0.08, e='in', b=0.15),
            FIST9(SLAM9, [0.5, 0.83, -1.2], [0.5, 0.83, -0.85], (1.15, 0.85, 1.15), {'lid': 0.0, 'mouth': 'O', 'brow': -0.9}, 0.04, 'out', 0.18),
            FIST9(r(SLAM9 + 0.18), [0.52, 0.85, -1.18], [0.52, 0.85, -0.85], (1, 1, 1), {'lid': 0.15, 'mouth': 'clench', 'brow': -0.8}, 0.15, b=0.12),
            k(r(SLAM9 + 0.6), look='camera', lookDur=0.2)]),],
        props=[KEPI('kepi9', 'officier'),
               P('chipolata9', 'sausage', pos=[0.0, 0.48, -1.45], opts={'len': 0.24, 'r': 0.028, 'color': '#C46A44', 'hop': [[r(SLAM9 + 0.02), 0.2, 0.45]]})],
        fx=[{'type': 'shake', 'at': SLAM9, 'dur': 0.15, 'amount': 0.012}],
        cams=[cam(0.0, [-0.2, 1.4, 2.35], [-0.18, 1.39, 2.15], [0.4, 1.12, -1.2], [0.4, 1.1, -1.2], lens=46)])
st.cue('thud', 'S09', SLAM9, 0.6); st.cue('sfx:tick', 'S09', 1.3, 0.12)

# 10: it was swapped for a spy. A long bridge in the fog, looking along it: two soldiers carry the chipolata away from us on a stretcher, along the
#     right-hand side; out of the fog a spy in a trench coat, hat and dark glasses walks toward us along the left; as they pass he glances at it
D10 = st.dur('S10'); BY = 6.0
P1A, P1B = [0.75, BY, -2.3], [0.75, BY, -5.6]
P2A, P2B = [0.75, BY, -0.35], [0.75, BY, -3.65]
SPYA, SPYB = [-0.75, BY, -9.0], [-0.75, BY, -3.6]
STR_A, STR_B = [0.75, r(BY + 0.8), -1.32], [0.75, r(BY + 0.8), -4.62]
WALK = lambda a, b: [k(0.0, to=b, dur=D10, clip='walk', ease='linear')]
st.shot('S10', 'grassland', setOpts={'clouds': 0, 'sky': ['#AEB8C0', '#D6DBDF'], 'grass': '#55616A'}, fog={'color': '#CDD3D8', 'near': 6, 'far': 32}, actors=[
        act('porteur1', P1A, 180, 'walk', 'neutral', keys=WALK(P1A, P1B)), act('porteur2', P2A, 180, 'walk', 'neutral', keys=WALK(P2A, P2B)),
        act('espion', SPYA, 0, 'walk', 'unimpressed', keys=[*WALK(SPYA, SPYB), k(0.0, look=[-0.75, r(BY + 1.6), 0.0]), k(0.95, look=[0.75, r(BY + 0.85), -3.3], lookDur=0.2), k(1.45, look=[2.2, r(BY + 2.2), 1.6], lookDur=0.25)])],
        props=[P('pont10', 'fogBridge', pos=[0.0, BY, -14.0], ry=90, opts={'L': 44, 'W': 4.2}),
               P('civiere10', 'stretcher', pos=STR_A, opts={'load': 'chipolata'}, keys=[k(0.0, to=STR_B, dur=D10, ease='linear')]),
               HELMET('casque10a', 'porteur1'), HELMET('casque10b', 'porteur2'),
               P('chapeau10', 'fedoraHat', on={'actor': 'espion', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'color': '#5A4A36'}),
               P('lunettes10', 'shades', on={'actor': 'espion', 'joint': 'head', 'offset': [0.0, 0.3, 0.095]}, opts={'ear': False})],
        cams=[cam(0.0, [2.0, r(BY + 4.3), 0.6], [1.95, r(BY + 4.25), 0.35], [0.1, r(BY + 0.6), -4.2], [0.1, r(BY + 0.6), -4.4], lens=48)])
st.cue('sfx:stepSoft', 'S10', 0.1, 0.2); st.cue('sfx:wind', 'S10', 0.0, 0.25)

# 11: the army put the barbecue out with a flamethrower. The garden, empty: a soldier in a gas mask, tanks on his back, braces at the fence and
#     blasts the little grill with a huge roaring jet of flame; the paratrooper is still sitting on it, still saluting; the grill turns black
D11 = st.dur('S11'); FIRE11 = 0.5; CHAR11 = 1.3
SOL11 = [-1.15, 0, 0.35]; RY11 = yaw(SOL11, GR)
GRIP11 = off(SOL11, RY11, 0.3, -0.12, 0.95)
LRY11 = yaw(GRIP11, GR)
FRONT11 = [r(GRIP11[0] + 0.48 * math.sin(math.radians(LRY11))), GRIP11[1], r(GRIP11[2] + 0.48 * math.cos(math.radians(LRY11)))]
HOLD11 = {'reach': {'R': [*GRIP11, 1, 0.03], 'L': [*FRONT11, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}}
PARA_SIT = lambda soot_at=None, extra=(): act('para', PARA_P, PARA_RY, 'sit', 'neutral', keys=[k(0.0, look='camera'), SALUTE(0.0, dur=0.0), *extra])
st.shot('S11', 'grassland', setOpts=GARDEN_SET, actors=[
        act('soldat', SOL11, RY11, 'stand', 'angry', keys=[k(0.0, look=[GR[0], 1.0, GR[2]]), k(0.0, toon={**HOLD11, 'sq': [1, 1, 1]}, toonDur=0.0),
            k(r(FIRE11 - 0.1), toon={**HOLD11, 'sq': [1.04, 0.96, 1.04], 'bend': {'spine': [0.15, 0, 0, 1, None]}}, toonDur=0.1),
            k(FIRE11, toon={**HOLD11, 'sq': [0.97, 1.03, 0.97], 'bend': {'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.06, toonEase='out'),
            k(r(FIRE11 + 0.12), toon={**HOLD11, 'sq': [1, 1, 1], 'bend': {'spine': [0.05, 0, 0, 1, None]}}, toonDur=0.15),
            *[k(r(FIRE11 + 0.35 + 0.22 * j), toon={**HOLD11, 'sq': [1.02, 0.98, 1.02] if j % 2 else [0.99, 1.01, 0.99], 'bend': {'spine': [0.08 if j % 2 else 0.0, 0, 0, 1, None]}}, toonDur=0.1) for j in range(7)]]),
        PARA_SIT(extra=[k(0.65, look=[SOL11[0], 1.6, SOL11[2]], lookDur=0.12), k(r(CHAR11 + 0.05), toon={'reach': {'R': SAL(PARA_P, PARA_RY)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'pop': 0.2, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.05, keepPose=True)])],
        props=[*GARDEN('party', grill=False), MASK('masque11', 'soldat'), HELMET('casque11', 'soldat'), HELMET('casque11p', 'para'), SOOT('suie11', 'para', CHAR11),
               P('reservoirs11', 'fuelTanks', on={'actor': 'soldat', 'joint': 'torso', 'offset': [0.0, 0.3, -0.2]}),
               P('lance11', 'flameThrower', pos=GRIP11, ry=LRY11, opts={'fire': [[FIRE11, r(D11 - 0.05)]], 'jet': 3.0, 'spread': 0.5}),
               P('gril', 'kettleGrill', pos=GR, opts={'charAt': CHAR11, 'smoke': False})],
        cams=[cam(0.0, [-3.25, 1.9, 3.25], [-3.15, 1.88, 3.08], [0.6, 1.15, -1.1], [0.62, 1.13, -1.1], lens=46)])
st.cue('sfx:roar', 'S11', FIRE11, 0.55); st.cue('whoosh', 'S11', r(FIRE11 - 0.05), 0.35)

# 12: the neighbourhood caught fire. Wide and low from his lawn: every house burning, smoke columns rising, the fence and the party table on fire;
#     the soldier stands in the middle with his lance; in front, the grill is a black lump with the paratrooper still sitting on it (ÉTEINT)
D12 = st.dur('S12')
SOL12 = [0.3, 0, -3.4]
st.card('S12', 'ÉTEINT', at=0.35)
st.shot('S12', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#A88C78', '#E2BC94']}, actors=[
        act('soldat', SOL12, yaw(SOL12, [-2.6, 0, 4.8]), 'stand', 'neutral', keys=[k(0.0, look=[6.8, 3.0, -9.5]), k(0.5, look=[-3.0, 3.0, -8.0], lookDur=0.35), k(1.0, look='camera', lookDur=0.2)]), PARA_SIT(extra=[k(0.9, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06, keepPose=True), k(1.0, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.06, keepPose=True)])],
        props=[*GARDEN('fire'), MASK('masque12', 'soldat'), HELMET('casque12', 'soldat'), HELMET('casque12p', 'para'), SOOT('suie12', 'para'),
               P('reservoirs12', 'fuelTanks', on={'actor': 'soldat', 'joint': 'torso', 'offset': [0.0, 0.3, -0.2]}),
               P('lance12', 'flameThrower', on={'actor': 'soldat', 'hand': 'R', 'offset': [0.0, -0.05, 0.02], 'rot': [1.2, 0.0, 0.0]}, opts={'fire': []})],
        cams=[cam(0.0, [-2.6, 1.15, 4.8], [-2.55, 1.17, 4.6], [2.6, 2.5, -9.0], [2.6, 2.6, -9.0], lens=50)])
st.cue('thunder', 'S12', 0.05, 0.35); st.cue('sfx:roar', 'S12', 0.1, 0.25)

# 13: the paratrooper did not move. Close on him, still sitting on the charred grill, still saluting, his face sooty in grey patches, smoke rising
#     from his trousers and his helmet; the houses burn behind him
D13 = st.dur('S13')
st.shot('S13', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#A88C78', '#E2BC94']}, actors=[PARA_SIT(extra=[k(1.25, toon={'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.05, keepPose=True), k(1.33, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.05, keepPose=True)])],
        props=[*GARDEN('fire'), HELMET('casque13', 'para'), SOOT('suie13', 'para'),
               P('fumee13a', 'smokeRibbon', pos=[0, 0, 0], opts={'pts': [add(GR, [0.12, 0.86, -0.1]), add(GR, [0.2, 1.6, -0.2]), add(GR, [0.05, 2.6, -0.3])], 'n': 16, 's0': 0.05, 's1': 0.15, 'speed': 0.45, 'shrink': False, 'color': '#6E6964'}),
               P('fumee13b', 'smokeRibbon', pos=[0, 0, 0], opts={'pts': [add(GR, [0.0, 1.95, 0.0]), add(GR, [0.08, 2.5, -0.05]), add(GR, [-0.1, 3.2, -0.1])], 'n': 10, 's0': 0.03, 's1': 0.09, 'speed': 0.5, 'shrink': False, 'color': '#5E5A56'})],
        cams=[cam(0.0, [0.4, 1.65, 1.65], [0.43, 1.65, 1.45], [0.88, 1.5, -1.3], [0.88, 1.5, -1.3], lens=44)])
st.cue('sfx:roar', 'S13', 0.0, 0.2); st.cue('sfx:tick', 'S13', 0.9, 0.1)

# 14: to reassure everyone, the minister ate a sausage. The press room: at the podium the minister holds up a sausage on a fork for the cameras,
#     smiles, then bites into it under a storm of flashes; his cheeks fill
D14 = st.dur('S14'); BITE14 = 1.55
MIN = [0.0, 0, -2.45]
PRESS = {'backdrop': 'SANTÉ|SÉCURITÉ|SANTÉ|SÉCURITÉ', 'chairs': False}
MOUTH = [0.0, 1.8, -2.32]
FK = lambda t, p, d=0.25, face=None, sq=(1, 1, 1), b=0.0: k(t, toon={'reach': {'R': [*p, 1, 0.03], 'L': [0.22, 1.17, -2.1, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': list(sq),
                                                                  'bend': {'spine': [b, 0, 0, 1, None]}, 'face': face or {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}}, toonDur=d, toonEase='inOut')
st.shot('S14', 'pressRoom', setOpts=PRESS, actors=[
        act('ministre', MIN, 0, 'stand', 'happy', keys=[k(0.0, look='camera'), FK(0.0, [-0.24, 1.25, -2.1], 0.0), FK(0.2, [-0.3, 1.62, -2.08], 0.3, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}),
            FK(r(BITE14 - 0.4), [-0.06, 1.42, -2.2], 0.3, {'lid': 0.3, 'mouth': 'O', 'brow': 0.2}, b=0.05),
            FK(BITE14, [-0.05, 1.4, -2.2], 0.06, {'lid': 0.4, 'mouth': 'clench', 'brow': 0.1, 'cheeks': 0.8}, (1.03, 0.97, 1.03), 0.12),
            FK(r(BITE14 + 0.25), [-0.22, 1.35, -2.1], 0.3, {'lid': 0.35, 'mouth': 'line', 'brow': 0.3, 'cheeks': 0.9}),
            k(r(BITE14 + 0.45), toon={'face': {'lid': 0.4, 'mouth': 'O', 'cheeks': 0.9}}, toonDur=0.08, keepPose=True), k(r(BITE14 + 0.6), toon={'face': {'lid': 0.3, 'mouth': 'line', 'cheeks': 0.9}}, toonDur=0.08, keepPose=True),
            k(r(BITE14 + 0.75), toon={'face': {'lid': 0.4, 'mouth': 'O', 'cheeks': 0.9}}, toonDur=0.08, keepPose=True)])],
        props=[FORK('fourchette14', 'ministre', len=0.2, r=0.034, bite=[BITE14, 0.45]),
               P('joueG14', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [0.1, 0.17, 0.1]}, opts={'growAt': BITE14, 'dur': 0.25, 'r': 0.055}),
               P('joueD14', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [-0.1, 0.17, 0.1]}, opts={'growAt': BITE14, 'dur': 0.25, 'r': 0.055}),
               P('flashs14', 'flashBursts', pos=[0.0, 1.05, -0.5], opts={'n': 8, 'w': 1.5, 'h': 0.5, 'from': 0.15, 'rate': 5, 'life': 0.14})],
        cams=[cam(0.0, [0.3, 1.72, 0.55], [0.28, 1.72, 0.35], [0.0, 1.62, -2.4], [0.0, 1.62, -2.4], lens=40)])
st.cue('sfx:shutter', 'S14', 0.2, 0.3); st.cue('sfx:shutter', 'S14', 0.8, 0.3); st.cue('sfx:crunch', 'S14', BITE14, 0.25)

# 15: he was put in quarantine. Same podium, a little wider: mid-chew, cheeks full, the fork at his mouth, a big glass bubble drops over him and
#     the podium, squashes as it lands and settles (QUARANTAINE); his eyes pop, then roll up to the dome; the flashes keep going
D15 = st.dur('S15'); DROP15 = 0.35
st.card('S15', 'QUARANTAINE', at=r(DROP15 + 0.12))
st.shot('S15', 'pressRoom', setOpts=PRESS, actors=[
        act('ministre', MIN, 0, 'stand', 'happy', keys=[k(0.0, look='camera'), FK(0.0, [-0.12, 1.38, -2.18], 0.0, {'lid': 0.35, 'mouth': 'line', 'cheeks': 0.9}),
            FK(DROP15, [-0.12, 1.38, -2.18], 0.04, {'lid': 0.0, 'pop': 0.5, 'mouth': 'clench', 'cheeks': 0.9, 'brow': 0.8}, (0.92, 1.1, 0.92)),
            FK(r(DROP15 + 0.15), [-0.12, 1.38, -2.18], 0.12, {'lid': 0.1, 'pop': 0.3, 'mouth': 'line', 'cheeks': 0.9, 'brow': 0.6}),
            k(r(DROP15 + 0.4), look=[0.0, 2.8, -2.2], lookDur=0.25), k(r(DROP15 + 1.0), look='camera', lookDur=0.2)])],
        props=[FORK('fourchette15', 'ministre', len=0.2, r=0.034, bite=[-1.0, 0.45]),
               P('joueG15', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [0.1, 0.17, 0.1]}, opts={'r': 0.055}),
               P('joueD15', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [-0.1, 0.17, 0.1]}, opts={'r': 0.055}),
               P('bulle15', 'glassDome', pos=[0.0, 4.2, -2.22], opts={'radius': 0.82, 'height': 2.6, 'base': False, 'opacity': 0.22},
                 keys=[k(r(DROP15 - 0.22), to=[0.0, 0.0, -2.22], dur=0.22, ease='in'), k(DROP15, squash=[1.12, 0.84, 1.12], dur=0.35)]),
               P('flashs15', 'flashBursts', pos=[0.0, 1.0, -0.4], opts={'n': 10, 'w': 1.7, 'h': 0.5, 'from': 0.05, 'rate': 7, 'life': 0.14})],
        fx=[{'type': 'shake', 'at': DROP15, 'dur': 0.15, 'amount': 0.01}],
        cams=[cam(0.0, [0.55, 1.62, 1.55], [0.5, 1.62, 1.35], [0.0, 1.45, -2.3], [0.0, 1.45, -2.3], lens=46)])
st.cue('whoosh', 'S15', r(DROP15 - 0.2), 0.3); st.cue('clang', 'S15', DROP15, 0.45); st.cue('sfx:shutter', 'S15', 0.5, 0.3)

# 16: the president decreed a national barbecue. On the ruins of the neighbourhood: the president raises a sausage on a fork like a toast before a
#     giant smoking grill; a band of two soldiers plays, invented flags wave, neighbours cheer
D16 = st.dur('S16'); TOAST16 = 0.4
PRES16 = [1.35, 0, -2.2]; RY16 = yaw(PRES16, [1.3, 0, 3.4])
BIG16 = [2.3, 0, -4.9]
CHEER = [('invite1', [2.45, 0, -1.1]), ('invite3', [2.9, 0, -3.0]), ('foule2', [0.2, 0, -1.0])]
st.shot('S16', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#9FB4C4', '#DADCD6']}, actors=[
        act('president', PRES16, RY16, 'stand', 'happy', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': [*off(PRES16, RY16, 0.3, 0.22, 1.2), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.0),
            k(TOAST16, toon={'reach': {'R': [*off(PRES16, RY16, 0.25, 0.3, 2.35), 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [0.94, 1.08, 0.94], 'face': {'lid': 0.1, 'mouth': 'smile', 'brow': 0.6}}, toonDur=0.25, toonEase='out'),
            k(r(TOAST16 + 0.3), toon={'reach': {'R': [*off(PRES16, RY16, 0.25, 0.3, 2.28), 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1, 1, 1], 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.2),
            k(1.5, toon={'reach': {'R': [*off(PRES16, RY16, 0.25, 0.3, 2.38), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15),
            k(1.7, toon={'reach': {'R': [*off(PRES16, RY16, 0.25, 0.3, 2.28), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15)]),
        act('musi1', [-0.15, 0, -3.3], yaw([-0.15, 0, -3.3], [1.3, 0, 3.4]), 'stand', 'neutral', keys=[k(r(0.2 + 0.5 * j), look=[1.3, 1.9 + 0.12 * (j % 2), 3.4], lookDur=0.12) for j in range(5)]),
        act('musi2', [0.45, 0, -3.9], yaw([0.45, 0, -3.9], [1.3, 0, 3.4]), 'stand', 'neutral', keys=[k(r(0.2 + 0.25 * j), look=[1.3, 1.5 + 0.15 * (j % 2), 3.4], lookDur=0.1) for j in range(10)]),
        *[act(who, p, yaw(p, PRES16), 'celebrate', 'happy') for who, p in CHEER]],
        props=[*GARDEN('burnt', grill=False),
               P('gril16', 'kettleGrill', pos=BIG16, scale=3.4, opts={'smokeH': 2.2, 'smokeN': 18, 'smokeSize': 1.2, 'wind': [-0.2, 0.0]}),
               FORK('fourchette16', 'president'), HELMET('casque16a', 'musi1'), HELMET('casque16b', 'musi2'),
               P('trompette16', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11], 'rot': [-0.3, -0.85, 0.0]}, opts={'kind': 'trumpet', 'beat': [0.2, 0.7, 1.2, 1.7, 2.2], 's': 1.15}),
               P('tambour16', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': [0.2, 0.45, 0.7, 0.95, 1.2, 1.45, 1.7, 1.95, 2.2]}),
               *[P(f'drapeau16{j}', 'bbqFlag', pos=p_, ry=a_, opts={'phase': j * 1.3}) for j, (p_, a_) in enumerate([([-0.6, 0, -4.6], 20), ([3.3, 0, -4.2], -25), ([2.8, 0, -6.9], -10)])]],
        cams=[cam(0.0, [1.3, 1.05, 3.4], [1.3, 1.08, 3.2], [1.6, 2.15, -3.0], [1.6, 2.2, -3.0], lens=54)])
st.cue('sfx:fanfare', 'S16', 0.1, 0.45)

# 17: on the embers of the neighbourhood. Low over a bed of glowing embers: soldiers and neighbours crouch in a row roasting sausages on long sticks;
#     in the middle, the paratrooper still sits saluting on the black grill; one of them holds a sausage out to him on her stick
D17 = st.dur('S17')
CROUCH = [('soldat', [-0.35, 0, -0.35]), ('invite1', [0.22, 0, -0.45]), ('invite2', [1.58, 0, -0.85]), ('foule2', [2.15, 0, -0.35])]
def STICK(pid, p, ry, tip):
    hand = off(p, ry, 0.35, 0.2, 0.55)
    dx, dy, dz = tip[0] - hand[0], tip[1] - hand[1], tip[2] - hand[2]; L = math.sqrt(dx * dx + dy * dy + dz * dz)
    rx = math.atan2(math.hypot(dx, dz), dy); ry_ = math.degrees(math.atan2(dx, dz))
    return P(pid, 'sausageStick', pos=hand, ry=r(ry_, 1), rot=[r(rx), 0.0, 0.0], opts={'L': r(L)}), hand
ST17 = []; ACT17 = []
for j, (who, p) in enumerate(CROUCH):
    ry = 0 if who != 'invite2' else -100
    tip = [r(p[0] + (0.08 if j % 2 else -0.08)), 0.32, 0.55] if who != 'invite2' else [r(PARA_P[0] + 0.22), r(PARA_P[1] + 1.2), r(PARA_P[2] + 0.3)]
    sp, hand = STICK(f'baton17{j}', p, ry, tip); ST17.append(sp)
    ACT17.append(act(who, p, ry, 'kneel', 'happy' if who != 'soldat' else 'neutral', keys=[k(0.0, look=tip if who != 'invite2' else 'camera'),
                 k(0.0, toon={'reach': {'R': [*hand, 1, 0.03]}, 'hands': {'R': 'grip'}}, toonDur=0.0)]))
st.shot('S17', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#9FB4C4', '#DADCD6']}, actors=[*ACT17, PARA_SIT(extra=[k(1.1, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06, keepPose=True), k(1.2, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.06, keepPose=True)])],
        props=[*GARDEN('burnt', grill=False), P('gril', 'kettleGrill', pos=GR, opts={'char': True, 'smokeN': 6, 'smokeH': 0.7}), HELMET('casque17', 'soldat'), HELMET('casque17p', 'para'), SOOT('suie17', 'para'),
               P('braises17', 'emberBed', pos=[0.9, 0.0, 0.55], opts={'w': 3.8, 'd': 1.0, 'lumps': 30, 'flames': 9, 'sparks': 18}), *ST17],
        cams=[cam(0.0, [0.9, 2.05, 3.9], [0.9, 2.03, 3.7], [0.9, 0.95, -0.7], [0.9, 0.97, -0.7], lens=46)])
st.cue('sfx:roar', 'S17', 0.0, 0.15); st.cue('sfx:tick', 'S17', 0.6, 0.1)

# 18: oh, and he was not invited. Framed exactly like the first shot: he stands alone on his lawn behind the charred stump of his fence, gas mask on,
#     an empty paper plate in his hand; a thread of the national barbecue's smoke drifts into his mask; behind him the neighbour clinks glasses with
#     a general; he looks down at the plate, then back at us
D18 = st.dur('S18'); CLINK18 = 1.15
NB18, GEN18 = [1.5, 0, -2.9], [2.15, 0, -2.7]
FILTER18 = off(H1, RY1, 0.24, 0.0, 1.68)
st.shot('S18', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#9FB4C4', '#DADCD6']}, actors=[
        act('mec', H1, RY1, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': [*off(H1, RY1, 0.32, -0.16, 1.05), 1, 0.04]}, 'hands': {'L': 'open'}, 'face': DEAD}, toonDur=0.0),
            k(0.55, look=[*off(H1, RY1, 0.4, -0.16, 1.0)], lookDur=0.25), k(1.6, look='camera', lookDur=0.25),
            k(2.3, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1, keepPose=True), k(2.45, toon={'face': DEAD}, toonDur=0.1, keepPose=True)]),
        act('voisin', NB18, yaw(NB18, GEN18), 'stand', 'happy', keys=[k(0.0, look=add(GEN18, [0, 1.7, 0])), *CLINK(CLINK18, NB18, GEN18), k(r(CLINK18 + 0.35), clip='laugh')]),
        act('general', GEN18, yaw(GEN18, NB18), 'stand', 'happy', keys=[k(0.0, look=add(NB18, [0, 1.7, 0])), *CLINK(CLINK18, GEN18, NB18), k(r(CLINK18 + 0.3), clip='laugh')])],
        props=[*GARDEN('burnt', grill=False), MASK('masque18', 'mec'),
               P('assiette18', 'paperPlate', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.06, 0.04], 'face': 'camera'}, opts={'r': 0.13, 'tiltX': 0.95}),
               P('gril18', 'kettleGrill', pos=[5.2, 0, -6.4], scale=3.4, opts={'smokeH': 2.0, 'smokeN': 16, 'smokeSize': 1.2, 'wind': [-0.6, 0.3]}),
               P('fumee18', 'smokeRibbon', pos=[0, 0, 0], opts={'pts': [[4.6, 6.8, -6.0], [2.0, 4.0, -1.0], [-0.2, 2.4, 2.2], FILTER18], 'n': 40, 's0': 0.1, 's1': 0.16, 'speed': 0.35, 'curl': 0.04}),
               GLASS('verre18a', 'voisin'), GLASS('verre18b', 'general', color='#E8B84A'), KEPI('kepi18', 'general')],
        cams=[{**C1}])
st.cue('sfx:clink', 'S18', CLINK18, 0.3); st.cue('sfx:sting', 'S18', 2.2, 0.25)

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
st.write("Le barbecue", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'voisin': {'preset': 'chef', 'seed': 831, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.14}, 'toon': EX},
    'invite1': {'preset': 'madame', 'seed': 832, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'invite2': {'preset': 'tourist', 'seed': 833, 'hat': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'invite3': {'preset': 'femme', 'seed': 834, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'foule1': {'preset': 'mamie', 'seed': 835, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'foule2': {'preset': 'worker', 'seed': 836, 'hat': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'foule3': {'preset': 'boss', 'seed': 837, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 838, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'hairColor': '#BDBDBD', 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12,
                  'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'para': {**SOLD, 'preset': 'cop', 'seed': 839},
    'soldat': {**SOLD, 'preset': 'cop2', 'seed': 840},
    'officier': {**SOLD, 'preset': 'cop', 'seed': 841, 'suit': '#4E5A32', 'facial': 'mustache'},
    'porteur1': {**SOLD, 'preset': 'cop', 'seed': 842}, 'porteur2': {**SOLD, 'preset': 'cop2', 'seed': 843},
    'espion': {'preset': 'commissaire', 'seed': 844, 'hat': 'none', 'suit': '#B79E72', 'lapel': '#A08A60', 'tie': '#3A3D44', 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 845, 'suit': '#3A4F6E', 'lapel': '#3A4F6E', 'tie': '#C8A030', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'musi1': {**SOLD, 'preset': 'cop', 'seed': 846}, 'musi2': {**SOLD, 'preset': 'cop2', 'seed': 847},
    'general': {'preset': 'politique', 'seed': 848, 'suit': '#4A5530', 'lapel': '#4A5530', 'tie': '#2E351E', 'glasses': False, 'facial': 'mustache', 'hairColor': '#9A9A96', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
})
