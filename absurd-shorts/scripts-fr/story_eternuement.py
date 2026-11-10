#!/usr/bin/env python3
"""L'éternuement (story 38, cycle 2 of the cartoon staging): this man sneezed and blew the whole town's hair about. The weather office
measured it: two hundred kilometres an hour. Above a hundred it is a storm, and a storm must have a first name: the next one on the
list was Josiane. Since then Josiane is on red alert; when Josiane sniffs, his street is evacuated; his insurer classed him as a natural
disaster. Then the wind turbines hired him: today Josiane lights three towns. He is allergic to pollen. Spring is coming.
Cartoon rig with the cycle 2 additions (fingers, a tie and hair that the wind takes, weight shifts): rig='toon', fingers, cloth, idleShift.
Gags: three breaths that blow him up like a balloon, the blast that pins the passers-by on a hairdresser's poster, the forecaster spun like a
top by her anemometer, the badge, the crowd that bends away, the street that empties on a sniff, the stamp that drives his head into his
shoulders, the sneeze that lights three towns, the grain of pollen he squints at. Natural look."""
from story_kit import *

st = Story('eternuement', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4), ('S03', 'L01', 8), ('S04', 'L02', 0), ('S05', 'L03', 0), ('S06', 'L04', 0), ('S07', 'L05', 0), ('S08', 'L06', 0), ('S09', 'L06', 5),
         ('S10', 'L07', 0), ('S11', 'L07', 2), ('S12', 'L08', 0), ('S13', 'L08', 3), ('S14', 'L09', 0), ('S15', 'L10', 0), ('S16', 21.3, 0), ('S17', 'L11', 1), ('S18', 'L12', 0), ('S19', 'L12', 5)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}   # a camera key that glides from the previous one instead of cutting
MX, MZ = 7.0, 0.0                                   # the man, on the right-hand pavement, facing down the street (+Z)
PX, PZ = 8.3, 4.6                                   # the advertising panel across the pavement, facing him
STREET = {'clear': [-45, 30], 'eiffelX': -30}
STREET_B = {**STREET, 'eiffel': False}                # looking down the street the other way: no tower (only one hazy edge of it showed between the roofs: it read as a scratch in the sky)
PANEL = P('panel', 'adPanel', pos=[PX, 0, PZ], ry=180, opts={'w': 2.5, 'h': 3.6, 'y0': 0.45, 'textH': 0.25})   # all its text in a strip above the heads of those who get pinned on it
WALKERS = [('p1', 7.65, 1.9, 0.06), ('p2', 8.35, 2.7, 0.1), ('p3', 9.0, 3.5, 0.14)]   # who, x, z, when the blast reaches him
HIGH = {'p1': 0.12, 'p2': 0.3, 'p3': 0.18}         # how high each one is pinned on the panel (low: the poster's lines stay readable above them)
MESSY = {'hairUp': 0.85}                            # hair left on end
DUST = lambda pid, pos, at_, per=0.7, s=0.7, **kw: P(pid, 'dustPuff', pos=pos, scale=s, opts={'once': True, 'startAt': at_, 'period': per, 'color': '#F6F3EC', **kw}, keys=[k(0.0, visible=False), k(at_, visible=True)])

# 1: he stops in the street: three breaths in, each one bigger; he swells, rises on his toes, off the ground; one finger under his nose
SNZ = {'hold': 0.5, 'fold': 0.6, 'chin': 1.3}       # the sneeze seen from the front: the face stays on us
SNAP = 0.1                                          # the release, at the end of the shot of the breaths: the head whips at us, then we cut behind him
D1 = st.dur('S01')
T01 = [0.0, 0.42, 0.76]                              # three breaths, each sooner than the last (a ratchet: what a breath gains stays); the top is held, trembling, till the release
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0, MZ], 0, 'stand', 'worried', keys=[k(0.0, clip='sneezeUp', params={'times': T01, 'last': 0.3, 'tremble': 2.0, 'float': 0.62, 'ik': 1}, blend=0.08),
            k(D1 - SNAP, clip='sneeze', params=SNZ, blend=0.03)])],
        cams=[cam(0.0, [MX - 1.15, 2.3, 3.7], [MX - 1.12, 2.35, 3.6], [MX, 1.85, MZ], [MX, 1.95, MZ], lens=44),
              glide([cam(0.46, [MX - 1.5, 1.5, 5.8], [MX - 1.5, 1.5, 5.8], [MX, 1.38, MZ], [MX, 1.38, MZ], lens=44)], 0.5)])
# 2: the sneeze, from behind him: the blast takes the passers-by off their feet and pins them on the hairdresser's poster; he is shot backward past us
B2 = 0.0
def walker(w, x, z, d, hit):
    return act(w, [x, 0, z + 0.3], 180, 'walk', 'neutral', keys=[k(0.0, to=[x, 0, z], dur=d, clip='walk', ease='linear'), k(d, clip='blownBack', blend=0.04),
        k(d + 0.02, to=[x, 0.0, PZ - 0.16], dur=hit - d - 0.02, glide=True, ease='in', face='keep'), k(hit, clip='poster', params={'high': HIGH[w], 'slideAt': 9.0, 'stars': 1}, blend=0.02, toon=MESSY, toonDur=0.05)])
HITS = {'p1': 0.3, 'p2': 0.36, 'p3': 0.42}
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0.3, MZ], 0, 'stand', 'worried', keys=[k(-SNAP, clip='sneeze', params=SNZ, blend=0.001),
        k(B2 + 0.03, to=[MX - 1.3, 0.6, MZ - 6.0], dur=0.22, glide=True, ease='out', face='keep')])] + [walker(w, x, z, d, HITS[w]) for w, x, z, d in WALKERS],
        props=[PANEL, P('blast', 'sneezeBlast', pos=[MX, 0.2, MZ + 0.4], opts={'at': B2, 'dur': 0.42, 'len': 4.6, 'spread': 1.6})],
        fx=[{'type': 'wind', 'at': B2, 'dur': 0.42, 'v': [0, 0, 30], 'attack': 0.03, 'release': 0.3}, {'type': 'shake', 'at': B2, 'dur': 0.3, 'amount': 0.05}] + [{'type': 'shake', 'at': t, 'dur': 0.1, 'amount': 0.02} for t in HITS.values()],
        cams=[cam(0.0, [MX + 0.7, 2.0, -3.2], [MX + 0.75, 1.95, -2.9], [8.0, 1.3, 3.0], [8.05, 1.35, 3.4], lens=58), glide([cam(0.4, [8.15, 1.75, -1.2], [8.2, 1.75, -1.4], [PX, 2.05, PZ], [PX, 2.05, PZ], lens=50)], 0.3)])
# 3: the hairdresser's poster, and three more: pinned flat, hair on end; one peels off and slides down, then another
SLIDE = {'p2': 0.22, 'p1': 0.5}
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act(w, [x, 0, PZ - 0.16], 180, 'stand', 'dizzy',
        keys=[k(-0.05, clip='poster', params={'high': HIGH[w], 'slideAt': SLIDE.get(w, 9.0) + 0.05, 'slide': 0.5, 'peelK': 3.0, 'stars': 1}, blend=0.001, toon=MESSY, toonDur=0)]) for w, x, z, d in WALKERS],
        props=[PANEL], cams=[cam(0.0, [PX + 0.2, 1.8, PZ - 6.5], [PX + 0.15, 1.8, PZ - 6.1], [PX, 2.2, PZ], [PX, 2.15, PZ], lens=44)])
# ---- the weather office (the town-hall set with its own banner): everybody's hair stays on end from now on
WALL, BAND = '#9DBBE0', '#A98B6B'                    # a blue wall: under the warm light of the room it comes out a pale blue-grey (measured: hue 215, 10 % saturated); a cream one came out the colour of the skins, and a pale blue one a warm grey
OFFICE = lambda bx, **kw: {'title': 'MÉTÉO', 'map': False, 'plate': False, 'bannerX': bx, 'bannerY': 2.95, 'flagX': 4.3, 'clockX': 4.6, 'wall': WALL, 'band': BAND, **kw}
FX, FZ = -1.7, 0.1                                  # the forecaster, left of the desk
# 4: the forecaster holds up her anemometer: the gust arrives, the cups blur, and it is she who turns: three turns, like a top
G4 = 0.22
st.shot('S04', 'mairie', setOpts=OFFICE(FX - 0.3, bannerY=3.58), actors=[act('meteo', [FX, 0, FZ], 0, 'raiseOverhead', 'proud', keys=[k(0.0, look=[FX - 0.4, 2.9, 0.6]), k(G4, look=None, expr='surprised'),
        k(G4 + 0.06, clip='spinTop', params={'turns': [[0, 0], [0.2, 5], [0.575, 5], [0.825, 0]]}, blend=0.06, toon=MESSY, toonDur=0.15), k(G4 + 0.95, expr='dizzy')])],
        props=[P('anemo', 'anemometer', on={'actor': 'meteo', 'hand': 'R', 'offset': [0, -0.1, 0], 'rot': [3.1416, 0, 0]}, opts={'spin': [[0, 0.7], [G4, 0.9], [G4 + 0.08, 15], [G4 + 0.7, 15], [G4 + 1.0, 2]], 'cups': '#F2C230', 'blur': '#F2D25A'}),   # yellow cups: red ones vanished on the red end of the banner
               P('gust', 'sneezeBlast', pos=[FX - 3.6, 0.35, FZ - 0.5], ry=90, opts={'at': G4 - 0.05, 'dur': 0.75, 'len': 7.5, 'spread': 1.7, 'n': 30, 'puff': 0.45}),
               P('pp1', 'flyingPaper', pos=[FX - 2.8, 1.2, FZ + 0.7], keys=[k(0.0, visible=False), k(G4, visible=True), k(G4, to=[FX + 2.8, 2.3, FZ + 0.9], dur=0.5, arc=0.5, ease='linear')]),
               P('pp2', 'flyingPaper', pos=[FX - 2.8, 2.2, FZ - 0.9], keys=[k(0.0, visible=False), k(G4 + 0.15, visible=True), k(G4 + 0.15, to=[FX + 2.8, 1.5, FZ - 0.7], dur=0.55, arc=0.4, ease='linear')])],
        fx=[{'type': 'wind', 'at': G4, 'dur': 0.7, 'v': [16, 0, 0], 'attack': 0.05, 'release': 0.3}, {'type': 'shake', 'at': G4, 'dur': 0.25, 'amount': 0.02}],
        cams=[cam(0.0, [FX - 0.4, 1.75, 4.7], [FX - 0.35, 1.75, 4.4], [FX, 1.6, FZ], [FX, 1.6, FZ], lens=44)])
