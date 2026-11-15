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
               P('bag1', 'fishBag', on={'actor': 'vendeur', 'hand': 'R', 'offset': [0.0, -0.02, 0.0]}, opts={'s': 1.3}, keys=[k(TAKE1, attach='mec', hand='R', offset=[0.0, -0.02, 0.0], face='camera')])],
        cams=[FC(0.0, [-0.2, 1.55, 2.6], [[ME1[0], 2.45, ME1[2]], [VE1[0], 2.45, VE1[2]], [ME1[0], 0.55, ME1[2]], [VE1[0], 0.9, VE1[2]], [-1.1, 1.9, -0.9]], top=0.16, bottom=0.76, drift=(0.1, 0.0, -0.12))])
st.cue('sfx:ding', 'S01', 0.1, 0.12); st.cue('sfx:splash', 'S01', r(TAKE1 + 0.3), 0.12)

# 2: the seller said: three grains a day. Close on the seller: he holds three grains up between finger and thumb, very serious, a finger wagging;
#    his other hand up three fingers' worth; the man's head in the foreground, his eyes on the grains
D2 = st.dur('S02'); TROIS2 = st.at('S02', 'L02', 5)
st.shot('S02', 'supermarket', setOpts=SHOP, actors=[
        act('vendeur', VE1, -60, 'talk', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['face', 0.3, 0.2, 0.24, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'brow': -0.4, 'lid': 0.15}}, toonDur=0.0),
            k(r(TROIS2 - 0.12), toon={'touch': {'R': ['face', 0.3, 0.28, 0.26, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'brow': -0.6, 'lid': 0.0, 'eye': 0.2}}, toonDur=0.1, toonEase='out'),   # on « trois »: the grains up, eyes wide
            *[k(r(TROIS2 + 0.15 + 0.16 * j), toon={'touch': {'R': ['face', r(0.3 + 0.03 * (1 if j % 2 else -1)), 0.28, 0.26, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'brow': -0.6, 'lid': 0.0, 'eye': 0.2}}, toonDur=0.08) for j in range(4)]]),   # a little wag
        act('mec', ME1, 62, 'stand', 'neutral', keys=[k(0.0, look=[r(VE1[0] + 0.1), 1.95, r(VE1[2] + 0.2)]), k(0.0, toon={'face': {'lid': 0.4, 'gy': 0.2}}, toonDur=0.0)])],
        props=[P('cnt2', 'table', pos=[-0.05, 0, -1.55], opts={'w': 1.6, 'd': 0.6, 'h': 1.0, 'color': '#C9A06A'}), *[P(f'aq2{j}', 'aquarium', pos=[r(-2.4 + 1.6 * j), 0, -3.55], opts={'w': 1.3}) for j in range(4)],
               HAND('gr2', 'grains', 'vendeur', off=(0.0, 0.0, 0.03), opts={'n': 3, 's': 2.6})],
        cams=[FC(0.0, [0.1, 1.95, 0.7], [[VE1[0], 2.5, VE1[2]], [VE1[0], 1.45, VE1[2]], [r(VE1[0] + 0.45), 2.1, r(VE1[2] + 0.3)]], top=0.16, bottom=0.74)])
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
D4 = st.dur('S04'); S4 = 5.2; TUB4 = [0.0, 0, -2.4]
st.shot('S04', 'laundryRoom', setOpts={'washer': False}, actors=[
        act('poisson', [0.05, FY(S4, 0.62), r(TUB4[2] + 0.05)], 90, 'walk', 'happy', scale=S4, keys=[k(0.0, look='camera')]),   # swimming on the spot, its tail swishing over the rim
        act('mec', [1.35, 0, -1.7], -30, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(r(D4 * 0.5), toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.08), k(r(D4 * 0.5 + 0.12), toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.1)])],
        props=[P('tub4', 'bathtub', pos=TUB4, opts={'water': True}), P('box4', 'grainBox', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.06]}, scale=1.2)],
        cams=[FC(0.0, [0.6, 1.45, 1.9], [[-1.0, 1.5, TUB4[2]], [1.2, 1.4, TUB4[2]], [0.0, 0.1, r(TUB4[2] + 0.4)], [1.35, 2.45, -1.7], [1.35, 0.3, -1.7]], top=0.16, bottom=0.78)])
