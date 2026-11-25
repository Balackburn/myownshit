#!/usr/bin/env python3
"""Le chifoumi (story 96, cycle 51; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man lost at rock-paper-scissors to his wife. He contested. The federation reviewed the action on video: she had played a hundredth too late.
Match cancelled, to be replayed at the national stadium. Scientists filmed his hand at ten thousand frames a second: he always plays rock, for thirty
years. Judged too predictable, he was replaced by an unbeatable robot hand built by a factory; its first rock cost the factory two storeys. The
olympic committee selected it, the president decorated it in advance. Eighty thousand spectators, the anthem. Chi, fou, mi: the stadium split in two.
The hand played rock. His wife played well. She has trained on him for thirty years. The loser had to take out the bin. The hand contested: the well
does not count.
Running gags: the kitchen bin nobody takes out while the result is under review: full with its lid propped up in the kitchen (S01), overflowing in
the corner of the replay (S03), piled to the first-floor window by his door (S10), a mountain circled by seagulls behind the stadium (S11), taller
than his house in the reveal (S16), never mentioned before line 16. The referee's glowing rectangle drawn in the air (S02), which the robot hand
repeats at the end (S17). « Depuis trente ans » (S06: his photos and a block of tally marks) comes back the other way in S15.
Staging: in the kitchen, low across the table, his navy-sleeved fist (rock) and her flat mitten (paper) pump and meet, a quarter of the frame each;
she lays her hand over his fist and smiles; behind them, lit, the red bin with its lid propped up by a bulging bag. In a video-referee room three
referees in anthracite with headsets, their backs to us, lean to a wall of screens looping the kitchen footage; the middle one turns round and draws
a rectangle with his forearm and it hangs in the air as a glowing trail; slow lateral pan. The replay fills the frame: the two hands frozen apart, stepping a frame at a time, a red line
drawn between them, the bin behind them now towering and overflowing with bags and flies, « RALENTI » brackets. On the pitch a referee blows his whistle and waves the
match off (ANNULÉ); cut to the stadium from the air: a packed oval and, on the centre spot, a little kitchen table with a red top and two chairs.
In a white lab his fist sits in a padded clamp, scientists write, a big camera on rails slides up to the fist. The whiteboard:
three photos of him making a fist (a wedding veil, a bicycle, asleep on a pillow); a scientist scribbles a thick block of tally marks on « trente
ans ». At the federation an official slams a giant stamp on his file photo (a red cross, no words); he looks at his own fist. In a factory a
giant robot arm with a graphite box mitten rises among welders' sparks and closes its fist; screens loop his fist. It slams the test table (smear,
squash, dust from the roof); outside, the box factory slides two storeys into a ring of dust, two dusty workers lean out of windows now at ground
level. At his door an official moves the blank bib from his chest onto the robot's hand while the president on a stepladder pins a plain medal on
its wrist; beside the door the bags reach the first-floor window. The stadium stands up, hands on hearts (an invented anthem); the wife in her
apron faces the towering hand across the table; behind the rim a mountain of bags and seagulls; the scoreboard reads FINALE / ELLE – LA MAIN.
The arm pumps three times, the ground jumping; from the air a crack runs across the pitch and the two halves of the stadium slide apart, both
crowds cheering, while a round hole opens beside the table. Low: the fist comes down, a clean silhouette on the sky. She holds out her mitten
curled into a ring; a stone rim rises round the hole, the fist misses the table and plunges into the well, its arm stretching after it; a splash
comes up (PERDU). In the stands he lowers his fist to his waist and looks at it; insert: the kitchen, his fist under her hand. His street: the
mountain of bags taller than his house, gulls on top; the dripping robot rolls up; a quick tilt up the heap. The hand turns to us and draws the
referee's glowing rectangle; behind it one more bag rolls down; hold.
Natural look; cycle 51: props_chifoumi.js (chifHand, chifBin, chifBagHeap, chifTrail, chifScreens, chifHeadset, chifRedLine, chifHud, chifStadium,
chifClamp, chifRailCam, chifBoard, chifFile, chifRobot, chifRoom, chifSparks, chifWeldMask, chifFactoryBox, chifHouse, chifBib, chifMedal,
chifStepladder, chifApron); table, chair, desk, whistle, clipboardProp (props.js), giantStamp (props_rambarde), softDust (props_barbecue) reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83), heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() (CHECKS); every extra cast
member has a preset; word timings come from timeline.json through st.at (words counted from 0); the payoff shots (S13, S14, S17) get their own
tight cameras; the crowd is instanced and the actors among it are checked one by one; mitten hands everywhere (fist, flat hand, a ring for the
well, never five fingers); no straight raised arm held still (every reach moves and comes down); one take per mechanism (his deadpan look at
the fist, her smile, the referee's puffed cheeks, the workers' cough); squash, stretch, smear and hang on the State's machine (the robot);
moving holds (breathing, blinks, loops on screens, gulls, drips); no flag, no rings, no emblem or insignia (plain blazer, plain medal, plain bib),
the anthem is invented (a choir and a fanfare from the effect bank); the stadium is built as two halves; no English, no brands; nobody hurt (the
workers lean out unhurt, dusty)."""
from story_kit import *
import math

st = Story('chifoumi', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0),
         ('S09', 'L09', 0), ('S09b', 'L09', 7), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S13', 'L13', 0), ('S14', 'L14', 0), ('S15', 'L15', 0),
         ('S15b', 39.5333, 0), ('S16', 'L16', 0), ('S17', 'L17', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def sub(a, b): return [r(a[i] - b[i]) for i in range(3)]
def mul(a, s): return [a[i] * s for i in range(3)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
# a prop's local point to the world and back (prop ry in degrees, as the engine applies it)
def tow(base, ry, p): c, s_ = math.cos(math.radians(ry)), math.sin(math.radians(ry)); return [r(base[0] + p[0] * c + p[2] * s_), r(base[1] + p[1]), r(base[2] - p[0] * s_ + p[2] * c)]
def tol(base, ry, w): c, s_ = math.cos(math.radians(ry)), math.sin(math.radians(ry)); dx, dz = w[0] - base[0], w[2] - base[2]; return [r(dx * c - dz * s_), r(w[1] - base[1]), r(dx * s_ + dz * c)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))
def chkc(sid, c, pts, end=False):
    frm, look = (c.get('to') or c['from'], c.get('lookAt2') or c['lookAt']) if end else (c['from'], c['lookAt'])
    chk(sid + ('>' if end else ''), frm, look, c['lens'], pts)
def FC(sid, frm, pts, top=0.2, bottom=0.74, lenses=range(30, 60), margin=0.07):
    look, lens, w = fit(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses)
    CHECKS.append(f'{sid} fit lens {lens}'); return look, lens or max(lenses)
def FB(sid, frm, pts, top=0.2, bottom=0.74, lenses=range(30, 57), margin=0.07, inside=None, level=True):
    # fitBack: back the camera away along the line from the points until a lens fits; the distance moved goes to CHECKS
    f2, look, lens = fitBack(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses, inside=inside, level=level)
    CHECKS.append(f'{sid} fitBack {frm} -> {f2} lens {lens}'); return f2, look, lens or max(lenses)
def W(sid, lid, i):
    # (cycle 51) word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
HIDE = [0.01, 0.01, 0.01]
# a moving hold: slow breathing keys that carry the face (a keepPose key drops the face), clear of the blinks
def life(t0, t1, face, ph=0.0, blinks=(), period=0.9, amp=0.013):
    out, bl, t_, i = [], sorted(blinks), t0 + ph, 0
    while t_ < t1 - 0.1:
        if not any(-0.04 < t_ - b < 0.2 for b in bl):
            q = [r(1 - amp * 0.4, 4), r(1 + amp, 4), r(1 - amp * 0.4, 4)] if i % 2 == 0 else [r(1 + amp * 0.3, 4), r(1 - amp * 0.6, 4), r(1 + amp * 0.3, 4)]
            out.append(k(r(t_), toon={'sq': q, 'face': face}, toonDur=r(period * 0.8), toonEase='inOut', keepPose=True))
        t_ += period / 2; i += 1
    for b in bl: out += blink(r(b), face)
    return out
def HAND(pid, pos, ry, keys=None, **o): return P(pid, 'chifHand', pos=pos, ry=ry, opts=o, **({'keys': keys} if keys else {}))
def HEADSET(pid, who): return P(pid, 'chifHeadset', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.32})
def APRON(pid, who, **o): return P(pid, 'chifApron', on={'actor': who, 'joint': 'torso', 'offset': [0.0, -0.1, 0.14]}, opts={'h': 1.1, 'w': 0.4, **o})
def hand_tip(elbow, ry, s, sleeve, tilt=0.0, ahead=0.1):
    # where the middle of a chifHand's mitten is (elbow + forearm + half a hand), for the checks and to aim things at it
    d = s * (sleeve + ahead); F = fwd(ry); return [r(elbow[0] + F[0] * d * math.cos(tilt)), r(elbow[1] - d * math.sin(tilt)), r(elbow[2] + F[2] * d * math.cos(tilt))]

# the robot's two-bone arm, mirrored from props_chifoumi.js (chifRobot) to place a hand on it from the script: shoulder height and links at s = 1
def robot_wrist_world(base, ry, p): return tow(base, ry, p)

for g_ in [('S01', 1.2, 'mec', 'fist under her hand'), ('S07', 1.9, 'mec', 'looks at his fist'), ('S14', 0.5, 'femme', 'the well'), ('S15', 1.0, 'mec', 'lowers his fist')]:
    st.gag(*g_)

# ============================== the kitchen (kitchenDay: the counter along the back wall at z -3.3, the hanging lamp at (0, 2.7, -1.0))
KIT = {'fridge': False}
KT = [0.3, 0, -1.05]                                                    # the little table, 1.1 x 0.75, its top at 0.76
HK = [-0.12, 0.03, -1.62]; RYH = 22                                     # him behind the table on the left, turned three-quarters to us (a V)
FK = [0.72, 0.03, -1.62]; RYF = -22                                     # her on the right
# (round 1) the bin lower and to her side, its lid at chest height behind her left shoulder (at head height it read as a third head in a beret)
BIN1 = [0.52, 0, -2.95]; BINS1 = 1.15
SH = 1.7; SLV = 0.1                                                     # the cartoon hands: 2.2 times real size, a short forearm
RYE1, RYF1 = 55, -55                                                    # the forearms' headings: his from the left, hers from the right, angled to us
# (round 1) the two throws land apart, each hand a quarter of the frame (they piled into one knot at centre left), and only then does she lay hers on his
FIST_T, PAP_T = [0.06, 1.08, -0.85], [0.58, 1.08, -0.85]
EH1 = [r(FIST_T[0] - fwd(RYE1)[0] * SH * (SLV + 0.1)), FIST_T[1], r(FIST_T[2] - fwd(RYE1)[2] * SH * (SLV + 0.1))]      # his right hand goes there (the prop's elbow)
EF1 = [r(PAP_T[0] - fwd(RYF1)[0] * SH * (SLV + 0.14)), PAP_T[1], r(PAP_T[2] - fwd(RYF1)[2] * SH * (SLV + 0.14))]      # her left hand
FIST1 = hand_tip(EH1, RYE1, SH, SLV)
PAP1 = hand_tip(EF1, RYF1, SH, SLV, ahead=0.14)
ONFIST1 = add(FIST1, [0.03, 0.095, 0.0])
# the pumps start further apart, and her paper cocks back and up before the throw (the wind-up)
EH1S = add(EH1, [0.02, 0.05, -0.1]); EF1S = add(EF1, [-0.08, 0.05, -0.1]); EF1W = add(EF1S, [0.1, 0.16, -0.12])
EF1B = [r(ONFIST1[0] - fwd(RYF1)[0] * SH * (SLV + 0.14)), r(ONFIST1[1] - 0.04), r(ONFIST1[2] - fwd(RYF1)[2] * SH * (SLV + 0.14))]
def KITCHEN_PROPS(n, lvl=0, binS=BINS1, flies=0):
    return [P(f'table{n}', 'table', pos=KT, opts={'w': 1.1, 'd': 0.75, 'h': 0.76, 'color': '#DDB27A', 'legs': '#9A6E42'}),
            P(f'chaiseH{n}', 'chair', pos=[HK[0], 0, HK[2]], ry=RYH, opts={'color': '#7FB0C8'}), P(f'chaiseF{n}', 'chair', pos=[FK[0], 0, FK[2]], ry=RYF, opts={'color': '#7FB0C8'}),
            P(f'poubelle{n}', 'chifBin', pos=BIN1, ry=-20, opts={'level': lvl, 's': binS, 'flies': flies, 'stink': 2 if lvl else 0})]
HEROHAND = lambda: {'scl': {'handR': HIDE, 'handL': HIDE}}
WIFEHAND = lambda: {'scl': {'handL': HIDE, 'handR': HIDE}}
HANDH = lambda pid, e=EH1, **o: HAND(pid, e, RYE1, s=SH, sleeve=SLV, side='L', **o)
HANDF = lambda pid, e=EF1, **o: HAND(pid, e, RYF1, s=SH, sleeve=SLV, side='R', skin='#EBC29C', sleeveColor='#5E8C7A', **o)

# 1: the hook. Across the kitchen table, the two of them in a V behind it: both pump twice (chi, fou), and on « perdu » they throw: his fist (rock)
#    from the left, her flat mitten (paper) from the right, each a quarter of the frame; she lays her hand over his fist and smiles; he looks down
#    at it, then at us. Between them, lit, the red bin with its lid propped up by a bulging bag (the running gag, never mentioned)
D1 = st.dur('S01'); THROW1 = r(W('S01', 'L01', 3) - 0.02); LAY1 = r(THROW1 + 0.26)
F1 = [0.3, 1.82, 1.05]; L1 = [0.3, 1.25, -1.5]
C1 = cam(0.0, F1, add(F1, [0.0, -0.03, -0.15]), L1, add(L1, [0, -0.02, 0]), lens=48, ease='inOut')
chkc('S01', C1, {'fist': FIST1, 'paper': PAP1, 'binTop': add(BIN1, [0, 0.92 * BINS1, 0]), 'binLid': add(BIN1, [0, 0.66 * BINS1, 0]), 'himHead': add(HK, [0, 1.92, 0]), 'herHead': add(FK, [0, 1.86, 0]), 'himEar': add(HK, [-0.2, 1.6, 0]), 'herEar': add(FK, [0.2, 1.6, 0])})
chkc('S01', C1, {'fist': FIST1, 'onFist': ONFIST1, 'himHead': add(HK, [0, 1.92, 0])}, end=True)
SMUG = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.45, 'cheeks': 0.6}
PUMPS1 = [0.05, 0.31]
# (round 1) bigger pumps on chi and fou: the forearm swings 1 rad, and each body rises on the up-swing and squashes on the down-beat
def PUMPK(base, face, deep=None):
    out = []
    for j, p in enumerate(PUMPS1):
        dn = deep if (deep and j == len(PUMPS1) - 1) else [1.08, 0.9, 1.08]
        out += [k(r(p + 0.06), toon={**base, 'sq': [0.95, 1.07, 0.95], 'face': face}, toonDur=0.07, toonEase='out'), k(r(p + 0.19), toon={**base, 'sq': dn, 'face': face}, toonDur=0.06, toonEase='in')]
    return out
HB1 = lambda e: {'reach': {'R': R5(e, 1, 0.0)}, **HEROHAND(), 'hip': 0}
FB1 = lambda e: {'reach': {'L': R5(e, 1, 0.0)}, **WIFEHAND(), 'hip': 0}
HF1 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}
DEADH = {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}
# (round 1) his double take when her paper covers his fist: a look down, back to us blank (seven frames), then the snap down with the eyes stretched
#     wide, the head drawn long on a stretched neck and the body stretched up, held trembling, an overshoot, the settle; the film's eyes-on-stalks
#     take is kept for the lab (S05)
LOOK1 = r(LAY1 + 0.16); BACK1 = r(LOOK1 + 0.22); SNAP1 = r(BACK1 + 0.24)
TAKE1 = {**HB1(EH1), 'sq': [0.9, 1.13, 0.9], 'scl': {'handR': HIDE, 'handL': HIDE, 'head': [0.86, 1.3, 0.86]}, 'bend': {'neck': [0.25, 0, 0, 1.6, None]},
         'face': {'lid': 0.0, 'eye': 0.9, 'brow': 1.0, 'jaw': 0.35, 'mouth': 'O', 'gy': 0.8, 'noBlink': 1}}
HERO1 = [k(-0.4, look=add(FIST1, [0, 0.3, 0.5])), k(0.0, toon={**HB1(EH1S), 'face': HF1}, toonDur=0.0), *PUMPK(HB1(EH1S), HF1),
         k(r(THROW1 - 0.02), toon={**HB1(EH1), 'sq': [0.96, 1.05, 0.96], 'face': {**HF1, 'brow': 0.1}}, toonDur=0.08, toonEase='out'),
         k(r(THROW1 + 0.12), toon={**HB1(EH1), 'face': {**HF1, 'brow': 0.1}}, toonDur=0.12),
         k(LOOK1, look=FIST1, lookDur=0.1), k(LOOK1, toon={**HB1(EH1), 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2, 'gy': 0.5}}, toonDur=0.08),
         k(BACK1, look='camera', lookDur=0.07), k(BACK1, toon={**HB1(EH1), 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}}, toonDur=0.07),
         k(r(SNAP1 - 0.01), look=FIST1, lookDur=0.05),
         *beat(SNAP1, TAKE1, antic={**HB1(EH1), 'sq': [1.1, 0.88, 1.1], 'scl': {'handR': HIDE, 'handL': HIDE, 'head': [1.1, 0.9, 1.1]}, 'face': {'lid': 0.6, 'mouth': 'clench', 'brow': -0.4}}, hold=0.33,
               over={**HB1(EH1), 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.1, 'eye': 0.3, 'mouth': 'o', 'brow': 0.7}}, settle={**HB1(EH1), 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.5}}, settle_f=4),
         k(r(SNAP1 + 0.52), look='camera', lookDur=0.1), k(r(SNAP1 + 0.52), toon={**HB1(EH1), 'face': DEADH}, toonDur=0.1)]