# 5: the gauge: the needle slams against the stop; dizzy, hair on end, she reads it out
st.shot('S05', 'mairie', setOpts=OFFICE(FX - 0.3, bannerY=3.58), actors=[act('meteo', [FX, 0, FZ], 0, 'stand', 'dizzy', keys=[k(0.0, toon=MESSY, toonDur=0), k(-0.05, clip='jelly', params={'amp': 0.12, 'freq': 9, 'decay': 1.5}, blend=0.001)] + st.talk('L03', 'S05', 'dizzy'))],
        props=[P('anemo', 'anemometer', on={'actor': 'meteo', 'hand': 'R', 'offset': [0, -0.1, 0], 'rot': [3.1416, 0, 0]}, opts={'spin': [[0, 2.5], [1.2, 0.3]], 'cups': '#F2C230', 'blur': '#F2D25A'}),
               P('gauge', 'windGauge', pos=[FX + 0.66, 2.3, FZ + 0.25], rot=[0.03, -0.1, 0.04], scale=0.01, opts={'at': 0.14, 'value': 200, 'r': 0.31}, keys=[k(0.02, scale=1.0, dur=0.16, ease='outBack')])],
        fx=[{'type': 'shake', 'at': 0.14, 'dur': 0.2, 'amount': 0.018}],
        cams=[cam(0.0, [FX + 0.5, 1.95, 3.5], [FX + 0.47, 1.97, 3.3], [FX + 0.32, 2.0, FZ], [FX + 0.32, 2.0, FZ], lens=44)])
# 6: the rule: above a hundred, it is a storm. The chief shows the scale; his finger pushes the rider up to the red band
BX = 1.6                                            # the boards on the back wall, right of the desk: the floor under the chief stays in the frame
CX, CZ = 2.6, -1.9                                  # the chief beside them, close to the wall
BY, LY = 2.25, 2.3                                  # the middle of the scale and of the list: high on the wall (the knob of the rolled list is out of his reach: he hops for it; hanging from it, his feet are half a metre off the floor)
LOOK6 = lambda y: [CX - 0.75, y, CZ + 1.3]         # a look toward the boards that keeps his face three quarters to us (a look at the board itself, behind him, showed the blank side of his head)
OFF6 = OFFICE(-3.0)                                 # the banner stays out of these frames
T6 = st.at('S06', 'L04', 5)                        # « tempête »
M6 = st.at('S06', 'L04', 2)                        # « cent »: the rider goes up to VENT first
RY = lambda i: round(BY + 1.6 * (0.5 - (0.17 + i * 0.275 + 0.125)), 3)   # the rider's height on band i (0: TEMPÊTE, 2: BRISE)
FING = lambda y, z=-2.5: {'R': [BX + 0.53, y, z, 1, 0.16]}                 # his fingertip under the rider (a guided hand: toon channel `reach`)
PT = lambda y, z=-2.5, **kw: {**MESSY, 'hands': {'R': 'point'}, 'reach': FING(y, z), **kw}
WAIT6 = lambda y: [CX + 0.34, y, CZ + 0.42, 1, 0.16, [1, -0.6, 0.2]]   # his other index, beside his face (further out it sat on the edge of the frame, the forearm cut)
LISTW, LISTH = 1.2, 1.9
ROLLED = P('list', 'nameList', pos=[BX, LY, -2.5], opts={'at': 9, 'w': LISTW, 'h': LISTH, 'unroll': [9, 0.27]})   # the roller list above the scale, rolled up: its knob hangs there from the start
st.shot('S06', 'mairie', setOpts=OFF6, actors=[act('chef', [CX, 0, CZ], 10, 'stand', 'determined', keys=[k(0.0, toon=PT(RY(2) - 0.07), toonDur=0),
        k(0.08, toon=PT(RY(2) - 0.12, -2.3), toonDur=0.06), k(0.15, toon=PT(RY(2) - 0.07), toonDur=0.04), k(0.24, toon=PT(RY(2) - 0.12, -2.3), toonDur=0.06), k(0.31, toon=PT(RY(2) - 0.07), toonDur=0.04),   # two taps under the rider
        k(M6 - 0.16, look=LOOK6(RY(1))), k(M6 + 0.1, look=None, expr='proud'),   # a look at the rider as it goes, then back to us: he presents to the camera
        k(M6 - 0.05, toon=PT(RY(1) - 0.07), toonDur=0.2, toonEase='out'),
        k(M6 + 0.26, toon=PT(RY(1) - 0.07, hands={'R': 'point', 'L': 'point'}, reach={**FING(RY(1) - 0.07), 'L': WAIT6(2.34)}, scl={'handL': [1.35, 1.35, 1.35]}, sq=[0.98, 1.03, 0.98]), toonDur=0.14, toonEase='outBack'),   # « attendez » : the other index goes up, to us
        k(M6 + 0.52, toon=PT(RY(1) - 0.07, hands={'R': 'point', 'L': 'point'}, reach={**FING(RY(1) - 0.07), 'L': WAIT6(2.43)}, scl={'handL': [1.35, 1.35, 1.35]}), toonDur=0.08), k(M6 + 0.62, toon=PT(RY(1) - 0.07), toonDur=0.14),
        k(T6 - 0.3, look=LOOK6(RY(0) + 0.2), expr='determined'),
        k(T6 - 0.26, toon=PT(RY(1) - 0.13, sq=[1.05, 0.93, 1.05]), toonDur=0.12), k(T6 - 0.12, toon=PT(RY(0) - 0.07, sq=[0.95, 1.1, 0.95]), toonDur=0.22, toonEase='out'),   # a dip, then up on his toes to the red band
        k(T6 + 0.06, look=None, expr='proud'), k(T6 + 0.14, toon=PT(RY(0) - 0.07), toonDur=0.15), k(T6 + 0.3, clip='handsOnHips', expr='proud', face=10, blend=0.2, look=None), k(T6 + 0.3, toon=MESSY, toonDur=0.18)])],
        props=[P('scale', 'windScale', pos=[BX, BY, -2.575], opts={'at': T6 - 0.12, 'midAt': M6 - 0.05, 'w': 1.15, 'h': 1.6, 'side': 1}), ROLLED],
        cams=[cam(0.0, [BX + 2.0, 1.95, 1.6], [BX + 1.95, 1.97, 1.35], [BX + 0.45, 2.05, -2.3], [BX + 0.43, 2.07, -2.3], lens=44)])   # three quarters from his side: a medium shot, cut at the knees; the next shot opens out to the floor
