#!/usr/bin/env python3
"""La moustache (story 67, cycle 29; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man shaved off his moustache. The moustache left on its own. It took the bus. It found a flat. And a job at the bank. The tax office sent it a
bill. It paid. It stood for the town hall. It won, with sixty per cent. The man wanted it back. It filed a complaint. The judge sentenced him to stay
shaved. The moustache became a minister. Then president. The man applied to be its assistant. It said no. Not hairy enough.
Staging: at the bathroom mirror the razor goes under his nose and the moustache drops off, lands on two tiny legs, opens its eyes, and walks out of
the door while he stares down at it, his lip bare; it hops onto the bus; a key in a flat's door; a tie at a bank counter, stamping; a letter opened,
its eyes popping; the banknotes counted out; a megaphone on a crate; the mayor's sash and the results board; him creeping up with a jar; at the
police desk it points at him; the judge's gavel, a razor held up; behind a minister's desk under the flag; at the president's lectern, flags and
flashes; him in a waiting room with his CV; it reads the CV and shakes its head; his bare lip, a look at us.
Natural look; cycle 29: the moustache creature (a bristly handlebar on two little legs, googly eyes), scale keys, props reused."""
from story_kit import *
import math

st = Story('moustache', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 18)])

PI = math.pi
P_NAVY = '#26365F'
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3, ink=None: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True, **({'ink': ink} if ink else {})})
DEAD = {'lid': 0.45}
MS = 0.62                                            # the moustache's size once it lives on its own (on his face it was 0.22)
LIP = {'face': {'lid': 0.45, 'mouth': 'line'}}

for g_ in [('S01', 1.0, 'mec', 'shave'), ('S02', 0.9, 'mous', 'walk'), ('S06', 0.8, 'mous', 'bill'), ('S09', 1.0, 'mous', 'won'), ('S12', 0.9, 'juge', 'gavel'), ('S16', 0.8, 'mous', 'no'), ('S17', 0.7, 'mec', 'end')]:
    st.gag(*g_)
st.card('S09', 'ÉLUE', at=0.5)
st.card('S12', 'RASÉ', at=0.6)
st.card('S16', 'NON', at=0.35)

# (review 1: 4.0 / 3.0) pass 2: a creature takes no reach or touch: its arms move only by clips (stampDesk, giveItem, drawMid, royalWave, point,
# shakeHead); its blinks are keyed shot by shot (one automatic blink fell at 0.73 s in ten shots); framings keep it front-on, whole and big
def MK(t, clip, blinks=(), **pp): return k(t, clip=clip, params={'blinks': list(blinks), **pp})   # a clip key of the moustache with this shot's blinks
SQ = lambda t, s, d=0.05, e='out': k(t, toon={'sq': list(s)}, toonDur=d, toonEase=e)
LAY = lambda t, a, d=0.08, e='out': k(t, toon={'lay': [a, 0.0]}, toonDur=d, toonEase=e)