# (round 1) her wind-up: she rises on the second pump and sinks into a deep squash with the paper cocked back, then throws stretched
FS1 = {'lid': 0.2, 'mouth': 'line', 'brow': 0.2}
FEMME1 = [k(-0.4, look=add(FIST1, [0, 0.3, 0.5])), k(0.0, toon={**FB1(EF1S), 'face': FS1}, toonDur=0.0), *PUMPK(FB1(EF1S), FS1)[:3],
          k(r(PUMPS1[1] + 0.13), toon={**FB1(EF1W), 'sq': [1.17, 0.8, 1.17], 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'smirk', 'brow': -0.5}}, toonDur=0.12, toonEase='inOut'),
          k(r(THROW1 - 0.01), toon={**FB1(EF1), 'sq': [0.91, 1.12, 0.91], 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': SMUG}, toonDur=0.06, toonEase='out'),
          k(r(THROW1 + 0.12), toon={**FB1(EF1), 'sq': [1.03, 0.97, 1.03], 'face': SMUG}, toonDur=0.08),
          k(LAY1, toon={**FB1(EF1B), 'sq': [1.02, 0.99, 1.02], 'face': SMUG}, toonDur=0.18, toonEase='inOut'),
          k(1.3, look='camera', lookDur=0.15), k(r(LAY1 + 0.25), toon={**FB1(EF1B), 'face': SMUG}, toonDur=0.1), *blink(1.85, SMUG)]
st.shot('S01', 'kitchenDay', setOpts=KIT, actors=[act('mec', HK, RYH, 'sit', 'neutral', keys=HERO1), act('femme', FK, RYF, 'sit', 'neutral', keys=FEMME1)],
        props=[*KITCHEN_PROPS(1), APRON('tablier1', 'femme'),
               HANDH('mainH1', e=EH1S, mode='rock', pumps=PUMPS1, pumpAmp=1.0, tilt=0.06, keys=[k(r(THROW1 - 0.02), to=EH1, dur=0.08, ease='out')]),
               HANDF('mainF1', e=EF1S, modes=[[-1, 'rock'], [r(THROW1 - 0.03), 'paper']], pumps=PUMPS1, pumpAmp=1.0, tiltK=[[0.0, 0.06], [r(PUMPS1[1] + 0.13), -0.25], [r(THROW1 - 0.01), 0.1], [r(THROW1 + 0.1), 0.06]],
                     keys=[k(r(PUMPS1[1] + 0.13), to=EF1W, dur=0.12, ease='inOut'), k(r(THROW1 - 0.01), to=EF1, dur=0.06, ease='out'), k(LAY1, to=EF1B, dur=0.18, ease='inOut')])],
        cams=[C1, glide([cam(r(SNAP1 - 0.05), add(F1, [0, 0.12, 0.2]), add(F1, [0, 0.12, 0.2]), add(L1, [0, 0.22, 0]), add(L1, [0, 0.22, 0]), lens=48)], 0.1),
              glide([cam(r(SNAP1 + 0.5), add(F1, [0, -0.02, -0.12]), add(F1, [0, -0.03, -0.15]), add(L1, [0, -0.01, 0]), add(L1, [0, -0.02, 0]), lens=48, ease='out')], 0.2)])
chkc('S01@take', {'from': add(F1, [0, 0.12, 0.2]), 'lookAt': add(L1, [0, 0.22, 0]), 'lens': 48}, {'takeTop': add(HK, [0, 2.4, 0]), 'fist': FIST1})
for t_ in PUMPS1: st.cue('sfx:step', 'S01', r(t_ + 0.19), 0.25)
st.cue('sfx:punch', 'S01', THROW1, 0.3); st.cue('sfx:paper', 'S01', r(LAY1 + 0.16), 0.25); st.cue('sfx:boing', 'S01', SNAP1, 0.25)

# ============================== the video-referee room (whiteVoid + chifRoom: cool grey walls; the wall of screens on the left wall)
ROOM2 = {'w': 9, 'd': 9, 'h': 4.6, 'wall': '#7D8CA3', 'floor': '#4A5262', 'band': '#5E6C82', 'bandH': 1.1, 'trim': '#2E3646', 'lights': 3, 'lightY': 4.5}
R2 = [[-1.0, 0, -2.6], [0.1, 0, -2.25], [1.1, 0, -2.7]]               # three referees with their backs to us, leaning toward the wall of screens
SCR2 = [0.0, 0, -3.95]
# 2: he contested; the federation reviewed the action on video. Behind three referees in anthracite with headsets who lean toward a wall of screens
#    looping the kitchen footage, the camera trucks right; on « fédération » the middle one turns round to us and draws a rectangle in the air with
#    his forearm, low in front of his chest so his face stays clear: a glowing trail that hangs, pulsing, to the cut
D2 = st.dur('S02'); RECT2 = r(W('S02', 'L02', 4) - 0.05); RDUR2 = 1.0
F2A, F2B = [-0.45, 2.0, 3.1], [0.35, 1.98, 3.0]
L2A, L2B = [-0.2, 1.62, -3.0], [0.2, 1.6, -3.0]
C2 = cam(0.0, F2A, F2B, add(L2A, [0, -0.25, 0]), add(L2B, [0, -0.25, 0]), lens=42, ease='inOut')
REF2 = R2[1]; RYR2 = yaw(REF2, F2B)
RC2 = off(REF2, RYR2, 0.62, -0.08, 1.38)                                # the rectangle's centre, low in front of his chest, facing the camera
RR = right(RYR2)
RW2, RH2 = 0.66, 0.4
RECTPTS2 = [[r(RC2[0] + RR[0] * sx * RW2 / 2), r(RC2[1] + sy * RH2 / 2), r(RC2[2] + RR[2] * sx * RW2 / 2)] for sx, sy in [(1, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)]]
chkc('S02', C2, {'ref1': add(R2[0], [0, 2.3, 0]), 'ref2': add(R2[1], [0, 2.3, 0]), 'ref3': add(R2[2], [0, 2.3, 0]), 'scrL': [-1.8, 2.55, -3.9], 'scrR': [1.8, 1.1, -3.9], 'rectL': RECTPTS2[1], 'rectR': RECTPTS2[0]})
chkc('S02', C2, {'ref1': add(R2[0], [0, 2.3, 0]), 'ref2face': add(R2[1], [0, 2.0, 0]), 'ref3': add(R2[2], [0, 2.3, 0]), 'rectL': RECTPTS2[1], 'rectR': RECTPTS2[0], 'rectLow': RECTPTS2[2]}, end=True)
# the hand rides the trail: one reach key per corner, at the times the trail gets there (constant speed, linear)
seglen = [math.dist(RECTPTS2[i], RECTPTS2[i + 1]) for i in range(4)]; TL2 = sum(seglen)
CORN2 = [RECT2] + [r(RECT2 + RDUR2 * sum(seglen[:i + 1]) / TL2) for i in range(4)]
REFF = {'lid': 0.35, 'mouth': 'line', 'brow': -0.4}
LEAN2 = {'bend': {'spine': [0.22, 0, 0, 1, None]}, 'face': REFF}
REFK2 = [k(0.0, look=[0.1, 1.8, -3.9], lookDur=0.0), k(0.0, toon=LEAN2, toonDur=0.0),
         k(r(RECT2 - 0.35), look=F2B, lookDur=0.2), k(r(RECT2 - 0.3), toon={'face': {**REFF, 'brow': 0.2}, 'reach': {'R': R5(RECTPTS2[0], 1, 0.1)}}, toonDur=0.25, toonEase='out')]
for i in range(4): REFK2.append(k(CORN2[i], toon={'face': {**REFF, 'brow': 0.3}, 'reach': {'R': R5(RECTPTS2[i + 1], 1, 0.1)}, 'hose': 0.15}, toonDur=r(CORN2[i + 1] - CORN2[i]), toonEase='linear'))
REFK2 += [k(r(CORN2[-1] + 0.05), toon={'face': {**REFF, 'brow': 0.1}, 'reach': {'R': R5(off(REF2, RYR2, 0.3, 0.25, 1.0), 0.0, 0.1)}}, toonDur=0.3, toonEase='inOut'), *blink(r(CORN2[-1] + 0.5), REFF)]
# (round 2) the side referees nod at the screens, shift their weight (a sway of the spine and a dip) and turn their heads to the rectangle, blinking
def NOD2(ph, sd, scr):
    ks = [k(r(ph + 0.6 * i), toon={**LEAN2, 'sq': [1.0, 1.0 - 0.02 * (i % 2), 1.0], 'bend': {'spine': [0.22, 0, sd * 0.07 * (1 if i % 2 else -1), 1, None], 'neck': [0.12 if i % 2 else 0.0, 0, 0, 1, None]}}, toonDur=0.3, toonEase='inOut') for i in range(5)]
    return ks + [k(r(RECT2 + 0.25 + 0.1 * sd), look=RC2, lookDur=0.2), k(r(RECT2 + 1.35 + 0.1 * sd), look=scr, lookDur=0.25)] + blink(r(ph + 0.9), REFF) + blink(r(RECT2 + 0.7 + 0.15 * sd), REFF)
st.shot('S02', 'whiteVoid', setOpts={'color': '#C9D0DA'}, actors=[
        act('arbitre1', R2[0], 170, 'stand', 'neutral', keys=[k(0.0, look=[-0.8, 1.9, -3.9], lookDur=0.0), k(0.0, toon=LEAN2, toonDur=0.0), *NOD2(0.2, 1, [-0.8, 1.9, -3.9])]),
        act('arbitre2', REF2, 180, 'stand', 'neutral', keys=[k(r(RECT2 - 0.4), to=REF2, dur=0.3, glide=True, face=RYR2), *REFK2]),
        act('arbitre3', R2[2], 190, 'stand', 'neutral', keys=[k(0.0, look=[0.9, 1.7, -3.9], lookDur=0.0), k(0.0, toon=LEAN2, toonDur=0.0), *NOD2(0.5, -1, [0.9, 1.7, -3.9])])],
        props=[P('salle2', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM2), P('ecrans2', 'chifScreens', pos=SCR2, opts={'cols': 3, 'rows': 2, 'sw': 1.15, 'sh': 0.7, 'y': 1.15}),
               P('console2', 'table', pos=[0.0, 0, -3.35], opts={'w': 3.6, 'd': 0.6, 'h': 0.95, 'color': '#2E3646', 'legs': '#1E2430'}),
               *[HEADSET(f'casque2_{i}', f'arbitre{i + 1}') for i in range(3)],
               P('trait2', 'chifTrail', pos=[0, 0, 0], opts={'pts': RECTPTS2, 'at': RECT2, 'dur': RDUR2, 'r': 0.014})],
        cams=[C2])
st.cue('sfx:beep', 'S02', 0.2, 0.15); st.cue('sfx:zip', 'S02', RECT2, 0.25); st.cue('sfx:bell', 'S02', r(RECT2 + RDUR2), 0.2)

# 3: she had played a hundredth too late. The replay fills the frame: the two hands frozen apart over the table, the playback stepping one frame at a
#    time (her flat hand creeps down in three jerks), then a red line drawn between them on « centième »; in the top corner the bin, huge now,
#    overflowing with bags; the « RALENTI » brackets over it all, a cool desaturated picture
D3 = st.dur('S03'); LINE3 = r(W('S03', 'L03', 5) - 0.1)
# (round 1) her flat hand starts high and comes down in three big jerks, each held (they could not be told apart), on a camera pulled back so the
#     heads sit at a third of the frame and the bag tower stands in the top right corner (it stood between their heads like a snowman); the replay is
#     graded cool and grey (it stayed warm), and the « centième » marker is a plain line with tick ends (the rings read as a dumbbell)
EF3 = add(EF1, [0.04, 0.22, 0.0]); STEP3 = 0.075
FIST3 = FIST1; PAP3 = hand_tip(EF3, RYF1, SH, SLV, ahead=0.14); PAP3E = add(PAP3, [0, -3 * STEP3, 0])
F3 = [0.3, 1.55, 2.3]; L3 = [0.3, 1.3, -1.5]; LENS3 = 46
C3 = cam(0.0, F3, add(F3, [0.0, 0.0, -0.08]), L3, L3, lens=LENS3)
BIN3 = [1.32, 0, -3.0]; BINS3 = 1.6
chkc('S03', C3, {'fist': FIST3, 'paper': PAP3, 'paperEnd': PAP3E, 'towerTop': add(BIN3, [0, 1.72 * BINS3, 0]), 'towerL': add(BIN3, [-0.4 * BINS3, 1.2 * BINS3, 0]), 'himHead': add(HK, [0, 2.0, 0]), 'herHead': add(FK, [0, 2.0, 0])})
STEPS3 = [0.3, 0.62, 0.94]
# the replay brackets fill the frame exactly: a plane 0.45 m in front of the lens, as tall as the frame there, turned to face it
_d3 = [L3[i] - F3[i] for i in range(3)]; _n3 = math.sqrt(sum(v * v for v in _d3)); _d3 = [v / _n3 for v in _d3]
HUDP = [r(F3[i] + _d3[i] * 0.45) for i in range(3)]; HUDH = r(2 * 0.45 * math.tan(math.radians(LENS3) / 2) * 0.98); HUDW = r(HUDH * 9 / 16)
_yb = math.asin(-_d3[0]); HUDR = [r(math.asin(_d3[1] / math.cos(_yb)), 4), r(_yb, 4), 0.0]
st.shot('S03', 'kitchenDay', setOpts=KIT, grade='saturate(0.28) contrast(1.1) brightness(1.03)', look={'warm': 0.0, 'sunColor': '#D2E0FF'}, actors=[
        act('mec', HK, RYH, 'sit', 'neutral', keys=[k(0.0, look=FIST3, lookDur=0.0), k(0.0, toon={'reach': {'R': R5(EH1, 1, 0.0)}, **HEROHAND(), 'hip': 0, 'breathe': 0, 'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0)]),
        act('femme', FK, RYF, 'sit', 'neutral', keys=[k(0.0, look=FIST3, lookDur=0.0), k(0.0, toon={'reach': {'L': R5(EF3, 1, 0.0)}, **WIFEHAND(), 'hip': 0, 'breathe': 0, 'face': SMUG}, toonDur=0.0),
                                                       *[k(t_, toon={'reach': {'L': R5(add(EF3, [0, -STEP3 * (j + 1), 0]), 1, 0.0)}, **WIFEHAND(), 'hip': 0, 'breathe': 0, 'face': SMUG}, toonDur=0.02) for j, t_ in enumerate(STEPS3)]])],
        props=[*KITCHEN_PROPS(3)[:3], P('poubelle3', 'chifBin', pos=BIN3, ry=-25, opts={'level': 2, 's': BINS3, 'flies': 6, 'stink': 3}),
               HANDH('mainH3', mode='rock', tilt=0.06),
               # (round 2) her flat hand turned 0.9 rad about the forearm so its flat face, not its edge, faces us
               HANDF('mainF3', e=EF3, mode='paper', tilt=0.06, roll=0.9, keys=[k(t_, to=add(EF3, [0, -STEP3 * (j + 1), 0]), dur=0.02) for j, t_ in enumerate(STEPS3)]),
               P('ligne3', 'chifRedLine', pos=[0, 0, 0], opts={'a': add(FIST3, [0.0, 0.13, 0.06]), 'b': add(PAP3E, [0.0, -0.05, 0.06]), 'at': LINE3, 'dur': 0.22, 'r': 0.016, 'ring': 0, 'tick': 0.16, 'view': [0, 0.1, 1]}),
               P('hud3', 'chifHud', pos=HUDP, rot=HUDR, opts={'w': HUDW, 'h': HUDH})],
        cams=[C3])
st.cue('sfx:scratch', 'S03', 0.0, 0.25); [st.cue('sfx:tick', 'S03', t_, 0.3) for t_ in STEPS3]; st.cue('sfx:zip', 'S03', LINE3, 0.2)

# ============================== the national stadium (grassland + chifStadium: the centre spot at the origin, the halves split along x = 0)
# (round 1) the hole moved behind her as the S14 close-up sees her, so the plunge and the splash play behind her while she holds the ring
# (round 2) the hole beside the table on the camera side (it was behind her, 2.9 m from the table): the S12 aerial shows it as a dark circle next to
#     the table and the S14 fist overshoots the table into it in the open; the halves end 8 m apart each (the gap reads 15-20 % of the aerial)
STAD = {'board': ['FINALE', 'ELLE – LA MAIN'], 'boardFar': -10.0, 'cheer': 0.7, 'hole': [-0.55, 1.3], 'holeR': 0.75}
SPL12E = 8.0
GRASS = {'clouds': 14, 'grass': '#78A85A'}
TBL = [0.0, 0, 0.0]
def PITCH_TABLE(n, keys=None, chairKeys=None):
    ck = lambda x: {'keys': chairKeys(x)} if chairKeys else {}
    return [P(f'tableS{n}', 'table', pos=TBL, opts={'w': 0.8, 'd': 0.6, 'h': 0.76, 'color': '#D8463A', 'legs': '#8A5A3A'}, **({'keys': keys} if keys else {})),
            P(f'chaiseA{n}', 'chair', pos=[-0.62, 0, 0.0], ry=90, opts={'color': '#7FB0C8'}, **ck(-0.62)), P(f'chaiseB{n}', 'chair', pos=[0.62, 0, 0.0], ry=-90, opts={'color': '#7FB0C8'}, **ck(0.62))]
REFP = [1.2, 0, 6.5]
# 4: match cancelled, to be replayed at the national stadium. On the pitch a referee blows his whistle, cheeks puffed, and waves the match off with
#    both forearms crossing (ANNULÉ stamps on « annulé », his head kept under the card); cut on « À rejouer » to the stadium from the air: a packed
#    oval and, on the centre spot, a little table with a red top and two chairs, the camera sinking toward it so the table reads
D4 = st.dur('S04'); WAVE4 = r(W('S04', 'L04', 1) - 0.05); CUT4 = r(W('S04', 'L04', 2) - 0.04)
F4A = off(REFP, 20, 3.0, 0.2, 1.55)
L4A, LENS4A = FC('S04', F4A, {'refTop': add(REFP, [0, 2.38, 0]), 'refWaist': add(REFP, [0, 0.95, 0]), 'handL': off(REFP, 20, 0.45, 0.45, 1.3), 'handR': off(REFP, 20, 0.45, -0.45, 1.3)}, top=0.22, bottom=0.72, lenses=range(30, 56))
C4A = cam(0.0, F4A, add(F4A, [0, 0, -0.12]), L4A, add(L4A, [0, 0.02, 0]), lens=LENS4A)
chkc('S04', C4A, {'refTop': add(REFP, [0, 2.35, 0]), 'refFeet': REFP, 'handsUp': add(REFP, [0, 1.5, 0])})
# (round 1) the aerial sinks to 21 m from the table so the table and its two chairs read (about 8 % of the width)
# (round 2) it sinks on to 11 m from the table (21 m left the table a red dot)
F4B, T4B = [0.0, 62.0, 46.0], [0.0, 8.2, 7.4]
C4B = cam(CUT4, F4B, T4B, [0, 0, -4.0], [0, 0, -0.3], lens=44, ease='out')
chkc('S04', C4B, {'table': TBL, 'standsN': [0, 9, -38], 'standsS': [0, 9, 38], 'endW': [-45, 9, 0], 'endE': [45, 9, 0]})
chkc('S04', C4B, {'table': TBL, 'tableL': [-0.4, 0.76, 0], 'tableR': [0.4, 0.76, 0], 'chairL': [-0.85, 0.5, 0], 'chairR': [0.85, 0.5, 0]}, end=True)
# (round 2) the whistle blast puffs the head itself (wide and short), white cuffs and gloves so the forearms read on the dark suit, and the
#     crossing swings open wider than his body each way
PUFF = {'lid': 0.2, 'mouth': 'O', 'jaw': 0.1, 'brow': 0.6, 'puff': 1}; PUFFS = [1.3, 0.9, 1.12]
WAVEP = lambda a: {'reach': {'R': R5(off(REFP, 20, 0.45, a * 0.72, 1.32), 1, 0.05), 'L': R5(off(REFP, 20, 0.42, -a * 0.72, 1.24), 1, 0.05)}, 'face': PUFF, 'scl': {'head': PUFFS}}
REFK4 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'face': {**PUFF, 'puff': 0.0}}, toonDur=0.0), k(0.04, toon={'face': {**PUFF, 'puff': 0.0}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.06),
         k(0.12, toon={'face': PUFF, 'scl': {'head': PUFFS}, 'sq': [1.05, 0.96, 1.05]}, toonDur=0.06, toonEase='outBack')]
for i, t_ in enumerate([WAVE4, r(WAVE4 + 0.14), r(WAVE4 + 0.28), r(WAVE4 + 0.42)]): REFK4.append(k(t_, toon=WAVEP(1 if i % 2 == 0 else -1), toonDur=0.1, toonEase='inOut'))
REFK4.append(k(r(WAVE4 + 0.56), toon={'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.15))
st.shot('S04', 'grassland', setOpts=GRASS, actors=[act('arbitreT', REFP, 20, 'stand', 'neutral', keys=[*REFK4, k(CUT4, visible=False)])],
        props=[P('stade4', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.8, 'board': None}), *PITCH_TABLE(4),
               P('sifflet4', 'whistle', on={'actor': 'arbitreT', 'joint': 'head', 'offset': [0.0, 0.11, 0.16], 'rot': [0, 1.5708, 0]}, scale=3.0)],
        cams=[C4A, C4B])
st.card('S04', 'ANNULÉ', at=r(WAVE4 + 0.04))
st.cue('sfx:whistle', 'S04', 0.1, 0.5); st.cue('rain', 'S04', CUT4, 0.12, r(D4 - CUT4)); st.cue('whoosh', 'S04', CUT4, 0.2, 0.3, 400, 1800)

# ============================== the lab (whiteVoid + chifRoom: white walls, a pale blue band)
ROOM5 = {'w': 10, 'd': 9, 'h': 3.6, 'wall': '#E6ECF0', 'floor': '#CDD3D8', 'band': '#A9C8DE', 'bandH': 1.0, 'trim': '#5E7E9A', 'lights': 3}
CL5 = [0.0, 0, -1.2]; CLH = 1.2
HM5 = [-0.42, 0, -1.65]; RYM5 = 12                                        # he stands beside the clamp, his left forearm in the jaws
EH5 = [0.0, CLH + 0.02, -1.32]; RYE5 = 0                                   # the forearm in the clamp, the fist out toward +Z
FIST5 = hand_tip(EH5, RYE5, 1.5, 0.22)
SAV5 = [[0.85, 0, -2.45], [0.2, 0, -3.35]]
# 5: scientists filmed his hand at ten thousand frames a second. His fist sits in an orange padded clamp under two bright lamps; two scientists in
#    white coats write on clipboards; a big camera on rails slides slowly toward the fist (the lens a hand from it by the end); he looks at us
D5 = st.dur('S05')
# (round 2) closer and square on (his head about 18 % of the width, it was 10 %), wide enough on the right for the rail camera's body to arrive
F5 = [0.05, 1.85, 2.0]; L5 = [0.06, 1.52, -1.4]
C5 = cam(0.0, F5, [0.08, 1.84, 1.75], L5, [0.1, 1.51, -1.4], lens=46, ease='inOut')
# (round 1) the rail comes in from the right, across our view, so the camera body never covers the fist and its lens ends a hand from it
RAIL5 = [1.72, 0, 0.0]; RY5R = -120; RZ1 = 0.8; LENS5END = tow(RAIL5, RY5R, [0, 1.25, RZ1 + 0.93])
chkc('S05', C5, {'fist': FIST5, 'himTop': add(HM5, [0, 2.32, 0]), 'himHead': add(HM5, [0, 2.0, 0]), 'sav1': add(SAV5[0], [0, 2.3, 0]), 'sav2': add(SAV5[1], [0, 2.3, 0]), 'sav2L': add(SAV5[1], [-0.35, 1.9, 0]), 'railCamStart': tow(RAIL5, RY5R, [0, 1.25, -1.1]), 'lampL': [-0.95, 1.95, -0.65]})
CHECKS.append(f'S05 lens end {LENS5END} to fist {r(math.dist(LENS5END, FIST5))} m')
chkc('S05', C5, {'fist': FIST5, 'himTop': add(HM5, [0, 2.32, 0]), 'himHead': add(HM5, [0, 2.0, 0]), 'lensEnd': LENS5END, 'sav2': add(SAV5[1], [0, 2.3, 0]), 'sav2L': add(SAV5[1], [-0.35, 1.9, 0])}, end=True)
SAVF = {'lid': 0.3, 'mouth': 'line', 'brow': 0.4}
def WRITE(who, p, ry, t0, n=8):
    base = off(p, ry, 0.42, 0.05, 1.25)
    ks = [k(0.0, look=FIST5, lookDur=0.0), k(0.0, toon={'reach': {'L': R5(off(p, ry, 0.4, -0.12, 1.3), 1, 0.05), 'R': R5(base, 1, 0.05)}, 'face': SAVF, 'bend': {'neck': [0.2, 0, 0, 1, None]}}, toonDur=0.0)]
    for i in range(n): ks.append(k(r(t0 + 0.13 * i), toon={'reach': {'L': R5(off(p, ry, 0.4, -0.12, 1.3), 1, 0.05), 'R': R5(off(p, ry, 0.42, 0.05 + 0.05 * (i % 2), 1.25 - 0.02 * (i % 3)), 1, 0.05)}, 'face': SAVF, 'bend': {'neck': [0.2, 0, 0, 1, None]}}, toonDur=0.1))
    return ks + [k(r(t0 + 0.13 * n + 0.2), look='camera', lookDur=0.15)] + blink(r(t0 + 0.13 * n + 0.7), SAVF)
HB5 = {'reach': {'L': R5(EH5, 1, 0.0)}, 'scl': {'handL': HIDE}}
H5F = {'lid': 0.42, 'mouth': 'line', 'brow': -0.1}
BULGE = lambda pop, pl, sq, extra=None: {**HB5, 'sq': sq, 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {'pop': pop, 'popLen': pl, 'eyeScale': 1.5, 'brow': 1, 'lid': 0.0, 'mouth': 'o', 'jaw': 0.15, 'tremble': 1, 'pupilShake': 1, 'sweat': 1, 'noBlink': 1, **(extra or {})}}
BUL5 = 2.0
HEROK5 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={**HB5, 'face': H5F}, toonDur=0.0),
          k(0.9, look=LENS5END, lookDur=0.2), k(0.9, toon={**HB5, 'face': {**H5F, 'lid': 0.25, 'brow': 0.3}}, toonDur=0.15),
          k(1.55, look='camera', lookDur=0.12),
          k(1.45, fx={'sweat': 1, 'sweatSize': 3.0}), k(1.45, toon={**HB5, 'sq': [0.98, 1.02, 0.98], 'face': {'lid': 0.1, 'brow': 0.7, 'mouth': 'line', 'sweat': 1, 'eye': 0.3}}, toonDur=0.15),
          k(r(BUL5 - 0.07), toon={**HB5, 'sq': [1.06, 0.93, 1.06], 'face': {'lid': 0.5, 'brow': -0.3, 'mouth': 'clench', 'sweat': 1, 'noBlink': 1}}, toonDur=0.05),
          k(BUL5, toon=BULGE(0.75, 0.12, [0.94, 1.07, 0.94]), toonDur=0.04, toonEase='outBack'),
          k(r(BUL5 + 0.08), toon=BULGE(0.6, 0.07, [0.96, 1.05, 0.96]), toonDur=0.06),
          *[k(r(BUL5 + 0.2 + 0.1 * i), toon=BULGE(0.62 + 0.04 * (i % 2), 0.08 + 0.01 * (i % 2), [0.96, 1.05 - 0.01 * (i % 2), 0.96]), toonDur=0.05) for i in range(4)],
          k(r(BUL5 + 0.62), toon=BULGE(0.5, 0.06, [0.97, 1.04, 0.97], {'mouth': 'line', 'jaw': 0.0}), toonDur=0.08)]
st.shot('S05', 'whiteVoid', setOpts={'color': '#E8EEF2'}, actors=[
        act('mec', HM5, RYM5, 'stand', 'neutral', keys=HEROK5),
        act('savant1', SAV5[0], -35, 'stand', 'neutral', keys=WRITE('savant1', SAV5[0], -35, 0.3)),
        act('savant2', SAV5[1], -20, 'stand', 'neutral', keys=WRITE('savant2', SAV5[1], -20, 0.9, 6))],
        props=[P('labo5', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM5), P('pince5', 'chifClamp', pos=CL5, opts={'h': CLH, 'lamps': False}),
               HAND('poing5', EH5, RYE5, s=1.5, sleeve=0.22, mode='rock'),
               P('rail5', 'chifRailCam', pos=RAIL5, ry=RY5R, opts={'len': 3.2, 'z0': -1.1, 'z1': RZ1, 't0': 0.0, 't1': r(D5 - 0.2)}),
               *[P(f'bloc5_{i}', 'clipboardProp', on={'actor': f'savant{i + 1}', 'hand': 'L', 'face': 'camera'}, scale=1.4) for i in range(2)]],
        cams=[C5])
st.cue('engine', 'S05', 0.0, 0.12); st.cue('sfx:shutter', 'S05', 0.6, 0.2); st.cue('sfx:shutter', 'S05', 1.6, 0.2); st.cue('sfx:boing', 'S05', BUL5, 0.25)

# 6: conclusion: he always plays rock; for thirty years. The whiteboard in the same lab: three photos of him making a fist (a wedding veil beside
#    him, a bicycle, asleep on a pillow), the camera panning along them; on « trente ans » a scientist scribbles a thick block of tally marks under
#    them row after row, the camera sinking to it
D6 = st.dur('S06'); TALLY6 = r(W('S06', 'L06', 5) - 0.1); TDUR6 = 0.85
BRD6 = [0.0, 0, -3.3]; BW6, BH6, BY6 = 2.3, 1.55, 0.8
SAV6 = [-1.65, 0, -2.8]
# (round 2) the tally block on the right two thirds of the board, the scientist at its right end so his arm reaches every stroke (it wrote with no
#     hand in shot); thick black marker strokes, a marker in his hand
TW6, TX6 = 0.62, 0.17; TRW6 = r(BW6 * TW6); TX06 = r(-TRW6 / 2 + BW6 * TX6); SAV6B = [1.6, 0, -2.75]
F6A, F6B = [-0.7, 1.95, -0.3], [0.45, 1.92, -0.4]
C6 = cam(0.0, F6A, F6B, [-0.55, 1.85, -3.3], [0.35, 1.82, -3.3], lens=46, ease='inOut')
C6B = glide([cam(r(TALLY6 - 0.1), [0.35, 1.6, 0.55], [0.4, 1.58, 0.45], [0.5, 1.42, -3.3], [0.55, 1.4, -3.3], lens=50, ease='out')], 0.35)
chkc('S06', C6, {'ph1': [-0.83, 1.92, -3.29], 'ph2': [0.0, 1.92, -3.29], 'ph3': [0.83, 1.92, -3.29]})
chkc('S06', C6, {'ph2': [0.0, 1.92, -3.29], 'ph3T': [0.83, 2.32, -3.29], 'ph3R': [1.2, 1.92, -3.29]}, end=True)
chkc('S06', C6B, {'tallyTL': [TX06, 1.44, -3.29], 'tallyBR': [r(TX06 + TRW6), 0.95, -3.29], 'photosLow': [0.0, 1.55, -3.29], 'savHead': add(SAV6B, [0, 2.3, 0]), 'savHand': [r(TX06 + 0.2), 1.3, -3.2]})
TROWY = [BY6 + BH6 * 0.4 - (j + 0.5) * BH6 * 0.33 / 5 for j in range(5)]
SAVK6 = [k(0.0, look=[0.0, 1.9, -3.3], lookDur=0.0), k(0.0, toon={'reach': {'L': R5([-1.2, 1.5, -3.2], 0.0, 0.08)}, 'face': SAVF}, toonDur=0.0)]
for j, y_ in enumerate(TROWY):
    t0 = r(TALLY6 + TDUR6 * j / 5); t1 = r(TALLY6 + TDUR6 * (j + 1) / 5)
    SAVK6 += [k(r(t0 - 0.02), toon={'reach': {'L': R5([r(TX06 + 0.04), y_, -3.18], 1, 0.12)}, 'face': {**SAVF, 'brow': 0.7}, 'hose': 0.3}, toonDur=0.03),
              k(t0, toon={'reach': {'L': R5([r(TX06 + TRW6 * 0.97), y_, -3.18], 1, 0.12)}, 'face': {**SAVF, 'brow': 0.7}, 'hose': 0.3}, toonDur=r(t1 - t0 - 0.02), toonEase='linear')]
SAVK6 += [k(r(TALLY6 + TDUR6 + 0.08), toon={'reach': {'L': R5([-1.4, 1.2, -3.0], 0.0, 0.08)}, 'face': SAVF}, toonDur=0.25), k(r(TALLY6 + TDUR6 + 0.15), look='camera', lookDur=0.15)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#E8EEF2'}, actors=[act('savant1', SAV6, 35, 'stand', 'neutral', keys=[k(r(TALLY6 - 0.45), to=SAV6B, dur=0.35, glide=True, face=-115), *SAVK6])],
        props=[P('labo6', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM5), P('tableau6', 'chifBoard', pos=BRD6, opts={'w': BW6, 'h': BH6, 'y': BY6, 'tallyAt': TALLY6, 'tallyDur': TDUR6, 'rows': 5, 'tallyW': TW6, 'tallyX': TX6, 'ink': '#15151A', 'inkW': 0.15}),
               P('feutre6', 'marker', on={'actor': 'savant1', 'hand': 'L'}, scale=2.2)],
        cams=[C6, C6B])
st.cue('sfx:paper', 'S06', r(TALLY6), 0.3); st.cue('sfx:scratch', 'S06', r(TALLY6 + 0.3), 0.18)

# ============================== the federation (whiteVoid + chifRoom: grey-green walls, the plaque FÉDÉRATION)
ROOM7 = {'w': 9, 'd': 8, 'h': 3.4, 'wall': '#B7C6BC', 'floor': '#C8B08C', 'band': '#8FA89A', 'bandH': 1.05, 'trim': '#3E5446', 'lights': 2, 'sign': ['FÉDÉRATION', 0.35, 2.62, 2.1, 0.42], 'signBg': '#2E4A3C'}
DESK7 = [0.0, 0, -1.5]; FILE7 = [0.1, 0.765, -1.4]
OF7 = [-0.55, 0, -2.25]; HM7 = [0.6, 0, -0.82]; RYM7 = -25
# 7: he was judged too predictable. From above the desk: the official behind it hangs a giant rubber stamp tilted toward us, then slams it down on
#    his file photo (two frames, a squash, the desk jumps); lifted off: a red cross in a slanted frame, no words; beside the desk he raises his own
#    fist to his chest and looks at it
D7 = st.dur('S07'); STAMP7 = r(W('S07', 'L07', 6) - 0.04)
# (round 1) the camera higher over the desk (it was not shot from above), the file and its mark bigger (70 px, lost once the stamp lifted)
F7 = [0.15, 3.9, 2.4]; L7 = [0.2, 1.0, -1.35]
C7 = cam(0.0, F7, add(F7, [0.0, -0.06, -0.15]), L7, L7, lens=48)
EH7 = off(HM7, RYM7, 0.3, 0.08, 1.42); RYE7 = RYM7 - 150; TILT7 = -1.1
FIST7 = [EH7[0], r(EH7[1] + 0.3), EH7[2]]
chkc('S07', C7, {'file': FILE7, 'fileTop': add(FILE7, [0, 0, -0.45]), 'fileNear': add(FILE7, [0, 0, 0.45]), 'ofHead': add(OF7, [0, 2.3, 0]), 'stampUp': [0.1, 2.25, -1.45], 'himHead': add(HM7, [0, 2.3, 0]), 'himFeet': HM7, 'fist': FIST7})
STK7 = [k(0.0, to=[0.12, 1.75, -1.55], dur=0.01), k(0.0, rotTo=[0.55, 0, 0], dur=0.01), k(0.25, to=[0.12, 1.95, -1.5], dur=r(STAMP7 - 0.35), ease='out'),
        k(r(STAMP7 - 0.07), to=[0.12, 0.8, -1.42], dur=0.07, ease='in'), k(r(STAMP7 - 0.07), rotTo=[0, 0, 0], dur=0.07),
        k(r(STAMP7 + 0.25), to=[0.05, 1.4, -1.75], dur=0.3, ease='out'), k(r(STAMP7 + 0.25), rotTo=[-0.3, 0, 0.2], dur=0.3)]
OFK7 = [k(0.0, look=FILE7, lookDur=0.0), k(0.0, toon={'reach': {'R': R5([0.06, 1.98, -1.55], 1, 0.0), 'L': R5([0.18, 1.98, -1.55], 1, 0.0)}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.7}}, toonDur=0.0),
        k(0.25, toon={'reach': {'R': R5([0.06, 2.18, -1.5], 1, 0.0), 'L': R5([0.18, 2.18, -1.5], 1, 0.0)}, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.9}}, toonDur=r(STAMP7 - 0.35), toonEase='out'),
        k(r(STAMP7 - 0.07), toon={'reach': {'R': R5([0.06, 1.03, -1.42], 1, 0.0), 'L': R5([0.18, 1.03, -1.42], 1, 0.0)}, 'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.7, 'mouth': 'clench', 'brow': -1}}, toonDur=0.07, toonEase='in'),
        k(r(STAMP7 + 0.25), toon={'reach': {'R': R5([0.0, 1.63, -1.75], 1, 0.0), 'L': R5([0.12, 1.63, -1.75], 1, 0.0)}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.3)]
# (round 1) the stamp's shockwave flattens him like a pancake beside the desk (his fist with him), held trembling, then he re-inflates in three
#     puffs past his height and settles, and only then looks at his fist
H7 = lambda e, sq=None, face=None, extra=None: {'reach': {'R': R5(e, 1, 0.0)}, 'scl': {'handR': HIDE}, 'hip': 0, **({'sq': sq} if sq else {}), 'face': face or {'lid': 0.42, 'mouth': 'line'}, **(extra or {})}
FL7 = 0.38; EH7F = [EH7[0], r(EH7[1] * FL7), EH7[2]]; SW7 = r(STAMP7 + 0.03)
FLAT7 = {'lid': 0.0, 'eye': 0.6, 'brow': 1.0, 'mouth': 'o', 'jaw': 0.2, 'noBlink': 1}
EHK7 = [(SW7, EH7F, 0.04), (r(SW7 + 0.28), [EH7[0], r(EH7[1] * 0.7), EH7[2]], 0.06), (r(SW7 + 0.38), [EH7[0], r(EH7[1] * 1.12), EH7[2]], 0.07), (r(SW7 + 0.48), [EH7[0], r(EH7[1] * 0.97), EH7[2]], 0.07), (r(SW7 + 0.58), EH7, 0.07)]
HEROK7 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon=H7(EH7), toonDur=0.0),
          k(SW7, toon=H7(EH7F, [1.5, FL7, 1.5], FLAT7, {'hairUp': 1}), toonDur=0.04, toonEase='out'),
          *[k(r(SW7 + 0.067 * (i + 1)), toon=H7(EH7F, [1.5 + 0.03 * (-1) ** i, FL7 - 0.02 * (-1) ** i, 1.5], FLAT7, {'hairUp': 1}), toonDur=0.03) for i in range(3)],
          k(r(SW7 + 0.28), toon=H7(EHK7[1][1], [1.25, 0.7, 1.25], {**FLAT7, 'puff': 1, 'mouth': 'kiss'}, {'hairUp': 0.8}), toonDur=0.06, toonEase='out'),
          k(r(SW7 + 0.38), toon=H7(EHK7[2][1], [0.9, 1.12, 0.9], {'lid': 0.0, 'eye': 0.4, 'brow': 0.8, 'mouth': 'o'}, {'hairUp': 0.6}), toonDur=0.07, toonEase='out'),
          k(r(SW7 + 0.48), toon=H7(EH7, [1.04, 0.97, 1.04], {'lid': 0.2, 'brow': 0.4, 'mouth': 'line'}), toonDur=0.07),
          k(r(SW7 + 0.58), toon=H7(EH7, None, {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}), toonDur=0.08),
          k(r(SW7 + 0.62), look=FIST7, lookDur=0.12), k(r(SW7 + 0.62), toon=H7(EH7, None, {'lid': 0.3, 'mouth': 'line', 'brow': 0.25, 'gy': 0.4}), toonDur=0.1)]
st.shot('S07', 'whiteVoid', setOpts={'color': '#DDE3DC'}, actors=[act('officiel7', OF7, 8, 'stand', 'neutral', keys=OFK7), act('mec', HM7, RYM7, 'stand', 'neutral', keys=HEROK7)],
        props=[P('bureau7', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM7), P('desk7', 'desk', pos=DESK7, opts={'w': 1.8, 'color': '#5E7A6A', 'top': '#B98A5A'}),
               P('dossier7', 'chifFile', pos=FILE7, ry=4, opts={'stampAt': STAMP7, 'w': 0.78, 'h': 0.92, 'markW': 0.94, 'markH': 0.66, 'markK': 1.5}), P('tampon7', 'giantStamp', pos=[0.12, 1.75, -1.55], opts={'s': 0.95}, keys=STK7),
               HAND('poing7', EH7, RYE7, s=1.35, sleeve=0.18, mode='rock', tilt=TILT7, keys=[k(t_, to=p_, dur=d_, ease='out') for t_, p_, d_ in EHK7])],
        cams=[C7, cam(STAMP7, add(F7, [0.0, -0.06, -0.15]), add(F7, [0.0, -0.06, -0.15]), L7, L7, lens=48, shake=0.03)])
st.cue('whoosh', 'S07', r(STAMP7 - 0.1), 0.2, 0.15, 600, 2400); st.cue('thud', 'S07', STAMP7, 0.6); st.cue('sfx:punch', 'S07', STAMP7, 0.3); st.cue('sfx:pop', 'S07', r(SW7 + 0.38), 0.25)

# ============================== the factory floor (whiteVoid + chifRoom: concrete, a hazard stripe, steel columns)
ROOM8 = {'w': 20, 'd': 16, 'h': 8, 'wall': '#9AA3AB', 'floor': '#7E8389', 'lights': 4, 'lightY': 7.9, 'stripes': True, 'hazard': True, 'hazardY': 1.6, 'beams': True}
RB8 = [0.0, 0, -3.0]
W8 = [[2.4, 0, -1.6], [-2.2, 0, -1.9]]
# 8: a factory built an unbeatable robot hand. Low, looking up: among welders' sparks the giant arm rises from its pedestal with a stretch, the
#    graphite box mitten closes into a fist with a pop on « robot » and flexes on « imbattable »; two screens on stands loop his fist
D8 = st.dur('S08'); CLOSE8 = r(W('S08', 'L08', 6) - 0.05); FLEX8 = r(W('S08', 'L08', 7))
PATH8 = [{'t': 0.0, 'p': [0, 1.5, 2.6], 'hp': -1.0, 'curl': 0.0}, {'t': 0.25, 'p': [0, 1.6, 2.6], 'hp': -1.0, 'curl': 0.0, 'ease': 'inOut'},
         {'t': r(CLOSE8 - 0.1), 'p': [0.75, 4.9, 2.07], 'hp': 1.0, 'curl': 0.0, 'roll': 0.6, 'st': 1.08, 'ease': 'out'}, {'t': CLOSE8, 'p': [0.75, 4.85, 2.07], 'hp': 1.05, 'curl': 1.0, 'roll': 0.6, 'st': 1.0, 'ease': 'out'},
         {'t': FLEX8, 'p': [0.75, 4.8, 2.1], 'hp': 0.98, 'curl': 1.0, 'roll': 0.6, 'ease': 'inOut'}, {'t': r(FLEX8 + 0.12), 'p': [0.75, 4.92, 2.05], 'hp': 1.1, 'curl': 1.0, 'roll': 0.6, 'ease': 'out'}, {'t': D8, 'p': [0.75, 4.86, 2.07], 'hp': 1.05, 'curl': 1.0, 'roll': 0.6, 'ease': 'inOut'}]
F8 = [2.7, 1.0, 4.4]
F8, L8, LENS8 = FB('S08', F8, {'handTop': tow(RB8, 0, [0, 6.5, 2.4]), 'base': add(RB8, [0, 0, 1.2]), 'w1': add(W8[0], [0, 2.2, 0]), 'w2': add(W8[1], [0, 2.2, 0]), 'w1f': W8[0]}, top=0.12, bottom=0.74)
F8, L8, LENS8 = [2.9, 1.0, 6.0], [0.3, 3.2, -1.2], 56
C8 = cam(0.0, F8, add(F8, [-0.25, 0.1, -0.2]), L8, add(L8, [0, 0.15, 0]), lens=LENS8, ease='inOut')
# (round 2) the two loop screens brought in beside the welders so both show in the frame (they were off the edges)
SCR8 = [[2.05, 0, -0.35, -38], [-1.75, 0, -0.75, 34]]
chkc('S08', C8, {'hand': tow(RB8, 0, [0, 5.5, 2.6]), 'handLow': tow(RB8, 0, [0, 1.5, 3.2]), 'scrA': add(SCR8[0][:3], [0, 1.75, 0]), 'scrB': add(SCR8[1][:3], [0, 1.75, 0]), 'scrAL': add(SCR8[0][:3], [-0.55, 1.75, 0]), 'scrBR': add(SCR8[1][:3], [0.55, 1.75, 0])})
WELD = lambda p, ry, ph: [k(0.0, look=add(RB8, [0, 0.6, 0]), lookDur=0.0), k(0.0, toon={'reach': {'R': R5(off(p, ry, 0.55, 0.0, 0.85), 1, 0.05), 'L': R5(off(p, ry, 0.45, 0.15, 0.95), 1, 0.05)}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.0),
                          *[k(r(ph + 0.35 * i), toon={'reach': {'R': R5(off(p, ry, 0.55, 0.05 * (i % 2), 0.85 + 0.03 * (i % 3)), 1, 0.05), 'L': R5(off(p, ry, 0.45, 0.15, 0.95), 1, 0.05)}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.25) for i in range(7)]]
st.shot('S08', 'whiteVoid', setOpts={'color': '#A9B0B6'}, actors=[act(f'soudeur{i + 1}', p, yaw(p, RB8), 'stand', 'neutral', keys=WELD(p, yaw(p, RB8), 0.1 * i)) for i, p in enumerate(W8)],
        props=[P('usine8', 'chifRoom', pos=[0, 0, 0], opts=ROOM8), P('robot8', 'chifRobot', pos=RB8, opts={'base': 'pedestal', 'path': PATH8, 'hits': [CLOSE8], 'smear': [[r(CLOSE8 - 0.5), r(CLOSE8 - 0.1)]], 'smearKind': 'block', 'smearLag': 0.06}),
               *[P(f'etincelles8_{i}', 'chifSparks', pos=off(p, yaw(p, RB8), 0.62, 0.0, 0.85), opts={'s': 1.0, 'ph': 0.7 * i}) for i, p in enumerate(W8)],
               *[P(f'ecran{n}8', 'chifScreens', pos=sc[:3], ry=sc[3], opts={'stand': True, 'kinds': ['fist'], 'y': 1.4, 'sw': 1.1, 'sh': 0.68}) for n, sc in zip('AB', SCR8)]],
        cams=[C8])
st.cue('engine', 'S08', 0.2, 0.25); st.cue('sfx:static', 'S08', 0.0, 0.12); st.cue('clang', 'S08', CLOSE8, 0.45); st.cue('sfx:rattleShort', 'S08', FLEX8, 0.25)

# 9: on its first try it played rock. Same factory: the arm winds up high (stretched, hanging three frames), then slams its fist down on the steel
#    test table on « pierre » (two-frame smear, the fist squashes, the table crumples, the camera shakes, dust falls from the roof)
D9 = st.dur('S09'); HIT9 = r(W('S09', 'L09', 6) + 0.02)
TT9 = [0.0, 0, 1.0]
# (round 1) the wind-up was a 1.3 s slow lean: now a turn to the table, a coil (links at 80 %, the fist drawn in low behind), a snap up stretched to
#     135 % past the top, four trembling frames of hang, then the slam in three frames (smear, squash)
COIL9 = r(HIT9 - 0.62); UP9 = r(HIT9 - 0.3); HANG9 = r(HIT9 - 0.1)
PATH9 = [{'t': 0.0, 'p': [0.75, 4.6, 2.07], 'hp': 1.05, 'curl': 1.0, 'roll': 0.6}, {'t': r(COIL9 - 0.2), 'p': [0.0, 4.2, 2.2], 'hp': 0.6, 'curl': 1.0, 'roll': 0.0, 'ease': 'inOut'},
         {'t': COIL9, 'p': [0.0, 2.3, 1.0], 'hp': 0.2, 'curl': 1.0, 'st': 0.8, 'ease': 'inOut'}, {'t': r(UP9 - 0.04), 'p': [0.0, 2.2, 0.95], 'hp': 0.15, 'curl': 1.0, 'st': 0.78, 'ease': 'linear'},
         {'t': UP9, 'p': [0.0, 6.5, 1.2], 'hp': 1.25, 'curl': 1.0, 'st': 1.35, 'ease': 'out'}, {'t': r(UP9 + 0.07), 'p': [0.0, 6.2, 1.25], 'hp': 1.15, 'curl': 1.0, 'st': 1.3, 'ease': 'inOut'},
         *[{'t': r(UP9 + 0.07 + 0.033 * (i + 1)), 'p': [0.04 * (-1) ** i, 6.22, 1.25], 'hp': 1.15, 'curl': 1.0, 'st': 1.3, 'ease': 'linear'} for i in range(4)],
         {'t': HIT9, 'p': [0, 1.7, 3.55], 'hp': -0.15, 'curl': 1.0, 'st': 1.05, 'ease': 'in'},
         {'t': r(HIT9 + 0.12), 'p': [0, 1.62, 3.55], 'hp': -0.18, 'curl': 1.0, 'ease': 'out'}, {'t': D9, 'p': [0, 1.66, 3.55], 'hp': -0.16, 'curl': 1.0, 'ease': 'inOut'}]
# (round 2) lower and tighter: the robot fills more of the frame, the table sits in the lower third, the loop screen beside it
F9 = [3.9, 1.3, 7.9]
L9, LENS9 = FC('S09', F9, {'up': tow(RB8, 0, [0, 7.3, 1.2]), 'table': add(TT9, [0.8, 0.0, 0.5]), 'tableL': add(TT9, [-0.8, 0.0, 0.5]), 'scr': [2.0, 2.4, -0.6]}, top=0.07, bottom=0.8, lenses=range(40, 70))
C9 = cam(0.0, F9, add(F9, [-0.15, 0, -0.25]), L9, add(L9, [0, -0.1, 0]), lens=LENS9, ease='inOut')
chkc('S09', C9, {'fistHit': tow(RB8, 0, [0, 1.3, 4.0]), 'tableTop': add(TT9, [0, 1.0, 0]), 'fistUp': tow(RB8, 0, [0, 7.8, 1.6]), 'coil': tow(RB8, 0, [0, 2.3, 1.4])})
st.shot('S09', 'whiteVoid', setOpts={'color': '#A9B0B6'}, actors=[],
        props=[P('usine9', 'chifRoom', pos=[0, 0, 0], opts=ROOM8), P('robot9', 'chifRobot', pos=RB8, opts={'base': 'pedestal', 'path': PATH9, 'hits': [HIT9], 'smear': [[r(UP9 - 0.06), r(UP9 + 0.02)], [r(HIT9 - 0.1), r(HIT9 + 0.01)]]}),
               P('table9', 'chifSteelTable', pos=TT9, opts={'w': 1.6, 'd': 1.0, 'h': 1.0, 'crumpleAt': HIT9, 'dip': 0.45, 'fold': 0.45}),
               P('poussiere9', 'softDust', pos=[0.0, 1.0, 1.0], opts={'at': HIT9, 'n': 12, 'size': 0.9, 'spread': 2.2, 'rise': 0.5, 'life': 1.0, 'color': '#D8D2C4'}),
               P('platre9', 'softDust', pos=[0.5, 6.5, 0.0], opts={'at': r(HIT9 + 0.05), 'n': 10, 'size': 0.8, 'spread': 3.5, 'rise': -2.5, 'life': 1.3, 'color': '#E8E4DA', 'opacity': 0.7}),
               P('ecranA9', 'chifScreens', pos=[2.0, 0, -0.6], ry=-38, opts={'stand': True, 'kinds': ['fist'], 'y': 1.4, 'sw': 1.1, 'sh': 0.68})],
        cams=[C9, cam(HIT9, F9, add(F9, [-0.15, 0, -0.25]), L9, add(L9, [0, -0.1, 0]), lens=LENS9, shake=0.06)])
st.cue('sfx:rattleShort', 'S09', COIL9, 0.25); st.cue('sfx:zip', 'S09', UP9, 0.25); st.cue('sfx:zip', 'S09', r(HIT9 - 0.1), 0.25); st.cue('thunder', 'S09', HIT9, 0.5); st.cue('sfx:crunch', 'S09', HIT9, 0.5)

# 9b: the factory lost two storeys. Outside, wide: the box factory with its rows of windows slides two storeys down into the ground with a jolt on
#    « perdu », a ring of dust rolling out along the grass; then closer: two workers in white hard hats lean out of two windows now at ground level,
#    dusty, unhurt, and cough a puff of dust
D9b = st.dur('S09b'); SINK9 = r(W('S09b', 'L09', 9) - 0.12); FH = 3.2
FAC = [0.0, 0, -14.0]; FBW, FBD = 16.0, 10.0
OPEN9 = [[2, 3], [2, 4]]
def WINX(c): return r(-FBW / 2 + (c + 0.5) * FBW / math.floor(FBW / 2.2))
WK = [[r(FAC[0] + WINX(c)), 0.04, r(FAC[2] + FBD / 2 + 0.24)] for f, c in OPEN9]
# (round 1) the workers' cut comes 0.5 s after the drop (0.47 s on screen before), so they get 0.9 s
SEEN9 = r(SINK9 + 0.5)
F9bA = [10.0, 2.2, 14.0]
F9bA, L9bA, LENS9bA = FB('S09b', F9bA, {'roof': add(FAC, [-FBW / 2, 4 * FH + 0.5, FBD / 2]), 'roofR': add(FAC, [FBW / 2, 4 * FH + 0.5, -FBD / 2]), 'footL': add(FAC, [-FBW / 2, 0, FBD / 2]), 'footR': add(FAC, [FBW / 2, 0, FBD / 2])}, top=0.14, bottom=0.72, lenses=range(30, 57))
# (round 1) wide enough for the whole building and the sky over it, so the two lost storeys read as sky
F9bA, L9bA, LENS9bA = [13.5, 1.8, 19.5], add(FAC, [0.6, 7.2, 1.0]), 54
C9bA = cam(0.0, F9bA, add(F9bA, [-0.25, 0, -0.2]), L9bA, L9bA, lens=LENS9bA)
chkc('S09b', C9bA, {'roofL': add(FAC, [-FBW / 2, 4 * FH + 0.5, FBD / 2]), 'roofR': add(FAC, [FBW / 2, 4 * FH + 0.5, -FBD / 2]), 'chimney': add(FAC, [FBW * 0.3, 4 * FH + 7, -FBD * 0.2]), 'footL': add(FAC, [-FBW / 2, 0, FBD / 2]), 'footR': add(FAC, [FBW / 2, 0, FBD / 2])})
F9bB = [r((WK[0][0] + WK[1][0]) / 2 + 0.4), 1.75, WK[0][2] + 6.3]
L9bB = [r((WK[0][0] + WK[1][0]) / 2), 1.3, WK[0][2]]
C9bB = cam(r(SEEN9 - 0.05), F9bB, add(F9bB, [-0.1, 0, -0.3]), add(L9bB, [0, 0.45, 0]), add(L9bB, [0, 0.45, 0]), lens=52)
chkc('S09b', C9bB, {'w1': add(WK[0], [0, 2.15, 0.6]), 'w2': add(WK[1], [0, 2.15, 0.6]), 'win1': [WK[0][0], 1.76, FAC[2] + FBD / 2], 'win2': [WK[1][0], 1.76, FAC[2] + FBD / 2]})
COUGH = {'lid': 0.6, 'mouth': 'O', 'jaw': 0.3, 'brow': 0.5, 'puff': 0.6}
# (round 1) they pop out of the windows (lean in two frames), a soot puff bursts round each head, and each coughs twice, jerking forward
def WORKER(i):
    t0 = r(SEEN9 + 0.06 * i)
    BASE = lambda sp, nk: {'bend': {'spine': [sp, 0, 0, 1, None], 'neck': [nk, 0, 0, 1, None]}, 'reach': {'R': R5(off(WK[i], 0, 0.45, 0.42, 1.18), 1, 0.05), 'L': R5(off(WK[i], 0, 0.45, -0.42, 1.18), 1, 0.05)}, 'hip': 0}
    ks = [k(0.0, visible=False), k(t0, visible=True), k(0.0, look='camera', lookDur=0.0),
          k(t0, toon={**BASE(0.3, -0.25), 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'o', 'brow': 0.8}}, toonDur=0.07, toonEase='out')]
    for j, c in enumerate([0.24, 0.5]):
        tc = r(t0 + c + 0.05 * i)
        ks += [k(r(tc - 0.05), toon={**BASE(0.15, -0.35), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.5, 'mouth': 'o', 'brow': 0.3, 'puff': 0.8}}, toonDur=0.05),
               k(tc, toon={**BASE(0.55, 0.2), 'sq': [1.07, 0.92, 1.07], 'face': COUGH}, toonDur=0.04, toonEase='out'),
               k(r(tc + 0.12), toon={**BASE(0.32, -0.2), 'face': {'lid': 0.55, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.1)]
    return ks
st.shot('S09b', 'grassland', setOpts=GRASS, actors=[act(f'ouvrier{i + 1}', WK[i], 0, 'stand', 'neutral', keys=WORKER(i)) for i in range(2)],
        props=[P('usineX9', 'chifFactoryBox', pos=FAC, opts={'w': FBW, 'd': FBD, 'floors': 4, 'fh': FH, 'sinkAt': SINK9, 'sinkDur': 0.22, 'sinkPow': 2.2, 'squash': 0.13, 'ghost': 0.42, 'dustK': 0.55, 'dustH': 0.45, 'dustS': 0.7, 'sinkFloors': 2, 'open': OPEN9, 'fill': 2.6}),
               *[P(f'suie9_{i}', 'softDust', pos=off(WK[i], 0, 0.5, 0, 1.95), opts={'at': r(SEEN9 + 0.02 + 0.06 * i), 'n': 7, 'size': 0.45, 'spread': 0.55, 'rise': 0.4, 'life': 0.55, 'color': '#4E4A46', 'opacity': 0.85}) for i in range(2)],
               *[P(f'toux9_{i}_{j}', 'softDust', pos=off(WK[i], 0, 0.75, 0, 1.75), opts={'at': r(SEEN9 + c + 0.05 * i), 'n': 4, 'size': 0.28, 'spread': 0.3, 'rise': 0.25, 'life': 0.45, 'color': '#6A645C', 'opacity': 0.8}) for i in range(2) for j, c in enumerate([0.24, 0.5])]],
        cams=[C9bA, C9bB])
st.cue('thunder', 'S09b', SINK9, 0.55); st.cue('sfx:crunch', 'S09b', r(SINK9 + 0.22), 0.4); st.cue('sfx:poof', 'S09b', r(SEEN9 + 0.02), 0.25); st.cue('sfx:poof', 'S09b', r(SEEN9 + 0.24), 0.18); st.cue('sfx:poof', 'S09b', r(SEEN9 + 0.5), 0.18)

# ============================== his street (pavillon without its house + chifHouse: the front at z -3.6, the door at x -1.2)
STREET = {'house': False, 'mailbox': False, 'fence': False}
HOUSE = [0.0, 0, -6.6]
RBT10 = [-5.0, 0, -4.3]                                                  # the robot beside the house, its arm running along the facade behind them
# (round 2) the fist held out level toward the right, its folded front (crease and wrapped thumb) turned three-quarters to us; the bib goes on the
#     side of the forearm (on the back of the hand it made the fist read as a monitor); the man stands right under the fist, the official beside
#     him, the ladder and the president at its wrist; a closer second camera for the medal
HANDW10 = [-2.0, 2.85, -3.0]
RYB10 = yaw(RBT10, HANDW10)
HM10 = [-0.75, 0, -2.4]; OFC10 = [-1.55, 0, -2.0]; OFC10B = [0.2, 0, -2.95]; LAD10 = [-2.6, 0, -2.55]; LADH10 = 0.7; PRS10 = [-2.6, r(LADH10 + 0.03), -2.55]
ROLL10 = -1.3; HP10 = 0.22
PATH10 = [{'t': 0.0, 'p': tol(RBT10, RYB10, HANDW10), 'hp': HP10, 'curl': 1.0, 'roll': ROLL10}, {'t': 1.0, 'p': tol(RBT10, RYB10, add(HANDW10, [0, 0.05, 0])), 'hp': r(HP10 + 0.03), 'curl': 1.0, 'roll': ROLL10, 'ease': 'inOut'},
          {'t': 2.0, 'p': tol(RBT10, RYB10, add(HANDW10, [0, -0.03, 0])), 'hp': r(HP10 - 0.02), 'curl': 1.0, 'roll': ROLL10, 'ease': 'inOut'}, {'t': 3.65, 'p': tol(RBT10, RYB10, add(HANDW10, [0, 0.04, 0])), 'hp': HP10, 'curl': 1.0, 'roll': ROLL10, 'ease': 'inOut'}]
FD10 = fwd(RYB10)
def robot_fore(base, ry, wrist, f, side=-1, st=1.0, hS=2.07):
    # a point on the side of chifRobot's forearm, f along it from the elbow (the prop's two-bone solve, elbow up, the turret facing the wrist)
    lp = tol(base, ry, wrist); rho, v = math.hypot(lp[0], lp[2]), lp[1] - hS; l1, l2 = 3.0 * st, 2.6 * st; d = min(max(math.hypot(rho, v), abs(l1 - l2) + 0.05), l1 + l2 - 0.02)
    a = math.atan2(v, rho); al = math.acos(max(-1, min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))); e = [l1 * math.cos(a + al), l1 * math.sin(a + al)]; w = [d * math.cos(a), d * math.sin(a)]
    q = [e[0] + (w[0] - e[0]) * f, e[1] + (w[1] - e[1]) * f]; yw = math.atan2(lp[0], lp[2])
    loc = [q[0] * math.sin(yw) + side * 0.25 * math.cos(yw), hS + q[1], q[0] * math.cos(yw) - side * 0.25 * math.sin(yw)]
    return tow(base, ry, loc)
BIBF10 = 0.6
BIBH = robot_fore(RBT10, RYB10, HANDW10, BIBF10)                                    # the bib on the front side of the forearm
FIST10 = [r(HANDW10[0] + FD10[0] * 0.7), r(HANDW10[1] + 0.1), r(HANDW10[2] + FD10[2] * 0.7)]
# 10: the olympic committee selected it; the president decorated it in advance. At his door, the robot's fist held out over him: an official in a
#     plain blazer unpins the blank bib from his chest and pins it on the robot's forearm, the man's eyes following it, then his shoulders sag;
#     closer: the president on a low stepladder rises on tiptoe, stretching up, pins a big plain medal on its wrist on « décorée » and pats it twice;
#     beside the door the bags reach the first-floor window
D10 = st.dur('S10'); MED10 = r(W('S10', 'L10', 8) - 0.04); CUT10 = r(W('S10', 'L10', 5) - 0.1)
UNPIN10, PIN10 = 0.45, 1.25
HEAP10 = [2.15, 0, -3.0]
F10A = [0.9, 1.75, 4.6]
L10A, LENS10A = FC('S10', F10A, {'him': add(HM10, [0, 2.3, 0]), 'himF': add(HM10, [0, 0.3, 0]), 'fist': add(FIST10, [0.4, 0.6, 0]), 'wrist': add(HANDW10, [-0.5, 0.5, 0]), 'of': add(OFC10, [-0.3, 2.3, 0]), 'heap': add(HEAP10, [-1.2, 3.6, 0])}, top=0.12, bottom=0.74)
C10A = cam(0.0, F10A, add(F10A, [-0.05, 0.03, -0.25]), L10A, add(L10A, [0, 0.03, 0]), lens=LENS10A)
F10B = [0.5, 2.35, 3.2]
L10B, LENS10B = FC('S10', F10B, {'fistTop': add(FIST10, [0.3, 0.55, 0]), 'medalLow': add(HANDW10, [0, -1.55, 0.3]), 'pres': add(PRS10, [-0.6, 2.65, 0]), 'presF': add(PRS10, [-0.5, 0.6, 0]), 'him': add(HM10, [0.3, 2.3, 0]), 'himM': add(HM10, [0.3, 1.2, 0])}, top=0.14, bottom=0.74, margin=0.05)
C10B = cam(CUT10, F10B, add(F10B, [0.05, 0.0, -0.3]), L10B, add(L10B, [0.0, 0.02, 0]), lens=LENS10B, ease='inOut')
chkc('S10', C10A, {'bibChest': add(HM10, [0, 1.45, 0.15]), 'bibArm': BIBH, 'fist': FIST10, 'him': add(HM10, [0, 2.3, 0]), 'himF': HM10, 'heapTop': add(HEAP10, [0, 4.6, 0])})
chkc('S10', C10B, {'wrist': HANDW10, 'fist': FIST10, 'bibArm': BIBH, 'medal': add(HANDW10, [0, -1.0, 0.4]), 'pres': add(PRS10, [0, 2.35, 0]), 'him': add(HM10, [0, 2.3, 0]), 'ladF': LAD10}, end=True)
BIBPATH = [add(HM10, [0.0, 1.42, 0.2]), add(HM10, [-0.45, 1.95, 0.25]), BIBH]
OFF10 = {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}
OFK10 = [k(CUT10, to=OFC10B, dur=0.01), k(CUT10, toon={'face': {**OFF10, 'mouth': 'smile'}, 'reach': {'R': R5(off(OFC10B, 20, 0.1, 0.28, 0.95), 1, 0.05)}}, toonDur=0.0), k(0.0, look=BIBPATH[0], lookDur=0.0), k(0.0, toon={'face': OFF10, 'reach': {'R': R5(off(OFC10, 20, 0.2, 0.2, 1.0), 0.0, 0.05)}}, toonDur=0.0),
         k(0.15, toon={'face': OFF10, 'reach': {'R': R5(BIBPATH[0], 1, 0.06)}}, toonDur=0.3, toonEase='inOut'),
         k(UNPIN10, toon={'face': OFF10, 'reach': {'R': R5(BIBPATH[1], 1, 0.06)}}, toonDur=0.35, toonEase='inOut'), k(r(UNPIN10 + 0.2), look=BIBH, lookDur=0.2),
         k(r(UNPIN10 + 0.35), toon={'face': OFF10, 'reach': {'R': R5(BIBPATH[2], 1, 0.06)}, 'sq': [0.95, 1.07, 0.95]}, toonDur=r(PIN10 - UNPIN10 - 0.35), toonEase='inOut'),
         k(PIN10, toon={'face': OFF10, 'reach': {'R': R5(add(BIBPATH[2], [0, -0.06, 0.04]), 1, 0.06)}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.06),
         k(r(PIN10 + 0.15), toon={'face': {**OFF10, 'mouth': 'smile'}, 'reach': {'R': R5(off(OFC10, 20, 0.1, 0.28, 0.95), 1, 0.05)}}, toonDur=0.35, toonEase='inOut'), k(r(PIN10 + 0.3), look='camera', lookDur=0.2),
         k(CUT10, toon={'face': {**OFF10, 'mouth': 'smile'}, 'reach': {'R': R5(off(OFC10B, 20, 0.1, 0.28, 0.95), 1, 0.05)}}, toonDur=0.0),
         *life(r(PIN10 + 0.6), D10, {**OFF10, 'mouth': 'smile'}, blinks=[2.2, 3.3]), k(r(MED10 + 0.1), look=add(HANDW10, [0, -0.8, 0.3]), lookDur=0.2)]
BIBK = [k(0.0, visible=False), k(UNPIN10, visible=True), k(UNPIN10, to=BIBPATH[1], dur=0.35, ease='inOut'), k(r(UNPIN10 + 0.35), to=BIBPATH[2], dur=r(PIN10 - UNPIN10 - 0.35), ease='inOut'), k(PIN10, visible=False)]
PRF = {'lid': 0.25, 'mouth': 'smile', 'brow': 0.4}
# the president: medal in hand at his chest, then on tiptoe, stretched up (squash and stretch of the whole rig) to the wrist; pin, two pats, down
WRIST10 = add(HANDW10, [-0.05, -0.12, 0.3]); MEDH10 = off(PRS10, 80, 0.35, 0.15, 1.35)
PRREST = lambda: {'L': R5(off(PRS10, 80, 0.25, -0.3, 1.05), 0.6, 0.05)}
PRK10 = [k(0.0, look=WRIST10, lookDur=0.0), k(0.0, toon={'face': PRF, 'reach': {**PRREST(), 'R': R5(MEDH10, 1, 0.05)}}, toonDur=0.0), *blink(0.9, PRF),
         k(r(CUT10 + 0.1), toon={'face': PRF, 'reach': {**PRREST(), 'R': R5(add(MEDH10, [0, -0.08, 0]), 1, 0.05)}, 'sq': [1.06, 0.93, 1.06]}, toonDur=0.15),
         k(r(MED10 - 0.42), toon={'face': {**PRF, 'brow': 0.7}, 'reach': {**PRREST(), 'R': R5(add(WRIST10, [0, 0.05, 0]), 1, 0.06)}, 'sq': [0.86, 1.2, 0.86], 'bend': {'spine': [-0.12, 0, 0, 1, None]}}, toonDur=0.38, toonEase='inOut'),
         k(MED10, toon={'face': {**PRF, 'mouth': 'O', 'brow': 0.8}, 'reach': {**PRREST(), 'R': R5(WRIST10, 1, 0.06)}, 'sq': [0.84, 1.22, 0.84], 'bend': {'spine': [-0.14, 0, 0, 1, None]}}, toonDur=0.05),
         k(r(MED10 + 0.16), toon={'face': PRF, 'reach': {**PRREST(), 'R': R5(add(WRIST10, [0.25, 0.18, 0.05]), 1, 0.06)}, 'sq': [0.88, 1.17, 0.88]}, toonDur=0.07),
         k(r(MED10 + 0.24), toon={'face': PRF, 'reach': {**PRREST(), 'R': R5(add(WRIST10, [0.25, 0.04, 0.05]), 1, 0.06)}, 'sq': [0.9, 1.14, 0.9]}, toonDur=0.05),
         k(r(MED10 + 0.33), toon={'face': PRF, 'reach': {**PRREST(), 'R': R5(add(WRIST10, [0.25, 0.2, 0.05]), 1, 0.06)}, 'sq': [0.88, 1.17, 0.88]}, toonDur=0.07),
         k(r(MED10 + 0.41), toon={'face': PRF, 'reach': {**PRREST(), 'R': R5(add(WRIST10, [0.25, 0.05, 0.05]), 1, 0.06)}, 'sq': [0.9, 1.14, 0.9]}, toonDur=0.05),
         k(r(MED10 + 0.55), toon={'face': {**PRF, 'mouth': 'smile', 'brow': 0.6}, 'reach': {**PRREST(), 'R': R5(off(PRS10, 80, 0.3, 0.25, 1.0), 0.3, 0.05)}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.2, toonEase='out'),
         k(r(MED10 + 0.75), toon={'face': {**PRF, 'mouth': 'smile', 'brow': 0.6}, 'sq': [1, 1, 1]}, toonDur=0.15, keepPose=True), k(r(MED10 + 0.6), look='camera', lookDur=0.2)]
MEDK10 = [k(0.0, visible=False), k(CUT10, visible=True), k(r(MED10 - 0.42), to=add(WRIST10, [0, 0.05, 0]), dur=0.38, ease='inOut'), k(MED10, visible=False)]
# the man: his eyes follow his bib from his chest up to the forearm, then his shoulders sag (squash, spine and neck bent) and stay down
SADF = {'lid': 0.6, 'mouth': 'line', 'brow': 0.6, 'gy': 0.3}
SAG10 = {'sq': [1.05, 0.92, 1.05], 'bend': {'spine': [0.16, 0, 0, 1, None], 'neck': [0.18, 0, 0, 1, None]}, 'face': SADF}
HEROK10 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0), k(0.2, look=BIBPATH[0], lookDur=0.15),
           k(UNPIN10, look=BIBPATH[1], lookDur=0.35), k(r(UNPIN10 + 0.35), look=BIBH, lookDur=r(PIN10 - UNPIN10 - 0.35)),
           k(r(PIN10 + 0.12), toon={**SAG10, 'sq': [1.08, 0.88, 1.08]}, toonDur=0.25, toonEase='out'), k(r(PIN10 + 0.4), toon=SAG10, toonDur=0.2),
           *life(r(PIN10 + 0.7), D10, SADF, blinks=[2.05, 3.2], amp=0.01), k(r(MED10 + 0.05), look=add(HANDW10, [0, -0.8, 0.3]), lookDur=0.25)]
st.shot('S10', 'pavillon', setOpts=STREET, actors=[act('mec', HM10, 8, 'stand', 'neutral', keys=HEROK10), act('officiel10', OFC10, 20, 'stand', 'neutral', keys=OFK10),
        act('president', PRS10, 80, 'stand', 'neutral', keys=PRK10)],
        props=[P('maison10', 'chifHouse', pos=HOUSE), P('ciel10', 'noClouds', pos=[0, 0, 0]), P('sacs10', 'chifBagHeap', pos=HEAP10, opts={'h': 4.6, 'r': 1.35, 'bag': 0.62, 'flies': 6, 'flyS': 0.9}),
               P('robot10', 'chifRobot', pos=RBT10, ry=RYB10, opts={'base': 'tracks', 'path': PATH10, 'bibAt': PIN10, 'bibFore': BIBF10, 'bibSide': -1, 'medalAt': MED10, 'medalS': 2.0, 'medalYaw': math.radians(yaw(HANDW10, F10B) - RYB10)}),
               P('dossardH10', 'chifBib', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.32, 0.15]}, keys=[k(UNPIN10, visible=False)]),
               P('dossardV10', 'chifBib', pos=BIBPATH[0], ry=12, keys=BIBK, opts={'w': 0.34, 'h': 0.27}), P('escabeau10', 'chifStepladder', pos=LAD10, ry=80, opts={'h': LADH10}),
               P('medaille10', 'chifMedal', pos=MEDH10, ry=r(yaw(MEDH10, F10B), 1), keys=MEDK10, opts={'s': 4.5})],
        cams=[C10A, C10B])
st.cue('sfx:paper', 'S10', UNPIN10, 0.2); st.cue('sfx:click', 'S10', PIN10, 0.3); st.cue('sfx:fanfare', 'S10', r(MED10 + 0.05), 0.2); st.cue('sfx:clink', 'S10', MED10, 0.3)
st.cue('sfx:stepSoft', 'S10', r(MED10 + 0.24), 0.15); st.cue('sfx:stepSoft', 'S10', r(MED10 + 0.41), 0.15)

# ============================== the final (the stadium again: the wife at the table, the robot on tracks facing her across it)
FM = [-1.0, 0, 0.0]; RYFM = 42
RBS = [3.4, 0, -0.3]; RYRS = -90
HEAP11 = [6.0, 0, -70.0]
UP11 = [0.6, 3.6, -0.1]                                                   # the fist towering over the table
def RS(p): return tol(RBS, RYRS, p)
# 11: eighty thousand spectators; national anthem. Low and wide from the pitch: the crowd sits cheering, then stands on « Hymne », right hands on
#     hearts (an invented anthem: a choir and a fanfare, no flags anywhere); on the centre spot the wife in her apron faces the towering fist across
#     the little table; behind the far rim a mountain of bin bags circled by seagulls; the scoreboard reads FINALE / ELLE – LA MAIN
D11 = st.dur('S11'); HYMN11 = r(W('S11', 'L11', 3) - 0.1)
# (round 1) the wide keeps the robot's base in and the scoreboard raised clear above the arm, the heap to the right; then a cut-in on the wife (she
#     was 5 % of the frame) across the table from the towering fist, the stands behind her rising as a wave on « Hymne », hands then to hearts
CUT11 = 1.25
F11, L11, LENS11 = [5.0, 1.3, 12.5], [-1.5, 6.5, -12.0], 56
C11 = cam(0.0, F11, add(F11, [-0.25, 0.1, -0.5]), L11, add(L11, [0, 0.3, 0]), lens=LENS11, ease='inOut')
chkc('S11', C11, {'robotBaseR': add(RBS, [1.5, 0, 0]), 'robotBaseL': add(RBS, [0, 0, 1.5]), 'table': TBL, 'wife': add(FM, [0, 2.2, 0]), 'fist': UP11, 'elbow': [2.4, 5.4, -0.2], 'boardTL': [-18, 29.5, -40.7], 'boardBR': [-2, 23.5, -40.7], 'heapTop': add(HEAP11, [0, 46, 0])})
F11B, L11B = [3.5, 1.3, 6.0], [-0.3, 2.3, -0.1]
C11B = cam(CUT11, F11B, add(F11B, [-0.2, 0.05, -0.3]), L11B, add(L11B, [0, 0.05, 0]), lens=56, ease='inOut')
chkc('S11', C11B, {'wifeH': add(FM, [0, 2.3, 0]), 'wifeF': add(FM, [0, 0.3, 0]), 'fist': UP11, 'fistTop': add(UP11, [0, 0.7, 0]), 'table': [0, 0.76, 0], 'standsBack': [-25, 6, -14]})
PATH11 = [{'t': 0.0, 'p': RS(UP11), 'hp': -0.25, 'curl': 1.0}, {'t': 1.2, 'p': RS(add(UP11, [0, 0.12, 0])), 'hp': -0.2, 'curl': 1.0, 'ease': 'inOut'}, {'t': D11, 'p': RS(add(UP11, [0, -0.05, 0])), 'hp': -0.27, 'curl': 1.0, 'ease': 'inOut'}]
WIFEF = {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}
st.shot('S11', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFM, 'stand', 'neutral', keys=[k(0.0, look=UP11, lookDur=0.0), k(0.0, toon={'face': WIFEF}, toonDur=0.0), *life(0.1, D11, WIFEF, blinks=[1.0, 2.35], amp=0.03, period=0.8),
                                                                    k(1.6, look=[-6, 4, -14], lookDur=0.25), k(2.1, look=UP11, lookDur=0.2)])],
        props=[P('stade11', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.9, 'boardUp': 9, 'boardHide': [[CUT11, 99]], 'standAt': HYMN11, 'standWave': 0.7, 'standH': 1.65, 'heartAt': r(HYMN11 + 0.5)}), *PITCH_TABLE(11), APRON('tablier11', 'femme'),
               P('montagne11', 'chifBagHeap', pos=HEAP11, opts={'h': 46, 'r': 30, 'bag': 3.2, 'gulls': 9, 'gullS': 4.0, 'gullR': 20, 'gullH': 6}),
               P('robot11', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH11})],
        cams=[C11, C11B])