st.cue('sfx:splash', 'S04', 0.3, 0.2); st.cue('sfx:splash', 'S04', 1.2, 0.15)

# 5: the day after, the municipal pool. The open-air pool: the fish fills the basin, its back out like an island, the water heaving; the lifeguard on
#    the deck blows his whistle, cheeks blown out; the man on the edge with his box
D5 = st.dur('S05'); S5 = 19.0; POOL = [0.0, 0.2, -6.0]
WHIS = lambda w: {'touch': {'R': ['face', 0.0, 0.13, 0.12, 1, 0.02]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'kiss', 'swell': r(w), 'puff': r(w), 'cheeks': r(w), 'eye': r(0.4 * w), 'lid': 0.0, 'brow': 0.8}}
st.shot('S05', 'grassland', actors=[
        act('poisson', [0.0, FY(S5, 0.4), -5.6], 160, 'walk', 'happy', scale=S5, keys=[k(0.0, look=[2.0, 2.0, 4.0])]),
        act('nageur', [4.1, 0.2, -1.6], -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=WHIS(0.0), toonDur=0.0), k(0.25, toon=WHIS(1.0), toonDur=0.08, toonEase='out'),
            *[k(r(0.45 + 0.22 * j), toon=WHIS(0.75 if j % 2 else 1.0), toonDur=0.08) for j in range(7)]]),   # three blasts on the whistle, cheeks out
        ],
        props=[P('pool5', 'pool', pos=POOL, opts={'w': 6, 'l': 12, 'deck': 3, 'waves': 3}), HAND('whis5', 'whistle', 'nageur', off=(0.0, 0.0, 0.04))],
        cams=[FC(0.0, [5.8, 3.4, 7.4], [[-3.2, 0.2, -12.0], [3.2, 0.2, -12.0], [4.1, 2.45, -1.6], [4.1, 0.2, -1.6], [0.0, 3.6, -5.6], [-3.2, 0.2, 0.0]], top=0.16, bottom=0.8)])
for j_ in range(3): st.cue('sfx:whistle', 'S05', r(0.25 + 0.44 * j_), 0.3)

