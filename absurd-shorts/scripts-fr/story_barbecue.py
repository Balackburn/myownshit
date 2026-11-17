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
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'bald',
        'gloves': '#2E3320', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.2, 'shift': 2.0, 'breathe': 2.0}}   # (round 1) bald: no hair through the helmets

# ---- the gardens (grassland): the low fence along Z at x 0; his lawn at -X, the neighbour's patio, grill and party at +X; their two cottages behind
GR = [0.9, 0, -1.3]                                    # the neighbour's red kettle grill, by the fence
H1 = [-0.9, 0, 1.6]; RY1 = -13                         # where he stands, on his side, facing us
FACE1 = off(H1, RY1, 0.12, 0.0, 1.76)                  # the front of his face
NB = [1.55, 0.06, -1.95]                               # the neighbour (chef's whites) beside the grill
G1, G2, G3 = [1.35, 0.06, -3.4], [1.95, 0.06, -2.75], [2.3, 0.06, -4.4]
HOUSE_H, HOUSE_N = [-6.8, 0, -9.5], [6.8, 0, -9.5]
BACK = [(-13.0, -22.0, '#EFC7C7', '#6A3A30'), (-1.5, -22.0, '#C9DDF0', '#B5402F'), (10.0, -22.0, '#F2B49A', '#4E5E7E'), (-7.0, -34.0, '#F4F2EC', '#B5402F'), (5.5, -34.0, '#E6CDE6', '#5E83C6'), (3.8, -15.5, '#F2E2A0', '#6A3A30'), (-4.5, -28.0, '#B9DDB0', '#B5402F')]
GARDEN_SET = {'clouds': 30, 'grass': '#86BE5C'}

SOOTS = ['#4A4440', '#3E3936', '#55504B', '#46413D']
def GARDEN(state='party', grill=True, para_char=False, gsmoke=None):
    """state: 'party' (summer, the party set), 'fire' (everything burning), 'burnt' (charred shells and embers)
    (round 1) burnt: the shells are soot-dark (the cottage's burnt mode takes its colour as the soot), with charred roof timbers and smoke wisps,
    and ash patches on the lawn"""
    burnt, fire = state == 'burnt', state == 'fire'
    ps = []
    for j, (pid, p, col, roof) in enumerate([('maison', HOUSE_H, '#F2D58A', '#B5402F'), ('voisins', HOUSE_N, '#B9DDB0', '#4E5E7E')]):
        ps.append(P(pid, 'cottage', pos=p, opts={'w': 6.4, 'd': 7.0, 'h': 2.9, 'color': SOOTS[j] if burnt else col, 'roof': roof, 'door': '#2F7F8C', 'burnt': burnt, 'seed': 3 if pid == 'maison' else 8}))
        if burnt: ps.append(P(f'poutres_{pid}', 'charredBeams', pos=p, opts={'w': 6.0, 'd': 6.6, 'h': 2.2, 'seed': 40 + j}))
    for j, (x, z, col, roof) in enumerate(BACK):
        ps.append(P(f'arriere{j}', 'cottage', pos=[x, 0, z], opts={'w': 6.4, 'd': 7.0, 'h': 2.9, 'color': SOOTS[(j + 2) % 4] if burnt else col, 'roof': roof, 'burnt': burnt, 'seed': 11 + j}))
        if burnt and j in (0, 1, 2, 5): ps.append(P(f'poutres_a{j}', 'charredBeams', pos=[x, 0, z], opts={'w': 6.0, 'd': 6.6, 'h': 2.0, 'n': 6, 'seed': 50 + j, 'smoke': j in (1, 5)}))
    if burnt:
        ps.append(P('cendres', 'ashPatches', pos=[0.5, 0, -4.0], opts={'w': 14, 'd': 12, 'n': 22, 'seed': 7}))
        ps.append(P('cloture', 'charredFence', pos=[0.0, 0, 0.0], ry=90, opts={'L': 9.0, 'seed': 5}))
        ps += [P(f'arbremort{j}', 'burntTree', pos=[x, 0, z], opts={'h': 4.5 + j * 0.4, 'seed': 30 + j}) for j, (x, z) in enumerate([(-5.2, -4.8), (8.2, -7.6), (-9.5, -15.0), (9.5, -16.5)])]
        ps.append(P('fumees', 'smokeField', pos=[0, 0, 0], opts={'points': [[6.8, -9.5, 6], [-1.5, -22, 7]], 'size': 0.9, 'color': '#6A645E'}))   # (final) thinner smoke: the charred shells and timbers read in outline, not a wall of smoke balls
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
        ps.append(P('gril', 'kettleGrill', pos=GR, opts={'char': burnt or fire or para_char, 'smokeH': 0.9, 'smokeN': 8 if gsmoke is None else gsmoke, 'smokeSize': 0.8, 'wind': [-0.3, 0.3]}))
    return ps
BURNT_SET = {'clouds': 12, 'grass': '#6C6253', 'sky': ['#B9C6CE', '#ECE6DA']}   # (final) a lighter sky: the charred timbers read in outline   # (round 1) scorched lawn, smoky sky; (round 2) the lawn grey-brown, not green

MASK = lambda pid, who: P(pid, 'gasMask', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
HELMET = lambda pid, who, **o: P(pid, 'armyHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95, **o})
KEPI = lambda pid, who, **o: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5730', 'band': '#2E3320', **o})
FORK = lambda pid, who, hand='R', roll=0.0, **o: P(pid, 'forkSausage', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.04, 0.03], 'face': 'camera', 'faceRoll': roll}, opts=o)
GLASS = lambda pid, who, hand='R', **o: P(pid, 'partyGlass', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.05, 0.03], 'face': 'camera'}, opts=o)
SOOT = lambda pid, who, at=None: P(pid, 'sootPatches', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, keys=([k(0.0, visible=False), k(at, visible=True)] if at is not None else []))

for g_ in [('S03', 0.98, 'president', 'button'), ('S06', 0.72, 'para', 'land'), ('S09', 0.86, 'officier', 'slam'), ('S15', 0.35, 'ministre', 'dome')]:
    st.gag(*g_)