st.cue('rain', 'S11', 0.0, 0.14, HYMN11); st.cue('sfx:fanfare', 'S11', HYMN11, 0.35); st.cue('sfx:choir', 'S11', r(HYMN11 + 0.3), 0.4)

# 12: chi, fou, mi: the stadium split in two. Low: the arm pumps its fist three times, on chi, fou and mi, the ground jumping on each beat (the table
#     hops, dust puffs); cut to the air: on « mi » a crack runs across the pitch past the table, a round hole opens beside it, and the two halves of
#     the stadium slide apart on « s'est fendu », both crowds still cheering
D12 = st.dur('S12'); B12 = [W('S12', 'L12', 0), W('S12', 'L12', 1), W('S12', 'L12', 2)]; SPLIT12 = r(W('S12', 'L12', 5) - 0.1)
CUT12 = r(B12[2] + 0.28)
PATH12 = [{'t': 0.0, 'p': RS(UP11), 'hp': -0.25, 'curl': 1.0}]
for b in B12: PATH12 += [{'t': r(b - 0.2), 'p': RS(add(UP11, [0, 0.7, 0])), 'hp': -0.05, 'curl': 1.0, 'ease': 'out', 'st': 1.05}, {'t': b, 'p': RS(add(UP11, [0, -0.35, 0])), 'hp': -0.4, 'curl': 1.0, 'ease': 'in'}]
PATH12 += [{'t': r(B12[2] + 0.25), 'p': RS(UP11), 'hp': -0.25, 'curl': 1.0, 'ease': 'out'}, {'t': D12, 'p': RS(add(UP11, [0, 0.1, 0])), 'hp': -0.25, 'curl': 1.0, 'ease': 'inOut'}]
# (round 2) the low shot closer on her and the table: each beat the table hops 0.3 m and tips, the chairs jump, her apron flaps and she bobs;
#     the aerial starts low over the table (the crack runs past it, the hole pops as a dark circle beside it), then cranes up and back as the two
#     halves lurch apart, overshoot and settle 8 m out each (dust lines puff along the crack)
F12A, L12A, LENS12A = [-2.2, 1.6, 6.2], [-0.1, 2.1, -0.3], 56
C12A = cam(0.0, F12A, F12A, L12A, L12A, lens=LENS12A)
chkc('S12', C12A, {'fistUp': add(UP11, [0.4, 1.5, 0]), 'fistLow': add(UP11, [0, -0.35, 0]), 'table': [0, 0.76, 0], 'tableHop': [0, 1.06, 0], 'wife': add(FM, [0, 2.2, 0]), 'wifeF': FM, 'apron': add(FM, [0, 0.6, 0]), 'base': RBS})
F12L, L12L = [0.4, 15.0, 10.5], [-0.25, 0.0, 0.45]
C12B = cam(CUT12, F12L, add(F12L, [0, 1.0, 0.7]), L12L, L12L, lens=50)
chkc('S12', C12B, {'table': TBL, 'hole': [STAD['hole'][0], 0, STAD['hole'][1]], 'holeL': [STAD['hole'][0] - 0.75, 0, STAD['hole'][1]], 'holeR': [STAD['hole'][0] + 0.75, 0, STAD['hole'][1]], 'wife': FM, 'robot': RBS})
F12B, T12B = [0.0, 62.0, 46.0], [0.0, 70.0, 52.0]
RISE12 = r(SPLIT12 - 0.08)
C12C = glide([cam(RISE12, F12B, T12B, [0.0, 0, -3.0], [0.0, 0, -3.0], lens=58)], 0.6)
chkc('S12', C12C, {'table': TBL, 'standsN': [0, 9, -38], 'standsS': [0, 9, 38], 'endW': [-45, 9, 0], 'endE': [45, 9, 0], 'gapNL': [-SPL12E, 2, -36], 'gapNR': [SPL12E, 2, -36], 'gapSL': [-SPL12E, 2, 36], 'gapSR': [SPL12E, 2, 36]}, end=True)
SPLITK12 = [[SPLIT12, 0], [r(SPLIT12 + 0.1), 2.6], [r(SPLIT12 + 0.2), 2.2], [r(SPLIT12 + 0.52), r(SPL12E * 1.22, 2)], [r(SPLIT12 + 0.7), r(SPL12E * 0.93, 2)], [r(SPLIT12 + 0.86), r(SPL12E * 1.03, 2)], [r(SPLIT12 + 0.98), SPL12E]]
TBLK12 = []
for i, b in enumerate(B12):
    TBLK12 += [k(b, to=[0, 0.3, 0], dur=0.07, ease='out'), k(b, rotTo=[0.0, 0.0, 0.14 * (-1) ** i], dur=0.07), k(r(b + 0.1), to=[0, 0, 0], dur=0.1, ease='in'), k(r(b + 0.1), rotTo=[0, 0, 0], dur=0.1)]