# 1: the hook. At the bathroom basin, from beside the mirror: the razor goes along his lip; the moustache on his lip opens its eyes, looks at us, and
#    drops onto the basin; his eyes follow it down
D1 = st.dur('S01'); SHAVE1 = 0.55; DROP1 = 0.9; LAND1 = 1.2; ME1 = [-1.7, 0, -1.2]; LIP1 = [-1.7, 1.8, -1.42]; RIM1 = [-1.72, 0.93, -1.66]
RAZ = lambda x, f=None: {'touch': {'R': ['face', r(x), 0.07, 0.24, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': f or {'lid': 0.35, 'mouth': 'line'}}
st.shot('S01', 'salleDeBain', setOpts={'half': 3.4}, actors=[
        act('mec', ME1, 180, 'stand', 'neutral', keys=[k(0.0, look=[-1.7, 1.95, -2.2]), k(0.0, toon={**RAZ(-0.1), 'hip': 0.0}, toonDur=0.0), k(0.08, toon=RAZ(0.1), toonDur=0.42, toonEase='inOut'),   # the razor along the lip, the fist under the mouth
            k(SHAVE1, toon=RAZ(0.12, {'lid': 0.0, 'eye': 0.35, 'mouth': 'line'}), toonDur=0.06), k(r(DROP1 + 0.05), look=RIM1),
            k(r(DROP1 + 0.05), toon={'touch': {'R': ['face', 0.14, -0.02, 0.32, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.45, 'gy': 0.7, 'mouth': 'O'}}, toonDur=0.15)]),   # his eyes follow it down
        act('mous', LIP1, 180, 'stand', 'closed', scale=0.22, keys=[MK(0.0, 'stand', [1.55]), k(SHAVE1, expr='surprised'), k(r(SHAVE1 + 0.05), look='camera'),   # it opens its eyes on his lip: a look at us...
            k(DROP1, to=RIM1, dur=r(LAND1 - DROP1), ease='in', face='keep'), MK(DROP1, 'airborne', [1.55]), SQ(DROP1, (0.85, 1.25, 0.85)),   # ...then it drops (review 1: no hang, no look)
            MK(LAND1, 'land', [1.55]), SQ(LAND1, (1.45, 0.6, 1.45), 0.04), SQ(r(LAND1 + 0.08), (0.88, 1.14, 0.88), 0.07), SQ(r(LAND1 + 0.2), (1.0, 1.0, 1.0), 0.1), k(r(LAND1 + 0.3), expr='neutral'), k(r(LAND1 + 0.35), look=[-1.7, 2.0, -1.2])])],   # lands with a squash, looks up at him
        props=[P('raz1', 'razor', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=1.3)],
        cams=[FC(0.0, [-0.85, 1.75, -1.85], [[ME1[0], 2.35, ME1[2]], [ME1[0], 1.55, ME1[2]], RIM1, [r(RIM1[0] - 0.3), 0.9, RIM1[2]]], top=0.14, bottom=0.78, inside=(-3.3, 3.3, 0.4, 2.8, -2.1, 3.0))])   # (review 1) beside the mirror: his face, the razor, the moustache on his lip and the white basin it lands on (a laundry room with no razor)
st.cue('sfx:stretch', 'S01', 0.1, 0.15); st.cue('sfx:pop', 'S01', SHAVE1, 0.2); st.cue('sfx:whistle', 'S01', DROP1, 0.15); st.cue('sfx:boing', 'S01', LAND1, 0.25)

# 2: the moustache left on its own. Low on the bathroom floor: it drops from the basin, lands squashed, recoils, and trots off past us, three-quarter
#    to the lens; behind it his legs, his head bent down after it
D2 = st.dur('S02'); M2 = [-1.62, 0, -1.58]; G2 = [-0.55, 0, -0.15]
st.shot('S02', 'salleDeBain', setOpts={'half': 3.4}, actors=[
        act('mous', [M2[0], 0.3, M2[2]], 35, 'airborne', 'surprised', scale=0.3, keys=[k(0.0, to=M2, dur=0.12, ease='in', face='keep'), MK(0.12, 'land', [0.5, 1.45]), SQ(0.12, (1.4, 0.62, 1.4), 0.04), SQ(0.2, (0.9, 1.12, 0.9), 0.06), SQ(0.32, (1.0, 1.0, 1.0), 0.1),
            k(0.3, expr='neutral'), k(0.45, to=G2, dur=r(D2 - 0.45), clip='walk', ease='linear'), MK(0.45, 'walk', [0.5, 1.45]), k(0.6, look=[0.4, 0.3, 1.2])]),   # (review 1) it lands, recoils and trots, three-quarter to us (from behind its curls read as fists)
        act('mec', ME1, 180, 'stand', 'neutral', keys=[k(0.0, look=[-1.6, 0.0, -1.5]), k(0.0, toon={'bend': {'neck': [0.5, 0, 0, 1, None], 'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'gy': 0.7, 'mouth': 'O'}}, toonDur=0.0), k(0.9, look=[-0.6, 0.0, -0.2])])],
        cams=[FC(0.0, [-0.2, 0.42, 0.75], [[M2[0], 0.25, M2[2]], [G2[0], 0.25, G2[2]], [G2[0], 0.0, G2[2]], [ME1[0], 1.1, ME1[2]], [r(ME1[0] - 0.3), 0.0, ME1[2]]], top=0.14, bottom=0.74, drift=(0.15, 0.0, 0.1))])
st.cue('thud', 'S02', 0.12, 0.2); st.cue('sfx:stepSoft', 'S02', 0.6, 0.15); st.cue('sfx:stepSoft', 'S02', 0.95, 0.15); st.cue('sfx:stepSoft', 'S02', 1.3, 0.15)

# 3: it took the bus. At the stop the city bus pulls up, its doors fold open; the moustache crouches and hops up into the doorway on an arc
D3 = st.dur('S03'); BUS3 = [3.4, 0, 0.0]; DOOR3 = [4.55, 0, 0.7]; HOP3 = 0.62; IN3 = [4.2, 0.45, 0.7]
st.shot('S03', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, actors=[
        act('mous', [5.25, 0, 0.7], -90, 'stand', 'neutral', scale=MS, keys=[MK(0.0, 'stand', [0.3]), k(0.0, look=[4.2, 0.6, 0.7]), SQ(r(HOP3 - 0.1), (1.18, 0.8, 1.18), 0.07),   # a crouch...
            k(HOP3, to=[4.75, 0.62, 0.7], dur=0.16, ease='out', face='keep'), k(r(HOP3 + 0.16), to=IN3, dur=0.14, ease='in', face='keep'), MK(HOP3, 'jump', [0.3], dur=0.3, height=0.0), SQ(HOP3, (0.82, 1.25, 0.82), 0.05),   # ...a stretched hop on an arc...
            SQ(r(HOP3 + 0.3), (1.3, 0.72, 1.3), 0.04), SQ(r(HOP3 + 0.38), (1.0, 1.0, 1.0), 0.1), MK(r(HOP3 + 0.3), 'stand', [0.3]), k(r(HOP3 + 0.4), look='camera')])],   # ...in at the door, a look back at us
        props=[P('bus3', 'cityBus', pos=[BUS3[0], 0, 11.0], ry=90, opts={'len': 7.6, 'doors': [[0.0, 0.0], [0.42, 0.0], [0.6, 1.0]]}, keys=[k(0.0, to=BUS3, dur=0.45, ease='out')])],   # (review 1) its doors toward the kerb (the hop was behind a blind side)
        cams=[FC(0.0, [7.0, 0.9, 3.1], [[5.25, 0.45, 0.7], [5.25, 0.0, 0.7], [IN3[0], 1.1, IN3[2]], [4.55, 2.3, 1.4], [4.55, 0.0, 0.0]], top=0.16, bottom=0.74)])
st.cue('sfx:brake', 'S03', 0.3, 0.25); st.cue('sfx:zip', 'S03', 0.45, 0.15); st.cue('sfx:boing', 'S03', HOP3, 0.2)

# 4: it found a flat. On a landing: before a wooden door numbered 12, its tiny suitcase beside it, it holds up a big gold key to us, then turns it in
#    the lock (clunk) and the door swings open; a look at us
D4 = st.dur('S04'); DR4 = [0.3, 0, -2.94]; KEY4 = [0.665, 0.36, -2.87]; MO4 = [0.92, 0, -2.5]; TURN4 = 0.85; OPEN4 = 1.05
st.shot('S04', 'immeubleHall', setOpts={'liftX': -2.4}, actors=[
        act('mous', MO4, -15, 'stand', 'happy', scale=MS, keys=[MK(0.0, 'holdUp', [0.22, 1.35]), k(0.0, look='camera'), MK(0.55, 'pokeFinger', [0.22, 1.35]), k(0.55, look=KEY4), k(0.55, turn=-60),
            SQ(TURN4, (1.08, 0.94, 1.08), 0.04), SQ(r(TURN4 + 0.08), (1.0, 1.0, 1.0), 0.08), MK(r(OPEN4 + 0.05), 'celebrate', [0.22, 1.35]), k(r(OPEN4 + 0.05), turn=-15), k(r(OPEN4 + 0.1), look='camera')])],   # (review 1) the key shown to us, turned in the lock (no key; its back to us)
        props=[P('porte4', 'door', pos=DR4, opts={'color': '#9A6A42', 'frame': '#6B4A30', 'name': '12', 'nameY': 0.62, 'openAt': OPEN4}),
               P('serr4', 'keyholePlate', pos=[KEY4[0], KEY4[1], -2.885], scale=1.4, keys=[k(OPEN4, visible=False)]),
               P('cle4a', 'bigKey', on={'actor': 'mous', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=0.9, keys=[k(0.62, visible=False)]),   # shown to us in its hand...
               P('cle4b', 'bigKey', pos=[KEY4[0], KEY4[1], -2.875], rot=[0.0, 0.0, 0.0], scale=0.9, keys=[k(0.0, visible=False), k(0.62, visible=True), k(TURN4, rotTo=[0.0, 0.0, 1.57], dur=0.12, ease='out'), k(OPEN4, visible=False)]),   # ...then in the lock, turned
               P('valise4', 'suitcase', pos=[1.25, 0, -2.45], ry=-20, scale=0.35)],
        cams=[FC(0.0, [1.1, 0.42, -1.0], [MO4, [MO4[0], 0.45, MO4[2]], KEY4, [DR4[0], 0.9, DR4[2]], [1.3, 0.0, -2.45]], top=0.16, bottom=0.78)])
st.cue('sfx:click', 'S04', r(TURN4 + 0.04), 0.25); st.cue('sfx:creak', 'S04', OPEN4, 0.2)

# 5: and a job at the bank. At window two of the bank, a little tie on, it stamps a form with a rubber stamp: bang, bang, bang, a squash on each hit
D5 = st.dur('S05'); STAMPS = [0.4, 0.8, 1.2]; MO5 = [0.0, 1.1, -2.42]
st.shot('S05', 'poste', setOpts={'title': 'BANQUE'}, actors=[act('mous', MO5, 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[0.05, 1.1, -2.25]),
            *[MK(r(t_ - 0.3), 'stampDesk', [0.95], hit=0.3) for t_ in STAMPS], *[kk for t_ in STAMPS for kk in (SQ(t_, (1.12, 0.86, 1.12), 0.04, 'in'), SQ(r(t_ + 0.08), (1.0, 1.0, 1.0), 0.08))], k(1.3, look='camera')])],   # (review 1) three stamps (the OK came with its arms still)
        props=[P('tamp5', 'rubberStamp', on={'actor': 'mous', 'hand': 'R', 'offset': [0.0, -0.02, 0.02]}, scale=1.6),
               P('form5', 'paperSheet', pos=[0.06, 1.105, -2.28], rot=[-PI / 2, 0, 0], opts={'w': 0.3, 'h': 0.4, 'lines': ['FORMULAIRE'], 'stamp': {'text': 'OK', 'color': '#C2342A', 'at': STAMPS[0]}}),
               *[P(f'ok5{j}', 'stampMark', pos=[r(0.02 + 0.07 * j), 1.108, r(-2.32 + 0.06 * j)], rot=[-PI / 2, 0, r(0.2 - 0.25 * j)], opts={'text': 'OK', 'w': 0.12, 'h': 0.06}, keys=[k(0.0, visible=False), k(STAMPS[j + 1], visible=True)]) for j in range(2)],
               P('cravate5', 'slab', on={'actor': 'mous', 'joint': 'head', 'offset': [0.0, -0.02, 0.06]}, opts={'w': 0.05, 'h': 0.14, 'd': 0.01, 'color': '#C8322A'})],
        cams=[FC(0.0, [0.25, 1.4, -0.7], [[MO5[0], 1.55, MO5[2]], [MO5[0], 1.1, MO5[2]], [-0.25, 1.3, MO5[2]], [0.25, 1.3, MO5[2]], [0.06, 1.1, -2.28]], top=0.18, bottom=0.76)])   # front-on at its eye level, whole and centred
for t_ in STAMPS: st.cue('thud', 'S05', t_, 0.2)

# 6: the tax office sent it a bill. Front-on at its eye level: it holds the letter out in front of it by both edges; its eyes shoot out on stalks over
#    the paper, wobble, and spring back
D6 = st.dur('S06'); POP6 = 0.8; MO6 = [0.0, 0.0, -0.6]
st.shot('S06', 'livingRoom', setOpts={'sofa': False}, actors=[act('mous', MO6, 0, 'stand', 'neutral', scale=MS, keys=[MK(0.0, 'readPhone', [0.35], popAt=[POP6, 1.95], popLen=0.32), k(0.0, look=[0.0, 0.1, 0.0]),
            SQ(r(POP6 - 0.06), (1.06, 0.92, 1.06), 0.05), SQ(POP6, (0.9, 1.16, 0.9), 0.05), SQ(r(POP6 + 0.12), (1.0, 1.0, 1.0), 0.12), k(r(POP6 + 0.05), expr='shocked'), k(2.0, expr='neutral')])],   # (review 1) the eyes on stalks (they never came out)
        props=[P('lettre6', 'paperSheet', on={'actor': 'mous', 'joint': 'head', 'offset': [0.0, -0.02, 0.17]}, face='camera', opts={'w': 0.24, 'h': 0.15, 'lines': ['IMPÔTS', 'À PAYER'], 'bright': True})],   # held in front of the body (it passed through it)
        cams=[FC(0.0, [0.0, 0.3, 0.75], [[MO6[0], 0.62, MO6[2]], [MO6[0], 0.0, MO6[2]], [-0.3, 0.25, MO6[2]], [0.3, 0.25, MO6[2]]], top=0.18, bottom=0.78)])
st.cue('sfx:paper', 'S06', 0.15, 0.2); st.cue('sfx:boing', 'S06', POP6, 0.3); st.cue('sfx:slideUp', 'S06', 1.95, 0.15)

# 7: it paid. From the clerk's side of the tax office window: on the counter it deals three banknotes out of its hand, one, two, three, each landing
#    on the last
D7 = st.dur('S07'); NOTES7 = [0.25, 0.5, 0.75]; MO7 = [0.0, 1.1, -2.1]
st.shot('S07', 'poste', setOpts={'title': 'CENTRE DES IMPÔTS'}, actors=[act('mous', MO7, 180, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[0.0, 1.1, -2.6]),
            *[MK(r(t_ - 0.25), 'giveItem', [0.05]) for t_ in NOTES7], *[SQ(t_, (1.05, 0.95, 1.05), 0.04) for t_ in NOTES7], k(0.95, look=[0.0, 1.6, -3.0])])],   # (review 1) dealt one by one (they slid in on their own)
        props=[*[P(f'note7{j}', 'banknote', on={'actor': 'mous', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}, face='camera', opts={'w': 0.18},
                   keys=[k(0.0, visible=False), k(r(NOTES7[j] - 0.2), visible=True), k(NOTES7[j], detach=True, fall=True, toss=[r(0.08 * (j - 1)), 0.6, -0.5], floor=r(1.112 + 0.004 * j), restRot=[-PI / 2, 0, r(0.25 * (j - 1))])]) for j in range(3)]],
        cams=[FC(0.0, [0.3, 1.45, -3.15], [[MO7[0], 1.55, MO7[2]], [MO7[0], 1.1, MO7[2]], [-0.28, 1.3, MO7[2]], [0.28, 1.3, MO7[2]], [0.0, 1.11, -2.35]], top=0.18, bottom=0.76, inside=(-3.0, 3.0, 1.2, 2.5, -3.3, -2.8))])
for t_ in NOTES7: st.cue('sfx:cash', 'S07', t_, 0.15)

# 8: it stood for the town hall. On a crate in the square, the megaphone to its mouth, it shouts (a squash on each word); its poster behind it
D8 = st.dur('S08'); MO8 = [6.4, 0.45, 0.0]
st.shot('S08', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, actors=[act('mous', MO8, -60, 'stand', 'angry', scale=MS, keys=[MK(0.0, 'yell', [1.3]), k(0.0, look='camera'),
            *[kk for j in range(4) for kk in (SQ(r(0.2 + 0.3 * j), (0.92, 1.12, 0.92), 0.05), SQ(r(0.33 + 0.3 * j), (1.04, 0.97, 1.04), 0.08))]])],
        props=[P('caisse8', 'slab', pos=[6.4, 0.22, 0.0], opts={'w': 0.5, 'h': 0.45, 'd': 0.5, 'color': '#B98A5A'}), P('mega8', 'megaphone', on={'actor': 'mous', 'hand': 'R', 'offset': [0.0, 0.0, 0.06]}, scale=0.6),
               P('affiche8', 'signBoard', pos=[7.35, 0, -0.75], ry=-60, opts={'text': 'VOTEZ\nMOUSTACHE', 'bg': '#2F62B5', 'fg': '#FFFFFF', 'w': 1.0, 'h': 1.3})],   # (review 1) on two lines (a stray bar between the words)
        cams=[FC(0.0, [5.0, 0.95, 1.45], [[MO8[0], 0.9, MO8[2]], [MO8[0], 0.0, MO8[2]], [7.35, 2.35, -0.75], [7.35, 1.0, -0.75]], top=0.18, bottom=0.78)])
st.cue('sfx:static', 'S08', 0.2, 0.2); st.cue('sfx:static', 'S08', 0.8, 0.15)

# 9: it won, with sixty per cent. In the town hall, centred and big on the table, in a thin tricolour sash, it jumps for joy; the results board fills to
#    sixty per cent beside it; confetti (ÉLUE)
D9 = st.dur('S09'); MO9 = [0.0, 0.76, 0.0]
st.shot('S09', 'mairie', setOpts={'plate': 'MAIRIE', 'map': False}, actors=[act('mous', MO9, 0, 'celebrate', 'happy', scale=MS, keys=[MK(0.0, 'celebrate', [1.6]), k(0.0, look='camera'),
            k(0.55, to=[0.0, 0.98, 0.0], dur=0.15, ease='out', face='keep'), k(0.7, to=MO9, dur=0.15, ease='in', face='keep'), SQ(0.5, (1.15, 0.85, 1.15), 0.05), SQ(0.56, (0.88, 1.16, 0.88), 0.06), SQ(0.85, (1.25, 0.78, 1.25), 0.04), SQ(0.95, (1.0, 1.0, 1.0), 0.1)])],   # a hop for joy
        props=[P('table9', 'desk', pos=[0.0, 0, 0.0], opts={'w': 1.2}), P('res9', 'resultsBoard', pos=[0.95, 1.45, -1.0], ry=-20, opts={'name': 'MOUSTACHE', 'fillAt': 0.1, 'pct': 60, 'w': 1.2, 'h': 0.8}),   # (review 1) 60 % / 40 % (it read 100 % / 0 %)
               *[P(f'ech9{j}', 'slab', on={'actor': 'mous', 'joint': 'head', 'offset': [0.0, r(0.07 - 0.028 * j), 0.075]}, rot=[0, 0, 0.55], opts={'w': 0.5, 'h': 0.026, 'd': 0.01, 'color': c_}) for j, c_ in enumerate(['#2F62B5', '#F4F4F0', '#E0413A'])],   # a thin tricolour sash (a flat blue bar hid its body)
               P('conf9', 'confetti', pos=[0.3, 0.8, 0.2], opts={'w': 2.0, 'h': 2.0, 'd': 1.0, 'n': 90})],
        cams=[FC(0.0, [0.25, 1.15, 1.9], [[MO9[0], 1.2, MO9[2]], [MO9[0], 0.7, MO9[2]], [-0.3, 0.95, 0.0], [0.95, 1.85, -1.0], [0.95, 1.05, -1.0]], top=0.2, bottom=0.78)])
st.cue('sfx:fanfare', 'S09', 0.15, 0.2); st.cue('pop', 'S09', 0.85, 0.15)

# 10: the man wanted it back. In the town hall he creeps up behind it with a glass jar raised in both hands and brings it down; it side-steps, the jar
#     lands empty on the table; it looks at us
D10 = st.dur('S10'); SLAM10 = 1.0; MO10 = [0.0, 0.76, 0.0]; DODGE10 = [0.33, 0.76, 0.05]; ME10 = [-0.6, 0, -0.45]
JAR = lambda y, f: {'reach': {'R': [-0.06, y, -0.02, 1, 0.02], 'L': [0.06, y, -0.02, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': f}
st.shot('S10', 'mairie', setOpts={'plate': 'MAIRIE', 'map': False}, actors=[
        act('mous', MO10, 0, 'stand', 'neutral', scale=MS, keys=[MK(0.0, 'stand', [0.45, 1.5]), k(0.0, look=[0.0, 1.0, 2.0]), k(r(SLAM10 - 0.08), to=DODGE10, dur=0.1, ease='out', face='keep'), SQ(r(SLAM10 - 0.08), (0.86, 1.12, 0.86), 0.04), SQ(r(SLAM10 + 0.04), (1.0, 1.0, 1.0), 0.1),
            k(1.2, look='camera'), MK(1.2, 'stareCamera', [0.45, 1.5])]),   # (review 1) it steps aside as the jar comes down (the jar never came down)
        act('mec', [-1.3, 0, -0.9], 40, 'walk', 'neutral', keys=[k(0.0, to=ME10, dur=0.7, clip='walk', then='stand', ease='out'), k(0.0, look=[0.0, 0.9, 0.0]), k(0.0, toon=JAR(1.55, {'lid': 0.55, 'mouth': 'smirk'}), toonDur=0.0),
            k(r(SLAM10 - 0.12), toon=JAR(0.84, {'lid': 0.3, 'mouth': 'clench'}), toonDur=0.1, toonEase='in'), k(r(SLAM10 + 0.25), toon=JAR(0.84, {'lid': 0.45, 'mouth': 'line'}), toonDur=0.15), k(1.35, look=DODGE10)])],
        props=[P('table10', 'desk', pos=[0.0, 0, 0.0], opts={'w': 1.2}), P('bocal10', 'glassJar', on={'actor': 'mec', 'hand': 'R', 'offset': [0.06, -0.06, 0.08]}, scale=1.1, keys=[k(SLAM10, detach=True)])],   # a clear glass jar (an opaque white box)
        cams=[FC(0.0, [1.45, 1.35, 2.3], [[MO10[0], 1.2, MO10[2]], [ME10[0], 2.45, ME10[2]], [ME10[0], 0.6, ME10[2]], [DODGE10[0], 0.76, DODGE10[2]]], top=0.16, bottom=0.78)])
st.cue('sfx:tiptoe', 'S10', 0.2, 0.12); st.cue('sfx:clink', 'S10', SLAM10, 0.3)

# 11: it filed a complaint. At the gendarmerie desk, from in front of it: the moustache on the desk leans back and points a long arm at him, snapping
#     forward; the gendarme types behind it
D11 = st.dur('S11'); MO11 = [-4.35, 0.76, -1.1]; ME11 = [-3.25, 0, 0.35]
st.shot('S11', 'office', actors=[
        act('flic', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 1.1, -1.2]), *[k(r(0.1 + 0.14 * j), toon={'reach': {'L': [-4.8, r(0.85 + 0.03 * (j % 2)), -1.55, 1, 0.03], 'R': [-4.4, r(0.88 - 0.03 * (j % 2)), -1.55, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.5}}, toonDur=0.06) for j in range(8)]]),
        act('mous', MO11, 35, 'stand', 'angry', scale=MS, keys=[MK(0.0, 'stand', [1.15]), k(0.0, look=[ME11[0], 1.9, ME11[2]]), LAY(0.08, -0.28, 0.18, 'inOut'),   # it leans back...
            MK(0.32, 'point', [1.15]), LAY(0.32, 0.22, 0.06), SQ(0.32, (0.86, 1.18, 0.86), 0.05), LAY(0.42, -0.06, 0.08, 'inOut'), LAY(0.52, 0.0, 0.1), SQ(0.45, (1.0, 1.0, 1.0), 0.1)]),   # ...and snaps forward into the point, overshoots, settles
        act('mec', ME11, -40, 'stand', 'neutral', keys=[k(0.0, look=[MO11[0], 1.0, MO11[2]]), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0), k(0.5, toon={'sq': [1.02, 0.97, 1.02], 'face': {'lid': 0.2, 'eye': 0.3, 'mouth': 'line'}}, toonDur=0.05)])],
        props=[P('pc11', 'laptop', pos=[-4.6, 0.76, -1.6], ry=180), P('gend11', 'signBoard', pos=[-4.4, 1.6, -3.55], opts={'text': 'GENDARMERIE', 'bg': P_NAVY, 'fg': '#FFFFFF', 'w': 1.8, 'h': 0.4, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [-3.9, 1.35, 1.9], [[-4.6, 2.2, -2.15], [MO11[0], 1.2, MO11[2]], [MO11[0], 0.76, MO11[2]], [ME11[0], 2.45, ME11[2]], [ME11[0], 0.3, ME11[2]]], top=0.16, bottom=0.78, inside=(-6.8, 6.8, 0.5, 3.0, -3.3, 9.0))])   # (review 1) in front of the desk, inside the room (the camera had backed into the side wall: a blank cream frame)
st.cue('sfx:typing', 'S11', 0.1, 0.12); st.cue('sfx:whoosh', 'S11', 0.32, 0.15)

# 12: the judge sentenced him to stay shaved. The judge brings the gavel down, then holds a big razor out to the side; in the dock in front, him,
#     three-quarter to us, his bare lip; a blink at us (RASÉ)
D12 = st.dur('S12'); BANG12 = 0.55; ME12 = [1.45, 0, -1.3]
GV = lambda y, L=None, f=None: {'reach': {'R': [0.4, y, -3.3, 1, 0.03], **({'L': L} if L else {})}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f or {'lid': 0.1, 'brow': -0.7, 'mouth': 'line'}}
st.shot('S12', 'courtroom', actors=[
        act('juge', [0.0, 0.3, -4.0], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=GV(2.6, f={'lid': 0.2, 'brow': -0.5}), toonDur=0.0), k(r(BANG12 - 0.06), toon=GV(2.75, f={'lid': 0.2, 'brow': -0.6}), toonDur=0.06),
            k(BANG12, toon={**GV(1.5, f={'lid': 0.0, 'brow': -0.7, 'mouth': 'open'}), 'sq': [1.05, 0.95, 1.05]}, toonDur=0.05, toonEase='in'),
            k(r(BANG12 + 0.45), toon=GV(1.5, [-1.0, 2.45, -3.45, 1, 0.03]), toonDur=0.15, toonEase='out'), *[k(r(BANG12 + 0.7 + 0.12 * j), toon=GV(1.5, [r(-1.0 + (0.07 if j % 2 else -0.05)), 2.47, -3.45, 1, 0.03]), toonDur=0.06) for j in range(5)]]),   # (review 1) the razor held out to his side (his arm crossed his face)
        act('mec', ME12, 15, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 2.4, -4.0]), k(0.0, toon=LIP, toonDur=0.0), k(r(BANG12 + 0.05), toon={'sq': [1.02, 0.97, 1.02], 'face': {'lid': 0.2, 'eye': 0.3}}, toonDur=0.05),
            k(r(BANG12 + 0.6), look='camera'), k(r(BANG12 + 0.85), toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(r(BANG12 + 1.0), toon=LIP, toonDur=0.1)])],   # turned to us: the bare lip, the blink (review 1: seen from behind)
        props=[P('gav12', 'gavel', on={'actor': 'juge', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}), P('raz12', 'razor', on={'actor': 'juge', 'hand': 'L', 'offset': [0.0, 0.0, 0.03]}, scale=2.2)],
        cams=[FC(0.0, [1.9, 1.7, 2.5], [[0.0, 2.75, -4.0], [-1.0, 2.6, -3.45], [ME12[0], 2.45, ME12[2]], [ME12[0], 1.2, ME12[2]]], top=0.2, bottom=0.76)])
st.cue('clang', 'S12', BANG12, 0.4); st.cue('sfx:whoosh', 'S12', r(BANG12 + 0.45), 0.12)

# 13: the moustache became a minister. On the minister's desk under the flag it signs a stack of papers with a fountain pen, scribble after scribble
D13 = st.dur('S13'); MO13 = [-4.6, 0.76, -1.6]
st.shot('S13', 'office', actors=[act('mous', MO13, 0, 'stand', 'neutral', scale=MS, keys=[MK(0.0, 'drawMid', [0.6, 1.5]), k(0.0, look=[-4.5, 0.78, -1.25]), *[SQ(r(0.25 + 0.4 * j), (1.04, 0.96, 1.04), 0.05) for j in range(4)], k(1.6, look='camera')])],   # (review 1) a pen and the signing (none)
        props=[P('stylo13', 'pen', on={'actor': 'mous', 'hand': 'R', 'offset': [0.0, -0.02, 0.02]}, scale=1.5), P('flag13', 'flag', pos=[-5.4, 0, -2.1], opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True}),
               *[P(f'pap13{j}', 'slab', pos=[-4.45, r(0.77 + 0.012 * j), -1.3], opts={'w': 0.3, 'h': 0.01, 'd': 0.4, 'color': '#FBF8EE', 'noShadow': True}) for j in range(8)],
               P('min13', 'signBoard', pos=[-4.6, 1.75, -3.55], opts={'text': 'MINISTÈRE', 'bg': P_NAVY, 'fg': '#FFFFFF', 'w': 1.6, 'h': 0.38, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [-4.2, 1.15, 0.2], [[MO13[0], 1.2, MO13[2]], [MO13[0], 0.76, MO13[2]], [-4.9, 1.0, MO13[2]], [-4.3, 1.0, MO13[2]], [-5.4, 1.9, -2.1]], top=0.18, bottom=0.76)])
for j in range(4): st.cue('sfx:scratch', 'S13', r(0.2 + 0.4 * j), 0.1)

# 14: then president. Behind the lectern between the flags, big and centred, it gives a royal wave; flashes go off in front of it
D14 = st.dur('S14'); FL14 = [0.12, 0.3, 0.48, 0.7, 0.88, 1.05]
st.shot('S14', 'pressRoom', setOpts={'backdrop': 'PRÉSIDENCE', 'fontScale': 0.6, 'podium': False, 'bg': '#5878A8', 'wall': '#4C6A96'}, actors=[act('mous', [0.0, 1.12, 0.0], 0, 'stand', 'happy', scale=MS, keys=[MK(0.0, 'royalWave', [0.85], freq=8.0), k(0.0, look='camera')])],   # (review 1) a lighter backdrop, the set's microphones gone (they sat on its eyes)
        props=[P('pod14', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), *[P(f'fl14{j}', 'flag', pos=[r(-0.95 + 1.9 * j), 0, -0.7], opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True}) for j in range(2)],
               P('flash14', 'flashBursts', pos=[0.0, 1.45, 0.75], face='camera', opts={'n': 6, 'w': 1.4, 'h': 0.9, 'at': FL14})],
        cams=[FC(0.0, [0.15, 1.38, 2.2], [[0.0, 1.6, 0.0], [0.0, 1.0, 0.2], [-0.32, 1.3, 0.0], [0.32, 1.3, 0.0], [-0.95, 2.2, -0.7], [0.95, 2.2, -0.7]], top=0.18, bottom=0.78)])
for t_ in FL14: st.cue('sfx:click', 'S14', t_, 0.18)

# 15: the man applied to be its assistant. A waiting room: he sits on a chair, his CV on his knees, deadpan; his eyes go to the door first, then his head
D15 = st.dur('S15')
CVP = {'touch': {'R': ['torso', -0.08, 0.15, 0.32, 1, 0.02], 'L': ['torso', 0.08, 0.15, 0.32, 1, 0.02]}, 'hands': {'R': 'pinch', 'L': 'pinch'}}
st.shot('S15', 'office', actors=[act('mec', [0.6, 0, 0.2], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={**CVP, **LIP}, toonDur=0.0),
            k(0.9, toon={**CVP, 'face': {'lid': 1.0}}, toonDur=0.08), k(1.02, toon={**CVP, **LIP}, toonDur=0.1),
            k(1.35, toon={**CVP, 'face': {'lid': 0.45, 'mouth': 'line', 'gx': 0.7}}, toonDur=0.12), k(1.5, look=[2.0, 1.6, -1.0]),   # (review 1) the eyes lead, the head follows (a two-frame snap)
            k(1.9, toon={**CVP, 'face': {'lid': 0.45, 'mouth': 'line', 'gx': -0.1}}, toonDur=0.12), k(2.02, look='camera'), k(2.12, toon={**CVP, 'face': {'lid': 1.0}}, toonDur=0.05), k(2.2, toon={**CVP, **LIP}, toonDur=0.08)])],
        props=[P('chaise15', 'chair', pos=[0.6, 0, 0.2]), P('cv15', 'paperSheet', on={'actor': 'mec', 'hand': 'R', 'offset': [0.08, 0.04, 0.02]}, opts={'w': 0.24, 'h': 0.32, 'lines': ['CV'], 'bright': True})],
        cams=[FC(0.0, [1.2, 1.3, 2.4], [[0.6, 1.9, 0.2], [0.6, 0.0, 0.2]], top=0.2, bottom=0.78)])

# 16: it said no. Front-on on the president's desk: it holds his CV out in front of it, closes its eyes and shakes its whole body no (NON)
D16 = st.dur('S16'); MO16 = [-4.6, 0.76, -1.6]
st.shot('S16', 'office', actors=[act('mous', MO16, 0, 'stand', 'neutral', scale=MS, keys=[MK(0.0, 'readPhone', [0.15]), k(0.0, look=[-4.6, 0.86, -1.2]), MK(0.32, 'shakeHead', []), k(0.32, expr='closed'), SQ(0.32, (1.05, 0.95, 1.05), 0.05)])],   # (review 1) the eyes shut, the body shakes no (eyes open, no shake)
        props=[P('cv16', 'paperSheet', on={'actor': 'mous', 'joint': 'head', 'offset': [0.0, -0.03, 0.17]}, face='camera', opts={'w': 0.2, 'h': 0.14, 'lines': ['CV'], 'bright': True})],
        cams=[FC(0.0, [-4.55, 1.05, -0.55], [[MO16[0], 1.18, MO16[2]], [MO16[0], 0.76, MO16[2]], [-4.88, 0.98, MO16[2]], [-4.32, 0.98, MO16[2]]], top=0.18, bottom=0.74)])
st.cue('sfx:paper', 'S16', 0.1, 0.15); st.cue('sfx:whoosh', 'S16', 0.4, 0.1)

# 17: not hairy enough. Close on him: his bare upper lip; a look at us, deadpan
D17 = st.dur('S17')
st.shot('S17', 'office', actors=[act('mec', [0.6, 0, 0.2], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=LIP, toonDur=0.0), k(0.45, toon={'face': {'lid': 0.45, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.2), k(0.85, toon=LIP, toonDur=0.2),
            k(1.45, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.07), k(1.57, toon=LIP, toonDur=0.1)])],
        props=[P('chaise17', 'chair', pos=[0.6, 0, 0.2])],
        cams=[FC(0.0, [0.75, 1.75, 1.3], [[0.6, 2.05, 0.2], [0.6, 1.35, 0.2]], top=0.16, bottom=0.74)])

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("La moustache", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'mous': {'type': 'creature', 'name': 'moustache', 'opts': {'seed': 671, 'armY': 0.55, 'armX': 0.24, 'breath': 0.03}},   # (review 1) the arms from under the wings (on top they read as horns); a breath
    'flic': {'preset': 'cop', 'seed': 672, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 673, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
