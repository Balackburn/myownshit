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

# 1: the hook. At the bathroom mirror (we are the mirror): the razor goes under his nose; the moustache drops off his lip
D1 = st.dur('S01'); SHAVE1 = 0.75; ME1 = [0.0, 0, -1.6]
st.shot('S01', 'laundryRoom', setOpts={'washer': False}, actors=[
        act('mec', ME1, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['face', -0.1, 0.18, 0.12, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(r(SHAVE1 - 0.3), toon={'touch': {'R': ['face', 0.08, 0.17, 0.12, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.25, toonEase='inOut'),   # the razor along his lip...
            k(r(SHAVE1 + 0.1), toon={'touch': {'R': ['face', 0.16, 0.05, 0.14, 1, 0.02]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.4, 'gy': 0.6, 'mouth': 'line'}}, toonDur=0.12), k(r(SHAVE1 + 0.1), look=[0.0, 0.3, -1.0])]),   # ...and he looks down after it
        act('mous', [0.0, 1.92, r(ME1[2] + 0.115)], 0, 'stand', 'neutral', scale=0.22, keys=[k(0.0, toon={'face': {'lid': 1.0}}, toonDur=0.0),
            k(SHAVE1, to=[0.18, 0.0, r(ME1[2] + 0.5)], dur=0.32, ease='in'), k(r(SHAVE1 + 0.34), toon={'sq': [1.3, 0.7, 1.3], 'face': {'lid': 1.0}}, toonDur=0.04), k(r(SHAVE1 + 0.42), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.0, 'eye': 0.4}}, toonDur=0.08, toonEase='out')])],   # it drops, squashes, opens its eyes
        props=[P('raz1', 'slab', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, opts={'w': 0.03, 'h': 0.16, 'd': 0.03, 'color': '#3A7BD5'})],
        cams=[FC(0.0, [0.25, 1.75, 0.6], [[0.0, 2.45, ME1[2]], [0.0, 1.0, ME1[2]], [0.25, 0.0, r(ME1[2] + 0.5)]], top=0.14, bottom=0.8)])
st.cue('sfx:stretch', 'S01', 0.3, 0.15); st.cue('sfx:pop', 'S01', SHAVE1, 0.25); st.cue('sfx:boing', 'S01', r(SHAVE1 + 0.34), 0.2)

# 2: the moustache left on its own. Low on the bathroom floor: it trots off to the door on its little legs; behind it his legs, his face looking down
D2 = st.dur('S02')
st.shot('S02', 'laundryRoom', setOpts={'washer': False}, actors=[
        act('mous', [0.2, 0, -1.1], 90, 'walk', 'neutral', scale=MS * 0.6, keys=[k(0.0, to=[2.6, 0, -0.6], dur=D2, clip='walk', ease='linear', face='keep'), k(0.0, look=[4.0, 0.2, -0.4])]),
        act('mec', ME1, 0, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 0.0, -1.0]), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.3, 'gy': 0.6, 'mouth': 'line'}}, toonDur=0.0)])],
        cams=[FC(0.0, [1.6, 0.55, 1.6], [[0.0, 2.45, ME1[2]], [2.6, 0.0, -0.6], [0.2, 0.0, -1.1]], top=0.14, bottom=0.8, drift=(0.6, 0.0, 0.0))])
st.cue('sfx:stepSoft', 'S02', 0.2, 0.15); st.cue('sfx:stepSoft', 'S02', 0.6, 0.15); st.cue('sfx:stepSoft', 'S02', 1.0, 0.15)

# 3: it took the bus. At the stop: the city bus pulls up, the moustache hops up the step and in
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, actors=[
        act('mous', [5.6, 0, 1.2], -90, 'hop', 'neutral', scale=MS, keys=[k(0.0, to=[4.3, 0.25, 0.4], dur=r(D3 - 0.2), ease='inOut', face='keep'), k(0.0, look=[3.0, 0.8, 0.0])])],
        props=[P('bus3', 'cityBus', pos=[3.4, 0, -12.0], ry=-90, opts={'len': 7.6}, keys=[k(0.0, to=[3.4, 0, -1.6], dur=0.5, ease='out')])],
        cams=[FC(0.0, [8.4, 1.4, 4.2], [[5.6, 0.7, 1.2], [4.3, 0.0, 0.4], [3.4, 3.0, -1.6], [3.4, 0.0, 2.2]], top=0.16, bottom=0.8)])