CHK12 = lambda x: [kk for i, b in enumerate(B12) for kk in (k(r(b + 0.01), to=[x, 0.18, 0.0], dur=0.06, ease='out'), k(r(b + 0.1), to=[x, 0, 0.0], dur=0.09, ease='in'))]
WIFEK12 = [k(0.0, look=UP11, lookDur=0.0), k(0.0, toon={'face': WIFEF}, toonDur=0.0)]
for b in B12:
    WIFEK12 += [k(b, toon={'sq': [1.1, 0.88, 1.1], 'face': {**WIFEF, 'lid': 0.7, 'brow': 0.3}}, toonDur=0.03, keepPose=True), k(r(b + 0.07), toon={'sq': [0.95, 1.07, 0.95], 'face': {**WIFEF, 'lid': 0.2}}, toonDur=0.07, keepPose=True),
                k(r(b + 0.18), toon={'sq': [1, 1, 1], 'face': WIFEF}, toonDur=0.12, keepPose=True)]
WIFEK12 += blink(0.4, WIFEF) + blink(1.0, WIFEF)
st.shot('S12', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFM, 'stand', 'neutral', keys=WIFEK12)],
        props=[P('stade12', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 1.0, 'standAt': -1, 'jumps': B12, 'crackAt': r(B12[2] + 0.3), 'crackDur': 0.5, 'holeAt': r(B12[2] + 0.62), 'split': SPLITK12,
                                                                'crackW': 0.9, 'dustAt': [SPLIT12], 'dustS': 1.3}),
               *PITCH_TABLE(12, keys=TBLK12, chairKeys=CHK12), APRON('tablier12', 'femme', flaps=B12, flapAmp=0.75),
               P('robot12', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH12, 'hits': B12}),
               *[P(f'boum12_{i}', 'softDust', pos=[0.0, 0.05, 0.0], opts={'at': b, 'n': 10, 'size': 0.7, 'spread': 2.4, 'rise': 0.4, 'life': 0.6, 'color': '#C9BFA8', 'opacity': 0.65}) for i, b in enumerate(B12)]],
        cams=[C12A, *[cam(b, F12A, F12A, L12A, L12A, lens=LENS12A, shake=0.05) for b in B12[:2]], C12B, C12C])
