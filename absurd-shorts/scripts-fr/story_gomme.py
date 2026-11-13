#!/usr/bin/env python3
"""La gomme à mâcher (story 51, cycle 13 of the cartoon staging): this man stepped on a piece of chewing gum three weeks ago. Since then it stretches
behind him. The pink strand crosses the whole of Paris. The town hall listed it as a communal road. On Sundays the children skip with it. The city
hung a cable car on it. Yesterday he wanted to get rid of it: he pulled hard. The strand brought him back home in one second. Since then he works
from home.
Staging: every gag is the strand pulling on his leg: the foot glued to the pavement while he walks on reading his phone (the leg stretched to twice
its length by the new foot IK, `plant`), the snap and the ripple; the strand trailing behind him, a lady hopping over it; a pink line down the street
to the Eiffel tower; a road worker painting white dashes on it and his roller getting stuck; the children turning it as a skipping rope, and at the
other end, on his sofa, his leg whirling round in time while he reads the paper; a cable-car cabin riding it over the roofs, and him hanging upside
down by the foot at his desk, still typing; the grab, the lean, the strand stretching thin and taut, the yank; flying feet first over the roofs
along the strand, deadpan; planted head first in his own sofa like a dart; working from home, the slack strand coiled on the floor, one last jerk
of the foot. Natural look; cycle 13 tools: plant (feet held at points of the world), tether sag keys / wobble / taper / thin / spin, the key-pose
probe (st.gag), the frozen / repeated-take audit."""
from story_kit import *
import math

st = Story('gomme', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 9), ('S03', 'L02', 1), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L05', 7),
         ('S08', 'L06', 0), ('S09', 'L06', 5), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L09', 4), ('S14', 'L10', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

GUM = '#F27BAA'
def STRAND(a, b, frm=None, until=None, sag=0.03, rad=0.02, taper=0.55, thin=None, **o):
    """the pink strand: a scene tether (director3: sag number or keys, wobble, taper, thin, spin)"""
    d = {'a': a, 'b': b, 'color': GUM, 'sag': sag, 'radius': rad, 'taper': taper, 'minPx': 5, 'rim': 0.35, **o}   # (pass 2) never under 5 px of the 1920 frame, a darker rim (the reviews: 1-2 px, 1.1:1 on the facades)
    if thin: d['thin'] = thin
    if frm is not None: d['from'] = frm
    if until is not None: d['until'] = until
    return d
FOOT = lambda who='mec', side='L': {'actor': who, 'joint': 'foot' + side, 'offset': [0, 0.01, 0.07]}   # the middle of the sole (the shoe hangs under the ankle joint)
HAND = lambda who='mec', side='R': {'actor': who, 'hand': side, 'offset': [0, -0.08, 0.02]}
PT = lambda p: {'point': [r(v) for v in p]}
STREET = {'clear': [-80, 80], 'paveW': 6.5, 'eiffelStyle': 'v2'}   # (pass 2) the connected Eiffel tower (the old one read as a stepladder)
LR = {'tv': False, 'carpet': False, 'pictureX': -1.7}   # (pass 2) the painting off the axis of his head (its frame sat behind it)
WINP = [1.75, 0.95, -3.55]                                          # (final pass) a window beside the sofa, its sill here: the strand goes out over it (the set's window at x 3.6 stood off every frame)
WINDOW = lambda pid: P(pid, 'window', pos=[WINP[0], WINP[1], -3.6], opts={'w': 1.0, 'h': 1.2, 'color': '#2F7F8C', 'curtains': '#C8202A'})
CITY = lambda pid: P(pid, 'cityBlocks', pos=[0, 0, 0], opts={'x0': -150, 'x1': 150, 'z0': -330, 'z1': 95, 'skip': [[-27, 27, -132, 100]], 'park': [-36, 20, -210, -140], 'seed': 23})   # (final pass) the city round the street (from the air a bare grey plain ran to the horizon)
SEAT = [0.0, 0, -2.75]
PHONE = lambda pid: P(pid, 'smartPhone', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.07, -0.06], 'face': 'camera', 'faceBack': True}, scale=1.85, opts={'case': '#22252B'})   # (pass 3) a thin dark phone (the flat yellow plane read as a card held to his ear)
READ = {'bend': {'neck': [0.62, 0, 0, 1, None]}, 'touch': {'R': ['torso', -0.06, 0.5, 0.4, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'gy': 0.8, 'lid': 0.35}}   # (pass 2) head down on his phone: absorbed (the cause of the step)
# (pass 3) the head tipped well down, the phone held out under his chin in front of the face (held at chin height beside the face it read as a call);
# guided in the frame of his torso (the touch on the face left the hand at his chest, behind the target); the phone up out of his fist (centred
# on the fist, the fist and the forearm hid it)
def PLANT(p, w=1.0, side='L', base=None):
    """a toon state with the foot held at p (weight w), on top of `base`"""
    d = dict(base or {}); d['plant'] = {side: [r(p[0]), r(p[1]), r(p[2]), w]}; return d
def RD(extra=None):
    """(pass 2) the reading state (head down on the phone) with extra channels on top"""
    d = {'bend': dict(READ['bend']), 'face': dict(READ['face']), 'touch': dict(READ['touch']), 'hands': dict(READ['hands'])}
    for k_, v in (extra or {}).items():
        if k_ in ('bend', 'face'): d[k_].update(v)
        else: d[k_] = v
    return d

# 1: the hook. Low on the pavement: he walks toward us reading his phone and puts his left shoe right on a pink blob of gum (squelch); he walks on:
#    the shoe stays
D1 = st.dur('S01'); TS = round(st.at('S01', 'L01', 6) - 0.06, 3)
BLOB = [7.2, 0, 0.0]; GUMPT = [BLOB[0], 0.03, BLOB[2]]
X1 = 7.08
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X1, 0, -1.25], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None),
            k(0.0, to=[X1, 0, 0.2], dur=TS, clip='walkRead', then='walkRead', ease='linear', face='move'),
            k(0.0, toon=RD(), toonDur=0.0), k(round(TS - 0.07, 3), toon=PLANT(GUMPT, 0.0, base=RD()), toonDur=0.0), k(TS, toon=PLANT(GUMPT, 1.0, base=RD()), toonDur=0.06),   # the shoe comes down on the gum and stays (his head down on the phone)
            k(TS, to=[X1, 0, 0.72], dur=round(D1 - TS + 0.04, 3), clip='walkRead', then='stand', ease='linear', face='keep'),
            k(round(TS + 0.22, 3), look=None)])],
        props=[PHONE('phone1'), P('blob1', 'gumBlob', pos=BLOB, opts={'r': 0.2, 'squelch': [[TS, 1.0]]})],
        cams=[FC(0.0, [7.55, 0.2, 1.75], [[GUMPT[0], 0.0, GUMPT[2]], [X1, 2.3, 0.72], [X1, 2.3, -1.25], [r(X1 + 0.5), 1.0, 0.2]], top=0.06, bottom=0.72)])
st.cue('sfx:splat', 'S01', TS, 0.45)