st.cue('sfx:brake', 'S03', 0.35, 0.25)

# 4: it found a flat. A landing: it turns a key in a door bigger than it, a tiny suitcase at its side, and the door swings in
D4 = st.dur('S04')
st.shot('S04', 'immeubleHall', actors=[
        act('mous', [0.0, 0, 0.0], 180, 'stand', 'happy', scale=MS, keys=[k(0.0, look=[0.0, 0.6, -1.0]), k(0.0, toon={'reach': {'R': [0.05, 0.45, -0.2, 1, 0.02]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.7, look='camera')])],
        props=[P('valise4', 'suitcase', pos=[0.28, 0, 0.1], scale=0.35)],
        cams=[FC(0.0, [0.9, 0.7, 1.6], [[0.0, 0.7, 0.0], [0.0, 0.0, 0.0], [0.4, 0.0, 0.1], [0.0, 1.4, -0.4]], top=0.16, bottom=0.78)])
st.cue('sfx:click', 'S04', 0.35, 0.2)

# 5: and a job at the bank. Behind a counter, a little tie on, it stamps a form: bang, bang
D5 = st.dur('S05'); STAMPS = [0.35, 0.75, 1.15]
STAMP = lambda up: {'reach': {'R': [0.12, r(0.95 + (0.18 if up else 0.0)), 0.12, 1, 0.02]}, 'hands': {'R': 'grip'}}
st.shot('S05', 'office', actors=[act('mous', [-4.6, 0.76, -1.6], 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look='camera'), k(0.0, toon=STAMP(1), toonDur=0.0),
            *[kk for t_ in STAMPS for kk in (k(r(t_ - 0.08), toon=STAMP(1), toonDur=0.06), k(t_, toon={**STAMP(0), 'sq': [1.08, 0.92, 1.08]}, toonDur=0.05, toonEase='in'))]])],
        props=[P('desk5', 'desk', pos=[-4.6, 0, -1.4], opts={'w': 1.4}), P('form5', 'paperSheet', pos=[-4.45, 0.77, -1.2], rot=[-PI / 2, 0, 0], opts={'w': 0.3, 'h': 0.4, 'lines': ['FORMULAIRE'], 'stamp': {'text': 'OK', 'color': '#C2342A', 'at': STAMPS[0]}})],
        cams=[FC(0.0, [-4.2, 1.2, 0.4], [[-4.6, 1.2, -1.6], [-4.6, 0.75, -1.6], [-4.3, 0.75, -1.2]], top=0.2, bottom=0.76)])
for t_ in STAMPS: st.cue('thud', 'S05', t_, 0.2)