# 7: and a storm has a first name: the knob of the list is out of reach: he hops for it and comes down with the list on his weight; it snaps back up like a
#    blind and takes him with it: he flies up after his arm, hangs from the knob with his legs swinging, and his weight brings the list down again
T7 = st.at('S07', 'L05', 6)
P7 = round(T7 - 0.42, 3)                            # he pulls the cord
PULL = 0.27                                         # the list comes down in eight frames
KX, KZ = BX + LISTW * 0.36, -2.44                   # the knob of the cord
KY = lambda k_: round(LY + LISTH / 2 - LISTH * k_ - 0.16, 3)   # its height when the list is unrolled by k_ (0..1)
GRAB = lambda y, hand='grip', **kw: {**MESSY, 'hands': {'R': hand}, 'reach': {'R': [KX, y, KZ, 1, 0.1]}, **kw}
UP7 = round(P7 + PULL + 0.1, 3)                     # the topper: the list snaps back up like a blind, his hand still on the knob
SNAP7, HANG7, DOWN7, K7 = 0.08, 0.34, 0.2, 0.06     # up to the top in two frames; he flies up after his arm, drops and hangs (ten frames in all); then his weight brings it down again
ROLL7 = [[UP7, 1.0], [UP7 + SNAP7, K7], [UP7 + HANG7, K7], [UP7 + HANG7 + DOWN7, 1.0]]
END7 = round(UP7 + HANG7 + DOWN7, 3)
C7 = [KX + 0.5, 0, KZ + 0.42]                       # where he stands to pull: right of the knob, so that his arm shows beside his head
HOP7, H7 = 0.45, 0.52                               # how high he hops for the knob; how high his feet hang when the list has snapped up
SW7 = lambda a_: {'legL': [a_, 0, 0, 1.05, None], 'legR': [-0.8 * a_, 0, 0, 1.05, None]}   # his legs swing
UP = lambda y: [C7[0], y, C7[2]]
st.shot('S07', 'mairie', setOpts=OFF6, actors=[act('chef', [CX, 0, CZ + 0.1], 10, 'handsOnHips', 'proud', keys=[k(0.0, toon=MESSY, toonDur=0), k(0.12, clip='thinkChin', expr='hmm', blend=0.16, look=[CX + 0.6, 2.6, 2.5]),
        k(P7 - 0.56, clip='pokeUp', expr='surprised', blend=0.1, look=None), k(P7 - 0.56, toon={**MESSY, 'sq': [0.94, 1.1, 0.94], 'hands': {'R': 'point'}}, toonDur=0.08, toonEase='outBack'), k(P7 - 0.42, toon={**MESSY, 'hands': {'R': 'point'}}, toonDur=0.1),
        k(P7 - 0.4, to=C7, dur=0.18, glide=True, ease='inOut', face=-25), k(P7 - 0.4, clip='stand', expr='determined', blend=0.12, look=[C7[0] - 1.0, 3.2, C7[2] + 1.0]),   # one step to the board, the eyes on the knob first
        k(P7 - 0.24, toon={**MESSY, 'sq': [1.1, 0.84, 1.1], 'hands': {'R': 'open'}}, toonDur=0.1, toonEase='out'),   # he crouches: the knob is too high
        k(P7 - 0.13, to=UP(HOP7), dur=0.11, glide=True, ease='out', face='keep'), k(P7 - 0.13, toon=GRAB(KY(0.015), 'open', sq=[0.93, 1.14, 0.93]), toonDur=0.1, toonEase='out'),   # and hops for it, stretched
        k(P7 - 0.02, toon=GRAB(KY(0.015)), toonDur=0.02), k(P7 - 0.02, look=None, expr='proud'),   # got it: his face to us, like a showman
        k(P7, to=UP(0), dur=0.15, glide=True, ease='in', face='keep'), k(P7, toon=GRAB(KY(1.0)), toonDur=PULL, toonEase='inOut'),   # he comes down and the list with him: one key for the hand, the same curve as the list (a second key on the way took the fist off the knob)
        k(P7 + PULL, toon=GRAB(KY(1.0), sq=[1.1, 0.85, 1.1]), toonDur=0.05), k(P7 + PULL + 0.05, toon=GRAB(KY(1.0)), toonDur=0.08, toonEase='outBack'),   # at the bottom he is squashed, comes back
        k(UP7, toon=GRAB(KY(K7), sq=[0.92, 1.15, 0.92]), toonDur=SNAP7, toonEase='inOut'), k(UP7, expr='take'),   # the arm goes first, as long as it takes (one frame with his feet still on the floor)
        k(UP7 + 0.03, to=UP(H7 + 0.14), dur=0.1, glide=True, ease='out', face='keep'),   # the body flies up after it, a little too high (his head stays in the frame)
        k(UP7 + 0.08, toon=GRAB(KY(K7), sq=[1.12, 0.84, 1.12], bend=SW7(-0.5)), toonDur=0.05),   # squashed at the top, knees up
        k(UP7 + 0.14, to=UP(H7), dur=0.08, glide=True, ease='in', face='keep'), k(UP7 + 0.2, toon=GRAB(KY(K7), sq=[0.93, 1.13, 0.93], bend=SW7(0.5)), toonDur=0.05),   # he drops: the arm takes his weight, the legs swing out
        k(UP7 + 0.24, expr='deadpan'), k(UP7 + 0.26, toon=GRAB(KY(K7), bend=SW7(-0.3)), toonDur=0.08),   # he hangs, a look at us; the legs swing back
        k(UP7 + HANG7, toon=GRAB(KY(1.0), sq=[1.05, 0.92, 1.05], bend=SW7(0.15)), toonDur=DOWN7, toonEase='inOut'), k(UP7 + HANG7, to=UP(0), dur=DOWN7 - 0.03, glide=True, ease='inOut', face='keep'), k(UP7 + HANG7, expr='worried'),
        k(END7 - 0.04, toon=GRAB(KY(1.0), sq=[1.12, 0.82, 1.12]), toonDur=0.04), k(END7 + 0.03, toon=GRAB(KY(1.0)), toonDur=0.1, toonEase='outBack'), k(END7 + 0.03, expr='proud')])],   # he lands flat-footed, squashed, and holds the list down
        props=[P('scale', 'windScale', pos=[BX, BY, -2.575], opts={'at': -1, 'w': 1.15, 'h': 1.6, 'side': 1}),
               P('list', 'nameList', pos=[BX, LY, -2.5], opts={'at': 9, 'w': LISTW, 'h': LISTH, 'unroll': [P7, PULL], 'roll': ROLL7})],
        fx=[{'type': 'shake', 'at': P7 + PULL, 'dur': 0.12, 'amount': 0.014}, {'type': 'shake', 'at': END7, 'dur': 0.1, 'amount': 0.014}],
        cams=[cam(0.0, [BX + 0.85, 1.5, 3.8], [BX + 0.8, 1.5, 3.6], [BX + 0.6, 1.45, -2.2], [BX + 0.57, 1.46, -2.2], lens=44)])   # aimed low: the air under his hanging feet sits above the captions
# 8: the next one on the list: his finger goes down the struck names
T8 = st.dur('S08')
NY = lambda i: round(LY + LISTH / 2 - (0.2 + i * 0.076) * LISTH, 3)   # the height of name i on the list (9: JOSIANE)
st.shot('S08', 'mairie', setOpts=OFF6, props=[P('list', 'nameList', pos=[BX, LY, -2.52], opts={'at': T8 - 0.22, 'w': LISTW, 'h': LISTH, 'unroll': [-5, PULL]}),
        P('hand', 'pointerHand', pos=[BX + 0.3, NY(0) + 0.05, -2.42], keys=[k(0.05, to=[BX + 0.3, NY(8), -2.42], dur=T8 - 0.4, ease='inOut'), k(T8 - 0.3, to=[BX + 0.36, NY(9), -2.42], dur=0.12, ease='out')])],
        cams=[cam(0.0, [BX + 0.08, LY + 0.15, 0.35], [BX + 0.06, LY - 0.25, 0.15], [BX, LY + 0.25, -2.5], [BX, LY - 0.45, -2.5], lens=44)])
# 9: Josiane. The badge on his chest; he looks at it, then at us
B9 = 0.3
st.shot('S09', 'mairie', setOpts=OFFICE(4.6), actors=[act('mec', [0.2, 0, 0.3], 0, 'stand', 'worried', keys=[k(B9, clip='jelly', params={'amp': 0.2}, expr='surprised', blend=0.03), k(B9 + 0.25, look=[0.2, 1.3, 0.8], expr='lookDown'), k(B9 + 0.55, look=None, expr='deadpan')]),
        act('chef', [1.6, 0, 0.55], -75, 'stand', 'proud', keys=[k(0.0, toon=MESSY, toonDur=0), k(B9 - 0.14, toon={**MESSY, 'hands': {'L': 'open'}, 'reach': {'L': [0.3, 1.52, 0.52, 1, 0.1]}}, toonDur=0.13, toonEase='in'),
            k(B9 + 0.06, toon=MESSY, toonDur=0.12)])],   # only the chief's arm comes into the frame, long, for the slap, and goes: the frame is the hero's
        props=[P('badge', 'nameBadge', pos=[1.7, 1.5, 0.75], rot=[0, -1.2, 0], scale=1.0, keys=[k(B9 - 0.12, to=[0.14, 1.52, 0.46], dur=0.12, ease='in'), k(B9 - 0.12, rotTo=[0, 0, -0.06], dur=0.12), k(B9, attach='mec', joint='torso', offset=[-0.06, 0.47, 0.19], rot=[0, 0, -0.06])])],
        fx=[{'type': 'shake', 'at': B9, 'dur': 0.15, 'amount': 0.02}],
        cams=[cam(0.0, [0.5, 1.7, 3.3], [0.45, 1.72, 2.9], [0.3, 1.7, 0.3], [0.28, 1.75, 0.3], lens=44)])