# 2: three weeks ago. From the front, three quarters: he walks on, on his phone; the left foot stays glued: the leg stretches back to the blob, twice
#    its length; it lets go: the leg snaps back with a ripple, a pink strand now runs from his sole to the blob; he does not even look
D2 = st.dur('S02'); SNAP = 1.0
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X1, 0, 0.72], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=PLANT(GUMPT, 1.0, base=RD()), toonDur=0.0),
            k(0.0, to=[X1, 0, 2.0], dur=round(SNAP + 0.5, 3), clip='walkRead', then='readPhone', ease='out', face='keep'),   # (final pass) 2.0: at 2.36 the leg reached its limit, the shoe lifted off the gum and his head left the frame   # (pass 2b) he stops for the take (it played while he walked on); (pass 3) slowing against the pull
            k(0.3, toon=PLANT(GUMPT, 1.0, base=RD({'lay': [0.14, 0]})), toonDur=0.4, toonEase='inOut'),   # (pass 3) leaning into it, the leg thinning
            k(round(SNAP - 0.12, 3), toon=PLANT(GUMPT, 1.0, base=RD({'sq': [0.97, 1.03, 0.97]})), toonDur=0.1),                      # the strain, just before
            k(SNAP, toon={'plant': {'L': [GUMPT[0], GUMPT[1], GUMPT[2], 0.0]}, 'wave': {'legL': [0.16, 1.0, 0.0, 1], 'shinL': [0.16, 1.0, -1.0, 1]},
                          'bend': {'legL': [-1.0, 0, 0, 1, None], 'shinL': [0.35, 0, 0, 1, None], 'armL': [0, 0.9, 0, 1, None], 'armR': [0, -0.6, 0, 1, None]}, 'lay': [-0.18, 0], 'face': {'lid': 0.0, 'brow': 0.6, 'eye': 0.3}}, toonDur=0.05, toonEase='out'),   # (pass 2) it lets go: the leg slings forward past the other, he rocks back...
            k(round(SNAP + 0.14, 3), toon={'wave': {'legL': [0.08, 1.0, 1.0, 1], 'shinL': [0.08, 1.0, 0.0, 1]}, 'bend': {'legL': [0.35, 0, 0, 1, None], 'armL': [0, 0.5, 0, 1, None], 'armR': [0, -0.4, 0, 1, None]}, 'lay': [0.16, 0], 'face': {'lid': 0.1, 'brow': 0.5}}, toonDur=0.08),   # ...stumbles forward...
            k(round(SNAP + 0.22, 3), toon={'wave': {'legL': [0.05, 1.0, 1.5, 1], 'shinL': [0.05, 1.0, 0.5, 1]}, 'bend': {'legL': [-0.2, 0, 0, 1, None], 'armL': [0, 0.3, 0, 1, None], 'armR': [0, -0.25, 0, 1, None]}, 'lay': [-0.07, 0], 'face': {'lid': 0.2, 'brow': 0.4}}, toonDur=0.07),   # (final pass) ...springs back...
            k(round(SNAP + 0.3, 3), toon={'bend': {'legL': [0.1, 0, 0, 1, None]}, 'lay': [0.03, 0], 'face': {'lid': 0.3}}, toonDur=0.06),   # ...a last wobble...
            k(round(SNAP + 0.36, 3), toon=RD({'wave': {'legL': [0.0, 1.0, 2.0, 1], 'shinL': [0.0, 1.0, 1.0, 1]}}), toonDur=0.1),   # ...and back to his phone
            k(round(SNAP + 0.34, 3), look=[r(GUMPT[0] - 1.6), 0.2, r(GUMPT[2] + 1.2)]), k(round(SNAP + 0.47, 3), look=None),   # (pass 2b) a glance back at the gum, back to his phone...
            # (pass 3) the glance three-quarters over the shoulder on our side, the eyes leading: aimed straight back we saw the back of his head
            k(round(SNAP + 0.52, 3), toon={'sq': [1.04, 0.95, 1.04]}, toonDur=0.03),   # ...the dip...
            k(round(SNAP + 0.56, 3), look='camera'),
            k(round(SNAP + 0.56, 3), toon={'sq': [0.95, 1.06, 0.95], 'bend': {'armL': [0, 0.5, 0, 1, None]}, 'reach': {'R': [r(X1 - 0.3), 0.98, 2.62, 1, 0.05]}, 'face': {'pop': 0.7, 'popLen': 0.28, 'brow': 1, 'jaw': 0.35}}, toonDur=0.04, toonEase='outBack')])],
        # (pass 3) the phone dropped to his waist in the take (on his chest it covered his chin)
        # (pass 2b) ...and the take at us, eyes out on stalks, the arms open, the forearm dropped (the phone off his face): with the take aimed at the gum behind him,
        # all we saw was the back of his head

        props=[PHONE('phone2'), P('blob2', 'gumBlob', pos=BLOB, opts={'r': 0.2, 'pull': [[0.2, 0.0], [0.6, 0.35], [round(SNAP - 0.05, 3), 0.6], [round(SNAP + 0.08, 3), 1.0]]})],   # (final pass) the gum webs up round the sole while it pulls
        tethers=[STRAND(PT(GUMPT), FOOT(), frm=SNAP, sag=0.0, rad=0.03, taper=0.5, thin=[0.8], wobble=[[SNAP, 0.06, 30, 6]])],
        cams=[FC(0.0, [1.6, 1.1, 1.25], [[GUMPT[0], 0.0, GUMPT[2]], [X1, 2.5, 2.1], [X1, 0.0, 2.1], [X1, 2.5, 1.0], [r(X1 + 0.4), 2.2, 2.1]], top=0.08, bottom=0.74),   # (final pass) his head kept in at the end of the stretch   # (pass 3) side on: the leg stretched to twice its length reads at its length (from the front it measured 1.1x); far enough back for him and the gum
              glide([FC(round(SNAP + 0.12, 3), [6.1, 1.6, 4.3], [[X1, 2.4, 2.0], [X1, 1.15, 2.0], [r(X1 - 0.45), 1.8, 2.0], [r(X1 + 0.45), 1.8, 2.0]], top=0.14, bottom=0.7, drift=(0.0, 0.0, 0.3))], 0.24)])   # (final pass) settled before the take, which now pops on camera   # (pass 2) a push in for the double take
st.cue('sfx:stretch', 'S02', 0.2, 0.3); st.cue('sfx:boing', 'S02', SNAP, 0.4)

# 3: since then it stretches behind him. From the front, low: he walks toward us on his phone, the pink strand trailing behind him all the way back to
#    the blob; a lady crossing the pavement hops over it, looks down at it, then at him
D3 = st.dur('S03'); HOP3 = 0.55
LADY_A = [5.4, 0, 4.4]; LADY_B = [r(X1 - 0.55), 0, 4.36]; LADY_C = [r(X1 + 0.55), 0, 4.32]; LADY_D = [9.4, 0, 4.25]   # (pass 3) a metre closer to us
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X1, 0, 5.3], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=RD(), toonDur=0.0), k(0.0, to=[X1, 0, 7.25], dur=round(D3 + 0.03, 3), clip='walkRead', then='stand', ease='linear', face='move'),
            k(round(D3 - 0.55, 3), look='camera')]),
        act('dame', LADY_A, 90, 'stand', 'neutral', keys=[k(0.0, look=[GUMPT[0], 0.0, 3.3]),
            k(0.0, to=LADY_B, dur=HOP3, clip='walk', then='stand', ease='linear', face='move'),
            # (pass 3) higher and held at the top
            k(HOP3, to=[X1, 0.62, 4.3], dur=0.16, glide=True, ease='out', face='keep'), k(HOP3, toon={'bend': {'legL': [-1.55, 0, 0, 1, None], 'shinL': [1.9, 0, 0, 1, None], 'legR': [-1.15, 0, 0, 1, None], 'shinR': [1.7, 0, 0, 1, None], 'armL': [0, 1.0, 0, 1, None], 'armR': [0, -1.0, 0, 1, None]}, 'sq': [0.92, 1.1, 0.92], 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.06),   # (pass 2) the hop: knees up, arms out (a stiff fold with straight legs)
            k(round(HOP3 + 0.22, 3), to=LADY_C, dur=0.14, glide=True, ease='in', face='keep'), k(round(HOP3 + 0.33, 3), toon={'sq': [1.1, 0.9, 1.1]}, toonDur=0.04), k(round(HOP3 + 0.42, 3), toon={}, toonDur=0.08),
            k(round(HOP3 + 0.38, 3), to=LADY_D, dur=round(D3 - HOP3 - 0.35, 3), clip='walk', then='stand', ease='linear', face='move'),
            k(round(HOP3 + 0.32, 3), look=[X1, 1.9, 6.4])])],
        props=[PHONE('phone3'), P('blob3', 'gumBlob', pos=BLOB, opts={'r': 0.2, 'pull': [[0.0, 1.0]]})],
        tethers=[STRAND(PT(GUMPT), FOOT(), sag=0.0, rad=0.07, taper=0.35, thin=[4.0])],
        cams=[FC(0.0, [4.3, 1.05, 10.4], [[X1, 2.3, 5.3], [X1, 2.3, 7.25], [GUMPT[0], 0.0, GUMPT[2]], [5.6, 1.9, 4.4], [9.0, 1.9, 4.25], [X1, 0.0, 7.25]], top=0.1, bottom=0.74, drift=(0.0, 0.0, 0.25))])