# 6: the town hall closed the pool. At the gate of the pool the mayor sets down a folding sign PISCINE FERMÉE, pleased with himself; behind him the
#    fish's eye over the edge of the basin, on the sign (FERMÉE)
D6 = st.dur('S06'); SIGN6 = 0.45
st.shot('S06', 'grassland', actors=[
        act('poisson', [0.6, FY(S5, -1.0), -3.5], 180, 'idle', 'neutral', scale=S5, keys=[k(0.0, look=[0.0, 1.0, 3.0])]),
        act('maire', [-0.9, 0.2, 2.5], 15, 'stand', 'happy', keys=[k(0.0, look=[0.3, 0.9, 2.6]), k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'R': [0.05, 1.0, 2.75, 1, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.0),
            k(r(SIGN6 + 0.1), toon={'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': {'mouth': 'smirk', 'lid': 0.3}}, toonDur=0.2, toonEase='out'), k(r(SIGN6 + 0.3), look='camera'),
            k(r(SIGN6 + 0.45), toon={'touch': {'R': ['torso', 0.0, 0.5, 0.25, 1, 0.03], 'L': ['torso', 0.0, 0.52, 0.27, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'mouth': 'smirk', 'lid': 0.3}}, toonDur=0.2)])],   # hands folded, satisfied
        props=[P('pool6', 'pool', pos=POOL, opts={'w': 6, 'l': 12, 'deck': 3, 'waves': 1.5}), P('sign6', 'closedSign', pos=[0.35, 0.2, 2.75], ry=-10, opts={'text': 'PISCINE|FERMÉE', 'at': SIGN6})],
        cams=[FC(0.0, [0.2, 1.4, 6.8], [[-0.9, 2.5, 2.5], [-0.9, 0.2, 2.5], [0.35, 1.3, 2.75], [0.6, 2.6, -3.5], [1.8, 0.2, 2.5]], top=0.22, bottom=0.78)])
st.cue('thud', 'S06', SIGN6, 0.3)

# 7: the fish moved into the lake. The lakeside: the fish shoots up out of the water in a high arc and dives back in: a wall of spray; a duck on the water
#    bobs in the wave
D7 = st.dur('S07'); S7 = 26.0; LEAP7 = [0.0, 0.95]
st.shot('S07', 'seaSurface', setOpts=LAKE, actors=[
        act('poisson', [-16.0, FY(S7, -6.0), -28.0], 90, 'fly', 'happy', scale=S7, keys=[k(0.0, to=[-2.0, FY(S7, 10.0), -26.0], dur=0.5, ease='out'), k(0.5, to=[10.0, FY(S7, -9.0), -24.0], dur=0.5, ease='in')]),   # up and over, into the lake
        act('can1', [2.5, 0.1, 1.5], -30, 'idle', 'neutral', scale=1.6, keys=[k(0.0, look=[-2.0, 6.0, -26.0]), k(r(LEAP7[1] + 0.1), to=[2.5, 0.6, 1.5], dur=0.2, ease='out'), k(r(LEAP7[1] + 0.3), to=[2.5, 0.1, 1.5], dur=0.3, ease='inOut')])],
        props=[P('spl7', 'waterDrops', pos=[9.0, 0.0, -23.0], opts={'at': r(LEAP7[1] - 0.02), 'n': 40, 's': 9.0})],
        cams=[FC(0.0, [6.0, 2.2, 12.0], [[-14.0, 0.0, -26.0], [12.0, 0.0, -24.0], [-2.0, 16.0, -26.0], [2.5, 0.0, 1.5]], top=0.14, bottom=0.78, lenses=range(26, 70))])
st.cue('whoosh', 'S07', 0.05, 0.3, 0.6, 200, 900); st.cue('sfx:splash', 'S07', LEAP7[1], 0.5)

# 8: it ate all the pedal boats. On the lake a row of swan pedal boats; the fish's head comes up behind them and gulps them one after the other: gone,
#    gone, gone; GLOUPS
D8 = st.dur('S08'); S8 = 26.0; EAT8 = [0.3, 0.62, 0.94, 1.26]
PED8 = [[-3.6, 0.0, -6.0], [-1.2, 0.0, -6.6], [1.2, 0.0, -6.2], [3.6, 0.0, -6.8]]
st.shot('S08', 'seaSurface', setOpts=LAKE, actors=[
        act('poisson', [-4.0, FY(S8, -2.0), -15.5], 0, 'eat', 'happy', scale=S8, keys=[k(0.0, to=[4.0, FY(S8, -2.0), -15.5], dur=D8, ease='linear')])],   # its head sweeping along the row
        props=[*[P(f'ped8{j}', 'pedalo', pos=p_, ry=r(-20 + 15 * j), opts={'seed': j, 'goneAt': EAT8[j]}) for j, p_ in enumerate(PED8)],
               BURST('glo8', [0.0, 3.0, -5.0], r(EAT8[2] + 0.02), 'GLOUPS !', 1.8, 0.3)],
        cams=[FC(0.0, [0.0, 2.4, 6.5], [[-4.4, 0.0, -6.0], [4.4, 0.0, -6.8], [0.0, 6.5, -10.0]], top=0.16, bottom=0.8)])
for t_ in EAT8: st.cue('sfx:gulp', 'S08', t_, 0.25)

# 9: the ducks filed a complaint. The gendarmerie: three ducks stand on the desk quacking at the gendarme, wings flapping; he types, deadpan
D9 = st.dur('S09'); DESK9 = [-4.6, 0, -1.4]
st.shot('S09', 'office', actors=[
        act('flic', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 1.1, -1.2]), k(0.0, toon={'reach': {'L': [-4.8, 0.85, -1.55, 1, 0.03], 'R': [-4.4, 0.85, -1.55, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.5}}, toonDur=0.0),
            *[k(r(0.15 + 0.14 * j), toon={'reach': {'L': [-4.8, r(0.85 + 0.03 * (j % 2)), -1.55, 1, 0.03], 'R': [-4.4, r(0.88 - 0.03 * (j % 2)), -1.55, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.5}}, toonDur=0.06) for j in range(9)]]),   # typing
        *[act(f'can{j + 1}', [r(-5.15 + 0.55 * j), 0.78, -1.0], r(170 + 10 * (j - 1)), 'angry', 'angry', scale=1.5, keys=[k(0.0, look=[-4.6, 1.6, -2.1])]) for j in range(3)]],
        props=[P('desk9', 'desk', pos=DESK9, opts={'w': 1.6}), P('pc9', 'laptop', pos=[-4.6, 0.76, -1.6], ry=180)],
        cams=[FC(0.0, [-3.6, 1.5, 1.4], [[-5.3, 1.5, -1.0], [-3.9, 1.5, -1.0], [-4.6, 2.3, -2.15], [-4.6, 0.6, -1.0]], top=0.16, bottom=0.76)])