# 6: the tax office sent it a bill. It opens the letter: its eyes pop out on stalks
D6 = st.dur('S06'); POP6 = 0.75
st.shot('S06', 'livingRoom', setOpts={'sofa': False}, actors=[act('mous', [0.0, 0.0, -0.6], 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[0.0, 0.5, 0.0]),
            k(0.0, toon={'touch': {'R': ['head', -0.12, 0.05, 0.18, 1, 0.02], 'L': ['head', 0.12, 0.05, 0.18, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            k(POP6, toon={'touch': {'R': ['head', -0.12, 0.05, 0.18, 1, 0.02], 'L': ['head', 0.12, 0.05, 0.18, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [0.92, 1.12, 0.92], 'face': {'pop': 0.7, 'popLen': 0.16}}, toonDur=0.05, toonEase='out')])],
        props=[P('lettre6', 'paperSheet', on={'actor': 'mous', 'hand': 'R', 'offset': [0.08, 0.05, 0.03]}, opts={'w': 0.22, 'h': 0.3, 'lines': ['IMPÔTS', '', 'À PAYER'], 'bright': True})],
        cams=[FC(0.0, [0.5, 0.75, 1.2], [[0.0, 0.85, -0.6], [0.0, 0.0, -0.6]], top=0.18, bottom=0.78)])
st.cue('sfx:paper', 'S06', 0.15, 0.2); st.cue('sfx:boing', 'S06', POP6, 0.25)

# 7: it paid. At a counter it counts out banknotes, one, two, three, deadpan
D7 = st.dur('S07'); NOTES7 = [0.2, 0.45, 0.7]
st.shot('S07', 'office', actors=[act('mous', [-4.6, 0.76, -1.6], 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[-4.5, 0.77, -1.2]),
            *[kk for t_ in NOTES7 for kk in (k(t_, toon={'reach': {'R': [0.15, 0.8, 0.05, 1, 0.02]}, 'hands': {'R': 'pinch'}}, toonDur=0.08), k(r(t_ + 0.12), toon={'reach': {'R': [0.05, 0.86, -0.02, 1, 0.02]}, 'hands': {'R': 'pinch'}}, toonDur=0.08))]])],
        props=[P('desk7', 'desk', pos=[-4.6, 0, -1.4], opts={'w': 1.4}), *[P(f'note7{j}', 'banknote', pos=[r(-4.45 + 0.05 * j), r(0.775 + 0.004 * j), r(-1.2 + 0.02 * j)], rot=[-PI / 2, 0, r(0.2 * j)], opts={'w': 0.2}, keys=[k(0.0, visible=False), k(NOTES7[j], visible=True)]) for j in range(3)]],
        cams=[FC(0.0, [-5.3, 1.0, -0.2], [[-4.6, 1.2, -1.6], [-4.6, 0.75, -1.6], [-4.4, 0.75, -1.2]], top=0.2, bottom=0.76)])
for t_ in NOTES7: st.cue('sfx:cash', 'S07', t_, 0.15)

# 8: it stood for the town hall. On a crate in the square, a megaphone in its hand, a poster of itself behind it
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts={'clear': [-8.0, 8.0]}, actors=[act('mous', [6.4, 0.45, 0.0], -90, 'stand', 'angry', scale=MS, keys=[k(0.0, look='camera'),
            k(0.0, toon={'touch': {'R': ['head', 0.0, 0.08, 0.2, 1, 0.02]}, 'hands': {'R': 'grip'}}, toonDur=0.0), *[k(r(0.2 + 0.25 * j), toon={'touch': {'R': ['head', 0.0, 0.08, 0.2, 1, 0.02]}, 'hands': {'R': 'grip'}, 'sq': [1.0, 1.05 if j % 2 else 0.97, 1.0]}, toonDur=0.08) for j in range(5)]])],
        props=[P('caisse8', 'slab', pos=[6.4, 0.22, 0.0], opts={'w': 0.5, 'h': 0.45, 'd': 0.5, 'color': '#B98A5A'}), P('mega8', 'megaphone', on={'actor': 'mous', 'hand': 'R', 'offset': [0.0, 0.0, 0.06]}, scale=0.6),
               P('affiche8', 'signBoard', pos=[7.4, 0, -0.9], ry=-60, opts={'text': 'VOTEZ|MOUSTACHE', 'bg': '#2F62B5', 'fg': '#FFFFFF', 'w': 1.0, 'h': 1.3})],
        cams=[FC(0.0, [4.4, 1.0, 1.6], [[6.4, 1.3, 0.0], [6.4, 0.0, 0.0], [7.4, 1.9, -0.9]], top=0.18, bottom=0.78)])
st.cue('sfx:static', 'S08', 0.2, 0.2)

# 9: it won, with sixty per cent. In the town hall the moustache in the mayor's sash; the results board fills to its name; confetti (ÉLUE)
D9 = st.dur('S09')
st.shot('S09', 'mairie', setOpts={'plate': 'MAIRIE', 'map': False}, actors=[act('mous', [0.0, 0.76, 0.0], 0, 'celebrate', 'happy', scale=MS, keys=[k(0.0, look='camera')])],
        props=[P('table9', 'desk', pos=[0.0, 0, 0.0], opts={'w': 1.2}), P('res9', 'resultsBoard', pos=[1.1, 1.5, -1.2], ry=-20, opts={'name': 'MOUSTACHE', 'fillAt': 0.1, 'w': 1.4, 'h': 0.9}),
               P('ech9', 'slab', on={'actor': 'mous', 'joint': 'head', 'offset': [0.0, 0.1, 0.06]}, rot=[0, 0, 0.5], opts={'w': 0.5, 'h': 0.05, 'd': 0.02, 'color': '#2F62B5'}),
               P('conf9', 'confetti', pos=[0.3, 0.8, 0.0], opts={'w': 2.4, 'h': 2.0, 'd': 1.0, 'n': 90})],
        cams=[FC(0.0, [0.4, 1.3, 2.4], [[0.0, 1.25, 0.0], [0.0, 0.7, 0.0], [1.1, 2.0, -1.2], [1.8, 1.0, -1.2]], top=0.2, bottom=0.78)])
st.cue('sfx:fanfare', 'S09', 0.15, 0.2)

# 10: the man wanted it back. In the town hall corridor he creeps up behind it on tiptoe with an upturned jar
D10 = st.dur('S10')
st.shot('S10', 'mairie', setOpts={'plate': 'MAIRIE', 'map': False}, actors=[
        act('mous', [0.0, 0.76, 0.0], 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[0.0, 1.0, 2.0])]),
        act('mec', [-1.4, 0, -0.6], 60, 'walk', 'neutral', keys=[k(0.0, to=[-0.55, 0, -0.35], dur=r(D10 - 0.2), clip='walk', then='stand', ease='out', face='keep'), k(0.0, look=[0.0, 0.9, 0.0]),
            k(0.0, toon={'reach': {'R': [-0.2, 1.6, -0.2, 1, 0.02], 'L': [-0.35, 1.6, -0.1, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0)])],
        props=[P('table10', 'desk', pos=[0.0, 0, 0.0], opts={'w': 1.2}), P('bocal10', 'slab', on={'actor': 'mec', 'hand': 'R', 'offset': [0.06, 0.05, 0.05]}, opts={'w': 0.22, 'h': 0.26, 'd': 0.22, 'color': '#CFE7F2'})],
        cams=[FC(0.0, [1.3, 1.4, 2.6], [[0.0, 1.25, 0.0], [-0.55, 2.45, -0.35], [-0.55, 0.0, -0.35], [0.0, 0.7, 0.0]], top=0.16, bottom=0.78)])

# 11: it filed a complaint. At the police desk it stands on the desk and points a little arm at him; the policeman types
D11 = st.dur('S11')
st.shot('S11', 'office', actors=[
        act('flic', [-4.6, 0, -2.15], 0, 'sit', 'neutral', keys=[k(0.0, look=[-4.6, 1.1, -1.2]), *[k(r(0.1 + 0.14 * j), toon={'reach': {'L': [-4.8, r(0.85 + 0.03 * (j % 2)), -1.55, 1, 0.03], 'R': [-4.4, r(0.88 - 0.03 * (j % 2)), -1.55, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.5}}, toonDur=0.06) for j in range(8)]]),
        act('mous', [-4.3, 0.76, -1.1], 40, 'point', 'angry', scale=MS, keys=[k(0.0, look=[-3.2, 1.6, 0.5])]),
        act('mec', [-3.2, 0, 0.5], 160, 'stand', 'neutral', keys=[k(0.0, look=[-4.3, 1.0, -1.1]), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[P('desk11', 'desk', pos=[-4.6, 0, -1.4], opts={'w': 1.6}), P('pc11', 'laptop', pos=[-4.6, 0.76, -1.6], ry=180)],
        cams=[FC(0.0, [-2.0, 1.5, 1.8], [[-4.6, 2.3, -2.15], [-4.3, 1.2, -1.1], [-3.2, 2.45, 0.5], [-3.2, 0.2, 0.5]], top=0.16, bottom=0.78)])
st.cue('sfx:cluck', 'S11', 0.2, 0.15)

# 12: the judge sentenced him to stay shaved. The judge brings the gavel down and holds up a razor; the man in the dock, his lip bare (RASÉ)
D12 = st.dur('S12'); BANG12 = 0.55
st.shot('S12', 'courtroom', actors=[
        act('juge', [0.0, 0.3, -4.0], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.4, 2.6, -3.4, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'brow': -0.5}}, toonDur=0.0),
            k(BANG12, toon={'reach': {'R': [0.4, 1.5, -3.3, 1, 0.03], 'L': [-0.5, 2.6, -3.4, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.0, 'brow': -0.7, 'mouth': 'open'}}, toonDur=0.05, toonEase='in')]),
        act('mec', [1.6, 0, -1.4], -40, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 2.4, -4.0]), k(0.0, toon=LIP, toonDur=0.0), k(r(BANG12 + 0.05), toon={'sq': [1.02, 0.97, 1.02], 'face': {'lid': 0.2, 'eye': 0.3}}, toonDur=0.05)])],
        props=[P('gav12', 'gavel', on={'actor': 'juge', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}), P('raz12', 'slab', on={'actor': 'juge', 'hand': 'L', 'offset': [0.0, 0.05, 0.04]}, opts={'w': 0.05, 'h': 0.28, 'd': 0.05, 'color': '#3A7BD5'})],
        cams=[FC(0.0, [1.6, 1.8, 2.6], [[0.0, 2.85, -4.0], [1.6, 2.45, -1.4], [1.6, 0.6, -1.4], [-0.6, 2.9, -3.4]], top=0.18, bottom=0.76)])