for b in B12: st.cue('thud', 'S12', b, 0.55)
st.cue('thunder', 'S12', r(B12[2] + 0.3), 0.5); st.cue('sfx:crunch', 'S12', SPLIT12, 0.45); st.cue('rain', 'S12', CUT12, 0.16, r(D12 - CUT12))

# 13: the hand played rock. Low and close by the table, looking up: the fist hangs high a beat, trembling, then comes down (smear) and stops above
#     the table with a squash: a clean dark fist silhouette against the sky
D13 = st.dur('S13'); ROCK13 = r(W('S13', 'L13', 4) - 0.04)
HIGH13 = [0.45, 5.3, -0.1]; LOW13 = [0.2, 2.9, -0.05]
PATH13 = [{'t': 0.0, 'p': RS(HIGH13), 'hp': -0.6, 'curl': 1.0, 'st': 1.1}, {'t': r(ROCK13 - 0.28), 'p': RS(add(HIGH13, [0, 0.15, 0])), 'hp': -0.55, 'curl': 1.0, 'st': 1.12, 'ease': 'out'},
          {'t': ROCK13, 'p': RS(LOW13), 'hp': -0.75, 'curl': 1.0, 'st': 1.0, 'ease': 'in'}, {'t': r(ROCK13 + 0.12), 'p': RS(add(LOW13, [0, 0.1, 0])), 'hp': -0.72, 'curl': 1.0, 'ease': 'out'},
          {'t': D13, 'p': RS(add(LOW13, [0, 0.06, 0])), 'hp': -0.74, 'curl': 1.0, 'ease': 'inOut'}]