st.cue('sfx:cluck', 'S09', 0.1, 0.3); st.cue('sfx:cluck', 'S09', 0.5, 0.3); st.cue('sfx:cluck', 'S09', 0.9, 0.3)

# 10: the judge sided with the fish. The courtroom: the judge brings his gavel down, BANG; the three ducks at the plaintiffs' bench are bowled over,
#     feet in the air
D10 = st.dur('S10'); BANG10 = st.at('S10', 'L10', 6)
st.shot('S10', 'courtroom', actors=[
        act('juge', [0.0, 0.3, -4.0], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.35, 2.15, -3.35, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.35}}, toonDur=0.0),
            k(r(BANG10 - 0.25), toon={'reach': {'R': [0.4, 2.6, -3.4, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'brow': -0.4}}, toonDur=0.18, toonEase='out'),   # up...
            k(BANG10, toon={'reach': {'R': [0.4, 1.5, -3.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.0, 'brow': -0.6, 'mouth': 'open'}}, toonDur=0.05, toonEase='in'),   # ...BANG
            k(r(BANG10 + 0.2), toon={'reach': {'R': [0.4, 1.55, -3.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.35}}, toonDur=0.15)]),
        *[act(f'can{j + 1}', [r(-3.7 + 0.45 * j), 0.78, 0.9], 160, 'angry', 'angry', scale=1.3, keys=[k(0.0, look=[0.0, 2.2, -4.0]), k(r(BANG10 + 0.04 + 0.04 * j), toon={'lay': [-1.4, 0.0]}, toonDur=0.12, toonEase='out')]) for j in range(3)]],
        props=[HAND('gav10', 'gavel', 'juge', off=(0.0, -0.02, 0.05)), P('desk10', 'desk', pos=[-3.3, 0, 1.0], opts={'w': 1.8})],
        cams=[FC(0.0, [-1.6, 1.9, 4.2], [[0.0, 2.75, -4.0], [-3.9, 0.7, 0.9], [-2.6, 1.5, 0.9], [0.6, 1.3, -3.3]], top=0.16, bottom=0.76)])
st.cue('clang', 'S10', BANG10, 0.4); st.cue('sfx:cluck', 'S10', r(BANG10 + 0.1), 0.25)

