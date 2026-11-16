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
CUFF = lambda pid, who, hand: P(pid, 'handcuffs', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.06, 0.0]}, scale=0.7)   # (review 2) bigger cuffs (15 px rings read as nothing)
CAST = lambda pid, who, foot='footL', s=1.45: P(pid, 'footCast', on={'actor': who, 'joint': foot, 'offset': [0.0, 0.02, 0.0]}, opts={'s': s, 'toes': True})
PAIN = {'lid': 0.85, 'mouth': 'O', 'brow': 0.9, 'blush': 0.6, 'sweat': 1.0}
HELM = lambda pid, who: P(pid, 'tacHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]})
VEST = lambda pid, who: P(pid, 'tacVest', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]})
MASK = lambda pid, who: P(pid, 'gasMask', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
KIT = lambda sid, who, mask=False: [HELM(f'helm{sid}{who}', who), VEST(f'vest{sid}{who}', who), *([MASK(f'mask{sid}{who}', who)] if mask else [])]
SEAL = lambda pid: P(pid, 'courtSeal', pos=[0.0, 4.08, -4.45], opts={'r': 0.42})   # (review 1) the scales of justice over the cross-like emblem above TRIBUNAL
DEAD = {'lid': 0.45, 'mouth': 'line'}
STREET = {'eiffelStyle': 'v2', 'clear': [-8.0, 8.0], 'clearL': [-8.0, 8.0]}

# the hop on one foot, holding the left foot: the left thigh up, the shin folded back, the spine bowed, both hands on the foot (the foot's place in
# his own frame, measured on a still); position keys from the bounces, toon keys at each take-off, top and landing carry the whole pose
FOOT = [0.09, 0.5, 0.41]; YAW = 0.6
def hold_pose(root, ry, face, sq=None, look=None, yaw=YAW):
    ry_ = ry + math.degrees(yaw)
    hl = loc(root, ry_, [FOOT[0] + 0.07, FOOT[1] + 0.06, FOOT[2] + 0.02]); hr = loc(root, ry_, [FOOT[0] - 0.06, FOOT[1] + 0.04, FOOT[2] + 0.07])
    t_ = {'bend': {'spine': [0.28, 0, 0, 1, None], 'legL': [-1.45, 0.1, 0, 1, None], 'shinL': [1.6, 0, 0, 1, None]}, 'yaw': yaw, 'auto': 0.15,
          'reach': {'L': [*hl, 1, 0.04], 'R': [*hr, 1, 0.04]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': face}
    if sq: t_['sq'] = sq
    return t_
def side_pose(root, ry, face, sq=None, look=None, yaw=0.0, foot=(0.42, 0.74, -0.1), out=(-0.62, 1.5, 0.12), lean=0.0):
    # (review 3) the figure-4 to the side: the hurt foot lifted out to his left (+X in his frame) at knee height by a planted point, held in his left
    # hand, the right arm flung out for balance; seen from S24's low camera it stands clear above the tabletop (the front-held foot of hold_pose hid
    # behind the top and both hands met at his crotch: « it reads as a blow to the groin »)
    ft = loc(root, ry, list(foot)); hl = loc(root, ry, [foot[0] - 0.02, foot[1] + 0.07, foot[2] + 0.04]); hr = loc(root, ry, list(out))
    t_ = {'plant': {'L': [*ft, 1]}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'auto': 0.15, 'reach': {'L': [*hl, 1, 0.04], 'R': [*hr, 1, 0.04]},
          'hands': {'L': 'grip', 'R': 'spread'}, 'face': face}
    if lean: t_['lay'] = [0.0, lean]
    if sq: t_['sq'] = sq
    return t_
def front_pose(root, ry, face, sq=None, look=None, yaw=0.0, foot=(0.1, 0.74, 0.42)):
    # (review 3) the held foot planted high in front (at hip height, not the knee), both hands on it: for a figure seen side-on (S16's guards)
    ft = loc(root, ry, list(foot)); hl = loc(root, ry, [foot[0] + 0.06, foot[1] + 0.06, foot[2] - 0.02]); hr = loc(root, ry, [foot[0] - 0.08, foot[1] + 0.05, foot[2] + 0.04])
    t_ = {'plant': {'L': [*ft, 1]}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'auto': 0.15, 'reach': {'L': [*hl, 1, 0.04], 'R': [*hr, 1, 0.04]},
          'hands': {'L': 'grip', 'R': 'grip'}, 'face': face}
    if sq: t_['sq'] = sq
    return t_
def hop_hold(t0, pts, dt, peak, ry, face, y0=0.0, sqL=0.07, yaw=YAW, pose=None):
    # (review 1) each toon key ends at least 0.02 s before the next one starts: where a key's blend ended on the very frame the next began, the
    # body folded flat for one frame at every take-off; the landing squash eases in over 0.06 s and out over 0.07 s, vertical (sq only)
    pose = pose or hold_pose
    keys, toon = [], []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; t = r(t0 + dt * i); m = [r((a[0] + b[0]) / 2), r(y0 + peak), r((a[1] + b[1]) / 2)]
        keys += [k(t, to=m, dur=r(dt / 2), ease='inOut', face='keep', glide=True), k(r(t + dt / 2), to=[b[0], y0, b[1]], dur=r(dt / 2), ease='inOut', face='keep', glide=True)]
        toon += [k(r(t + 0.01), toon=pose([a[0], y0, a[1]], ry, face, [1 - sqL * 0.7, 1 + sqL, 1 - sqL * 0.7], yaw=yaw), toonDur=0.07, toonEase='out'),
                 k(r(t + 0.1), toon=pose(m, ry, face, [1.0, 1.0, 1.0], yaw=yaw), toonDur=r(dt / 2 - 0.12), toonEase='inOut'),
                 k(r(t + dt - 0.08), toon=pose([b[0], y0, b[1]], ry, face, [1 + sqL, 1 - sqL, 1 + sqL], yaw=yaw), toonDur=0.06, toonEase='inOut')]
    return keys, toon

for g_ in [('S01', 0.75, 'mec', 'bonk'), ('S10', 0.6, 'pilote', 'hop'), ('S11', 1.2, 'pilote', 'medal'), ('S20', 0.9, 'mec', 'coupable'), ('S24', 0.7, 'mecP', 'bonk2')]:
    st.gag(*g_)
st.card('S10', 'ARRÊTÉE', at=0.3)
st.card('S15', 'CONDAMNÉE', at=0.32)
st.card('S20', 'COUPABLE', at=0.74)

# 1 and 24, the loop: low at floor level in front of the table (its long side across the frame); he walks toward us from the back of the room and
#    his left foot slams into the table's far right leg: BONK, a squash, stars; he springs up, his eyes pop out on stalks with headroom to spare, and
#    hops back on one foot holding his toe; the table, in the foreground, does not move; the painting (S01) and the barred window (S24) sit at the
#    same place on the right, off his head and arms; in S24 a warm bulb hangs in the top left corner
T1 = [0.0, 0, 0.0]; WALK_FROM = [0.42, 0, -2.0]; HIT_AT = [0.42, 0, -0.66]
HOPS1 = [[HIT_AT[0], HIT_AT[2]], [0.6, -0.92], [0.38, -1.18], [0.66, -1.36], [0.44, -1.54], [0.6, -1.66], [0.45, -1.78]]
def loop_shot(sid, set_, who, t_hit, setOpts=None, extra_props=(), hang=0.0, take=1.0, hops=HOPS1, bump=None, pose=None, wobble=0):
    # (review 1) a low camera (0.26 m, under the top, three-quarter from the right) sees the toe meet the far leg between the legs, with a shock
    # accent; `hang`: the pain registers that much later (S24: he stands with his toe on the leg, blank, then the bigger take); `bump`: the last hop
    # ends against the bunk and bounces off it
    D = st.dur(sid); walk = r(t_hit - 0.02); tp = r(t_hit + 0.16 + hang); th = r(tp + 0.14)
    POPF = {'lid': 0.0, 'eye': 0.5, 'pop': 1.0, 'popLen': r(min(0.3 * take, 0.34)), 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}   # (review 2) the stalks capped: S24's eyes went out of the top
    ks = [k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0),
          k(0.0, to=HIT_AT, dur=walk, clip='walk', ease='linear'),
          k(r(walk - 0.08), toon={'bend': {'legL': [-0.45, 0, 0, 1, None], 'shinL': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.06),
          k(t_hit, toon={'bend': {'legL': [-0.5, 0, 0, 1, None], 'shinL': [0.2, 0, 0, 1, None], 'spine': [-0.1, 0, 0, 1, None]}, 'sq': [1.1, 0.9, 1.1],
                         'face': ({'lid': 0.35, 'mouth': 'line'} if hang else {**POPF, 'popLen': 0.22})}, toonDur=0.04, toonEase='out')]   # the toe hits
    if hang:   # (S24) nothing for a beat: the toe on the leg, a slow blink, then the eyes widen
        ks += [k(r(t_hit + 0.08), toon={'bend': {'legL': [-0.5, 0, 0, 1, None], 'shinL': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.1),
               k(r(tp - 0.16), toon={'bend': {'legL': [-0.5, 0, 0, 1, None], 'shinL': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.08)]
    ks += [k(tp, toon={'bend': {'legL': [-0.9, 0, 0, 1, None], 'shinL': [1.2, 0, 0, 1, None]}, 'sq': [r(1 - 0.1 * take), r(1 + 0.15 * take), r(1 - 0.1 * take)],
                       'face': POPF}, toonDur=0.08, toonEase='out')]   # the pain arrives
    hk, ht = hop_hold(th, hops, 0.3, 0.2, 0, PAIN, pose=pose)
    ks += hk + ht + [k(th, look='camera')]
    tend = r(th + 0.3 * (len(hops) - 1))
    if bump:   # bounces off the bunk's edge: a squash and a step back
        pz = pose or hold_pose
        ks += [k(tend, to=bump, dur=0.14, ease='out', face='keep', glide=True),
               k(r(tend + 0.01), toon=pz([hops[-1][0], 0.0, hops[-1][1]], 0, PAIN, [1.12, 0.9, 1.12]), toonDur=0.04, toonEase='out'),
               k(r(tend + 0.08), toon={**pz(bump, 0, PAIN, [0.97, 1.03, 0.97]), 'settle': 0.8}, toonDur=0.12)]
        # (review 3) then he balances on one foot to the end, the hurt foot held out to the side, wobbling: a longer hang than S01's hops
        for i in range(wobble):
            ks.append(k(r(tend + 0.22 + 0.12 * i), toon=pz(bump, 0, {**PAIN, 'lid': 0.7 if i % 2 else 0.9}, [1.0, 1.0, 1.0], lean=r(0.07 * (-1) ** i)) if pz is side_pose else pz(bump, 0, PAIN), toonDur=0.1, toonEase='inOut'))
        st.cue('thud', sid, tend, 0.35)
    props = [TBL(f't{sid}', T1), P(f'stars{sid}', 'impactStars', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.62, 0.0]}, opts={'at': r(tp + 0.02), 'n': r(5 + 2 * (take - 1)) if take > 1 else 5}),
             P(f'toe{sid}', 'impactStars', pos=[0.47, 0.07, -0.27], opts={'at': r(t_hit + 0.01), 'n': 6, 'r': 0.22, 'dur': 0.35}),
             *extra_props]
    st.shot(sid, set_, setOpts=setOpts, actors=[act(who, WALK_FROM, 0, 'stand', 'neutral', keys=ks)], props=props,
            fx=[{'type': 'shake', 'at': t_hit, 'dur': 0.14, 'amount': 0.012}],
            cams=[cam(0.0, [1.3, 0.26, 1.9], [1.28, 0.26, 1.86], [0.3, 0.93, -0.8], [0.3, 0.94, -0.8], lens=71)])   # (review 2) headroom: lens 60 -> 71, aimed up 13 cm (the stretched head went out of the top)
    st.cue('sfx:stepSoft', sid, 0.15, 0.12); st.cue('sfx:stepSoft', sid, 0.45, 0.12)
    st.cue('sfx:bonk', sid, t_hit, 0.5); st.cue('sfx:gasp', sid, r(tp + 0.02), 0.3)
    for i in range(len(hops) - 1): st.cue('thud', sid, r(th + 0.3 * i + 0.28), 0.1)
loop_shot('S01', 'livingRoom', 'mec', 0.7, setOpts={'tv': False, 'carpet': False, 'pictureX': 0.8, 'pictureW': 1.0})   # (review 2) the painting moved right, off his walk and hops: S24's window sits at the same place in the frame

# 2: it was premeditated. The table alone in the empty room, a slow push-in at knee height; a lamp swings over it; four yellow evidence markers pop
#    up round its legs one after another
D2 = st.dur('S02')
st.shot('S02', 'livingRoom', setOpts={'tv': False, 'carpet': False},
        props=[TBL('t2', T1), P('lampe2', 'pendantLamp', pos=[0.0, 2.15, 0.0], opts={'drop': 0.9, 'swing': [[-0.4, 0.35]], 'color': '#E8452C'}),
               *[MARK(f'm2{j}', p_, j + 1, r(0.15 + 0.22 * j), ry=a_, s=1.6) for j, (p_, a_) in enumerate([([0.36, 0, 0.5], -15), ([-0.36, 0, 0.52], 15), ([-0.3, 0.42, 0.05], 10), ([0.3, 0.42, -0.05], -10)])]],
        cams=[cam(0.0, [0.0, 1.15, 2.9], [0.0, 1.1, 2.25], [0.0, 0.3, 0.0], [0.0, 0.28, 0.0], lens=46)])
for j in range(4): st.cue('sfx:pop', 'S02', r(0.15 + 0.22 * j), 0.18)
st.cue('sfx:sting', 'S02', 0.05, 0.25)

# 3: special forces. Night, his street from low: the block's front, a helicopter over it sweeping its searchlight off to the right of the riders;
#    three ropes hang from it and three men in black slide down them from the first frame, 0.15 s apart, fast then braking (review 3: the beam
#    swept across the left rider and washed him white)
D3 = st.dur('S03'); BLK3 = [0.0, 0, -8.0]
SW3 = [(-0.9, 0.0), (0.3, 0.15), (1.3, 0.3)]   # (review 2) the slides start at the top of the shot, 0.15 s apart
st.shot('S03', 'parisStreet', setOpts={**STREET, 'night': True}, actors=[
        *[act(f'swat{j + 1}', [x_, r(6.8 - 0.4 * j), -5.6], 15, 'stand', 'determined', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': [x_, r(9.4 - 0.4 * j), -5.45, 1, 0.03], 'R': [x_, r(9.1 - 0.4 * j), -5.45, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'legL': [-0.3, 0.1, 0, 1, None], 'legR': [-0.2, -0.1, 0, 1, None], 'shinL': [0.5, 0, 0, 1, None], 'shinR': [0.4, 0, 0, 1, None]}}, toonDur=0.0),
            k(d_, to=[x_, r(2.7 - 0.25 * j), -5.6], dur=0.72, ease='out', glide=True, face='keep'),   # (review 2) they stop sliding with their feet above the captions
            k(d_, toon={'reach': {'L': [x_, r(4.8 - 0.3 * j), -5.45, 1, 0.03], 'R': [x_, r(4.5 - 0.3 * j), -5.45, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'legL': [-0.3, 0.1, 0, 1, None], 'legR': [-0.2, -0.1, 0, 1, None], 'shinL': [0.5, 0, 0, 1, None], 'shinR': [0.4, 0, 0, 1, None]}}, toonDur=0.72, toonEase='out')])
          for j, (x_, d_) in enumerate(SW3)]],
        props=[P('blk3', 'holedBlock', pos=BLK3, opts={'w': 6.0, 'h': 10.0, 'holeAt': 99.0, 'night': True, 'door': True}), *sum([KIT('3', f'swat{j + 1}') for j in range(3)], []),
               P('heli3', 'helicopter', pos=[0.3, 10.2, -5.2], ry=90, scale=1.0, opts={'spin': 6, 'beam': True, 'beamLen': 14, 'beamR': 1.8, 'tilt': 25, 'sweep': [[0.0, 165], [D3, 195]]}),
               *[P(f'corde3{j}', 'rope', pos=[x_, 9.6, -5.45], opts={'len': 9.3, 'seed': j, 'sway': 0.0}) for j, (x_, _) in enumerate(SW3)]],
        cams=[cam(0.0, [2.4, 1.3, 7.5], [2.3, 1.32, 7.2], [0.1, 6.0, -6.0], [0.1, 5.7, -6.0], lens=52)])
st.cue('sfx:rotor', 'S03', 0.0, 0.4); st.cue('sfx:siren', 'S03', 0.2, 0.15)
for j, (_, d_) in enumerate(SW3): st.cue('sfx:slideDown', 'S03', d_, 0.15)

# 4: surrounded the building. Night, low by the facade on the door's right: four men in black crouch in a wide arc round the lit door, floor between
#    each of them, all turned to it (three-quarter front to us), each with his own thin torch beam on the door; a cool rim light from behind them
#    edges their silhouettes; on « l'immeuble » they all take one step in together and settle
# (review 3) they overlapped into one black mass like a conga line, the beams merged into one white ribbon and the lower third was empty pavement:
# a wider arc (3 m, 75 degrees) seen from low against the facade, square to the arc's chord, spreads them across the frame, each beam is aimed at its
# own spot on the door, a rim light behind them
D4 = st.dur('S04'); DOOR4 = [0.0, 0, -8.0]; STEP4 = 0.4
RING4 = []
for a_ in (-75, -50, -25, 0):
    x_, z_ = r(3.0 * math.sin(math.radians(a_))), r(-8.0 + 3.0 * math.cos(math.radians(a_)))
    RING4.append((x_, z_, r(math.degrees(math.atan2(-x_, -8.0 - z_)))))
DSPOT4 = [[-0.25, 1.75, -7.97], [0.15, 1.35, -7.97], [-0.15, 0.95, -7.97], [0.25, 0.6, -7.97]]   # each beam's spot on the door
def lamp4(j, p_):
    x_, z_, ry_ = RING4[j]; g_ = loc(p_, ry_, [-0.05, 1.3, 0.45]); Z = unit3([DSPOT4[j][i] - g_[i] for i in range(3)])
    X = unit3(cross3([0.0, 1.0, 0.0], Z)); Y = cross3(Z, X); rx, ry2, rz = axes_euler(X, Y, Z)
    return g_, ry2, [rx, 0, rz], r(math.sqrt(sum((DSPOT4[j][i] - g_[i]) ** 2 for i in range(3))) - 0.38)
def swat4(j, x_, z_, ry_):
    x2, z2 = r(x_ * 0.88), r(-8.0 + (z_ + 8.0) * 0.88)
    crouch = {'spine': [0.3, 0, 0, 1, None], 'legL': [-0.55, 0, 0, 1, None], 'shinL': [0.95, 0, 0, 1, None], 'legR': [-0.55, 0, 0, 1, None], 'shinR': [0.95, 0, 0, 1, None]}
    aim = lambda p_: {'R': [*loc(p_, ry_, [-0.05, 1.3, 0.55]), 1, 0.03], 'L': [*loc(p_, ry_, [0.08, 1.25, 0.3]), 1, 0.03]}
    return act(f'swat{j + 1}', [x_, 0, z_], ry_, 'stand', 'determined', keys=[k(0.0, look=[0.0, 1.2, -8.0]),
        k(0.0, toon={'reach': aim([x_, 0, z_]), 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': crouch, 'sq': [1.04, 0.9, 1.04]}, toonDur=0.0),
        k(r(STEP4 + 0.03 * j), to=[x2, 0, z2], dur=0.24, ease='inOut', glide=True, face='keep'),
        k(r(STEP4 + 0.02 + 0.03 * j), toon={'reach': aim([x2, 0, z2]), 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': crouch, 'sq': [1.04, 0.9, 1.04], 'settle': 0.7}, toonDur=0.22, toonEase='inOut')])
def lampP4(j):
    x_, z_, ry_ = RING4[j]; p1 = [x_, 0, z_]; p2 = [r(x_ * 0.88), 0, r(-8.0 + (z_ + 8.0) * 0.88)]
    g1, ry1, rot1, L1 = lamp4(j, p1); g2, _, _, _ = lamp4(j, p2)
    return P(f'lampe4{j}', 'tacLight', pos=g1, ry=ry1, rot=rot1, opts={'len': L1, 'r': 0.07, 'beam': 0.42}, keys=[k(r(STEP4 + 0.03 * j), to=g2, dur=0.24, ease='inOut')])
st.shot('S04', 'parisStreet', setOpts={**STREET, 'night': True}, actors=[swat4(j, *q) for j, q in enumerate(RING4)],
        props=[P('blk4', 'holedBlock', pos=DOOR4, opts={'w': 6.0, 'h': 10.0, 'holeAt': 99.0, 'night': True, 'door': True}),
               *sum([KIT('4', f'swat{j + 1}') for j in range(4)], []), *[lampP4(j) for j in range(4)],
               P('contre4', 'glowLight', pos=[0.0, 2.3, -7.5], opts={'at': -1.0, 'k': 16, 'dist': 7, 'color': '#FFD48A'}),
               P('rim4', 'glowLight', pos=[-4.6, 2.6, -4.2], opts={'at': -1.0, 'k': 14, 'dist': 6.5, 'color': '#BFD8FF'})],
        cams=[cam(0.0, [5.5, 0.75, -7.55], [5.4, 0.75, -7.45], [-1.2, 1.75, -6.3], [-1.25, 1.75, -6.35], lens=58)])   # (review 3) low against the facade, square to the arc's chord: the four men spread across the frame with gaps (story_kit.project: heads at x 0.09-0.73), the lit door at the right edge
st.cue('sfx:rotor', 'S04', 0.0, 0.3); st.cue('sfx:stepRun', 'S04', STEP4, 0.25)

# 5: the table refused to comply. The living room from the front right: the open door in the back wall, a bright canister already rolling across
#    the floor from it toward the table (from the first frame: the line gives 0.67 s), and BANG: a soft white glow swallows the room
D5 = st.dur('S05'); BANG5 = 0.42; DOOR5 = [-2.6, 0, -3.58]
st.shot('S05', 'livingRoom', setOpts={'tv': False, 'carpet': False},
        props=[TBL('t5', T1), P('porte5', 'openDoor', pos=DOOR5, opts={'open': 1.25}),
               P('grenade5', 'flashCanister', pos=[0.0, 0, 0.0], opts={'s': 2.0, 'path': [[0.0, -1.7, -2.3], [0.3, -0.35, -0.55], [r(BANG5 - 0.02), 0.05, -0.05]], 'hide': r(BANG5 + 0.05)}),
               P('flash5', 'flashBang', pos=[0.05, 0.35, -0.05], opts={'at': BANG5, 'r': 2.4, 'fade': 0.3, 'soft': True})],
        fx=[{'type': 'flash', 'at': BANG5, 'dur': 0.18}, {'type': 'shake', 'at': BANG5, 'dur': 0.2, 'amount': 0.02}],
        cams=[cam(0.0, [1.9, 1.0, 2.8], [1.86, 0.98, 2.7], [-0.8, 0.5, -1.4], [-0.8, 0.5, -1.4], lens=52)])
st.cue('sfx:rattleShort', 'S05', 0.0, 0.25); st.cue('sfx:punch', 'S05', BANG5, 0.55); st.cue('thunder', 'S05', BANG5, 0.3)

# 6: (on « refusé ») the smoke clears: the table is exactly where it was; behind it three men in helmets and gas masks crouch in an arc, their
#    narrow lamp beams aimed down so they meet in a pool on the tabletop; at the table's right end a fourth, side-on to us, leans in over it with
#    his neck stretched and peers at it in profile, his head in front of the beams; the table does not move
# (review 3) the cones pointed across at chest height over the table and crossed; the peering man's head sat inside a cone (a pale ghost box, he
# read as headless); the table was small with an empty lower third: the beams now run from each lamp to a point on the top, the peer stands at the
# right end facing it, and the camera is lower and closer
D6 = st.dur('S06')
AIM6 = [(-0.85, -0.8, 32), (-0.25, -1.05, 6), (0.18, -1.2, -10)]
SPOT6 = [[-0.22, 0.43, -0.02], [0.0, 0.43, 0.06], [0.2, 0.43, -0.02]]   # where each beam lands on the tabletop
PEER6 = [1.15, 0, 0.22]   # (review 3) far enough right that his leaning head clears the third man's
CR6 = {'spine': [0.3, 0, 0, 1, None], 'legL': [-0.6, 0, 0, 1, None], 'shinL': [1.05, 0, 0, 1, None], 'legR': [-0.6, 0, 0, 1, None], 'shinR': [1.05, 0, 0, 1, None]}
def lamp6(j):
    x_, z_, a_ = AIM6[j]; g_ = loc([x_, 0, z_], a_, [-0.05, 1.15, 0.45]); Z = unit3([SPOT6[j][i] - g_[i] for i in range(3)])
    X = unit3(cross3([0.0, 1.0, 0.0], Z)); Y = cross3(Z, X); rx, ry_, rz = axes_euler(X, Y, Z)
    L_ = r(math.sqrt(sum((SPOT6[j][i] - g_[i]) ** 2 for i in range(3))) - 0.38)
    return g_, P(f'lampe6{j}', 'tacLight', pos=g_, ry=ry_, rot=[rx, 0, rz], opts={'len': L_, 'r': 0.11, 'beam': 0.34})
LAMPS6 = [lamp6(j) for j in range(3)]
def swat6(j):
    x_, z_, a_ = AIM6[j]; g_ = LAMPS6[j][0]
    return act(f'swat{j + 1}', [x_, 0, z_], a_, 'stand', 'determined', keys=[k(0.0, look=[0.0, 0.42, 0.0]),
        k(0.0, toon={'reach': {'R': [g_[0], r(g_[1] - 0.03), g_[2], 1, 0.03], 'L': [*loc([x_, 0, z_], a_, [0.08, 1.1, 0.3]), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': CR6, 'sq': [1.04, 0.88, 1.04]}, toonDur=0.0),
        k(r(0.5 + 0.13 * j), toon={'face': {'lid': 1.0}}, toonDur=0.04), k(r(0.56 + 0.13 * j), toon={'face': {'lid': 0.3}}, toonDur=0.05)])
LEAN6 = 0.42
peer6 = act('swat4', PEER6, -90, 'stand', 'determined', keys=[k(0.0, look=[0.0, 0.45, 0.0]),
    k(0.0, toon={'reach': {'R': [*loc(PEER6, -90, [-0.2, 0.62, 0.2]), 1, 0.03], 'L': [*loc(PEER6, -90, [0.2, 0.62, 0.2]), 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': CR6, 'sq': [1.04, 0.9, 1.04]}, toonDur=0.0),
    k(LEAN6, to=[r(PEER6[0] - 0.1), 0, PEER6[2]], dur=0.24, ease='inOut', glide=True, face='keep'),
    k(LEAN6, toon={'reach': {'R': [*loc([r(PEER6[0] - 0.18), 0, PEER6[2]], -90, [-0.22, 0.46, 0.42]), 1, 0.03], 'L': [*loc([r(PEER6[0] - 0.18), 0, PEER6[2]], -90, [0.22, 0.46, 0.42]), 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'},
                     'bend': {**CR6, 'spine': [0.72, 0, 0, 1, None], 'neck': [0.32, 0, 0, 1.35, None]}, 'sq': [1.04, 0.92, 1.04]}, toonDur=0.26, toonEase='inOut'),
    k(r(LEAN6 + 0.5), toon={'reach': {'R': [*loc([r(PEER6[0] - 0.18), 0, PEER6[2]], -90, [-0.22, 0.46, 0.42]), 1, 0.03], 'L': [*loc([r(PEER6[0] - 0.18), 0, PEER6[2]], -90, [0.22, 0.46, 0.42]), 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'},
                     'bend': {**CR6, 'spine': [0.76, 0, 0, 1, None], 'neck': [0.38, 0.12, 0, 1.4, None]}, 'sq': [1.03, 0.94, 1.03]}, toonDur=0.2, toonEase='inOut')])
st.shot('S06', 'livingRoom', setOpts={'tv': False, 'carpet': False}, actors=[*[swat6(j) for j in range(3)], peer6],
        props=[TBL('t6', T1), *sum([KIT('6', f'swat{j + 1}', mask=True) for j in range(4)], []), *[q[1] for q in LAMPS6],
               P('flaque6', 'glowLight', pos=[0.0, 0.9, 0.0], opts={'at': -1.0, 'k': 6, 'dist': 2.2, 'color': '#FFF0C0'}),
               P('fumee6', 'toonPuff', pos=[0.0, 0.15, 0.25], opts={'at': -0.5, 'n': 6, 'life': 0.95, 'size': 0.28, 'rise': 0.9, 'spread': 1.1, 'color': '#F2F0EA'})],
        cams=[cam(0.0, [0.45, 0.8, 3.6], [0.4, 0.79, 3.45], [0.3, 1.0, -0.5], [0.28, 1.0, -0.5], lens=62)])   # (review 3) low and aimed up a little: the table half the width in the lower middle, its feet just above the captions (story_kit.project), the three heads at a third of the height, the peer at the right
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
        props=[P('blk8', 'holedBlock', pos=B1, opts={'w': 6.0, 'h': 10.0, 'hole': [0.0, 1.05, 1.4], 'holeAt': HIT8, 'bulge': 0.07}),   # (review 2) a bulge before the burst
               P('char8', 'battleTank', pos=[0.0, 0, -5.0], ry=180, scale=0.72, keys=[k(0.0, to=[0.0, 0, -11.1], dur=D8, ease='linear')], opts={'rumble': [[0.0, 9.0, 0.02]]}),
               P('briques8', 'brickBurst', pos=[0.0, 1.05, -8.9], opts={'at': HIT8, 'n': 30, 'floor': 1.05, 'speed': 5.5})],
        cams=[cam(0.0, [3.8, 1.2, -0.6], [3.6, 1.2, -1.0], [0.0, 2.2, -9.0], [0.0, 2.2, -9.0], lens=46)])
st.cue('engine', 'S08', 0.0, 0.3); st.cue('sfx:crunch', 'S08', HIT8, 0.6); st.cue('thunder', 'S08', HIT8, 0.35)

# 9: it came out three buildings further on. From the far side, off the tank's path: three separate blocks one behind another with gaps between
#    them, the nearest the lowest, their roofs stepping up; the near one's front bursts and the tank comes out nose up, the table riding on its long
#    gun with the muzzle sticking out in front of it; the camera swings round toward the tank's path and pushes in, ending nearly in line with it,
#    the table in the middle of the frame at about a third of the width (review 1: in line with the path the three read as one tiered building)
D9 = st.dur('S09'); OUT9 = 0.45
BL9 = [(-4.0, 7.0), (-11.0, 11.0), (-18.0, 15.0)]   # (front z, height): the blocks face the camera, the side the tank comes out of; the nearest is the third block
ZT = lambda t: r(-8.8 + 9.9 * t / D9)   # the tank's pivot along its path
TABLE9 = []   # (review 3) the table rides ON the long gun, 1.62 m ahead of the tank's pivot (the muzzle sticks out 0.8 m in front of it; at 2.34 m it sat
#   past the muzzle and read as riding the hull), lifted by the nose-up (0.14 rad: 0.22 m, 0.16 m back) and wobbling
for t_, dy, dz, rz in [(0.0, 0.0, 0.0, 0.0), (r(OUT9 - 0.02), 0.0, 0.0, 0.0), (r(OUT9 + 0.12), 0.22, -0.16, 0.12), (r(OUT9 + 0.32), 0.2, -0.14, -0.14), (r(OUT9 + 0.48), -0.03, 0.02, 0.1), (r(OUT9 + 0.62), 0.0, 0.0, -0.06), (r(OUT9 + 0.8), 0.0, 0.0, 0.03), (D9, 0.0, 0.0, 0.0)]:
    TABLE9.append((t_, [0.0, r(1.05 + dy), r(ZT(t_) + 1.62 + dz)], rz))
st.shot('S09', 'parisStreet', setOpts={**STREET, 'clear': [-14.0, 14.0], 'clearL': [-14.0, 14.0]}, fx=[{'type': 'shake', 'at': OUT9, 'dur': 0.3, 'amount': 0.02}, {'type': 'shake', 'at': r(OUT9 + 0.45), 'dur': 0.15, 'amount': 0.012}], actors=[],
        props=[*[P(f'blk9{j}', 'holedBlock', pos=[0.0, 0, z_], opts={'w': 4.6, 'h': h_, 'd': 4.0, 'hole': [0.0, 1.05, 1.4], **({'holeAt': OUT9} if j == 0 else {}), 'color': ['#EBDDC4', '#E6D3D3', '#DCE3EA'][j]})
                 for j, (z_, h_) in enumerate(BL9)],
               P('char9', 'battleTank', pos=[0.0, 0, -8.8], ry=0, scale=0.72, keys=[k(0.0, to=[0.0, 0, 1.1], dur=D9, ease='linear'),
                   k(r(OUT9 - 0.04), rotTo=[-0.14, 0.0, 0.0], dur=0.14, ease='out'), k(r(OUT9 + 0.34), rotTo=[0.04, 0.0, 0.0], dur=0.12, ease='in'), k(r(OUT9 + 0.5), rotTo=[0.0, 0.0, 0.0], dur=0.16, ease='inOut')], opts={'rumble': [[0.0, 9.0, 0.02]]}),
               P('t9', 'coffeeTable', pos=TABLE9[0][1], keys=[k(TABLE9[i - 1][0], to=TABLE9[i][1], dur=r(TABLE9[i][0] - TABLE9[i - 1][0]), ease='linear') for i in range(1, len(TABLE9))]
                   + [k(TABLE9[i - 1][0], rotTo=[0.0, 0.0, TABLE9[i][2]], dur=r(TABLE9[i][0] - TABLE9[i - 1][0]), ease='inOut') for i in range(2, len(TABLE9))]),
               P('briques9', 'brickBurst', pos=[0.0, 1.05, -3.9], opts={'at': OUT9, 'n': 30, 'floor': 1.05, 'speed': 5.0})],
        cams=[cam(0.0, [10.5, 2.4, 15.0], [1.7, 1.45, 9.9], [0.0, 4.5, -10.0], [0.0, 1.3, 2.6], lens=44, ease='inOut')])   # (review 3) it ends nearly in line with the tank's path, on the table (it drifted to the left edge): the tank comes at the lens
st.cue('engine', 'S09', 0.0, 0.35); st.cue('sfx:crunch', 'S09', OUT9, 0.55); st.cue('thud', 'S09', r(OUT9 + 0.45), 0.4)

# 10: four pairs of handcuffs. On the pavement, high three-quarter front, the camera travelling back with them: four soldiers, each cuffed to a leg
#     of the table with big dark steel cuffs, carry it toward us like a stretcher, in step; behind the table on the right, in the gap between it and
#     the soldiers, the tank driver in his padded helmet hops on one foot holding his toe (ARRÊTÉE); the table fills a third of the width
D10 = st.dur('S10'); TB10 = [0.0, 0.62, 0.0]
SOL10 = [(1.0, 0.36), (-1.0, 0.36), (1.12, -0.4), (-1.12, -0.4)]
def sold10(j, x_, z_):
    side = 1 if x_ > 0 else -1; hand = 'R' if side < 0 else 'L'; legp = [r(side * 0.46), 0.95, r(0.21 if z_ > 0 else -0.21)]
    return act(f'sold{j + 1}', [x_, 0, r(z_ - 1.2)], 0, 'stand', 'determined', keys=[k(0.0, look='camera'),
        k(0.0, to=[x_, 0, r(z_ + 0.4)], dur=D10, clip='walk', ease='linear'),
        *[k(r(t_), toon={'reach': {hand: [legp[0], legp[1], r(legp[2] - 1.2 + 1.6 * t_ / D10), 1, 0.03]}, 'hands': {hand: 'grip'}}, toonDur=0.2) for t_ in (0.0, D10 * 0.5, D10)]])
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[*[sold10(j, x_, z_) for j, (x_, z_) in enumerate(SOL10)],
        act('pilote', [0.95, 0, -3.6], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), *sum(hop_hold(0.0, [[0.95, -3.6], [0.86, -3.2], [0.98, -2.8], [0.86, -2.4], [0.96, -2.0]], 0.3, 0.24, 0, PAIN, sqL=0.12), [])])],   # (review 3) the driver hops behind and to the right of the table, in the gap between it and the right-hand soldiers: from the high camera his hop and held toe clear the tabletop (behind it, only his head bobbed)
        props=[P('t10', 'coffeeTable', pos=[0.0, 0.55, -1.2], opts={'cuffs': True, 'cuffColor': '#4A5058', 'cuffS': 1.5}, keys=[k(0.0, to=[0.0, 0.55, 0.4], dur=D10, ease='linear')]),
               *[CUFF(f'cuff10{j}', f'sold{j + 1}', 'R' if x_ < 0 else 'L') for j, (x_, _) in enumerate(SOL10)],
               *[KEPI(f'kepi10{j}', f'sold{j + 1}') for j in range(4)],
               P('casque10', 'tankHelmet', on={'actor': 'pilote', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'s': 0.82})],
        cams=[cam(0.0, [-0.6, 3.4, 4.6], [-0.6, 3.4, 6.2], [0.0, 0.9, -0.6], [0.0, 0.9, 1.0], lens=48)])   # (review 2) pushed in, travelling back with them: the table a third of the width
st.cue('sfx:cuff', 'S10', 0.1, 0.3); st.cue('sfx:cuff', 'S10', 0.22, 0.25)
for i in range(4): st.cue('sfx:stepHeavy', 'S10', r(0.1 + 0.3 * i), 0.15); st.cue('thud', 'S10', r(0.3 + 0.3 * i), 0.08)

# 11: the tank driver was decorated. A square in the sun, flags, a three-man band playing behind; the general, turned to us (grey moustache), pins
#     a medal low on the driver's chest with his near hand; the driver salutes with his far hand, balanced on one leg, his left foot in a big
#     foot-shaped plaster cast with pink toes held out at knee height beside him; he wobbles
D11 = st.dur('S11'); PIN11 = 1.0; PIL11 = [0.2, 0, 0.0]; GEN11 = [-0.45, 0, 0.45]   # (review 2) the general closer and turned to us (we saw the grey back of his head)
BEATS11 = [r(0.15 + 0.3 * i) for i in range(7)]
CHEST11 = loc(PIL11, -10, [0.1, 1.62, 0.17])   # (review 2) lower on the chest: the pinning arm and the salute met in a knot at the shoulder
SAL11 = loc(PIL11, -10, [0.17, 2.06, 0.13]); CASTUP11 = loc(PIL11, -10, [0.36, 0.62, 0.12])   # the salute with his far (left) hand; the cast held out at knee height, clear of the standing leg
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('pilote', PIL11, -10, 'stand', 'determined', keys=[k(0.0, look='camera'),
            *[k(r(0.02 + 0.3 * i), toon={'plant': {'L': [*CASTUP11, 1]}, 'reach': {'L': [*SAL11, 1, 0.03]}, 'hands': {'L': 'open'}, 'lay': [0.0, r(0.11 * (-1) ** i)], 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.26 if i else 0.0, toonEase='inOut') for i in range(7)]]),
        act('general', GEN11, 22, 'stand', 'determined', keys=[k(0.0, look=[CHEST11[0], CHEST11[1], CHEST11[2]]),
            k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(r(PIN11 - 0.35), toon={'reach': {'L': [r(CHEST11[0] - 0.05), CHEST11[1], r(CHEST11[2] + 0.07), 1, 0.03]}, 'hands': {'L': 'grip'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.3, toonEase='out'),
            k(r(PIN11 + 0.12), toon={'reach': {'L': [r(CHEST11[0] - 0.05), CHEST11[1], r(CHEST11[2] + 0.07), 1, 0.03]}, 'hands': {'L': 'grip'}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.06),
            k(r(PIN11 + 0.35), toon={'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.25), k(r(PIN11 + 0.4), look='camera')]),
        *[act(f'musi{j + 1}', [[-2.5, 1.6, 2.6][j], 0, -2.8], [20, -10, -20][j], 'stand', 'neutral', keys=[k(0.0, look='camera'), *[k(b_, toon={'sq': [1.03, 0.95, 1.03], 'face': {'lid': 0.5, 'mouth': 'kiss' if j == 0 else 'line'}}, toonDur=0.06) for b_ in BEATS11],
            *[k(r(b_ + 0.12), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.4, 'mouth': 'kiss' if j == 0 else 'line'}}, toonDur=0.1) for b_ in BEATS11]]) for j in range(3)]],
        props=[P('platre11', 'footCast', on={'actor': 'pilote', 'joint': 'footL', 'offset': [0.0, 0.02, 0.0]}, opts={'s': 1.9, 'toes': True}), P('casque11', 'tankHelmet', on={'actor': 'pilote', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'s': 0.82}),
               P('medaille11', 'medal', on={'actor': 'pilote', 'joint': 'torso', 'offset': [0.1, 0.44, 0.17]}, scale=2.2, keys=[k(0.0, visible=False), k(PIN11, visible=True)]),
               KEPI('kepi11g', 'general', color='#2B3A2A', band='#E2B53C'),
               P('instr110', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11], 'rot': [-0.3, -0.85, 0.0]}, opts={'kind': 'trumpet', 'beat': BEATS11[::2], 's': 1.15}),
               P('instr111', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.3, 0.0]}, opts={'kind': 'sousa', 'beat': BEATS11[::2]}),
               P('instr112', 'bandInstr', on={'actor': 'musi3', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': BEATS11}),
               P('drap11', 'flagPole', pos=[2.3, 0, -3.6], opts={'h': 4.2}), P('drap11b', 'flagPole', pos=[-2.9, 0, -3.8], opts={'h': 4.2}), P('drap11c', 'flagPole', pos=[0.5, 0, -4.6], opts={'h': 4.6})],
        cams=[FC(0.0, [0.7, 1.4, 4.0], [[0.6, 2.6, 0.0], [0.2, 0.0, 0.0], [-1.0, 2.6, 0.3], [-0.75, 0.0, 0.3]], top=0.1, bottom=0.76, lenses=range(30, 70))])
st.cue('sfx:fanfare', 'S11', 0.0, 0.35); st.cue('sfx:clink', 'S11', PIN11, 0.3)

# courtroom: the dock at the front left, the table in it between two gendarmes, the judge at the bench at the back, the jury on the right
DOCK = [-1.4, 0, 1.4]; TD = [-1.4, 0.0, 1.38]; DH = 0.7; SH_ = 0.74   # the dock's panel and the stand the table stands on   # the table stands in the dock (the dock's panel 0.95 m: the table's top shows over the rail on a stand)
STAND = lambda pid, p: P(pid, 'table', pos=p, opts={'w': 0.9, 'd': 0.55, 'h': SH_, 'color': '#6B4426', 'legs': '#5A3820'})   # a low stand inside the dock lifts the table over the rail
GEND = [(-2.35, 1.25, 20), (-0.45, 1.25, -20)]
def gend_actors(look_keys=()):
    return [act(f'gend{j + 1}', [x_, 0, z_], a_, 'stand', 'determined', keys=[k(0.0, look='camera'), *(look_keys[j] if look_keys else [])]) for j, (x_, z_, a_) in enumerate(GEND)]

# 12: at the trial. The courtroom from the back, high, a slow push-in: the judge at the bench, the dock at the front left, the coffee table standing
#     in it on a low stand, a gendarme each side, still; the judge leans far over his bench, neck stretched, a big magnifying glass raised to his
#     eye, and peers at it
D12 = st.dur('S12')
# (review 3) the judge's peer could not be seen at his size and the left gendarme did the peering instead; the same peer beat came back in S06 and
# S13: here the judge leans far over his bench with his neck stretched and a big magnifying glass raised to his eye (his own device), the gendarmes
# keep still, and the camera pushes in a little
JG12 = [0.0, 0.3, -4.35]
st.shot('S12', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[act('juge', JG12, 0, 'stand', 'neutral', keys=[k(0.0, look=[TD[0], 1.0, TD[2]]),
            k(0.0, toon={'reach': {'R': [0.3, 1.01, -4.0, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(0.35, toon={'reach': {'R': [0.28, 1.05, -3.98, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.1),
            k(0.5, toon={'reach': {'R': [0.0, 1.52, -3.8, 1, 0.03]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.55, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1.45, None]}, 'sq': [0.96, 1.06, 0.96],
                         'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.22, toonEase='outBack'),
            k(1.0, toon={'reach': {'R': [0.02, 1.53, -3.79, 1, 0.03]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.58, 0, 0, 1, None], 'neck': [0.32, 0.1, 0, 1.5, None]},
                         'face': {'lid': 0.6, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.3, toonEase='inOut')]),
        *gend_actors([[k(0.8, toon={'face': {'lid': 1.0}}, toonDur=0.04), k(0.86, toon={'face': {'lid': 0.4}}, toonDur=0.05), k(1.2, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.2)], [k(0.4, look=[0.0, 1.8, -4.3], lookDur=0.3), k(1.1, look='camera', lookDur=0.2)]])],
        props=[SEAL('sceau12'), GKEPI('kepi12a', 'gend1'), GKEPI('kepi12b', 'gend2'), P('box12', 'dockBox', pos=DOCK, opts={'h': DH}), STAND('stand12', [DOCK[0], 0, DOCK[2] - 0.05]), TBL('t12', [TD[0], SH_, TD[2]]),
               # the glass is a free prop moved with his hand (attached to the hand it lay along his forearm like a stick): its lens faces us, in front
               # of his eye once he leans in
               P('loupe12', 'magnifyingGlass', pos=[0.3, 0.75, -4.0], scale=1.3, keys=[k(0.35, to=[0.28, 0.79, -3.98], dur=0.1, ease='out'), k(0.5, to=[0.0, 1.26, -3.8], dur=0.22, ease='outBack'), k(1.0, to=[0.02, 1.27, -3.79], dur=0.3, ease='inOut')])],
        cams=[cam(0.0, [-2.6, 3.2, 5.6], [-2.4, 3.0, 4.9], [-0.6, 1.0, -1.5], [-0.5, 1.15, -1.8], lens=50, ease='inOut')])
st.cue('sfx:crickets', 'S12', 0.0, 0.05)

# 13: no remorse. Close on the dock: the table between the two gendarmes, a slow push-in; the one on the right glances at it, back at us, then
#     snaps back to it in a double take, eyes out, and back to us; the table does not move
D13 = st.dur('S13')
st.shot('S13', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=gend_actors([[], [*doubleTake(0.1, [TD[0], 0.9, TD[2]], back='camera', pop=0.4, blank=0.2, hold=0.3), k(0.85, look='camera', lookDur=0.1)]]),   # (review 3) a true double take (the third peer beat in 11 s had the same pose)
        props=[SEAL('sceau13'), GKEPI('kepi13a', 'gend1'), GKEPI('kepi13b', 'gend2'), P('box13', 'dockBox', pos=DOCK, opts={'h': DH}), STAND('stand13', [DOCK[0], 0, DOCK[2] - 0.05]), TBL('t13', [TD[0], SH_, TD[2]])],
        cams=[FC(0.0, [-1.2, 1.7, 5.6], [[-2.6, 2.6, 1.25], [-0.2, 2.6, 1.25], [-2.6, 0.9, 1.25], [-0.2, 0.9, 1.25], [TD[0], SH_, TD[2]]], top=0.14, bottom=0.8, lenses=range(30, 56), drift=(0.0, 0.0, -0.3))])

# 14: the defence pleaded it was there first. From high over the aisle: the lawyer at the far end flings a roll toward us and it unrolls down the
#     aisle: a plan of the living room, the table drawn in its place and a trail of footprints walking straight into it with a red star; on the right
#     the three jurors, all in frame, blink, then lean in one after another and blink again
D14 = st.dur('S14'); PLAN14 = [0.0, 0.02, -1.8]
JURY = [(1.4, -2.3, -70), (1.5, -1.55, -80), (1.58, -0.8, -95)]   # (review 3) closer to the aisle: the third juror was out of frame
THROW14 = 0.22; LAND14 = 0.36
st.shot('S14', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[
        act('avocat', [0.0, 0, -2.3], 0, 'stand', 'determined', keys=[k(0.0, look=[0.0, 0.0, 0.0]),
            k(0.0, toon={'reach': {'L': [0.22, 2.25, -2.55, 1, 0.03], 'R': [-0.22, 2.25, -2.55, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [-0.3, 0, 0, 1, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': 0.6}}, toonDur=0.0),
            k(r(THROW14 - 0.06), toon={'reach': {'L': [0.3, 1.35, -1.55, 1, 0.03], 'R': [-0.3, 1.35, -1.55, 1, 0.03]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'spine': [0.5, 0, 0, 1, None]}, 'sq': [1.05, 0.94, 1.05], 'face': {'lid': 0.1, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.09, toonEase='out'),
            k(0.6, toon={'reach': {'L': [0.45, 1.35, -1.8, 1, 0.03], 'R': [-0.45, 1.35, -1.8, 1, 0.03]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.25, toonEase='inOut'),
            k(1.1, toon={'reach': {'L': [0.55, 1.5, -1.8, 1, 0.03]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.3), k(1.3, look='camera')]),
        # (review 3) the hold after the unroll went dead: the three jurors now lean in one after another (0.12 s apart, each overshooting and
        # settling), blink at different times and shift their weight
        *[act(f'jure{j + 1}', [x_, 0, z_], a_, 'sit', 'neutral', keys=[k(0.0, look=[0.0, 0.0, z_]),
            k(r(0.75 + 0.1 * j), toon={'face': {'lid': 1.0}}, toonDur=0.04), k(r(0.81 + 0.1 * j), toon={'face': {'lid': 0.35}}, toonDur=0.05),
            k(r(1.15 + 0.12 * j), toon={'bend': {'spine': [0.42, 0, 0, 1, None], 'neck': [0.26, 0, 0, 1.3, None]}, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.14, toonEase='out'),
            k(r(1.36 + 0.12 * j), toon={'bend': {'spine': [0.32, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1.22, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.16, toonEase='inOut'),
            k(r(1.7 + 0.13 * j), toon={'bend': {'spine': [0.32, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1.22, None]}, 'face': {'lid': 1.0, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.04),
            k(r(1.76 + 0.13 * j), toon={'bend': {'spine': [0.34, 0, 0, 1, None], 'neck': [0.2, 0.08 * (j - 1), 0, 1.22, None]}, 'lay': [0.0, r(0.05 * (1 - j))], 'face': {'lid': 0.1, 'eye': 0.4, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.12)])
          for j, (x_, z_, a_) in enumerate(JURY)]],
        props=[SEAL('sceau14'), P('plan14', 'planScroll', pos=PLAN14, rot=[-PI / 2, 0, 0], opts={'w': 1.6, 'len': 3.4, 'unroll': [[LAND14, 0.02], [1.05, 1.0]]}, keys=[k(0.0, visible=False), k(LAND14, visible=True)]),
               P('rouleau14', 'paperRoll', pos=[0.0, 2.25, -2.5], opts={'w': 1.6, 'spin': 16}, keys=[k(THROW14, to=[0.0, 1.9, -2.05], dur=r((LAND14 - THROW14) / 2), ease='out'),
                   k(r((THROW14 + LAND14) / 2), to=[0.0, 0.1, PLAN14[2]], dur=r((LAND14 - THROW14) / 2), ease='in'), k(LAND14, visible=False)]),
               *[P(f'fantome14{j}', 'paperRoll', pos=[0.0, 2.25, -2.5], opts={'w': 1.6, 'spin': 16, 'opacity': [0.45, 0.22][j]},   # (review 2) the smear of the throw: two fading copies trail the roll
                   keys=[k(0.0, visible=False), k(r(THROW14 + 0.03 * (j + 1)), visible=True), k(r(THROW14 + 0.03 * (j + 1)), to=[0.0, 1.9, -2.05], dur=r((LAND14 - THROW14) / 2), ease='out'),
                         k(r((THROW14 + LAND14) / 2 + 0.03 * (j + 1)), to=[0.0, 0.1, PLAN14[2]], dur=r((LAND14 - THROW14) / 2), ease='in'), k(r(LAND14 + 0.02 * (j + 1)), visible=False)]) for j in range(2)],
               P('banc14', 'dockBox', pos=[2.0, 0, -1.55], ry=-90, opts={'w': 2.6, 'd': 0.6, 'h': 0.6, 'color': '#6E4A2E'})],
        cams=[cam(0.0, [-0.9, 4.4, 3.9], [-0.85, 4.35, 3.7], [0.5, 0.8, -1.1], [0.5, 0.8, -1.15], lens=52)])
st.cue('sfx:whoosh', 'S14', THROW14, 0.3); st.cue('sfx:paper', 'S14', LAND14, 0.35); st.cue('sfx:gasp', 'S14', 1.27, 0.3)

# 15: twenty years. Close on the dock: a giant stamp drops in and hangs over the table, lifts a little, slams down and squashes on its face: the
#     table's legs crush flat and spring back with an overshoot (CONDAMNÉE); the gendarmes flinch
D15 = st.dur('S15'); STAMP15 = 0.3
st.shot('S15', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=gend_actors([[k(r(STAMP15 + 0.02), toon={'sq': [1.08, 0.88, 1.08], 'face': {'lid': 1.0, 'mouth': 'clench'}}, toonDur=0.04), k(r(STAMP15 + 0.3), toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.15)]] * 2),
        props=[SEAL('sceau15'), GKEPI('kepi15a', 'gend1'), GKEPI('kepi15b', 'gend2'), P('box15', 'dockBox', pos=DOCK, opts={'h': DH}), STAND('stand15', [DOCK[0], 0, DOCK[2] - 0.05]),
               P('t15', 'coffeeTable', pos=[TD[0], SH_, TD[2]], opts={'squash': [[0.0, 0.0], [r(STAMP15 - 0.01), 0.0], [STAMP15, 1.0], [r(STAMP15 + 0.3), 1.0], [r(STAMP15 + 0.4), -0.3], [r(STAMP15 + 0.5), 0.12], [r(STAMP15 + 0.6), -0.04], [r(STAMP15 + 0.68), 0.0]]},
                   keys=[k(r(STAMP15 + 0.38), rotTo=[0.0, 0.0, 0.07], dur=0.08, ease='out'), k(r(STAMP15 + 0.46), rotTo=[0.0, 0.0, -0.06], dur=0.08, ease='inOut'), k(r(STAMP15 + 0.54), rotTo=[0.0, 0.0, 0.03], dur=0.08, ease='inOut'), k(r(STAMP15 + 0.62), rotTo=[0.0, 0.0, 0.0], dur=0.08, ease='inOut')]),
               # (review 2) the stamp drops in, hangs, lifts a little (anticipation), slams, squashes on its face, and goes back up
               P('tampon15', 'tableStamp', pos=[TD[0], 4.5, TD[2]], scale=4.0, opts={'squash': [[r(STAMP15 - 0.005), 0.0], [STAMP15, 1.0], [r(STAMP15 + 0.04), 1.0], [r(STAMP15 + 0.12), 0.0]]},
                 keys=[k(0.0, to=[TD[0], 3.42, TD[2]], dur=0.12, ease='out'), k(0.12, to=[TD[0], 3.72, TD[2]], dur=0.08, ease='out'),
                       k(r(STAMP15 - 0.1), to=[TD[0], r(SH_ + 0.42 * 0.25 + 1.52), TD[2]], dur=0.1, ease='in'), k(r(STAMP15 + 0.1), to=[TD[0], 4.7, TD[2]], dur=0.14, ease='out')])],
        fx=[{'type': 'shake', 'at': STAMP15, 'dur': 0.2, 'amount': 0.025}],
        cams=[cam(0.0, [0.6, 1.8, 4.7], [0.56, 1.79, 4.55], [-1.4, 1.25, 1.3], [-1.4, 1.25, 1.3], lens=40)])
st.cue('sfx:gavel', 'S15', 0.0, 0.35); st.cue('clack', 'S15', STAMP15, 0.55); st.cue('thud', 'S15', STAMP15, 0.4); st.cue('sfx:boing', 'S15', r(STAMP15 + 0.4), 0.25)

# 16: in prison, it reoffended. A high three-quarter view (about 40 degrees down) pushed in on the table in the middle of the cell under a bare bulb;
#     three guards on a wide circle round it, side-on to us and facing away from it, hop in place on the same beat, each holding his raised left
#     foot high on his outer side with both hands, a squash at every landing; floor shows between every guard and the table (review 2: from
#     straight above the hops and the held feet did not read; review 3: the outer guards' held feet ended on the table's corners)
D16 = st.dur('S16'); C16 = [0.45, 0, 0.25]
# (review 3) the outer guards' held feet and hands ended on the table's corners (« three guards gripping the table »): each guard now faces AWAY from
# the table, side-on to us, so the held foot (planted high, at hip height, front_pose) is on his far side; a wider circle leaves floor between
# every hand or foot and the table
G16 = [((-0.62, 0.72), -90), ((1.52, 0.6), 90), ((0.62, -0.92), -90)]   # (x, z), facing: left faces left, right faces right, the back one faces left
def guard16(j):
    (x_, z_), ry_ = G16[j]
    pts = [[r(x_ + (0.035 if i % 2 else 0.0) * (1 if ry_ > 0 else -1)), z_] for i in range(8)]
    kk, tt = hop_hold(0.0, pts, 0.24, 0.2, ry_, PAIN, sqL=0.1, yaw=0.15, pose=front_pose)
    return act(f'gard{j + 1}', [x_, 0, z_], ry_, 'stand', 'neutral', keys=[k(0.0, look='camera'), *kk, *tt])
CAM16 = [1.81, 5.2, 6.66]   # 37 degrees down, 6.9 m back on a 40-degree lens (less perspective: the guards' heads stay inside the frame)
st.shot('S16', 'brightCell', setOpts={'w': 4.0, 'd': 7.6, 'h': 7.5, 'bars': False}, actors=[guard16(j) for j in range(3)],
        props=[TBL('t16', C16), P('ampoule16', 'cellBulb', pos=[0.45, 3.5, 0.25], opts={'drop': 0.55, 'power': 7, 'range': 7})],
        cams=[cam(0.0, CAM16, [1.79, 5.18, 6.58], [0.45, 0.66, 0.1], [0.45, 0.66, 0.1], lens=52)])   # (review 3) 40 -> 52: the wider circle and the feet held out on the outer sides fit (story_kit.project)
for i in range(7): st.cue('thud', 'S16', r(0.24 * i + 0.22), 0.12)
st.cue('sfx:grunt', 'S16', 0.3, 0.2)

# 17: three guards. Life. In the roofed corridor outside the cell, front: the three guards in a row on crutches, their left feet in big plaster casts
#     with pink toes held up behind them, saluting with flat hands, in front of steel-grey bars and a lit cell; between the second and the third,
#     the cell door with a white board at head height; a giant stamp (light wooden block, red knob) hangs over it, tipped to us (red face), swings
#     flat like a hammer on « Perpétuité », lifts straight off and leaves PERPÉTUITÉ in bold red; the camera snaps in on the board (40 % of the
#     width); they jump, caps popping, then hold the salute
D17 = st.dur('S17'); ST17 = r(st.at('S17', 'L13', 2) + 0.02)
DOOR17 = [-0.05, 0, 0.0]; PLATE17 = [r(DOOR17[0] + 0.45), 1.95, r(DOOR17[2] + 0.08)]   # the door's hinge (it spans +X 0.9 m) and its plate at head height
GD17 = [(-1.25, 0.95, 12), (-0.5, 1.1, 5), (1.25, 0.95, -10)]
def gard17(j, x_, z_, a_):
    # (review 3) the casts read as small pinkish blocks at floor level and the salute as a raised fist: the cast foot is held higher behind, the
    # saluting hand is flat (open) and the crutch hand grips
    lift = {'plant': {'L': [*loc([x_, 0, z_], a_, [0.12, 0.62, -0.44]), 1]}, 'hands': {'R': 'open', 'L': 'grip'}}
    return act(f'gard{j + 1}', [x_, 0, z_], a_, 'stand', 'determined', keys=[k(0.0, look='camera'), k(r(0.1 + 0.08 * j), clip='salute'),
        k(0.0, toon={**lift, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
        k(r(ST17 + 0.02), toon={**lift, 'sq': [0.95, 1.12, 0.95], 'hat': [0.16, r(0.25 * (-1) ** j), 0.0], 'face': {'lid': 0.0, 'eye': 0.5, 'pop': 0.5, 'popLen': 0.15, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out'),
        k(r(ST17 + 0.2), toon={**lift, 'sq': [1.04, 0.95, 1.04], 'hat': [0.0, 0.0, 0.0], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.12, toonEase='in'),
        k(r(ST17 + 0.4), toon={**lift, 'face': {'lid': 0.4, 'mouth': 'line'}, 'settle': 0.6}, toonDur=0.15)])
# (review 2) the corridor is roofed (an open top showed a pale sky: it read as a yard), the bars and the door frame are steel grey and a bulb lights the
# cell behind them (navy guards on navy bars merged), the stamp hangs a beat at three-quarters, its handle and red face to us, then turns flat
# and slams; the plate is a white board 1 m wide and the camera snaps in on it after the hit (17 % of the width read as nothing on a phone)
SL17 = 1.14   # knob to face on a scale of 3
ROT17 = [-0.45, 0.6, 0.0]; FLAT17 = [r(PI / 2), 0.0, 0.0]   # hanging upright over the plate, tipped toward us and turned a little (its red face and handle seen), then it swings flat like a hammer
HANG17 = [PLATE17[0], 3.3, 0.75]; BACK17 = [PLATE17[0], 3.5, 0.9]
# (review 3) flat on the plate the stamp showed us its back (« a backlit black television »): it now hits at a slant, its handle tilted up and to
# the right, so at the contact we see its side, the gold band and the red face's edge on the plate
H17 = unit3([0.6, 0.25, 0.76]); X17 = unit3([1.0 - H17[0] * H17[0], -H17[0] * H17[1], -H17[0] * H17[2]]); Z17 = cross3(X17, H17)   # its long side kept as level as the slant allows
_rx, _ry, _rz = axes_euler(X17, H17, Z17); HIT17 = [_rx, r(math.radians(_ry), 4), _rz]
KNOB17 = [r(PLATE17[0] + H17[0] * SL17), r(PLATE17[1] + H17[1] * SL17), r(PLATE17[2] + 0.04 + H17[2] * SL17)]
st.shot('S17', 'brightCell', setOpts={'w': 4.4, 'd': 5.4, 'bars': False}, actors=[gard17(j, *q) for j, q in enumerate(GD17)],
        props=[*[CAST(f'platre17{j}', f'gard{j + 1}', s=2.0) for j in range(3)],
               *[P(f'bequille17{j}', 'crutch', on={'actor': f'gard{j + 1}', 'hand': 'L', 'offset': [0.0, -0.02, 0.0]}) for j in range(3)],
               P('plafond17', 'slab', pos=[0.0, 2.86, 4.6], opts={'w': 9.0, 'h': 0.12, 'd': 3.9, 'color': '#D9D2C4'}),
               P('ampoule17', 'cellBulb', pos=[0.35, 2.78, -1.3], opts={'drop': 0.3, 'power': 8, 'range': 8}),
               P('barreaux17', 'steelBars', pos=[-1.0, 0, 0.0], opts={'width': 1.9, 'height': 2.8}), P('barreaux17b', 'steelBars', pos=[1.65, 0, 0.0], opts={'width': 1.6, 'height': 2.8}),
               P('porte17', 'barDoor', pos=DOOR17, opts={'w': 0.9, 'open': 0.0, 'plate': True, 'plateY': PLATE17[1], 'plateW': 1.0, 'plateH': 0.42, 'frame': '#7D858F'}),
               # (review 3) a lighter wooden block, a slanted contact (HIT17) and it leaves the plate sooner, tipping its red face back toward us
               P('tampon17', 'tableStamp', pos=[PLATE17[0], 4.6, 0.75], rot=ROT17, scale=3.0, opts={'block': '#9A6A40', 'squash': [[r(ST17 - 0.01), 0.0], [ST17, 1.0], [r(ST17 + 0.04), 1.0], [r(ST17 + 0.1), 0.0]]},
                 keys=[k(0.0, visible=False), k(r(ST17 - 0.4), visible=True), k(r(ST17 - 0.4), to=HANG17, dur=0.14, ease='out'),
                       k(r(ST17 - 0.11), to=KNOB17, dur=0.11, ease='in'), k(r(ST17 - 0.11), rotTo=HIT17, dur=0.11, ease='in'),
                       k(r(ST17 + 0.07), to=BACK17, dur=0.16, ease='out'), k(r(ST17 + 0.07), rotTo=ROT17, dur=0.16, ease='out'), k(r(ST17 + 0.28), visible=False)]),
               P('marque17', 'stampMark', pos=[PLATE17[0], PLATE17[1], r(PLATE17[2] + 0.025)], opts={'text': 'PERPÉTUITÉ', 'w': 0.92, 'h': 0.36}, keys=[k(0.0, visible=False), k(ST17, visible=True)])],
        fx=[{'type': 'shake', 'at': ST17, 'dur': 0.2, 'amount': 0.02}],
        cams=[cam(0.0, [0.0, 1.55, 5.5], [-0.02, 1.55, 5.42], [0.0, 1.3, 0.5], [0.0, 1.3, 0.5], lens=66),
              glide([cam(r(ST17 + 0.1), [0.12, 1.62, 5.4], [0.12, 1.62, 5.36], [0.4, 1.78, 0.06], [0.4, 1.78, 0.06], lens=46)], 0.2)])
st.cue('clack', 'S17', ST17, 0.6); st.cue('thud', 'S17', ST17, 0.35); st.cue('clang', 'S17', r(ST17 + 0.02), 0.3)

# 18: on appeal, the table had an X-ray. The radiology room, framed tight on the light box (43 % of the width) and the doctor in teal scrubs, the
#     upturned table's legs at the left; he taps his chin four times looking at the table, blinks, his eyes dart to the dark box and back; on « radio »
#     the box blinks on: the X-ray of a table, glowing; the doctor points at it inside the frame and holds, then looks at us with a smirk before the cut
D18 = st.dur('S18'); XR18 = r(st.at('S18', 'L14', 7) - 0.05); BED = [-0.5, 0, -0.6]; UP = [BED[0], r(0.84 + 0.42), BED[2]]   # the table upside down (turned about Z: the bruise faces us)
DOC18 = [1.05, 0, -0.35]; DRY18 = -52   # (review 3) turned further toward the table (-30): looking 70 degrees off his facing, his head rolled over sideways
st.shot('S18', 'hospital', setOpts={'monitor': False}, actors=[
        # (review 3) the chin-in-hand pose held 1.6 s with the head pitched forward in front of his chest (the neck looked broken): he looks
        # level toward the table (a low look target rolled his head over), no neck bend; he taps his chin four times, blinks, his eyes dart to the dark box and back before it
        # lights, then the point
        act('docteur', DOC18, DRY18, 'stand', 'neutral', keys=[k(0.0, look=[BED[0] + 0.45, 1.95, BED[2] + 0.1]), k(0.0, toon={'reach': {'L': [0.62, 1.3, -0.3, 1, 0.03]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, look=[BED[0] + 0.5, 1.95, BED[2] + 0.1], lookDur=0.3),
            # the chin taps are a guided hand in front of the chin, not a face touch (the touch pulled his head over sideways)
            *[k(r(0.55 + 0.17 * i), toon={'reach': {'R': [*loc(DOC18, DRY18, [-0.03, [1.74, 1.69][i % 2], [0.2, 0.25][i % 2]]), 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.1 if i else 0.25, toonEase='inOut') for i in range(4)],
            k(1.2, toon={'reach': {'R': [*loc(DOC18, DRY18, [-0.03, 1.74, 0.2]), 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'lid': 1.0, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.05),
            k(1.27, toon={'reach': {'R': [*loc(DOC18, DRY18, [-0.03, 1.74, 0.2]), 1, 0.03]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.07),
            k(1.38, look=[0.55, 1.6, -1.6], lookDur=0.06), k(1.54, look=[BED[0] + 0.5, 1.95, BED[2] + 0.1], lookDur=0.08),
            k(r(XR18 + 0.05), look=[0.55, 1.6, -1.6], lookDur=0.15),
            k(r(XR18 + 0.04), toon={'reach': {'R': [0.78, 1.62, -1.15, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.12, toonEase='out'), k(r(XR18 + 0.2), look='camera', lookDur=0.1),
            k(r(XR18 + 0.3), toon={'reach': {'R': [0.78, 1.62, -1.15, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'smirk', 'brow': 0.3}}, toonDur=0.12)])],   # (review 2) the point lands and holds before the cut
        props=[P('lit18', 'xrayBed', pos=BED), P('t18', 'coffeeTable', pos=UP, rot=[0, 0, PI], opts={'bruise': True}),
               P('ecran18', 'xrayScreen', pos=[0.55, 0, -1.65], ry=-8, opts={'at': XR18})],
        cams=[FC(0.0, [0.16, 1.7, 3.6], [[-0.15, 2.12, -1.65], [1.25, 2.12, -1.65], [-0.15, 1.0, -1.65], [1.25, 1.0, -1.65], [DOC18[0] + 0.35, 2.45, DOC18[2]], [DOC18[0] - 0.3, 2.45, DOC18[2]], [DOC18[0] + 0.35, 1.0, DOC18[2]],
                                       [r(BED[0] - 0.15), 1.72, BED[2]], [r(BED[0] + 0.55), 0.95, BED[2]]], top=0.1, bottom=0.74, lenses=range(30, 60), drift=(0.0, 0.0, -0.12))])   # (review 2) tighter: the light box 43 % of the width, the doctor whole
st.cue('sfx:beep', 'S18', XR18, 0.3); st.cue('sfx:click', 'S18', r(XR18 - 0.02), 0.2)

# 19: it had a bruise. Extreme close-up on one leg of the upturned table: a blue bruise on the wood; a yellow evidence marker pops up beside it
D19 = st.dur('S19'); BRU19 = [r(BED[0] - 0.46), r(UP[1] - 0.36 * 0.55), r(BED[2] + 0.21 + 0.04)]   # the bruised leg after the turn about Z: x mirrored, pointing up
st.shot('S19', 'hospital', setOpts={'monitor': False},
        props=[P('lit19', 'xrayBed', pos=BED), P('t19', 'coffeeTable', pos=UP, rot=[0, 0, PI], opts={'bruise': True, 'legT': 0.09}),
               MARK('m19', [r(BRU19[0] + 0.15), 0.84, r(BRU19[2] + 0.05)], 5, 0.3, ry=-15, s=0.9)],
        cams=[cam(0.0, [r(BRU19[0] + 0.12), r(BRU19[1] - 0.02), r(BRU19[2] + 0.62)], [r(BRU19[0] + 0.11), r(BRU19[1] - 0.02), r(BRU19[2] + 0.55)], [r(BRU19[0] + 0.06), r(BRU19[1] - 0.13), BRU19[2]], [r(BRU19[0] + 0.06), r(BRU19[1] - 0.13), BRU19[2]], lens=40)])
st.cue('sfx:pop', 'S19', 0.3, 0.25); st.cue('sfx:sting', 'S19', 0.05, 0.2)

# 20: this man was convicted. Now he stands on a plain grey box in a low dock, in his suit, his bare feet showing over the rail, between the
#     gendarmes; the gavel falls (heard), he braces, COUPABLE lands and he steps back leaning far back, arms flung out, eyes popping, and holds it
#     a third of a second, shivering, as if hit in the chest, then settles
D20 = st.dur('S20'); HIT20 = 0.74
# (review 2) he stands on a step inside a lower dock, so his bare feet show over the rail; on COUPABLE he takes a full step back, arms flung out
DH20 = 0.55; ST20 = [DOCK[0], 0, r(DOCK[2] - 0.2)]; M20 = [DOCK[0], SH_, r(DOCK[2] - 0.05)]; BK20 = [DOCK[0], SH_, r(DOCK[2] - 0.36)]
st.shot('S20', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[
        act('mec', M20, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            # (review 3) the take lasted three frames and was back to neutral by 0.33 s: now a two-frame brace, the extreme held 0.36 s with a
            # shiver (arms flung out, eyes out, leaning far back) while he steps back, then the overshoot and the settle; the step is a plain box
            k(r(HIT20 - 0.07), toon={'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.05),
            k(HIT20, to=BK20, dur=0.2, ease='out', glide=True, face='keep'),
            *[k(r(HIT20 + 0.067 * i), toon={'lay': [-0.4, 0.0], 'sq': [0.9, 1.12, 0.9] if i % 2 == 0 else [0.92, 1.1, 0.92],
                                            'reach': {'R': [r(DOCK[0] - 0.85), r(SH_ + 1.7), r(BK20[2] + 0.12), 1, 0.04], 'L': [r(DOCK[0] + 0.85), r(SH_ + 1.7), r(BK20[2] + 0.12), 1, 0.04]},
                                            'hands': {'R': 'spread', 'L': 'spread'}, 'bend': {'legR': [0.45, 0, 0, 1, None], 'shinR': [0.3, 0, 0, 1, None]},
                                            'face': {'lid': 0.0, 'eye': 0.5, 'pop': 0.6, 'popLen': 0.18, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05 if i == 0 else 0.04, toonEase='out') for i in range(6)],
            k(r(HIT20 + 0.4), toon={'lay': [0.08, 0.0], 'sq': [1.05, 0.95, 1.05], 'reach': {'R': [r(DOCK[0] - 0.55), r(SH_ + 1.25), r(BK20[2] + 0.1), 1, 0.04], 'L': [r(DOCK[0] + 0.55), r(SH_ + 1.25), r(BK20[2] + 0.1), 1, 0.04]},
                                   'hands': {'R': 'spread', 'L': 'spread'}, 'face': {'lid': 0.2, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.1, toonEase='in'),
            k(r(HIT20 + 0.52), toon={'lay': [0.0, 0.0], 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.12)]), *gend_actors()],
        props=[SEAL('sceau20'), GKEPI('kepi20a', 'gend1'), GKEPI('kepi20b', 'gend2'), P('box20', 'dockBox', pos=DOCK, opts={'h': DH20}),
               P('stand20', 'slab', pos=[ST20[0], r(SH_ / 2), ST20[2]], opts={'w': 0.9, 'h': SH_, 'd': 0.9, 'color': '#8E9196', 'outline': 0.01})],   # (review 3) a plain grey box: the brown slab-on-legs read as the coffee table (he seemed to stand on it)
        fx=[{'type': 'shake', 'at': HIT20, 'dur': 0.15, 'amount': 0.015}],
        cams=[FC(0.0, [-0.9, 1.6, 5.0], [[DOCK[0], 3.0, M20[2]], [DOCK[0], SH_, r(DOCK[2] + 0.1)], [r(DOCK[0] - 0.8), r(SH_ + 1.6), BK20[2]], [r(DOCK[0] + 0.8), r(SH_ + 1.6), BK20[2]],
                                       [-2.35, 2.55, 1.25], [-0.45, 2.55, 1.25], [-2.35, 0.9, 1.25], [-0.45, 0.9, 1.25]], top=0.2, bottom=0.74)])
st.cue('sfx:gavel', 'S20', r(HIT20 - 0.05), 0.5); st.cue('sfx:punch', 'S20', HIT20, 0.25)

# 21: (on « coups et blessures ») the plaintiff: the coffee table on the courtroom floor, low and close, a white bandage wound round its front leg, an
#     evidence marker beside it; a gendarme kneels by it and pats its top, then looks at us; the table does not move
D21 = st.dur('S21'); PL21 = [0.6, 0, 2.6]
st.shot('S21', 'courtroom', setOpts={'sign': 'TRIBUNAL'}, actors=[
        act('gend2', [r(PL21[0] - 0.85), 0, r(PL21[2] - 0.45)], 55, 'kneel', 'neutral', keys=[k(0.0, look=[PL21[0], 0.4, PL21[2]]),
            *[k(r(0.15 + 0.22 * i), toon={'reach': {'R': [r(PL21[0] - 0.3), r(0.47 + (0.06 if i % 2 == 0 else 0.0)), r(PL21[2] - 0.05), 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.1) for i in range(4)],
            k(0.75, look='camera', lookDur=0.2)])],
        props=[SEAL('sceau21'), TBL('t21', PL21, bruise=True, bandage=True), GKEPI('kepi21', 'gend2'), MARK('m21', [r(PL21[0] + 0.45), 0, r(PL21[2] + 0.5)], 6, -1.0, ry=-20, s=1.2)],
        cams=[cam(0.0, [r(PL21[0] + 0.95), 0.55, r(PL21[2] + 2.1)], [r(PL21[0] + 0.93), 0.55, r(PL21[2] + 2.02)], [r(PL21[0] - 0.1), 0.45, PL21[2]], [r(PL21[0] - 0.1), 0.45, PL21[2]], lens=64)])

# 22: and of the three buildings. From higher up, pushing in: behind the judge (whole, at the right, behind his bench), the courtroom's back wall
#     teeters, holds, falls flat and slams in a cloud of dust; behind it, in the daylight, the three blocks on a diagonal, the same round hole through
#     all three; the judge spins round, then gives us a big take, eyes out, jaw dropped, wig lifting
D22 = st.dur('S22'); FALL22 = 0.25
# (review 1) the three blocks stand along a line 40 degrees off the camera's axis, each turned to face back along it: three separate facades step
# back with gaps between them and the three holes in line; a wooden floor runs up to the wall (no asphalt before it falls); the judge spins round
TH22 = math.radians(-40); DIR22 = [math.sin(TH22), -math.cos(TH22)]
# (review 2) a higher camera (4.6 m) puts the judge under the near hole; the judge and his bench move inside the right edge (his spin played half out of
# frame); the line of blocks starts 1 m further left, narrower (3.8 m) and shallower (2.4 m) blocks 6 m apart: each hole clears the block in front of
# it (lateral step 3.9 m > half a block + a hole) and the third is no longer cut at the left edge; the wall teeters, holds,
# falls and slams in a cloud of dust (LAND22)
BL22 = [([r(0.6 + 6.0 * j * DIR22[0]), 0, r(-11.0 + 6.0 * j * DIR22[1])], h_) for j, h_ in enumerate((7.0, 11.0, 15.0))]
LAND22 = r(FALL22 + 0.22 + 0.36)
st.shot('S22', 'parisStreet', setOpts={**STREET, 'clear': [-14.0, 14.0], 'clearL': [-14.0, 14.0]}, actors=[act('juge', [1.0, 0.3, 0.2], -20, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(r(FALL22 + 0.04), look=[-1.0, 2.5, -8.0], lookDur=0.12), k(r(FALL22 + 0.06), toon={'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.95, 1.07, 0.95], 'lay': [-0.12, 0.0]}, toonDur=0.08, toonEase='out'),
            k(r(LAND22), toon={'face': {'lid': 0.0, 'eye': 0.5, 'pop': 1.0, 'popLen': 0.3, 'mouth': 'O', 'brow': 1.0, 'jaw': 0.5}, 'sq': [1.12, 0.86, 1.12], 'hairUp': 1.0, 'lay': [0.06, 0.0]}, toonDur=0.05, toonEase='out'),
            k(r(LAND22 + 0.1), toon={'face': {'lid': 0.0, 'eye': 0.5, 'pop': 0.9, 'popLen': 0.28, 'mouth': 'O', 'brow': 1.0, 'jaw': 0.45}, 'sq': [0.94, 1.08, 0.94], 'hairUp': 0.9, 'lay': [0.04, 0.0]}, toonDur=0.06),
            k(r(LAND22 + 0.32), look='camera', lookDur=0.15), k(r(LAND22 + 0.36), toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.2)])],   # (review 3) a bigger take: eyes out on longer stalks, the jaw drops, the wig lifts
        props=[P('sol22', 'carpet', pos=[0.0, 0.0, 3.2], opts={'w': 16.0, 'd': 9.6, 'color': '#B98A5A'}), P('banc22', 'courtBench', pos=[0.7, 0, 0.5]), P('mur22', 'fallWall', pos=[0.0, 0, -1.6], opts={'w': 12.0, 'h': 6.0, 'at': FALL22, 'teeter': True}),
               *[P(f'poussiere22{j}', 'toonPuff', pos=[x_, 0.15, z_], opts={'at': LAND22, 'n': 6, 'life': 0.6, 'size': 0.55, 'rise': 0.7, 'spread': 2.2, 'color': '#E3D9C6'}) for j, (x_, z_) in enumerate([(-3.5, -6.8), (0.0, -7.2), (3.5, -6.8), (0.0, -2.0)])],
               *[P(f'blk22{j}', 'holedBlock', pos=p_, ry=r(-math.degrees(TH22)), opts={'w': 3.8, 'd': 2.4, 'h': h_, 'hole': [0.0, 1.05, 1.4], 'color': ['#EBDDC4', '#E6D3D3', '#DCE3EA'][j]}) for j, (p_, h_) in enumerate(BL22)]],
        fx=[{'type': 'shake', 'at': LAND22, 'dur': 0.2, 'amount': 0.02}],
        cams=[cam(0.0, [0.0, 4.6, 7.8], [0.6, 3.8, 5.4], [-1.1, 1.3, -12.0], [-0.9, 1.6, -12.0], lens=54, ease='inOut')])   # (review 3) the judge and his bench 0.8 m closer and a push-in toward them: his turn and take play 1.5 times larger, the three holes stay in frame
st.cue('sfx:stretch', 'S22', FALL22, 0.25); st.cue('thunder', 'S22', LAND22, 0.4); st.cue('thud', 'S22', LAND22, 0.45)

# 23: his cellmate is the table. Inside the narrow cell, toward the bars: a guard shoves him in through the door; he stumbles toward us on an arc,
#     arms flailing, and brakes on his heels beside the table's end, which stands across the cell between him and his bunk; he looks down at it; the
#     door slams behind him: he flinches and glances back over his shoulder, then looks down at the table and at us
# (review 2) the shove is seen: the guard stands beside the doorway (not behind him: two heads stacked), draws his arms back, pushes on his back; he
# stumbles in on an arc, arms out, and stops short of the table with a heel brake; the guard steps out of the doorway before the door slams, so the
# man is alone with the table
D23 = st.dur('S23'); SLAM23 = 1.15; TC = [0.0, 0, 0.85]
MS23 = [0.8, 0, 2.28]; GD23 = [1.68, 0, 2.5]; PUSH23 = 0.16; STOP23 = 0.66; E23 = [1.05, 0, 1.42]
BACK23 = [0.83, 1.42, 2.42]   # his back, where the guard's hands land
GRY23 = r(math.degrees(math.atan2(MS23[0] - GD23[0], MS23[2] - GD23[2])))
st.shot('S23', 'brightCell', setOpts={'w': 3.0, 'd': 4.4, 'bars': False}, actors=[
        # (review 3) facing -Z his left hand is at -X: the arms were crossed (an X across the chest at 15 fps); he now stumbles on an arc to the
        # table's right end, where his feet and the heel brake show beside it (they were hidden behind it); on the slam he flinches and glances back
        # over his shoulder at the door, then looks down at the table and at us
        act('mecP', MS23, 180, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [-0.06, 0.0], 'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0),
            k(r(PUSH23 + 0.02), toon={'lay': [0.22, 0.0], 'sq': [0.95, 1.07, 0.95], 'reach': {'L': [0.32, 1.55, 1.98, 1, 0.04], 'R': [1.28, 1.6, 2.0, 1, 0.04]}, 'hands': {'L': 'spread', 'R': 'spread'},
                                   'face': {'lid': 0.0, 'eye': 0.5, 'pop': 0.5, 'popLen': 0.14, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.06, toonEase='out'),
            k(r(PUSH23 + 0.02), path=[[0.78, 0, 1.98], [0.84, 0, 1.68], E23], dur=r(STOP23 - PUSH23 - 0.02), ease='out', glide=True, face='keep'),   # straight at us first, veering to the table's end once the guard has stepped out (it crossed in front of him: two heads stacked)
            k(r(PUSH23 + 0.24), toon={'lay': [0.22, 0.0], 'reach': {'L': [0.42, 1.88, 1.5, 1, 0.04], 'R': [1.45, 1.5, 1.6, 1, 0.04]}, 'hands': {'L': 'spread', 'R': 'spread'},
                                   'bend': {'legL': [-0.5, 0, 0, 1, None], 'shinL': [0.6, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.14, toonEase='inOut'),
            k(r(STOP23 - 0.04), toon={'lay': [-0.22, 0.0], 'sq': [1.06, 0.93, 1.06], 'reach': {'L': [0.62, 1.95, 1.28, 1, 0.04], 'R': [1.5, 1.9, 1.32, 1, 0.04]}, 'hands': {'L': 'spread', 'R': 'spread'},
                                   'bend': {'legR': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'clench', 'brow': 1.0}}, toonDur=0.08, toonEase='out'),   # the heel brake: leaning back, arms up
            k(r(STOP23 + 0.14), toon={'lay': [0.0, 0.0], 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2, 'gy': 0.7}, 'settle': 0.6}, toonDur=0.2, toonEase='inOut'),
            k(0.95, look=[0.0, 0.42, TC[2]], lookDur=0.12),
            *react(SLAM23, s=0.8, keep={'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line'}}, look=[0.8, 1.5, 2.45]),
            k(r(SLAM23 + 0.3), look=[0.0, 0.42, TC[2]], lookDur=0.12), k(r(SLAM23 + 0.48), look='camera', lookDur=0.12),
            k(r(SLAM23 + 0.56), toon={'face': {'lid': 1.0, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.05), k(r(SLAM23 + 0.62), toon={'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.08)]),
        act('gard1', GD23, GRY23, 'stand', 'determined', keys=[k(0.0, look=[BACK23[0], 1.6, BACK23[2]]),
            k(0.0, toon={'reach': {'R': [1.32, 1.4, 2.78, 1, 0.03], 'L': [1.52, 1.38, 2.86, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.0),   # arms drawn back
            k(r(PUSH23 - 0.04), toon={'reach': {'R': [r(BACK23[0] + 0.05), BACK23[1], r(BACK23[2] - 0.0), 1, 0.03], 'L': [r(BACK23[0] + 0.2), r(BACK23[1] - 0.05), r(BACK23[2] + 0.1), 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'},
                                   'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.05, toonEase='out'),   # contact
            k(r(PUSH23 + 0.08), toon={'reach': {'R': [0.62, 1.42, 2.1, 1, 0.03], 'L': [0.8, 1.36, 2.18, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.38, 0, 0, 1, None]}}, toonDur=0.1, toonEase='out'),   # follow-through
            k(0.28, toon={'hands': {'R': 'rest', 'L': 'rest'}}, toonDur=0.12),
            k(0.26, to=[3.3, 0, 2.95], dur=0.32, clip='walk', ease='inOut')])],   # (review 3) he steps out of the doorway sooner and further, out of frame on the left (his head stacked behind the man's)
        props=[TBL('t23', TC), P('ampoule23', 'cellBulb', pos=[-0.75, 2.8, 0.3], opts={'drop': 0.5, 'power': 6, 'swing': 0.05}),
               P('barreaux23', 'steelBars', pos=[-0.45, 0, 2.1], opts={'width': 1.5, 'height': 2.8}), P('porte23', 'barDoor', pos=[0.3, 0, 2.1], opts={'w': 0.9, 'open': -1.6, 'slam': SLAM23, 'frame': '#7D858F'})],
        cams=[cam(0.0, [-0.65, 1.3, -2.0], [-0.6, 1.29, -1.92], [0.25, 1.0, 1.2], [0.25, 1.0, 1.2], lens=66)])
st.cue('sfx:whoosh', 'S23', PUSH23, 0.25); st.cue('sfx:stepRun', 'S23', 0.25, 0.2); st.cue('sfx:brake', 'S23', r(STOP23 - 0.04), 0.2)
st.cue('clang', 'S23', SLAM23, 0.5)

# 24: he stubbed his toe again the first night. The cell, framed exactly like the first shot: his foot hits the table's leg, a blank beat, the
#     bigger take, he hops holding the hurt foot out to the side, bounces off the bunk and balances on one foot, wobbling, to the end
# (review 3) S24 hops in the figure-4 to the side (side_pose: the foot held out clear above the tabletop, one hand on it, the other arm out), one hop
# fewer, then bounces off the bunk and balances on one foot, wobbling, to the end (it read as a blow to the groin: both hands at the crotch behind
# the tabletop)
loop_shot('S24', 'brightCell', 'mecP', 0.65, setOpts={'w': 3.0, 'd': 4.8, 'bars': False}, hang=0.35, take=1.5, pose=side_pose, wobble=3,
          hops=[[HIT_AT[0], HIT_AT[2]], [0.25, -0.86], [0.05, -0.98], [-0.12, -1.08], [-0.26, -1.14]], bump=[-0.14, 0.0, -1.1],
          extra_props=[P('ampoule24', 'cellBulb', pos=[-0.55, 2.85, -0.3], opts={'drop': 0.4, 'power': 6, 'swing': 0.04}),   # (review 2) the bulb in the top left corner, off his head line
                       P('fenetre24', 'cellWindow', pos=[0.95, 2.0, -2.255], opts={'cover': [0.86, 0.66, '#D9DAD3'], 'coverAt': [-0.55, 0.0, 0.05]})])   # (review 2) the window where S01's painting is; the set's own window hidden
st.cue('sfx:crickets', 'S24', 0.0, 0.08)

SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'gloves': '#F6F6F2', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'barefoot': True, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
st.write("La table basse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecP': {**MEC, 'preset': 'mecPrisonnier'},
    **{f'swat{j + 1}': {'preset': 'swat', 'outfit': 'suit', 'hat': 'none', 'suit': '#1C2430', 'pants': '#1C2430', 'shirt': '#1C2430', 'lapel': '#1C2430', 'tie': '#1C2430', 'cuff': '#1C2430', 'gloves': '#14161A', 'glasses': False,
                         'seed': 801 + j, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},
    **{f'sold{j + 1}': {**SOLD, 'preset': 'cop' if j % 2 == 0 else 'cop2', 'seed': 805 + j} for j in range(4)},
    'pilote': {**SOLD, 'preset': 'cop', 'seed': 809, 'suit': '#4E5A32', 'facial': 'mustache'},
    'general': {'preset': 'politique', 'seed': 810, 'suit': '#4A5530', 'lapel': '#4A5530', 'tie': '#2E351E', 'glasses': False, 'facial': 'mustache', 'hair': 'receding', 'hairColor': '#6E6A64', 'beardColor': '#6E6A64', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},   # (review 2) darker grey, receding: his painted face read as a grey block
    **{f'musi{j + 1}': {'preset': 'serveur', 'seed': 811 + j, 'suit': '#B5302A', 'pants': '#1C1F2A', 'glasses': False, 'build': {'width': 1.0 + 0.1 * (j == 1), 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    **{f'gend{j + 1}': {'preset': 'cop', 'seed': 814 + j, 'suit': '#1F2A44', 'pants': '#1F2A44', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(2)},
    'avocat': {'preset': 'avocat', 'seed': 816, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jure1': {'preset': 'madame', 'seed': 817, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'jure2': {'preset': 'boss', 'seed': 818, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jure3': {'preset': 'mamie', 'seed': 819, 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    **{f'gard{j + 1}': {'preset': 'cop', 'seed': 820 + j, 'suit': '#4F6273', 'pants': '#3E4D5A', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    'docteur': {'preset': 'doctor', 'seed': 823, 'suit': '#4F9C93', 'lapel': '#4F9C93', 'cuff': '#4F9C93', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},   # (review 2) teal scrubs: a white coat on the cream wall read at 1.04:1
})