F13 = [-0.6, 0.7, 3.3]
_u, _v, _w = FB('S13', F13, {'fistLow': add(LOW13, [-0.5, -0.5, 0]), 'fistLowR': add(LOW13, [0.7, 0.4, 0]), 'fistHigh': add(HIGH13, [-0.3, 0.6, 0]), 'tableTop': [0.0, 0.76, 0.0]}, top=0.12, bottom=0.74)
L13, LENS13 = [0.45, 3.0, -0.2], 56
C13 = cam(0.0, F13, add(F13, [0.1, -0.03, -0.12]), L13, L13, lens=LENS13)
st.shot('S13', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFM, 'stand', 'neutral', keys=[k(0.0, look=LOW13, lookDur=0.0), k(0.0, toon={'face': WIFEF}, toonDur=0.0)])],
        props=[P('stade13', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.8, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'crackW': 0.12, 'split': [[0, SPL12E]]}), *PITCH_TABLE(13), APRON('tablier13', 'femme'),
               P('robot13', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH13, 'hits': [ROCK13], 'smear': [[r(ROCK13 - 0.12), r(ROCK13 + 0.01)]]})],
        cams=[C13, cam(ROCK13, F13, add(F13, [0.1, -0.03, -0.12]), L13, L13, lens=LENS13, shake=0.03)])