# 11: the ducks appealed. Close on the three ducks back on their feet, hopping mad, quacking up at the bench (APPEL)
D11 = st.dur('S11')
st.shot('S11', 'courtroom', actors=[*[act(f'can{j + 1}', [r(-3.7 + 0.45 * j), 0.78, 0.9], 160, 'hop', 'angry', scale=1.3, keys=[k(0.0, look=[0.0, 2.2, -4.0])]) for j in range(3)]],
        props=[P('desk11', 'desk', pos=[-3.3, 0, 1.0], opts={'w': 1.8})],
        cams=[FC(0.0, [-2.6, 1.15, 2.6], [[-3.95, 1.6, 0.9], [-2.6, 1.6, 0.9], [-3.3, 0.75, 0.9]], top=0.26, bottom=0.74)])
st.cue('sfx:cluck', 'S11', 0.05, 0.35); st.cue('sfx:cluck', 'S11', 0.4, 0.35); st.cue('sfx:cluck', 'S11', 0.8, 0.35)

# 12: the fish ate the courthouse. The courthouse on the lakeshore; the giant fish rears up out of the lake behind it, jaws wide, and swallows it in one
#     gulp; it swells, satisfied
D12 = st.dur('S12'); S12 = 62.0; GULP12 = 0.55
st.shot('S12', 'seaSurface', setOpts=LAKE, actors=[
        act('poisson', [0.0, FY(S12, 2.0), -26.0], 0, 'idle', 'neutral', scale=S12, keys=[k(0.0, to=[0.0, FY(S12, 4.5), -16.0], dur=GULP12, ease='out'), k(r(GULP12 - 0.42), clip='gulp')])],   # rearing up and forward, the gulp
        props=[P('trib12', 'townHall', pos=[0.0, 0.0, 8.5], opts={'text': 'TRIBUNAL', 'w': 6}, keys=[k(r(GULP12), visible=False)])],
        cams=[FC(0.0, [3.0, 1.8, 22.0], [[-3.4, 0.0, 8.5], [3.4, 0.0, 8.5], [0.0, 22.0, -16.0], [-10.0, 0.0, -10.0], [10.0, 0.0, -10.0]], top=0.12, bottom=0.8, lenses=range(26, 64))])
st.cue('sfx:gulp', 'S12', GULP12, 0.5)

# 13: the army was sent. A country road to the lake: three tanks rolling toward us in a line, dust behind them
D13 = st.dur('S13')
st.shot('S13', 'grassland', actors=[],
        props=[*[P(f'tank13{j}', 'armyTank', pos=[r(-1.0 + 1.0 * j), 0, r(-26.0 - 9.0 * j)], ry=180, scale=5.0, keys=[k(0.0, to=[r(-1.0 + 1.0 * j), 0, r(-14.0 - 9.0 * j)], dur=D13, ease='linear')]) for j in range(3)]],
        cams=[FC(0.0, [5.0, 1.2, 4.0], [[-3.0, 0.0, -14.0], [3.0, 0.0, -14.0], [0.0, 4.5, -14.0], [1.0, 0.0, -44.0]], top=0.2, bottom=0.8)])
st.cue('sfx:engine', 'S13', 0.0, 0.45)

# 14: three tanks, two fighter jets. On the lakeshore the three tanks aim their guns at the water; two jets scream in low overhead toward the lake, where
#     the fish's head waits
D14 = st.dur('S14'); S14 = 62.0
st.shot('S14', 'seaSurface', setOpts=LAKE, actors=[act('poisson', [0.0, FY(S14, -2.0), -40.0], 0, 'idle', 'neutral', scale=S14, keys=[k(0.0, look=[0.0, 2.0, 10.0])])],
        props=[*[P(f'tank14{j}', 'armyTank', pos=[r(-7.0 + 7.0 * j), 0.0, 9.0], ry=180, scale=5.0) for j in range(3)],
               *[P(f'jet14{j}', 'fighterJet', pos=[r(-6.0 + 12.0 * j), 14.0, 40.0], ry=180, opts={'burner': 1.0}, keys=[k(0.0, to=[r(-6.0 + 12.0 * j), 9.0, -10.0], dur=D14, ease='linear')]) for j in range(2)]],
        cams=[FC(0.0, [12.0, 2.5, 30.0], [[-10.0, 0.0, 9.0], [9.0, 0.0, 9.0], [0.0, 20.0, -40.0], [-6.0, 10.0, 0.0]], top=0.14, bottom=0.8, lenses=range(26, 70))])