# 10: the weather report: the storm on the map has his name; the forecaster, hair on end, reaches up: her arm goes out like a telescopic pointer to tap it
MAPX, MAPY, MAPW, MAPH = 0.8, 3.05, 1.2, 1.75
TAG = [MAPX + 0.02 * MAPW - 0.31 * MAPW - 0.06, MAPY - 0.3 * MAPH, -2.44]   # just left of the storm's name tag (stormMap with bandTop: 0.3 h under the middle): her finger lands beside the name
ARM10 = lambda pt, **kw: {**MESSY, 'hands': {'L': 'point'}, 'reach': {'L': [pt[0], pt[1], pt[2], 1, 0.16, [0.5, -1, 0.2]]}, 'scl': {'handL': [1.5, 1.5, 1.5]}, **kw}
BACK10 = lambda d: [round(TAG[0] - 0.55 * d, 3), round(TAG[1] - 0.42 * d, 3), round(TAG[2] + 0.5 * d, 3)]   # the fingertip pulled back d metres along the arm
TAP10 = 0.36
TAPS10 = [TAP10, TAP10 + 0.34, TAP10 + 0.6]
W10 = lambda a: {'armL': [a, 0, 0, 1, None], 'foreL': [-a * 1.3, 0, 0, 1, None]}   # a wobble that runs down the arm
st.shot('S10', 'mairie', setOpts=OFFICE(4.6), actors=[act('meteo', [-0.95, 0, -1.3], 12, 'stand', 'happy', keys=[k(0.0, toon=MESSY, toonDur=0),
        k(0.08, toon={**MESSY, 'hands': {'L': 'point'}, 'reach': {'L': [-0.45, 1.95, -1.75, 1, 0.16, [0.5, -1, 0.2]]}, 'sq': [1.04, 0.94, 1.04]}, toonDur=0.12), k(0.1, expr='proud'),   # the arm comes up, short: an ordinary arm
        k(0.26, toon=ARM10([TAG[0] + 0.12, TAG[1] + 0.1, TAG[2] - 0.02], sq=[0.97, 1.05, 0.97]), toonDur=0.1, toonEase='outBack'),   # then it shoots up the diagonal, too far (the map takes it), and settles beside the name
        k(TAP10 + 0.02, toon=ARM10(TAG, bend=W10(0.3)), toonDur=0.05), k(TAP10 + 0.08, toon=ARM10(TAG, bend=W10(-0.2)), toonDur=0.06), k(TAP10 + 0.15, toon=ARM10(TAG, bend=W10(0.1)), toonDur=0.06), k(TAP10 + 0.22, toon=ARM10(TAG), toonDur=0.06),
        k(TAPS10[1] - 0.1, toon=ARM10(BACK10(0.3)), toonDur=0.08), k(TAPS10[1] - 0.02, toon=ARM10(TAG), toonDur=0.04), k(TAPS10[1] + 0.04, toon=ARM10(TAG, bend=W10(0.18)), toonDur=0.05), k(TAPS10[1] + 0.1, toon=ARM10(TAG), toonDur=0.06),
        k(TAPS10[2] - 0.1, toon=ARM10(BACK10(0.3)), toonDur=0.08), k(TAPS10[2] - 0.02, toon=ARM10(TAG), toonDur=0.04), k(TAPS10[2] + 0.04, toon=ARM10(TAG, bend=W10(0.18), face={'lid': 1}), toonDur=0.05), k(TAPS10[2] + 0.1, toon=ARM10(TAG), toonDur=0.06)])],
        props=[P('map', 'stormMap', pos=[MAPX, MAPY, -2.5], opts={'w': MAPW, 'h': MAPH, 'bandTop': True, 'tapAt': TAPS10, 'tapAmp': 0.09})],
        fx=[{'type': 'shake', 'at': TAP10, 'dur': 0.1, 'amount': 0.014}],
        cams=[cam(0.0, [-0.4, 1.7, 4.7], [-0.38, 1.75, 4.4], [-0.05, 2.3, -2.0], [-0.03, 2.33, -2.0], lens=44)])
# 11: red alert: he walks down the street, a beacon turning on his head; the passers-by bend away from him one after the other, like wheat
SIDE11 = [('p1', MX - 0.56, 1.2, 1), ('p2', MX + 0.8, 0.2, -1), ('p3', MX - 0.56, -0.8, 1)]   # who, x, z, which way he bends (away from the middle)
V11 = 2.3                                           # his speed (m/s)
Z11 = -2.0                                          # where he starts
BEACON = P('beacon', 'beacon', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.565, 0], 'rot': [0, 0, 0]}, opts={'r': 0.13, 'beams': 1.9, 'beamOpacity': 0.26, 'beamWidth': 0.11, 'beamTilt': 0.38})   # on top of his skull, clear of the hair: his eyes stay free; two beams sweep the street
BADGE = P('badge', 'nameBadge', on={'actor': 'mec', 'joint': 'torso', 'offset': [-0.06, 0.47, 0.19], 'rot': [0, 0, -0.06]})
st.shot('S11', 'parisStreet', setOpts=STREET_B, actors=[act('mec', [MX, 0, Z11], 0, 'walk', 'worried', keys=[k(0.0, to=[MX, 0, Z11 + V11 * st.dur('S11')], dur=st.dur('S11'), clip='walk', ease='linear'),
            k(0.35, look=[MX - 2, 1.8, 3.0]), k(0.75, look=[MX + 2, 1.8, 4.0]), k(1.1, look=None)])] +   # he looks at those who shrink from him, one side then the other
        [act(w, [x, 0, z], 15 * sd, 'stand', 'neutral', keys=[k(0.0, toon=MESSY, toonDur=0), k(round((z - Z11 - 0.9) / V11, 3), clip='leanAway', params={'side': -sd, 'ph': i}, expr='scared', toon=MESSY, toonDur=0.05)]) for i, (w, x, z, sd) in enumerate(SIDE11)],   # they face us, he comes up behind them: they bend outward without looking
        props=[BEACON, BADGE],
        cams=[cam(0.0, [MX + 0.2, 1.8, 3.6], [MX + 0.15, 1.8, 5.0], [MX, 1.45, 0.0], [MX, 1.5, 0.3], lens=44, ease='linear')])
# 12: when Josiane sniffs: close on him, three quarters: the nose goes up, twice. Behind his shoulder three heads in a row: at the first sniff they glance at him,
#     look away, and at the second their heads whip back, eyes out on stalks (a double take, three times, staggered)
HZ = 1.6                                            # where he stands for the sniff and the evacuation
P12 = [('p1', MX + 0.72, 0.5), ('p2', MX + 1.35, -0.1), ('p3', MX + 1.95, -0.7)]   # the three passers-by, in a row behind his left shoulder
AWAY12 = [MX + 5.0, 1.6, 9.0]                       # where they were looking
GO12 = st.dur('S12') - 0.13                         # their legs start to spin: it carries over the cut
LEAN12 = {'bend': {'spine': [0, 0.2, 0, 1, None], 'neck': [0, 0.18, 0, 1.25, None]}}   # they lean toward him, necks out
st.shot('S12', 'parisStreet', setOpts=STREET_B, actors=[act('mec', [MX, 0, HZ], 0, 'stand', 'worried', keys=[k(0.03, clip='sniff', params={'n': 1, 'ik': 1}, blend=0.06), k(0.45, clip='sniff', params={'n': 1, 'ik': 1, 'held': 1}, blend=0.03)])] +
        [act(w, [x, 0, z], 0, 'stand', 'neutral', keys=[k(0.0, toon=MESSY, toonDur=0), k(0.0, look=AWAY12), k(0.1, look='mec', expr='hmm'), k(0.13, toon={**MESSY, **LEAN12}, toonDur=0.08, toonEase='outBack'),
            k(0.33, look=AWAY12, expr='neutral'), k(0.33, toon=MESSY, toonDur=0.08),
            k(0.6 + 0.05 * i, look='mec', clip='startle', expr='scared', blend=0.05), k(0.6 + 0.05 * i, toon={**MESSY, **LEAN12, 'face': {'pop': 0.5, 'popLen': 0.08, 'eyeScale': 1.2}}, toonDur=0.07, toonEase='outBack'),
            k(GO12 + 0.03 * i, clip='scramble', params={'dur': 0.36, 'expr': 'scared'}, blend=0.04)]) for i, (w, x, z) in enumerate(P12)],
        props=[BEACON, BADGE],
        cams=[cam(0.0, [MX - 0.5, 1.95, 5.0], [MX - 0.48, 1.95, 4.8], [MX + 0.7, 1.9, 0.5], [MX + 0.7, 1.9, 0.5], lens=44)])
