#!/usr/bin/env python3
"""Le poisson rouge (story 65, cycle 27; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man bought a goldfish. The seller said: three grains a day. He gave it three hundred. The next day it needed the bathtub. The day after, the
municipal pool. The town hall closed the pool. The fish moved into the lake. It ate all the pedal boats. The ducks filed a complaint. The judge
sided with the fish. The ducks appealed. The fish ate the courthouse. The army was sent: three tanks, two fighter jets. The fish took them for
grains. The government negotiated. Historic agreement: it got the sea. In exchange it guards the coast, paid three grains a day. The man bought
himself another goldfish. He gives it three hundred.
Staging: a pet shop, the bag handed over the counter; the seller's three grains held up between finger and thumb; at home the box upturned over the
bowl, the flakes piling over the rim, the fish's eyes popping; the fish filling the bathtub, its tail over the rim; filling the municipal pool, the
lifeguard blowing his whistle cheeks out; the mayor's sign PISCINE FERMÉE (FERMÉE); the fish's leap into the lake, a wall of spray; the swan pedal
boats gulped one after the other; three ducks quacking at a gendarme's desk; the judge's gavel, the ducks bowled over; the ducks hopping mad
(APPEL); the courthouse swallowed in one gulp; three tanks rolling, two jets screaming over; gulped like grains, the fish swelling and smiling; the
minister on the jetty talking up to the head; the agreement held up to the flashes (ACCORD); the fish patrolling the coast in a captain's cap;
three grains held up to a mouth the size of a garage; back at the pet shop; the box upturned again, the new fish's eyes popping, a look at us.
Natural look; cycle 27 tools: the fish's gulp clip (jaw, swelling), props_poisson.js (fishBag, fishBowl, grainBox, grains, pool, closedSign,
pedalo, glassTank), face.swell (cheeks blown out), level heads (bend lvl)."""
from story_kit import *
import math

st = Story('poisson', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 22)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3, ink=None: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True, **({'ink': ink} if ink else {})})
GLOW = lambda pid, pos, col='#FFE6B8', k_=2.5, dist=4.0: P(pid, 'glowLight', pos=pos, opts={'color': col, 'k': k_, 'dist': dist})
DEAD = {'lid': 0.45}
FY = lambda S, yc: r(yc - 0.55 * S)                 # the fish's actor height so that its body's middle sits at yc (the swimmer floats 0.55 x its scale up)
SHOP = {'fr': True, 'signs': [['ANIMALERIE', '#2E8C5A', '#FFFFFF', -1.2, -3.85], ['POISSONS', '#F2701E', '#FFFFFF', 1.4, -3.85]]}
LAKE = {'sand': '#8CC56A', 'sea': '#3E9CB8', 'parasols': False}   # a lake: a grassy shore, green-blue water
SEA = {'parasols': False}
HAND = lambda pid, name, who, hand='R', off=(0.0, -0.06, 0.03), **kw: P(pid, name, on={'actor': who, 'hand': hand, 'offset': list(off)}, **kw)
# (review 2) the far shore of the lake: trees and roofs (the lake had the sea's open horizon, so the sea was no upgrade)
SHORE = lambda sid: [P(f'shore{sid}', 'floorSlab', pos=[0.0, 0.0, -95.0], opts={'w': 320.0, 'd': 40.0, 'h': 0.6, 'color': '#7DBA5A'}),
                     *[P(f'tr{sid}{i}', 'tree', pos=[r(-110.0 + 18.0 * i + 5.0 * ((i * 7) % 3)), 0.6, r(-80.0 - 6.0 * (i % 3))], scale=4.0, opts={'seed': i + 4}) for i in range(13)],
                     *[P(f'ho{sid}{i}', 'cottage', pos=[r(-60.0 + 30.0 * i), 0.6, -86.0], scale=2.4, opts={'seed': i + 2}) for i in range(5)]]
XLOOK = {'sat': 0.8}   # (review 1) the exteriors graded down: saturation 156-216 against 112-157 indoors and 100-145 in the series' reference
GULP = lambda **p: {'open': 0.28, 'hold': 0.12, 'snap': 0.05, **p}   # (review 1) the gulp's beats as clip params: jaws wide held, a two-frame snap, the swell

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.5, 'mec', 'bag'), ('S03', 1.1, 'mec', 'pour'), ('S04', 1.2, 'poisson', 'tub'), ('S05', 1.2, 'nageur', 'whistle'), ('S08', 1.0, 'poisson', 'pedalo'),
           ('S10', 0.9, 'juge', 'gavel'), ('S12', 1.0, 'poisson', 'court'), ('S15', 1.0, 'poisson', 'gulp'), ('S17', 1.2, 'ministre', 'deal'), ('S21', 1.6, 'mec', 'end')]:
    st.gag(*g_)
st.card('S06', 'FERMÉE', at=0.55)
st.card('S11', 'APPEL', at=0.35)
st.card('S17', 'ACCORD', at=0.5)

