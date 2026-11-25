#!/usr/bin/env python3
"""next_config.py PREV_FOLDER STORY ROUND DRAFT NUMBER TITLE [TEMPLATE]: write configs/<story><round>.py for make_critic.py from the previous round's
folder (its brief, words, evidence and prompts): the roles come from that story's own prompts (never another story's), the new/choices/summary/shots
from its brief, the gloss from its words, the stills and strips from its evidence. Edit ROUND_NOTE, ROUND_LINE (and SHOTS or STILLS when the
staging changed) in the written file before running make_critic.py."""
import re, sys, os
import os as _os
PIPE = _os.environ.get('PIPE', '/tmp/pipe')
PIPELINE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
ROOT = _os.path.dirname(PIPELINE_DIR)
REPO = _os.path.dirname(ROOT)
_os.makedirs(f'{PIPE}/critic/configs', exist_ok=True)
SP = PIPE
P, story, rnd, draft, num, title = sys.argv[1:7]; tmpl = sys.argv[7] if len(sys.argv) > 7 else 'feu1'
b = open(f'{P}/brief.md', encoding='utf-8').read()
g = lambda pat: re.search(pat, b).group(1)
new = g(r"\*\*What is new in this episode \(the thing to judge\):\*\* (.*)"); cho = g(r"\*\*Deliberate choices in this episode:\*\* (.*)")
summ = re.search(r'\*\*This episode:\*\* ".*?"\. (.*)', b).group(1)
shots = dict(re.findall(r"^- (S\d\d) [0-9.]+-[0-9.]+ s:? (.*)$", b, re.M))
cards = dict(re.findall(r"(?:: |, )([A-ZÀ-Ý0-9][A-ZÀ-Ý0-9 ,'’€\-]*?) over (.*?) from [0-9.]+ s", b.split('**Audience')[1].split('\n')[0]))   # a card can be several words (MONUMENT HISTORIQUE) or hold a comma (0,01 €)
w = open(f'{P}/words.md', encoding='utf-8').read(); gl = dict(re.findall(r"^- (L\d\d) [^\[]*\[(.*?)\]", w, re.M))
ev = open(f'{P}/evidence.txt', encoding='utf-8').read()
st = re.findall(r"frame_([a-z0-9_]+)\.jpg — full frame at ([0-9.]+) s \((.*?)\), from the draft", ev)
cardst = set(re.findall(r"frame_([a-z0-9_]+)\.jpg — [^\n]*title card band", ev))
pairs = re.findall(r"motion_([A-Z0-9_]+)\.jpg — (.*)", ev)
def _expand(p):   # (15 Nov) a strip is named by its first and last shot: S11_S13 is S11, S12 and S13 (read as two shots, rounds 2 and 3 lost the middle one)
    ids = p.split('_')
    if len(ids) != 2: return p
    a_, b_ = int(re.match(r'\d+', ids[0][1:]).group()), int(re.match(r'\d+', ids[1][1:]).group())
    return p if b_ - a_ <= 1 else '_'.join('S%02d' % i for i in range(a_, b_ + 1))
pairs = [(_expand(p), d) for p, d in pairs]
roles = []
for role in ('anim', 'art'):
    t = open(f'{P}/prompt_{role}.txt', encoding='utf-8').read().split('\nFirst read in full:')[0].strip(); roles.append((role, t))
out = [f"# round-{rnd} review of « {title} » (story {num}) from draft {draft}: written by next_config.py from {os.path.basename(P)} (its own roles, brief, words, evidence)",
       f"STORY = {story!r}; ROUND = {int(rnd)}; DRAFT = {int(draft)}; NUMBER = {int(num)}; TITLE = {title!r}; TEMPLATE = {tmpl!r}",
       f"CARD_WHAT = {cards!r}", f"NEW = {new!r}", f"CHOICES = {cho!r}", f"SUMMARY = {summ!r}", f"GLOSS = {gl!r}", f"SHOTS = {shots!r}",
       "ROUND_NOTE = 'EDIT ME'", "ROUND_LINE = 'EDIT ME'",
       f"STILLS = {[(n, float(t), n in cardst) for n, t, _ in st]!r}", f"STILL_DESC = {dict((n, d) for n, t, d in st)!r}",
       f"PAIRS = {[p.replace('_', '+') for p, _ in pairs]!r}", f"PAIR_DESC = {dict((p.replace('_', '+'), d) for p, d in pairs)!r}",
       f"ROLES = {roles!r}"]
F = f'{SP}/critic/configs/{story}{rnd}.py'; open(F, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(F, len(shots), 'shots', len(gl), 'lines', len(st), 'stills', len(pairs), 'strips', 'cards', cards)
