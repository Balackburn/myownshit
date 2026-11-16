#!/usr/bin/env python3
"""La table basse (story 80, cycle 42; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man stubbed his toe on his coffee table. It was premeditated. Special forces surrounded the building. The table refused to comply. So a tank
came in through the front. It came out three buildings further on. Four pairs of handcuffs. The tank driver was decorated. At the trial, it showed
no remorse. The defence pleaded it was there first. Twenty years. In prison, it reoffended. Three guards. Life. On appeal, the table had an X-ray.
It had a bruise. This man was convicted of assault. And of the three buildings. His cellmate is the table. He stubbed his toe again the first night.
Staging: barefoot in his living room he walks into the table (low at floor level, the table in the foreground): BONK, he hops on one foot holding
his toe, the table does not move; the table alone under a swinging lamp, yellow evidence markers popping up round its legs; at night a helicopter
with a searchlight over his block, special forces sliding down ropes; a ring of them round the door, rifles up; a flashbang in the living room, the
smoke clears: the table, exactly where it was; a tank comes down the street and drives into the facade in a burst of bricks; seen from the far side,
three blocks in a row, the same round hole through the first two, and the tank bursts out of the third with the table on its gun; four soldiers each
cuffed to a leg carry it off like a stretcher (ARRÊTÉE), the tank driver hopping behind them holding his toe; a band plays, a general pins a medal on
the driver, who salutes on one leg, his foot in plaster; the courtroom; the table in the dock between two gendarmes, perfectly still; the defence
unrolls a floor plan of the living room down the aisle, footprints walking straight into the table, the jury leans in; a giant stamp crushes the
table's legs flat (CONDAMNÉE), they spring back; in the cell three guards hop round the motionless table, each holding a foot; the three in casts on
crutches salute as a giant stamp hits the cell door (PERPÉTUITÉ); in hospital the table lies legs up on an X-ray table and the light box lights up
with the X-ray of a table; one leg, close: a blue bruise, an evidence marker pops up; the man in the dock (COUPABLE), he staggers; the table, a
bandage round its leg, at the plaintiff's bench; the courtroom's back wall falls flat and shows the three holed blocks; a guard shoves him into a
narrow cell where the table stands between him and his bunk, the door slams; that night, framed exactly like the first shot, his foot hits the leg
and he hops again; the table does not move.
Natural look; cycle 42: props_table.js (coffeeTable, evidenceMarker, flashBang, rope, holedBlock, brickBurst, footCast, crutch, planScroll, xrayBed,
xrayScreen, barDoor, fallWall, dockBox, tankHelmet); battleTank, toonPuff (props_bocal.js), helicopter (props_lunettes.js), bandInstr, kepi, medal,
handcuffs, bigStamp, stampMark, pendantLamp reused.
Lessons applied from the start: the table is the same model in every shot and never moves by itself; every face three-quarter to us at least; feet
and payoffs above the caption band; holds get a gesture."""
from story_kit import *
import math

st = Story('table', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L03', 4), ('S05', 'L04', 0), ('S06', 'L04', 3), ('S07', 'L05', 0),
         ('S08', 'L05', 4), ('S09', 'L06', 0), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L09', 5), ('S14', 'L10', 0),
         ('S15', 'L11', 0), ('S16', 'L12', 0), ('S17', 'L13', 0), ('S18', 'L14', 0), ('S19', 'L15', 0), ('S20', 'L16', 0), ('S21', 'L16', 6),
         ('S22', 'L17', 0), ('S23', 'L18', 0), ('S24', 'L19', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def loc(p, ry, v, s=1.0):
    """the world position of the local point v of something standing at p, turned ry degrees about Y and scaled s"""
    a_ = math.radians(ry); return [r(p[0] + s * (v[0] * math.cos(a_) + v[2] * math.sin(a_))), r(p[1] + s * v[1]), r(p[2] + s * (-v[0] * math.sin(a_) + v[2] * math.cos(a_)))]

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
TBL = lambda pid, pos, ry=0, **o: P(pid, 'coffeeTable', pos=pos, ry=ry, opts=o)
MARK = lambda pid, pos, n, at_, ry=0, s=1.0: P(pid, 'evidenceMarker', pos=pos, ry=ry, opts={'n': n, 'at': at_, 's': s})
KEPI = lambda pid, who, **o: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, **o})
GKEPI = lambda pid, who: KEPI(pid, who, color='#1F2A44', band='#1F2A44')   # a gendarme's navy kepi
CUFF = lambda pid, who, hand: P(pid, 'handcuffs', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.06, 0.0]}, scale=0.45)
CAST = lambda pid, who, foot='footL': P(pid, 'footCast', on={'actor': who, 'joint': foot, 'offset': [0.0, 0.02, 0.0]}, opts={'s': 1.0})
PAIN = {'lid': 0.85, 'mouth': 'O', 'brow': 0.9, 'blush': 0.6, 'sweat': 1.0}
DEAD = {'lid': 0.45, 'mouth': 'line'}
STREET = {'eiffelStyle': 'v2', 'clear': [-8.0, 8.0], 'clearL': [-8.0, 8.0]}