st.cue('clang', 'S12', BANG12, 0.4)

# 13: the moustache became a minister. Behind a great desk under the flag it signs papers, a stack of them
D13 = st.dur('S13')
st.shot('S13', 'office', actors=[act('mous', [-4.6, 0.76, -1.65], 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[-4.5, 0.77, -1.25]),
            *[k(r(0.15 + 0.2 * j), toon={'reach': {'R': [r(0.1 + 0.05 * (j % 2)), 0.8, 0.12, 1, 0.02]}, 'hands': {'R': 'pinch'}}, toonDur=0.08) for j in range(6)]])],
        props=[P('desk13', 'desk', pos=[-4.6, 0, -1.4], opts={'w': 1.6}), P('flag13', 'flag', pos=[-5.6, 0, -2.0], opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True}),
               *[P(f'pap13{j}', 'slab', pos=[-4.25, r(0.77 + 0.012 * j), -1.3], opts={'w': 0.3, 'h': 0.01, 'd': 0.4, 'color': '#FBF8EE', 'noShadow': True}) for j in range(8)]],
        cams=[FC(0.0, [-4.0, 1.3, 0.8], [[-4.6, 1.25, -1.65], [-4.6, 0.6, -1.65], [-5.6, 2.2, -2.0], [-4.25, 0.9, -1.3]], top=0.18, bottom=0.76)])