st.cue('whoosh', 'S13', r(ROCK13 - 0.14), 0.3, 0.2, 300, 1500); st.cue('clang', 'S13', ROCK13, 0.35)

# 14: his wife played well. Close: she holds out her closed fist (a rock fake-out), her face behind it; cut higher on « fait »: she raises it and
#     on the first syllable of « puits » it pops open into a curled mitten ring past its size, while a stone rim rises round the hole beside the
#     table; the robot fist cocks, arcs down, overshoots the table and plunges into the well, its arm stretching down into the rim; a hang of three
#     frames, then a crown of drops rises out of the well and falls back (PERDU after the splash, her head under the card)
D14 = st.dur('S14'); WELL14 = r(W('S14', 'L14', 4) - 0.01); FAIT14 = W('S14', 'L14', 3)
# (round 2) the high angle holds 0.64 s (it held 0.1 s): the cut moves up to « fait », so the ring pops in the high angle with her hand big and
#     clear of her head; the plunge is in the open beside the table, not behind her head; the splash is a crown of drops, not a column
CUTA14 = r(FAIT14 + 0.08)
HOLE = STAD['hole']; HW = [HOLE[0], 0, HOLE[1]]
RIM14 = r(WELL14 + 0.01); COCK14 = r(WELL14 + 0.05); PASS14 = r(COCK14 + 0.045); RIMT14 = r(PASS14 + 0.03); DEEP14 = r(RIMT14 + 0.035)
SPL14 = r(DEEP14 + 0.085); REC14 = r(SPL14 + 0.07); CARD14 = r(SPL14 + 0.08)
# the arm into the well: an L, the upper arm stretched level over the table, the forearm straight down into the rim (both links 1.45 times)
DEEPW14 = [HOLE[0], -0.8, HOLE[1]]
RYFW = 50
EWC14 = off(FM, RYFW, 0.28, 0.16, 1.5)
FIST14 = hand_tip(EWC14, RYFW, 2.0, 0.14, tilt=-0.15)
F14A = off(FM, RYFW, 2.35, 0.1, 1.72)
L14A = [r((FIST14[0] + FM[0]) / 2), 1.7, r((FIST14[2] + FM[2]) / 2)]
C14A = cam(0.0, F14A, off(FM, RYFW, 2.2, 0.1, 1.72), L14A, L14A, lens=38)
chkc('S14', C14A, {'fist': FIST14, 'face': add(FM, [0, 1.95, 0]), 'headTop': add(FM, [0, 2.3, 0])})
F14B, L14B, LENS14B = [-2.0, 5.2, 6.2], [-0.72, 0.95, 0.5], 42
C14B = cam(CUTA14, F14B, F14B, L14B, L14B, lens=LENS14B)
# the raised ring hand: the forearm out to her right and up, turned so that the hollow (the hand's X, the thumb side) faces the camera
EWH14 = off(FM, RYFW, 0.1, 0.4, 1.85); EWH14L = add(EWH14, [0.06, -0.28, -0.04]); TILTH14 = -0.7; SH14 = 3.0
_d = [F14B[0] - EWH14[0], F14B[2] - EWH14[2]]; RYH14 = r(math.degrees(math.atan2(-_d[1], _d[0])), 1)
RING14 = hand_tip(EWH14, RYH14, SH14, 0.14, tilt=TILTH14, ahead=0.07)
chkc('S14', C14B, {'ring': RING14, 'wifeHead': add(FM, [0, 2.0, 0]), 'wifeTop': add(FM, [0, 2.32, 0]), 'wifeFeet': FM, 'well': HW, 'rimNear': add(HW, [0, 0.5, 0.85]), 'rimL': add(HW, [-0.85, 0.5, 0]),
                       'table': [0, 0.76, 0], 'fistAbove': add(LOW13, [0, 0.1, 0]), 'pass': [-0.25, 1.45, 0.8], 'splashTop': add(HW, [0, 2.0, 0])})
CHECKS.append(f'S14 ring forearm heading {RYH14}, high angle {r(D14 - CUTA14, 2)} s, splash at {SPL14}, card at {CARD14}')
PATH14 = [{'t': 0.0, 'p': RS(add(LOW13, [0, 0.08, 0])), 'hp': -0.74, 'curl': 1.0},
          {'t': r(WELL14 + 0.01), 'p': RS(add(LOW13, [0, 0.1, 0])), 'hp': -0.72, 'curl': 1.0, 'ease': 'inOut'},
          {'t': COCK14, 'p': RS(add(LOW13, [0.2, 0.45, -0.1])), 'hp': -0.45, 'curl': 1.0, 'st': 1.05, 'ease': 'out'},
          {'t': PASS14, 'p': RS([-0.25, 1.6, 0.8]), 'hp': -1.2, 'curl': 1.0, 'st': 1.15, 'ease': 'in'},
          {'t': RIMT14, 'p': RS([HOLE[0] + 0.05, 1.1, HOLE[1]]), 'hp': -1.5, 'curl': 1.0, 'st': 1.3, 'ease': 'linear'},
          {'t': DEEP14, 'p': RS(DEEPW14), 'hp': -1.57, 'curl': 1.0, 'st': 1.47, 'ease': 'out'},
          {'t': r(DEEP14 + 0.04), 'p': RS(add(DEEPW14, [0, 0.04, 0])), 'hp': -1.57, 'curl': 1.0, 'st': 1.45, 'ease': 'inOut'},
          {'t': SPL14, 'p': RS(DEEPW14), 'hp': -1.57, 'curl': 1.0, 'st': 1.47, 'ease': 'inOut'},
          {'t': REC14, 'p': RS(add(DEEPW14, [0, 0.3, 0])), 'hp': -1.55, 'curl': 1.0, 'st': 1.4, 'ease': 'out'},
          {'t': r(REC14 + 0.08), 'p': RS(add(DEEPW14, [0, 0.08, 0])), 'hp': -1.57, 'curl': 1.0, 'st': 1.44, 'ease': 'inOut'},
          {'t': D14, 'p': RS(add(DEEPW14, [0, 0.14, 0])), 'hp': -1.57, 'curl': 1.0, 'st': 1.43, 'ease': 'inOut'}]