st.cue('sfx:engine', 'S14', 0.0, 0.4); st.cue('sfx:jet', 'S14', 0.2, 0.45)

# 15: the fish took them for grains. Its head: the jets dive into its open mouth like flakes, the shells of the tanks after them; GLOUPS: it swells,
#     its eyes close, happy
D15 = st.dur('S15'); S15 = 62.0; GULP15 = 0.85
st.shot('S15', 'seaSurface', setOpts=LAKE, actors=[act('poisson', [0.0, FY(S15, 0.0), -30.0], 0, 'idle', 'neutral', scale=S15, keys=[k(r(GULP15 - 0.42), clip='gulp'), k(0.0, look=[0.0, 4.0, 10.0])])],
        props=[*[P(f'jet15{j}', 'fighterJet', pos=[r(-10.0 + 20.0 * j), 16.0, 30.0], ry=180, opts={'burner': 1.0}, keys=[k(0.0, to=[0.0, 8.0, -9.0], dur=r(GULP15 - 0.05), ease='in'), k(r(GULP15 - 0.04), visible=False)]) for j in range(2)],
               *[P(f'tank15{j}', 'armyTank', pos=[r(-8.0 + 8.0 * j), 0.0, 12.0], ry=180, scale=5.0, keys=[k(0.2, to=[0.0, 6.0, -9.0], dur=r(GULP15 - 0.25), ease='in'), k(r(GULP15 - 0.04), visible=False)]) for j in range(3)],
               BURST('glo15', [9.0, 18.0, -6.0], r(GULP15 + 0.05), 'GLOUPS !', 7.0, 0.35)],
        cams=[FC(0.0, [14.0, 4.0, 30.0], [[-14.0, 0.0, 0.0], [14.0, 0.0, 0.0], [0.0, 24.0, -30.0], [0.0, 0.0, 12.0]], top=0.14, bottom=0.8, lenses=range(26, 66))])
st.cue('whoosh', 'S15', 0.1, 0.35, 0.7, 200, 1200); st.cue('sfx:gulp', 'S15', GULP15, 0.55)

# 16: the government negotiated. A wooden jetty out into the lake: the minister in a dark suit, briefcase in hand, talks up at the fish's head, which
#     fills the water at the end of the jetty, deadpan; he mops his brow
D16 = st.dur('S16'); S16 = 62.0; JET = [0.0, 0.0, 2.0]
JETTY = lambda pid: P(pid, 'slab', pos=[0.0, 0.25, 4.0], opts={'w': 2.2, 'h': 0.2, 'd': 10.0, 'color': '#A8774A'})
st.shot('S16', 'seaSurface', setOpts=LAKE, actors=[
        act('poisson', [0.0, FY(S16, 2.0), -16.0], 0, 'idle', 'neutral', scale=S16, keys=[k(0.0, look=[0.0, 2.0, 2.0])]),
        act('ministre', [0.2, 0.35, 0.6], 180, 'talk', 'worried', keys=[k(0.0, look=[0.0, 6.0, -8.0]), k(0.0, toon={'face': {'sweat': 1.0, 'brow': 0.6}}, toonDur=0.0),
            k(0.7, toon={'touch': {'L': ['face', 0.1, 0.35, 0.1, 1, 0.03]}, 'hands': {'L': 'open'}, 'face': {'sweat': 1.0, 'brow': 0.7}}, toonDur=0.2, toonEase='inOut'), k(1.2, toon={'face': {'sweat': 1.0, 'brow': 0.6}}, toonDur=0.2)])],   # mopping his brow
        props=[JETTY('jet16'), HAND('case16', 'briefcase', 'ministre', off=(0.0, -0.1, 0.0))],
        cams=[FC(0.0, [3.2, 1.5, 4.6], [[0.2, 2.6, 0.6], [0.2, 0.35, 0.6], [0.0, 12.0, -16.0], [-3.0, 3.0, -10.0]], top=0.14, bottom=0.78, lenses=range(26, 66))])