# 13: the street is evacuated: their legs spin on the spot, then they are gone, each his own way (a wig stays in the air where a head was, then drops); sandbags
#     pop up round him; he watches each one go, blinks at us, and sniffs once more
RUN13 = [('p1', [MX - 9, 0, -1.5], 0.0, -100), ('p2', [MX + 2.5, 0, -15.0], 0.07, 170), ('p3', [MX + 9, 0, 0.5], 0.14, 95)]   # who, where to, when, the way he turns
SPIN13 = 0.2                                        # the legs spin that long in this shot (they started 0.13 s before the cut)
st.shot('S13', 'parisStreet', setOpts=STREET_B, actors=[act('mec', [MX, 0, HZ], 0, 'stand', 'worried', keys=[k(-0.5, clip='sniff', params={'n': 2, 'ik': 1}, blend=0.001), k(0.0, toon={'hands': {'R': 'point'}}, toonDur=0),
            k(0.24, look=[MX - 6, 1.6, 0.0]), k(0.4, look=[MX + 2.5, 1.6, -9.0]), k(0.56, look=[MX + 6, 1.6, 1.5]), k(0.8, look=None, expr='deadpan'), k(0.82, toon={'hands': {'R': 'point'}, 'face': {'lid': 1}}, toonDur=0.05),
            k(0.9, toon={'hands': {'R': 'point'}}, toonDur=0.06), k(0.96, clip='sniff', params={'n': 1, 'ik': 1}, expr='worried', blend=0.05)])] +
        [act(w, [x, 0, z], 0, 'stand', 'scared', keys=[k(0.0, toon={**MESSY, 'face': {'pop': 0.5, 'popLen': 0.08, 'eyeScale': 1.2}}, toonDur=0),
            k(-0.13 + 0.03 * i, clip='scramble', params={'dur': 0.36, 'expr': 'scared'}, blend=0.001, face=fc), k(SPIN13 + d, toon=MESSY, toonDur=0.05),
            k(SPIN13 + d, to=to, dur=0.16, clip='dashOff', ease='in', blend=0.03), k(SPIN13 + d + 0.17, visible=False)]) for i, ((w, x, z), (_, to, d, fc)) in enumerate(zip(P12, RUN13))],
        props=[BEACON, BADGE,
               P('wig', 'wig', pos=[MX + 0.72, 2.2, 0.5], keys=[k(0.0, visible=False), k(SPIN13 + 0.02, visible=True), k(SPIN13 + 0.26, to=[MX + 0.72, 0.02, 0.5], dur=0.2, ease='in')]),
               DUST('d13a', [MX + 0.3, 0.05, 0.5], SPIN13 + 0.02, 0.6, 0.8), DUST('d13b', [MX + 1.35, 0.05, -0.5], SPIN13 + 0.09, 0.6, 0.8), DUST('d13c', [MX + 2.3, 0.05, -0.6], SPIN13 + 0.16, 0.6, 0.8),
               P('bags1', 'sandbags', pos=[MX, 0, HZ - 0.8], scale=0.01, opts={'n': 4, 'rows': 2}, keys=[k(0.62, scale=1.0, dur=0.14, ease='outBack')]),
               P('bags2', 'sandbags', pos=[MX - 0.98, 0, HZ - 0.25], ry=75, scale=0.01, opts={'n': 2, 'rows': 2, 'seed': 7}, keys=[k(0.7, scale=1.0, dur=0.14, ease='outBack')]),
               P('bags3', 'sandbags', pos=[MX + 0.98, 0, HZ - 0.25], ry=-75, scale=0.01, opts={'n': 2, 'rows': 2, 'seed': 9}, keys=[k(0.78, scale=1.0, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [MX + 0.7, 3.3, 7.4], [MX + 0.7, 3.3, 7.4], [MX + 0.6, 0.8, 0.8], [MX + 0.6, 0.8, 0.8], lens=44),
              glide([cam(0.42, [MX + 0.1, 3.2, 6.2], [MX + 0.1, 3.2, 6.1], [MX, 1.0, HZ], [MX, 1.0, HZ], lens=44)], 0.36)])
# 14: his insurer: a very big stamp, raised with both feet off the floor, comes down on his head: the head is driven into his shoulders; CAT. NAT. on his
#     forehead; the certificate drops onto the wall
HIT14 = round(st.at('S14', 'L09', 3) + 0.05, 3)    # on « classé »
T14 = st.at('S14', 'L09', 4)                        # « catastrophe »
FALL14 = round(st.dur('S14') - 0.9, 3)              # he hangs, leaning, then goes over backward, stiff: the fall is staged across the frame, in a shot of its own
INSUR = {'wall': '#B7CDBE', 'band': '#6F8379', 'trim': '#4E6158', 'floor': '#A39685', 'joint': '#8C8070', 'banner': False, 'map': False, 'plate': False, 'flagX': 9, 'clockX': 9, 'deskZ': -2.05, 'deskX': -1.7, 'desk': '#6F8379', 'deskSide': '#5F7268'}   # the insurer's office: grey-green, its own sign; the desk in the same greys, away from where his head lands (its wood had the hue of the skins)
HX14, HZ14 = 0.25, 0.9                              # the hero
AX14, AZ14, ARY14 = -0.42, 0.36, 51                 # the insurer, behind his right shoulder, three quarters to us: he strikes toward us
SK = 1.6                                            # the stamp's size: its face is 0.42 * SK under the knob
# the stamp is not carried by the hand: it follows its own path (knob positions in the room) and the insurer's hand is guided to its knob. The contact is exact and
# the stamp goes where the staging wants it: up over his head, down on the hero's skull, back up along its arc, then beside the insurer's cheek
K_TOP2 = [-0.8, 3.08, 0.05]                          # during the hold the stamp goes on climbing: he stretches up after it, on his toes, and it trembles more and more
EY = lambda x, y, **kw: {'face': {'gx': x, 'gy': y}, **kw}   # the hero's eyes alone (toon face.gx / gy; - = to his right / up): his head stays on us
K_LOW, K_TOP, K_HIT, K_IN, K_REB, K_END = [-0.72, 1.4, 0.72], [-0.74, 2.5, 0.18], [HX14, 2.34 + 0.42 * SK, HZ14], [HX14, 1.92 + 0.42 * SK, HZ14], [-0.5, 3.05, 0.42], [-1.0, 1.15, 0.7]
BACK14 = [-2.3, 0, 0.3]                              # the insurer walks off to the left once he has read his stamp: the fall is the hero's alone
GR = lambda pt, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [pt[0], pt[1], pt[2], 1, 0.05]}, **kw}
UP14, W14, RB14 = 0.42, 0.07, 0.2                   # the stamp goes up in that time; the strike takes two frames; the rebound
st.shot('S14', 'mairie', setOpts=INSUR, actors=[act('mec', [HX14, 0, HZ14], -8, 'stand', 'worried', keys=[k(0.0, toon=EY(-0.8, 0.0), toonDur=0), k(0.05, expr='surprised'), k(0.05, toon=EY(-0.7, -0.9), toonDur=UP14, toonEase='out'),   # only his eyes go to the stamp and climb after it, wide
            k(0.5, expr='gulp'), k(0.5, toon=EY(-0.6, -1.0, sq=[1.05, 0.92, 1.05], bend={'neck': [0, 0, 0, 0.8, None]}), toonDur=HIT14 - 0.62, toonEase='inOut'), k(HIT14 - 0.24, expr='scared'),   # he swallows and shrinks under it, the neck goes in
            k(HIT14 - 0.02, clip='headHammer', params={'at': 0.02}, blend=0.02), k(HIT14 - 0.02, toon={}, toonDur=0.02), k(HIT14 + 0.42, expr='dizzy'), k(HIT14 + 0.42, toon={'face': {'cross': 1, 'stars': 1}}, toonDur=0.1), k(HIT14 + 0.5, clip='jelly', params={'amp': 0.1, 'freq': 5, 'decay': 0.6}, blend=0.15),
            k(FALL14, clip='plankFall', params={'dur': 0.27, 'hang': 0.17, 'feet': 0.95}, blend=0.05), k(FALL14, toon={'face': {'cross': 1, 'stars': 1}, 'auto': 0}, toonDur=0.05),
            k(FALL14 + 0.58, toon={'face': {'cross': 1, 'stars': 1}, 'auto': 0, 'bend': {'neck': [1.0, 0, 0, 1.3, None]}}, toonDur=0.12, toonEase='outBack')]),   # flat on his back, legs up, he lifts his head: the stamped face comes to us between his feet
        act('assureur', [AX14, 0, AZ14], ARY14, 'stand', 'smug', keys=[k(0.0, toon=GR(K_LOW), toonDur=0), k(0.0, look='mec'), k(0.02, clip='stampDown', params={'hit': HIT14, 'rest': 0.25}, expr='determined', blend=0.1),
            k(0.04, toon=GR(K_TOP), toonDur=UP14, toonEase='outBack'), k(0.04 + UP14, toon=GR(K_TOP2, sq=[0.92, 1.17, 0.92]), toonDur=HIT14 - W14 - 0.04 - UP14, toonEase='linear'),
            k(0.5, look=[K_TOP2[0], K_TOP2[1] + 0.5, K_TOP2[2]]), k(0.68, look='mec'), k(HIT14 - W14, toon=GR(K_HIT), toonDur=W14, toonEase='in'), k(HIT14, toon=GR(K_IN), toonDur=0.03),
            k(HIT14 + 0.1, toon=GR(K_REB), toonDur=RB14, toonEase='out'), k(HIT14 + 0.1 + RB14, toon=GR(K_END), toonDur=0.3, toonEase='inOut'),
            k(HIT14 + 0.3, clip='stand', expr='proud', blend=0.2, look=[HX14, 2.45, HZ14]),   # he reads his stamp on the forehead: the head tips to it, a nod, a second one
            k(HIT14 + 0.44, toon=GR(K_END, bend={'neck': [0.3, 0, 0, 1.12, None]}, sq=[1.03, 0.96, 1.03]), toonDur=0.07), k(HIT14 + 0.52, toon=GR(K_END), toonDur=0.07),
            k(HIT14 + 0.6, toon=GR(K_END, bend={'neck': [0.3, 0, 0, 1.12, None]}, sq=[1.03, 0.96, 1.03]), toonDur=0.07), k(HIT14 + 0.68, toon=GR(K_END), toonDur=0.07),
            k(FALL14 - 0.2, to=BACK14, dur=0.34, clip='walk', ease='in', face=-80), k(FALL14 - 0.2, toon={'hands': {'R': 'grip'}}, toonDur=0.1, look=None, expr='smug'), k(FALL14 - 0.03, visible=False)])],   # gone when the camera changes (a sliver of him stayed at the edge of the fall's frame)
        props=[P('stamp', 'bigStamp', pos=K_LOW, ry=ARY14, rot=[0, 0, 0], rotOrder='YXZ', scale=SK, keys=[k(0.04, to=K_TOP, dur=UP14, ease='outBack'), k(0.04, rotTo=[2.69, ARY14 * 0.01745, 0], dur=UP14, ease='outBack'), k(0.04 + UP14, to=K_TOP2, dur=HIT14 - W14 - 0.04 - UP14, ease='linear'), *[k(round(0.04 + UP14 + 0.06 * j, 3), rotTo=[2.69 + (0.05 + 0.025 * j) * (1 if j % 2 else -1), ARY14 * 0.01745, 0], dur=0.06, ease='inOut') for j in range(int((HIT14 - W14 - 0.04 - UP14) / 0.06))],   # it trembles at the top, more and more
                   k(HIT14 - W14, to=K_HIT, dur=W14, ease='in', arc=0.06), k(HIT14 - W14, rotTo=[6.283, ARY14 * 0.01745, 0], dur=W14, ease='in'), k(HIT14, to=K_IN, dur=0.03),
                   k(HIT14 + 0.1, to=K_REB, dur=RB14, ease='out'), k(HIT14 + 0.1, rotTo=[5.6, ARY14 * 0.01745, 0], dur=RB14, ease='out'),
                   k(HIT14 + 0.1 + RB14, to=K_END, dur=0.3, ease='inOut'), k(HIT14 + 0.1 + RB14, rotTo=[6.283, ARY14 * 0.01745, 0], dur=0.3, ease='inOut'), k(FALL14 - 0.2, to=[BACK14[0] - 0.5, 1.15, 0.6], dur=0.34, ease='in')]),   # it leaves the frame at his side; in the fall shot he has put it down
               P('mark', 'stampMark', pos=[0, 0, 0], opts={'w': 0.27, 'h': 0.15}, keys=[k(0.0, visible=False), k(HIT14 + 0.02, visible=True), k(HIT14 + 0.02, attach='mec', joint='head', offset=[0.0, 0.4, 0.089], rot=[0, 0, -0.12])]),
               P('sign', 'signBoard', pos=[0.75, 0, -2.57], opts={'text': 'ASSURANCES', 'w': 1.3, 'h': 0.36, 'height': 3.5, 'posts': False, 'frame': '#2E4A3F', 'bg': '#F4F1E8', 'fg': '#2E4A3F'}, keys=[k(FALL14 - 0.03, visible=False)]),   # not in the fall's frame (the low camera cut it in two)
               P('diploma', 'catNatDiploma', pos=[-1.1, 5.4, -2.55], opts={'w': 0.95, 'h': 0.7}, keys=[k(T14 - 0.05, to=[-1.1, 2.75, -2.55], dur=0.2, ease='outBack')])],
        fx=[{'type': 'shake', 'at': HIT14, 'dur': 0.2, 'amount': 0.035}, {'type': 'shake', 'at': T14 + 0.15, 'dur': 0.1, 'amount': 0.012}, {'type': 'shake', 'at': FALL14 + 0.44, 'dur': 0.15, 'amount': 0.02}],
        cams=[cam(0.0, [-0.15, 1.75, 5.9], [-0.15, 1.75, 5.7], [-0.1, 1.62, 0.6], [-0.1, 1.62, 0.6], lens=44),
              glide([cam(HIT14 + 0.14, [-0.05, 2.0, 4.4], [-0.05, 2.0, 4.3], [-0.02, 2.2, 0.6], [-0.02, 2.2, 0.6], lens=44)], 0.24),
              cam(FALL14 - 0.03, [2.05, 0.6, 4.1], [2.05, 0.6, 4.1], [0.3, 1.2, 0.2], [0.3, 1.2, 0.2], lens=44),   # the fall, low and close, three quarters: he stands the height of the frame,
              glide([cam(FALL14 + 0.15, [1.42, 0.48, 2.98], [1.4, 0.48, 2.94], [0.3, 0.85, -0.3], [0.3, 0.85, -0.3], lens=44)], 0.32)])   # and the camera goes down with him: the body lies across the frame, the legs come up in a V under the certificate