# 4: the pink strand crosses the whole of Paris. High over the street: a pink line down the middle of the avenue to the Eiffel tower; a pluck runs
#    along it
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', setOpts={**STREET, 'clear': [-200, 80]}, actors=[],
        props=[P('blob4', 'gumBlob', pos=[7.2, 0, 26.0], scale=6.0, opts={'r': 0.13}), CITY('city4')],
        tethers=[STRAND(PT([7.2, 0.4, 26.0]), PT([-6.0, 0.4, -160.0]), sag=0.0, rad=0.32, taper=0.0, via=[[3.0, 8.0, 6.0], [-13.5, 22.0, -18.0], [12.5, 23.0, -62.0], [-12.5, 22.0, -105.0], [-7.0, 8.0, -145.0]], ripple=[[0.25, 2.2, 0.9], [1.3, 2.2, 0.9]], segments=96, minPx=6)],   # (pass 2) over the roofs of block after block to the tower (one straight line down one street did not say « all of Paris »)
        cams=[cam(0.0, [-16.0, 40.0, 62.0], [-12.5, 37.0, 47.0], [-4.0, 14.0, -60.0], [-4.0, 15.0, -68.0], lens=44)])   # (pass 3) the top of the tower inside the frame
        # (pass 2c) a real flight along the strand, a second pluck (the freeze check read 1.07 s with nothing moving by a pixel at strip size)
st.cue('whoosh', 'S04', 0.25, 0.25, 0.8, 300, 900)

# 5: the town hall listed it as a communal road. On the pavement: a road worker walks backwards painting white dashes on the strand with a roller on a
#    pole; behind him a blue street plate VOIRIE COMMUNALE on a post; the roller sticks: he tugs, a pink thread stretches from it and snaps; he looks at us
D5 = st.dur('S05'); CARD5 = round(st.at('S05', 'L04', 4) - 0.05, 3); STK5 = 1.1   # (pass 3) earlier: the tug, the snap, the stumble and the plate need 1.1 s
SX5 = 6.4; W5A = [6.95, 0, 1.9]; W5B = [6.95, 0, -0.35]; WALK5 = 1.05; W5C = [6.95, 0, -0.85]
POLE5 = 1.45; TIL5 = 2.26                                           # the pole: from the hands (prop origin) down and forward (+Z) to the roller on the strand
def HANDLE5(t):                                                     # where his hands hold the pole at t (he walks backwards toward -Z, facing +Z)
    u = min(1.0, max(0.0, t / WALK5)); return [r(SX5 + 0.12), 1.05, r(W5A[2] + 0.32 + (W5B[2] - W5A[2]) * u)]
HEAD5 = lambda t, a=TIL5: [SX5, r(HANDLE5(t)[1] + POLE5 * math.cos(a)), r(HANDLE5(t)[2] + POLE5 * math.sin(a))]
DASHES = [(z, r(max(0.05, (W5A[2] + 0.32 + POLE5 * math.sin(TIL5) - z) / (W5A[2] - W5B[2]) * WALK5))) for z in (3.0, 2.6, 2.2, 1.8, 1.4)]
def GRIP5(t, a=TIL5, extra=None):
    return GRIPH(HANDLE5(t), a, extra)