# 17: historic agreement: it got the sea. On the jetty the minister holds up the signed agreement to two photographers whose flashes go off; the fish
#     behind him smiles (ACCORD)
D17 = st.dur('S17'); FL17 = [0.45, 0.8, 1.2, 1.55]
SNAP17 = lambda w: {'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [r(-0.12 * w), 0, 0, 1, None]}, 'face': {'lid': r(0.6 * w)}}
st.shot('S17', 'seaSurface', setOpts=LAKE, actors=[
        act('poisson', [0.0, FY(S16, 2.0), -16.0], 0, 'idle', 'happy', scale=S16, keys=[k(0.0, look=[0.0, 2.0, 4.0])]),
        act('ministre', [0.0, 0.35, 1.0], 0, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['face', -0.32, 0.4, 0.15, 1, 0.03], 'L': ['face', 0.32, 0.4, 0.15, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.1}}, toonDur=0.0),
            *[k(t_, toon={'touch': {'R': ['face', -0.32, r(0.4 + 0.05 * (j % 2)), 0.15, 1, 0.03], 'L': ['face', 0.32, r(0.4 + 0.05 * (j % 2)), 0.15, 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'mouth': 'bigsmile', 'lid': 0.1 if j % 2 else 0.3}}, toonDur=0.12) for j, t_ in enumerate([0.5, 0.9, 1.3, 1.7, 2.1])]]),   # the agreement up in both hands, nodding to the flashes
        *[act(pid_, pos_, ry_, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.9, 1.0]), k(0.0, toon=SNAP17(0.0), toonDur=0.0),
            *[kk for tf in fl_ for kk in (k(tf, toon=SNAP17(1.0), toonDur=0.04, toonEase='out'), k(r(tf + 0.12), toon=SNAP17(0.0), toonDur=0.14))]]) for pid_, pos_, ry_, fl_ in
          [('photo1', [-1.4, 0.35, 3.4], 160, [FL17[0], FL17[2]]), ('photo2', [1.5, 0.35, 3.6], -160, [FL17[1], FL17[3]])]]],   # each flash: a little bob back
        props=[JETTY('jet17'), P('doc17', 'slab', on={'actor': 'ministre', 'hand': 'R', 'offset': [0.3, 0.05, 0.02]}, opts={'w': 0.62, 'h': 0.42, 'd': 0.01, 'color': '#FBF8EE'}),
               HAND('cam17a', 'pressCamera', 'photo1', off=(0.06, 0.0, 0.08), opts={'flashAt': [FL17[0], FL17[2]]}), HAND('cam17b', 'pressCamera', 'photo2', off=(0.06, 0.0, 0.08), opts={'flashAt': [FL17[1], FL17[3]]})],
        cams=[FC(0.0, [1.1, 1.5, 7.2], [[0.0, 2.7, 1.0], [0.0, 0.35, 1.0], [-1.4, 2.4, 3.4], [1.5, 2.4, 3.6], [0.0, 10.0, -16.0]], top=0.22, bottom=0.78, lenses=range(26, 66))])
for t_ in FL17: st.cue('sfx:click', 'S17', t_, 0.25)

