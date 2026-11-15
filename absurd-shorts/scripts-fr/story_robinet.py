#!/usr/bin/env python3
"""Le robinet (story 71, cycle 33; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man forgot to turn off his tap. The water ran down the stairs. Then into the street. The neighbours got out their rubber rings. The firemen
pumped all night. The water rose even faster. The town hall declared the town a seaside resort. The tourists came to sunbathe on the roofs. The
navy sent a submarine. It parked outside the bakery. The scientists added a sea to the maps. The president came by pedalo. He opened a lighthouse.
Three years later, this man pulled the plug. The sea drained into his bathtub. In six seconds. The submarine too. He got his water bill. He is
contesting it.
Staging: he opens the bath tap wide, the phone rings, he walks off whistling; an old lady coming down the stairs with her tea is lifted by the
water and rides it down seated, sipping; the water bursts out of the front door into the street; on the balconies a neighbour blows up a duck
ring, another puts on a diving mask; at night two firemen pump the street and the outflow hose pours it back three metres away; a policeman
directing traffic goes under, his cap floating, his white glove still directing; the mayor on the roof of the half-drowned town hall declares,
a banner unrolls (STATION BALNÉAIRE), a parasol opens; tourists on the roofs, one swan-dives off a chimney; a periscope pops up, looks round,
sees us, ducks and comes back; the submarine surfaces outside the bakery's fifth-floor window, a sailor pops out of the hatch and takes a
baguette from the baker; two scientists paint a new sea on the wall map, shaped like a bathtub; the president pedals a swan pedalo between the
chimneys, his guards swimming in rubber rings; he presses a button, the lighthouse on this man's roof lights up and its beam catches him; three
years later the bathroom is a sea floor (seaweed on the tap, a crab on the rim), he wades in and pulls the plug: PLOP; the whirlpool round his
building swallows the pedalo, the boats, the deckchairs and the submarine; the street drained, fish flopping, the pedalo on a lamp post; the
submarine's tail stuck in his plughole, its periscope turning to him; the postman hands him the bill and it unrolls down the stairs; he stamps it
CONTESTÉ; the tap drips.
Natural look; cycle 33 tools: props_robinet.js (bathTub: fills, overflows, drains, drips, seaweed, barnacles, the submarine's tail; bathPlug,
cascade, whirlpool, submarine with periscope and hatch, seaMap, fishFlop, crab, duckRing, lighthouseLive), the salleDeBain set, billScroll prices."""
from story_kit import *
import math

st = Story('robinet', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L07', 4),
         ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L11', 4), ('S14', 'L12', 0), ('S15', 'L13', 0), ('S16', 'L14', 0),
         ('S17', 'L14', 4), ('S18', 'L15', 0), ('S19', 'L16', 0), ('S20', 'L17', 0), ('S21', 'L18', 0), ('S22', 'L19', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3, ink=None: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True, **({'ink': ink} if ink else {})})