# ---- the wind farm. For the sneeze he faces a far corner of the field (ry 135): three turbines up there, three towns on the ridge beyond
FIELD = lambda **kw: {'clouds': 14, 'seed': 31, **kw}
TPOS = [(4.95, -6.55), (10.31, -11.67), (18.54, -17.55)]   # laid out for the camera of the second half of S17: left, middle, right, each further away
TURB = lambda keys=None, **kw: [P(f'turb{i}', 'windTurbine', pos=[x, 0, z], ry=-45, opts={'h': 9, 'rpm': 0, 'phase': i * 0.7, **({'rpmKeys': keys(i)} if keys else {}), **kw}) for i, (x, z) in enumerate(TPOS)]
MAT = lambda **kw: P('mat', 'mattressWall', pos=[-0.72, 0, 0.72], ry=-45, opts={'n': 1, 'h': 1.75, **kw})   # one mattress standing a metre behind him
# 15: hired: the engineer shakes his hand so hard that the shake runs up his arm and through him like a wave, grinning at us as for a photograph; when he
#     lets go the hero rings like a twanged ruler; a thumb up, big, between the two of them
S15E = 0.95                                         # the shaking stops
TW15 = 0.0                                          # the twist of the hand that sets the thumb upright
GRIP = [0.0, 1.42, 0.5]                             # the point their hands hold (guided hands): in front of them, toward us; both men are turned three quarters to the camera
THUMB = [0.0, 2.0, 0.45]                           # where the thumb comes up: in the gap between the two heads, against the sky, toward us (the arm passes under his face, not over it)
SHK = {'grip': GRIP, 'stopAt': S15E, 'freq': 3.6, 'amp': [0.07, 0.3]}
st.shot('S15', 'grassland', setOpts=FIELD(seed=37), actors=[act('mec', [-0.5, 0, 0.1], 55, 'stand', 'worried', keys=[k(0.0, clip='shakeHands2', params={**SHK, 'role': 'wave'}, blend=0.06), k(0.0, look='inge'), k(0.45, look=None),
            k(S15E + 0.45, clip='jelly', params={'amp': 0.07, 'freq': 2.6, 'decay': 0.4}, expr='dizzy', blend=0.2), k(S15E + 0.45, toon={'face': {'cross': 0.7, 'stars': 1}}, toonDur=0.2)]),   # he goes on swaying, eyes crossed
        act('inge', [0.5, 0, 0.1], -55, 'stand', 'bigGrin', keys=[k(0.0, clip='shakeHands2', params={**SHK, 'role': 'pump', 'two': 1, 'thumbAt': S15E + 0.08, 'thumb': THUMB, 'thumbTwist': TW15}, blend=0.06),
            k(0.0, look=[-0.3, 1.8, 4.0]),   # his head to the camera: he shakes the hand without looking at it
            k(S15E + 0.1, toon={'scl': {'handL': [1.7, 1.7, 1.7]}}, toonDur=0.15, toonEase='outBack')])],   # the thumb, big; the clip pumps it twice
        props=[P(f'turb{i}', 'windTurbine', pos=[x, 0, z], opts={'h': 9, 'rpm': 0, 'phase': i * 0.7}) for i, (x, z) in enumerate([(-4.05, -12.7), (3.3, -18.7)])] +   # one tower at each edge: the sky between the heads is clear
              [BADGE, P('fl1', 'flowers', pos=[-1.5, 0, 1.0]), P('fl2', 'flowers', pos=[1.4, 0, 1.3])],
        cams=[cam(0.0, [0.3, 1.3, 5.7], [0.25, 1.3, 5.4], [0.05, 1.86, 0.2], [0.03, 1.89, 0.2], lens=44)])   # room above the heads: the last stroke throws him a head higher
# 16: at dusk, today: the engineer, behind the hero's shoulder (behind the gun), holds a pepper pot over his head at the end of a fishing rod, in front of his
#     nose: a rhythm of its own this time: one long breath while the pot comes down, the engineer leaning away, then a short one: he ducks; the release
DUSK = {'sky': ['#33437A', '#F2A368'], 'grass': '#5E8A4E'}
D16 = st.dur('S16')
E16 = [-0.85, 0, -0.21]                             # the engineer
GX = lambda c: [-0.67, round(2.5 - c, 3), -0.2]     # the grip of the rod: he lowers it by c: the pot comes down toward the nose
ROD = lambda c, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [GX(c)[0], GX(c)[1], GX(c)[2], 1, 0.05]}, **kw}
BR = [0.0, 0.56]                                    # two breaths: a long one, a short one (sneezeUp `times`)
st.shot('S16', 'grassland', setOpts=FIELD(**DUSK), lighting='dusk', actors=[act('mec', [0, 0, 0], 135, 'stand', 'worried', keys=[k(-0.05, clip='sneezeUp', params={'times': BR, 'last': 0.3, 'tremble': 2.5, 'float': 0.25, 'ik': 1, 'back': 0.6}, blend=0.001),
            k(D16 - SNAP, clip='sneeze', params=SNZ, blend=0.03)]),
        act('inge', E16, 90, 'stand', 'bigGrin', keys=[k(0.0, toon=ROD(0.0), toonDur=0), k(0.0, look=[0.2, 2.6, -0.2]),
            k(0.08, toon=ROD(0.12, bend={'spine': [-0.24, 0, 0, 1, None]}), toonDur=0.42, toonEase='inOut'), k(0.3, expr='worried'),   # the pot comes down through the long breath; he leans away from it
            k(BR[1] - 0.02, toon=ROD(0.16, bend={'spine': [-0.3, 0, 0, 1, None]}, sq=[1.12, 0.74, 1.12], touch={'L': ['head', 0.0, 0.56, 0.04, 1, 0.1]}), toonDur=0.12, toonEase='outBack'), k(BR[1], expr='scared')])],   # the short one: he ducks, a hand on his helmet
        props=TURB() + [P('rod', 'pepperRod', pos=GX(0.0), ry=90, opts={'swing': 0.12, 'len': 1.1, 'drop': 0.1, 'pot': 1.7, 'back': False}, keys=[k(0.08, to=GX(0.12), dur=0.42, ease='inOut'), k(BR[1] - 0.02, to=GX(0.16), dur=0.12, ease='outBack')]),
               MAT(), P('turbB', 'windTurbine', pos=[-22, 0, 14], ry=120, opts={'h': 9, 'rpm': 0, 'phase': 0.4})],
        cams=[cam(0.0, [3.35, 2.3, -1.25], [3.22, 2.48, -1.2], [-0.2, 2.05, 0.05], [-0.2, 2.35, 0.05], lens=44),
              glide([cam(D16 - SNAP - 0.02, [3.22, 2.1, -1.2], [3.22, 2.1, -1.2], [-0.1, 1.15, 0.0], [-0.1, 1.15, 0.0], lens=44)], 0.07)])   # the camera whips down with his head: the open mouth ends in the middle of the frame, above the captions