# 18: in exchange it guards the coast. The open sea: the fish cruises past the shore in a captain's cap, a sailboat bobbing in its wake
D18 = st.dur('S18'); S18 = 62.0
st.shot('S18', 'seaSurface', setOpts=SEA, actors=[act('poisson', [-30.0, FY(S18, 1.0), -30.0], 90, 'walk', 'neutral', scale=S18, keys=[k(0.0, to=[0.0, FY(S18, 1.0), -30.0], dur=D18, ease='linear'), k(0.0, look=[40.0, 4.0, -30.0])])],
        props=[P('cap18', 'copCap', on={'actor': 'poisson', 'joint': 'head', 'offset': [0.0, 0.1, 0.0]}, scale=0.7)],
        cams=[FC(0.0, [8.0, 3.0, 30.0], [[-30.0, 0.0, -30.0], [10.0, 0.0, -30.0], [-10.0, 22.0, -30.0], [0.0, 0.0, 6.0]], top=0.16, bottom=0.8, drift=(4.0, 0.0, 0.0), lenses=range(26, 66))])
st.cue('sfx:honk', 'S18', 0.6, 0.25)

# 19: paid three grains a day. Low on the jetty: an official holds up three grains to the fish's open mouth, as big as a garage door; the fish gapes,
#     deadpan
D19 = st.dur('S19')
st.shot('S19', 'seaSurface', setOpts=LAKE, actors=[
        act('poisson', [0.0, FY(S16, 0.5), -9.0], 0, 'idle', 'neutral', scale=S16, keys=[k(0.0, look=[0.0, 1.5, 2.0])]),
        act('agent', [0.3, 0.35, 1.2], 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 3.0, -2.0]), k(0.0, toon={'reach': {'R': [0.1, 2.3, 0.6, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.0),
            *[k(r(0.2 + 0.2 * j), toon={'reach': {'R': [r(0.1 + 0.02 * (1 if j % 2 else -1)), 2.3, 0.6, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4 if j != 3 else 1.0}}, toonDur=0.08) for j in range(6)]])],   # a nervous little tremble, a blink
        props=[JETTY('jet19'), HAND('gr19', 'grains', 'agent', off=(0.0, 0.0, 0.03), opts={'n': 3, 's': 2.6})],
        cams=[FC(0.0, [2.2, 0.8, 4.4], [[0.3, 2.6, 1.2], [0.3, 0.35, 1.2], [0.0, 8.0, -9.0], [-3.0, 0.0, -2.0]], top=0.14, bottom=0.78, lenses=range(26, 66))])

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
        cams=[FC(0.0, [1.2, 1.7, 2.4], [[ME1[0], 2.45, ME1[2]], [VE1[0], 2.45, VE1[2]], [ME1[0], 0.9, ME1[2]], [VE1[0], 0.9, VE1[2]]], top=0.16, bottom=0.76)])
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
GOLD = {'seed': 651, 'colors': {'body': '#F2701E', 'fin': '#F9A23B', 'belly': '#FFC27A'}}
DUCK = lambda seed: {'type': 'creature', 'name': 'duck', 'opts': {'seed': seed}}
st.write("Le poisson rouge", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'poisson': {'type': 'creature', 'name': 'fish', 'opts': GOLD},
    'vendeur': {'preset': 'restaurateur', 'seed': 652, 'suit': '#2F8F5B', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'nageur': {'preset': 'sportif', 'seed': 653, 'suit': '#D83A2E', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 654, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'suit': '#A9A397', 'lapel': '#A9A397', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic': {'preset': 'cop', 'seed': 655, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 656, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 657, 'suit': '#33363D', 'lapel': '#33363D', 'tie': '#2F62B5', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'photo1': {'preset': 'journaliste', 'seed': 658, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'photo2': {'preset': 'journaliste', 'seed': 659, 'suit': '#7A5C8E', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'agent': {'preset': 'officiel', 'seed': 660, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'can1': DUCK(661), 'can2': DUCK(662), 'can3': DUCK(663),
})