# the hop on one foot, holding the left foot: the left thigh up, the shin folded back, the spine bowed, both hands on the foot (the foot's place in
# his own frame, measured on a still); position keys from the bounces, toon keys at each take-off, top and landing carry the whole pose
FOOT = [0.09, 0.5, 0.41]; YAW = 0.6
def hold_pose(root, ry, face, sq=None, look=None, yaw=YAW):
    ry_ = ry + math.degrees(yaw)
    hl = loc(root, ry_, [FOOT[0] + 0.07, FOOT[1] + 0.06, FOOT[2] + 0.02]); hr = loc(root, ry_, [FOOT[0] - 0.06, FOOT[1] + 0.04, FOOT[2] + 0.07])
    t_ = {'bend': {'spine': [0.28, 0, 0, 1, None], 'legL': [-1.45, 0.1, 0, 1, None], 'shinL': [1.6, 0, 0, 1, None]}, 'yaw': yaw,
          'reach': {'L': [*hl, 1, 0.04], 'R': [*hr, 1, 0.04]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': face}
    if sq: t_['sq'] = sq
    return t_
def hop_hold(t0, pts, dt, peak, ry, face, y0=0.0):
    keys, toon = [], []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; t = r(t0 + dt * i); m = [r((a[0] + b[0]) / 2), r(y0 + peak), r((a[1] + b[1]) / 2)]
        keys += [k(t, to=m, dur=r(dt / 2), ease='out', face='keep', glide=True), k(r(t + dt / 2), to=[b[0], y0, b[1]], dur=r(dt / 2), ease='in', face='keep', glide=True)]
        toon += [k(t, toon=hold_pose([a[0], y0, a[1]], ry, face, [0.88, 1.14, 0.88]), toonDur=0.04, toonEase='out'),
                 k(r(t + dt / 2), toon=hold_pose(m, ry, face, [1.0, 1.0, 1.0]), toonDur=r(dt / 2 - 0.04)),
                 k(r(t + dt - 0.03), toon=hold_pose([b[0], y0, b[1]], ry, face, [1.12, 0.88, 1.12]), toonDur=0.03, toonEase='in')]
    return keys, toon

for g_ in [('S01', 0.75, 'mec', 'bonk'), ('S10', 0.6, 'pilote', 'hop'), ('S11', 1.2, 'pilote', 'medal'), ('S20', 0.9, 'mec', 'coupable'), ('S24', 0.7, 'mecP', 'bonk2')]:
    st.gag(*g_)
st.card('S10', 'ARRÊTÉE', at=0.3)
st.card('S15', 'CONDAMNÉE', at=0.32)
st.card('S20', 'COUPABLE', at=0.74)

# 1 and 24, the loop: low at floor level in front of the table (its long side across the frame); he walks toward us from the back of the room and
#    his left foot slams into the table's far right leg: BONK, a squash, stars; he springs up and hops back on one foot holding his toe, mouth open,
#    eyes squeezed; the table, in the foreground, does not move
T1 = [0.0, 0, 0.0]; WALK_FROM = [0.42, 0, -2.0]; HIT_AT = [0.42, 0, -0.66]
def loop_shot(sid, set_, who, t_hit, setOpts=None, extra_props=(), dur=None):
    D = st.dur(sid); walk = r(t_hit - 0.02)
    ks = [k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0),
          k(0.0, to=HIT_AT, dur=walk, clip='walk', ease='linear'),
          k(walk, toon={'bend': {'legL': [-0.45, 0, 0, 1, None], 'shinL': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.06),
          k(t_hit, toon={'bend': {'legL': [-0.5, 0, 0, 1, None], 'shinL': [0.2, 0, 0, 1, None], 'spine': [-0.1, 0, 0, 1, None]}, 'sq': [1.12, 0.86, 1.12],
                         'face': {'lid': 0.0, 'eye': 0.5, 'pop': 1.0, 'popLen': 0.22, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.03, toonEase='out'),   # the toe hits: eyes out, a squash
          k(r(t_hit + 0.16), toon={'bend': {'legL': [-0.9, 0, 0, 1, None], 'shinL': [1.2, 0, 0, 1, None]}, 'sq': [0.9, 1.15, 0.9],
                                   'face': {'lid': 0.0, 'eye': 0.5, 'pop': 1.0, 'popLen': 0.3, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.08, toonEase='out')]   # the pain arrives a beat later
    hk, ht = hop_hold(r(t_hit + 0.3), [[HIT_AT[0], HIT_AT[2]], [0.6, -0.92], [0.38, -1.18], [0.66, -1.36], [0.44, -1.54], [0.6, -1.66], [0.45, -1.78]], 0.3, 0.2, 0, PAIN)
    ks += hk + ht + [k(r(t_hit + 0.3), look='camera')]
    props = [TBL(f't{sid}', T1), P(f'stars{sid}', 'impactStars', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.62, 0.0]}, opts={'at': r(t_hit + 0.02), 'n': 5}),
             *extra_props]
    st.shot(sid, set_, setOpts=setOpts, actors=[act(who, WALK_FROM, 0, 'stand', 'neutral', keys=ks)], props=props,
            fx=[{'type': 'shake', 'at': t_hit, 'dur': 0.14, 'amount': 0.012}],
            cams=[cam(0.0, [0.55, 0.45, 2.0], [0.54, 0.45, 1.96], [0.25, 0.9, -0.8], [0.25, 0.91, -0.8], lens=60)])
    st.cue('sfx:stepSoft', sid, 0.15, 0.12); st.cue('sfx:stepSoft', sid, 0.45, 0.12)
    st.cue('sfx:bonk', sid, t_hit, 0.5); st.cue('sfx:gasp', sid, r(t_hit + 0.18), 0.3)
    for i in range(6): st.cue('thud', sid, r(t_hit + 0.6 + 0.3 * i), 0.1)
loop_shot('S01', 'livingRoom', 'mec', 0.7, setOpts={'tv': False, 'carpet': False})

# 2: it was premeditated. The table alone in the empty room, a slow push-in at knee height; a lamp swings over it; four yellow evidence markers pop
#    up round its legs one after another
D2 = st.dur('S02')
st.shot('S02', 'livingRoom', setOpts={'tv': False, 'carpet': False},
        props=[TBL('t2', T1), P('lampe2', 'pendantLamp', pos=[0.0, 2.15, 0.0], opts={'drop': 0.9, 'swing': [[-0.4, 0.35]], 'color': '#E8452C'}),
               *[MARK(f'm2{j}', p_, j + 1, r(0.15 + 0.22 * j), ry=a_, s=1.6) for j, (p_, a_) in enumerate([([0.36, 0, 0.5], -15), ([-0.36, 0, 0.52], 15), ([-0.3, 0.42, 0.05], 10), ([0.3, 0.42, -0.05], -10)])]],
        cams=[cam(0.0, [0.0, 0.8, 2.9], [0.0, 0.76, 2.2], [0.0, 0.5, 0.0], [0.0, 0.48, 0.0], lens=46)])
for j in range(4): st.cue('sfx:pop', 'S02', r(0.15 + 0.22 * j), 0.18)
st.cue('sfx:sting', 'S02', 0.05, 0.25)

# 3: special forces. Night, his street from low: the block's front, a helicopter over it sweeping its searchlight; three ropes hang from it and
#    three men in black slide down them, one after another
D3 = st.dur('S03'); BLK3 = [0.0, 0, -8.0]
SW3 = [(-0.9, 0.0), (0.3, 0.18), (1.3, 0.34)]
st.shot('S03', 'parisStreet', setOpts={**STREET, 'night': True}, actors=[
        *[act(f'swat{j + 1}', [x_, r(6.8 - 0.4 * j), -5.6], 15, 'stand', 'determined', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': [x_, r(9.4 - 0.4 * j), -5.45, 1, 0.03], 'R': [x_, r(9.1 - 0.4 * j), -5.45, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'legL': [-0.3, 0.1, 0, 1, None], 'legR': [-0.2, -0.1, 0, 1, None], 'shinL': [0.5, 0, 0, 1, None], 'shinR': [0.4, 0, 0, 1, None]}}, toonDur=0.0),
            k(d_, to=[x_, r(2.2 - 0.3 * j), -5.6], dur=r(D3 - d_), ease='in', glide=True, face='keep'),
            k(d_, toon={'reach': {'L': [x_, r(4.8 - 0.3 * j), -5.45, 1, 0.03], 'R': [x_, r(4.5 - 0.3 * j), -5.45, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'legL': [-0.3, 0.1, 0, 1, None], 'legR': [-0.2, -0.1, 0, 1, None], 'shinL': [0.5, 0, 0, 1, None], 'shinR': [0.4, 0, 0, 1, None]}}, toonDur=r(D3 - d_), toonEase='in')])
          for j, (x_, d_) in enumerate(SW3)]],
        props=[P('blk3', 'holedBlock', pos=BLK3, opts={'w': 6.0, 'h': 10.0, 'holeAt': 99.0}),
               P('heli3', 'helicopter', pos=[0.3, 10.2, -5.2], ry=90, scale=1.0, opts={'spin': 6, 'beam': True, 'beamLen': 14, 'beamR': 1.8, 'tilt': 25, 'sweep': [[0.0, -25], [D3, 25]]}),
               *[P(f'corde3{j}', 'rope', pos=[x_, 9.6, -5.45], opts={'len': 9.3, 'seed': j, 'sway': 0.0}) for j, (x_, _) in enumerate(SW3)]],
        cams=[cam(0.0, [2.4, 1.3, 7.5], [2.3, 1.32, 7.2], [0.1, 6.0, -6.0], [0.1, 5.7, -6.0], lens=52)])
st.cue('sfx:rotor', 'S03', 0.0, 0.4); st.cue('sfx:siren', 'S03', 0.2, 0.15)
for j, (_, d_) in enumerate(SW3): st.cue('sfx:slideDown', 'S03', d_, 0.15)

# 4: surrounded the building. Night, the block's door, three-quarter: four men in black in a half ring round it, rifles (held torches) up and aimed
#    at the door, crouched; they shuffle in a step closer together; the searchlight circle sweeps over them
D4 = st.dur('S04'); DOOR4 = [0.0, 0, -8.0]
RING4 = [(-1.8, -6.1, 35), (-0.65, -5.4, 12), (0.65, -5.4, -12), (1.8, -6.1, -35)]
st.shot('S04', 'parisStreet', setOpts={**STREET, 'night': True}, actors=[
        *[act(f'swat{j + 1}', [x_, 0, z_], 180 + a_, 'stand', 'determined', keys=[k(0.0, look=[0.0, 1.0, -8.0]),
            k(0.0, toon={'reach': {'R': [*loc([x_, 0, z_], 180 + a_, [-0.05, 1.45, 0.55]), 1, 0.03], 'L': [*loc([x_, 0, z_], 180 + a_, [0.08, 1.4, 0.3]), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'},
                         'bend': {'spine': [0.25, 0, 0, 1, None], 'legL': [-0.4, 0, 0, 1, None], 'shinL': [0.7, 0, 0, 1, None], 'legR': [-0.4, 0, 0, 1, None], 'shinR': [0.7, 0, 0, 1, None]}, 'sq': [1.04, 0.92, 1.04]}, toonDur=0.0),
            k(r(0.3 + 0.08 * j), to=[r(x_ * 0.85), 0, r(z_ - 0.35)], dur=0.3, ease='inOut', glide=True, face='keep')]) for j, (x_, z_, a_) in enumerate(RING4)]],
        props=[P('blk4', 'holedBlock', pos=DOOR4, opts={'w': 6.0, 'h': 10.0, 'holeAt': 99.0}),
               *[P(f'lampe4{j}', 'tacLight', pos=loc([x_, 0, z_], 180 + a_, [-0.05, 1.45, 0.45]), ry=180 + a_, opts={'len': 3.2, 'r': 0.5},
                   keys=[k(r(0.3 + 0.08 * j), to=loc([r(x_ * 0.85), 0, r(z_ - 0.35)], 180 + a_, [-0.05, 1.45, 0.45]), dur=0.3, ease='inOut')]) for j, (x_, z_, a_) in enumerate(RING4)]],
        cams=[cam(0.0, [3.6, 1.7, -7.4], [3.5, 1.7, -7.3], [-0.4, 1.1, -5.4], [-0.4, 1.1, -5.4], lens=56)])
st.cue('sfx:rotor', 'S04', 0.0, 0.3); st.cue('sfx:stepRun', 'S04', 0.3, 0.2)

# 5: the table refused to comply. Inside, the living room door from the side of the table: a canister rolls in onto the rug and BANG: a white flash
#    fills the room
D5 = st.dur('S05'); BANG5 = 0.36
st.shot('S05', 'livingRoom', setOpts={'tv': False, 'carpet': False},
        props=[TBL('t5', T1),
               P('flash5', 'flashBang', pos=[0.9, 0.5, -0.6], opts={'at': BANG5, 'r': 2.4, 'fade': 0.3})],
        fx=[{'type': 'flash', 'at': BANG5, 'dur': 0.18}, {'type': 'shake', 'at': BANG5, 'dur': 0.2, 'amount': 0.02}],
        cams=[cam(0.0, [-1.3, 0.9, 2.4], [-1.25, 0.9, 2.25], [0.4, 0.35, -0.5], [0.4, 0.35, -0.5], lens=52)])
st.cue('sfx:rattleShort', 'S05', 0.0, 0.2); st.cue('sfx:punch', 'S05', BANG5, 0.55); st.cue('thunder', 'S05', BANG5, 0.3)

# 6: (on « refusé ») the smoke clears: the table is exactly where it was; behind it four men in gas masks crouch, rifles aimed at it; one leans in
#    and peers at it; the table does not move
D6 = st.dur('S06')
AIM6 = [(-1.5, -1.2, 35), (-0.5, -1.6, 12), (0.6, -1.6, -12), (1.6, -1.2, -35)]
st.shot('S06', 'livingRoom', setOpts={'tv': False, 'carpet': False}, actors=[
        *[act(f'swat{j + 1}', [x_, 0, z_], a_, 'stand', 'determined', keys=[k(0.0, look=[0.0, 0.42, 0.0]),
            k(0.0, toon={'reach': {'R': [*loc([x_, 0, z_], a_, [-0.05, 1.3, 0.55]), 1, 0.03], 'L': [*loc([x_, 0, z_], a_, [0.08, 1.25, 0.3]), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'},
                         'bend': {'spine': [0.3, 0, 0, 1, None], 'legL': [-0.5, 0, 0, 1, None], 'shinL': [0.9, 0, 0, 1, None], 'legR': [-0.5, 0, 0, 1, None], 'shinR': [0.9, 0, 0, 1, None]}, 'sq': [1.04, 0.9, 1.04]}, toonDur=0.0),
            *([k(0.55, toon={'reach': {'R': [*loc([x_, 0, z_], a_, [-0.05, 1.0, 0.75]), 1, 0.03], 'L': [*loc([x_, 0, z_], a_, [0.08, 0.95, 0.5]), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'},
                             'bend': {'spine': [0.7, 0, 0, 1, None], 'legL': [-0.6, 0, 0, 1, None], 'shinL': [1.1, 0, 0, 1, None], 'legR': [-0.6, 0, 0, 1, None], 'shinR': [1.1, 0, 0, 1, None]}, 'sq': [1.04, 0.9, 1.04]}, toonDur=0.35, toonEase='inOut')] if j == 2 else [])])
          for j, (x_, z_, a_) in enumerate(AIM6)]],
        props=[TBL('t6', T1), *[P(f'lampe6{j}', 'tacLight', pos=loc([x_, 0, z_], a_, [-0.05, 1.3, 0.45]), ry=a_, opts={'len': 1.2, 'r': 0.25, 'beam': 0.12}) for j, (x_, z_, a_) in enumerate(AIM6)]],
        cams=[cam(0.0, [0.3, 1.3, 3.0], [0.28, 1.28, 2.8], [0.0, 1.0, -0.7], [0.0, 0.98, -0.7], lens=52)])
st.cue('sfx:static', 'S06', 0.0, 0.08)

# 7: so a tank. His street by day, low on the road: the block's facade at the end, the tank rumbling toward it from the camera's side, its gun level;
#    the ground shakes at each turn of its tracks
D7 = st.dur('S07'); B1 = [0.0, 0, -9.0]   # his block (front at z -9, facing +Z)
st.shot('S07', 'parisStreet', setOpts=STREET, fx=[{'type': 'shake', 'at': t_, 'dur': 0.12, 'amount': 0.008} for t_ in (0.2, 0.5, 0.8)], actors=[],
        props=[P('blk7', 'holedBlock', pos=B1, opts={'w': 6.0, 'h': 10.0, 'hole': [0.0, 1.05, 1.4], 'holeAt': 99.0}),
               P('char7', 'battleTank', pos=[0.0, 0, 3.0], ry=180, scale=0.72, keys=[k(0.0, to=[0.0, 0, -3.2], dur=D7, ease='linear')], opts={'rumble': [[0.0, 9.0, 0.02]]})],
        cams=[cam(0.0, [2.2, 0.8, 7.5], [2.0, 0.85, 6.6], [0.0, 2.2, -6.0], [0.0, 2.2, -7.0], lens=46)])
st.cue('engine', 'S07', 0.0, 0.4)

# 8: entered through the facade. Closer on the facade, three-quarter: the tank drives straight into it: CRASH, a round hole bursts open, bricks fly
#    at us in a cloud of dust; the tank disappears inside
D8 = st.dur('S08'); HIT8 = 0.3
st.shot('S08', 'parisStreet', setOpts=STREET, fx=[{'type': 'shake', 'at': HIT8, 'dur': 0.3, 'amount': 0.025}], actors=[],
        props=[P('blk8', 'holedBlock', pos=B1, opts={'w': 6.0, 'h': 10.0, 'hole': [0.0, 1.05, 1.4], 'holeAt': HIT8}),
               P('char8', 'battleTank', pos=[0.0, 0, -5.0], ry=180, scale=0.72, keys=[k(0.0, to=[0.0, 0, -11.1], dur=D8, ease='linear')], opts={'rumble': [[0.0, 9.0, 0.02]]}),
               P('briques8', 'brickBurst', pos=[0.0, 1.05, -8.9], opts={'at': HIT8, 'n': 30, 'floor': 1.05, 'speed': 5.5})],
        cams=[cam(0.0, [3.8, 1.2, -0.6], [3.6, 1.2, -1.0], [0.0, 2.2, -9.0], [0.0, 2.2, -9.0], lens=46)])
st.cue('engine', 'S08', 0.0, 0.3); st.cue('sfx:crunch', 'S08', HIT8, 0.6); st.cue('thunder', 'S08', HIT8, 0.35)

# 9: it came out three buildings further on. From the far side, low and almost in line with the tank's path: three blocks one behind another, the
#    nearest the lowest, their roofs stepping up; a round hole already through the far two; the near one's back wall bursts and the tank comes out at
#    us, the table balanced on the end of its gun
D9 = st.dur('S09'); OUT9 = 0.45
BL9 = [(-4.0, 7.0), (-11.0, 11.0), (-18.0, 15.0)]   # (front z, height): the blocks face the camera, the side the tank comes out of; the nearest is the third block
st.shot('S09', 'parisStreet', setOpts=STREET, fx=[{'type': 'shake', 'at': OUT9, 'dur': 0.3, 'amount': 0.02}], actors=[],
        props=[*[P(f'blk9{j}', 'holedBlock', pos=[0.0, 0, z_], opts={'w': 6.0, 'h': h_, 'd': 4.0, 'hole': [0.0, 1.05, 1.4], **({'holeAt': OUT9} if j == 0 else {}), 'color': ['#EBDDC4', '#E6D3D3', '#DCE3EA'][j]})
                 for j, (z_, h_) in enumerate(BL9)],
               P('char9', 'battleTank', pos=[0.0, 0, -8.8], ry=0, scale=0.72, keys=[k(0.0, to=[0.0, 0, 1.1], dur=D9, ease='linear')], opts={'rumble': [[0.0, 9.0, 0.02]]}),
               P('t9', 'coffeeTable', pos=[0.0, 1.08, -6.46], keys=[k(0.0, to=[0.0, 1.08, 3.44], dur=D9, ease='linear')]),
               P('briques9', 'brickBurst', pos=[0.0, 1.05, -3.9], opts={'at': OUT9, 'n': 30, 'floor': 1.05, 'speed': 5.0})],
        cams=[cam(0.0, [2.6, 1.8, 17.0], [2.4, 1.8, 16.0], [0.0, 4.2, -10.0], [0.0, 3.8, -10.0], lens=46)])
st.cue('engine', 'S09', 0.0, 0.35); st.cue('sfx:crunch', 'S09', OUT9, 0.55)

# 10: four pairs of handcuffs. On the pavement, three-quarter front: four soldiers, each cuffed to a leg of the table, carry it toward us like a
#     stretcher, in step; behind them the tank driver, in his padded helmet, hops on one foot holding his toe (ARRÊTÉE)
D10 = st.dur('S10'); TB10 = [0.0, 0.62, 0.0]
SOL10 = [(0.95, 0.3), (-0.95, 0.3), (0.95, -0.34), (-0.95, -0.34)]
def sold10(j, x_, z_):
    side = 1 if x_ > 0 else -1; hand = 'R' if side < 0 else 'L'; legp = [r(side * 0.46), 0.95, r(0.21 if z_ > 0 else -0.21)]
    return act(f'sold{j + 1}', [x_, 0, r(z_ - 1.2)], 0, 'stand', 'determined', keys=[k(0.0, look='camera'),
        k(0.0, to=[x_, 0, r(z_ + 0.4)], dur=D10, clip='walk', ease='linear'),
        *[k(r(t_), toon={'reach': {hand: [legp[0], legp[1], r(legp[2] - 1.2 + 1.6 * t_ / D10), 1, 0.03]}, 'hands': {hand: 'grip'}}, toonDur=0.2) for t_ in (0.0, D10 * 0.5, D10)]])
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[*[sold10(j, x_, z_) for j, (x_, z_) in enumerate(SOL10)],
        act('pilote', [1.9, 0, -2.2], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), *sum(hop_hold(0.0, [[1.9, -2.2], [1.7, -1.95], [1.95, -1.7], [1.75, -1.45], [1.95, -1.2]], 0.3, 0.2, 0, PAIN), [])])],
        props=[P('t10', 'coffeeTable', pos=[0.0, 0.55, -1.2], opts={'cuffs': True}, keys=[k(0.0, to=[0.0, 0.55, 0.4], dur=D10, ease='linear')]),
               *[CUFF(f'cuff10{j}', f'sold{j + 1}', 'R' if x_ < 0 else 'L') for j, (x_, _) in enumerate(SOL10)],
               *[KEPI(f'kepi10{j}', f'sold{j + 1}') for j in range(4)],
               P('casque10', 'tankHelmet', on={'actor': 'pilote', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'s': 0.82})],
        cams=[FC(0.0, [1.4, 2.9, 4.6], [[1.0, 2.5, 0.4], [-1.0, 2.5, 0.4], [1.0, 0.0, 0.4], [-1.0, 0.0, 0.4], [1.9, 2.6, -1.4], [1.9, 0.0, -2.2]], top=0.1, bottom=0.76, lenses=range(30, 70))])
st.cue('sfx:cuff', 'S10', 0.1, 0.3); st.cue('sfx:cuff', 'S10', 0.22, 0.25)
for i in range(4): st.cue('sfx:stepHeavy', 'S10', r(0.1 + 0.3 * i), 0.15); st.cue('thud', 'S10', r(0.3 + 0.3 * i), 0.08)

# 11: the tank driver was decorated. A square in the sun, flags, a three-man band playing behind; the general pins a medal on the driver's chest; the
#     driver salutes, balanced on one leg, his left foot in a big plaster cast held up behind him; he wobbles
D11 = st.dur('S11'); PIN11 = 1.0; PIL11 = [0.2, 0, 0.0]; GEN11 = [-0.75, 0, 0.3]
BEATS11 = [r(0.15 + 0.3 * i) for i in range(7)]
CHEST11 = loc(PIL11, -10, [0.12, 1.78, 0.17])
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('pilote', PIL11, -10, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.05, clip='salute'),
            *[k(r(0.0 + 0.25 * i), toon={'bend': {'legL': [0.55, 0.05, 0, 1, None], 'shinL': [1.2, 0, 0, 1, None]}, 'lay': [0.0, r(0.06 * (-1) ** i)], 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.25, toonEase='inOut') for i in range(8)]]),
        act('general', GEN11, 55, 'stand', 'determined', keys=[k(0.0, look=[CHEST11[0], CHEST11[1], CHEST11[2]]),
            k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(r(PIN11 - 0.35), toon={'reach': {'R': [r(CHEST11[0] - 0.06), CHEST11[1], r(CHEST11[2] + 0.06), 1, 0.03]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.3, toonEase='out'),
            k(r(PIN11 + 0.12), toon={'reach': {'R': [r(CHEST11[0] - 0.06), CHEST11[1], r(CHEST11[2] + 0.06), 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.06),
            k(r(PIN11 + 0.35), toon={'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.25), k(r(PIN11 + 0.4), look='camera')]),
        *[act(f'musi{j + 1}', [r(-1.6 + 1.4 * j), 0, -2.6], r(15 - 15 * j), 'stand', 'neutral', keys=[k(0.0, look='camera'), *[k(b_, toon={'sq': [1.03, 0.95, 1.03], 'face': {'lid': 0.5, 'mouth': 'kiss' if j == 0 else 'line'}}, toonDur=0.06) for b_ in BEATS11],
            *[k(r(b_ + 0.12), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.4, 'mouth': 'kiss' if j == 0 else 'line'}}, toonDur=0.1) for b_ in BEATS11]]) for j in range(3)]],
        props=[CAST('platre11', 'pilote'), P('casque11', 'tankHelmet', on={'actor': 'pilote', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'s': 0.82}),
               P('medaille11', 'medal', on={'actor': 'pilote', 'joint': 'torso', 'offset': [0.12, 0.6, 0.17]}, scale=2.2, keys=[k(0.0, visible=False), k(PIN11, visible=True)]),
               KEPI('kepi11g', 'general', color='#2B3A2A', band='#E2B53C'),
               P('instr110', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11], 'rot': [-0.3, -0.85, 0.0]}, opts={'kind': 'trumpet', 'beat': BEATS11[::2], 's': 1.15}),
               P('instr111', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.3, 0.0]}, opts={'kind': 'sousa', 'beat': BEATS11[::2]}),
               P('instr112', 'bandInstr', on={'actor': 'musi3', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': BEATS11}),
               P('drap11', 'flagPole', pos=[2.2, 0, -3.4], opts={'h': 5.0})],
        cams=[FC(0.0, [0.7, 1.4, 4.0], [[0.6, 2.6, 0.0], [0.2, 0.0, 0.0], [-1.0, 2.6, 0.3], [-0.75, 0.0, 0.3]], top=0.1, bottom=0.76, lenses=range(30, 70))])
st.cue('sfx:fanfare', 'S11', 0.0, 0.35); st.cue('sfx:clink', 'S11', PIN11, 0.3)

# courtroom: the dock at the front left, the table in it between two gendarmes, the judge at the bench at the back, the jury on the right
DOCK = [-1.4, 0, 1.4]; TD = [-1.4, 0.0, 1.38]; DH = 0.7; SH_ = 0.74   # the dock's panel and the stand the table stands on   # the table stands in the dock (the dock's panel 0.95 m: the table's top shows over the rail on a stand)
STAND = lambda pid, p: P(pid, 'table', pos=p, opts={'w': 0.9, 'd': 0.55, 'h': SH_, 'color': '#6B4426', 'legs': '#5A3820'})   # a low stand inside the dock lifts the table over the rail
GEND = [(-2.35, 1.25, 20), (-0.45, 1.25, -20)]
def gend_actors(look_keys=()):
    return [act(f'gend{j + 1}', [x_, 0, z_], a_, 'stand', 'determined', keys=[k(0.0, look='camera'), *(look_keys[j] if look_keys else [])]) for j, (x_, z_, a_) in enumerate(GEND)]

# 12: at the trial. The courtroom from the back, high: the judge at the bench, the dock at the front left, the coffee table standing in it on a low
#     stand, a gendarme each side; the judge leans forward and peers at it
D12 = st.dur('S12')
st.shot('S12', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[act('juge', [0.0, 0.3, -4.35], 0, 'stand', 'neutral', keys=[k(0.0, look=[TD[0], 1.0, TD[2]]), k(0.6, toon={'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.4)]),
        *gend_actors([[k(0.7, look=[TD[0], 0.9, TD[2]], lookDur=0.3)], [k(0.4, look=[0.0, 1.8, -4.3], lookDur=0.3), k(1.1, look='camera', lookDur=0.2)]])],
        props=[GKEPI('kepi12a', 'gend1'), GKEPI('kepi12b', 'gend2'), P('box12', 'dockBox', pos=DOCK, opts={'h': DH}), STAND('stand12', [DOCK[0], 0, DOCK[2] - 0.05]), TBL('t12', [TD[0], SH_, TD[2]])],
        cams=[cam(0.0, [-2.6, 3.2, 5.6], [-2.58, 3.15, 5.3], [-0.6, 1.0, -1.5], [-0.6, 1.0, -1.5], lens=50)])
st.cue('sfx:crickets', 'S12', 0.0, 0.05)

# 13: no remorse. Close on the dock: the table between the two gendarmes, a slow push-in; the one on the right turns his eyes to it, then his head,
#     and back to us; the table does not move
D13 = st.dur('S13')
st.shot('S13', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=gend_actors([[], [k(0.25, look=[TD[0], 0.9, TD[2]], lookDur=0.25), k(0.75, look='camera', lookDur=0.15)]]),
        props=[GKEPI('kepi13a', 'gend1'), GKEPI('kepi13b', 'gend2'), P('box13', 'dockBox', pos=DOCK, opts={'h': DH}), STAND('stand13', [DOCK[0], 0, DOCK[2] - 0.05]), TBL('t13', [TD[0], SH_, TD[2]])],
        cams=[cam(0.0, [-1.05, 1.7, 5.8], [-1.1, 1.65, 5.2], [-1.4, 1.5, 1.3], [-1.4, 1.5, 1.3], lens=48)])

# 14: the defence pleaded it was there first. From high over the aisle: the lawyer at the far end flings a roll toward us and it unrolls down the
#     aisle: a plan of the living room, the table drawn in its place and a trail of footprints walking straight into it with a red star; on the right
#     the three jurors lean in at once
D14 = st.dur('S14'); PLAN14 = [0.0, 0.02, -1.8]
JURY = [(2.1, -1.9, -70), (2.3, -1.0, -80), (2.45, -0.1, -95)]
st.shot('S14', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[
        act('avocat', [0.0, 0, -2.3], 0, 'stand', 'determined', keys=[k(0.0, look=[0.0, 0.0, 0.0]),
            k(0.0, toon={'reach': {'L': [0.15, 0.6, -1.9, 1, 0.03], 'R': [-0.15, 0.6, -1.9, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.6, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.25, toon={'reach': {'L': [0.4, 1.3, -1.4, 1, 0.03], 'R': [-0.4, 1.3, -1.4, 1, 0.03]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'open', 'brow': 0.6}}, toonDur=0.15, toonEase='out'),
            k(1.1, toon={'reach': {'L': [0.55, 1.5, -1.8, 1, 0.03]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.3), k(1.3, look='camera')]),
        *[act(f'jure{j + 1}', [x_, 0, z_], a_, 'sit', 'neutral', keys=[k(0.0, look=[0.0, 0.0, z_]), k(r(1.25 + 0.04 * j), toon={'bend': {'spine': [0.55, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1.3, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.2, toonEase='out')])
          for j, (x_, z_, a_) in enumerate(JURY)]],
        props=[P('plan14', 'planScroll', pos=PLAN14, rot=[-PI / 2, 0, 0], opts={'w': 1.6, 'len': 3.4, 'unroll': [[0.2, 0.02], [0.95, 1.0]]}),
               P('banc14', 'dockBox', pos=[2.75, 0, -1.0], ry=-90, opts={'w': 2.8, 'd': 0.6, 'h': 0.6, 'color': '#6E4A2E'})],
        cams=[cam(0.0, [-0.9, 4.4, 3.9], [-0.85, 4.35, 3.7], [0.5, 0.8, -1.1], [0.5, 0.8, -1.15], lens=52)])
st.cue('sfx:paper', 'S14', 0.25, 0.35); st.cue('sfx:gasp', 'S14', 1.27, 0.3)

# 15: twenty years. Close on the dock: a giant stamp drops onto the table: its legs crush flat for a frame and spring back (CONDAMNÉE); the gendarmes
#     flinch
D15 = st.dur('S15'); STAMP15 = 0.3
st.shot('S15', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=gend_actors([[k(r(STAMP15 + 0.02), toon={'sq': [1.08, 0.88, 1.08], 'face': {'lid': 1.0, 'mouth': 'clench'}}, toonDur=0.04), k(r(STAMP15 + 0.3), toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.15)]] * 2),
        props=[GKEPI('kepi15a', 'gend1'), GKEPI('kepi15b', 'gend2'), P('box15', 'dockBox', pos=DOCK, opts={'h': DH}), STAND('stand15', [DOCK[0], 0, DOCK[2] - 0.05]),
               TBL('t15', [TD[0], SH_, TD[2]], squash=[[0.0, 0.0], [r(STAMP15 - 0.01), 0.0], [STAMP15, 1.0], [r(STAMP15 + 0.1), 1.0], [r(STAMP15 + 0.2), -0.25], [r(STAMP15 + 0.32), 0.08], [r(STAMP15 + 0.42), 0.0]]),
               P('tampon15', 'bigStamp', pos=[TD[0], 4.2, TD[2]], scale=4.0, keys=[k(r(STAMP15 - 0.12), to=[TD[0], r(SH_ + 0.42 * 0.25 + 1.46), TD[2]], dur=0.12, ease='in'), k(r(STAMP15 + 0.18), to=[TD[0], 4.4, TD[2]], dur=0.3, ease='out')])],
        fx=[{'type': 'shake', 'at': STAMP15, 'dur': 0.2, 'amount': 0.025}],
        cams=[cam(0.0, [0.5, 2.9, 4.4], [0.45, 2.88, 4.25], [-1.4, 1.3, 1.3], [-1.4, 1.3, 1.3], lens=40)])
st.cue('sfx:gavel', 'S15', 0.0, 0.35); st.cue('clack', 'S15', STAMP15, 0.55); st.cue('thud', 'S15', STAMP15, 0.4); st.cue('sfx:boing', 'S15', r(STAMP15 + 0.18), 0.2)

# 16: in prison, it reoffended. Top down on the cell: the table in the middle; three guards hop round it in a circle, each holding a foot
D16 = st.dur('S16')
def ring16(j):
    pts = []
    for i in range(7):
        a_ = math.radians(j * 120 + i * 20); pts.append([r(1.0 * math.cos(a_)), r(0.15 + 0.9 * math.sin(a_))])
    ry_ = j * 120 + 90
    kk, tt = hop_hold(r(0.04 * j), pts, 0.28, 0.18, -(j * 120) - 90 + 180, PAIN)
    return act(f'gard{j + 1}', [pts[0][0], 0, pts[0][1]], -(j * 120) - 90 + 180, 'stand', 'neutral', keys=[k(0.0, look='camera'), *kk, *tt])
st.shot('S16', 'brightCell', setOpts={'w': 4.0, 'd': 4.0, 'h': 7.5}, actors=[ring16(j) for j in range(3)],
        props=[TBL('t16', [0.0, 0, 0.15])],
        cams=[cam(0.0, [0.3, 4.3, 3.3], [0.28, 4.25, 3.2], [0.0, 0.7, 0.0], [0.0, 0.7, 0.0], lens=55)])
for i in range(6): st.cue('thud', 'S16', r(0.28 * i + 0.25), 0.1)
st.cue('sfx:grunt', 'S16', 0.3, 0.2)

# 17: three guards. Life. In the corridor outside the cell, front: the three guards in a staggered row, each on a crutch, a plaster cast on the left
#     foot held up, saluting; on « Perpétuité » a giant stamp slams onto the white plate of the cell door beside them and leaves PERPÉTUITÉ in red;
#     they flinch and hold the salute
D17 = st.dur('S17'); ST17 = r(st.at('S17', 'L13', 2) + 0.02)
DOOR17 = [0.25, 0, 0.0]; PLATE17 = [r(DOOR17[0] + 0.45), r(2.15 * 0.62), r(DOOR17[2] + 0.08)]   # the door's hinge (it spans +X 0.9 m) and its plate
GD17 = [(-1.45, 1.15, 15), (-0.85, 0.8, 8), (-0.2, 1.45, -5)]
st.shot('S17', 'brightCell', setOpts={'w': 4.0, 'd': 3.0, 'bars': False}, actors=[
        *[act(f'gard{j + 1}', [x_, 0, z_], a_, 'stand', 'determined', keys=[k(0.0, look='camera'), k(r(0.1 + 0.08 * j), clip='salute'),
            k(0.0, toon={'bend': {'legL': [0.5, 0.05, 0, 1, None], 'shinL': [1.0, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(r(ST17 + 0.03), toon={'bend': {'legL': [0.5, 0.05, 0, 1, None], 'shinL': [1.0, 0, 0, 1, None]}, 'sq': [1.06, 0.92, 1.06], 'face': {'lid': 1.0, 'mouth': 'clench'}}, toonDur=0.04),
            k(r(ST17 + 0.3), toon={'bend': {'legL': [0.5, 0.05, 0, 1, None], 'shinL': [1.0, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.15)]) for j, (x_, z_, a_) in enumerate(GD17)]],
        props=[*[CAST(f'platre17{j}', f'gard{j + 1}') for j in range(3)],
               *[P(f'bequille17{j}', 'crutch', on={'actor': f'gard{j + 1}', 'hand': 'L', 'offset': [0.0, -0.02, 0.0]}) for j in range(3)],
               P('barreaux17', 'jailBars', pos=[-1.0, 0, 0.0], opts={'width': 2.4, 'height': 2.8}), P('porte17', 'barDoor', pos=DOOR17, opts={'w': 0.9, 'open': 0.0, 'plate': True}),
               P('tampon17', 'bigStamp', pos=[PLATE17[0], PLATE17[1], r(PLATE17[2] + 1.75)], rot=[PI / 2, 0, 0], scale=3.0, keys=[k(0.0, visible=False), k(r(ST17 - 0.12), visible=True),
                   k(r(ST17 - 0.12), to=[PLATE17[0], PLATE17[1], r(PLATE17[2] + 1.12)], dur=0.12, ease='in'), k(r(ST17 + 0.25), to=[PLATE17[0], 4.6, r(PLATE17[2] + 1.6)], dur=0.3, ease='in')]),
               P('marque17', 'stampMark', pos=[PLATE17[0], PLATE17[1], r(PLATE17[2] + 0.02)], opts={'text': 'PERPÉTUITÉ', 'w': 0.66, 'h': 0.24}, keys=[k(0.0, visible=False), k(ST17, visible=True)])],
        fx=[{'type': 'shake', 'at': ST17, 'dur': 0.2, 'amount': 0.02}],
        cams=[cam(0.0, [-0.3, 2.0, 4.5], [-0.32, 2.0, 4.45], [-0.3, 1.15, 0.5], [-0.3, 1.15, 0.5], lens=66)])
st.cue('clack', 'S17', ST17, 0.6); st.cue('thud', 'S17', ST17, 0.35); st.cue('clang', 'S17', r(ST17 + 0.02), 0.3)

# 18: on appeal, the table had an X-ray. The radiology room: the table lies on its back on the X-ray table, legs in the air; a doctor at the light
#     box; on « radio » the box blinks on: the X-ray of a table, glowing; the doctor points at it, then looks at us
D18 = st.dur('S18'); XR18 = r(st.at('S18', 'L14', 7) - 0.05); BED = [-0.5, 0, -0.6]; UP = [BED[0], r(0.84 + 0.42), BED[2]]   # the table upside down (turned about Z: the bruise faces us)
st.shot('S18', 'hospital', setOpts={'monitor': False}, actors=[
        act('docteur', [1.25, 0, -0.2], -30, 'stand', 'neutral', keys=[k(0.0, look=[BED[0], 1.0, BED[2]]), k(0.0, toon={'reach': {'L': [0.8, 1.3, -0.15, 1, 0.03]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0), k(0.5, look=[BED[0] + 0.4, 1.3, BED[2]], lookDur=0.3),
            k(r(XR18 + 0.05), look=[0.6, 1.6, -1.5], lookDur=0.15),
            k(r(XR18 + 0.1), toon={'reach': {'R': [0.95, 1.65, -1.0, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.2), k(r(XR18 + 0.55), look='camera', lookDur=0.12)])],
        props=[P('lit18', 'xrayBed', pos=BED), P('t18', 'coffeeTable', pos=UP, rot=[0, 0, PI], opts={'bruise': True}),
               P('ecran18', 'xrayScreen', pos=[0.55, 0, -1.65], ry=-8, opts={'at': XR18})],
        cams=[FC(0.0, [-0.3, 1.8, 4.0], [[r(BED[0] - 1.0), 0.8, BED[2]], [r(BED[0] + 1.0), 0.8, BED[2]], [BED[0], 1.4, BED[2]], [-0.15, 2.15, -1.65], [1.25, 2.15, -1.65], [1.25, 2.55, -0.2], [1.25, 0.0, -0.2]], top=0.12, bottom=0.76, lenses=range(30, 70))])
st.cue('sfx:beep', 'S18', XR18, 0.3); st.cue('sfx:click', 'S18', r(XR18 - 0.02), 0.2)

# 19: it had a bruise. Extreme close-up on one leg of the upturned table: a blue bruise on the wood; a yellow evidence marker pops up beside it
D19 = st.dur('S19'); BRU19 = [r(BED[0] - 0.46), r(UP[1] - 0.36 * 0.55), r(BED[2] + 0.21 + 0.04)]   # the bruised leg after the turn about Z: x mirrored, pointing up
st.shot('S19', 'hospital', setOpts={'monitor': False},
        props=[P('lit19', 'xrayBed', pos=BED), P('t19', 'coffeeTable', pos=UP, rot=[0, 0, PI], opts={'bruise': True, 'legT': 0.09}),
               MARK('m19', [r(BRU19[0] + 0.15), 0.84, r(BRU19[2] + 0.05)], 5, 0.3, ry=-15, s=0.9)],
        cams=[cam(0.0, [r(BRU19[0] + 0.12), r(BRU19[1] + 0.06), r(BRU19[2] + 0.62)], [r(BRU19[0] + 0.11), r(BRU19[1] + 0.06), r(BRU19[2] + 0.55)], [r(BRU19[0] + 0.06), r(BRU19[1] - 0.05), BRU19[2]], [r(BRU19[0] + 0.06), r(BRU19[1] - 0.05), BRU19[2]], lens=40)])
st.cue('sfx:pop', 'S19', 0.3, 0.25); st.cue('sfx:sting', 'S19', 0.05, 0.2)

# 20: this man was convicted. Now he stands in the dock, in his suit, barefoot, between the gendarmes; the gavel falls (heard), COUPABLE lands and he
#     staggers back as if hit in the chest
D20 = st.dur('S20'); HIT20 = 0.74
st.shot('S20', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[
        act('mec', [DOCK[0], 0, r(DOCK[2] - 0.15)], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(HIT20, toon={'lay': [-0.3, 0.0], 'sq': [0.9, 1.12, 0.9], 'reach': {'R': [r(DOCK[0] - 0.05), 1.65, r(DOCK[2] + 0.05), 1, 0.03]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out'),
            k(r(HIT20 + 0.25), toon={'lay': [-0.1, 0.0], 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.2, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.15),
            k(r(HIT20 + 0.6), toon={'lay': [0.0, 0.0], 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.25)]), *gend_actors()],
        props=[GKEPI('kepi20a', 'gend1'), GKEPI('kepi20b', 'gend2'), P('box20', 'dockBox', pos=DOCK)],
        fx=[{'type': 'shake', 'at': HIT20, 'dur': 0.15, 'amount': 0.015}],
        cams=[FC(0.0, [-0.9, 1.6, 5.0], [[DOCK[0], 2.6, DOCK[2]], [DOCK[0], 0.9, r(DOCK[2] + 0.5)], [-2.35, 2.55, 1.25], [-0.45, 2.55, 1.25], [-2.35, 0.9, 1.25], [-0.45, 0.9, 1.25]], top=0.12, bottom=0.72)])
st.cue('sfx:gavel', 'S20', r(HIT20 - 0.05), 0.5); st.cue('sfx:punch', 'S20', HIT20, 0.25)

# 21: (on « coups et blessures ») the plaintiff: the coffee table on the courtroom floor, low and close, a white bandage wound round its front leg, an
#     evidence marker beside it; a gendarme kneels by it and pats its top, then looks at us; the table does not move
D21 = st.dur('S21'); PL21 = [0.6, 0, 2.6]
st.shot('S21', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[
        act('gend2', [r(PL21[0] - 0.85), 0, r(PL21[2] - 0.45)], 55, 'kneel', 'neutral', keys=[k(0.0, look=[PL21[0], 0.4, PL21[2]]),
            *[k(r(0.15 + 0.22 * i), toon={'reach': {'R': [r(PL21[0] - 0.3), r(0.47 + (0.06 if i % 2 == 0 else 0.0)), r(PL21[2] - 0.05), 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.1) for i in range(4)],
            k(0.75, look='camera', lookDur=0.2)])],
        props=[TBL('t21', PL21, bruise=True, bandage=True), GKEPI('kepi21', 'gend2'), MARK('m21', [r(PL21[0] + 0.75), 0, r(PL21[2] + 0.25)], 6, -1.0, ry=-20, s=1.2)],
        cams=[cam(0.0, [r(PL21[0] + 0.95), 0.95, r(PL21[2] + 2.0)], [r(PL21[0] + 0.93), 0.95, r(PL21[2] + 1.92)], [r(PL21[0] - 0.05), 0.78, PL21[2]], [r(PL21[0] - 0.05), 0.78, PL21[2]], lens=60)])

# 22: and of the three buildings. Behind the judge, the courtroom's back wall tips over and falls flat; behind it, in the daylight, the three blocks
#     in a row, the same round hole through all three
D22 = st.dur('S22'); FALL22 = 0.25
st.shot('S22', 'parisStreet', setOpts=STREET, actors=[act('juge', [-1.3, 0.3, -0.6], 15, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(r(FALL22 + 0.5), look=[0.0, 2.0, -14.0], lookDur=0.25)])],
        props=[P('banc22', 'courtBench', pos=[-1.3, 0, -0.3]), P('mur22', 'fallWall', pos=[0.0, 0, -1.6], opts={'w': 12.0, 'h': 6.0, 'at': FALL22}),
               *[P(f'blk22{j}', 'holedBlock', pos=[0.0, 0, z_], opts={'w': 6.0, 'h': h_, 'hole': [0.0, 1.05, 1.4], 'color': ['#EBDDC4', '#E6D3D3', '#DCE3EA'][j]}) for j, (z_, h_) in enumerate([(-11.0, 7.0), (-18.0, 11.0), (-25.0, 15.0)])]],
        cams=[cam(0.0, [0.3, 1.5, 7.5], [0.28, 1.5, 7.2], [-0.2, 3.4, -10.0], [-0.2, 3.6, -12.0], lens=50)])
st.cue('sfx:stretch', 'S22', 0.0, 0.2); st.cue('thunder', 'S22', r(FALL22 + 0.42), 0.4); st.cue('thud', 'S22', r(FALL22 + 0.42), 0.4)

# 23: his cellmate is the table. Inside the narrow cell, toward the bars: a guard shoves him in through the door; he stumbles toward us and stops at
#     the table, which stands across the cell between him and his bunk; he looks down at it, then at us; the door slams behind him
D23 = st.dur('S23'); SLAM23 = 1.15; TC = [0.0, 0, 0.2]
st.shot('S23', 'brightCell', setOpts={'w': 3.0, 'd': 4.4, 'bars': False}, actors=[
        act('mecP', [0.55, 0, 1.6], 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.42, 0.2]),
            k(0.05, toon={'lay': [0.25, 0.0], 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.08, toonEase='out'),
            k(0.05, to=[0.3, 0, 0.75], dur=0.35, ease='out', glide=True, face='keep'),
            k(0.45, toon={'lay': [0.0, 0.0], 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2, 'gy': 0.7}}, toonDur=0.2),
            k(0.85, look='camera', lookDur=0.15), k(0.85, toon={'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.15)]),
        act('gard1', [0.9, 0, 2.3], 200, 'stand', 'determined', keys=[k(0.0, look=[0.4, 1.4, 1.2]), k(0.0, toon={'reach': {'R': [0.65, 1.5, 1.65, 1, 0.03], 'L': [0.45, 1.45, 1.7, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}}, toonDur=0.0),
            k(0.25, toon={'reach': {'R': [0.6, 1.5, 1.35, 1, 0.03], 'L': [0.4, 1.45, 1.4, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}}, toonDur=0.1, toonEase='out'), k(0.55, toon={'hands': {'R': 'rest', 'L': 'rest'}}, toonDur=0.3)])],
        props=[TBL('t23', TC), P('barreaux23', 'jailBars', pos=[-0.45, 0, 2.1], opts={'width': 1.5, 'height': 2.8}), P('porte23', 'barDoor', pos=[0.3, 0, 2.1], opts={'w': 0.9, 'open': -1.6, 'slam': SLAM23})],
        cams=[cam(0.0, [-0.65, 1.3, -2.0], [-0.6, 1.29, -1.92], [0.25, 1.15, 1.2], [0.25, 1.15, 1.2], lens=66)])
st.cue('sfx:stepRun', 'S23', 0.1, 0.2); st.cue('clang', 'S23', SLAM23, 0.5)

# 24: he stubbed his toe again the first night. The cell, framed exactly like the first shot: his foot hits the table's leg, he hops on one foot
loop_shot('S24', 'brightCell', 'mecP', 0.65, setOpts={'w': 3.0, 'd': 4.8, 'bars': False})
st.cue('sfx:crickets', 'S24', 0.0, 0.08)

SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'gloves': '#F6F6F2', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'barefoot': True, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
st.write("La table basse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecP': {**MEC, 'preset': 'mecPrisonnier'},
    **{f'swat{j + 1}': {'preset': 'swat', 'seed': 801 + j, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},
    **{f'sold{j + 1}': {**SOLD, 'preset': 'cop' if j % 2 == 0 else 'cop2', 'seed': 805 + j} for j in range(4)},
    'pilote': {**SOLD, 'preset': 'cop', 'seed': 809, 'suit': '#4E5A32', 'facial': 'mustache'},
    'general': {'preset': 'politique', 'seed': 810, 'suit': '#4A5530', 'lapel': '#4A5530', 'tie': '#2E351E', 'glasses': False, 'facial': 'mustache', 'hairColor': '#9A9A96', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    **{f'musi{j + 1}': {'preset': 'serveur', 'seed': 811 + j, 'suit': '#B5302A', 'pants': '#1C1F2A', 'glasses': False, 'build': {'width': 1.0 + 0.1 * (j == 1), 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    **{f'gend{j + 1}': {'preset': 'cop', 'seed': 814 + j, 'suit': '#1F2A44', 'pants': '#1F2A44', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(2)},
    'avocat': {'preset': 'avocat', 'seed': 816, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jure1': {'preset': 'madame', 'seed': 817, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'jure2': {'preset': 'boss', 'seed': 818, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jure3': {'preset': 'mamie', 'seed': 819, 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    **{f'gard{j + 1}': {'preset': 'cop', 'seed': 820 + j, 'suit': '#4F6273', 'pants': '#3E4D5A', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    'docteur': {'preset': 'doctor', 'seed': 823, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