# 17: the sneeze. First from the side, twenty frames for the mattress: he is shot back, seat first, into it; it bows under him and holds him four frames; it
#     springs back and throws him out, rolled in a ball, on an arc; he lands squashed and comes back up dizzy (the engineer has taken cover behind it: it
#     bumps him). Then the far corner of the field: the blast runs up to the turbines, they spin up one after the other; beside each one a town comes on at
#     once, under a warm glow: one, two, three
SN17 = 0.0
HIT17, BOW17, HOLD17, FLY17 = 0.1, 0.08, 0.12, 0.2  # he hits the mattress; it bows; it holds him; his flight out
OUT17 = round(HIT17 + BOW17 + HOLD17, 3)            # the mattress springs back: it throws him out
B17 = 0.7                                           # the cut to the turbines
IN17 = lambda d, y=-0.32: [round(-0.707 * d, 3), y, round(0.707 * d, 3)]   # d metres behind where he stood
LAND17 = [-0.25, 0, 0.25]                           # where he comes down: short of where he stood (further on, the frame cut him, squashed, in two)
E17 = [-1.41, 0, 0.73]                              # the engineer, behind the far end of the mattress: his head shows over it
UPT = lambda i: round(B17 + 0.2 + 0.15 * i, 3)      # turbine i has reached its speed: its town comes on
st.shot('S17', 'grassland', setOpts=FIELD(**DUSK), lighting='dusk', actors=[act('mec', [0, 0.3, 0], 135, 'stand', 'worried', keys=[k(-SNAP, clip='sneeze', params=SNZ, blend=0.001),
            k(SN17 + 0.03, to=IN17(0.72), dur=HIT17 - 0.03, glide=True, ease='out', face='keep'), k(SN17 + 0.03, clip='blownBack', blend=0.04),
            k(HIT17, to=IN17(1.0), dur=BOW17, glide=True, ease='out', face='keep'), k(HIT17 + 0.02, toon={'sq': [1.15, 1.0, 0.72]}, toonDur=BOW17, toonEase='out'),   # he sinks into it, pressed
            k(OUT17, to=LAND17, dur=FLY17, glide=True, ease='linear', arc=0.6, face='keep'), k(OUT17, clip='cannonball', params={'spin': 1 / FLY17, 'expr': 'dizzy'}, blend=0.03), k(OUT17, toon={'sq': [0.92, 1.12, 0.92]}, toonDur=0.05),   # thrown out, rolled in a ball: one turn
            k(OUT17 + FLY17, clip='land', expr='dizzy', blend=0.02), k(OUT17 + FLY17, toon={'sq': [1.5, 0.58, 1.0], 'face': {'stars': 1, 'cross': 1}}, toonDur=0.04),   # he lands flat-footed, squashed to half his height (wider across the shoulders, not longer: seen from the side he stays in the frame)
            k(OUT17 + FLY17 + 0.05, toon={'sq': [0.92, 1.1, 0.92], 'face': {'stars': 1, 'cross': 1}}, toonDur=0.1, toonEase='outBack'), k(OUT17 + FLY17 + 0.16, toon={'face': {'stars': 1, 'cross': 1}}, toonDur=0.1)]),
        act('inge', E17, 135, 'stand', 'scared', keys=[k(0.0, look=[0, 1.6, 0]), k(0.0, toon={'sq': [1.08, 0.86, 1.08]}, toonDur=0),
            k(HIT17 + 0.02, toon={'sq': [0.9, 1.14, 0.9], 'hat': [0.3, 0.3, 0]}, toonDur=0.06, toonEase='out'), k(HIT17 + 0.02, clip='startle', expr='surprised', blend=0.04), k(HIT17 + 0.12, toon={'sq': [1.05, 0.92, 1.05]}, toonDur=0.12, toonEase='outBack'),   # the mattress bumps him: his helmet jumps
            k(OUT17 + 0.1, toon={}, toonDur=0.1), k(OUT17 + 0.1, look='mec'), k(OUT17 + FLY17 + 0.08, look=[8, 5, -9])])],   # he watches him go by, then looks up at the turbines
        props=TURB(lambda i: [[0, 0], [UPT(i) - 0.16, 0], [UPT(i), 95], [9, 95]], blur=0.8, ghosts=3, blurSpread=4) +
              [MAT(hitAt=HIT17, dent=0.3, hold=BOW17 + HOLD17), P('blast', 'sneezeBlast', pos=[0.3, 1.7, -0.3], ry=135, opts={'at': SN17, 'dur': 0.6, 'len': 16, 'spread': 2.4, 'n': 36}),
               P('towns', 'townLights', pos=[17.88, 0, -32.49], ry=-27.2, scale=1.4, opts={'at': [UPT(0), UPT(1), UPT(2)], 'houses': 3, 'landmarks': True, 'sites': [[-3.2, 4.29], [0, 0], [4.83, -4.29]], 'pop': True, 'glow': 12, 'glowK': 0.9})],   # one town beside each turbine, as wide as the gap between two towers allows
        fx=[{'type': 'wind', 'at': SN17, 'dur': 0.5, 'v': [20, 0, -20], 'attack': 0.03, 'release': 0.3}, {'type': 'shake', 'at': SN17, 'dur': 0.3, 'amount': 0.04}, {'type': 'shake', 'at': HIT17, 'dur': 0.12, 'amount': 0.03}, {'type': 'shake', 'at': OUT17 + FLY17, 'dur': 0.12, 'amount': 0.02}],
        cams=[cam(0.0, [4.7, 1.5, 1.55], [4.6, 1.5, 1.55], [-0.12, 1.0, 0.12], [-0.12, 1.0, 0.12], lens=44),   # wide enough for the mattress and for where he lands, aimed low: the landing above the captions
              cam(B17, [-1.0, 1.5, 9.5], [-0.9, 1.55, 9.2], [8.0, 4.3, -8.0], [8.0, 4.4, -8.0], lens=50)])