# 14: then president. At a lectern between flags it waves; flashes go off
D14 = st.dur('S14'); FL14 = [0.2, 0.5]
st.shot('S14', 'pressRoom', actors=[act('mous', [0.0, 1.05, 0.0], 0, 'celebrate', 'happy', scale=MS, keys=[k(0.0, look='camera')])],
        props=[P('pod14', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), *[P(f'fl14{j}', 'flag', pos=[r(-1.2 + 2.4 * j), 0, -0.8], opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True}) for j in range(2)]],
        cams=[FC(0.0, [0.3, 1.5, 3.4], [[0.0, 1.65, 0.0], [0.0, 0.0, 0.2], [-1.2, 2.6, -0.8], [1.2, 2.6, -0.8]], top=0.18, bottom=0.78)])
for t_ in FL14: st.cue('sfx:click', 'S14', t_, 0.2)

# 15: the man applied to be its assistant. A waiting room: he sits on a chair, his CV on his knees, deadpan
D15 = st.dur('S15')
st.shot('S15', 'office', actors=[act('mec', [0.6, 0, 0.2], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'touch': {'R': ['torso', -0.08, 0.15, 0.32, 1, 0.02], 'L': ['torso', 0.08, 0.15, 0.32, 1, 0.02]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.0),
            k(0.9, toon={'touch': {'R': ['torso', -0.08, 0.15, 0.32, 1, 0.02], 'L': ['torso', 0.08, 0.15, 0.32, 1, 0.02]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 1.0}}, toonDur=0.08), k(1.02, toon={'touch': {'R': ['torso', -0.08, 0.15, 0.32, 1, 0.02], 'L': ['torso', 0.08, 0.15, 0.32, 1, 0.02]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, **LIP}, toonDur=0.1)])],
        props=[P('chaise15', 'chair', pos=[0.6, 0, 0.2]), P('cv15', 'paperSheet', on={'actor': 'mec', 'hand': 'R', 'offset': [0.08, 0.04, 0.02]}, opts={'w': 0.24, 'h': 0.32, 'lines': ['CV'], 'bright': True})],
        cams=[FC(0.0, [1.2, 1.3, 2.4], [[0.6, 1.9, 0.2], [0.6, 0.0, 0.2]], top=0.2, bottom=0.78)])