H2 = [r(SX5 + 0.12), 1.12, -0.62]; H2b = [r(SX5 + 0.12), 1.18, -0.78]; H3 = [r(SX5 + 0.12), 1.05, -0.53]   # (pass 3) the hands going back with him: leaning, the snap, after the stumble
def GRIPH(h, a=TIL5, extra=None):
    d = {'reach': {'R': [h[0], h[1], h[2], 1, 0.05], 'L': [h[0], r(h[1] + 0.25 * math.cos(a)), r(h[2] + 0.25 * math.sin(a)), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
    d.update(extra or {}); return d
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('ouvrier', W5A, 0, 'stand', 'neutral', keys=[k(0.0, look=[SX5, 0.0, 2.6]),
            k(0.0, to=W5B, dur=WALK5, clip='walk', then='stand', ease='linear', face='keep', back=True),                        # backwards, painting
            *[k(round(t_, 3), toon=GRIP5(t_), toonDur=0.15, toonEase='linear') for t_ in (0.0, 0.3, 0.6, 0.9, WALK5)],
            k(STK5, toon=GRIP5(WALK5, 1.95, {'sq': [0.97, 1.04, 0.97]}), toonDur=0.08),                                      # he lifts: it sticks
            k(round(STK5 + 0.14, 3), toon=GRIP5(WALK5, 2.1), toonDur=0.08),
            k(round(STK5 + 0.26, 3), toon=GRIPH(H2, 1.72, {'sq': [0.93, 1.07, 0.93], 'lay': [-0.6, 0], 'bend': {'legL': [-0.35, 0, 0, 1, None], 'shinL': [0.3, 0, 0, 1, None]}, 'face': {'brow': -0.7, 'lid': 0.55, 'jaw': 0.35}}), toonDur=0.26, toonEase='out'),
            # (pass 3) the big tug: leaning back 35 degrees, a foot up, the gum thread stretching to arm's length (at 13 degrees the review saw him upright)
            k(round(STK5 + 0.52, 3), to=W5C, dur=0.3, clip='walk', then='stand', ease='out', face='keep', back=True),            # it snaps: a stumble backwards...
            k(round(STK5 + 0.52, 3), toon=GRIPH(H2b, 1.5, {'lay': [-0.38, 0], 'face': {'brow': 0.6, 'eye': 0.3, 'jaw': 0.2}}), toonDur=0.05, toonEase='out'),
            k(round(STK5 + 0.64, 3), toon=GRIPH(H2b, 1.6, {'lay': [-0.5, 0], 'bend': {'legR': [-0.4, 0, 0, 1, None], 'shinR': [0.3, 0, 0, 1, None]}, 'face': {'brow': 0.8, 'eye': 0.35, 'jaw': 0.3}}), toonDur=0.08),   # (final pass) ...still going, a foot up...
            k(round(STK5 + 0.8, 3), toon=GRIPH(H3, 1.95, {'lay': [-0.1, 0]}), toonDur=0.12, settle=0.6),                         # ...caught...
            k(round(STK5 + 0.9, 3), toon=GRIPH(H3, 1.95, {'lay': [0.03, 0], 'sq': [1.02, 0.98, 1.02]}), toonDur=0.06),   # ...settles
            k(round(STK5 + 0.92, 3), look='camera')])],
        props=[P('roller5', 'paintRoller', pos=HANDLE5(0.0), rot=[TIL5, 0, 0], opts={'len': POLE5, 'rollerW': 0.22, 'rollerR': 0.065, 'color': '#F4F2EA', 'sleeve': '#F4F2EA'},
                 keys=[k(0.0, to=HANDLE5(WALK5), dur=WALK5, ease='linear'), k(STK5, rotTo=[1.95, 0, 0], dur=0.08), k(round(STK5 + 0.14, 3), rotTo=[2.1, 0, 0], dur=0.08),
                       k(round(STK5 + 0.26, 3), rotTo=[1.72, 0, 0], dur=0.26, ease='out'), k(round(STK5 + 0.26, 3), to=H2, dur=0.26, ease='out'),
                       k(round(STK5 + 0.52, 3), rotTo=[1.45, 0, 0], dur=0.05, ease='out'), k(round(STK5 + 0.52, 3), to=H2b, dur=0.05, ease='out'),   # (pass 3) the release whips the roller up...
                       k(round(STK5 + 0.58, 3), rotTo=[2.0, 0, 0], dur=0.3, ease='inOut'), k(round(STK5 + 0.58, 3), to=H3, dur=0.28, ease='inOut')]),   # ...and it falls back
               P('plaque5', 'streetPlaque', pos=[8.6, 0, -1.1], ry=-25, opts={'lines': ['VOIRIE', 'COMMUNALE'], 'post': 2.45, 'w': 0.95, 'h': 0.5, 'screw': [[round(STK5 + 0.56, 3), 0.5]]}),   # (pass 2) the plate swings on its last screw (it never moved)
               *[P(f'dash5{i}', 'paperSheet', pos=[SX5, 0.1, z], rot=[round(-PI / 2, 4), 0, 0], opts={'w': 0.08, 'h': 0.3, 'paper': '#FFFFFF', 'bright': True}, keys=[k(0.0, visible=False), k(t_, visible=True)]) for i, (z, t_) in enumerate(DASHES)]],
        tethers=[STRAND(PT([SX5, 0.04, -9.0]), PT([SX5, 0.04, 9.0]), sag=0.0, rad=0.05, taper=0.0, n=12),
                 STRAND(PT([SX5, 0.07, r(HEAD5(WALK5)[2])]), {'prop': 'roller5', 'offset': [0, round(POLE5 - 0.04, 3), 0.03]}, frm=round(STK5 - 0.02, 3), until=round(STK5 + 0.53, 3), sag=0.0, rad=0.035, taper=0.6)],   # (pass 3) a thick thread, stretched for a quarter second
        cams=[FC(0.0, [4.0, 1.3, 4.6], [[6.95, 2.25, 1.9], [6.95, 2.25, -0.35], [8.6, 2.5, -1.1], [8.6, 1.95, -1.1], [SX5, 0.0, 3.0], [SX5, 0.0, -1.0]], top=0.22, bottom=0.74),
              glide([FC(round(STK5 + 0.05, 3), [4.7, 1.3, 2.7], [[6.95, 2.25, -0.35], [6.95, 2.2, -0.85], [8.6, 2.5, -1.1], [8.6, 1.95, -1.1], [SX5, 0.0, 1.2], [6.95, 0.0, -0.85]], top=0.22, bottom=0.74)], 0.4)])   # (pass 3) a push in on the tug   # (probe) his head below the title card band (29 % of it under VOIRIE COMMUNALE)
st.card('S05', 'VOIRIE COMMUNALE', at=CARD5)
st.cue('sfx:scratch', 'S05', 0.15, 0.25); st.cue('sfx:stretch', 'S05', round(STK5 + 0.26, 3), 0.3); st.cue('sfx:twang', 'S05', round(STK5 + 0.52, 3), 0.3)

# 6: on Sundays the children skip with it. On the pavement, two children turn the strand like a skipping rope, a third jumps it, in time
D6 = st.dur('S06'); FQ = 1.5; ZA, ZB, XK = -22.0, -18.4, 6.6; ZC = round((ZA + ZB) / 2, 3)
def CIRC(t0, t1, c, rr, f, ph=0.0, n=12, w=1.0, tip=0.05):
    """reach keys that turn a hand round a small circle in the plane y-x at c (a skipping rope's handle)"""
    out, i = [], 0
    while True:
        t = round(t0 + i / (n * f), 3)
        if t > t1: break
        a = 2 * PI * (f * t + ph); out.append((t, [r(c[0] + rr * math.sin(a)), r(c[1] - rr * math.cos(a)), r(c[2]), w, tip])); i += 1
    return out
def TURN(side, c, ph):
    return [k(t, toon={'reach': {side: p}, 'hands': {side: 'grip'}}, toonDur=round(1 / (12 * FQ), 3), toonEase='linear') for t, p in CIRC(0.0, D6, c, 0.13, FQ, ph)]
HOPS6 = [round(n / FQ, 3) for n in range(0, 4) if n / FQ < D6]
def JUMPS(base):
    ks = []
    for th in HOPS6:
        a = max(0.0, round(th - 0.13, 3)); ks += [k(a, to=[base[0], 0.26, base[2]], dur=0.12, glide=True, ease='out', face='keep'), k(round(a + 0.12, 3), to=list(base), dur=0.12, glide=True, ease='in', face='keep'),
                                                  k(round(a + 0.24, 3), toon={'sq': [1.1, 0.88, 1.1], 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.03), k(round(a + 0.3, 3), toon={'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.06)]
    return ks
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('enfant1', [XK, 0, ZA], 0, 'stand', 'happy', keys=[k(0.0, look=[XK, 0.9, ZC]), *TURN('R', [XK - 0.05, 0.85, ZA + 0.32], 0.0)]),
        act('enfant2', [XK, 0, ZB], -110, 'stand', 'happy', keys=[k(0.0, look='camera'), *TURN('R', [XK - 0.2, 0.85, ZB - 0.3], 0.0)]),   # (pass 3) turned to us, the rope in his right hand (his back was to us)
        act('enfant3', [XK, 0, ZC], -90, 'stand', 'happy', keys=[k(0.0, look='camera'), *JUMPS([XK, 0, ZC])])],
        tethers=[STRAND(HAND('enfant1', 'R'), HAND('enfant2', 'R'), sag=0.24, rad=0.028, taper=0.2, spin=[FQ, 0.0]),
                 STRAND(PT([XK, 0.3, -70.0]), HAND('enfant1', 'R'), sag=0.004, rad=0.026, taper=0.0),
                 STRAND(HAND('enfant2', 'R'), PT([XK, 0.03, 40.0]), sag=0.0, rad=0.026, taper=0.0, via=[[r(XK - 0.45), 0.03, r(ZB + 0.45)]])],   # (pass 3) the tail drops to the pavement in front of him
        cams=[FC(0.0, [1.1, 1.35, -13.2], [[XK, 1.45, ZA], [XK, 1.45, ZB], [XK, 0.0, ZC], [XK, 1.85, ZC], [XK, 0.0, ZA], [XK, 0.0, ZB], [XK, 1.1, r(ZB + 0.45)], [XK, 1.1, r(ZA - 0.45)]], top=0.12, bottom=0.74)])
st.cue('sfx:whoosh', 'S06', 0.0, 0.2)

# 7: at the other end, on his sofa, reading the paper, deadpan: his left leg whirls round in time with the rope, the strand going out of the window
D7 = st.dur('S07'); C7 = [r(SEAT[0] + 0.78), 0.8, r(SEAT[2] + 0.45)]; WIN7 = [WINP[0], r(WINP[1] + 0.06), r(WINP[2] + 0.02)]   # (final pass) out over the sill of the window beside the sofa   # (pass 2) the circle at his side, in the plane of the wall
def WHIRL(t0, t1, f, rr=0.42, ph=0.25):
    out, i = [], 0
    while True:
        t = round(t0 + i / (12 * f), 3)
        if t > t1: break
        a = 2 * PI * (f * t + ph); p = [r(C7[0] + rr * math.sin(a)), r(C7[1] - rr * math.cos(a)), C7[2]]
        out.append(k(t, toon={**PAPER7, 'plant': {'L': [*p, 1.0]}, 'sq': [1.0, r(1.0 - 0.025 * math.cos(a)), 1.0], 'bend': {'spine': [r(0.03 * math.cos(a)), 0, r(0.07 * math.sin(a)), 1, None]}}, toonDur=round(1 / (12 * f), 3), toonEase='linear')); i += 1   # (final pass) the torso jostled by each turn of the leg
    return out
PAPER7 = {'reach': {'L': [r(SEAT[0] - 0.25), 1.3, r(SEAT[2] + 0.5), 1, 0.05], 'R': [r(SEAT[0] + 0.25), 1.3, r(SEAT[2] + 0.5), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}
st.shot('S07', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[SEAT[0], 1.35, r(SEAT[2] + 0.45)]), *WHIRL(0.0, D7, FQ), k(round(D7 - 0.5, 3), look='camera')])],
        props=[P('paper7', 'newspaper', pos=[SEAT[0], 1.08, r(SEAT[2] + 0.45)], rot=[1.3, 0, 0], scale=1.55, opts={'headline': 'DIMANCHE'}), WINDOW('win7')],
        tethers=[STRAND(FOOT(), PT(WIN7), sag=0.16, rad=0.026, taper=0.25, spin=[FQ, 0.25])],
        cams=[FC(0.0, [0.55, 1.25, 0.4], [[SEAT[0], 1.9, SEAT[2]], [r(C7[0] + 0.45), 0.3, C7[2]], [r(C7[0] + 0.45), 1.25, C7[2]], [r(SEAT[0] - 0.5), 1.0, SEAT[2]], [r(WINP[0] + 0.3), 1.6, -3.55], [r(WINP[0] + 0.3), 0.9, -3.55]], top=0.1, bottom=0.74),   # (final pass) the window in the frame
              glide([FC(round(D7 - 0.62, 3), [0.3, 1.5, -1.25], [[SEAT[0], 1.95, SEAT[2]], [r(SEAT[0] - 0.42), 1.05, SEAT[2]], [r(SEAT[0] + 0.42), 1.05, SEAT[2]]], top=0.12, bottom=0.72)], 0.35)])   # (final pass) a real waist-up shot for the glance (1.25x closer read as the same shot)   # (pass 3) a medium shot: the leg still turning beside his glance   # (pass 2) a push in for his glance at us
st.cue('sfx:whoosh', 'S07', 0.1, 0.2)

# 8: the city hung a cable car on it. From a roof: a red cabin with three riders rides along the pink strand over the street, swinging, the strand
#    dipping under it; the Eiffel tower behind
D8 = st.dur('S08'); Y8, Z8 = 15.5, -12.0
st.shot('S08', 'parisStreet', setOpts={**STREET, 'clear': [-200, 80]}, actors=[],
        props=[P('cab8', 'cableCar', pos=[-4.6, round(Y8 - 2.2, 3), Z8], opts={'riders': 3, 'swing': [[0.0, 0.16], [0.6, 0.07]], 'tilt': -0.04, 'glassOpacity': 0.28, 'riderScale': 1.35, 'lean': 0.2, 'riderFace': True, 'riderLook': 0.4}, keys=[k(0.0, to=[2.2, round(Y8 - 2.2, 3), Z8], dur=D8, ease='linear')]), CITY('city8')],   # (pass 2) the strand dips under the cabin; riders seen (opaque panes hid them)
        tethers=[STRAND(PT([-20.0, round(Y8 + 1.7, 3), Z8]), {'prop': 'cab8', 'offset': [0, 0.06, 0]}, sag=0.0, rad=0.07, taper=0.0, n=14),
                 STRAND({'prop': 'cab8', 'offset': [0, 0.06, 0]}, PT([20.0, round(Y8 + 1.7, 3), Z8]), sag=0.0, rad=0.07, taper=0.0, n=14),
                 STRAND(PT([-70.0, round(Y8 + 1.7, 3), Z8]), PT([-20.0, round(Y8 + 1.7, 3), Z8]), sag=0.0, rad=0.07, taper=0.0, n=6),
                 STRAND(PT([20.0, round(Y8 + 1.7, 3), Z8]), PT([70.0, round(Y8 + 1.7, 3), Z8]), sag=0.0, rad=0.07, taper=0.0, n=6)],
        # (pass 3) the strand pulled down into a V by the grip (13 degrees each side; at 3 degrees it read as a straight bar)
        cams=[cam(0.0, [-3.6, 12.8, -4.2], [0.2, 12.8, -4.2], [-4.4, 12.3, -12.0], [1.9, 12.3, -12.0], lens=44)])
st.cue('sfx:rotor', 'S08', 0.0, 0.25)

# 9: ... and him at his desk, hanging upside down by the foot from the strand that comes in by the window, swinging gently, still typing, deadpan
D9 = st.dur('S09'); ME9 = [-1.75, 3.17, -2.3]   # (pass 3) 13 cm lower: his face just over the lid, his hands down on the keys (they hung at head height)
HANG = {'lay': [0, round(PI, 4)], 'bend': {'legR': [0.55, 0, 0, 1, None], 'shinR': [-1.5, 0, 0, 1, None]}}
WIN9 = [0.4, 3.35, -3.36]                                                                     # a window high on the back wall: the strand comes in there
SW9 = 0.035; KEYS9 = [-1.75, 0.8, -1.82]; STEP9 = 0.1                                      # (pass 3) a gentle swing; the middle of the keyboard (laptop turned to him)
A9 = lambda t: round(PI + SW9 * math.sin(t * 2 * PI * 0.9), 4)
def MIRROR9(p, a):
    """(pass 3) a hand target for a body rolled by `a` about its feet: the reach is solved before the roll, so it is given the point the roll carries onto p"""
    dx, dy = p[0] - ME9[0], p[1] - ME9[1]; c_, s_ = math.cos(a), math.sin(a)
    return [r(ME9[0] + c_ * dx + s_ * dy), r(ME9[1] - s_ * dx + c_ * dy), r(p[2])]
def TYPE9(i, a):
    """(pass 3) both hands on the keys, tapping in turn (the reach pointed them at the ceiling when given the keys themselves: hence MIRROR9)"""
    up = 0.04 if i % 2 else 0.0
    L = [r(KEYS9[0] - 0.1), r(KEYS9[1] + 0.04 - up), KEYS9[2]]; R = [r(KEYS9[0] + 0.1), r(KEYS9[1] + up), KEYS9[2]]
    return {'reach': {'L': [*MIRROR9(L, a), 1, 0.05], 'R': [*MIRROR9(R, a), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}, 'hose': 0.1}
st.shot('S09', 'office', setOpts={'door': False}, actors=[
        act('mec', ME9, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            *[k(round(i * STEP9, 3), toon={**HANG, 'lay': [0, A9(i * STEP9)], **TYPE9(i, A9(i * STEP9)), 'tie': [0.95, 0.2, 1.3], 'hip': 0}, toonDur=(STEP9 if i else 0.0), toonEase='linear') for i in range(int(D9 / STEP9) + 2)]])],
        # (pass 3) the first key is the settled hang (it popped in from a standing pose); the tie swung aside off his face; hip 0: no idle weight shift (it slid the hands off the keys)
        props=[P('desk9', 'desk', pos=[-1.75, 0, -1.55], ry=180, opts={'w': 1.2, 'd': 0.6}), P('laptop9', 'laptop', pos=[-1.75, 0.76, -1.72], ry=180, opts={'text': 'RAPPORT'}),
               P('win9', 'plainWall', pos=[WIN9[0], 2.75, -3.38], opts={'w': 1.0, 'h': 1.2, 'color': '#BFE3F5'})],   # (pass 2) the window the strand comes in by
        tethers=[STRAND(FOOT(), PT(WIN9), sag=0.05, rad=0.03, taper=0.2)],
        cams=[FC(0.0, [-0.6, 1.6, 1.6], [[-1.75, 3.5, -2.3], [-1.75, 0.85, -2.3], [-1.75, 0.74, -1.45], [WIN9[0], 3.4, WIN9[2]], [-2.25, 1.5, -2.3]], top=0.06, bottom=0.74)])   # (pass 2) wider: the shoe, the strand to the window, his face at the keys
st.cue('sfx:squeak', 'S09', 0.1, 0.25); st.cue('sfx:click', 'S09', 0.0, 0.25)

# 10: yesterday he wanted to get rid of it. On the pavement, the strand running from his shoe back toward home: he looks down, bends, grabs it with
#     both hands, stands up with it, plants his feet wide, takes a deep breath
D10 = st.dur('S10'); X10, Z10 = 7.1, 40.0; GRAB = 0.55; UP10 = 1.0
FAR = PT([7.2, 0.05, 0.0])
WIDE10 = {'L': [r(X10 - 0.27), 0.0, r(Z10 + 0.04), 1.0], 'R': [r(X10 + 0.27), 0.0, r(Z10 - 0.04), 1.0]}   # (pass 3) the feet planted wide from the grab on (together in the wide shot)
def HOLD10(lift=0.95, fwd=0.4, extra=None):
    d = {'plant': WIDE10, 'reach': {'L': [r(X10 - 0.08), lift, r(Z10 - fwd + 0.05), 1, 0.05], 'R': [r(X10 + 0.06), r(lift - 0.04), r(Z10 - fwd - 0.12), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}
    d.update(extra or {}); return d
st.shot('S10', 'parisStreet', setOpts={**STREET, 'clear': [-80, 120]}, actors=[
        act('mec', [X10, 0, Z10], 180, 'stand', 'unimpressed', keys=[k(0.0, look=[X10, 0.0, r(Z10 - 0.6)]),
            k(round(GRAB - 0.27, 3), to=[X10, -0.42, Z10], dur=0.24, glide=True, ease='out', face='keep'),
            k(round(GRAB - 0.25, 3), toon={'plant': WIDE10, 'bend': {'spine': [0.45, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'reach': {'L': [r(X10 - 0.05), 0.12, r(Z10 - 0.5), 1, 0.05], 'R': [r(X10 + 0.06), 0.12, r(Z10 - 0.65), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.25),   # crouches and grabs
            k(GRAB, toon={'plant': WIDE10, 'bend': {'spine': [0.45, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'reach': {'L': [r(X10 - 0.05), 0.1, r(Z10 - 0.5), 1, 0.05], 'R': [r(X10 + 0.06), 0.1, r(Z10 - 0.65), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}, toonDur=0.08),
            k(round(UP10 - 0.3, 3), to=[X10, 0, Z10], dur=0.3, glide=True, ease='inOut', face='keep'),
            k(UP10, toon=HOLD10(), toonDur=0.3, toonEase='outBack'), k(round(UP10 + 0.1, 3), look=[X10, 1.0, r(Z10 - 8)]),
            k(round(UP10 + 0.4, 3), toon=HOLD10(extra={'bend': {'spine': [-0.14, 0, 0, 1, None]}, 'sq': [1.04, 1.05, 1.07], 'scl': {'head': [1.04, 1.02, 1.04]}, 'face': {'eye': 0.15}}), toonDur=0.14, toonEase='out'),   # (pass 3) first the chest rises...
            k(round(UP10 + 0.56, 3), toon=HOLD10(extra={'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'sq': [1.1, 1.06, 1.16], 'scl': {'head': [1.55, 1.2, 1.55]}, 'face': {'expr': 'puffed', 'exprW': 1.0, 'eye': 0.25, 'puff': 1.0}}), toonDur=0.3, toonEase='inOut'),   # (final pass) half again as wide (at 1.3 it read as 20 %)
            # ...then the head swells like a balloon over nine frames, the puffed face (eyes open, frown, cheeks out)...
            *[k(round(UP10 + 0.88 + 0.066 * i_, 3), toon=HOLD10(extra={'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'sq': [round(1.1 + (0.012 if i_ % 2 else -0.008), 3), 1.06, 1.16], 'scl': {'head': ([1.6, 1.23, 1.6] if i_ % 2 else [1.5, 1.17, 1.5])}, 'face': {'expr': 'puffed', 'exprW': 1.0, 'eye': 0.25, 'puff': 1.0}}), toonDur=0.033) for i_ in range(4)],
            # ...and shakes in the hold, about to burst (it froze flat)
            k(round(UP10 + 0.9, 3), look='camera')])],
        tethers=[STRAND(FOOT(), HAND('mec', 'L'), frm=round(GRAB + 0.02, 3), sag=0.25, rad=0.024, taper=0.3),
                 STRAND(HAND('mec', 'R'), FAR, frm=round(GRAB + 0.02, 3), sag=0.0, rad=0.026, taper=0.0, thin=[2.0], n=14),
                 STRAND(FOOT(), FAR, until=round(GRAB + 0.02, 3), sag=0.0, rad=0.026, taper=0.0, n=14)],
        cams=[FC(0.0, [4.4, 1.3, 36.6], [[X10, 2.3, Z10], [X10, 0.0, Z10], [r(X10 - 0.4), 1.0, r(Z10 - 1.0)], [r(X10 + 0.5), 1.2, Z10]], top=0.12, bottom=0.74),
              glide([FC(round(UP10 + 0.02, 3), [5.6, 1.7, 37.6], [[X10, 2.55, Z10], [X10, 0.8, r(Z10 - 0.35)], [r(X10 - 0.6), 1.7, Z10], [r(X10 + 0.6), 1.7, Z10]], top=0.12, bottom=0.7)], 0.3)])   # (final pass) the fists and the strand above the caption band, room for the swollen head   # (pass 2) a push in for the puffed cheeks; (pass 3) settled before the breath (it read as more camera move)
st.cue('sfx:stretch', 'S10', UP10, 0.25); st.cue('sfx:sniff', 'S10', round(UP10 + 0.7, 3), 0.3)

# 11: he pulled hard. From the side: he leans right back, arms out along the strand, which goes thin and taut and hums; he trembles; held; then the
#     strand wins: his arms shoot out after it, his feet leave the ground, and he is gone out of the frame
D11 = st.dur('S11'); YANK = 1.12; GONE = round(YANK + 0.37, 3)   # (pass 3) GONE: he leaves after the hang; (final pass) held eleven frames (five did not register)
def PULL(lean, fwd, extra=None):
    d = {'lay': [round(-lean, 3), 0], 'reach': {'L': [r(X10 - 0.06), 1.0, r(Z10 - fwd), 1, 0.05], 'R': [r(X10 + 0.06), 0.97, r(Z10 - fwd - 0.14), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'},
         'bend': {'legL': [-0.25, 0.22, 0, 1, None], 'legR': [-0.25, -0.22, 0, 1, None], 'shinL': [0.45, 0, 0, 1, None], 'shinR': [0.45, 0, 0, 1, None]},
         'plant': {'L': [r(X10 - 0.2), 0.0, r(Z10 - 0.35), 1.0], 'R': [r(X10 + 0.2), 0.0, r(Z10 - 0.3), 1.0]}, 'face': {'expr': 'strain', 'exprW': 1.0, 'puff': 0.9},
         'scl': {'head': [1.12, 1.04, 1.12]}}   # (pass 2b) still swollen with the held breath (it goes out at the pop), the strain (eyes squeezed, teeth, vein); (pass 3) the feet apart (they crossed)
    if extra: d.update(extra)
    return d
def UHOH(w=1.0, extra=None):
    """(pass 3) yanked off the pavement: horizontal on his side, facing us, the arms over his head along the strand, an uh-oh at us"""
    d = {'lay': [0, round(PI / 2, 4)], 'bend': {'armL': [0, 2.8, 0, 1, None], 'armR': [0, -2.8, 0, 1, None], 'legL': [0.3, 0, 0, 1, None], 'shinL': [0.55, 0, 0, 1, None], 'legR': [0.08, 0, 0, 1, None]},
         'hands': {'L': 'grip', 'R': 'grip'}, 'hairUp': 1.0, 'face': {'brow': 1.0, 'pop': round(0.45 * w, 3), 'popLen': 0.25, 'mouth': 'O', 'jaw': round(0.15 + 0.15 * w, 3), 'lid': 0.0, 'noBlink': 1}}
    if extra: d.update(extra)
    return d
TREM11 = [round(0.36 + 0.066 * j_, 3) for j_ in range(6)]
CAM11 = [r(X10 - 2.9), 1.45, r(Z10 - 3.1)]
st.shot('S11', 'parisStreet', setOpts={**STREET, 'clear': [-80, 120]}, actors=[
        act('mec', [X10, 0, r(Z10 + 0.15)], 180, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [X10, 1.0, r(Z10 - 8)], 'cheat': 0.45}),
            # (pass 3) no travel smear: on his side the smear's sideways stretch stood him upright at the exit
            # (pass 3) the strain face cheated toward us (side-on it read as a profile)
            k(0.0, toon=PULL(0.2, 0.45), toonDur=0.0), k(0.04, toon=PULL(0.45, 0.55), toonDur=0.28, toonEase='out'),   # (pass 3) he leans right back at once...
            *[k(t_, toon=PULL(round(0.45 + 0.012 * j_ + (0.012 if j_ % 2 else -0.012), 3), 0.56, {'sq': [1.0, (1.02 if j_ % 2 else 0.985), 1.0]}), toonDur=0.033) for j_, t_ in enumerate(TREM11)],
            # ...trembling every two frames, the lean creeping further back (the pull pose was the same for 0.7 s)
            k(0.76, toon=PULL(0.53, 0.58, {'face': {'puff': 0.0, 'brow': 1.0, 'pop': 0.75, 'popLen': 0.32, 'lid': 0.0, 'mouth': 'O', 'jaw': 0.5}, 'hairUp': 1.0, 'scl': {}}), toonDur=0.033, toonEase='out'),   # (pass 2) it is going to win: eyes out on stalks, hair up...
            *[k(round(0.8 + 0.066 * i, 3), toon=PULL(0.53, 0.58, {'face': {'brow': 1.0, 'pop': 0.75, 'popLen': 0.32, 'lid': 0.0, 'mouth': 'O', 'jaw': 0.5}, 'hairUp': 1.0, 'scl': {}, 'sq': [1.0, round(1.0 + (0.02 if i % 2 else -0.02), 3), 1.0]}), toonDur=0.033) for i in range(4)],   # ...held ten frames, shaking
            k(YANK, look='camera'), k(YANK, face=[CAM11[0], CAM11[2]], turn=0.1),
            k(YANK, toon=UHOH(0.0), toonDur=0.06, toonEase='out'),
            k(YANK, to=[r(X10 - 0.7), 1.0, r(Z10 + 0.85)], dur=0.07, glide=True, ease='out', face='keep'),   # (pass 3) yanked off the pavement, spun round to us...
            k(round(YANK + 0.07, 3), to=[r(X10 - 0.62), 1.08, r(Z10 + 0.7)], dur=0.3, glide=True, ease='linear', face='keep'), k(round(YANK + 0.12, 3), look='camera'),   # ...hanging there eleven frames, eyes on us: uh-oh...
            # (the body tips about its feet: the feet set back toward our right so that the 2.5 m from his shoes to his hands sit in the frame)
            k(round(YANK + 0.1, 3), toon=UHOH(1.0), toonDur=0.08),
            k(GONE, toon=UHOH(1.0, {'sq': [0.8, 1.3, 0.8]}), toonDur=0.04),
            k(GONE, to=[r(X10 + 1.0), 3.0, r(Z10 - 26.0)], dur=0.1, glide=True, ease='in', face='keep')])],   # ...and gone, stretched, along the strand (frame left)
        props=[P('dust11', 'dustPuff', pos=[X10, 0.1, r(Z10 + 0.1)], scale=0.45, opts={'once': True, 'startAt': YANK, 'period': 0.45, 'color': '#FFFFFF'}, keys=[k(0.0, visible=False), k(YANK, visible=True), k(round(YANK + 0.45, 3), visible=False)]),   # (pass 3) small, white, gone: the grey puffs read as rocks
               P('zip11', 'zipLines', pos=[r(X10 - 0.3), 1.05, r(Z10 + 0.6)], face='camera', opts={'at': GONE, 'dur': 0.2, 'n': 6, 'len': 3.2, 'w': 0.55, 'horiz': 1})],   # (final pass) long thin streaks along his path (four short bars read as door fittings)   # (pass 3) and speed lines where he was, four frames
        tethers=[STRAND(FOOT(), HAND('mec', 'L'), until=GONE, sag=0.25, rad=0.022, taper=0.3),
                 STRAND(HAND('mec', 'R'), FAR, sag=[[0.0, 0.004], [0.4, 0.0]], rad=0.03, taper=0.0, thin=[1.2], n=14, wobble=[[0.65, 0.025, 60, 0.8]]),
                 STRAND(FOOT(), FAR, frm=GONE, sag=0.0, rad=0.03, taper=0.0, n=14)],
        cams=[FC(0.0, [r(X10 - 2.0), 1.2, r(Z10 - 2.2)], [[X10, 2.45, r(Z10 + 0.15)], [X10, 0.35, r(Z10 + 0.15)], [r(X10 - 0.45), 1.5, r(Z10 + 0.15)], [r(X10 + 0.45), 1.3, r(Z10 - 0.6)]], top=0.12, bottom=0.74),
              glide([FC(round(YANK - 0.08, 3), CAM11, [[X10, 2.4, r(Z10 + 0.15)], [X10, 0.0, r(Z10 + 0.15)], [X10, 1.0, r(Z10 - 1.5)], [X10, 2.05, r(Z10 + 1.15)], [X10, 1.4, r(Z10 + 1.35)], [r(X10 + 1.15), 1.2, r(Z10 - 1.0)], [r(X10 - 0.85), 0.9, r(Z10 + 1.0)]], top=0.12, bottom=0.74)], 0.14)])
        # (final pass) close and low in the tremble (he filled a third of the frame), then a quick pull back as the strand wins
        # (pass 3) 45 degrees in front: his face at the pull, and the yank crossing out of the frame on the left (straight on, it flew into the lens)
st.cue('sfx:stretch', 'S11', 0.3, 0.35); st.cue('sfx:boing', 'S11', YANK, 0.45); st.cue('whoosh', 'S11', round(GONE - 0.02, 3), 0.4, 0.3, 500, 3200)

# 12: brought him home in one second. Alongside him over the roofs: he flies feet first along the pink strand, stretched by the speed, tie and hair
#     streaming, deadpan; the roofs race past under him
D12 = st.dur('S12'); Y12, Z12 = 24.0, -30.0   # (pass 2) above every roof: at 17 m the camera began inside a building (0.2 s of grey)
st.shot('S12', 'parisStreet', setOpts={**STREET, 'clear': [-200, 80]}, actors=[
        act('mec', [16.0, Y12, Z12], 0, 'stand', 'unimpressed', smear=0.6, keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [0, round(-PI / 2, 4)], 'hairUp': 1.0, 'sq': [0.86, 1.24, 0.86], 'face': {'lid': 0.35}, 'bend': {'armL': [0, 2.7, 0, 1, None], 'armR': [0, -2.7, 0, 1, None]}}, toonDur=0.0),   # (pass 2) stretched by the speed, the arms trailing back over his head
            k(0.0, to=[-16.0, Y12, Z12], dur=D12, glide=True, ease='linear', face='keep')])],
        props=[CITY('city12')],
        tethers=[STRAND(FOOT(), PT([-80.0, Y12, Z12]), sag=0.0, rad=0.04, taper=0.0, n=8)],
        cams=[cam(0.0, [17.0, round(Y12 + 0.7, 3), round(Z12 + 7.4, 3)], [-15.0, round(Y12 + 0.7, 3), round(Z12 + 7.4, 3)], [17.0, round(Y12 - 0.1, 3), Z12], [-15.0, round(Y12 - 0.1, 3), Z12], lens=46)])
st.cue('whoosh', 'S12', 0.0, 0.45, 0.85, 400, 3000)

# 13: home. His living room: he falls in from above, upside down, feet first along the strand, and plants himself head first in his own sofa like a dart;
#     the cushions bounce, dust; his legs stick up, quiver, flop
D13 = st.dur('S13'); HIT13 = 0.42; FLAT13 = round(HIT13 + 0.066, 3)
DART = {'lay': [0, round(PI, 4)], 'bend': {'armL': [0, 0.12, 0, 1, None], 'armR': [0, -0.12, 0, 1, None]}}   # (pass 2) the arms trailing up along him (a stiff T read as a cross)
st.shot('S13', 'livingRoom', setOpts=LR, actors=[
        act('mec', [0.05, 6.4, -2.88], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**DART, 'face': {'lid': 0.35}}, toonDur=0.0),
            k(0.0, to=[0.05, 1.5, -2.88], dur=HIT13, glide=True, ease='in', face='keep'),   # (final pass) the feet low at the hit: squashed to half, his head stays in the cushion (it squashed in the air)
            k(FLAT13, to=[0.05, 2.34, -2.88], dur=0.09, glide=True, ease='out', face='keep'), k(round(FLAT13 + 0.09, 3), to=[0.05, 2.28, -2.88], dur=0.08, glide=True, ease='inOut', face='keep'),   # ...the body springs back up out of it
            k(HIT13, toon={**DART, 'sq': [1.55, 0.5, 1.55]}, toonDur=0.025, toonEase='out'),                                                          # the impact: flattened to half on the contact frame...
            k(round(HIT13 + 0.033, 3), toon={**DART, 'sq': [1.55, 0.5, 1.55]}, toonDur=0.03),                                                    # ...held two frames...
            k(FLAT13, toon={**DART, 'sq': [0.88, 1.18, 0.88], 'wave': {'legL': [0.12, 1.0, 0.0, 1], 'legR': [0.12, 1.0, 0.5, 1]}}, toonDur=0.06, toonEase='outBack'),   # ...re-inflated past straight, quivering
            k(round(HIT13 + 0.25, 3), toon={**DART, 'wave': {'legL': [0.06, 1.0, 1.0, 1], 'legR': [0.06, 1.0, 1.5, 1]}}, toonDur=0.12),
            k(round(HIT13 + 0.4, 3), toon={**DART, 'bend': {**DART['bend'], 'legL': [0.0, 0.85, 0, 1, None], 'legR': [0.0, 0.35, 0, 1, None], 'shinL': [0.6, 0, 0, 1, None], 'shinR': [0.5, 0, 0, 1, None]}}, toonDur=0.15, toonEase='in'),   # the legs topple to one side...
            k(round(HIT13 + 0.55, 3), toon={**DART, 'bend': {**DART['bend'], 'legL': [0.0, 0.7, 0, 1, None], 'legR': [0.0, 0.22, 0, 1, None], 'shinL': [0.7, 0, 0, 1, None], 'shinR': [0.6, 0, 0, 1, None]}}, toonDur=0.08, toonEase='out'),   # ...bounce...
            k(round(HIT13 + 0.66, 3), toon={**DART, 'bend': {**DART['bend'], 'legL': [0.0, 0.8, 0, 1, None], 'legR': [0.0, 0.3, 0, 1, None], 'shinL': [0.65, 0, 0, 1, None], 'shinR': [0.55, 0, 0, 1, None]}}, toonDur=0.1)])],   # ...and settle
        props=[P('dust13', 'dustPuff', pos=[0.05, 0.55, -2.6], scale=0.8, opts={'once': True, 'startAt': HIT13, 'period': 0.6, 'color': '#F2EAD8'}, keys=[k(0.0, visible=False), k(HIT13, visible=True)]), WINDOW('win13')],
        tethers=[STRAND(FOOT(), PT([WINP[0], r(WINP[1] + 0.06), r(WINP[2] + 0.02)]), sag=[[0.0, 0.0], [round(HIT13 + 0.05, 3), 0.0], [round(HIT13 + 0.3, 3), 0.12]], rad=0.03, taper=0.2)],   # (final pass) from the window (it dropped from the ceiling)   # (pass 2) the strand stays, going slack after the landing (it vanished)
        fx=[{'type': 'shake', 'at': HIT13, 'dur': 0.16, 'amount': 0.012}],
        cams=[FC(0.0, [0.55, 1.45, 1.0], [[0.05, 2.45, -2.88], [-1.25, 0.4, -2.75], [r(WINP[0] + 0.4), 0.9, -3.55], [0.05, 3.5, -2.88], [r(WINP[0] + 0.4), 1.6, -3.55]], top=0.08, bottom=0.74)])   # (final pass) the window in the frame
st.cue('whoosh', 'S13', 0.0, 0.35, 0.4, 600, 2400); st.cue('thud', 'S13', HIT13, 0.5)

# 14: since then he works from home. On his sofa, deadpan, the laptop on his knees, typing; the slack strand coiled on the floor from his shoe to the
#     window; a last jerk of the foot (the children again); he does not even look; a slow blink
D14 = st.dur('S14'); JERK = round(D14 - 1.05, 3)
LAP14 = {'reach': {'L': [-0.12, 0.72, -2.25, 1, 0.08], 'R': [0.12, 0.72, -2.25, 1, 0.08]}, 'hands': {'L': 'flat', 'R': 'flat'}, 'face': {'noBlink': 1}}   # (pass 3) only keyed blinks
COIL = [[0.3, 0.22, -1.95], [0.35, 0.03, -1.65], [-0.35, 0.03, -1.15], [0.1, 0.03, -0.55], [0.95, 0.03, -0.75], [1.5, 0.03, -1.45], [1.95, 0.03, -2.6], [WINP[0], r(WINP[1] + 0.06), r(WINP[2] + 0.02)]]   # (pass 2) soft loops on the floor to the window; (final pass) up to the sill of the window beside the sofa, and eased up from the floor to his shoe (it kinked square)
st.shot('S14', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[0.0, 0.75, -2.2]), k(0.0, toon=LAP14, toonDur=0.0),
            *[k(round(0.2 + 0.1 * i, 3), toon={**LAP14, 'reach': {'L': [r(-0.12 + 0.035 * (i % 2)), r(0.72 + 0.045 * (i % 2)), -2.25, 1, 0.08], 'R': [r(0.12 - 0.035 * ((i + 1) % 2)), r(0.72 + 0.045 * ((i + 1) % 2)), -2.25, 1, 0.08]},
                                                  'bend': {'neck': [round(0.05 + 0.03 * (i % 2), 3), 0, 0, 1, None]}}, toonDur=0.05) for i in range(int((JERK - 0.3) / 0.1))],   # typing (pass 2c: hands up 4.5 cm, the head nodding with them: at 1.2 cm the freeze check read a still)
            k(round(JERK - 0.6, 3), toon={**LAP14, 'sq': [1.0, 1.015, 1.0], 'face': {'lid': 1.0, 'noBlink': 1}}, toonDur=0.05), k(round(JERK - 0.48, 3), toon=LAP14, toonDur=0.07),   # (pass 2) an ordinary blink, a breath
            k(JERK, toon={**LAP14, 'reach': {'L': [-0.12, 0.88, -2.25, 1, 0.08], 'R': [0.12, 0.88, -2.25, 1, 0.08]}, 'plant': {'L': [0.35, 0.95, -1.75, 1.0]}, 'sq': [1.03, 0.97, 1.03], 'lay': [0.05, 0]}, toonDur=0.05, toonEase='out'), k(round(JERK + 0.12, 3), toon={**LAP14, 'plant': {'L': [0.35, 0.95, -1.75, 0.0]}}, toonDur=0.12, toonEase='in'),   # the jerk of the foot, his hips jostled, the face unmoved; (final pass) the hands ride up with the laptop (the fingers went through its lid)
            k(round(JERK + 0.22, 3), toon={**LAP14, 'face': {'lid': 1.0, 'noBlink': 1}}, toonDur=0.05), k(round(JERK + 0.32, 3), toon=LAP14, toonDur=0.08),   # (pass 3) the eyes open through the jerk, the blink seven frames after
            k(round(JERK + 0.55, 3), look='camera'), k(round(D14 - 0.55, 3), toon={**LAP14, 'face': {'lid': 1, 'noBlink': 1}}, toonDur=0.14), k(round(D14 - 0.33, 3), toon=LAP14, toonDur=0.16)])],   # a slow blink at us
        props=[P('lap14', 'laptop', pos=[0.0, 0.6, -2.22], ry=180, scale=1.6, opts={'text': 'VISIO'}, keys=[k(JERK, to=[0.0, 0.76, -2.2], dur=0.06, ease='out'), k(round(JERK + 0.12, 3), to=[0.0, 0.6, -2.22], dur=0.1, ease='in')]), WINDOW('win14')],   # (final pass) a real hop (5 px read as nothing), hung two frames   # (pass 2) the laptop jumps with the jerk
        tethers=[STRAND(PT(COIL[-1]), FOOT(), sag=0.0, rad=0.026, taper=0.0, via=COIL[-2::-1], ripple=[[round(JERK - 0.62, 3), 0.2, 1.6]])],   # (final pass) bigger and slower, across the frame (it was not seen)
        # (pass 3) the cord laid from the window to his shoe: the ripple runs in from the window and reaches the foot with the jerk (it ran away from him)   # (pass 2) one cord in soft loops, a ripple running down it on the jerk (three straight segments read as a pipe)
        cams=[FC(0.0, [0.65, 1.5, 0.45], [[SEAT[0], 1.9, SEAT[2]], [0.35, 0.0, -1.7], [-0.35, 0.0, -1.15], [r(SEAT[0] - 0.55), 1.0, SEAT[2]], [r(WINP[0] + 0.3), 1.0, -3.55], [r(WINP[0] + 0.3), 1.6, -3.55]], top=0.1, bottom=0.74, drift=(0.0, -0.05, -0.3))])   # (final pass) the window in the frame   # (pass 2) a little higher: the fingers on the keys, the loops; (pass 2c) a slow push in
st.cue('sfx:click', 'S14', 0.2, 0.25); st.cue('sfx:boing', 'S14', JERK, 0.25)

# (cycle 13) the key poses, measured in the engine by render3 --probe
for g_ in [('S01', round(TS + 0.1, 3), 'mec', 'step'), ('S02', round(SNAP - 0.05, 3), 'mec', 'leg_stretch'), ('S03', HOP3, 'dame', 'hop'),
           ('S05', round(STK5 + 0.3, 3), 'ouvrier', 'stuck_roller'), ('S06', 0.05, 'enfant3', 'skip'), ('S07', 0.6, 'mec', 'leg_whirl'),
           ('S09', 0.5, 'mec', 'hanging'), ('S10', round(UP10 + 0.8, 3), 'mec', 'breath'), ('S11', 0.9, 'mec', 'pull'), ('S11', round(YANK + 0.03, 3), 'mec', 'yank'),
           ('S12', round(D12 / 2, 3), 'mec', 'flight'), ('S14', round(D14 - 0.5, 3), 'mec', 'blink')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])

st.write("La gomme à mâcher", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={   # hairRest: still heads keep their hair block
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'shoes': True, 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'dame': {'preset': 'madame', 'seed': 511, 'suit': '#7A4E8C', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'ouvrier': {'preset': 'worker', 'seed': 512, 'build': {'width': 0.95, 'headWidth': 1.2}},
    # (pass 2) children who read as children: shorter, bigger heads, bright clothes (in teal tracksuits, all one height, they read as three businessmen)
    'enfant1': {'preset': 'gamin', 'seed': 513, 'suit': '#E8452C', 'pants': '#2F4F8C', 'build': {'height': 0.52, 'width': 0.8, 'headScale': 1.5}},
    'enfant2': {'preset': 'gamin', 'seed': 514, 'suit': '#F2C80F', 'pants': '#3A7D44', 'build': {'height': 0.56, 'width': 0.8, 'headScale': 1.45}},
    'enfant3': {'preset': 'gamin', 'seed': 515, 'suit': '#3FA34D', 'pants': '#C8202A', 'hat': 'beanie', 'hatColor': '#E8452C', 'build': {'height': 0.48, 'width': 0.8, 'headScale': 1.55}},
})