# ---- spring: the same field in flower: daisies, buttercups and poppies all over the grass, tufts, trees in blossom; the turbines far away at the edges
BLOSSOM = lambda pid, x, z, sc, seed=3: P(pid, 'tree', pos=[x, 0, z], scale=sc, opts={'seed': seed, 'color': '#F2A9C4', 'color2': '#F8CBDA', 'color3': '#E98FB3'})
MEADOW = lambda **kw: P('meadow', 'flowerMeadow', pos=[0, 0, -4], opts={'w': 26, 'd': 30, 'n': 560, 'near': 0.5, 'clear': [0, 4, 0.7], 'h': 0.34, 'head': 0.075, **kw})   # the hero stands at its (0, 4)
TUFTS = P('tufts', 'tallGrass', pos=[0, 0, -4], opts={'w': 26, 'd': 30, 'h': 0.3, 'count': 360, 'thin': 0.035, 'seed': 14})
# 18: he is allergic to pollen: very close: one grain drifts down to the tip of his nose; his eyes follow it until they cross
G18 = 1.0                                           # the grain lands
NOSE = [-0.005, 1.975, 0.15]                        # on the nostrils (measured on a still: 0.13 m under the bridge, where it sat on an eye)
st.shot('S18', 'grassland', setOpts=FIELD(), actors=[act('mec', [0, 0, 0], 0, 'stand', 'worried', keys=[k(0.0, look='grain', expr='surprised'), k(0.42, look=[0.04, 1.8, 1.6]),   # the head comes back to us before the grain is close (a look at a thing 5 cm from the face twists the head away)
            k(G18 - 0.35, toon={'face': {'cross': 1}}, toonDur=0.3, toonEase='inOut'),
            k(G18 + 0.12, toon={'face': {'cross': 1}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.1), k(G18 + 0.3, toon={'face': {'cross': 1, 'lid': 0.45}}, toonDur=0.12)])],
        props=[P('grain', 'pollenGrain', pos=[0.55, 2.5, 0.9], opts={'r': 0.019}, scale=1.7, keys=[k(0.0, to=[0.16, 2.14, 0.45], dur=0.55, arc=0.06, ease='inOut'), k(0.55, to=NOSE, dur=G18 - 0.55, arc=-0.04, ease='inOut'),
                   k(G18, scale=1.3, dur=0.0), k(G18, attach='mec', joint='head', offset=[0.0, 0.17, 0.108], rot=[0, 0, 0])]),   # once landed it rides on the head: it stays on the nostrils whatever the head does
               MEADOW(), TUFTS, BLOSSOM('bt1', -2.3, -13.0, 2.3), BLOSSOM('bt2', 3.4, -19.0, 2.6, 8)],
        cams=[cam(0.0, [0.12, 2.02, 1.75], [0.1, 2.02, 1.5], [0, 2.02, 0], [0, 2.02, 0], lens=40)])
# 19: spring is coming: the field in flower, a yellow cloud that drifts to him; the breaths again, as a ratchet: each one shorter and bigger than the last, and
#     what it has gained stays: he rises like a balloon, every flower of the field leans to him a little more, everything loose flies to him; we leave on the
#     top of the biggest breath, held, trembling, before the sneeze. He faces us (a quarter turn toward the cloud): the last image keeps his face
T19 = [0.0, 0.66, 1.2, 1.64, 2.0]                   # when each breath starts, after 0.35 s: gaps of 20, 16, 13, 11 frames
PULL19 = [[0.3, 0.0]] + [x for t_, a0, a1 in zip(T19, [0.0, 0.2, 0.42, 0.66, 0.92], [0.2, 0.42, 0.66, 0.92, 1.25]) for x in ([round(0.35 + t_, 3), a0], [round(0.35 + t_ + 0.2, 3), a1])]   # how far the flowers lean to him
st.shot('S19', 'grassland', setOpts=FIELD(), actors=[act('mec', [0, 0, 0], 25, 'stand', 'scared', keys=[k(0.0, look=[6, 2, 1]), k(0.35, clip='sneezeUp', params={'times': T19, 'last': 0.36, 'tremble': 2.5, 'float': 1.3, 'ik': 1, 'back': 0.55}, blend=0.08, look=None),
            ] + [k(round(0.35 + t_ + 0.08, 3), toon={'sq': [v, round(0.82 * v + 0.18, 3), v]}, toonDur=0.2, toonEase='outBack') for t_, v in zip(T19, [1.15, 1.35, 1.58, 1.82, 2.1])])],
        props=[P(f'turb{i}', 'windTurbine', pos=[x, 0, z], opts={'h': 9, 'rpm': 0, 'phase': 0.5 + i}) for i, (x, z) in enumerate([(-14.9, -44.0), (4.5, -52.0)])] + [P('cloud', 'pollenCloud', pos=[7.5, 2.0, 0.5], opts={'n': 150, 'size': [7, 3.4, 3.5], 'dir': [-2.3, -0.05, -0.1], 'seed': 12}),
               MEADOW(toward=[0, 4], pull=PULL19), TUFTS, BLOSSOM('bt1', -2.3, -13.0, 2.3), BLOSSOM('bt2', 3.4, -19.0, 2.6, 8),
               P('pp1', 'flyingPaper', pos=[4.2, 1.2, 1.2], keys=[k(0.9, to=[1.25, 3.0, 0.6], dur=1.9, arc=0.5, ease='linear')]),   # they come with the wind, slowly, on his breath: in the frame for the last ten frames, still on their way at the cut
               P('wig', 'wig', pos=[3.6, 3.6, 0.7], keys=[k(0.6, to=[1.2, 5.45, 0.5], dur=2.25, ease='linear')])],   # the wig high in the clear sky, toward his nose
        fx=[{'type': 'wind', 'at': 0.6, 'dur': 2.2, 'v': [-6, 0, 0], 'attack': 1.2, 'release': 0.1}],
        cams=[cam(0.0, [0.7, 1.9, 4.8], [1.0, 2.6, 9.3], [0.2, 1.7, 0], [0.1, 3.5, 0], lens=44, ease='inOut')])   # the frame keeps his hair when a breath lifts it

# sound on the actions
for i_, t_ in enumerate(T01): st.cue('sfx:stretch', 'S01', t_, 0.3 + 0.05 * i_)
st.cue('thunder', 'S02', B2, 0.5); st.cue('whoosh', 'S02', B2, 0.5, 0.5, 300, 3000)
for w_, t_ in HITS.items(): st.cue('sfx:splat', 'S02', t_, 0.35)
for t_ in SLIDE.values(): st.cue('sfx:squeak', 'S03', t_, 0.35)
st.cue('whoosh', 'S04', G4, 0.4, 0.7, 400, 2500); st.cue('sfx:zip', 'S04', G4 + 0.08, 0.3)
st.cue('sfx:twang', 'S05', 0.14, 0.4); st.cue('pop', 'S05', 0.02, 0.3)
st.cue('sfx:tick', 'S06', 0.15, 0.2); st.cue('sfx:tick', 'S06', 0.31, 0.2); st.cue('sfx:slideUp', 'S06', M6 - 0.05, 0.25); st.cue('sfx:slideUp', 'S06', T6 - 0.12, 0.35); st.cue('sfx:zip', 'S07', P7, 0.3); st.cue('clack', 'S07', P7 + PULL, 0.4); st.cue('sfx:spring', 'S07', UP7, 0.4); st.cue('sfx:slideUp', 'S07', UP7 + HANG7, 0.3); st.cue('clack', 'S07', END7, 0.35); st.cue('sfx:tick', 'S08', T8 - 0.22, 0.4)
st.cue('sfx:splat', 'S09', B9, 0.4); st.cue('sfx:zip', 'S10', 0.26, 0.3); st.cue('pop', 'S10', TAP10, 0.35); st.cue('sfx:tick', 'S10', TAPS10[1], 0.28); st.cue('sfx:tick', 'S10', TAPS10[2], 0.28)
for i, (_, _, z, _) in enumerate(SIDE11): st.cue('sfx:squeak', 'S11', round((z - Z11 - 0.9) / V11, 3), 0.3)
st.cue('sfx:gasp', 'S12', 0.62, 0.35)
for _, _, d, _ in RUN13: st.cue('sfx:zip', 'S13', SPIN13 + d, 0.35)
st.cue('sfx:poof', 'S13', 0.62, 0.3); st.cue('sfx:poof', 'S13', 0.74, 0.3)
st.cue('sfx:stretch', 'S14', 0.06, 0.35); st.cue('whoosh', 'S14', HIT14 - W14, 0.3, 0.12, 500, 4000); st.cue('thud', 'S14', HIT14, 0.55); st.cue('sfx:spring', 'S14', HIT14 + 0.17, 0.4); st.cue('clack', 'S14', T14 + 0.15, 0.35)
st.cue('sfx:squeak', 'S14', FALL14 + 0.02, 0.3); st.cue('thud', 'S14', FALL14 + 0.44, 0.5)
for i_ in range(4): st.cue('sfx:squeak', 'S15', round(0.07 + i_ * 0.278, 3), 0.25 + 0.05 * i_)
st.cue('sfx:spring', 'S15', S15E + 0.03, 0.4); st.cue('pop', 'S15', S15E + 0.2, 0.3)
for i_, t_ in enumerate(BR): st.cue('sfx:stretch', 'S16', max(0.0, t_ - 0.05), 0.3 + 0.08 * i_)
st.cue('thunder', 'S17', SN17, 0.5); st.cue('whoosh', 'S17', SN17, 0.45, 0.6, 300, 3000); st.cue('sfx:splat', 'S17', HIT17, 0.4); st.cue('sfx:stretch', 'S17', HIT17 + 0.04, 0.3); st.cue('sfx:spring', 'S17', OUT17, 0.45); st.cue('thud', 'S17', OUT17 + FLY17, 0.4)
for i in range(3): st.cue('pop', 'S17', UPT(i), 0.4)
st.cue('sfx:tick', 'S18', G18, 0.3)
for i, t_ in enumerate(T19): st.cue('sfx:stretch', 'S19', round(0.35 + t_, 3), 0.28 + 0.05 * i)

st.card('S09', 'JOSIANE')
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'éternuement", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'p1': CITIZEN('femme', 31, glasses=False, hair='long', hairColor='#5A3A28'), 'p2': CITIZEN('boss', 33, glasses=False, suit='#4B5059', tie='#B86A2E', hair='slick', facial='mustache', build={'belly': 0}),   # charcoal with painted lapels (the waiter's flat black read as a cut-out) 'p3': CITIZEN('mamie', 35, suit='#D98A3C'),
    'meteo': CITIZEN('journaliste', 37, suit='#3E6E8C'), 'chef': CITIZEN('prefet', 39, build={'belly': 0.1}, suit='#7D8791', tie='#2F6E5C'),   # not the hero's navy and red
    'assureur': CITIZEN('boss', 41, suit='#6A5A4A', glasses=True), 'inge': CITIZEN('worker', 43, glasses=False, skin='#8A5A3C', faceRim=True)})
import os
if os.environ.get('ETERN_DBG'): print({n: round(v, 3) for n, v in globals().items() if isinstance(v, float) and n[0].isupper()}, {s_: round(st.dur(s_), 3) for s_ in ['S%02d' % i for i in range(1, 20)]})