DEAD = {'lid': 0.45}
XLOOK = {'sat': 0.85}
BLINK = lambda t_, base=None: [k(t_, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(r(t_ + 0.11), toon={'face': base or DEAD}, toonDur=0.07)]
FLOOD = lambda pid, y0, y1=None, t0=0.0, t1=0.5, w=30.0, d=60.0, pos=(0.0, 0, 0.0), fl=None, op=0.74: P(pid, 'floodWater', pos=list(pos), opts={'w': w, 'd': d, 'y0': y0, 'y1': y1 if y1 is not None else y0, 't0': t0, 't1': t1, 'opacity': op, 'color': '#3A90CF', **({'floaters': fl} if fl else {})})
# (stills 1) the drowned town at roof level: Haussmann blocks sunk so that their top floor and roof stand out of the water (the skyHigh set laid a
# deck of white clouds under the roofs); BATH: the bathroom's inside, for the cameras (one ended behind a wall: a peach screen)
TOWN = lambda sid, wy, spots: [P(f'blk{sid}{i}', 'haussmann', pos=[x_, r(wy - 16.2 + dh), z_], ry=ry_, opts={'w': 13.0, 'h': 17.0, 'floors': 6, 'cols': 5, 'seed': i + 20}) for i, (x_, z_, ry_, dh) in enumerate(spots)]
BATH = (-3.25, 3.25, 0.3, 2.85, -2.05, 4.8)   # the bathroom widened to a half-width of 3.4 m (at 2.6 the cameras went to 80-degree lenses)

# his bathroom (the salleDeBain set, back wall at z -2.2): the bathtub along the back wall, the taps at +x
TUB = [0.25, 0, -1.65]; TW = 1.9; TD = 0.95
TAPH = [r(TUB[0] + TW / 2 - 0.12), 0.91, r(TUB[2] - 0.16)]            # the hot tap's handle
MOUTH = [r(TUB[0] + TW / 2 - 0.35), 1.06, TUB[2]]                     # the spout
DRAIN = [r(TUB[0] + TW / 2 - 0.42), 0.19, TUB[2]]                     # the plughole
RIMZ = r(TUB[2] + TD / 2)                                             # the front rim
TUBP = lambda pid, **o: P(pid, 'bathTub', pos=TUB, opts={'w': TW, 'd': TD, 'h': 0.6, **o})

for g_ in [('S02', 1.0, 'mamie', 'surf'), ('S04', 1.0, 'voisin1', 'duck'), ('S05', 1.2, 'pompier1', 'loop'), ('S06', 1.0, 'agent', 'glove'), ('S09', 1.6, 'touriste2', 'dive'),
           ('S10', 1.2, None, 'periscope'), ('S11', 1.0, 'marin', 'hatch'), ('S14', 1.0, 'president', 'pedalo'), ('S15', 1.0, 'president', 'beam'), ('S17', 0.6, 'mec', 'plop'),
           ('S18', 1.0, None, 'whirlpool'), ('S20', 0.6, 'mec', 'sub'), ('S21', 0.8, 'facteur', 'scroll'), ('S22', 0.5, 'mec', 'stamp')]:
    st.gag(*g_)
st.card('S08', 'BALNÉAIRE', at=0.2)
st.card('S14', 'PÉDALO', at=0.3)
st.card('S19', 'SIX SECONDES', at=0.15)

# 1: the hook. His bathroom: he turns the hot tap full on, the water gushes into the tub; the phone rings in the next room: he leaves at once,
#    whistling, toward us, without a look back; the tap roars on
D1 = st.dur('S01'); ON1 = 0.3; RING1 = 0.75; GO1 = 0.95
ME1 = [1.75, 0, -1.5]   # at the tap end, three-quarter to the camera
st.shot('S01', 'salleDeBain', setOpts={'half': 3.4}, actors=[act('mec', ME1, -100, 'stand', 'neutral', keys=[k(0.0, look=[TAPH[0], 0.9, TAPH[2]]),
            k(0.0, toon={'reach': {'R': [TAPH[0], 0.95, TAPH[2], 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.0),
            k(0.18, toon={'reach': {'R': [r(TAPH[0] - 0.03), 0.97, r(TAPH[2] + 0.04), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.12, toonEase='out'),   # a full turn of the tap
            k(ON1, look=[MOUTH[0], 0.5, MOUTH[2]]), k(0.55, toon={'face': {'lid': 0.25, 'mouth': 'smile'}}, toonDur=0.12),
            k(RING1, look=[3.0, 1.6, 2.0]), k(r(RING1 + 0.02), toon={'face': {'lid': 0.0, 'brow': 0.5}}, toonDur=0.06),   # the phone: his head snaps round
            k(GO1, to=[2.3, 0, 1.9], dur=r(D1 - GO1 + 0.4), ease='in', clip='walk'), k(r(GO1 + 0.15), look='camera'), k(r(GO1 + 0.2), toon={'face': {'lid': 0.2, 'mouth': 'O'}}, toonDur=0.08)])],   # off toward us, whistling
        props=[TUBP('tub1', fillKeys=[[0.0, 0.2], [ON1, 0.2], [D1, 0.55]], tap=[ON1, 99.0]),
               P('notes1', 'whistleNotes', on={'actor': 'mec', 'joint': 'head', 'offset': [0.12, 0.05, 0.12]}, opts={'from': r(GO1 + 0.2), 'every': 0.22, 'n': 4, 'size': 0.09})],
        cams=[FC(0.0, [-0.5, 2.0, 1.4], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.0, ME1[2]], [r(ME1[0] + 0.5), 1.4, ME1[2]], [r(TUB[0] - TW / 2), 0.1, TUB[2]], [MOUTH[0], 1.1, MOUTH[2]], [r(TUB[0] - TW / 2), 0.9, RIMZ]], top=0.14, bottom=0.78, inside=BATH)])   # (stills 1) higher, into the tub (the water and the stream were hidden by its wall); him whole
st.cue('sfx:click', 'S01', 0.18, 0.3); st.cue('sfx:pour', 'S01', ON1, 0.45); st.cue('sfx:ring', 'S01', RING1, 0.35)

# 2: the water ran down the stairs. Up a flight of stairs from its foot: the water pours off the landing and down the steps toward us, a lip of
#    foam in front; the old lady coming down with her cup of tea is lifted by it and rides it down seated, cup level, and sips as she slides past
D2 = st.dur('S02'); T2 = 0.05; SP2 = 3.6; ST2 = [0.0, 0, 1.0]; N2 = 12
PROF2 = [[-2.75, 2.42], [r(ST2[2] - (N2 - 1) * 0.28), 2.42], [ST2[2], 0.22], [r(ST2[2] + 0.3), 0.02]]
def along(prof, s):   # the point at distance s along a profile [[z, y], ...]
    for i in range(1, len(prof)):
        (za, ya), (zb, yb) = prof[i - 1], prof[i]; l = math.hypot(zb - za, yb - ya)
        if s <= l: u = s / l; return [za + (zb - za) * u, ya + (yb - ya) * u]
        s -= l
    return [prof[-1][0] + s, prof[-1][1]]
STEP2 = 6; MZ2 = r(ST2[2] - STEP2 * 0.28 - 0.14); MY2 = r(0.2 * (STEP2 + 1))   # the old lady on the seventh step
S_HIT2 = 0.52 + math.hypot(PROF2[1][0] - PROF2[2][0], PROF2[1][1] - PROF2[2][1]) * ((PROF2[1][0] - MZ2) / (PROF2[1][0] - PROF2[2][0]) if False else (MZ2 - PROF2[1][0]) / (PROF2[2][0] - PROF2[1][0]))
HIT2 = r(T2 + S_HIT2 / SP2)
RIDE2 = []
for i in range(1, 13):
    t_ = r(HIT2 + 0.1 * i)
    if t_ > D2 - 0.02: break
    z_, y_ = along(PROF2 + [[r(ST2[2] + 3.4), 0.02]], (t_ - T2) * SP2 + 0.15); z_ = min(z_, 1.5); RIDE2.append(k(r(t_ - 0.1), to=[0.15, r(y_ + 0.07), r(z_)], dur=0.1, ease='linear', face='keep', glide=True))
st.shot('S02', 'immeubleHall', setOpts={'back': -3.2, 'plant': False}, actors=[
        act('mamie', [0.15, MY2, MZ2], 0, 'stand', 'neutral', keys=[k(0.0, look=[0.1, 0.0, 2.0]), k(0.0, toon={'face': {'lid': 0.35}}, toonDur=0.0),
            k(r(HIT2 - 0.25), look=[0.1, 3.0, -2.6]), k(HIT2, clip='sitFloorSip'), k(HIT2, toon={'face': {'lid': 0.4, 'brow': 0.2}}, toonDur=0.06), *RIDE2, k(r(HIT2 + 0.35), look='camera')])],   # lifted and carried, she sips
        props=[P('stairs2', 'stairs', pos=ST2, opts={'steps': N2, 'w': 1.5}), P('land2', 'floorSlab', pos=[0.0, 2.32, -2.95], opts={'w': 1.8, 'd': 0.5, 'h': 0.1}),
               P('casc2', 'cascade', pos=[0.0, 0, 0.0], opts={'profile': PROF2, 'w': 1.45, 'at': T2, 'speed': SP2, 'thick': 0.08, 'pool': 3.2}),
               P('cup2', 'mug', on={'actor': 'mamie', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]})],
        cams=[FC(0.0, [0.9, 0.9, 4.6], [[0.0, 2.9, -2.9], [0.0, 0.0, 1.5], [0.15, r(MY2 + 1.9), MZ2], [-0.75, 1.0, 0.0], [0.75, 1.0, 0.0], [0.15, 1.4, 1.5]], top=0.12, bottom=0.82)])   # (her ride stops at the foot of the stairs)
st.cue('whoosh', 'S02', 0.05, 0.35, 1.0, 200, 1200); st.cue('sfx:splash', 'S02', HIT2, 0.3)

# 3: then into the street. From across the road: the water bursts out of his building's front door and spreads over the pavement and the road;
#    a man walking along reading his paper walks on, the water round his ankles
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts={'clear': [-6.0, 6.0]}, look=XLOOK, actors=[
        act('passant', [7.4, 0, -3.0], 0, 'walkRead', 'neutral', keys=[k(0.0, to=[7.4, 0, 0.2], dur=D3, ease='linear', clip='walkRead'), k(0.0, toon={'face': {'lid': 0.5}}, toonDur=0.0)])],
        props=[P('door3', 'door', pos=[10.15, 0, 0.0], ry=-90, opts={'w': 1.5, 'h': 2.6, 'open': 1.0}),
               P('casc3', 'cascade', pos=[10.1, 0, 0.0], ry=-90, opts={'profile': [[0.0, 1.0], [0.25, 0.9], [1.1, 0.05]], 'w': 1.5, 'at': 0.0, 'speed': 4.0, 'thick': 0.1, 'pool': 4.5}),
               FLOOD('fl3', 0.0, 0.32, 0.15, D3, w=30.0, d=40.0, pos=(0.0, 0, 0.0), fl=[{'kind': 'letter', 'x': 3.0, 'z': -1.0, 'ry': 0.5, 's': 1.0}, {'kind': 'stool', 'x': -1.0, 'z': 1.5, 'ry': 0.3, 's': 1.0}]),
               P('paper3', 'newspaper', on={'actor': 'passant', 'hand': 'R', 'offset': [0.05, 0.0, 0.05]})],
        cams=[FC(0.0, [1.0, 1.4, 6.5], [[10.15, 3.0, 0.0], [10.15, 0.0, -1.0], [7.4, 2.45, -1.8], [7.0, 0.0, 1.0], [4.5, 0.0, 2.5]], top=0.14, bottom=0.8)])
st.cue('sfx:splash', 'S03', 0.05, 0.4); st.cue('whoosh', 'S03', 0.1, 0.3, 0.8, 200, 1000)

# 4: the neighbours got out their rubber rings. Up the facade from the flooded street: on one balcony a neighbour blows into a duck ring that swells
#    with an overshoot and looks at him; on the one above, a lady pulls a diving mask down over her eyes; the water below
D4 = st.dur('S04'); BX4 = 9.6
BLOW4 = lambda puff: {'touch': {'R': ['face', -0.05, -0.1, 0.16, 1, 0.02], 'L': ['face', 0.05, -0.1, 0.16, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'mouth': 'O', 'swell': r(0.9 * puff), 'eye': r(0.3 * puff), 'lid': 0.2}}
st.shot('S04', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, look=XLOOK, actors=[
        act('voisin1', [BX4, 3.6, -1.0], -90, 'stand', 'neutral', keys=[k(0.0, look=[8.6, 4.3, -1.0]), k(0.0, toon=BLOW4(0.0), toonDur=0.0),
            *[kk for i, t_ in enumerate((0.15, 0.5, 0.85)) for kk in (k(t_, toon=BLOW4(1.0), toonDur=0.1, toonEase='out'), k(r(t_ + 0.22), toon=BLOW4(0.2), toonDur=0.1))],
            k(1.25, toon={'touch': {'R': ['face', -0.05, -0.1, 0.16, 1, 0.02], 'L': ['face', 0.05, -0.1, 0.16, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'eye': 0.8, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.06), k(1.3, look='camera')]),   # the duck looks at him: his eyes pop
        act('voisine2', [BX4, 6.8, 1.2], -90, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['face', -0.1, 0.12, 0.14, 1, 0.02], 'L': ['face', 0.1, 0.12, 0.14, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            k(0.55, toon={'touch': {'R': ['face', -0.1, 0.0, 0.16, 1, 0.02], 'L': ['face', 0.1, 0.0, 0.16, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.12, toonEase='inOut'), *BLINK(1.4, {'lid': 0.3})])],
        props=[P('balc4a', 'balcony', pos=[9.55, 3.6, -1.0], ry=-90, opts={'w': 2.6, 'd': 1.1, 'rail': 'front'}), P('balc4b', 'balcony', pos=[9.55, 6.8, 1.2], ry=-90, opts={'w': 2.6, 'd': 1.1, 'rail': 'front'}),
               P('duck4', 'duckRing', pos=[9.05, 3.95, -1.0], ry=-90, opts={'r': 0.42, 'inflate': [0.1, 1.15]}, keys=[k(1.15, rotTo=[0, r(-PI / 2 + 0.5), 0], dur=0.15, ease='out')]),
               P('mask4', 'diveMask', on={'actor': 'voisine2', 'joint': 'head', 'offset': [0.0, -0.18, 0.0]}, keys=[k(0.0, offset=[0.0, -0.06, 0.0], dur=0.0), k(0.55, offset=[0.0, -0.18, 0.0], dur=0.12)]),
               FLOOD('fl4', 1.9, 2.0, 0.0, D4, w=30.0, d=40.0)],
        cams=[FC(0.0, [3.4, 2.3, 5.8], [[BX4, 6.3, -1.0], [BX4, 8.9, 1.2], [8.8, 3.6, -1.0], [8.8, 2.0, 1.5], [9.6, 2.1, -2.6]], top=0.14, bottom=0.8)])
st.cue('sfx:stretch', 'S04', 0.15, 0.3); st.cue('sfx:stretch', 'S04', 0.5, 0.3); st.cue('sfx:stretch', 'S04', 0.85, 0.3); st.cue('sfx:squeak', 'S04', 1.15, 0.3)

# 5: the firemen pumped all night. At night in the flooded street: a fire engine; one fireman works the pump, the other holds the outflow hose
#    and pours the water back into the street three metres away; he looks from the jet to the intake, then at us
D5 = st.dur('S05')
st.shot('S05', 'parisStreet', setOpts={'night': True, 'clear': [-8.0, 8.0]}, look={'sun': 0.1, 'sunColor': '#8FA4E0', 'fill': 0.25, 'exposure': 1.05, 'probe': 0.35, 'hemi': 0.25}, actors=[
        act('pompier1', [-1.2, 0.55, 1.0], 60, 'stand', 'neutral', keys=[k(0.0, look=[1.6, 0.5, 1.6]),
            k(0.0, toon={'reach': {'R': [-0.75, 1.15, 1.25, 1, 0.03], 'L': [-0.95, 1.05, 1.05, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(0.75, look=[-3.0, 0.5, -0.8]), k(1.2, look=[1.6, 0.5, 1.6]), k(1.45, look='camera'), k(1.5, toon={'reach': {'R': [-0.75, 1.15, 1.25, 1, 0.03], 'L': [-0.95, 1.05, 1.05, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'brow': 0.3}}, toonDur=0.1), *BLINK(1.85, {'lid': 0.5, 'brow': 0.3})]),   # the jet, the intake, us
        act('pompier2', [-3.6, 0.55, -1.6], 20, 'stand', 'neutral', keys=[k(0.0, look=[-3.2, 1.0, -1.0]),
            *[kk for i in range(5) for kk in (k(r(0.05 + 0.4 * i), toon={'reach': {'R': [-3.4, 1.35, -1.2, 1, 0.03], 'L': [-3.6, 1.35, -1.2, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.15, toonEase='inOut'),
                                       k(r(0.25 + 0.4 * i), toon={'reach': {'R': [-3.4, 0.95, -1.2, 1, 0.03], 'L': [-3.6, 0.95, -1.2, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.15, toonEase='inOut'))]])],   # the pump handle up and down
        props=[P('truck5', 'fireTruck', pos=[-5.6, 0, -2.0], ry=0), FLOOD('fl5', 0.55, 0.55, 0.0, 1.0, w=30.0, d=50.0, op=0.8),
               P('jet5', 'waterJet', on={'actor': 'pompier1', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'len': 2.2, 'lance': 0.6, 'on': [[0.0, True]]}),
               P('pump5', 'floorSlab', pos=[-3.5, 0.55, -1.2], opts={'w': 0.5, 'd': 0.4, 'h': 0.55, 'color': '#C8322A'})],
        tethers=[{'a': {'prop': 'truck5', 'offset': [1.2, 1.0, 1.2]}, 'b': {'actor': 'pompier1', 'hand': 'L'}, 'color': '#C9A43E', 'radius': 0.05, 'radial': 8, 'sag': 0.5, 'n': 14},
                 {'a': {'prop': 'truck5', 'offset': [1.3, 0.8, 0.6]}, 'b': {'prop': 'pump5', 'offset': [3.6, -0.6, 1.4]}, 'color': '#C9A43E', 'radius': 0.05, 'radial': 8, 'sag': 0.3, 'n': 14}],
        cams=[FC(0.0, [3.4, 1.7, 6.2], [[-1.2, 2.95, 1.0], [-3.6, 2.95, -1.6], [1.8, 0.5, 1.8], [-3.0, 0.5, 0.0], [-5.6, 2.5, -2.0]], top=0.14, bottom=0.8)])
st.cue('sfx:splash', 'S05', 0.1, 0.25); st.cue('sfx:rattle', 'S05', 0.05, 0.2); st.cue('sfx:rattle', 'S05', 0.85, 0.2); st.cue('sfx:rattle', 'S05', 1.65, 0.2)

# 6: the water rose even faster. At a crossing a policeman directs the traffic with his whistle; the water climbs from his waist over his head in a
#    second; his cap floats up; his white glove still waves the traffic on above the water, bubbles rising
D6 = st.dur('S06'); UP6 = [0.25, 1.15]; Y6 = [1.0, 2.6]
def lvl6(t_):
    u = min(1.0, max(0.0, (t_ - UP6[0]) / (UP6[1] - UP6[0]))); u = 1 - (1 - u) ** 2; return Y6[0] + (Y6[1] - Y6[0]) * u
WAVE6 = lambda a, hy=2.35: {'reach': {'R': [r(0.35 + 0.15 * a), hy, r(0.25 * a), 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'O'}}
st.shot('S06', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, look=XLOOK, actors=[
        act('agent', [0.0, 0, 0.0], 25, 'stand', 'neutral', keys=[k(0.0, look='camera'), *[k(r(0.08 + 0.3 * i), toon=WAVE6(1 if i % 2 else -1, 2.35 if i < 3 else 3.05), toonDur=0.18, toonEase='inOut') for i in range(7)]])],
        props=[FLOOD('fl6', Y6[0], Y6[1], UP6[0], UP6[1], w=30.0, d=50.0),
               P('cap6', 'copCap', on={'actor': 'agent', 'joint': 'head', 'offset': [0.0, 0.31, 0.0]}, keys=[k(0.62, detach=True), *[k(r(0.62 + 0.08 * i), to=[r(0.05 + 0.04 * i), r(lvl6(0.62 + 0.08 * (i + 1)) + 0.02), r(0.1 + 0.03 * i)], dur=0.08, ease='linear') for i in range(14) if 0.62 + 0.08 * (i + 1) < D6]]),
               P('bub6', 'bubbles', pos=[0.05, 1.6, 0.15], opts={'rate': 9.0, 'area': 0.2, 'h': 1.2, 'life': 0.9, 'speed': 1.2}, keys=[k(0.0, visible=False), k(0.75, visible=True)]),
               P('whis6', 'whistle', on={'actor': 'agent', 'joint': 'head', 'offset': [0.0, -0.05, 0.17]})],
        cams=[FC(0.0, [1.9, 3.7, 5.8], [[0.0, 2.5, 0.0], [0.0, 0.9, 0.0], [0.8, 3.2, 0.2], [-1.2, 0.9, 1.2], [1.4, 0.9, 1.2]], top=0.14, bottom=0.8, inside=(-20.0, 20.0, 3.2, 20.0, -30.0, 30.0))])   # (stills 1) above the water's final level (under it, the box's faces vanish: a dry street)
st.cue('sfx:whistle', 'S06', 0.1, 0.3); st.cue('sfx:gulp', 'S06', 0.6, 0.35); st.cue('sfx:whistle', 'S06', 1.3, 0.15)

# 7: the town hall declared... The town hall with the water halfway up its columns; the mayor in his sash on its roof lifts his megaphone and a
#    finger
D7 = st.dur('S07'); TH = [0.0, 0, -6.0]
st.shot('S07', 'grassland', look=XLOOK, actors=[act('maire', [0.0, 4.75, -6.2], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': [0.12, 1.55 + 4.75, -5.9, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'line'}}, toonDur=0.0),
            k(0.25, toon={'reach': {'R': [0.12, 1.62 + 4.75, -5.85, 1, 0.03], 'L': [-0.35, 2.2 + 4.75, -5.95, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'point'}, 'face': {'mouth': 'O', 'brow': 0.6}}, toonDur=0.12, toonEase='out'), *BLINK(1.0, {'mouth': 'line'})])],
        props=[P('th7', 'townHall', pos=TH, opts={'w': 7.0, 'h': 4.5, 'text': 'MAIRIE', 'gable': 'v2'}), FLOOD('fl7', 2.3, 2.4, 0.0, D7, w=40.0, d=40.0),
               P('sash7', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]}), P('mega7', 'megaphone', on={'actor': 'maire', 'hand': 'R', 'offset': [0.0, 0.0, 0.08]})],
        cams=[FC(0.0, [2.2, 3.4, 4.0], [[0.0, 7.4, -6.2], [-3.5, 2.4, -4.0], [3.5, 2.4, -4.0], [0.0, 4.75, -6.2]], top=0.14, bottom=0.78)])
st.cue('sfx:static', 'S07', 0.25, 0.25)

# 8: ...the town a seaside resort. Closer: a banner unrolls down the front of the town hall, STATION BALNÉAIRE; a striped parasol opens beside the
#    mayor; bunting; he lowers the megaphone and looks at us
D8 = st.dur('S08')
st.shot('S08', 'grassland', look=XLOOK, actors=[act('maire', [-0.9, 4.75, -6.2], 15, 'stand', 'happy', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': [-0.75, 1.0 + 4.75, -6.0, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'smile'}}, toonDur=0.0), *BLINK(0.9, {'mouth': 'smile'})])],
        props=[P('th8', 'townHall', pos=TH, opts={'w': 7.0, 'h': 4.5, 'text': 'MAIRIE', 'gable': 'v2'}), FLOOD('fl8', 2.4, 2.4, 0.0, 1.0, w=40.0, d=40.0),
               P('ban8', 'carnivalBanner', pos=[0.6, 4.05, -3.65], opts={'text': 'STATION BALNÉAIRE', 'w': 4.6, 'h': 1.05, 'startAt': 0.05, 'dur': 0.35}),
               P('para8', 'parasol', pos=[-0.1, 4.5, -6.0], opts={'openAt': 0.3, 'colors': ['#E8463A', '#FFFFFF']}),
               P('bunt8', 'bunting', pos=[0.0, 4.55, -3.9], opts={'len': 6.8, 'sag': 0.35, 'n': 14}),
               P('sash8', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]}), P('mega8', 'megaphone', on={'actor': 'maire', 'hand': 'R', 'offset': [0.0, 0.0, 0.08]})],
        cams=[FC(0.0, [1.4, 4.4, 2.0], [[-0.9, 7.3, -6.2], [-2.0, 3.0, -3.9], [3.0, 3.0, -3.9], [0.6, 4.6, -3.9]], top=0.2, bottom=0.78)])
st.cue('whoosh', 'S08', 0.05, 0.3, 0.5, 400, 1800); st.cue('sfx:fanfare', 'S08', 0.35, 0.2)

# 9: the tourists came to sunbathe on the roofs. Roof level, the water lapping at the gutters: tourists in sunglasses on deckchairs on the zinc,
#    a parasol; one stands on a chimney, spreads his arms and swan-dives into the street-sea: splash
D9 = st.dur('S09'); WY9 = 14.6; DIVE9 = 1.0
st.shot('S09', 'grassland', look=XLOOK, actors=[
        act('touriste1', [-1.2, r(WY9 + 1.15), 0.2], 20, 'reclineBack', 'happy', keys=[k(0.0, look=[0.0, 30.0, 10.0]), k(0.0, toon={'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=0.0), k(1.5, look='camera'), k(1.5, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.1)]),
        act('touriste2', [1.5, r(WY9 + 2.2), -0.6], 90, 'stand', 'happy', keys=[k(0.0, look=[4.0, WY9, 0.0]), k(0.35, clip='swanDive'), k(r(DIVE9 - 0.05), clip='swanDive'),
            k(DIVE9, to=[4.2, r(WY9 + 3.0), -0.6], dur=0.3, ease='out', glide=True, face='keep'), k(r(DIVE9 + 0.3), to=[5.4, r(WY9 - 0.8), -0.6], dur=0.3, ease='in', glide=True, face='keep'), k(r(DIVE9 + 0.6), visible=False)])],
        props=[P('roof9a', 'zincRoof', pos=[-1.0, r(WY9 + 0.6), -0.2], opts={'w': 5.0}), P('roof9b', 'zincRoof', pos=[1.8, r(WY9 + 0.6), -0.4], ry=90, opts={'w': 3.0}),
               P('chair9', 'deckChair', pos=[-1.2, r(WY9 + 1.15), 0.2], ry=20), P('para9', 'parasol', pos=[-2.4, r(WY9 + 1.15), -0.3], opts={'openAt': -1.0}),
               FLOOD('fl9', WY9, WY9, 0.0, 1.0, w=600.0, d=600.0, op=0.86), *TOWN('9', WY9, [(-15.0, -20.0, 0, 0.0), (5.0, -24.0, 0, 0.7), (21.0, -9.0, -90, 0.3), (-27.0, -6.0, 90, 0.9)]),
               P('shades9a', 'shades', on={'actor': 'touriste1', 'joint': 'head', 'offset': [0.0, 0.2, 0.16]}), P('shades9b', 'shades', on={'actor': 'touriste2', 'joint': 'head', 'offset': [0.0, 0.2, 0.16]}),
               P('drops9', 'waterDrops', pos=[5.4, WY9, -0.6], opts={'at': r(DIVE9 + 0.58), 'n': 26, 'r': 0.07, 'speed': 4.5, 'spread': 0.9, 'color': '#BFE6F7', 'life': 0.8})],
        cams=[FC(0.0, [0.6, r(WY9 + 1.9), 6.5], [[-1.2, r(WY9 + 2.0), 0.2], [1.5, r(WY9 + 4.6), -0.6], [5.4, WY9, -0.6], [-2.8, WY9, 0.6]], top=0.14, bottom=0.78)])
st.cue('sfx:boing', 'S09', DIVE9, 0.25); st.cue('sfx:splash', 'S09', r(DIVE9 + 0.58), 0.45)

# 10: the navy sent a submarine. Low over the water in the drowned street: a periscope pops up, looks left, right, sees us, ducks under with a gulp
#     and slowly comes back up, staring; the dark shape of the hull under the water
D10 = st.dur('S10'); WY10 = 3.0
st.shot('S10', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, look=XLOOK, actors=[],
        props=[FLOOD('fl10', WY10, WY10, 0.0, 1.0, w=30.0, d=60.0, op=0.78),
               P('sub10', 'submarine', pos=[0.0, r(WY10 - 2.6), -1.0], ry=20, opts={'len': 6.0, 'peri': [[0.0, 0.0], [0.15, 0.0], [0.4, 1.0], [1.15, 1.0], [1.25, 0.25], [1.45, 0.25], [1.8, 0.85]],
                    'periYaw': [[0.0, -20.0], [0.45, -20.0], [0.65, -80.0], [0.85, 40.0], [1.0, -20.0], [1.12, -20.0]]})],
        cams=[FC(0.0, [-0.6, r(WY10 + 1.7), 5.6], [[0.0, r(WY10 + 1.4), -0.6], [-1.6, WY10, 1.0], [1.6, WY10, 1.0], [0.0, r(WY10 - 1.0), -2.0]], top=0.2, bottom=0.78, inside=(-20.0, 20.0, r(WY10 + 0.7), 20.0, -40.0, 40.0))])   # (stills 1) kept above the surface
st.cue('sfx:pop', 'S10', 0.3, 0.25); st.cue('sfx:gulp', 'S10', 1.15, 0.3); st.cue('sfx:squeak', 'S10', 1.5, 0.2)

# 11: it parked outside the bakery. The submarine surfaces under the bakery's fifth-floor window (BOULANGERIE, an arrow pointing down); the hatch
#     flips open, a sailor pops out like a jack-in-the-box and takes the baguette the baker hands down
D11 = st.dur('S11'); WY11 = 14.6; SUB11 = [8.2, r(WY11 - 1.15), 0.0]; HATCH11 = 0.45
SUBH = [SUB11[0], r(SUB11[1] + 6.0 * 0.26 * 0.9 + 6.0 * 0.26 * 0.62), r(SUB11[2] - 6.0 * 0.04 - (6.0 * 0.24 - 6.0 * 0.26 * 0.42) * 0.25)]   # the hatch (rotated 90 deg below)
st.shot('S11', 'grassland', look=XLOOK, actors=[
        act('marin', [r(SUB11[0] + 0.06), r(SUBH[1] - 1.5), SUB11[2]], -90, 'stand', 'happy', keys=[k(0.0, visible=False), k(r(HATCH11 + 0.08), visible=True),
            k(r(HATCH11 + 0.08), to=[r(SUB11[0] + 0.06), r(SUBH[1] - 0.75), SUB11[2]], dur=0.18, ease='outBack', glide=True, face='keep'), k(r(HATCH11 + 0.08), look=[10.0, r(WY11 + 2.4), 0.0]),
            k(r(HATCH11 + 0.1), toon={'sq': [0.85, 1.25, 0.85], 'face': {'eye': 0.3, 'mouth': 'smile'}}, toonDur=0.06), k(r(HATCH11 + 0.26), toon={'sq': [1.0, 1.0, 1.0], 'face': {'mouth': 'smile'}}, toonDur=0.1),
            k(0.95, toon={'reach': {'R': [9.6, r(WY11 + 2.55), 0.05, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'smile'}}, toonDur=0.15, toonEase='out'), k(1.35, look='camera')]),
        act('boulanger', [10.25, r(WY11 + 1.2), 0.0], -90, 'stand', 'happy', keys=[k(0.0, look=[8.2, r(WY11 + 1.4), 0.0]), k(0.0, toon={'reach': {'R': [9.65, r(WY11 + 2.5), 0.05, 1, 0.03]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.0),
            k(1.2, toon={'reach': {'R': [9.9, r(WY11 + 2.2), 0.0, 1, 0.03]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'mouth': 'smile'}}, toonDur=0.15)])],
        props=[FLOOD('fl11', WY11, WY11, 0.0, 1.0, w=600.0, d=600.0, op=0.86), *TOWN('11', WY11, [(-6.0, -24.0, 0, 0.4), (-22.0, -8.0, 90, 0.8)]), P('fac11', 'haussmann', pos=[10.6, r(WY11 - 13.2), 0.0], ry=-90, opts={'w': 13.0, 'h': 18.0, 'floors': 6, 'cols': 5}),
               P('sign11', 'signBoard', pos=[10.0, r(WY11 + 3.0), 1.4], ry=-90, opts={'text': 'BOULANGERIE', 'w': 2.4, 'h': 0.45, 'height': 0.0, 'bg': '#7A4A2A', 'fg': '#F6E7C1', 'posts': False}),
               P('sub11', 'submarine', pos=SUB11, ry=90, opts={'len': 6.0, 'hatchAt': HATCH11, 'peri': [[0.0, 1.0]]}, keys=[k(0.0, to=SUB11, dur=0.0), k(0.0, to=[SUB11[0], r(SUB11[1] - 1.2), SUB11[2]], dur=0.0), k(0.0, to=SUB11, dur=0.35, ease='out')]),
               P('cap11', 'captainCap', on={'actor': 'marin', 'joint': 'head', 'offset': [0.0, 0.17, -0.01]}, scale=1.0),
               P('bag11', 'baguette', on={'actor': 'boulanger', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, keys=[k(1.12, attach='marin', hand='R', offset=[0.0, 0.0, 0.05])]),
               P('hat11', 'chefHat', on={'actor': 'boulanger', 'joint': 'head', 'offset': [0.0, 0.4, 0.0]})],
        cams=[FC(0.0, [3.0, r(WY11 + 1.6), 5.2], [[8.2, r(WY11 + 3.6), 0.0], [10.25, r(WY11 + 3.4), 0.0], [5.4, WY11, 0.0], [10.0, WY11, 1.6]], top=0.14, bottom=0.78)])
st.cue('sfx:splash', 'S11', 0.1, 0.3); st.cue('sfx:boing', 'S11', r(HATCH11 + 0.08), 0.3); st.cue('sfx:clink', 'S11', HATCH11, 0.25)

# 12: the scientists added... In a map room two scientists in white coats: one rolls a paint roller of blue across the big wall map, left to right
D12 = st.dur('S12'); P12 = [0.15, r(D12 + 1.2)]
ROLL12 = lambda u: [r(-1.15 + 2.3 * u), 1.75, -2.45]
st.shot('S12', 'mairie', setOpts={'desk': False, 'banner': False, 'map': False}, actors=[
        act('savant1', [-1.3, 0, -1.75], 160, 'stand', 'neutral', keys=[k(0.0, look=[-1.0, 1.6, -2.6]), k(0.0, toon={'reach': {'R': ROLL12(0.0) + [1, 0.03], 'L': [ROLL12(0.0)[0] - 0.1, 1.45, -2.4, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.0),
            k(0.15, to=[0.4, 0, -1.75], dur=r(D12 - 0.15), ease='linear', face='keep', glide=True),
            *[k(r(0.15 + 0.15 * i), toon={'reach': {'R': ROLL12(min(1.0, (0.15 * i) / (P12[1] - P12[0]))) + [1, 0.03], 'L': [r(ROLL12(min(1.0, (0.15 * i) / (P12[1] - P12[0])))[0] - 0.1), 1.45, -2.4, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.15, toonEase='linear') for i in range(1, 9) if 0.15 + 0.15 * i < D12]]),
        act('savant2', [1.4, 0, -1.35], -150, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, -2.6]), k(0.0, toon={'touch': {'R': ['face', -0.08, -0.12, 0.1, 1, 0.02]}, 'hands': {'R': 'point'}}, toonDur=0.0), *BLINK(0.7, {})])],
        props=[P('map12', 'seaMap', pos=[0.0, 1.75, -2.53], opts={'w': 2.6, 'h': 1.8, 'paint': P12}),
               P('roll12', 'paintRoller', on={'actor': 'savant1', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'color': '#2F7FC4', 'len': 0.5})],
        cams=[FC(0.0, [0.2, 1.5, 2.6], [[-1.3, 2.45, -1.75], [1.4, 2.45, -1.35], [-1.4, 0.8, -2.53], [1.4, 0.8, -2.53], [0.0, 2.7, -2.53], [1.4, 0.0, -1.35]], top=0.14, bottom=0.75)])
st.cue('sfx:slideUp', 'S12', 0.2, 0.25)

# 13: ...a sea to the maps. Close on the map: the new sea in the middle of the country is a bathtub on four feet, its tap and all; the roller
#     finishes it, MER and a little boat pop up in it; the second scientist taps it with his pointer and looks at us
D13 = st.dur('S13'); LAB13 = 0.55
st.shot('S13', 'mairie', setOpts={'desk': False, 'banner': False, 'map': False}, actors=[
        act('savant2', [1.25, 0, -1.9], -140, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.75, -2.53]), k(0.0, toon={'reach': {'R': [0.3, 1.7, -2.45, 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3}}, toonDur=0.0),
            k(r(LAB13 + 0.1), toon={'reach': {'R': [0.28, 1.72, -2.49, 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3}}, toonDur=0.05), k(r(LAB13 + 0.18), toon={'reach': {'R': [0.3, 1.7, -2.44, 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3}}, toonDur=0.05),
            k(r(LAB13 + 0.35), look='camera'), *BLINK(r(LAB13 + 0.7), {'lid': 0.3})])],
        props=[P('map13', 'seaMap', pos=[0.0, 1.75, -2.53], opts={'w': 2.6, 'h': 1.8, 'paint': [-1.0, 0.25], 'labelAt': LAB13})],
        cams=[FC(0.0, [0.1, 1.7, 0.0], [[-1.3, 2.65, -2.53], [1.3, 0.85, -2.53], [1.25, 2.4, -1.9]], top=0.16, bottom=0.7)])   # his knees at the frame's foot
st.cue('sfx:pop', 'S13', LAB13, 0.25); st.cue('sfx:tick', 'S13', r(LAB13 + 0.1), 0.2)

# 14: the president came by pedalo. Between the chimneys at roof level: the president pedals a swan pedalo, knees pumping up to his chin, his two
#     guards swimming beside him in rubber rings; a wave and a look at us
D14 = st.dur('S14'); WY14 = 14.6; PED14 = [-2.0, WY14, 0.0]
PEDAL = lambda a: {'bend': {'legL': [r(-1.5 - 0.6 * a), 0, 0, 1, None], 'legR': [r(-1.5 + 0.6 * a), 0, 0, 1, None]}, 'face': {'mouth': 'smile', 'lid': 0.2}}
st.shot('S14', 'grassland', look=XLOOK, actors=[
        act('president', [-2.0, r(WY14 + 0.25), 0.0], 70, 'sit', 'happy', keys=[k(0.0, to=[0.6, r(WY14 + 0.25), 0.4], dur=D14, ease='linear', face='keep', glide=True), k(0.0, look='camera'),
            *[k(r(0.1 * i), toon=PEDAL(1 if i % 2 else -1), toonDur=0.1, toonEase='inOut') for i in range(int(D14 / 0.1))]]),
        *[act(f'garde{j + 1}', [-2.1, r(WY14 - 1.05), r(-1.3 + 2.6 * j)], 70, 'scuba', 'neutral', keys=[k(0.0, to=[0.5, r(WY14 - 1.05), r(-0.9 + 2.6 * j)], dur=D14, ease='linear', face='keep', glide=True), k(0.0, look=[3.0, WY14, 0.0]), k(r(0.9 + 0.3 * j), look='camera')]) for j in range(2)]],
        props=[FLOOD('fl14', WY14, WY14, 0.0, 1.0, w=600.0, d=600.0, op=0.86), *TOWN('14', WY14, [(-12.0, -22.0, 0, 0.5), (12.0, -26.0, 0, 0.0), (-26.0, -2.0, 90, 0.8)]), P('ped14', 'pedalo', pos=PED14, ry=70, keys=[k(0.0, to=[0.6, WY14, 0.4], dur=D14, ease='linear')]),
               *[P(f'ring14{j}', 'duckRing', pos=[-2.1, r(WY14 + 0.05), r(-1.3 + 2.6 * j)], ry=70, opts={'r': 0.45, 'bob': True}, keys=[k(0.0, to=[0.5, r(WY14 + 0.05), r(-0.9 + 2.6 * j)], dur=D14, ease='linear')]) for j in range(2)],
               P('roof14a', 'zincRoof', pos=[-4.0, r(WY14 + 0.6), -4.0], opts={'w': 7.0}), P('roof14b', 'zincRoof', pos=[4.5, r(WY14 + 0.6), -3.0], ry=90, opts={'w': 4.0})],
        cams=[FC(0.0, [2.8, r(WY14 + 1.6), 5.0], [[-2.0, r(WY14 + 1.9), 0.0], [0.6, r(WY14 + 1.9), 0.4], [-2.1, WY14, -1.3], [0.5, WY14, 1.7], [-4.0, r(WY14 + 2.2), -4.0]], top=0.2, bottom=0.78)])
st.cue('sfx:squeak', 'S14', 0.1, 0.2); st.cue('sfx:splash', 'S14', 0.6, 0.15)

# 15: he opened a lighthouse. On the roof of this man's building, now a lighthouse: the president presses a big red button; the lamp lights, the
#     beam sweeps round and catches him full in the face; squint, smile
D15 = st.dur('S15'); WY15 = 14.6; PRESS15 = 0.35; LH15 = [0.0, r(WY15 + 0.6), -2.0]
st.shot('S15', 'grassland', look={'sat': 0.85, 'exposure': 0.95}, actors=[
        act('president', [1.6, r(WY15 + 0.6), -0.4], -60, 'stand', 'happy', keys=[k(0.0, look=[1.05, r(WY15 + 1.6), -0.8]),
            k(0.0, toon={'reach': {'R': [1.1, r(WY15 + 1.75), -0.75, 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'mouth': 'smile'}}, toonDur=0.0),
            k(PRESS15, toon={'reach': {'R': [1.1, r(WY15 + 1.62), -0.75, 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'mouth': 'smile'}}, toonDur=0.06), k(r(PRESS15 + 0.2), look=[0.0, r(WY15 + 5.4), -2.0]),
            k(1.0, look='camera'), k(1.02, toon={'face': {'lid': 0.85, 'mouth': 'bigsmile', 'brow': -0.3}}, toonDur=0.04), k(1.55, toon={'face': {'lid': 0.4, 'mouth': 'smile'}}, toonDur=0.1)])],   # the beam in his face
        props=[FLOOD('fl15', WY15, WY15, 0.0, 1.0, w=600.0, d=600.0, op=0.86), *TOWN('15', WY15, [(-14.0, -20.0, 0, 0.3), (14.0, -16.0, -90, 0.6)]), P('roof15', 'floorSlab', pos=[0.4, r(WY15 + 0.3), -1.2], opts={'w': 5.0, 'd': 4.0, 'h': 0.3, 'color': '#8C9AA8'}),
               P('lh15', 'lighthouseLive', pos=LH15, opts={'h': 6.0, 'onAt': r(PRESS15 + 0.05), 'aim': [[0.0, 140.0], [r(PRESS15 + 0.05), 140.0], [0.95, 40.0], [1.05, 62.0], [1.6, 62.0], [2.2, 200.0]], 'len': 14.0}),
               P('btn15', 'bigButton', pos=[1.1, r(WY15 + 0.6), -0.75], opts={'pressAt': PRESS15})],
        cams=[FC(0.0, [4.2, r(WY15 + 2.2), 4.4], [[0.0, r(WY15 + 6.8), -2.0], [1.6, r(WY15 + 2.95), -0.4], [1.6, r(WY15 + 0.6), -0.4], [-1.8, WY15, 0.0]], top=0.12, bottom=0.78)])
st.cue('sfx:click', 'S15', PRESS15, 0.3); st.cue('sfx:ding', 'S15', 1.0, 0.3)

# 16: three years later... His bathroom is a sea floor: the water up to the rim, seaweed hanging from the tap, barnacles on the tub, a crab on the
#     rim snapping, a fish going by; he wades in to the tub, a diving mask up on his forehead
D16 = st.dur('S16'); WY16 = 0.72
st.shot('S16', 'salleDeBain', setOpts={'half': 3.4}, look={'exposure': 1.0}, actors=[act('mec', [2.5, 0, -0.45], -105, 'stand', 'unimpressed', keys=[k(0.0, to=[1.65, 0, -0.7], dur=D16, ease='out', clip='walk'), k(0.0, look=[0.9, 0.8, -1.6]), k(0.0, toon={'face': DEAD}, toonDur=0.0), k(0.85, look='camera')])],
        props=[TUBP('tub16', fill=1.05, tap=[-1.0, 99.0], weed=True, barnacles=True), FLOOD('fl16', WY16, WY16, 0.0, 1.0, w=5.4, d=7.0, pos=(0.0, 0, 1.2), op=0.62),
               P('crab16', 'crab', pos=[0.0, 0.78, r(RIMZ - 0.02)], opts={'s': 0.22, 'path': [[0.0, -0.3, 0.0], [0.5, 0.15, 0.0], [1.2, 0.15, 0.0]], 'snap': [0.55, 0.85]}),
               P('fish16', 'fishSchool', pos=[0.0, 0.0, -0.4], opts={'n': 4, 'rx': 1.4, 'rz': 0.6, 'y': [0.3, 0.6], 'size': 0.12, 'speed': 0.8, 'color': '#F28C28'}),
               P('mask16', 'diveMask', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})],
        cams=[FC(0.0, [-1.9, 0.95, 1.0], [[1.65, 2.45, -0.7], [-0.7, 0.6, TUB[2]], [MOUTH[0], 1.4, MOUTH[2]], [0.0, 0.7, RIMZ], [2.5, 1.0, -0.45]], top=0.14, bottom=0.78, inside=BATH)])   # low over the water from the left
st.cue('sfx:splash', 'S16', 0.1, 0.25); st.cue('sfx:splash', 'S16', 0.6, 0.2)

# 17: ...this man pulled the plug. Close over the tub: his arm plunges in and yanks the plug out on its chain: PLOP; at once a spiral turns on the
#     water and the level starts to drop; he holds the dripping plug up, deadpan
D17 = st.dur('S17'); PULL17 = 0.55
st.shot('S17', 'salleDeBain', setOpts={'half': 3.4}, look={'exposure': 1.0}, actors=[act('mec', [0.45, 0, -0.9], 156, 'stand', 'unimpressed', keys=[k(0.0, look=[DRAIN[0], 0.3, DRAIN[2]]),
            k(0.0, toon={'reach': {'R': [r(DRAIN[0] + 0.05), 0.62, r(DRAIN[2] + 0.1), 1, 0.03]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.0),
            k(0.2, toon={'reach': {'R': [DRAIN[0], 0.22, DRAIN[2], 1, 0.03]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.55, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.2, toonEase='in'),
            k(PULL17, toon={'reach': {'R': [r(DRAIN[0] + 0.05), 1.5, r(DRAIN[2] + 0.45), 1, 0.03]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.05, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'brow': 0.3}}, toonDur=0.08, toonEase='out'),   # the yank
            k(r(PULL17 + 0.3), look='camera'), *BLINK(r(PULL17 + 0.6))])],
        props=[TUBP('tub17', fillKeys=[[0.0, 1.0], [PULL17, 1.0], [r(D17 + 1.0), 0.45]], swirl=[PULL17, 99.0], plugOut=PULL17, weed=True, barnacles=True),
               FLOOD('fl17', WY16, 0.45, PULL17, r(D17 + 1.0), w=5.4, d=7.0, pos=(0.0, 0, 1.2), op=0.62),
               P('plug17', 'bathPlug', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}, opts={'at': PULL17}, keys=[k(0.0, visible=False), k(PULL17, visible=True)]),
               BURST('plop17', [r(DRAIN[0] + 0.2), 1.2, r(DRAIN[2] + 0.4)], r(PULL17 + 0.02), 'PLOP !', 0.42, 0.3)],
        cams=[FC(0.0, [1.9, 1.3, -1.5], [[0.45, 2.45, -0.9], [DRAIN[0], 0.3, DRAIN[2]], [-0.3, 0.75, TUB[2]], [r(DRAIN[0] + 0.05), 1.65, r(DRAIN[2] + 0.45)]], top=0.14, bottom=0.86, inside=BATH)])   # from the tap end: his face over the tub
st.cue('sfx:pop', 'S17', PULL17, 0.45); st.cue('sfx:gulp', 'S17', r(PULL17 + 0.2), 0.35)

# 18: the sea went off into his bathtub. From high over the drowned town: a whirlpool round his building (the lighthouse on its roof at the
#     centre) swallows the pedalo, the duck rings, the deckchairs, a sailboat and the submarine, round and round and down (GLOUGLOU)
D18 = st.dur('S18'); WY18 = 10.0   # (stills 1) above the ground: under it the funnel was buried in the grass
ITEMS18 = [{'kind': 'pedalo', 'r': 13.0, 'a': 0.3, 's': 1.6, 'from': 0.0, 'dur': 1.9, 'turns': 1.4}, {'kind': 'sub', 'r': 15.0, 'a': 2.4, 's': 1.0, 'from': 0.0, 'dur': 2.1, 'turns': 1.2},
           {'kind': 'boat', 'r': 11.0, 'a': 4.0, 's': 1.2, 'from': 0.0, 'dur': 1.6, 'turns': 1.5}, {'kind': 'ring', 'r': 8.0, 'a': 1.5, 's': 2.2, 'from': 0.0, 'dur': 1.2, 'turns': 1.6},
           {'kind': 'duck', 'r': 9.5, 'a': 5.2, 's': 1.6, 'from': 0.0, 'dur': 1.4, 'turns': 1.6}, {'kind': 'chair', 'r': 7.0, 'a': 3.3, 's': 2.0, 'from': 0.0, 'dur': 1.0, 'turns': 1.4},
           {'kind': 'parasol', 'r': 12.0, 'a': 5.9, 's': 1.6, 'from': 0.1, 'dur': 1.8, 'turns': 1.3}]
st.shot('S18', 'grassland', look=XLOOK, actors=[],
        props=[P('pool18', 'whirlpool', pos=[0.0, WY18, 0.0], opts={'r': 22.0, 'funnel': 4.2, 'depth': 9.0, 'at': 0.0, 'dur': 1.2, 'spin': 3.4, 'items': ITEMS18}),
               P('bld18', 'floorSlab', pos=[0.0, r(WY18 - 8.0), 0.0], opts={'w': 4.4, 'd': 4.4, 'h': 9.2, 'color': '#EFE6D2'}), P('lh18', 'lighthouseLive', pos=[0.0, r(WY18 + 1.2), 0.0], opts={'h': 4.5, 'onAt': 0.0, 'rate': 0.8, 'len': 9.0}),
               *[P(f'rf18{i}', 'zincRoof', pos=[r(17.0 * math.cos(i * 1.05 + 0.4)), r(WY18 + 0.4), r(17.0 * math.sin(i * 1.05 + 0.4))], ry=r(i * 60.0), opts={'w': 5.0}) for i in range(6)],
               BURST('glou18', [-5.0, r(WY18 + 6.0), 4.0], 0.5, 'GLOUGLOU', 3.6, 0.6)],
        cams=[FC(0.0, [0.0, r(WY18 + 50.0), 14.0], [[-13.0, WY18, -12.0], [13.0, WY18, 12.0], [-13.0, WY18, 12.0], [13.0, WY18, -12.0]], top=0.14, bottom=0.8, lenses=range(26, 74))])
st.cue('whoosh', 'S18', 0.05, 0.45, 1.8, 120, 800); st.cue('sfx:gulp', 'S18', 1.2, 0.4)

# 19: in six seconds. Down in the street, drained and dripping: fish flopping on the road, a crab scuttling, the swan pedalo hanging from a street
#     lamp, a duck ring round a tree; the policeman, soaked, still directing the traffic, seaweed on his cap (SIX SECONDES)
D19 = st.dur('S19')
st.shot('S19', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, look={'sat': 0.8}, actors=[
        act('agent', [-0.6, 0, -2.0], 25, 'stand', 'neutral', keys=[k(0.0, look='camera'), *[k(r(0.05 + 0.3 * i), toon=WAVE6(1 if i % 2 else -1), toonDur=0.18, toonEase='inOut') for i in range(5)]])],
        props=[*[P(f'fish19{i}', 'fishFlop', pos=[r(-1.6 + 1.1 * i), 0, r(1.4 - 0.5 * (i % 2))], ry=r(30.0 * i), opts={'s': 0.32, 'rate': r(1.8 + 0.3 * i), 'phase': r(0.27 * i), 'color': ['#9AA7B2', '#F28C28', '#9AA7B2', '#C9B26A'][i]}) for i in range(4)],
               P('crab19', 'crab', pos=[0.0, 0, 0.0], opts={'s': 0.22, 'path': [[0.0, 1.6, 2.2], [D19, 0.6, 2.2]]}),
               P('lamp19', 'streetLamp', pos=[3.6, 0, -3.0]), P('ped19', 'pedalo', pos=[3.4, 3.2, -3.0], rot=[0.0, 0.6, 0.35]),
               P('cap19', 'copCap', on={'actor': 'agent', 'joint': 'head', 'offset': [0.0, 0.31, 0.0]}), P('weed19', 'seaweed', on={'actor': 'agent', 'joint': 'head', 'offset': [0.05, 0.4, 0.0]}, scale=0.25),
               P('puddle19', 'meltPuddle', pos=[0.4, 0.01, 0.6], scale=3.0)],
        cams=[FC(0.0, [1.2, 1.2, 6.2], [[-0.6, 2.6, -2.0], [-1.8, 0.0, 1.6], [2.0, 0.0, 1.6], [3.6, 3.8, -3.0]], top=0.2, bottom=0.8)])
st.cue('sfx:splat', 'S19', 0.15, 0.2); st.cue('sfx:splat', 'S19', 0.55, 0.2); st.cue('sfx:whistle', 'S19', 0.7, 0.15)

# 20: the submarine too. His bathroom, drained: the empty tub, the submarine's tail sticking out of the plughole, its propeller turning; its
#     periscope turns to him; he looks down at it, then at us
D20 = st.dur('S20')
st.shot('S20', 'salleDeBain', setOpts={'half': 3.4}, actors=[act('mec', [0.5, 0, -0.85], 156, 'stand', 'unimpressed', keys=[k(0.0, look=[DRAIN[0], 0.3, DRAIN[2]]), k(0.0, toon={'face': DEAD, 'bend': {'spine': [0.45, 0, 0, 1, None]}}, toonDur=0.0), k(0.65, look='camera'), *BLINK(0.95)])],
        props=[TUBP('tub20', fill=0.0, sub=True, subYaw=[[0.0, -90.0], [0.3, -90.0], [0.5, 35.0]], weed=True, barnacles=True),
               P('plug20', 'bathPlug', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]})],
        cams=[FC(0.0, [1.6, 1.05, -1.5], [[0.5, 2.45, -0.85], [DRAIN[0], 0.2, DRAIN[2]], [r(DRAIN[0] - 0.12), 0.62, r(DRAIN[2] + 0.06)], [0.0, 0.75, RIMZ]], top=0.14, bottom=0.86, inside=BATH)])   # (stills 1) low at the tap end, the tail in front, him over the rim (from inside the tub he was out of the frame)
st.cue('sfx:squeak', 'S20', 0.45, 0.25)

# 21: he got his water bill. On his landing: the postman hands him the bill; it unrolls from his hand down to the floor, across the landing and
#     down the stairs; the postman's eyes follow it down
D21 = st.dur('S21')
st.shot('S21', 'immeubleHall', setOpts={'back': -3.2, 'plant': False}, actors=[
        act('mec', [-0.5, 0, -1.6], 30, 'stand', 'unimpressed', keys=[k(0.0, look=[0.2, 1.3, -1.2]), k(0.0, toon={'reach': {'R': [-0.1, 1.45, -1.25, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0), k(1.0, look='camera'), *BLINK(1.3)]),
        act('facteur', [0.6, 0, -1.2], -60, 'stand', 'neutral', keys=[k(0.0, look=[-0.1, 1.4, -1.25]), k(0.0, toon={'reach': {'R': [0.0, 1.35, -1.2, 1, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.0),
            k(0.35, look=[-0.1, 0.0, -0.4]), k(0.8, look=[0.4, 0.0, 1.6]), k(0.85, toon={'reach': {'R': [0.15, 1.2, -1.0, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'eye': 0.5, 'brow': 0.6}}, toonDur=0.1)])],
        props=[P('bill21', 'billScroll', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, opts={'w': 0.34, 'top': 1.45, 'head': "FACTURE D'EAU", 'items': ['UNE MER', 'UN SOUS-MARIN', 'UN PHARE', 'LES POMPIERS', 'LES BOUÉES', 'UN PÉDALO'],
                    'prices': ['4 000 000 000 €', '820 000 000 €', '12 000 000 €', '3 600 000 €', '48 000 €', '1 200 €'], 'len': [[0.0, 0.3], [0.15, 0.3], [1.2, 4.0]], 'rowsPer': 0.45}),
               P('bag21', 'mailBag', on={'actor': 'facteur', 'joint': 'torso', 'offset': [0.2, 0.4, 0.0]}), P('cap21', 'copCap', on={'actor': 'facteur', 'joint': 'head', 'offset': [0.0, 0.31, 0.0]}, opts={'color': '#2F5E8C'})],
        cams=[FC(0.0, [1.9, 1.5, 2.6], [[-0.5, 2.45, -1.6], [0.6, 2.45, -1.2], [-0.5, 0.0, 1.0], [-0.1, 1.5, -1.25]], top=0.14, bottom=0.8)])
st.cue('sfx:paper', 'S21', 0.15, 0.35); st.cue('sfx:slideDownLong', 'S21', 0.25, 0.25)

# 22: he is contesting it. By his bathtub, sitting on a stool with the bill on his knees: he stamps it, THUNK: CONTESTÉ; looks at us; behind him the
#     tap drips once into the empty tub: plic. The end hold
D22 = st.dur('S22'); STAMP22 = 0.3; DRIP22 = r(D22 - 0.75)
st.shot('S22', 'salleDeBain', setOpts={'half': 3.4}, actors=[act('mec', [-0.2, 0, -0.5], 20, 'sit', 'unimpressed', keys=[k(0.0, look=[-0.15, 0.55, -0.2]),
            k(0.0, toon={'reach': {'R': [-0.12, 0.9, -0.15, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(STAMP22, toon={'reach': {'R': [-0.12, 0.66, -0.13, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'brow': -0.3}}, toonDur=0.06, toonEase='in'),   # THUNK
            k(r(STAMP22 + 0.25), toon={'reach': {'R': [0.15, 0.8, -0.2, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.15), k(r(STAMP22 + 0.35), look='camera'),
            k(r(DRIP22 + 0.15), look=[MOUTH[0], 1.0, MOUTH[2]]), k(r(DRIP22 + 0.55), look='camera'), *BLINK(r(D22 - 0.35))])],
        props=[TUBP('tub22', fill=0.0, drips=[DRIP22]), P('stool22', 'barStool', pos=[-0.2, 0, -0.55], scale=0.75),
               P('bill22', 'waterBill', pos=[-0.15, 0.58, -0.15], rot=[-1.4, 0.0, 0.0], opts={'w': 0.5, 'h': 0.4, 'amount': '4 836 849 200 €', 'stamp': 'CONTESTÉ', 'stampDelay': r(STAMP22 + 1.02), 'popAt': -1.0}),
               P('stamp22', 'bigStamp', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.0]}, scale=0.6)],
        cams=[FC(0.0, [2.1, 1.1, 0.9], [[-0.2, 2.1, -0.5], [-0.2, 0.0, -0.5], [MOUTH[0], 1.1, MOUTH[2]], [-0.9, 0.5, TUB[2]]], top=0.2, bottom=0.74, inside=BATH)])   # from the right: him, the tap behind; (stills 1) kept inside (behind the wall: a peach screen)
st.cue('sfx:stampDown' if False else 'thud', 'S22', STAMP22, 0.35); st.cue('sfx:tick', 'S22', r(DRIP22 + 0.33), 0.35)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le robinet", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'mamie': {'preset': 'mamie', 'seed': 711, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'passant': {'preset': 'boss', 'seed': 712, 'suit': '#5A6470', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'voisin1': {'preset': 'pyjama', 'seed': 713, 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'voisine2': {'preset': 'madame', 'seed': 714, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'pompier1': {'preset': 'pompier', 'seed': 715, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'pompier2': {'preset': 'pompier', 'seed': 716, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'agent': {'preset': 'cop', 'seed': 717, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 718, 'suit': '#2C3440', 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'touriste1': {'preset': 'tourist', 'seed': 719, 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'touriste2': {'preset': 'tourist', 'seed': 720, 'suit': '#3FA7D6', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'marin': {'preset': 'sportif', 'seed': 721, 'suit': '#F4F4F0', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'boulanger': {'preset': 'chef', 'seed': 722, 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'savant1': {'preset': 'savant', 'seed': 723, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 724, 'hairColor': '#8A6A4A', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 725, 'suit': '#4A4D55', 'lapel': '#4A4D55', 'tie': '#9A1F2E', 'hairColor': '#D2D2D2', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'garde1': {'preset': 'officiel', 'seed': 726, 'suit': '#1F2A44', 'lapel': '#1F2A44', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'garde2': {'preset': 'officiel', 'seed': 727, 'suit': '#1F2A44', 'lapel': '#1F2A44', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'facteur': {'preset': 'officiel', 'seed': 728, 'suit': '#2F5E8C', 'lapel': '#2F5E8C', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