# 1: the hook. Medium shot, him in the foreground on his lawn, facing us; over the low fence on the right the neighbour's garden party: three
#    guests in profile raise their glasses and clink them high, twice, the chef laughs with his fork; a ribbon of grey smoke leaves the little
#    red kettle grill, flows left in front of the party and straight into his nose; he breathes it, his eyes narrow, he coughs twice
#    (round 1: the party moved right of the grill so the smoke no longer hides the guests' heads; the ribbon comes in from in front of his face;
#    the clink is high and in profile; a readable double cough)
#    (round 2: the ribbon's tip reaches his nose and a sniff pulls it in; each cough is an inhale then a bend held three or four frames with a
#    puff; the clinking guests stand 1.2 m apart across the view, glasses raised over their heads, so the clink reads in silhouette; the chef laughs)
D1 = st.dur('S01'); CLINK1 = 0.85; CLINK1b = 1.62; SNIFF1 = 1.12; COUGH1 = 1.72; COUGH1b = 2.12
C1 = cam(0.0, [-1.75, 1.7, 5.4], [-1.67, 1.69, 5.15], [1.0, 1.35, -2.6], [0.98, 1.36, -2.6], lens=50)
NOSE1 = off(H1, RY1, 0.17, 0.0, 1.96)                 # just in front of his nose (the box head puts the nose near 1.95 m)
CTR1 = [1.95, 0.06, -2.3]; PERP1 = [0.887, 0.0, 0.461]   # the middle of the clink, and the horizontal across the camera's view there
GA, GB, GC = [r(CTR1[0] - 0.58 * PERP1[0]), 0.06, r(CTR1[2] - 0.58 * PERP1[2])], [r(CTR1[0] + 0.58 * PERP1[0]), 0.06, r(CTR1[2] + 0.58 * PERP1[2])], [2.1, 0.06, -3.35]
NB1 = [0.45, 0.06, -1.9]                             # the chef left of the grill, clear of the clink (the smoke goes over his head)
TOAST1 = [CTR1[0], 2.58, CTR1[2]]                    # where the glasses meet: over their heads
def CLINK(t0, who_p, meet, hand='R', low=1.55):
    """a raised clink: the glass comes up from chest height to the meeting point, taps, and drops back a little"""
    rest = [r(who_p[0] + (meet[0] - who_p[0]) * 0.3), low, r(who_p[2] + (meet[2] - who_p[2]) * 0.3)]
    tap = [r(who_p[0] + (meet[0] - who_p[0]) * 0.86), meet[1], r(who_p[2] + (meet[2] - who_p[2]) * 0.86)]
    return [k(r(t0 - 0.32), toon={'reach': {hand: [*rest, 1, 0.04]}, 'hands': {hand: 'grip'}}, toonDur=0.15),
            k(r(t0 - 0.12), toon={'reach': {hand: [*tap, 1, 0.04]}, 'hands': {hand: 'grip'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.12, toonEase='out'),
            k(r(t0 + 0.05), toon={'reach': {hand: [*add(tap, [0, 0.06, 0]), 1, 0.04]}, 'hands': {hand: 'grip'}, 'sq': [1, 1, 1]}, toonDur=0.06),
            k(r(t0 + 0.28), toon={'reach': {hand: [*add(rest, [0, 0.25, 0]), 1, 0.04]}, 'hands': {hand: 'grip'}}, toonDur=0.22)]
SMOKE1 = P('fumee1', 'smokeRibbon', pos=[0, 0, 0], opts={'pts': [add(GR, [0, 1.0, 0]), [0.55, 3.0, -0.9], off(H1, RY1, 0.7, -0.1, 2.2), NOSE1], 'n': 50, 's0': 0.045, 's1': 0.1,
                                                         'speed': 0.42, 'wob': 0.03, 'curl': 0.02})
COUGH = lambda t, s_=1.0: [k(r(t - 0.2), toon={'face': {'lid': 0.75, 'mouth': 'O', 'cheeks': 0.6, 'brow': 0.3}, 'sq': [0.97, 1.05, 0.97], 'bend': {'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.14),   # the inhale
                           k(t, toon={'face': {'lid': 1.0, 'mouth': 'O', 'cheeks': 0.1, 'brow': -0.4}, 'sq': [1 + 0.08 * s_, 1 - 0.1 * s_, 1 + 0.08 * s_], 'bend': {'spine': [0.3 * s_, 0, 0, 1, None]}}, toonDur=0.05, toonEase='out'),
                           k(r(t + 0.12), toon={'face': {'lid': 1.0, 'mouth': 'O', 'cheeks': 0.1, 'brow': -0.4}, 'sq': [1 + 0.06 * s_, 1 - 0.08 * s_, 1 + 0.06 * s_], 'bend': {'spine': [0.34 * s_, 0, 0, 1, None]}}, toonDur=0.1),   # the bend held
                           k(r(t + 0.26), toon={'face': {'lid': 0.7, 'mouth': 'line', 'brow': 0.2}, 'sq': [0.99, 1.02, 0.99], 'bend': {'spine': [0.06, 0, 0, 1, None]}}, toonDur=0.12)]
CHEF_LAUGH = lambda t0, t1: [k(r(t0 + 0.22 * i), toon={'face': {'mouth': 'laugh' if i % 2 == 0 else 'bigsmile', 'lid': 0.65, 'brow': 0.5}, 'sq': [1.03, 0.96, 1.03] if i % 2 == 0 else [0.98, 1.03, 0.98]}, toonDur=0.08) for i in range(int((t1 - t0) / 0.22) + 1)]
st.shot('S01', 'grassland', setOpts=GARDEN_SET, actors=[
        act('mec', H1, RY1, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.55, toon={'face': {'lid': 0.6, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.25),
            k(SNIFF1, look=[-1.75, 2.6, 5.4], lookDur=0.1), k(SNIFF1, toon={'face': {'lid': 0.85, 'mouth': 'line', 'brow': 0.2}, 'sq': [0.97, 1.05, 0.97], 'bend': {'spine': [-0.08, 0, 0, 1, None]}}, toonDur=0.08),   # the sniff: head up, chest up, eyes shut
            k(r(SNIFF1 + 0.22), look='camera', lookDur=0.12), k(r(SNIFF1 + 0.22), toon={'face': {'lid': 0.65, 'mouth': 'line'}, 'sq': [1, 1, 1]}, toonDur=0.12),
            *COUGH(COUGH1), *COUGH(COUGH1b, 0.75), k(r(COUGH1b + 0.36), toon={'face': DEAD, 'sq': [1, 1, 1]}, toonDur=0.12)]),
        act('voisin', NB1, yaw(NB1, [-1.6, 0, 4.6]), 'laugh', 'happy', keys=CHEF_LAUGH(0.0, D1)),
        act('invite1', GA, yaw(GA, GB), 'stand', 'happy', keys=[k(0.0, look=add(GB, [0, 1.8, 0])), *CLINK(CLINK1, GA, TOAST1), *CLINK(CLINK1b, GA, TOAST1), k(r(CLINK1 + 0.3), clip='laugh')]),
        act('invite2', GB, yaw(GB, GA), 'stand', 'happy', keys=[k(0.0, look=add(GA, [0, 1.8, 0])), *CLINK(CLINK1, GB, TOAST1), *CLINK(CLINK1b, GB, TOAST1), k(r(CLINK1 + 0.35), clip='laugh')]),
        act('invite3', GC, yaw(GC, [1.3, 0, 2.6]), 'stand', 'happy', keys=[k(0.0, look=TOAST1), *CLINK(CLINK1, GC, TOAST1, hand='L'), *CLINK(CLINK1b, GC, TOAST1, hand='L'), k(r(CLINK1 + 0.4), clip='laugh')])],
        props=[*GARDEN('party', gsmoke=5), SMOKE1, FORK('fourchette1', 'voisin'), GLASS('verre1a', 'invite1'), GLASS('verre1b', 'invite2', color='#E8B84A'), GLASS('verre1c', 'invite3', hand='L'),
               P('tinte1', 'twinkle', pos=TOAST1, opts={'at': CLINK1, 's': 0.12}), P('tinte1b', 'twinkle', pos=TOAST1, opts={'at': CLINK1b, 's': 0.12}),
               P('toux1', 'softDust', pos=add(NOSE1, [0.0, -0.22, 0.18]), opts={'at': r(COUGH1 + 0.03), 'n': 7, 'size': 0.16, 'life': 0.6, 'rise': 0.12, 'spread': 0.3, 'color': '#8E8982', 'opacity': 0.85}),
               P('toux1b', 'softDust', pos=add(NOSE1, [0.0, -0.22, 0.18]), opts={'at': r(COUGH1b + 0.03), 'n': 6, 'size': 0.14, 'life': 0.5, 'rise': 0.1, 'spread': 0.26, 'color': '#8E8982', 'opacity': 0.85})],
        cams=[C1])
st.cue('sfx:clink', 'S01', CLINK1, 0.35); st.cue('sfx:clink', 'S01', CLINK1b, 0.3); st.cue('sfx:grunt', 'S01', COUGH1, 0.25); st.cue('sfx:grunt', 'S01', COUGH1b, 0.18)

# 2: he cried chemical attack. Closer, still on his lawn: the phone in his left hand held flat against his left ear, dead serious, he talks
#    (mouth flapping on « crié »); a curl of the smoke comes in over the fence from the party, stretches and is sucked into the receiver; the
#    chef and a guest carry on laughing over his shoulder
#    (round 1: the phone is held at the ear in the frame of his face; the smoke ends in the receiver; the party stays in the frame)
#    (round 2: he is turned three-quarter so the phone sits on his visible left ear, along the jaw, receiver at the ear and mouthpiece at the jaw:
#    a slim red phone fixed to the side of his head, his hand on its lower end; a thin tendril of smoke is drawn into the mouthpiece; the chef
#    stands further right, clear of the arm; no stretch that pushed his head to the top of the frame)
D2 = st.dur('S02'); RY2 = -60
MOUTHPIECE2 = off(H1, RY2, 0.07, -0.15, 1.83)          # the lower end of the phone, by his jaw (his left side: s < 0)
EAR2 = {'touch': {'L': ['face', 0.62, 0.02, -0.04, 1, 0.0]}, 'hands': {'L': 'grip'}}   # a point on the face is a `touch`, not a `reach`; (final) lower on the phone: the elbow drops
W2 = [(0.27, 0.56), (0.67, 0.93), (1.01, 1.75)]                  # « crié », « l'attaque », « chimique » (the word times of L02 in the shot)
def FLAPS2():
    """(final) the mouth flaps on the words (toon keys replace the state: the touch on the phone is repeated in each), with a head bob on the stressed ones"""
    ks = []
    for j, (a, b) in enumerate(W2):
        n = max(2, int((b - a) / 0.1)); bob = 0.14 if j != 1 else 0.06
        for i in range(n + 1):
            t = r(a + (b - a) * i / n); op = i % 2 == 0 and i < n
            ks.append(k(t, toon={**EAR2, 'face': {'lid': 0.3, 'mouth': 'O' if op else 'line', 'brow': -0.6}, 'bend': {'spine': [0.02, 0, 0, 1, None], 'neck': [bob if (i == 0) else 0.03, 0, 0, 1, None]}}, toonDur=0.05))
    return ks
LOOK2 = off(H1, RY2, 3.0, 0.0, 1.85)
NB2 = [1.55, 0.06, -1.25]
st.shot('S02', 'grassland', setOpts=GARDEN_SET, actors=[
        act('mec', H1, RY2, 'stand', 'unimpressed', keys=[k(0.0, look=LOOK2), k(0.0, toon={**EAR2, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.0),
            *FLAPS2(), k(1.62, toon={**EAR2, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.5, 'gx': 0.8}, 'bend': {'spine': [0.0, 0, 0, 1, None], 'neck': [0.0, 0, 0, 1, None]}}, toonDur=0.12)]),
        act('voisin', NB2, yaw(NB2, [-1.6, 0, 4.6]), 'laugh', 'happy', keys=CHEF_LAUGH(0.0, D2)), act('invite1', [2.15, 0.06, -2.4], yaw([2.15, 0, -2.4], [-1.0, 0, 3.0]), 'laugh', 'happy')],
        props=[*GARDEN('party', gsmoke=4), P('tel2', 'earPhone', on={'actor': 'mec', 'joint': 'head', 'offset': [0.135, 0.2, 0.01]}), FORK('fourchette2', 'voisin'), GLASS('verre2a', 'invite1'),
               P('fumee2', 'smokeTendril', pos=[0, 0, 0], opts={'pts': [[0.55, 2.45, -0.5], [0.1, 2.5, 0.6], off(H1, RY2, 0.35, -0.5, 2.05), MOUTHPIECE2], 'at': 0.12, 'grow': 0.8, 'suck': 1.28, 'suckDur': 0.16,
                                                                'r0': 0.04, 'r1': 0.011, 'wob': 0.035, 'color': '#B8B3AA', 'opacity': 0.82})],   # (final) a thin tapering tendril that stretches to the phone and snaps into it
        cams=[cam(0.0, [-2.05, 1.8, 3.75], [-2.0, 1.8, 3.6], [-0.4, 1.7, 0.6], [-0.4, 1.7, 0.6], lens=44)])
st.cue('sfx:beep', 'S02', 0.05, 0.12)

# 3: the president set off the nuclear alert. His office: behind the desk, he winds his right fist up over his head (stretching tall) and slams it
#    down on the big red button: the dome squashes flat, he squashes with it, the desk jumps; two red sirens on the back wall start spinning and the
#    room turns red; he looks at us, satisfied
#    (round 1: a smear trail and a stretched body on the downswing; both sirens in the frame; a strong red wash)
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
            PK(0.8, [-0.36, 2.48, -1.72], (0.92, 1.14, 0.92), {'lid': 0.05, 'mouth': 'clench', 'brow': -0.9}, 0.1),
            PK(r(HIT3 - 0.1), [-0.42, 1.78, -1.36], (0.88, 1.16, 0.88), dur=0.06, ease='in', bend=0.18),
            PK(r(HIT3 - 0.04), [BTN3[0], 1.14, BTN3[2]], (1.0, 1.02, 1.0), dur=0.05, ease='in', bend=0.3),
            PK(HIT3, [BTN3[0], 1.0, BTN3[2]], (1.2, 0.78, 1.2), {'lid': 0.0, 'pop': 0.4, 'mouth': 'clench', 'brow': -0.9}, 0.04, 'out', bend=0.35),
            PK(r(HIT3 + 0.16), [BTN3[0], 1.02, BTN3[2]], (0.95, 1.07, 0.95), {'lid': 0.2, 'mouth': 'line', 'brow': -0.5}, 0.12, bend=0.2),
            PK(r(HIT3 + 0.34), [-0.32, 1.1, -1.5], (1, 1, 1), {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}, 0.25, hand='rest'),
            k(r(HIT3 + 0.45), look='camera', lookDur=0.15)])],
        props=[P('bureau3', 'table', pos=DESK3, opts={'w': 1.6, 'd': 0.9, 'h': DH, 'color': '#5A3E2B', 'legs': '#3E2A1C'},
                 keys=[k(HIT3, to=[0.0, 0.025, -1.2], dur=0.04), k(r(HIT3 + 0.05), to=DESK3, dur=0.1)]),
               P('bouton3', 'bigRedButton', pos=BTN3, opts={'pressAt': HIT3}),
               P('sirene3a', 'alarmSiren', pos=[-1.4, 2.5, -3.58], opts={'from': r(HIT3 + 0.04), 's': 1.6, 'power': 18, 'reach': 10, 'opacity': 0.28}),
               P('sirene3b', 'alarmSiren', pos=[0.45, 2.5, -3.58], opts={'from': r(HIT3 + 0.04), 's': 1.6, 'power': 18, 'reach': 10, 'opacity': 0.28}),
               P('trainee3', 'smearArc', pos=[0, 0, 0], opts={'pts': [[-0.36, 2.45, -1.72], [-0.5, 1.95, -1.42], [BTN3[0], 1.12, BTN3[2]]], 'win': [r(HIT3 - 0.13), r(HIT3 + 0.03)], 'r': 0.075, 'color': '#3A3E48', 'opacity': 0.5}),
               P('etoiles3', 'impactStars', pos=[BTN3[0], r(DH + 0.18), BTN3[2]], opts={'at': HIT3, 'n': 5})],
        fx=[{'type': 'shake', 'at': HIT3, 'dur': 0.18, 'amount': 0.014}],
        cams=[cam(0.0, [0.45, 1.3, 1.3], [0.42, 1.3, 1.12], [-0.05, 1.38, -1.6], [-0.05, 1.38, -1.6], lens=50)])
st.cue('whoosh', 'S03', 0.5, 0.2); st.cue('thud', 'S03', HIT3, 0.55); st.cue('sfx:siren', 'S03', r(HIT3 + 0.05), 0.45)

# 4: the whole country put on a gas mask. A street of pastel cottages: a crowd standing in the road, every one of them in a gas mask (him in front
#    in his suit); a single wisp of smoke drifts across in front of them and every head turns together to follow it
#    (round 2: the crowd stands frozen, masks to us; a thin wisp drifts in from the left IN FRONT of the masks at mask height; on one frame every
#    head snaps round to it together, then tracks it; he snaps a beat late)
D4 = st.dur('S04'); SNAP4 = 0.62; LATE4 = 0.86
CROWD4 = [('mec', 0.0, 3.6), ('invite1', -0.85, 2.85), ('invite2', 0.9, 2.75), ('invite3', -0.35, 2.0), ('foule3', 0.45, 1.85), ('foule1', -1.25, 1.2), ('foule2', 1.3, 1.1)]
WISP0, WISP1 = [-1.25, 1.98, 4.35], [2.6, 2.02, 4.35]  # just in front of him (z 3.6), at the height of the masks; (final) it starts at the frame's left edge
WIN4 = 0.12                                          # the wisp enters the frame then (before the heads snap at 0.62)
def wisp_at(t): u = max(0.0, min(1.0, (t - WIN4) / (D4 - WIN4))); return [r(WISP0[i] + (WISP1[i] - WISP0[i]) * u) for i in range(3)]
def LOOKS4(t_snap): return [k(0.0, look=[0.4, 2.0, 10.5]), k(t_snap, look=wisp_at(t_snap + 0.05), lookDur=0.04)] + [k(r(t), look=wisp_at(t + 0.25), lookDur=0.25) for t in [t_snap + 0.1 + 0.25 * j for j in range(8)] if t < D4]
st.shot('S04', 'cottageStreet', actors=[act(who, [x, 0, z], 0, 'stand', 'neutral', keys=LOOKS4(LATE4 if who == 'mec' else SNAP4)) for j, (who, x, z) in enumerate(CROWD4)],
        props=[*[MASK(f'masque4{j}', who) for j, (who, _, _) in enumerate(CROWD4)],
               *[P(f'souffle4{j}{i}', 'toonPuff', pos=[x, 1.66, r(z + 0.24)], opts={'at': r(0.2 + 0.23 * j + 0.85 * i), 'n': 2, 'size': 0.04, 'life': 0.5, 'rise': 0.12, 'spread': 0.05, 'color': '#E2DED6'})
                 for j, (_, x, z) in enumerate(CROWD4) for i in range(2)],
               P('volute4', 'smokeRibbon', pos=WISP0, opts={'pts': [[0, 0, 0], [-0.6, 0.08, 0], [-1.2, -0.03, 0], [-1.8, 0.06, 0]], 'n': 24, 's0': 0.075, 's1': 0.04, 'speed': 0.6, 'shrink': False, 'wob': 0.025, 'color': '#A9A49C'},
                 keys=[k(WIN4, to=WISP1, dur=r(D4 - WIN4), ease='linear')])],
        cams=[cam(0.0, [0.4, 2.55, 10.5], [0.38, 2.5, 10.2], [0.0, 1.55, 2.2], [0.0, 1.55, 2.2], lens=38)])
st.cue('sfx:wind', 'S04', 0.0, 0.25); st.cue('sfx:sniff', 'S04', 0.6, 0.15)

# 5: the army dropped a whole regiment. Low in the little garden, looking up: the sky fills with parachutes coming down; in front, the guests and the
#    neighbour look up, sausages still on their forks
D5 = st.dur('S05')
SKY5 = [1.4, 12.0, -12.0]
G5 = [('voisin', [1.25, 0.06, -1.15]), ('invite1', [2.35, 0.06, -1.45]), ('invite2', [1.75, 0.06, -2.2]), ('invite3', [3.0, 0.06, -2.4])]
st.shot('S05', 'grassland', setOpts=GARDEN_SET, actors=[act(who, p, yaw(p, [2.0, 0, 1.6]), 'stand', 'surprised', keys=[k(0.0, look=add(SKY5, [j * 1.5 - 2, 0, 0])), k(r(0.6 + 0.1 * j), look=add(SKY5, [j * 1.5 - 2, -3.0, 2.0]), lookDur=0.8),
            k(0.0, toon={'reach': {'R': [*off(p, yaw(p, [2.0, 0, 1.6]), 0.32, 0.2, 1.58), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.0),   # (round 1) forks raised, out of the caption band
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
SAL = lambda p, ry: [*off([p[0], 0, p[2]], ry, 0.06, 0.2, p[1] + 1.6), 1, 0.03]   # (final) the flat hand at the side of the helmet's rim, by the temple (in front, it covered an eye; higher, the arm went straight up)
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
#    (round 2: the ridge broken into a V; the canopies are light cloth domes with gore seams collapsed into it; the boots kick out of the chimney's
#    mouth; three soldiers hang by their lines from the gutter and a window lintel; soft dust; he breathes into his mask, which puffs, and his head
#    droops slowly)
st.shot('S07', 'grassland', setOpts=GARDEN_SET, actors=[act('mec', H7, yaw(H7, [-4.3, 0, 2.6]), 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.6, toon={'face': {'lid': 0.5, 'mouth': 'line'}, 'sq': [0.99, 1.02, 0.99], 'bend': {'spine': [0.04, 0, 0, 1, None]}}, toonDur=0.3),
            k(0.85, look=add(H7, [-0.4, 0.9, 2.2]), lookDur=0.6), k(1.1, toon={'face': {'lid': 0.6, 'mouth': 'line'}, 'sq': [1.02, 0.98, 1.02], 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.4),
            k(1.35, toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.02, 0.98, 1.02], 'bend': {'spine': [0.13, 0, 0, 1, None]}}, toonDur=0.08), k(1.45, toon={'face': {'lid': 0.6, 'mouth': 'line'}, 'sq': [1.02, 0.98, 1.02], 'bend': {'spine': [0.13, 0, 0, 1, None]}}, toonDur=0.08)])],
        props=[*[p_ for p_ in GARDEN('party', grill=False) if p_['id'] != 'maison'], MASK('masque7', 'mec'),
               P('maison7', 'cavedHouse', pos=HOUSE_H, opts={'color': '#F2D58A', 'roof': '#B5402F', 'kick': [0.0, 9.0], 'hang': [[-0.85, 0.55, 0.0], [2.6, 0.8, 1.7]], 'hangWin': [[1.92, 2.2, 0.35, 3.1]]}),
               P('poussiere7', 'softDust', pos=add(HOUSE_H, [0.0, 3.4, 3.4]), opts={'at': 0.0, 'n': 12, 'size': 1.2, 'life': 1.3, 'rise': 1.4, 'spread': 3.0, 'color': '#EDE7DA', 'opacity': 0.7}),
               *[P(f'souffle7{i}', 'toonPuff', pos=add(off(H7, yaw(H7, [-4.3, 0, 2.6]), 0.24, 0.0, 1.98), [0, 0, 0]), opts={'at': r(0.3 + 0.42 * i), 'n': 3, 'size': 0.05, 'life': 0.45, 'rise': 0.12, 'spread': 0.06, 'color': '#E8E4DC'}) for i in range(4)]],
        cams=[cam(0.0, [-4.0, 1.6, 3.4], [-4.05, 1.62, 3.2], [-6.0, 3.2, -8.0], [-6.0, 3.25, -8.0], lens=50)])
st.cue('sfx:crunch', 'S07', 0.02, 0.35); st.cue('sfx:stepHeavy', 'S07', 0.4, 0.15)

# 8: six sausages were taken prisoner. Low and close on the cell: six fat sausages stand upright in a row on the floor, each one framed in a gap
#    of the barred door; a long olive arm reaches in from the left edge, grips the open door and slams it on them (CAPTURÉES): they jump with a
#    stretch, hang, and land with a squash
#    (round 1: the sausages are three times bigger and lined up with the gaps of the bars; the soldier is only an arm, out of the card band)
D8 = st.dur('S08'); SLAM8 = 0.95
CAM8 = [-0.05, 0.5, 5.55]; ZB8, ZS8 = 2.65, 2.38             # the camera, the plane of the closed door's bars, the plane of the sausages
SAUS8 = [[r(-0.05 + (-0.55 + 0.2 * i + 0.05) * (CAM8[2] - ZS8) / (CAM8[2] - ZB8)), 0.0, ZS8] for i in range(6)]
#    (round 2: the arm comes in from the left edge at 0.35 s, grips the door, pulls it a little further open (anticipation), then yanks it shut)
SOL8 = [-1.05, 0, 3.4]; RY8 = 90
OPEN8 = 0.8; ANT8 = [0.62, 0.8, 0.18]                # the door's opening, and the anticipation (it is pulled open a little further first)
EDGE8 = lambda A, y=0.85, rad=0.55: [r(-0.75 + rad * math.cos(A)), y, r(ZB8 + rad * math.sin(A))]   # a bar of the door 0.55 m from its hinge, opened A rad (in the frame)
GRAB8 = lambda t, A, d=0.06, e='inOut', sq=(1, 1, 1), h='grip': k(t, toon={'reach': {'R': [*EDGE8(A), 1, 0.02]}, 'hands': {'R': h}, 'hose': 0.1, 'sq': list(sq)}, toonDur=d, toonEase=e)
OFF8 = [-1.0, 0.95, 3.25]                            # his hand out of the frame on the left, before it comes in
st.card('S08', 'CAPTURÉES', at=r(SLAM8 + 0.12))
st.shot('S08', 'prisonCell', setOpts={'bars': False}, actors=[
        act('soldat', SOL8, RY8, 'stand', 'angry', keys=[k(0.0, look=[-0.2, 0.3, 2.4]), k(0.0, toon={'reach': {'R': [*OFF8, 1, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.0),
            k(0.35, toon={'reach': {'R': [*OFF8, 1, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.05),
            GRAB8(0.5, OPEN8, 0.15, 'out', h='open'), GRAB8(0.56, OPEN8, 0.05),
            GRAB8(ANT8[1], OPEN8 + ANT8[2], r(ANT8[1] - ANT8[0]), sq=(0.97, 1.03, 0.97)), GRAB8(r(SLAM8 - 0.06), 0.5, 0.06, 'in'), GRAB8(SLAM8, 0.0, 0.06, 'in'),
            k(r(SLAM8 + 0.18), toon={'reach': {'R': [*OFF8, 1, 0.04]}, 'hands': {'R': 'rest'}}, toonDur=0.2)])],
        props=[P('grille8', 'cellDoor', pos=[0.0, 0, 2.6], opts={'w': 6.4, 'dx': -0.05, 'dw': 1.4, 'open': OPEN8, 'antic': ANT8, 'slamAt': SLAM8}), HELMET('casque8', 'soldat'),
               *[P(f'saucisse8{i}', 'sausage', pos=p_, opts={'len': 0.5, 'r': 0.064, 'hop': [[r(SLAM8 + 0.02 + 0.02 * i), 0.17, 0.52, 0.3]]}) for i, p_ in enumerate(SAUS8)]],
        fx=[{'type': 'shake', 'at': SLAM8, 'dur': 0.15, 'amount': 0.014}],
        cams=[cam(0.0, CAM8, [-0.05, 0.49, 5.4], [-0.05, 0.36, ZS8], [-0.05, 0.36, ZS8], lens=40)])
st.cue('whoosh', 'S08', r(SLAM8 - 0.15), 0.2); st.cue('clang', 'S08', SLAM8, 0.6)

# 9: a chipolata refused to talk. The interrogation room: on the suspect's chair, on a stack of phone books, a single chipolata stands in the
#    lamp's pool of light; the officer, three-quarter to us, leans over the table, winds both fists up and slams them down: the chipolata jumps,
#    hangs in the air and lands back on the books, silent; he glares at it, then at us
#    (round 1: lower and closer, the chipolata twice as big and lit; the officer's face in the frame; both fists; a held hang on the hop)
D9 = st.dur('S09'); SLAM9 = 0.86
OFF9 = [0.8, 0, -0.85]; RY9 = -62
BOOKS9 = [0.0, 0.47, -1.45]; NB9 = 9; TOPB9 = r(BOOKS9[1] + 0.055 * NB9)   # (final) a taller stack, so it shows over the table
CHIP9 = [0.0, TOPB9, -1.45]
FL9 = lambda f, sd, y: off(OFF9, RY9, f, sd, y)
#    (round 2: the room is dark round a hard pool of lamp light on the chipolata (a cone from the lamp); the officer's spine bends less and he looks
#    at a point between the chipolata and us, so his face stays toward the lens through the slam and the hang)
FACE9 = [-0.25, 1.5, 0.4]                                   # where he looks during the slam: between the chipolata and the lens
FIST9 = lambda t, f, y, sq=(1, 1, 1), face=None, d=0.12, e='inOut', b=0.35: k(t, toon={'reach': {'R': [*FL9(f, 0.2, y), 1, 0.03], 'L': [*FL9(f, -0.2, y), 1, 0.03]}, 'hands': {'R': 'fist', 'L': 'fist'}, 'sq': list(sq),
                                                                              'bend': {'spine': [b, 0, 0, 1, None]}, 'face': face or {'lid': 0.2, 'mouth': 'line', 'brow': -0.8}}, toonDur=d, toonEase=e)
st.shot('S09', 'interrogation', actors=[
        act('officier', OFF9, RY9, 'stand', 'angry', keys=[k(0.0, look=add(CHIP9, [0, 0.4, 0])), k(0.3, look=FACE9, lookDur=0.15),
            FIST9(0.0, 0.38, 0.95, d=0.0, b=0.08), FIST9(0.46, 0.24, 2.48, (0.93, 1.09, 0.93), {'lid': 0.1, 'mouth': 'clench', 'brow': -0.9}, 0.26, 'out', -0.1),   # (final) both fists high over his head...
            FIST9(0.74, 0.22, 2.55, (0.92, 1.1, 0.92), {'lid': 0.05, 'mouth': 'clench', 'brow': -0.95}, 0.24, b=-0.12),                                    # ...held four frames
            FIST9(r(SLAM9 - 0.07), 0.43, 1.0, (0.92, 1.1, 0.92), d=0.04, e='in', b=0.06),
            FIST9(SLAM9, 0.45, 0.83, (1.16, 0.84, 1.16), {'lid': 0.0, 'mouth': 'scream', 'brow': -0.9}, 0.04, 'out', 0.12),
            FIST9(r(SLAM9 + 0.18), 0.45, 0.85, (1, 1, 1), {'lid': 0.15, 'mouth': 'clench', 'brow': -0.8}, 0.15, b=0.1),
            FIST9(r(SLAM9 + 0.75), 0.45, 0.85, (1, 1, 1), {'lid': 0.25, 'mouth': 'line', 'brow': -0.9}, 0.2, b=0.08),
            k(r(SLAM9 + 0.75), look='camera', lookDur=0.15)])],
        props=[KEPI('kepi9', 'officier'),
               *[P(f'annuaire9{i}', 'slab', pos=[0.0, r(BOOKS9[1] + 0.0275 + 0.055 * i), -1.45], ry=(i % 3 - 1) * 6, opts={'w': 0.34, 'h': 0.05, 'd': 0.26, 'color': '#E8C43A' if i % 2 == 0 else '#F2EEE0'}) for i in range(NB9)],
               P('chipolata9', 'sausage', pos=CHIP9, opts={'len': 0.5, 'r': 0.062, 'color': '#C46A44', 'hop': [[r(SLAM9 + 0.02), 0.32, 0.62, 0.36]], 'face': {'ry': -0.75, 'look': -0.35, 'y': 0.72}}),   # (final) eyes and pressed lips, turned away from him
               P('cache9', 'slab', pos=[1.8, 2.5, -3.14], opts={'w': 0.64, 'h': 0.64, 'd': 0.02, 'color': '#5A6066'}),   # (final) hides the wall clock (behind his head it read as a big ear)
               P('contre9', 'flickerLight', pos=[1.55, 2.55, -1.95], opts={'color': '#FFD9A8', 'intensity': 6, 'distance': 3.4, 'rate': 0.12}),   # (final) a rim light on his shoulders and arms
               P('cone9', 'lightCone', pos=[0, 0, 0], opts={'from': [0.0, 2.06, -0.75], 'to': [0.0, TOPB9, -1.45], 'r': 0.42, 'opacity': 0.14})],
        fx=[{'type': 'shake', 'at': SLAM9, 'dur': 0.15, 'amount': 0.012}],
        dark=[[0.0, 0.62, 0.001]], darkFloor=0.42, darkTint='#2E333C', darkPool={'at': [0.2, 1.25, -1.2], 'r': 1.25, 'k': 1.0, 'tint': '#FFE9C0'},
        cams=[cam(0.0, [-0.42, 1.52, 2.75], [-0.38, 1.51, 2.58], [0.42, 1.42, -1.0], [0.42, 1.41, -1.0], lens=42)])
st.cue('thud', 'S09', SLAM9, 0.6); st.cue('sfx:tick', 'S09', 1.5, 0.12)

# 10: it was swapped for a spy. A long bridge in the fog, seen three-quarter from the right side: two soldiers carry the chipolata away from us
#     on a stretcher, holding its handles; it sits up on it under a white blanket; out of a veil of fog ahead a spy in a trench coat, hat and dark
#     glasses walks toward us on the other side; as they cross, his head turns and his glance lands on it, and stays on it
#     (round 1: the chipolata sits up, bigger, and stays in view between the bearers; the bearers hold the handles; the spy walks out of a fog veil)
D10 = st.dur('S10'); BY = 6.0
SZ0, SV = -3.2, 1.4                                         # the stretcher's middle: z at t 0, speed toward -Z
STZ = lambda t: r(SZ0 - SV * t)
SPZ0, SPV = -7.95, 2.0                                       # the spy: z at t 0 (just behind the first veil), speed toward +Z
#     (round 2: a bigger chipolata sitting up with its body showing above a blanket that hugs only its lower third; the bearers on the right lane,
#     the spy on the far left lane, 2.3 m apart; a camera high behind the bearers' lane, so the spy's head stays clear of the helmets)
SX10, SPX10 = 0.9, -1.4                                      # the stretcher's lane and the spy's lane
P1A, P1B = [SX10, BY, r(SZ0 - 1.25)], [SX10, BY, r(STZ(D10) - 1.25)]
NX10 = 0.6                                                   # (final) the near bearer walks a little to the left, so the chipolata shows between the two
P2A, P2B = [NX10, BY, r(SZ0 + 1.25)], [NX10, BY, r(STZ(D10) + 1.25)]
SPYA, SPYB = [SPX10, BY, SPZ0], [SPX10, BY, r(SPZ0 + SPV * D10)]
STR_A, STR_B = [SX10, r(BY + 0.82), STZ(0)], [SX10, r(BY + 0.82), STZ(D10)]
WALK = lambda a, b: [k(0.0, to=b, dur=D10, clip='walk', ease='linear')]
def CARRY(end):
    """the bearer's two hands on the handles at one end of the stretcher (end -1: the front, +1: the back), keyed along the walk"""
    ks = []
    for i in range(int(D10 / 0.2) + 2):
        t = r(min(D10, i * 0.2)); z = r(STZ(t) + end * 0.95)
        ks.append(k(t, toon={'reach': {'R': [r(SX10 + 0.275), r(BY + 0.84), z, 1, 0.03], 'L': [r(SX10 - 0.275), r(BY + 0.84), z, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.2 if i else 0.0, toonEase='linear'))
    return ks
CROSS10 = 0.95
st.shot('S10', 'grassland', setOpts={'clouds': 0, 'sky': ['#AEB8C0', '#D6DBDF'], 'grass': '#55616A'}, fog={'color': '#CDD3D8', 'near': 8, 'far': 22}, actors=[   # (final) clear in front, thick behind
        act('porteur1', P1A, 180, 'walk', 'neutral', keys=WALK(P1A, P1B) + CARRY(-1)), act('porteur2', P2A, 180, 'walk', 'neutral', keys=WALK(P2A, P2B) + CARRY(1)),
        act('espion', SPYA, 0, 'walk', 'unimpressed', keys=[*WALK(SPYA, SPYB), k(0.0, look=[SPX10, r(BY + 1.6), 2.0]),
            k(CROSS10, look=[SX10, r(BY + 1.15), STZ(1.25)], lookDur=0.15), k(1.25, look=[SX10, r(BY + 1.15), STZ(1.6)], lookDur=0.35), k(1.7, look=[SX10, r(BY + 1.15), STZ(1.9)], lookDur=0.2)])],
        props=[P('pont10', 'fogBridge', pos=[0.0, BY, -14.0], ry=90, opts={'L': 44, 'W': 4.2, 'veils': [-6.1, -3.6, 1.5], 'veilAs': [0.55, 0.9, 0.97]}),   # (final) thin veil near, thick ones behind
               P('civiere10', 'stretcher', pos=STR_A, opts={'load': 'sit2', 'len': 0.64, 'r': 0.088}, keys=[k(0.0, to=STR_B, dur=D10, ease='linear')]),
               HELMET('casque10a', 'porteur1'), HELMET('casque10b', 'porteur2'),
               P('chapeau10', 'fedoraHat', on={'actor': 'espion', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'color': '#5A4A36'}),
               P('lunettes10', 'shades', on={'actor': 'espion', 'joint': 'head', 'offset': [0.0, 0.3, 0.095]}, opts={'ear': False})],
        cams=[cam(0.0, [2.7, r(BY + 3.4), 1.2], [2.65, r(BY + 3.35), 0.9], [0.1, r(BY + 0.9), -4.6], [0.0, r(BY + 0.9), -5.6], lens=44)])
st.cue('sfx:stepSoft', 'S10', 0.1, 0.2); st.cue('sfx:wind', 'S10', 0.0, 0.25)

# 11: the army put the barbecue out with a flamethrower. Three-quarter from the front, wide: on the left, behind his own fence, a soldier in a gas
#     mask, tanks on his back, crouches for two frames and fires: a long, narrow jet of flame stretches from the nozzle across the frame onto the
#     little grill on the right and splashes round it; the paratrooper still sits on it, still saluting; knees and tanks shake with the recoil;
#     the red grill darkens to black under the flame; the jet cuts and the grill is a smoking black lump, the paratrooper sooted, still saluting
#     (round 1: a side view of the jet, lance in profile; the grill is in the frame and visibly blackens; the flame stops before the cut)
D11 = st.dur('S11'); FIRE11 = 0.5; CHAR11 = 0.75; CHARD11 = 0.6; STOP11 = 1.6
G11 = [1.95, 0, -1.8]                                        # the grill in shots 11 to 13 (the neighbour's patio)
SOL11 = [-0.6, 0, -1.2]; RY11 = yaw(SOL11, G11)              # (final) further from the grill: a longer jet
PARA11 = [G11[0], 0.39, G11[2]]; PRY11 = 10
CAM11 = [2.0, 1.2, 6.0]                                      # (final) lower and re-aimed: the grill at 55-65 % of the height, his tanks in the frame
GRIP11 = off(SOL11, RY11, 0.3, 0.15, 0.95)
TGT11 = [r(G11[0] - 0.08), 0.72, G11[2]]
Z11 = unit3([TGT11[i] - GRIP11[i] for i in range(3)]); X11 = unit3(cross3([0, 1, 0], Z11)); Y11 = cross3(Z11, X11)
LRX11, LRY11, LRZ11 = axes_euler(X11, Y11, Z11)
JET11 = r(math.dist(GRIP11, TGT11) - 1.05 + 0.05)
FRONT11 = [r(GRIP11[i] + Z11[i] * 0.48) for i in range(3)]
HOLD11 = {'reach': {'R': [*GRIP11, 1, 0.03], 'L': [*FRONT11, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}}
SALP = lambda p, ry: [*off([p[0], 0, p[2]], ry, 0.06, 0.2, p[1] + 1.6), 1, 0.03]
def SALUTE2(p, ry, t, sq=(1, 1, 1), dur=0.1, face=None):
    return k(t, toon={'reach': {'R': SALP(p, ry), 'L': [*off([p[0], 0, p[2]], ry, 0.25, -0.22, p[1] + 0.55), 1, 0.04]}, 'hands': {'R': 'open', 'L': 'rest'},
                      'sq': list(sq), 'face': face or {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=dur, toonEase='out')
PARA_AT = lambda p, ry, extra=(): act('para', p, ry, 'sit', 'neutral', keys=[k(0.0, look='camera'), SALUTE2(p, ry, 0.0, dur=0.0), *extra])
def WISPS(g, ry, pid, at=None, col='#6E6964'):
    """(final) soft wisps of smoke rising from his trousers (beside his hips, a little behind him) and from the top of his helmet: soft sprites, not dark
    balls on his chest (the grills under him have no smoke of their own any more)"""
    out = [P(f'{pid}{j}', 'softWisp', pos=off([g[0], 0, g[2]], ry, -0.1, sd * 0.26, 0.66), opts={'at': at or 0.0, 'n': 12, 'life': 1.5, 'rise': 1.5, 's0': 0.06, 's1': 0.3, 'drift': [sd * 0.18, -0.12], 'color': col, 'opacity': 0.7})
           for j, sd in enumerate((-1, 1))]
    out.append(P(f'{pid}c', 'softWisp', pos=off([g[0], 0, g[2]], ry, -0.02, 0.0, 2.25), opts={'at': at or 0.0, 'n': 10, 'life': 1.4, 'rise': 1.1, 's0': 0.05, 's1': 0.24, 'drift': [0.1, -0.1], 'color': col, 'opacity': 0.65}))
    return out
REC11 = [k(r(FIRE11 + 0.07 * j), toon={**HOLD11, 'sq': [1.03, 0.96, 1.03] if j % 2 else [0.99, 1.01, 0.99], 'bend': {'spine': [0.12 if j % 2 else 0.05, 0, 0, 1, None]}}, toonDur=0.035) for j in range(1, 16)]
st.shot('S11', 'grassland', setOpts=GARDEN_SET, actors=[
        act('soldat', SOL11, RY11, 'stand', 'angry', keys=[k(0.0, look=[G11[0], 1.0, G11[2]]), k(0.0, toon={**HOLD11, 'sq': [1, 1, 1]}, toonDur=0.0),
            k(r(FIRE11 - 0.13), toon={**HOLD11, 'sq': [1.07, 0.9, 1.07], 'bend': {'spine': [0.22, 0, 0, 1, None]}}, toonDur=0.07), k(r(FIRE11 - 0.13), to=[SOL11[0], -0.1, SOL11[2]], dur=0.07),
            k(FIRE11, toon={**HOLD11, 'sq': [0.95, 1.05, 0.95], 'bend': {'spine': [-0.12, 0, 0, 1, None]}}, toonDur=0.04, toonEase='out'),
            *REC11, k(STOP11, toon={**HOLD11, 'sq': [1, 1, 1], 'bend': {'spine': [0.04, 0, 0, 1, None]}}, toonDur=0.2), k(STOP11, to=[SOL11[0], 0, SOL11[2]], dur=0.2),
            k(r(STOP11 + 0.3), look='camera', lookDur=0.2)]),
        PARA_AT(PARA11, PRY11, extra=[k(0.6, look=[SOL11[0], 1.6, SOL11[2]], lookDur=0.12), k(r(CHAR11 + CHARD11), toon={'reach': {'R': SALP(PARA11, PRY11)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'pop': 0.25, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.05, keepPose=True),
                                      k(r(STOP11 + 0.1), look='camera', lookDur=0.1), k(r(STOP11 + 0.35), toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06, keepPose=True), k(r(STOP11 + 0.45), toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.06, keepPose=True)])],
        props=[*[p_ for p_ in GARDEN('party', grill=False) if p_['id'] not in ('assiette0', 'assiette1', 'assiette2')], MASK('masque11', 'soldat'), HELMET('casque11', 'soldat'), HELMET('casque11p', 'para'), SOOT('suie11', 'para', r(CHAR11 + CHARD11)),
               P('reservoirs11', 'fuelTanks', on={'actor': 'soldat', 'joint': 'torso', 'offset': [0.0, 0.3, -0.2]}),
               P('lance11', 'flameThrower', pos=GRIP11, ry=LRY11, rot=[LRX11, 0.0, LRZ11], opts={'fire': [[FIRE11, STOP11]], 'jet': JET11, 'spread': 0.1, 'taper': True, 'splash': 0.26},
                 keys=[k(r(FIRE11 + 0.07 * j), to=add(GRIP11, [0, 0.012 if j % 2 else -0.008, 0]), dur=0.035) for j in range(1, 16)] + [k(STOP11, to=GRIP11, dur=0.1)]),
               P('gril', 'kettleGrill', pos=G11, opts={'charAt': CHAR11, 'charDur': CHARD11, 'smoke': False}),   # (final) no smoke of its own: its puffs sat on his chest
               *WISPS(G11, PRY11, 'fumee11', at=r(STOP11 + 0.02))],
        fx=[{'type': 'shake', 'at': FIRE11, 'dur': r(STOP11 - FIRE11), 'amount': 0.006}],
        cams=[cam(0.0, CAM11, [1.96, 1.2, 5.85], [0.6, 1.1, -1.6], [0.6, 1.11, -1.6], lens=46)])
st.cue('sfx:roar', 'S11', FIRE11, 0.55); st.cue('whoosh', 'S11', r(FIRE11 - 0.05), 0.35); st.cue('sfx:poof', 'S11', STOP11, 0.3)

# 12: the neighbourhood caught fire. Low behind the grill: in the foreground the charred black grill with the paratrooper still sitting on it,
#     still saluting, sooted; behind him the whole neighbourhood burns, black smoke columns; the soldier stands in the middle distance with his
#     lance lowered (ÉTEINT, over a picture that says the opposite)
#     (round 1: the grill and the paratrooper in the foreground)
D12 = st.dur('S12')
SOL12 = [-0.2, 0, -5.2]                                      # (final) in a gap on the left, against the fire, not behind him
st.card('S12', 'ÉTEINT', at=0.35)
st.shot('S12', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#A88C78', '#E2BC94']}, actors=[
        act('soldat', SOL12, yaw(SOL12, [3.9, 0, 2.4]), 'stand', 'neutral', keys=[k(0.0, look=[6.8, 3.0, -9.5]), k(0.5, look=[-3.0, 3.0, -8.0], lookDur=0.35), k(1.0, look='camera', lookDur=0.2)]),
        PARA_AT(PARA11, PRY11 + 15, extra=[k(0.9, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06, keepPose=True), k(1.0, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.06, keepPose=True)])],
        props=[*GARDEN('fire', grill=False), P('gril12', 'kettleGrill', pos=G11, opts={'char': True, 'smoke': False}), MASK('masque12', 'soldat'), HELMET('casque12', 'soldat'), HELMET('casque12p', 'para'), SOOT('suie12', 'para'),
               P('reservoirs12', 'fuelTanks', on={'actor': 'soldat', 'joint': 'torso', 'offset': [0.0, 0.3, -0.2]}),
               P('lance12', 'flameThrower', on={'actor': 'soldat', 'hand': 'R', 'offset': [0.0, -0.05, 0.02], 'rot': [1.2, 0.0, 0.0]}, opts={'fire': []}),
               *WISPS(G11, PRY11 + 15, 'fumee12', col='#5E5A56')],
        cams=[cam(0.0, [2.4, 1.2, 0.9], [2.37, 1.2, 0.8], [1.0, 1.45, -4.5], [1.0, 1.46, -4.5], lens=50)])   # (final) closer: the grill and him fill the lower half, cut at the knees
st.cue('thunder', 'S12', 0.05, 0.35); st.cue('sfx:roar', 'S12', 0.1, 0.25)

# 13: the paratrooper did not move. Close on him, still sitting on the charred grill, still saluting, his face sooty in grey patches, smoke rising
#     from his trousers and his helmet; the houses burn behind him; one slow blink
D13 = st.dur('S13')
st.shot('S13', 'grassland', setOpts={**GARDEN_SET, 'sky': ['#A88C78', '#E2BC94']}, actors=[PARA_AT(PARA11, PRY11, extra=[k(1.12, toon={'face': {'lid': 1.0, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.18, keepPose=True), k(1.5, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.18, keepPose=True)])],   # (final) one slow full blink
        props=[*GARDEN('fire', grill=False), P('gril13', 'kettleGrill', pos=G11, opts={'char': True, 'smoke': False}), HELMET('casque13', 'para'), SOOT('suie13', 'para'),
               *WISPS(G11, PRY11, 'fumee13')],
        cams=[cam(0.0, [r(G11[0] - 0.5), 1.72, r(G11[2] + 3.2)], [r(G11[0] - 0.47), 1.72, r(G11[2] + 3.0)], [r(G11[0] - 0.02), 1.6, G11[2]], [r(G11[0] - 0.02), 1.6, G11[2]], lens=44)])
st.cue('sfx:roar', 'S13', 0.0, 0.2); st.cue('sfx:tick', 'S13', 0.9, 0.1)

# 14: to reassure everyone, the minister ate a sausage. The press room: at the podium the minister holds up a sausage on a fork for the cameras,
#     smiles, then bites into it under a storm of flashes; his cheeks fill
#     (round 2: he holds it up for the cameras, leans back with his mouth wide open, the fork swings up in an arc to his mouth, his head pushes
#     forward into the bite and his cheeks inflate with an overshoot; three full-frame flashes on the bite, a third of a second apart; the press in
#     silhouette along the bottom edge; a lighter grey-blue backdrop so his navy suit stands out, and no flags)
D14 = st.dur('S14'); BITE14 = 1.5
MIN = [0.0, 0, -2.45]
PRESS = {'backdrop': 'SANTÉ', 'chairs': False, 'flags': False, 'fg': 'rgba(255,255,255,0.1)', 'fontScale': 0.6,   # (final) one short word, smaller: whole words, none cut behind his head
         'wall': '#8A9CB0', 'bg': '#93A5B9', 'band': '#71839A', 'trim': '#5C6E84'}   # (round 2) a lighter grey-blue: the navy suit reads against it
MOUTH = [0.0, 1.8, -2.32]
FK = lambda t, p, d=0.25, face=None, sq=(1, 1, 1), b=0.0: k(t, toon={'reach': {'R': [*p, 1, 0.03], 'L': [0.22, 1.17, -2.1, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': list(sq),
                                                                  'bend': {'spine': [b, 0, 0, 1, None]}, 'face': face or {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}}, toonDur=d, toonEase='inOut')
FLASH14 = [r(BITE14 + 0.02), r(BITE14 + 0.36), r(BITE14 + 0.7)]
st.shot('S14', 'pressRoom', setOpts=PRESS, actors=[
        act('ministre', MIN, 0, 'stand', 'happy', keys=[k(0.0, look='camera'), FK(0.0, [-0.26, 1.4, -2.1], 0.0), FK(0.2, [-0.34, 1.86, -2.06], 0.3, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}),   # (his mouth is near 2.2 m: the box head)
            FK(0.85, [-0.36, 1.8, -2.08], 0.2, {'lid': 0.25, 'mouth': 'smile', 'brow': 0.4}),
            FK(1.12, [-0.32, 1.42, -2.12], 0.18, {'lid': 0.1, 'mouth': 'scream', 'brow': 0.6}, (0.97, 1.05, 0.97), -0.16),            # leans back, mouth wide open, the fork drawn down
            FK(1.32, [-0.24, 1.98, -1.95], 0.1, {'lid': 0.1, 'mouth': 'scream', 'brow': 0.6}, (0.97, 1.04, 0.97), -0.1),               # the arc: up and out...
            FK(r(BITE14 - 0.04), [0.25, 1.67, -2.1], 0.08, {'lid': 0.2, 'mouth': 'scream', 'brow': 0.5}, (1.0, 1.0, 1.0), 0.12),        # ...in to the mouth
            FK(BITE14, [0.25, 1.67, -2.1], 0.04, {'lid': 0.5, 'mouth': 'clench', 'brow': 0.1, 'cheeks': 0.8}, (1.06, 0.94, 1.06), 0.2),   # the bite: head forward
            FK(r(BITE14 + 0.2), [-0.24, 1.55, -2.1], 0.25, {'lid': 0.35, 'mouth': 'line', 'brow': 0.3, 'cheeks': 0.9}, (0.98, 1.02, 0.98), 0.02),
            k(r(BITE14 + 0.45), toon={'face': {'lid': 0.4, 'mouth': 'O', 'cheeks': 0.9}}, toonDur=0.08, keepPose=True), k(r(BITE14 + 0.6), toon={'face': {'lid': 0.3, 'mouth': 'line', 'cheeks': 0.9}}, toonDur=0.08, keepPose=True),
            k(r(BITE14 + 0.75), toon={'face': {'lid': 0.4, 'mouth': 'O', 'cheeks': 0.9}}, toonDur=0.08, keepPose=True)])],
        props=[FORK('fourchette14', 'ministre', len=0.22, r=0.036, bite=[BITE14, 0.45]),
               P('joueG14', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [0.1, 0.17, 0.1]}, opts={'growAt': BITE14, 'dur': 0.3, 'r': 0.062}),
               P('joueD14', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [-0.1, 0.17, 0.1]}, opts={'growAt': BITE14, 'dur': 0.3, 'r': 0.062}),
               P('presse14', 'pressCrowd', pos=[0, 0, 0], opts={'heads': [[-0.3, 1.02, -1.65], [-0.06, 0.98, -1.6], [0.2, 1.04, -1.68], [0.44, 1.0, -1.62]], 'camsAt': [[-0.18, 1.32, -1.66, 0.55], [0.32, 1.36, -1.68, -0.55]], 'y': 1.0, 'color': '#232833',
                                                               'flash': [[FLASH14[0], 0], [FLASH14[1], 1], [FLASH14[2], 0], [0.3, 1], [0.95, 0]]})],   # (final) three heads and two raised cameras in silhouette along the bottom
        fx=[{'type': 'flash', 'at': ft, 'dur': 0.1} for ft in FLASH14],
        cams=[cam(0.0, [0.3, 1.72, 0.55], [0.28, 1.72, 0.35], [0.0, 1.62, -2.4], [0.0, 1.62, -2.4], lens=40)])
st.cue('sfx:shutter', 'S14', 0.2, 0.3); st.cue('sfx:shutter', 'S14', 0.8, 0.3); st.cue('sfx:crunch', 'S14', BITE14, 0.25)

# 15: he was put in quarantine. Same podium, a little wider: mid-chew, cheeks full, the fork at his mouth; a big glass bubble falls into the frame
#     (its shadow growing on the podium and the floor), drops over him and the podium, squashes as it lands and settles (QUARANTAINE); his eyes
#     pop; he glances up at the dome, back at us, then his head snaps up to it again, eyes out on stalks (a double take); the flashes keep going
#     (round 1: the fall lasts four draft frames inside the picture, with a shadow; the double take)
D15 = st.dur('S15'); DROP15 = 0.35; FALL15 = 0.28
FK15 = {'reach': {'R': [-0.12, 1.38, -2.18, 1, 0.03], 'L': [0.22, 1.17, -2.1, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'open'}}
st.card('S15', 'QUARANTAINE', at=r(DROP15 + 0.12))
st.shot('S15', 'pressRoom', setOpts=PRESS, actors=[
        act('ministre', MIN, 0, 'stand', 'happy', keys=[k(0.0, look='camera'), FK(0.0, [-0.12, 1.38, -2.18], 0.0, {'lid': 0.35, 'mouth': 'line', 'cheeks': 0.9}),
            FK(DROP15, [-0.12, 1.38, -2.18], 0.04, {'lid': 0.0, 'pop': 0.5, 'mouth': 'clench', 'cheeks': 0.9, 'brow': 0.8}, (0.92, 1.1, 0.92)),
            FK(r(DROP15 + 0.15), [-0.12, 1.38, -2.18], 0.12, {'lid': 0.1, 'pop': 0.2, 'mouth': 'line', 'cheeks': 0.9, 'brow': 0.6}),
            *doubleTake(0.72, [0.0, 2.9, -2.2], keep={**FK15, 'face': {'cheeks': 0.9}}, back='camera', pop=0.7, blank=0.2, hold=0.32)])],
        props=[FORK('fourchette15', 'ministre', len=0.2, r=0.034, bite=[-1.0, 0.45]),
               P('joueG15', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [0.1, 0.17, 0.1]}, opts={'r': 0.055}),
               P('joueD15', 'cheekPuff', on={'actor': 'ministre', 'joint': 'head', 'offset': [-0.1, 0.17, 0.1]}, opts={'r': 0.055}),
               P('bulle15', 'glassBell', pos=[0.0, 3.3, -2.15], opts={'r': 0.78, 'wall': 1.62, 'base': 0.2, 'rim': 0.78, 'tint': '#BFE6F2'},   # (final) a fresnel rim along its whole outline, one curved highlight
                 keys=[k(r(DROP15 - FALL15), to=[0.0, 0.0, -2.15], dur=FALL15, ease='in'), k(DROP15, squash=[1.12, 0.84, 1.12], dur=0.35)]),
               P('ombre15', 'dropShadow', pos=[0.0, 0.0, -2.15], opts={'win': [r(DROP15 - FALL15), DROP15], 'rx': 0.85, 'rz': 0.75, 'opacity': 0.4}),
               P('anneau15', 'dropShadow', pos=[0.0, 0.0, -2.15], opts={'win': [r(DROP15 - 0.04), DROP15], 'rx': 0.84, 'rz': 0.84, 'ring': 0.86, 'from': 1.0, 'opacity': 0.55, 'y': 0.014}),   # (final) its contact ring on the floor
               P('ombre15b', 'dropShadow', pos=[0.0, 1.14, -2.05], opts={'win': [r(DROP15 - FALL15), DROP15], 'rx': 0.35, 'rz': 0.25, 'opacity': 0.35, 'y': 0.0}),
               P('flashs15', 'flashBursts', pos=[0.0, 2.05, -1.6], opts={'n': 8, 'w': 2.3, 'h': 0.9, 'from': 0.05, 'rate': 5, 'life': 0.14})],   # (round 2) above the caption band, round his head
        fx=[{'type': 'shake', 'at': DROP15, 'dur': 0.15, 'amount': 0.01}],
        cams=[cam(0.0, [0.3, 1.5, 1.75], [0.28, 1.5, 1.6], [0.0, 1.42, -2.15], [0.0, 1.42, -2.15], lens=44)])   # (final) pushed in: him and the bell fill the frame, its top just under the card
st.cue('whoosh', 'S15', r(DROP15 - 0.25), 0.3); st.cue('clang', 'S15', DROP15, 0.45); st.cue('sfx:shutter', 'S15', 0.5, 0.3); st.cue('sfx:boing', 'S15', 1.08, 0.2)

# 16: the president decreed a national barbecue. On the ruins of the neighbourhood (soot-black shells, charred roof timbers, ash on a scorched
#     lawn): the president dips his fork, then whips a sausage up over his head like a toast (a smear on the swing) before a giant smoking grill;
#     two soldiers of the band play, invented flags wave, four neighbours jump and pump their arms
#     (round 1: burnt shells instead of pastel houses; the crowd in the frame and alive; a smear on the toast)
D16 = st.dur('S16'); TOAST16 = 0.42
PRES16 = [1.35, 0, -2.2]; RY16 = yaw(PRES16, [1.3, 0, 3.4])
BIG16 = [2.3, 0, -4.9]
#     (round 2: the crowd spread to the edges so gaps open onto the burnt shells behind; a band soldier with his drum in the left gap; a bigger
#     sausage on the toast; flags with the invented fork-and-sausage emblem on a pale field, no bands)
CHEER = [('invite1', [-0.05, 0, -0.95]), ('invite3', [2.85, 0, -1.15]), ('foule2', [0.35, 0, -4.6]), ('foule3', [3.25, 0, -4.7])]
TH = lambda h, f=0.25, sd=0.3: [*off(PRES16, RY16, f, sd, h), 1, 0.03]
def CHEERK(p, j):
    ry = yaw(p, PRES16); ks = [k(0.0, look=add(PRES16, [0, 2.2, 0]))]
    for i in range(6):
        t = r(0.08 + 0.42 * i + 0.1 * j)
        if t > D16 - 0.2: break
        ks += [k(t, to=[p[0], 0.17, p[2]], dur=0.13, ease='out'), k(r(t + 0.15), to=[p[0], 0, p[2]], dur=0.12, ease='in'),
               k(t, toon={'reach': {'R': [*off(p, ry, 0.12, 0.28, 2.55), 1, 0.04], 'L': [*off(p, ry, 0.12, -0.28, 2.5), 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'O', 'brow': 0.6}}, toonDur=0.1, toonEase='out'),
               k(r(t + 0.24), toon={'reach': {'R': [*off(p, ry, 0.2, 0.3, 1.95), 1, 0.04], 'L': [*off(p, ry, 0.2, -0.3, 1.9), 1, 0.04]}, 'hands': {'R': 'fist', 'L': 'fist'}, 'face': {'mouth': 'smile', 'brow': 0.4}}, toonDur=0.12)]
    return ks
st.shot('S16', 'grassland', setOpts=BURNT_SET, actors=[
        act('president', PRES16, RY16, 'stand', 'happy', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': TH(1.2, 0.3, 0.22)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.0),
            k(0.24, toon={'reach': {'R': TH(0.98, 0.32, 0.24)}, 'hands': {'R': 'grip'}, 'sq': [1.05, 0.94, 1.05], 'face': {'lid': 0.4, 'mouth': 'smile', 'brow': 0.1}}, toonDur=0.12),
            k(TOAST16, toon={'reach': {'R': TH(2.55, 0.28, 0.3)}, 'hands': {'R': 'grip'}, 'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.05, 'mouth': 'smile', 'brow': 0.7}}, toonDur=0.07, toonEase='out'),
            k(r(TOAST16 + 0.12), toon={'reach': {'R': TH(2.35)}, 'hands': {'R': 'grip'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.15, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.1),
            k(r(TOAST16 + 0.3), toon={'reach': {'R': TH(2.32)}, 'hands': {'R': 'grip'}, 'sq': [1, 1, 1], 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15),
            k(1.5, toon={'reach': {'R': TH(2.42)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15),
            k(1.7, toon={'reach': {'R': TH(2.3)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15),
            k(2.1, toon={'reach': {'R': TH(2.4)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.25, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15)]),
        act('musi1', [3.6, 0, -6.2], yaw([3.6, 0, -6.2], [1.3, 0, 3.4]), 'stand', 'neutral', keys=[k(r(0.2 + 0.5 * j), look=[1.3, 1.9 + 0.12 * (j % 2), 3.4], lookDur=0.12) for j in range(5)]),
        act('musi2', [0.42, 0, -2.75], yaw([0.42, 0, -2.75], [1.3, 0, 3.4]), 'stand', 'neutral', keys=[k(r(0.2 + 0.25 * j), look=[1.3, 1.5 + 0.15 * (j % 2), 3.4], lookDur=0.1) for j in range(10)]),
        *[act(who, p, yaw(p, PRES16), 'stand', 'happy', keys=CHEERK(p, j)) for j, (who, p) in enumerate(CHEER)]],
        props=[*GARDEN('burnt', grill=False),
               P('gril16', 'kettleGrill', pos=BIG16, scale=3.4, opts={'smokeH': 2.2, 'smokeN': 18, 'smokeSize': 1.2, 'wind': [-0.2, 0.0], 'lit': True}),   # (final) its bowl, rim and bars glow warm
               FORK('fourchette16', 'president', len=0.3, r=0.05), HELMET('casque16a', 'musi1'), HELMET('casque16b', 'musi2'),
               P('trainee16', 'smearArc', pos=[0, 0, 0], opts={'pts': [off(PRES16, RY16, 0.32, 0.24, 1.0), off(PRES16, RY16, 0.5, 0.3, 1.8), off(PRES16, RY16, 0.28, 0.3, 2.55)], 'win': [r(TOAST16 - 0.1), r(TOAST16 + 0.05)], 'r': 0.06, 'color': '#3A3E48', 'opacity': 0.5}),
               P('trompette16', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11], 'rot': [-0.3, -0.85, 0.0]}, opts={'kind': 'trumpet', 'beat': [0.2, 0.7, 1.2, 1.7, 2.2], 's': 1.15}),
               P('tambour16', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': [0.2, 0.45, 0.7, 0.95, 1.2, 1.45, 1.7, 1.95, 2.2]}),
               *[P(f'drapeau16{j}', 'bbqFlag', pos=p_, ry=a_, opts={'phase': j * 1.3}) for j, (p_, a_) in enumerate([([-0.75, 0, -3.6], 8), ([3.75, 0, -3.4], 172), ([2.2, 0, -7.2], -4)])]],
        cams=[cam(0.0, [1.3, 1.05, 3.4], [1.3, 1.08, 3.2], [1.6, 2.15, -3.0], [1.6, 2.2, -3.0], lens=54)])
st.cue('sfx:fanfare', 'S16', 0.1, 0.45); st.cue('whoosh', 'S16', r(TOAST16 - 0.08), 0.25)

# 17: on the embers of the neighbourhood. Low over a bed of glowing embers: neighbours and a soldier kneel round it roasting sausages on long
#     sticks angled into the coals; behind it, in the middle, the paratrooper still sits saluting on the black grill; standing beside him, the
#     yellow neighbour pushes her sausage on its stick toward his face
#     (round 1: the roasters crouch round the embers, sticks into the coals; the far, bright part of the bed sits above the caption band and its
#     near part is dark ash; no cone flames; the offered sausage points at him)
#     (round 2: a lower camera; the roasters kneel round the bed and turn their sticks, with small weight shifts, finger-length sausages turning;
#     the embers light them from below; the yellow neighbour stands on the right, fully in the frame and three-quarter to us, and pushes her sausage
#     at the paratrooper, whose eyes slide to it while his head stays still; the kneeling madame (whose bare leg read as a pipe) is replaced by the
#     man in the suit)
D17 = st.dur('S17')
G17 = [1.3, 0, -2.0]; PARA17 = [G17[0], 0.39, G17[2]]
BED17 = [1.3, 0.0, 0.55]                                     # (final) a wide bed from the camera's feet to the roasters (z 2.45 to -1.35), off both edges
def STICK(pid, hand, tip, keys=None, turn=0.0):
    """a roasting stick from the hand to the tip: its long axis (+Y) aimed with axes_euler (a yaw and a pitch about X only tilt it in the YZ plane)"""
    Y = unit3([tip[i] - hand[i] for i in range(3)]); X = unit3(cross3(Y, [0, 0, 1] if abs(Y[2]) < 0.9 else [1, 0, 0])); Z = cross3(X, Y)
    rx, ry_, rz = axes_euler(X, Y, Z)
    return P(pid, 'sausageStick', pos=hand, ry=ry_, rot=[rx, 0.0, rz], opts={'L': r(math.dist(hand, tip)), 'len': 0.38, 'r': 0.06, 'stickR': 0.014, 'turn': turn}, keys=keys or [])   # (final) bigger sausages on the tips
ROAST = [('foule3', [0.42, 0, -1.6], 32, [0.8, 0.3, -0.85]), ('foule2', [2.22, 0, -1.62], -34, [1.85, 0.3, -0.88]), ('soldat', [-0.15, 0, -2.3], 24, [0.25, 0.3, -1.25])]   # (final) kneeling at the far edge, three-quarter to us
ST17 = []; ACT17 = []
for j, (who, p, ry, tip) in enumerate(ROAST):
    hand = off(p, ry, 0.38, 0.18, 0.62)
    ST17.append(STICK(f'baton17{j}', hand, tip, turn=(2.2 if j % 2 else -2.6)))
    ACT17.append(act(who, p, ry, 'kneel', 'happy' if who != 'soldat' else 'neutral', keys=[k(0.0, look=tip), k(0.0, toon={'reach': {'R': [*hand, 1, 0.03]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
                     *[k(r(0.25 + 0.38 * i + 0.11 * j), toon={'reach': {'R': [*add(hand, [0, 0.03 if i % 2 == 0 else 0.0, 0]), 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.02, 0.98, 1.02] if i % 2 == 0 else [0.99, 1.01, 0.99],
                                                              'bend': {'spine': [0.08 if i % 2 == 0 else 0.02, 0, 0, 1, None]}}, toonDur=0.25) for i in range(4)]]))
Y17 = [2.55, 0, -2.75]; YRY17 = yaw(Y17, [1.3, 0, -1.6])                     # (final) behind him on the right, turned to him: her face three-quarter to us
YHAND17 = off(Y17, YRY17, 0.3, 0.22, 1.42); YTIP17 = [r(G17[0] + 0.18), 1.92, r(G17[2] + 0.3)]
st.shot('S17', 'grassland', setOpts=BURNT_SET, actors=[*ACT17,
        act('invite2', Y17, YRY17, 'stand', 'happy', keys=[k(0.0, look=[1.25, 2.0, -1.2]), k(0.0, toon={'reach': {'R': [*YHAND17, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'smile', 'brow': 0.4}}, toonDur=0.0),
            k(0.4, toon={'reach': {'R': [*add(YHAND17, [-0.12, 0.03, 0.0]), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'bigsmile', 'brow': 0.6}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'sq': [0.98, 1.02, 0.98]}, toonDur=0.2),
            k(0.9, toon={'reach': {'R': [*add(YHAND17, [-0.2, 0.05, 0.02]), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'bigsmile', 'brow': 0.7}, 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'sq': [0.97, 1.03, 0.97]}, toonDur=0.2)]),
        PARA_AT(PARA17, -3, extra=[k(0.55, toon={'reach': {'R': SALP(PARA17, -3)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2, 'gx': 0.85, 'gy': 0.15}}, toonDur=0.25, keepPose=True),   # his eyes slide to the sausage
                                  k(1.15, toon={'reach': {'R': SALP(PARA17, -3)}, 'hands': {'R': 'open'}, 'face': {'lid': 1.0, 'mouth': 'line', 'gx': 0.85, 'gy': 0.15}}, toonDur=0.06, keepPose=True),
                                  k(1.25, toon={'reach': {'R': SALP(PARA17, -3)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.2, 'gx': 0.85, 'gy': 0.15}}, toonDur=0.06, keepPose=True)])],
        props=[*GARDEN('burnt', grill=False), P('gril', 'kettleGrill', pos=G17, opts={'char': True, 'smoke': False}), *WISPS(G17, -3, 'fumee17'), HELMET('casque17', 'soldat'), HELMET('casque17p', 'para'), SOOT('suie17', 'para'),
               P('braises17', 'emberBed', pos=BED17, opts={'w': 5.2, 'd': 3.8, 'lift': 0.2, 'lumps': 70, 'glowLumps': 0.35, 'flames': 0, 'sparks': 26, 'nearDark': 0.5, 'nearTint': '70,26,14', 'light': 2.8, 'lightR': 4.5,
                                                           'timbers': [[-1.1, -1.0, 1.7, 0.35], [0.7, -0.6, 1.5, -0.4], [-0.3, 0.5, 1.3, 1.25], [1.5, 0.3, 1.2, 0.9], [-0.8, 1.4, 1.0, -0.2]]}), *ST17,   # (final) roof timbers glowing in the coals
               STICK('baton17y', YHAND17, YTIP17, keys=[k(0.4, to=add(YHAND17, [-0.12, 0.03, 0.0]), dur=0.2), k(0.9, to=add(YHAND17, [-0.2, 0.05, 0.02]), dur=0.2)])],
        cams=[cam(0.0, [1.3, 0.95, 3.75], [1.3, 0.95, 3.6], [1.3, 1.05, -1.6], [1.3, 1.06, -1.6], lens=56)])   # (final) low over the coals
st.cue('sfx:roar', 'S17', 0.0, 0.15); st.cue('sfx:tick', 'S17', 0.6, 0.1)

# 18: oh, and he was not invited. Framed exactly like the first shot: he stands alone on his scorched lawn behind the charred stump of his fence, gas
#     mask on, an empty paper plate in his hand; a thread of the national barbecue's smoke drifts into his mask; behind him, apart and in profile,
#     the neighbour and a general raise their glasses high and clink them (a twinkle); he tilts his head down to the plate, holds it, the plate
#     sags, and his head snaps back up to us
#     (round 1: the clink in clear silhouette, arms apart; a held look down at the plate and a snap back; the plate droops)
#     (round 2: the glasses meet above their heads, apart and in profile, with a twinkle; his look down at the plate is held with a visible shoulder
#     sag, then snaps back; the plate flops down with an overshoot)
D18 = st.dur('S18'); CLINK18 = 1.15; DOWN18 = r(st.at('S18', 'L18', 4) - 0.14); UP18 = r(st.at('S18', 'L18', 5) + 0.56)   # (final) the look down held across « pas invité »
NB18, GEN18 = [r(CTR1[0] - 0.62 * PERP1[0]), 0, r(CTR1[2] - 0.62 * PERP1[2] - 0.3)], [r(CTR1[0] + 0.62 * PERP1[0]), 0, r(CTR1[2] + 0.62 * PERP1[2] - 0.3)]
TOAST18 = [CTR1[0], 2.6, r(CTR1[2] - 0.3)]
FILTER18 = off(H1, RY1, 0.24, 0.0, 1.68)
PLATE18 = off(H1, RY1, 0.34, -0.16, 1.02)
BIG18 = [3.4, 0, -8.0]
st.shot('S18', 'grassland', setOpts=BURNT_SET, actors=[
        act('mec', H1, RY1, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': [*off(H1, RY1, 0.32, -0.16, 1.05), 1, 0.04]}, 'hands': {'L': 'open'}, 'face': DEAD}, toonDur=0.0),
            k(DOWN18, look=add(PLATE18, [0, -0.25, 0.1]), lookDur=0.12), k(DOWN18, toon={'reach': {'L': [*off(H1, RY1, 0.32, -0.16, 1.0), 1, 0.04]}, 'hands': {'L': 'open'}, 'face': {'lid': 0.45, 'mouth': 'line'}, 'bend': {'spine': [0.2, 0, 0, 1, None], 'neck': [0.5, 0, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.16),
            k(r(DOWN18 + 0.45), toon={'reach': {'L': [*off(H1, RY1, 0.32, -0.16, 0.96), 1, 0.04]}, 'hands': {'L': 'open'}, 'face': {'lid': 0.55, 'mouth': 'line'}, 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.55, 0, 0, 1, None]}, 'sq': [1.06, 0.93, 1.06]}, toonDur=0.3),   # the shoulders sag
            k(UP18, look='camera', lookDur=0.05),
            k(UP18, toon={'reach': {'L': [*off(H1, RY1, 0.32, -0.16, 1.03), 1, 0.04]}, 'hands': {'L': 'open'}, 'face': DEAD, 'sq': [0.96, 1.05, 0.96], 'bend': {'spine': [-0.04, 0, 0, 1, None], 'neck': [-0.06, 0, 0, 1, None]}}, toonDur=0.04, toonEase='out'),
            k(r(UP18 + 0.12), toon={'reach': {'L': [*off(H1, RY1, 0.32, -0.16, 1.03), 1, 0.04]}, 'hands': {'L': 'open'}, 'face': DEAD, 'sq': [1, 1, 1], 'bend': {'spine': [0.0, 0, 0, 1, None], 'neck': [0.0, 0, 0, 1, None]}}, toonDur=0.12),
            k(2.3, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1, keepPose=True), k(2.45, toon={'face': DEAD}, toonDur=0.1, keepPose=True)]),
        act('voisin', NB18, yaw(NB18, GEN18), 'stand', 'happy', keys=[k(0.0, look=add(GEN18, [0, 1.85, 0])), *CLINK(CLINK18, NB18, TOAST18), *CLINK(2.35, NB18, TOAST18), k(r(CLINK18 + 0.35), clip='laugh')]),
        act('general', GEN18, yaw(GEN18, NB18), 'stand', 'happy', keys=[k(0.0, look=add(NB18, [0, 1.85, 0])), *CLINK(CLINK18, GEN18, TOAST18, hand='L'), *CLINK(2.35, GEN18, TOAST18, hand='L'), k(r(CLINK18 + 0.3), clip='laugh')])],
        props=[*GARDEN('burnt', grill=False), MASK('masque18', 'mec'),
               P('assiette18', 'paperPlate', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.02, 0.13], 'face': 'camera'}, opts={'r': 0.14, 'tiltX': 0.95, 'droop': [r(DOWN18 + 0.35), 0.75], 'floppy': True, 'droopDur': 0.3}),   # (final) in front of the hand: the thumb read as food on it
               P('gril18', 'kettleGrill', pos=BIG18, scale=3.4, opts={'smokeH': 2.0, 'smokeN': 16, 'smokeSize': 1.2, 'wind': [-0.6, 0.3]}),
               P('fumee18', 'smokeTendril', pos=[0, 0, 0], opts={'pts': [add(BIG18, [0, 3.4, 0]), [1.4, 3.3, -2.8], off(H1, RY1, 0.8, -0.2, 1.9), FILTER18], 'at': 0.0, 'grow': 0, 'r0': 0.05, 'r1': 0.014, 'wob': 0.03,
                                                             'color': '#9A958E', 'opacity': 0.8, 'off': [r(D18 - 1.1), 0.5]}),   # (final) a thin thread into the filter, drawn away from his face in the last second (bunched puffs read as a beard)
               GLASS('verre18a', 'voisin'), GLASS('verre18b', 'general', hand='L', color='#E8B84A'), KEPI('kepi18', 'general'),
               P('tinte18', 'twinkle', pos=TOAST18, opts={'at': CLINK18, 's': 0.14}), P('tinte18b', 'twinkle', pos=TOAST18, opts={'at': 2.35, 's': 0.12})],
        cams=[{**C1}])
st.cue('sfx:clink', 'S18', CLINK18, 0.3); st.cue('sfx:clink', 'S18', 2.35, 0.22); st.cue('sfx:sting', 'S18', 2.2, 0.25)

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