# 16: it said no. Behind the president's desk it reads the CV and shakes its head, its eyes closed (NON)
D16 = st.dur('S16')
st.shot('S16', 'office', actors=[act('mous', [-4.6, 0.76, -1.6], 0, 'stand', 'neutral', scale=MS, keys=[k(0.0, look=[-4.5, 0.85, -1.25]),
            k(0.0, toon={'touch': {'R': ['head', -0.12, 0.0, 0.2, 1, 0.02], 'L': ['head', 0.12, 0.0, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            *[k(r(0.35 + 0.16 * j), look=[r(-4.6 + (0.5 if j % 2 else -0.5)), 0.85, 0.0]) for j in range(4)], k(0.35, toon={'touch': {'R': ['head', -0.12, 0.0, 0.2, 1, 0.02], 'L': ['head', 0.12, 0.0, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.08)])],
        props=[P('desk16', 'desk', pos=[-4.6, 0, -1.4], opts={'w': 1.6}), P('cv16', 'paperSheet', on={'actor': 'mous', 'hand': 'R', 'offset': [0.08, 0.04, 0.02]}, opts={'w': 0.24, 'h': 0.32, 'lines': ['CV'], 'bright': True})],
        cams=[FC(0.0, [-4.75, 0.95, -0.7], [[-4.6, 1.3, -1.6], [-4.6, 0.9, -1.6]], top=0.18, bottom=0.74)])

# 17: not hairy enough. Close on him: his bare upper lip; a look at us, deadpan
D17 = st.dur('S17')
st.shot('S17', 'office', actors=[act('mec', [0.6, 0, 0.2], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=LIP, toonDur=0.0), k(0.45, toon={'face': {'lid': 0.45, 'mouth': 'line', 'gy': 0.5}}, toonDur=0.2), k(0.85, toon=LIP, toonDur=0.2)])],
        props=[P('chaise17', 'chair', pos=[0.6, 0, 0.2])],
        cams=[FC(0.0, [0.75, 1.75, 1.3], [[0.6, 2.05, 0.2], [0.6, 1.35, 0.2]], top=0.16, bottom=0.74)])

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("La moustache", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'mous': {'type': 'creature', 'name': 'moustache', 'opts': {'seed': 671}},
    'flic': {'preset': 'cop', 'seed': 672, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 673, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