RINGF = {'lid': 0.15, 'mouth': 'smile', 'brow': 0.5}
HW14 = lambda e: {'reach': {'R': R5(e, 1, 0.0)}, 'scl': {'handR': HIDE, 'handL': HIDE}, 'hip': 0}
WIFEK14 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={**HW14(EWC14), 'face': {**WIFEF, 'lid': 0.3}}, toonDur=0.0),
           k(0.42, toon={**HW14(add(EWC14, [0, -0.03, 0])), 'sq': [1.05, 0.95, 1.05], 'face': {**WIFEF, 'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.12),
           k(0.62, toon={**HW14(add(EWC14, [0, 0.02, 0])), 'sq': [0.98, 1.03, 0.98], 'face': {**WIFEF, 'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.1),
           k(CUTA14, look=RING14, lookDur=0.0), k(CUTA14, toon={**HW14(EWH14L), 'sq': [1.04, 0.96, 1.04], 'face': {**WIFEF, 'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.0),
           k(r(CUTA14 + 0.02), toon={**HW14(EWH14), 'sq': [0.95, 1.07, 0.95], 'face': {**WIFEF, 'lid': 0.4, 'mouth': 'smirk'}}, toonDur=r(WELL14 - CUTA14 - 0.04), toonEase='out'),
           k(WELL14, toon={**HW14(add(EWH14, [0, 0.05, 0])), 'sq': [0.93, 1.09, 0.93], 'face': RINGF}, toonDur=0.04, toonEase='out'),
           k(r(WELL14 + 0.1), toon={**HW14(add(EWH14, [0, 0.03, 0])), 'sq': [1.03, 0.98, 1.03], 'face': RINGF}, toonDur=0.08),
           k(r(WELL14 + 0.12), look=HW, lookDur=0.12),
           k(r(SPL14 + 0.06), toon={**HW14(add(EWH14, [0, 0.04, 0])), 'face': {**RINGF, 'brow': 0.7, 'lid': 0.25}}, toonDur=0.1)]
st.shot('S14', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFW, 'stand', 'neutral', keys=WIFEK14)],
        props=[P('stade14', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.8, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'rimAt': RIM14, 'splashAt': SPL14, 'splashH': 1.6, 'splashS': 1.3, 'splashTp': 0.11, 'crackW': 0.12, 'split': [[0, SPL12E]]}), *PITCH_TABLE(14), APRON('tablier14', 'femme'),
               HAND('poing14', EWC14, RYFW, s=2.0, sleeve=0.14, side='R', skin='#EBC29C', sleeveColor='#5E8C7A', mode='rock', tiltK=[[0.0, -0.15], [0.42, -0.05], [0.62, -0.22]], keys=[k(CUTA14, visible=False)]),
               HAND('puits14', EWH14L, RYH14, s=SH14, sleeve=0.14, side='R', skin='#EBC29C', sleeveColor='#5E8C7A', thumbColor='#D58A64', ringR=0.056, modes=[[-1, 'rock'], [WELL14, 'well']], ringOver=0.4, ringDur=0.08,
                    tiltK=[[CUTA14, -0.45], [r(WELL14 - 0.02), TILTH14], [r(WELL14 + 0.1), r(TILTH14 - 0.08)], [r(WELL14 + 0.2), TILTH14]], roll=0.55,
                    keys=[k(0.0, visible=False), k(CUTA14, visible=True), k(r(CUTA14 + 0.02), to=EWH14, dur=r(WELL14 - CUTA14 - 0.04), ease='out')]),
               P('robot14', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH14, 'smear': [[r(COCK14 + 0.01), RIMT14]], 'smearKind': 'block', 'smearLag': 0.05})],
        cams=[C14A, C14B, cam(SPL14, F14B, F14B, L14B, L14B, lens=LENS14B, shake=0.03)])
st.card('S14', 'PERDU', at=CARD14)
st.cue('sfx:pop', 'S14', WELL14, 0.4); st.cue('sfx:slideDown', 'S14', COCK14, 0.35); st.cue('sfx:splash', 'S14', SPL14, 0.45); st.cue('sfx:boing', 'S14', REC14, 0.2)

# 15: she has trained on him for thirty years. In the stands (the -X half, slid away), among cheering fans, he slowly lowers his clenched fist from
#     his chest to his waist and looks at it, deadpan; his two neighbours cheer
D15 = st.dur('S15')
SPL = SPL12E
HS15 = [r(-8.0 - SPL), 1.2 + 2 * 0.7, 23.6]
RYS15 = yaw(HS15, [-SPL, 0, 0]) - 12
NB15 = [off(HS15, RYS15, 0.0, -0.85, 0.0), off(HS15, RYS15, 0.0, 0.85, 0.0)]
EH15A = off(HS15, RYS15, 0.32, 0.08, 1.32); EH15B = off(HS15, RYS15, 0.3, 0.1, 0.95)
# (round 1) he deflates slowly as the fist comes down: the body sinks to 82 % and widens, the back rounds, the head droops and flattens a little; the
#     fist rides down with him
SAG15 = 0.82; EH15C = off(HS15, RYS15, 0.34, 0.1, r(0.95 * SAG15))
F15 = off(HS15, RYS15, 2.9, 0.3, 1.55)
F15, L15, LENS15 = FB('S15', F15, {'head': add(HS15, [0, 2.32, 0]), 'fist': add(EH15A, [0, 0.35, 0]), 'fistLow': EH15B, 'nb1': add(NB15[0], [0, 2.2, 0]), 'nb2': add(NB15[1], [0, 2.2, 0])}, top=0.2, bottom=0.74, lenses=range(30, 56))
C15 = cam(0.0, F15, off(HS15, RYS15, 2.6, 0.25, 1.45), L15, add(L15, [0, -0.08, 0]), lens=LENS15, ease='inOut')
CHEER = lambda p, ry, ph: [k(0.0, look=[-SPL, 2, 0], lookDur=0.0), *[k(r(ph + 0.22 * i), toon={'reach': {'R': R5(off(p, ry, 0.15, -0.35, 2.35 if i % 2 == 0 else 2.05), 1, 0.05), 'L': R5(off(p, ry, 0.15, 0.35, 2.05 if i % 2 == 0 else 2.35), 1, 0.05)}, 'face': {'lid': 0.0, 'mouth': 'O', 'jaw': 0.4, 'brow': 0.8}, 'sq': [1.0, 1.03 if i % 2 else 0.98, 1.0]}, toonDur=0.18, toonEase='inOut') for i in range(8)]]
SAGK = lambda e, u, face: {'reach': {'R': R5(e, 1, 0.0)}, 'scl': {'handR': HIDE, 'head': [r(1 + 0.05 * u, 3), r(1 - 0.08 * u, 3), r(1 + 0.05 * u, 3)]}, 'hip': 0,
                             'sq': [r(1 + 0.12 * u, 3), r(1 - (1 - SAG15) * u, 3), r(1 + 0.12 * u, 3)], 'bend': {'spine': [r(0.26 * u, 3), 0, 0, 1, None], 'neck': [r(0.08 * u, 3), 0, 0, 1, None]}, 'face': face}
SAGF = lambda u: {'lid': r(0.45 + 0.3 * u, 3), 'mouth': 'line', 'brow': r(-0.1 + 0.4 * u, 3), 'gy': r(0.5 * u, 3)}
HEROK15 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon=SAGK(EH15A, 0.0, SAGF(0.0)), toonDur=0.0),
           k(0.3, toon=SAGK(EH15B, 0.35, SAGF(0.2)), toonDur=0.45, toonEase='inOut'), k(0.55, look=EH15C, lookDur=0.35),
           k(0.75, toon=SAGK(lerp3(EH15B, EH15C, 0.6), 0.75, SAGF(0.7)), toonDur=0.4, toonEase='inOut'),
           k(1.15, toon=SAGK(EH15C, 1.0, SAGF(1.0)), toonDur=0.3, toonEase='out')]
st.shot('S15', 'grassland', setOpts=GRASS, actors=[act('mec', HS15, RYS15, 'stand', 'neutral', keys=HEROK15),
        act('supporter1', NB15[0], RYS15, 'stand', 'neutral', keys=CHEER(NB15[0], RYS15, 0.0)), act('supporter2', NB15[1], RYS15, 'stand', 'neutral', keys=CHEER(NB15[1], RYS15, 0.11))],
        props=[P('stade15', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 1.0, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'rimAt': -1, 'split': [[0, SPL]], 'clear': [[HS15[0] + SPL, HS15[2], 2.0]]}),
               HAND('poing15', EH15A, RYS15 + 20, s=1.35, sleeve=0.18, mode='rock', tiltK=[[0.3, -0.9], [1.1, -0.45]], keys=[k(0.3, to=EH15B, dur=0.45, ease='inOut'), k(0.75, to=lerp3(EH15B, EH15C, 0.6), dur=0.4, ease='inOut'), k(1.15, to=EH15C, dur=0.3, ease='out')])],
        cams=[C15])
st.cue('rain', 'S15', 0.0, 0.16, D15); st.cue('whoosh', 'S15', 0.75, 0.12, 0.6, 900, 300)

# 15b: « ...ans. » (round 1) not the S01 kitchen any more (it read as recycled footage): still in the stands from a new, closer angle on his other
#      side; his wife has come up into the row behind him, leans over his shoulder and her arm stretches down to pat his fist twice (each pat squashes
#      him a little more); he stays sagged and deadpan, the neighbour beside him still cheering
D15b = st.dur('S15b')
WB15 = off(HS15, RYS15, -1.25, 0.42, 0.7)
# her pats land on the top of his head (on the fist her arm passed behind his body): each one squashes his box head
PAT15 = [0.1, 0.3]; HTOP15 = off(HS15, RYS15, 0.06, 0.0, 1.95); FPAT = add(HTOP15, [0.0, 0.34, 0.05]); FHIT = add(HTOP15, [0.0, 0.03, 0.04])
F15b = off(HS15, RYS15, 2.4, -0.55, 1.6)
F15b, L15b, LENS15b = FB('S15b', F15b, {'head': add(HS15, [0, 2.05, 0]), 'fist': EH15C, 'wifeHead': add(WB15, [0, 2.15, 0]), 'wifeHand': FPAT, 'nb': add(NB15[0], [0, 2.2, 0])}, top=0.2, bottom=0.72, lenses=range(34, 56))
C15b = cam(0.0, F15b, add(F15b, [0.05, -0.02, -0.08]), L15b, L15b, lens=LENS15b)
chkc('S15b', C15b, {'head': add(HS15, [0, 2.05, 0]), 'fist': EH15C, 'wifeHead': add(WB15, [0, 2.15, 0]), 'wifeHand': FPAT, 'nb1': add(NB15[0], [0, 2.2, 0]), 'nb2': add(NB15[1], [0, 2.2, 0])})
WPAT = lambda p, sq=None: {'reach': {'L': R5(p, 1, 0.08)}, 'hands': {'L': 'open'}, 'scl': {'handL': [1.7, 1.7, 1.7]}, 'hose': 0.2, 'hip': 0, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': SMUG, **({'sq': sq} if sq else {})}
WIFEK15b = [k(-0.5, look=HTOP15), k(0.0, toon=WPAT(FPAT), toonDur=0.0)]
# his head kept up enough for the face to read from this lower angle (bowed, it showed the top of his head)
SAGB = lambda e, u: {**SAGK(e, u, {**SAGF(1.0), 'gy': 0.0, 'lid': 0.6}), 'bend': {'spine': [0.18, 0, 0, 1, None], 'neck': [-0.22, 0, 0, 1, None]}}
HEROK15b = [k(-0.5, look='camera'), k(0.0, toon=SAGB(EH15C, 1.0), toonDur=0.0)]
for t_ in PAT15:
    WIFEK15b += [k(t_, toon=WPAT(FHIT, [1.02, 0.98, 1.02]), toonDur=0.05, toonEase='in'), k(r(t_ + 0.09), toon=WPAT(FPAT), toonDur=0.07, toonEase='out')]
    HEROK15b += [k(r(t_ + 0.03), toon={**SAGB(EH15C, 1.08), 'scl': {'handR': HIDE, 'head': [1.18, 0.74, 1.18]}}, toonDur=0.03, toonEase='out'), k(r(t_ + 0.12), toon=SAGB(EH15C, 1.0), toonDur=0.07, toonEase='outBack')]
WIFEK15b += [k(0.42, look='camera', lookDur=0.1)]
st.shot('S15b', 'grassland', setOpts=GRASS, actors=[act('mec', HS15, RYS15, 'stand', 'neutral', keys=HEROK15b), act('femme', WB15, RYS15, 'stand', 'neutral', keys=WIFEK15b),
        act('supporter1', NB15[0], RYS15, 'stand', 'neutral', keys=CHEER(NB15[0], RYS15, 0.05))],
        props=[P('stade15b', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 1.0, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'rimAt': -1, 'split': [[0, SPL]], 'clear': [[HS15[0] + SPL, HS15[2], 2.0], [WB15[0] + SPL, WB15[2], 1.2]]}),
               APRON('tablier15b', 'femme'),
               HAND('poing15b', EH15C, RYS15 + 20, s=1.35, sleeve=0.18, mode='rock', tilt=-0.45)],
        cams=[C15b])
st.cue('sfx:stepSoft', 'S15b', PAT15[0], 0.35); st.cue('sfx:stepSoft', 'S15b', PAT15[1], 0.35)

# ============================== his street again: the bags taller than the house
HEAP16 = [3.4, 0, -3.6]
RBT16A, RBT16B = [-9.0, 0, 1.2], [-2.6, 0, 1.4]; RYB16 = 75
# 16: the loser had to take out the bin. His street: the mountain of bags beside his house, taller than its roof, gulls on top, flies; the
#     dripping robot rolls in on its tracks and stops in front of it; a quick tilt up the heap to the gulls (under a second)
D16 = st.dur('S16'); STOP16 = 0.95; TILT16 = r(W('S16', 'L16', 5) - 0.25)
PATH16 = [{'t': 0.0, 'p': [0, 2.4, 2.6], 'hp': -0.5, 'curl': 0.8}, {'t': D16, 'p': [0, 2.5, 2.6], 'hp': -0.45, 'curl': 0.8, 'ease': 'inOut'}]
F16 = [-1.2, 1.4, 14.5]
L16A = [-3.5, 2.2, 0.5]
C16A = cam(0.0, F16, add(F16, [0.2, 0, -0.2]), L16A, [-1.5, 2.3, 1.0], lens=44, ease='out')
L16B, LENS16B = FC('S16', F16, {'heapTop': add(HEAP16, [0, 11.5, 0]), 'gulls': add(HEAP16, [0, 14.5, 0]), 'roof': [0, 8.2, -6.6]}, top=0.08, bottom=0.6, lenses=range(36, 56))
C16B = glide([cam(TILT16, F16, add(F16, [0.0, 0.1, -0.1]), L16B, L16B, lens=LENS16B, ease='inOut')], 0.42)
chkc('S16', C16A, {'robotStop': add(RBT16B, [0, 3.0, 0]), 'robotStopF': RBT16B, 'heapFoot': add(HEAP16, [-6, 0, 3])})
chkc('S16', C16B, {'heapTop': add(HEAP16, [0, 11.5, 0]), 'roof': [0, 8.2, -6.6]})
st.shot('S16', 'pavillon', setOpts=STREET, actors=[],
        props=[P('maison16', 'chifHouse', pos=HOUSE), P('ciel16', 'noClouds', pos=[0, 0, 0]), P('montagne16', 'chifBagHeap', pos=HEAP16, opts={'h': 11.5, 'r': 6.5, 'bag': 0.9, 'gulls': 5, 'gullS': 1.3, 'gullR': 4.5, 'gullH': 2.0, 'perch': 2, 'flies': 10}),
               P('robot16', 'chifRobot', pos=RBT16A, ry=RYB16, opts={'base': 'tracks', 'path': PATH16, 'drip': True}, keys=[k(0.0, to=RBT16B, dur=STOP16, ease='out')])],
        cams=[C16A, C16B])
st.cue('engine', 'S16', 0.0, 0.3); st.cue('sfx:brake', 'S16', r(STOP16 - 0.2), 0.2); st.cue('sfx:squeak', 'S16', r(TILT16 + 0.3), 0.25)

# 17: the hand contested: the well does not count. Close on the robot in front of the heap: the dripping hand turns to us, flat, and on « contesté »
#     draws the referee's rectangle in the air, the same glowing trail; behind it one more bag rolls down the heap; it holds, deadpan, the trail
#     pulsing, drips falling, the gulls circling
D17 = st.dur('S17'); RECT17 = r(W('S17', 'L17', 3) - 0.1); RDUR17 = 1.1; ROLL17 = r(W('S17', 'L17', 7) - 0.3)
RB17 = RBT16B; RY17 = 40
def R17(w): return tol(RB17, RY17, w)
# (round 1) the end hold: the flat hand (finger creases, a pale thumb, a lighter back) parks against the cream house wall on the left, the rectangle
#     hangs to its right over the heap, clear of the arm, drawn by the same smooth trail as the referee's (the robot's own stepped trail is gone);
#     the bags are charcoal and dark green with a spec light and a few odd blue and white ones (the heap was a black mass)
RC17 = [-0.05, 4.15, 1.0]; RW17, RH17 = 1.7, 1.1
# (round 2) further back and to the left so the base and the arm are not cut by the left edge; in the hold the camera tilts up to the gulls
F17 = [-2.4, 2.4, 12.5]; L17, LENS17 = [-1.2, 4.4, 0.4], 52; L17E = [-1.0, 5.9, 0.4]
RR17 = right(yaw(RC17, F17))
RECT17P = [[r(RC17[0] + RR17[0] * sx * RW17 / 2), r(RC17[1] + sy * RH17 / 2), r(RC17[2] + RR17[2] * sx * RW17 / 2)] for sx, sy in [(1, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)]]
seg17 = [math.dist(RECT17P[i], RECT17P[i + 1]) for i in range(4)]; TL17 = sum(seg17)
CORN17 = [RECT17] + [r(RECT17 + RDUR17 * sum(seg17[:i + 1]) / TL17) for i in range(4)]
HP17, ROLLH = 1.3, 0.67
def WRIST17(c, hp=HP17, k_=0.8):
    # the wrist that puts the flat hand's middle on the point c (the hand points up at hp, out from the turret)
    yw = math.atan2(c[0] - RB17[0], c[2] - RB17[2]); d = [math.sin(yw) * math.cos(hp), math.sin(hp), math.cos(yw) * math.cos(hp)]
    return R17([r(c[i] - d[i] * k_) for i in range(3)])
REST17 = [-1.85, 4.05, 0.85]
PATH17 = [{'t': 0.0, 'p': WRIST17(add(REST17, [0.1, -0.5, 0.1]), 0.6), 'hp': 0.6, 'curl': 0.8, 'roll': 0.0},
          {'t': r(RECT17 - 0.12), 'p': WRIST17(RECT17P[0]), 'hp': HP17, 'curl': 0.0, 'roll': ROLLH, 'ease': 'inOut'}]
for i in range(4): PATH17.append({'t': CORN17[i + 1], 'p': WRIST17(RECT17P[i + 1]), 'hp': HP17, 'curl': 0.0, 'roll': ROLLH, 'ease': 'linear'})
PATH17 += [{'t': r(CORN17[-1] + 0.45), 'p': WRIST17(REST17), 'hp': HP17, 'curl': 0.0, 'roll': ROLLH, 'ease': 'inOut'},
           {'t': r(CORN17[-1] + 1.2), 'p': WRIST17(add(REST17, [0, 0.06, 0])), 'hp': HP17 + 0.03, 'curl': 0.0, 'roll': ROLLH, 'ease': 'inOut'},
           {'t': D17, 'p': WRIST17(add(REST17, [0, -0.02, 0])), 'hp': HP17, 'curl': 0.0, 'roll': ROLLH, 'ease': 'inOut'}]
TILT17 = r(ROLL17 + 1.0)
C17 = cam(0.0, F17, add(F17, [0.0, 0.05, -0.35]), L17, add(L17, [0, 0.03, 0]), lens=LENS17, ease='inOut')
C17B = glide([cam(TILT17, add(F17, [0.0, 0.05, -0.35]), add(F17, [0.0, 0.1, -0.5]), add(L17, [0, 0.03, 0]), L17E, lens=LENS17, ease='inOut')], 0.25)
chkc('S17', C17, {'rectTL': RECT17P[1], 'rectBR': RECT17P[3], 'rest': REST17, 'restTop': add(REST17, [0, 0.9, 0]), 'base': RB17, 'baseL': add(RB17, [-1.3, 0, 0.6]), 'heapTop': add(HEAP16, [0, 11.5, 0]), 'houseWallL': [-3.0, 4.3, -3.6], 'rollStart': add(HEAP16, [-1.2, 9.6, 0.5]), 'rollEnd': add(HEAP16, [-1.2, 0.5, 7.0])})
chkc('S17', C17B, {'rectTL': RECT17P[1], 'rectBR': RECT17P[3], 'rest': REST17, 'heapTop': add(HEAP16, [0, 11.5, 0]), 'gulls': add(HEAP16, [-2.5, 13.5, 0]), 'baseL': add(RB17, [-1.3, 0.5, 0.6])}, end=True)
st.shot('S17', 'pavillon', setOpts=STREET, actors=[],
        props=[P('maison17', 'chifHouse', pos=HOUSE), P('ciel17', 'noClouds', pos=[0, 0, 0]), P('montagne17', 'chifBagHeap', pos=HEAP16, opts={'h': 11.5, 'r': 6.5, 'bag': 0.9, 'gulls': 7, 'gullS': 1.4, 'gullR': 4.0, 'gullH': 2.0, 'perch': 2, 'flies': 10, 'rollAt': ROLL17, 'rollDur': 1.2, 'rollX': -3.5, 'rollS': 1.7, 'rollColor': '#3B6FB5', 'emis': '#2E3740'}),
               P('robot17', 'chifRobot', pos=RB17, ry=RY17, opts={'base': 'tracks', 'path': PATH17, 'drip': True, 'fingers': 4, 'paperW': 1.12, 'paperT': 0.8, 'handColor': '#5E6773', 'backColor': '#7C8692', 'thumbColor': '#A9B0B8'}),
               P('trait17', 'chifTrail', pos=[0, 0, 0], opts={'pts': RECT17P, 'at': RECT17, 'dur': RDUR17, 'r': 0.035})],
        cams=[C17, C17B])
st.cue('sfx:rattleShort', 'S17', 0.1, 0.2); st.cue('sfx:zip', 'S17', RECT17, 0.25); st.cue('sfx:bell', 'S17', CORN17[-1], 0.2); st.cue('thud', 'S17', r(ROLL17 + 1.15), 0.25); st.cue('sfx:squeak', 'S17', 3.2, 0.2)

print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
FEMME = {'preset': 'femme', 'seed': 961, 'glasses': False, 'build': {'width': 0.9, 'headWidth': 1.25, 'height': 0.94}, 'toon': TOON}
ARB = {'preset': 'boss', 'outfit': 'suit', 'suit': '#2E3138', 'pants': '#2A2C32', 'shirt': '#2E3138', 'lapel': '#454952', 'tie': '#2E3138', 'cuff': '#2E3138', 'hat': 'none', 'glasses': False, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
SAV = {'preset': 'doctor', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
WORK = {'preset': 'worker', 'hat': 'none', 'hair': 'bald', 'facial': 'none', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
FAN = {'preset': 'boss', 'outfit': 'suit', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("Le chifoumi", rig='toon', fingers=False, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'femme': FEMME,
    'arbitre1': {**ARB, 'seed': 962, 'hair': 'crew'}, 'arbitre2': {**ARB, 'seed': 963, 'facial': 'mustache', 'hair': 'receding'}, 'arbitre3': {**ARB, 'seed': 964, 'hair': 'slick', 'skin': '#8A5A3A', 'faceRim': True},
    'arbitreT': {**ARB, 'seed': 965, 'hair': 'buzz', 'suit': '#1F2126', 'shirt': '#1F2126', 'cuff': '#F4F4F0', 'gloves': '#F4F4F0'},
    'savant1': {**SAV, 'seed': 966}, 'savant2': {**SAV, 'seed': 967, 'hair': 'bun', 'lipstick': True, 'glasses': False},
    'officiel7': {'preset': 'politique', 'seed': 968, 'suit': '#6E7480', 'lapel': '#5A606C', 'tie': '#7A2E3A', 'hairColor': '#8A8A8A', 'glasses': True, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'soudeur1': {**WORK, 'seed': 969}, 'soudeur2': {**WORK, 'seed': 970},
    'ouvrier1': {**WORK, 'seed': 971, 'hat': 'hardhat2', 'hatColor': '#E8E4DA', 'suit': '#8A9AAA', 'bandColor': '#C9C2B2'}, 'ouvrier2': {**WORK, 'seed': 972, 'hat': 'hardhat2', 'hatColor': '#E8E4DA', 'suit': '#8A9AAA', 'facial': 'mustache', 'bandColor': '#C9C2B2'},
    'officiel10': {'preset': 'politique', 'seed': 973, 'suit': '#3A5A8C', 'lapel': '#2E4A76', 'tie': '#E2E6EC', 'shirt': '#F2F2EE', 'hairColor': '#5A3A28', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 974, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#2C3E5C', 'hairColor': '#BDBDBD', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'supporter1': {**FAN, 'seed': 975, 'suit': '#E0413A', 'shirt': '#F4F4F0', 'lapel': '#B8302A', 'tie': '#F4F4F0', 'hair': 'crew'}, 'supporter2': {**FAN, 'seed': 976, 'suit': '#2F62B5', 'shirt': '#F2C230', 'lapel': '#244B86', 'tie': '#F2C230', 'facial': 'mustache', 'hair': 'receding'},
})