# 1: the hook. A pet shop: aquariums along the wall, the counter; the seller hands him a bag with a goldfish across the counter; he holds it up beside
#    his face and looks at us, deadpan; the fish goes round in the bag
D1 = st.dur('S01'); TAKE1 = 0.7
ME1 = [-0.75, 0, -0.9]; VE1 = [0.55, 0, -1.55]
st.shot('S01', 'supermarket', setOpts=SHOP, actors=[
        act('mec', ME1, 62, 'stand', 'neutral', keys=[k(0.0, look=[VE1[0], 1.9, VE1[2]]), k(r(TAKE1 - 0.25), toon={'reach': {'R': [-0.15, 1.25, -1.2, 1, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.2, toonEase='inOut'),
            k(TAKE1, toon={'reach': {'R': [-0.15, 1.25, -1.2, 1, 0.03]}, 'hands': {'R': 'grip'}}, toonDur=0.05),
            k(r(TAKE1 + 0.3), look='camera'), k(r(TAKE1 + 0.32), toon={'touch': {'R': ['face', -0.32, 0.12, 0.12, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.25, toonEase='inOut')]),   # the bag up beside his face, a look to us
        act('vendeur', VE1, -60, 'stand', 'happy', keys=[k(0.0, look=[ME1[0], 1.9, ME1[2]]), k(0.0, toon={'reach': {'R': [-0.1, 1.3, -1.25, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'smile'}}, toonDur=0.0),
            k(r(TAKE1 + 0.05), toon={'reach': {'R': [0.15, 1.15, -1.3, 0, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'smile'}}, toonDur=0.25, toonEase='inOut')])],
        props=[P('cnt1', 'table', pos=[-0.05, 0, -1.55], opts={'w': 1.6, 'd': 0.6, 'h': 1.0, 'color': '#C9A06A'}), P('till1', 'cashRegister', pos=[0.45, 1.0, -1.65], ry=-20, opts={'text': '3,50'}),
               *[P(f'aq1{j}', 'aquarium', pos=[r(-2.4 + 1.6 * j), 0, -3.55], opts={'w': 1.3}) for j in range(4)],
               P('bag1', 'fishBag', on={'actor': 'vendeur', 'hand': 'R', 'offset': [0.0, -0.02, 0.0]}, opts={'s': 1.5}, keys=[k(TAKE1, attach='mec', hand='R', offset=[0.0, -0.02, 0.0], face='camera')])],
        cams=[FC(0.0, [0.0, 1.55, 3.0], [[ME1[0], 2.45, ME1[2]], [r(VE1[0] + 0.45), 2.45, VE1[2]], [ME1[0], 0.55, ME1[2]], [r(VE1[0] + 0.45), 0.9, VE1[2]], [-1.15, 1.9, -0.9]], top=0.16, bottom=0.76, drift=(0.1, 0.0, -0.12)),
              FC(1.0, [0.66, 1.9, -0.15], [[ME1[0], 2.5, ME1[2]], [ME1[0], 1.4, ME1[2]], [-0.94, 1.95, -0.55], [-0.56, 1.95, -1.25]], top=0.16, bottom=0.74)])   # (review 1) cut in on him and the bag by his face: the fish never read in it
st.cue('sfx:ding', 'S01', 0.1, 0.12); st.cue('sfx:splash', 'S01', r(TAKE1 + 0.3), 0.12)

# 2: the seller said: three grains a day. Close on the seller: he holds three grains up between finger and thumb, very serious, a finger wagging;
#    his other hand up three fingers' worth; the man's head in the foreground, his eyes on the grains
D2 = st.dur('S02'); TROIS2 = st.at('S02', 'L02', 5); GR2 = [0.15, 1.02, -1.4]
POINT2 = lambda x, y, eye=0.0: {'reach': {'R': [r(0.68 + x), r(1.68 + y), -1.62, 1, 0.03], 'L': [r(GR2[0] + 0.05), 1.2, GR2[2], 1, 0.03]}, 'hands': {'R': 'point', 'L': 'point'}, 'face': {'brow': -0.6, 'lid': 0.0, 'eye': eye}}   # (review 2) the index up beside his head, against the wall (skin on skin it was lost)
st.shot('S02', 'supermarket', setOpts=SHOP, actors=[
        act('vendeur', VE1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=POINT2(0.3, 0.22), toonDur=0.0),
            k(r(TROIS2 - 0.12), toon=POINT2(0.3, 0.34, 0.25), toonDur=0.1, toonEase='out'),   # (review 1) on « trois »: the index up, eyes wide; the other hand points at the grains
            *[k(r(TROIS2 + 0.12 + 0.14 * j), toon=POINT2(r(0.3 + 0.07 * (1 if j % 2 else -1)), 0.34, 0.25), toonDur=0.07) for j in range(6)]]),   # the finger wags: three, not one more
        act('mec', ME1, 62, 'stand', 'neutral', keys=[k(0.0, look=GR2), k(0.0, toon={'face': {'lid': 0.4, 'gy': 0.4}}, toonDur=0.0)])],
        props=[P('cnt2', 'table', pos=[-0.05, 0, -1.55], opts={'w': 1.6, 'd': 0.6, 'h': 1.0, 'color': '#C9A06A'}), *[P(f'aq2{j}', 'aquarium', pos=[r(-2.4 + 1.6 * j), 0, -3.55], opts={'w': 1.3}) for j in range(4)],
               P('sau2', 'slab', pos=[GR2[0], 1.0, GR2[2]], opts={'w': 0.34, 'h': 0.02, 'd': 0.26, 'color': '#FFFFFF'}), P('gr2', 'grains', pos=[GR2[0], 1.05, GR2[2]], opts={'n': 3, 's': 3.0, 'color': '#8A5A32'})],
        cams=[FC(0.0, [0.1, 1.3, -0.5], [list(GR2), [VE1[0], 2.5, VE1[2]], [VE1[0], 1.35, VE1[2]], [0.95, 2.3, -1.4]], top=0.14, bottom=0.78, lenses=range(30, 70))])   # (review 1) low over the counter, the grains big in front: an open palm read as a wave
st.cue('sfx:pop', 'S02', TROIS2, 0.15)

# 3: he gave it three hundred. At home: the fishbowl on a little table; he upturns a whole box of grains over it: a stream of flakes that piles up into
#    a mound over the rim; the fish's eyes pop out
D3 = st.dur('S03'); POUR3 = [0.12, r(D3 - 0.2)]
BOWL3 = [0.35, 0.72, -1.2]; ME3 = [-0.18, 0, -1.68]   # (audit) behind the bowl at three-quarters, his face to us (side on, a box head reads as the back of the head)
st.shot('S03', 'livingRoom', setOpts={'sofa': False, 'plant': False}, actors=[
        act('mec', ME3, 40, 'stand', 'unimpressed', keys=[k(0.0, look=[BOWL3[0], 0.9, BOWL3[2]]), k(0.0, toon={'reach': {'R': [r(BOWL3[0] - 0.05), 1.42, r(BOWL3[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.45, 'gy': 0.4}}, toonDur=0.0),
            k(r(D3 - 0.45), look='camera'), k(r(D3 - 0.42), toon={'reach': {'R': [r(BOWL3[0] - 0.05), 1.42, r(BOWL3[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.15)])],   # a look to us, still pouring
        props=[P('tab3', 'table', pos=[BOWL3[0], 0, BOWL3[2]], opts={'w': 0.6, 'd': 0.6, 'h': 0.72}),
               P('bowl3', 'fishBowl', pos=BOWL3, opts={'r': 0.2, 'flakes': [POUR3[0], POUR3[1], 160], 'pour': 0.5, 'popAt': r(D3 - 0.4)}),
               P('box3', 'grainBox', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.06]}, rot=[0.0, 0.0, 2.3], scale=1.2)],   # upturned
        cams=[FC(0.0, [-0.9, 1.35, 1.0], [[ME3[0], 2.45, ME3[2]], [BOWL3[0], 0.6, BOWL3[2]], [ME3[0], 1.0, ME3[2]], [r(BOWL3[0] + 0.3), 1.3, BOWL3[2]]], top=0.16, bottom=0.76)])
st.cue('sfx:crunch', 'S03', 0.15, 0.18); st.cue('sfx:crunch', 'S03', 0.55, 0.15); st.cue('sfx:boing', 'S03', r(D3 - 0.4), 0.25)

# 4: the next day it needed the bathtub. The bathroom: the goldfish fills the tub, its back out of the water, its head over one end and its tail
#    flopping over the other; he stands beside it with the box, deadpan
D4 = st.dur('S04'); S4 = 3.4; TUB4 = [0.0, 0, -2.4]   # (review 1) a claw-foot tub with taps and water, big enough for the fish: its fins cut through the box tub
st.shot('S04', 'laundryRoom', setOpts={'washer': False}, actors=[
        act('poisson', [0.12, FY(S4, 0.86), TUB4[2]], 90, 'walk', 'happy', scale=S4, keys=[k(0.0, look='camera')]),   # swimming on the spot, its tail swishing over the rim
        act('mec', [1.45, 0, -1.65], -35, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(0.55, toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.07), k(0.68, toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.1),
            k(1.15, look=[0.6, 1.3, TUB4[2]]), k(1.6, look='camera')])],   # a glance down at the fish, back to us
        props=[P('tub4', 'clawTub', pos=TUB4, opts={'w': 2.1, 'd': 1.05, 'h': 0.62}), P('box4', 'grainBox', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.06]}, scale=1.2),
               P('spl4a', 'waterDrops', pos=[-1.15, 0.8, TUB4[2]], opts={'at': 0.3, 'n': 16, 'r': 0.04, 'speed': 2.6, 'dir': [0, 1, 0.3]}), P('spl4b', 'waterDrops', pos=[-1.15, 0.8, TUB4[2]], opts={'at': 1.25, 'n': 12, 'r': 0.035, 'speed': 2.2, 'dir': [0, 1, 0.3]})],
        cams=[FC(0.0, [0.9, 1.45, 2.6], [[-1.35, 0.85, TUB4[2]], [1.3, 0.85, TUB4[2]], [0.12, 1.75, TUB4[2]], [0.0, 0.0, r(TUB4[2] + 0.6)], [1.45, 2.45, -1.65], [1.45, 0.3, -1.65]], top=0.16, bottom=0.78)])
st.cue('sfx:splash', 'S04', 0.3, 0.2); st.cue('sfx:splash', 'S04', 1.25, 0.15)

# 5: the day after, the municipal pool. The open-air pool: the fish fills the basin, its back out like an island, the water heaving; the lifeguard on
#    the deck blows his whistle, cheeks blown out; the man on the edge with his box
D5 = st.dur('S05'); S5 = 19.0; POOL = [0.0, 0.2, -6.0]; GUARD5 = [3.6, 0.2, -1.0]
WHIS = lambda w: {'touch': {'R': ['face', 0.0, 0.13, 0.12, 1, 0.02]}, 'hands': {'R': 'pinch'}, 'scl': {'head': [r(1 + 0.1 * w), r(1 + 0.06 * w), r(1 + 0.1 * w)]}, 'face': {'mouth': 'kiss', 'swell': r(1.2 * w), 'puff': r(w), 'cheeks': r(w), 'eye': r(0.45 * w), 'lid': 0.0, 'brow': 0.8}}
st.shot('S05', 'grassland', look=XLOOK, actors=[
        act('poisson', [0.0, FY(S5, 0.4), -5.6], 160, 'walk', 'happy', scale=S5, keys=[k(0.0, look=[2.0, 2.0, 4.0])]),
        act('nageur', GUARD5, 20, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=WHIS(0.0), toonDur=0.0),
            *[kk for j in range(3) for kk in (k(r(0.2 + 0.4 * j), toon=WHIS(r(0.65 + 0.2 * j)), toonDur=0.07, toonEase='out'), k(r(0.42 + 0.4 * j), toon=WHIS(0.0), toonDur=0.12, toonEase='in'))]])],   # (review 2) three blasts, each bigger, a full deflate between (it read as one held puff)
        props=[P('pool5', 'pool', pos=POOL, opts={'w': 6, 'l': 12, 'deck': 3, 'waves': 3}), HAND('whis5', 'whistle', 'nageur', off=(0.0, 0.0, 0.04))],
        cams=[FC(0.0, [5.0, 1.55, 1.9], [[GUARD5[0], 2.5, GUARD5[2]], [GUARD5[0], 1.2, GUARD5[2]], [0.0, 4.6, -5.6], [-3.0, 0.2, -11.5], [3.0, 0.2, -11.5]], top=0.14, bottom=0.78, lenses=range(26, 70))])
for j_ in range(3): st.cue('sfx:whistle', 'S05', r(0.2 + 0.4 * j_), 0.3)

# 6: the town hall closed the pool. At the gate of the pool the mayor sets down a folding sign PISCINE FERMÉE, pleased with himself; behind him the
#    fish's eye over the edge of the basin, on the sign (FERMÉE)
D6 = st.dur('S06'); SIGN6 = 0.45; SG6 = [0.35, 0.2, 2.75]
st.shot('S06', 'grassland', look=XLOOK, actors=[
        act('poisson', [0.6, FY(S5, -1.0), -6.8], 180, 'idle', 'neutral', scale=S5, keys=[k(0.0, look=[0.0, 1.0, 3.0])]),
        act('maire', [-0.75, 0.2, 2.45], 25, 'stand', 'happy', keys=[k(0.0, look=[0.3, 1.2, 2.75]),
            k(0.0, toon={'bend': {'spine': [0.12, 0, 0, 1, None]}, 'reach': {'R': [0.3, 1.82, 2.75, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'smirk', 'lid': 0.2}}, toonDur=0.0),
            k(r(SIGN6 - 0.02), toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'reach': {'R': [0.3, 1.47, 2.75, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'smirk', 'lid': 0.0}}, toonDur=0.08, toonEase='in'),   # (review 1) he plants it: down onto its legs
            k(r(SIGN6 + 0.25), toon={'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': {'mouth': 'smirk', 'lid': 0.3}}, toonDur=0.2, toonEase='out'), k(r(SIGN6 + 0.35), look='camera'),
            k(r(SIGN6 + 0.5), toon={'touch': {'R': ['torso', 0.0, 0.5, 0.25, 1, 0.03], 'L': ['torso', 0.0, 0.52, 0.27, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'mouth': 'smirk', 'lid': 0.3}}, toonDur=0.2)])],   # hands folded, satisfied
        props=[P('pool6', 'pool', pos=POOL, opts={'w': 6, 'l': 12, 'deck': 3, 'waves': 1.5}),
               P('sign6', 'closedSign', pos=[SG6[0], 0.55, SG6[2]], ry=-10, rot=[0.0, 0.0, 0.12], opts={'text': 'INTERDIT|AUX POISSONS', 'icon': 'noFish', 'w': 0.8, 'h': 1.0},
                 keys=[k(r(SIGN6 - 0.1), to=SG6, dur=0.1, ease='in'), k(r(SIGN6 - 0.1), rotTo=[0.0, -0.17, 0.0], dur=0.1, ease='in'), k(SIGN6, rotTo=[0.06, -0.17, -0.04], dur=0.06, ease='out'), k(r(SIGN6 + 0.06), rotTo=[0.0, -0.17, 0.0], dur=0.12, ease='inOut')])],
        cams=[FC(0.0, [0.6, 1.5, 7.8], [[-1.15, 2.5, 2.45], [-1.15, 0.2, 2.45], [0.8, 1.5, 2.75], [0.6, 3.0, -6.8]], top=0.22, bottom=0.78)])   # (needs the user, decided) the sign says INTERDIT AUX POISSONS with a crossed-out goldfish: FERMÉE was on screen three times at once (card, sign, caption)
st.cue('thud', 'S06', SIGN6, 0.3)

# 7: the fish moved into the lake. The lakeside: the fish shoots up out of the water in a high arc and dives back in: a wall of spray; a duck on the water
#    bobs in the wave
D7 = st.dur('S07'); S7 = 26.0; LEAP7 = [0.0, 0.95]; DUCK7 = [4.6, 0.05, 9.2]
SQ7 = lambda sq, lay: {'sq': sq, 'lay': lay}
st.shot('S07', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[
        act('poisson', [-9.0, FY(S7, -9.0), -28.0], 90, 'walk', 'happy', scale=S7, keys=[
            k(0.0, to=[0.0, FY(S7, 10.0), -26.0], dur=0.45, ease='out', face='keep'), k(0.45, to=[8.0, FY(S7, -9.0), -24.0], dur=0.5, ease='in', face='keep'),   # up and over, into the lake
            k(0.0, toon=SQ7([1.22, 1.22, 0.72], [-0.45, 0.0]), toonDur=0.0),   # (review 1) the take-off: squashed...
            k(0.06, toon=SQ7([0.84, 0.84, 1.38], [-0.6, 0.0]), toonDur=0.1, toonEase='out'),   # ...stretched as it shoots up...
            k(0.36, toon=SQ7([1.0, 1.0, 1.0], [0.0, 0.0]), toonDur=0.14, toonEase='inOut'),   # ...round at the top of the arc...
            k(0.62, toon=SQ7([0.88, 0.88, 1.28], [0.75, 0.0]), toonDur=0.2, toonEase='in')]),   # ...stretched again, nose down into the dive
        act('can1', DUCK7, 200, 'idle', 'neutral', scale=1.6, keys=[k(0.0, look=[-2.0, 6.0, -26.0]), k(0.25, look=[-2.0, 18.0, -26.0]), k(0.6, look=[10.0, 4.0, -24.0]),
            k(r(LEAP7[1] + 0.12), to=[DUCK7[0], 0.6, DUCK7[2]], dur=0.18, ease='out'), k(r(LEAP7[1] + 0.3), to=DUCK7, dur=0.3, ease='inOut')])],   # (review 1) the duck close in front for scale, its head following the leap
        props=[P('spl7a', 'waterDrops', pos=[-8.0, 0.0, -28.0], opts={'at': 0.02, 'n': 40, 'r': 0.45, 'speed': 9.0, 'spread': 0.35, 'dir': [0, 1, 0.1], 'life': 0.9, 'color': '#F4FBFF'}), P('spl7', 'waterDrops', pos=[8.0, 0.0, -23.0], opts={'at': r(LEAP7[1] - 0.02), 'n': 90, 'r': 0.6, 'speed': 14.0, 'spread': 0.3, 'dir': [0, 1, 0.05], 'life': 1.0, 'color': '#F4FBFF'}), *SHORE('7')],
        cams=[FC(0.0, [6.0, 1.3, 12.5], [[-10.0, 0.0, -26.0], [10.0, 0.0, -24.0], [0.0, 17.0, -26.0], list(DUCK7)], top=0.14, bottom=0.8, lenses=range(26, 70))])   # (review 2) the take-off inside the frame (it was cut at the left edge)
st.cue('whoosh', 'S07', 0.05, 0.3, 0.6, 200, 900); st.cue('sfx:splash', 'S07', 0.02, 0.3); st.cue('sfx:splash', 'S07', LEAP7[1], 0.5)

# 8: it ate all the pedal boats. On the lake a row of swan pedal boats; the fish's head comes up behind them and gulps them one after the other: gone,
#    gone, gone; GLOUPS
D8 = st.dur('S08'); S8 = 26.0; EAT8 = [0.3, 0.62, 0.94, 1.26]
PED8 = [[-3.6, 0.0, -6.4], [-1.2, 0.0, -6.4], [1.2, 0.0, -6.4], [3.6, 0.0, -6.4]]
MOUTH8 = r(0.215 * S8 - 0.2)   # from its root to the middle of its open mouth at the end of the lunge: the lips close round each boat
X8 = lambda t: r(PED8[0][0] - MOUTH8 + 7.5 * (t - EAT8[0]))   # its head along the row at 7.5 m/s: the mouth on boat j at EAT8[j]
st.shot('S08', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[
        act('poisson', [X8(0.0), FY(S8, 2.4), -6.4], 90, 'walk', 'happy', scale=S8, keys=[k(0.0, to=[X8(D8), FY(S8, 2.4), -6.4], dur=D8, ease='linear'),
            *[k(r(t_ - 0.14), clip='gulp', params=GULP(open=0.1, hold=0.04, snap=0.04, jaw=0.95, drop=0.5, mouth=1.35, lunge=0.25, swell=0.4)) for t_ in EAT8]])],   # (review 1) a nip per boat, the lips round it, in profile (they vanished behind a head whose mouth never showed)
        props=[*[P(f'ped8{j}', 'pedalo', pos=p_, ry=90, opts={'seed': j, 'goneAt': r(EAT8[j] + 0.03), 'suck': [0.0, 0.4, -0.9]}) for j, p_ in enumerate(PED8)],
               *[BURST(f'miam8{j}', [r(PED8[j][0] - 0.6), 5.2, -1.8], r(EAT8[j] + 0.04), 'MIAM', 1.3, 0.28) for j in range(4)], *SHORE('8')],   # a small MIAM per boat; (review 2) in front of the head (inside it, they never showed)
        cams=[FC(0.0, [-2.4, 1.3, 7.0], [[-4.6, 0.0, -6.4], [1.8, 0.0, -6.4], [-4.0, 8.6, -6.4], [-1.0, 0.0, -6.4]], top=0.16, bottom=0.8, drift=(4.2, 0.0, 0.0), lenses=range(26, 66))])   # side on, panning with its head along the row
for t_ in EAT8: st.cue('sfx:gulp', 'S08', r(t_ + 0.03), 0.25)

# 9: the ducks filed a complaint. The gendarmerie: three ducks stand on the desk quacking at the gendarme, wings flapping; he types, deadpan
D9 = st.dur('S09'); DESK9 = [-4.6, 0, -1.4]
TYPE9 = lambda j: {'reach': {'L': [-4.8, r(0.86 + 0.06 * (j % 2)), -1.55, 1, 0.03], 'R': [-4.4, r(0.92 - 0.06 * (j % 2)), -1.55, 1, 0.03]}, 'hands': {'L': 'point', 'R': 'point'}, 'bend': {'neck': [r(0.06 * (j % 2)), 0, 0, 1, None]}, 'face': {'lid': 0.5}}
st.shot('S09', 'office', actors=[
        act('flic', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 1.1, -1.2]), k(0.0, toon=TYPE9(0), toonDur=0.0), *[k(r(0.1 + 0.12 * j), toon=TYPE9(j + 1), toonDur=0.05) for j in range(12)]]),   # (review 1) two fingers typing, the head nodding with each key (it did not read)
        *[act(f'can{j + 1}', [[-5.3, -4.95, -3.95][j], 0.78, -1.0], [150, 170, 210][j], 'talk', 'angry', scale=1.5, keys=[k(0.0, look=[-4.6, 1.6, -2.1]),
            *[kk for i_ in range(4) for kk in (k(r(0.08 + 0.36 * i_ + 0.11 * j), to=[[-5.3, -4.95, -3.95][j], 0.98, -1.0], dur=0.08, ease='out', face='keep'), k(r(0.16 + 0.36 * i_ + 0.11 * j), to=[[-5.3, -4.95, -3.95][j], 0.78, -1.0], dur=0.08, ease='in', face='keep'))]]) for j in range(3)]],   # beaks clacking, hopping in turn; (review 2) to the sides of him
        props=[P('desk9', 'desk', pos=DESK9, opts={'w': 1.6}), P('pc9', 'laptop', pos=[-4.6, 0.76, -1.6], ry=180),
               P('sign9', 'signBoard', pos=[-4.6, 0, -3.45], opts={'text': 'GENDARMERIE', 'w': 1.45, 'h': 0.36, 'height': 2.2, 'bg': '#1F3B73', 'fg': '#FFFFFF', 'frame': '#F4F4F0', 'posts': False}),
               P('flag9', 'regionFlag', pos=[-5.75, 0, -2.9], opts={'kind': 'fr'}), P('clock9', 'wallClock', pos=[-3.3, 2.35, -3.47], opts={'rate': 0.0})],   # (review 1) the sign, a tricolour and a clock on a bare wall
        cams=[FC(0.0, [-4.3, 1.6, 1.1], [[-5.5, 1.5, -1.0], [-3.75, 1.5, -1.0], [-4.6, 2.65, -3.45], [-4.6, 0.6, -1.0]], top=0.14, bottom=0.76)])   # (review 2) higher, the ducks to the sides: his face and hands clear
st.cue('sfx:cluck', 'S09', 0.1, 0.3); st.cue('sfx:cluck', 'S09', 0.5, 0.3); st.cue('sfx:cluck', 'S09', 0.9, 0.3)

# 10: the judge sided with the fish. The courtroom: the judge brings his gavel down, BANG; the three ducks at the plaintiffs' bench are bowled over,
#     feet in the air
D10 = st.dur('S10'); BANG10 = st.at('S10', 'L10', 6)
st.shot('S10', 'courtroom', actors=[
        act('juge', [0.0, 0.3, -4.0], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.35, 2.15, -3.35, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.35}}, toonDur=0.0),
            k(r(BANG10 - 0.25), toon={'reach': {'R': [0.4, 2.6, -3.4, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'brow': -0.4}}, toonDur=0.18, toonEase='out'),   # up...
            k(BANG10, toon={'reach': {'R': [0.4, 1.5, -3.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.0, 'brow': -0.6, 'mouth': 'open'}}, toonDur=0.05, toonEase='in'),   # ...BANG
            k(r(BANG10 + 0.2), toon={'reach': {'R': [0.4, 1.55, -3.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.35}}, toonDur=0.15)]),
        *[act(f'can{j + 1}', [r(-2.0 + 0.45 * j), 0.78, -1.5], 150, 'talk', 'angry', scale=1.3, keys=[k(0.0, look=[0.0, 2.2, -4.0]), k(r(BANG10 + 0.03 + 0.05 * j), clip='flee'),
            k(r(BANG10 + 0.03 + 0.05 * j), toon={'lay': [-1.5, r(0.35 * (j - 1))], 'sq': [1.1, 0.9, 1.1]}, toonDur=0.1, toonEase='out'),   # (review 1) bowled over one after the other by the shock wave, feet kicking (their heads never moved)
            k(r(BANG10 + 0.03 + 0.05 * j), to=[r(-2.1 + 0.45 * j), 0.98, -1.25], dur=0.08, ease='out'), k(r(BANG10 + 0.11 + 0.05 * j), to=[r(-2.15 + 0.45 * j), 0.8, -1.15], dur=0.1, ease='in')]) for j in range(3)]],
        props=[HAND('gav10', 'gavel', 'juge', off=(0.0, -0.02, 0.05)), P('desk10', 'desk', pos=[-1.55, 0, -1.5], ry=40, opts={'w': 1.8}), BURST('bang10', [-0.25, 2.65, -3.0], BANG10, 'BANG !', 0.9, 0.22)],
        cams=[FC(0.0, [-1.6, 1.45, 1.6], [[0.0, 2.75, -4.0], [-2.3, 0.75, -1.5], [-0.9, 1.6, -1.5], [0.6, 1.3, -3.3]], top=0.16, bottom=0.76)])   # (review 1) nearer the ducks, the judge behind them
st.cue('clang', 'S10', BANG10, 0.4); st.cue('sfx:cluck', 'S10', r(BANG10 + 0.1), 0.25)

# 11: the ducks appealed. Close on the three ducks back on their feet, hopping mad, quacking up at the bench (APPEL)
D11 = st.dur('S11')
HOP11 = lambda j, x: [kk for i_ in range(3) for kk in (k(r(0.28 + 0.36 * i_ + 0.09 * j), to=[x, 1.06, r(0.85 - 0.08 * i_)], dur=0.1, ease='out', face='keep'), k(r(0.38 + 0.36 * i_ + 0.09 * j), to=[x, 0.78, r(0.8 - 0.08 * i_)], dur=0.1, ease='in', face='keep'),
        k(r(0.48 + 0.36 * i_ + 0.09 * j), toon={'sq': [1.25, 0.75, 1.25]}, toonDur=0.03, toonEase='out'), k(r(0.53 + 0.36 * i_ + 0.09 * j), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.08))]
st.shot('S11', 'courtroom', actors=[*[act(f'can{j + 1}', [r(-3.7 + 0.45 * j), 0.78, 0.9], 180, 'talk', 'angry', scale=1.3, keys=[k(0.0, look=[0.0, 2.2, -4.0]),
            k(0.0, toon={'sq': [1.45, 0.3, 1.45]}, toonDur=0.0), k(r(0.08 + 0.05 * j), toon={'sq': [0.82, 1.28, 0.82]}, toonDur=0.1, toonEase='out'), k(r(0.2 + 0.05 * j), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.1, toonEase='inOut'),   # (review 1) flat from the gavel, they pop back up...
            *HOP11(j, r(-3.7 + 0.45 * j))]) for j in range(3)]],   # ...and hop, beaks open, straight at the bench: seen from it (a back view, beaks shut)
        props=[P('desk11', 'desk', pos=[-3.3, 0, 1.0], opts={'w': 1.8})],
        cams=[FC(0.0, [-3.3, 1.2, -0.6], [[-4.0, 1.4, 0.9], [-2.55, 1.4, 0.9], [-3.3, 0.72, 0.9]], top=0.26, bottom=0.74)])   # (stills 3) pushed in: their heads are at 1.3 m, two thirds of the frame was wall
st.cue('sfx:cluck', 'S11', 0.05, 0.35); st.cue('sfx:cluck', 'S11', 0.4, 0.35); st.cue('sfx:cluck', 'S11', 0.8, 0.35)

# 12: the fish ate the courthouse. The courthouse on the lakeshore; the giant fish rears up out of the lake behind it, jaws wide, and swallows it in one
#     gulp; it swells, satisfied
D12 = st.dur('S12'); S12 = 62.0; SNAP12 = 0.8; TRIB = [0.0, 0.0, 9.0]
st.shot('S12', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[
        act('poisson', [0.0, FY(S12, -14.0), -26.0], 0, 'idle', 'neutral', scale=S12, keys=[
            k(0.0, to=[0.0, FY(S12, 5.5), -7.5], dur=0.5, ease='out', face='keep'),   # rearing up behind the courthouse, the jaws opening...
            k(0.62, to=[0.0, FY(S12, 5.0), -3.0], dur=0.18, ease='in', face='keep'),   # ...held wide over it, then down onto it...
            k(0.86, to=[0.0, FY(S12, 4.6), -3.8], dur=0.5, ease='out', face='keep'),   # ...(review 2) and stays, face to us, swelling (the move back turned it round: its back and a fin like a plank)
            k(0.05, clip='gulp', params=GULP(open=0.42, hold=0.33, snap=0.05, jaw=1.2, drop=0.6, mouth=1.6, grow=0.12, lunge=0.0, swell=1.6, wobble=1, bliss=0.85))])],   # (review 1) the jaws twice the building's width for ten frames, a two-frame snap, the body swelling past round, wobbling
        props=[P('trib12', 'townHall', pos=TRIB, opts={'text': 'TRIBUNAL', 'w': 5}, keys=[k(r(SNAP12 + 0.03), visible=False)]),
               BURST('glo12', [7.0, 8.0, 6.0], r(SNAP12 + 0.05), 'GLOUPS !', 5.5, 0.4), *SHORE('12')],
        cams=[FC(0.0, [11.0, 2.2, 30.0], [[-2.8, 0.0, TRIB[2]], [2.8, 0.0, TRIB[2]], [0.0, 22.0, -7.5], [-7.0, 0.0, -7.5], [7.0, 0.0, -7.5], [0.0, 6.0, 8.0]], top=0.12, bottom=0.8, lenses=range(26, 64))])   # three-quarters: the open jaws over the building (in front, it hid the mouth); (stills 3) its face after the snap in the frame
st.cue('sfx:gulp', 'S12', r(SNAP12 + 0.03), 0.5)

# 13: the army was sent. A country road to the lake: three tanks rolling toward us in a line, dust behind them
D13 = st.dur('S13'); TK13 = lambda j: [r(-2.0 + 2.0 * j), 0, r(-24.0 - 8.0 * j)]
st.shot('S13', 'grassland', look=XLOOK, actors=[],
        props=[P('road13', 'roadStrip', pos=[0.0, 0.0, -40.0], opts={'len': 140, 'w': 8}),
               *[P(f'tank13{j}', 'armyTank', pos=TK13(j), ry=0, scale=5.0, keys=[k(0.0, to=[TK13(j)[0], 0, r(TK13(j)[2] + 11.0)], dur=D13, ease='linear'),
                   *[k(r(0.1 * j + 0.3 * i_), rotTo=[0.035 if i_ % 2 else -0.025, 0.0, 0.0], dur=0.3, ease='inOut') for i_ in range(5)]]) for j in range(3)],   # (review 1) on a road, barrels at us, rocking on their tracks (they drove backwards: no barrels)
               *[P(f'dust13{j}', 'dustPuff', pos=[TK13(j)[0], 0, r(TK13(j)[2] - 2.6)], scale=3.5, opts={'period': 0.45, 'seed': 30 + j, 'color': '#D9CDB0'}, keys=[k(0.0, to=[TK13(j)[0], 0, r(TK13(j)[2] + 8.4)], dur=D13, ease='linear')]) for j in range(3)]],
        cams=[FC(0.0, [-0.9, 0.7, -8.6], [[-3.6, 0.0, -13.5], [-0.4, 0.0, -13.5], [-2.0, 3.6, -13.5], [2.0, 0.0, -30.0]], top=0.3, bottom=0.82, lenses=range(26, 64))])   # (stills 3) nearer; (review 2) low on the road, the lead tank at the lens (9 % of the frame under empty sky)
st.cue('sfx:engine', 'S13', 0.0, 0.45)

# 14: three tanks, two fighter jets. On the lakeshore the three tanks aim their guns at the water; two jets scream in low overhead toward the lake, where
#     the fish's head waits
D14 = st.dur('S14'); S14 = 62.0
st.shot('S14', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[act('poisson', [0.0, FY(S14, 2.0), -16.0], 0, 'idle', 'neutral', scale=S14, keys=[k(0.0, look=[0.0, 2.0, 10.0]), k(0.0, clip='idle', params={'blinks': [0.42, 1.5, 1.66]})])],
        props=[*[P(f'tank14{j}', 'armyTank', pos=[r(-5.0 + 5.0 * j), 0.0, 9.0], ry=180, scale=5.0, keys=[k(r(0.3 + 0.2 * j), rotTo=[-0.04, 0.0, 0.0], dur=0.08, ease='out'), k(r(0.38 + 0.2 * j), rotTo=[0.0, 0.0, 0.0], dur=0.2, ease='inOut')]) for j in range(3)],
               *[P(f'jet14{j}', 'fighterJet', pos=[r(-6.0 + 12.0 * j), 14.0, 40.0], ry=180, opts={'burner': 1.0}, keys=[k(0.0, to=[r(-4.0 + 8.0 * j), 10.0, -6.0], dur=D14, ease='linear')]) for j in range(2)]],
        cams=[FC(0.0, [7.0, 1.4, 24.0], [[-8.0, 0.0, 9.0], [8.0, 0.0, 9.0], [0.0, 17.0, -16.0], [-8.0, 0.0, -10.0], [8.0, 0.0, -10.0]], top=0.14, bottom=0.8, lenses=range(26, 70))])   # (review 1) the head bigger than the three tanks together (it was one tank wide)
st.cue('sfx:engine', 'S14', 0.0, 0.4); st.cue('sfx:jet', 'S14', 0.2, 0.45)

# 15: the fish took them for grains. Its head: the jets dive into its open mouth like flakes, the shells of the tanks after them; GLOUPS: it swells,
#     its eyes close, happy
D15 = st.dur('S15'); S15 = 62.0; GULP15 = 0.85; M15 = [0.0, 4.2, -12.5]
st.shot('S15', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[act('poisson', [0.0, FY(S15, 6.0), -26.0], 0, 'idle', 'neutral', scale=S15, keys=[k(0.0, look=[0.0, 4.0, 10.0]),
            k(0.05, clip='gulp', params=GULP(open=0.3, hold=0.5, snap=0.05, jaw=1.25, drop=0.7, mouth=1.7, grow=0.15, lunge=0.15, swell=1.9, wobble=1, bliss=0.8))])],   # (review 1) jaws wide while the army flies in, the snap, a balloon swell, eyes shut, happy
        props=[*[P(f'jet15{j}', 'fighterJet', pos=[r(-10.0 + 20.0 * j), 16.0, 30.0], ry=180, opts={'burner': 1.0}, keys=[
                   k(0.0, to=[r(9.0 - 18.0 * j), 11.0, 6.0], dur=0.3, ease='linear'), k(0.3, to=[r(-4.0 + 8.0 * j), 7.0, -5.0], dur=0.28, ease='linear'), k(0.58, to=M15, dur=0.24, ease='in'),
                   k(0.0, rotTo=[0.0, 0.0, r(1.2 - 2.4 * j)], dur=0.6, ease='inOut'), k(r(GULP15 - 0.04), visible=False)]) for j in range(2)],   # spiralling into the mouth
               *[P(f'tank15{j}', 'armyTank', pos=[r(-8.0 + 8.0 * j), 0.0, 12.0], ry=180, scale=5.0, keys=[
                   k(r(0.12 + 0.06 * j), to=[r((-8.0 + 8.0 * j) * 0.6), 5.0, 2.0], dur=0.3, ease='out'), k(r(0.42 + 0.06 * j), to=M15, dur=r(GULP15 - 0.47 - 0.06 * j), ease='in'),
                   k(r(0.12 + 0.06 * j), rotTo=[r(2.5 + 0.6 * j), r(1.2 * (j - 1)), 0.8], dur=0.7, ease='in'), k(r(GULP15 - 0.04), visible=False)]) for j in range(3)],   # sucked up off the shore, tumbling, like flakes
               BURST('scr15', [9.0, 14.0, -4.0], r(GULP15 + 0.05), 'SCRONCH !', 7.5, 0.4)],
        cams=[FC(0.0, [15.0, 3.0, 28.0], [[-12.0, 0.0, -14.0], [12.0, 0.0, -14.0], [0.0, 25.0, -26.0], [0.0, 0.0, 12.0]], top=0.14, bottom=0.8, lenses=range(26, 66))])
st.cue('whoosh', 'S15', 0.1, 0.35, 0.7, 200, 1200); st.cue('sfx:gulp', 'S15', GULP15, 0.55)

# 16: the government negotiated. A wooden jetty out into the lake: the minister in a dark suit, briefcase in hand, talks up at the fish's head, which
#     fills the water at the end of the jetty, deadpan; he mops his brow
D16 = st.dur('S16'); S16 = 62.0; JET = [0.0, 0.0, 2.0]
JETTY = lambda pid, w=2.2: P(pid, 'slab', pos=[0.0, 0.25, 4.0], opts={'w': w, 'h': 0.2, 'd': 10.0, 'color': '#A8774A'})
MOP16 = lambda x: {'touch': {'L': ['face', x, 0.33, 0.12, 1, 0.03]}, 'hands': {'L': 'open'}, 'yaw': -1.35, 'face': {'sweat': 1.0, 'brow': 0.75, 'mouth': 'grimace', 'eye': 0.2}}
st.shot('S16', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[
        act('poisson', [0.0, FY(S16, 1.0), -30.0], 0, 'idle', 'neutral', scale=S16, keys=[k(0.0, look=[0.4, 2.0, 0.8]), k(0.0, clip='idle', params={'blinks': [0.95]})]),
        act('ministre', [0.4, 0.35, 0.8], 160, 'talk', 'worried', keys=[k(0.0, look=[0.0, 6.0, -12.0]), k(0.0, toon={'face': {'sweat': 1.0, 'brow': 0.6}}, toonDur=0.0),
            k(0.62, toon=MOP16(0.12), toonDur=0.14, toonEase='out'), k(0.66, look='camera'),   # (review 1) mid-negotiation he turns to us, mopping his brow (his back to us, a cloud on his head)
            k(1.05, toon=MOP16(-0.08), toonDur=0.14, toonEase='inOut'), k(1.3, toon=MOP16(0.12), toonDur=0.14, toonEase='inOut')])],
        props=[JETTY('jet16'), HAND('case16', 'briefcase', 'ministre', off=(0.0, -0.1, 0.0)), HAND('hk16', 'slab', 'ministre', hand='L', off=(0.0, -0.02, 0.05), opts={'w': 0.26, 'h': 0.26, 'd': 0.012, 'color': '#FFFFFF'}), *SHORE('16')],
        cams=[FC(0.0, [2.6, 1.5, 4.6], [[0.4, 2.6, 0.8], [0.4, 0.35, 0.8], [-0.4, 1.6, 0.8], [1.2, 1.6, 0.8], [-3.1, 7.6, -19.5], [3.1, 7.6, -19.5]], top=0.14, bottom=0.78, lenses=range(26, 66))])   # (stills 3) the fish's eyes behind him; (review 2) the minister whole (the left edge cut him)

# 17: historic agreement: it got the sea. On the jetty the minister holds up the signed agreement to two photographers whose flashes go off; the fish
#     behind him smiles (ACCORD)
D17 = st.dur('S17'); FL17 = [0.45, 0.8, 1.2, 1.55]
SNAP17 = lambda w: {'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [r(-0.12 * w), 0, 0, 1, None]}, 'face': {'lid': r(0.6 * w)}}
HOLD17 = lambda j: {'touch': {'R': ['torso', -0.2, r(0.55 + 0.03 * (j % 2)), 0.3, 1, 0.03], 'L': ['torso', 0.2, r(0.55 + 0.03 * (j % 2)), 0.3, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.1 if j % 2 else 0.3}}
st.shot('S17', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[
        act('poisson', [0.0, FY(S16, 1.0), -36.0], 0, 'idle', 'happy', scale=S16, keys=[k(0.0, look=[0.0, 2.0, 4.0])]),
        act('ministre', [0.0, 0.35, 1.0], 0, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=HOLD17(0), toonDur=0.0), *[k(t_, toon=HOLD17(j + 1), toonDur=0.12) for j, t_ in enumerate([0.5, 0.9, 1.3, 1.7, 2.1])]]),   # (review 1) the agreement held at his chest under his smile (it covered his face)
        *[act(pid_, pos_, ry_, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.9, 1.0]), k(0.0, toon=SNAP17(0.0), toonDur=0.0),
            *[kk for tf in fl_ for kk in (k(tf, toon=SNAP17(1.0), toonDur=0.04, toonEase='out'), k(r(tf + 0.12), toon=SNAP17(0.0), toonDur=0.14))]]) for pid_, pos_, ry_, fl_ in
          [('photo1', [-1.7, 0.35, 2.1], 125, [FL17[0], FL17[2]]), ('photo2', [1.75, 0.35, 2.3], -125, [FL17[1], FL17[3]])]]],   # (review 1) on the jetty; each flash a bob back; (review 2) at the sides (in front they hid the minister)
        props=[JETTY('jet17', 4.4), *SHORE('17'), P('doc17', 'slab', on={'actor': 'ministre', 'hand': 'R', 'offset': [0.2, 0.08, 0.02]}, opts={'w': 0.62, 'h': 0.42, 'd': 0.01, 'color': '#FBF8EE'}),
               HAND('cam17a', 'pressCamera', 'photo1', off=(0.06, 0.0, 0.08), opts={'flashAt': [FL17[0], FL17[2]], 'burst': 0.45}), HAND('cam17b', 'pressCamera', 'photo2', off=(0.06, 0.0, 0.08), opts={'flashAt': [FL17[1], FL17[3]], 'burst': 0.45})],   # big white flashes (faint sparkles)
        cams=[FC(0.0, [1.1, 1.5, 7.6], [[0.0, 2.7, 1.0], [0.0, 0.35, 1.0], [-1.7, 2.4, 2.1], [1.75, 2.4, 2.3], [0.0, 6.5, -36.0], [0.0, 1.5, -30.0]], top=0.22, bottom=0.78, lenses=range(26, 66))])
for t_ in FL17: st.cue('sfx:click', 'S17', t_, 0.25)

# 18: in exchange it guards the coast. The open sea: the fish cruises past the shore in a captain's cap, a sailboat bobbing in its wake
D18 = st.dur('S18'); S18 = 62.0
st.shot('S18', 'seaSurface', setOpts=SEA, look=XLOOK, actors=[act('poisson', [-30.0, FY(S18, 1.0), -30.0], 90, 'walk', 'neutral', scale=S18, keys=[k(0.0, to=[0.0, FY(S18, 1.0), -30.0], dur=D18, ease='linear'), k(0.0, look=[40.0, 4.0, -30.0]), k(0.0, clip='walk', params={'blinks': [0.3, 1.45]})])],
        props=[P('cap18', 'captainCap', on={'actor': 'poisson', 'joint': 'head', 'offset': [0.0, 0.17, -0.01]}, scale=36.0),   # (review 1) a white captain's cap on the head joint, offset in its own units (it read as a navy band over its eyes)
               P('lh18', 'lighthouse', pos=[16.0, 0.0, 2.0], opts={'h': 14.0}), P('boat18', 'sailboat', pos=[-34.0, 0.0, -12.0], ry=90, scale=3.0, keys=[k(0.0, to=[-10.0, 0.0, -12.0], dur=D18, ease='linear')])],   # a lighthouse, a sailboat: known sizes; (review 2) the boat in front all along (behind, it never showed)
        cams=[FC(0.0, [14.0, 2.4, 30.0], [[-30.0, 0.0, -30.0], [10.0, 0.0, -30.0], [-10.0, 22.0, -30.0], [16.0, 16.0, 2.0], [16.0, 0.0, 2.0]], top=0.14, bottom=0.8, drift=(4.0, 0.0, 0.0), lenses=range(26, 66))])
st.cue('sfx:honk', 'S18', 0.6, 0.25)

# 19: paid three grains a day. Low on the jetty: an official holds up three grains to the fish's open mouth, as big as a garage door; the fish gapes,
#     deadpan
D19 = st.dur('S19'); NIB19 = 0.3; OFF19 = [0.0, 0.35, -0.6]
SHAKE19 = lambda j, eye=0.0: {'reach': {'R': [r(0.12 + 0.025 * (1 if j % 2 else -1)), 2.1, -1.25, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': eye, 'brow': 0.6, 'sweat': 1.0}}
st.shot('S19', 'seaSurface', setOpts=LAKE, look=XLOOK, actors=[
        act('poisson', [0.0, FY(S16, 4.4), -15.0], 0, 'idle', 'neutral', scale=S16, keys=[k(0.0, look=[0.1, 2.1, -1.2]),
            k(NIB19, clip='gulp', params=GULP(open=0.5, hold=0.2, snap=0.05, jaw=0.7, drop=0.25, mouth=1.0, lunge=0.1, swell=0.12, bliss=0.6))]),   # (review 1) the lips part slowly, a small snap takes only the grains, a satisfied blink
        act('agent', OFF19, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.1, 2.3, -1.6]), k(0.0, toon=SHAKE19(0), toonDur=0.0),
            *[k(r(0.08 * (j + 1)), toon=SHAKE19(j + 1), toonDur=0.04) for j in range(12)],   # holding up the three grains at arm's length, trembling
            k(1.03, toon={**SHAKE19(0, 0.5), 'sq': [0.94, 1.08, 0.94], 'reach': {'R': [0.1, 1.95, -0.95, 1, 0.03]}}, toonDur=0.05, toonEase='out'),   # the snap: he flinches, eyes wide
            k(1.2, toon={**SHAKE19(0, 0.2), 'reach': {'R': [0.1, 1.95, -0.95, 1, 0.03]}}, toonDur=0.15), k(1.3, look='camera')])],
        props=[JETTY('jet19'), HAND('gr19', 'grains', 'agent', off=(0.0, 0.0, 0.03), opts={'n': 3, 's': 7.0, 'color': '#8A5A32'}, keys=[k(1.02, visible=False)]),
               BURST('miam19', [1.3, 2.7, -1.5], 1.08, 'miam.', 1.5, 0.45), *SHORE('19')],   # (review 2) three grains you can count; the smallest word of the four, but legible, at the lips
        cams=[FC(0.0, [2.0, 1.0, 1.4], [[0.0, 2.4, -0.6], [0.0, 0.35, -0.6], [0.0, 2.1, -1.8], [1.6, 3.5, -1.8]], top=0.12, bottom=0.8),   # (review 1) outside the fish (the camera was inside it): him whole beside the lips...
              FC(0.95, [9.0, 1.2, 4.0], [[0.0, 0.35, -0.6], [3.1, 10.1, -4.5], [-3.1, 10.1, -4.5], [0.0, -0.5, -2.5]], top=0.1, bottom=0.8, lenses=range(26, 70))])   # ...then the whole face; (review 2) cut on open eyes, before the snap, then a slow happy blink

# 20: the man bought himself another goldfish. The pet shop again: the seller hands him another bag; the seller's smile going stiff
D20 = st.dur('S20'); TAKE20 = 0.6
st.shot('S20', 'supermarket', setOpts=SHOP, actors=[
        act('mec', ME1, 62, 'stand', 'unimpressed', keys=[k(0.0, look=[VE1[0], 1.9, VE1[2]]), k(r(TAKE20 - 0.25), toon={'reach': {'R': [-0.15, 1.25, -1.2, 1, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.2, toonEase='inOut'),
            k(TAKE20, toon={'reach': {'R': [-0.15, 1.25, -1.2, 1, 0.03]}, 'hands': {'R': 'grip'}}, toonDur=0.05), k(r(TAKE20 + 0.35), toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.25)]),
        act('vendeur', VE1, -60, 'stand', 'worried', keys=[k(0.0, look=[ME1[0], 1.9, ME1[2]]), k(0.0, toon={'reach': {'R': [-0.1, 1.3, -1.25, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'smile', 'sweat': 1.0}}, toonDur=0.0),
            k(r(TAKE20 + 0.05), toon={'reach': {'R': [0.15, 1.15, -1.3, 0, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'grimace', 'sweat': 1.0, 'eye': 0.3}}, toonDur=0.25, toonEase='inOut')])],
        props=[P('cnt20', 'table', pos=[-0.05, 0, -1.55], opts={'w': 1.6, 'd': 0.6, 'h': 1.0, 'color': '#C9A06A'}), P('till20', 'cashRegister', pos=[0.45, 1.0, -1.65], ry=-20, opts={'text': '3,50'}),
               *[P(f'aq20{j}', 'aquarium', pos=[r(-2.4 + 1.6 * j), 0, -3.55], opts={'w': 1.3}) for j in range(4)],
               P('bag20', 'fishBag', on={'actor': 'vendeur', 'hand': 'R', 'offset': [0.0, -0.02, 0.0]}, opts={'s': 1.3}, keys=[k(TAKE20, attach='mec', hand='R', offset=[0.0, -0.02, 0.0], face='camera')])],
        cams=[FC(0.0, [0.0, 1.6, 2.6], [[ME1[0], 2.6, ME1[2]], [VE1[0], 2.6, VE1[2]], [ME1[0], 1.0, ME1[2]], [VE1[0], 1.0, VE1[2]], [-1.25, 1.9, -0.9], [1.05, 1.9, -1.55]], top=0.16, bottom=0.76),   # (review 1) both faces in
              FC(0.95, [-0.2, 1.75, -0.4], [[VE1[0], 2.55, VE1[2]], [VE1[0], 1.45, VE1[2]], [r(VE1[0] - 0.35), 1.9, VE1[2]], [r(VE1[0] + 0.35), 1.9, VE1[2]]], top=0.18, bottom=0.72)])   # (review 2) cut in on his stiff smile and the sweat (60 px wide in the two-shot)
st.cue('sfx:ding', 'S20', 0.1, 0.12)

# 21: he gives it three hundred. At home again, the box upturned over the new bowl, the flakes piling over the rim, the fish's eyes popping; a look at
#     us, deadpan
D21 = st.dur('S21')
st.shot('S21', 'livingRoom', setOpts={'sofa': False, 'plant': False}, actors=[
        act('mec', ME3, 40, 'stand', 'unimpressed', keys=[k(0.0, look=[BOWL3[0], 0.9, BOWL3[2]]), k(0.0, toon={'reach': {'R': [r(BOWL3[0] - 0.05), 1.42, r(BOWL3[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.45, 'gy': 0.4}}, toonDur=0.0),
            k(0.75, look='camera'), k(0.78, toon={'reach': {'R': [r(BOWL3[0] - 0.05), 1.42, r(BOWL3[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.15),
            k(1.5, toon={'reach': {'R': [r(BOWL3[0] - 0.05), 1.42, r(BOWL3[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.07), k(1.62, toon={'reach': {'R': [r(BOWL3[0] - 0.05), 1.42, r(BOWL3[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.1)])],
        props=[P('tab21', 'table', pos=[BOWL3[0], 0, BOWL3[2]], opts={'w': 0.6, 'd': 0.6, 'h': 0.72}),
               P('bowl21', 'fishBowl', pos=BOWL3, opts={'r': 0.2, 'flakes': [0.1, 1.2, 170], 'pour': 0.5, 'popAt': 1.0}),
               P('box21', 'grainBox', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.06]}, rot=[0.0, 0.0, 2.3], scale=1.2)],
        cams=[FC(0.0, [0.8, 1.45, 1.4], [[ME3[0], 2.45, ME3[2]], [BOWL3[0], 0.6, BOWL3[2]], [ME3[0], 1.0, ME3[2]], [r(BOWL3[0] + 0.3), 1.3, BOWL3[2]]], top=0.16, bottom=0.76)])   # (script) another angle than S03: the callback is the same action, seen from his other side
st.cue('sfx:crunch', 'S21', 0.12, 0.18); st.cue('sfx:crunch', 'S21', 0.6, 0.15); st.cue('sfx:boing', 'S21', 1.0, 0.25)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
GOLD = {'seed': 651, 'bigMouth': True, 'colors': {'body': '#F2701E', 'fin': '#F9A23B', 'belly': '#FFC27A', 'lip': '#FF9466', 'mouth': '#4A1418', 'tongue': '#E0626E'}}   # (review 1) the cartoon mouth: the gulps never showed an open mouth
DUCK = lambda seed: {'type': 'creature', 'name': 'duck', 'opts': {'seed': seed}}
st.write("Le poisson rouge", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'poisson': {'type': 'creature', 'name': 'fish', 'opts': GOLD},
    'vendeur': {'preset': 'restaurateur', 'seed': 652, 'suit': '#2F8F5B', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'nageur': {'preset': 'sportif', 'seed': 653, 'suit': '#D83A2E', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 654, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'suit': '#A9A397', 'lapel': '#A9A397', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic': {'preset': 'cop', 'seed': 655, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 656, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 657, 'suit': '#7A7F87', 'lapel': '#7A7F87', 'tie': '#2F62B5', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'photo1': {'preset': 'journaliste', 'seed': 658, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'photo2': {'preset': 'journaliste', 'seed': 659, 'suit': '#7A5C8E', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'agent': {'preset': 'officiel', 'seed': 660, 'suit': '#EDEBE3', 'lapel': '#EDEBE3', 'tie': '#1F3B73', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'can1': DUCK(661), 'can2': DUCK(662), 'can3': DUCK(663),
})
