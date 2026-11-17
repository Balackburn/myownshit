#!/usr/bin/env python3
"""make_config1.py SPEC.py: write configs/<story>1.py (a round-1 critic config) from a short spec: the story-specific prose (NEW, CHOICES, SUMMARY,
GLOSS, CARD_WHAT, ANIM_GAGS, ART_FOCUS) is written by hand in the spec; the shot list (the words each shot speaks, from the timeline's word timings,
and what it shows, from the '# N:' comment above each shot in scripts-fr/story_<story>.py), the stills (one per shot, after the card when there is
one), the strip groups and the roles are filled in here."""
import json, re, sys, importlib.util
import os as _os
PIPE = _os.environ.get('PIPE', '/tmp/pipe')
PIPELINE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
ROOT = _os.path.dirname(PIPELINE_DIR)
REPO = _os.path.dirname(ROOT)
_os.makedirs(f'{PIPE}/critic/configs', exist_ok=True)
SP = PIPE
spec = importlib.util.spec_from_file_location('spec', sys.argv[1]); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
st = S.STORY
d = json.load(open(f'{ROOT}/scripts-fr/story_{st}.json', encoding='utf-8'))
scenes = [(sc['id'], sc['start'], sc['start'] + sc['duration']) for sc in d['scenes']]
tl = json.load(open(f'{ROOT}/stories7/{st}/timeline.json', encoding='utf-8'))['lines']
cards = {}
for c in re.split(r',(?=S\d+@)', open(f'{ROOT}/stories7/{st}/cards.txt', encoding='utf-8').read().strip()):   # a card's own text may hold a comma (0,01 €)
    sh, rest = c.split('@'); at, word = rest.split(':', 1); cards[sh] = (float(at), word)
# the '# N:' comments: the first sentence paraphrases the line, the rest says what the shot shows
src = open(f'{ROOT}/scripts-fr/story_{st}.py', encoding='utf-8').read().split('\n')
desc, cur = {}, None
for ln in src:
    m = re.match(r'^# (\d+): (.*)$', ln)
    if m: cur = int(m.group(1)); desc[cur] = m.group(2).strip(); continue
    if cur is not None and re.match(r'^#\s{2,}', ln): desc[cur] += ' ' + ln.lstrip('#').strip(); continue
    cur = None
def body(n):
    t = desc.get(n, '')
    m = re.search(r'\.\.\.?\s|\.\s', t)
    rest = t[m.end():].strip() if m else t
    rest = re.sub(r'\s*\((?:[A-ZÀ-Ü0-9 ,\'’€\-]+)\)\s*$', '', rest)
    return rest[0].lower() + rest[1:] if rest else rest
words = []
for li, l in enumerate(tl):
    ws = l.get('words') or []
    for wi, w in enumerate(ws): words.append((li, wi, len(ws), w['w'], (w['s'] + w['e']) / 2))
shots = {}
for sid, a, b in scenes:
    ws = [w for w in words if a <= w[4] < b]
    n = int(sid[1:])
    if ws:
        txt = ' '.join(w[3] for w in ws)
        pre = '' if ws[0][1] == 0 else '...'; post = '' if ws[-1][1] == ws[-1][2] - 1 else '...'
        frag = f'« {pre}{txt}{post} »'
    else:
        frag = '(no words)'
    card = f' ({cards[sid][1]} card)' if sid in cards else ''
    b_ = body(n).rstrip('.')
    shots[sid] = f'{frag}: {b_}{card}.'
stills, sdesc = [], {}
for sid, a, b in scenes:
    n = int(sid[1:])
    if sid in cards: t = min(b - 0.05, a + cards[sid][0] + 0.3)
    else: t = a + 0.6 * (b - a)
    name = f's{n:02d}'
    stills.append((name, round(t, 2), sid in cards))
    first = re.split(r'[;:]', body(n))[0].strip().rstrip('.')
    sdesc[name] = f'{sid}: {first}' + (f' ({cards[sid][1]} card)' if sid in cards else '')
lastid, la, lb = scenes[-1]
stills.append(('s_end', round(lb - 0.15, 2), False)); sdesc['s_end'] = f'{lastid}: the end hold'
pairs, grp, gdur = [], [], 0.0
for sid, a, b in scenes:
    if grp and (gdur + (b - a) > 4.6 or len(grp) == 3): pairs.append(grp); grp, gdur = [], 0.0
    grp.append(sid); gdur += b - a
if grp: pairs.append(grp)
pnames = ['+'.join(g) for g in pairs]
pdesc = {}
for i, g in enumerate(pairs):
    parts = '; '.join(re.split(r'[;:,]', body(int(s[1:])))[0].strip().rstrip('.') for s in g)
    span = f'{g[0]}-{g[-1]}' if len(g) > 1 else g[0]
    pdesc['+'.join(g)] = (f'every second frame (15 per second) of {span}: ' if i == 0 else f'{span}: ') + parts
robinet = open(f'{PIPELINE_DIR}/critic_template/robinet1.py', encoding='utf-8').read().split('\n')
anim_head = [l for l in robinet if l.startswith('ANIM_HEAD')][0]
tail = [l for l in robinet if l.startswith('ROUND_NOTE = ROUND_NOTE')][0]
R = repr
out = [f"STORY = {R(st)}; ROUND = 1; DRAFT = 1; NUMBER = {S.NUMBER}; TITLE = {R(S.TITLE)}; TEMPLATE = 'feu1'",
       f"CARD_WHAT = {R(S.CARD_WHAT)}", f"NEW = {R(S.NEW)}", f"CHOICES = {R(S.CHOICES)}", f"SUMMARY = {R(S.SUMMARY)}", f"GLOSS = {R(S.GLOSS)}",
       'SHOTS = {', *[f' {R(k)}: {R(v)},' for k, v in shots.items()], '}',
       "ROUND_NOTE = 'This is the first review of this film (round 1): no previous scores.'",
       "ROUND_LINE = 'This is the first review of this film: judge what the evidence shows, on its own merits.'",
       f"STILLS = {R(stills)}", f"STILL_DESC = {R(sdesc)}", f"PAIRS = {R(pnames)}", f"PAIR_DESC = {R(pdesc)}", anim_head,
       "ROLES = [('anim', ANIM_HEAD + " + R("Judge the running gag, " + S.ANIM_GAGS + ": does each step escalate and read, and is the timing right. For each gag: does it read in the time it is given, what is missing. Also judge the micro-movements you can see (blinks, eyes leading the head, breathing, the life in the holds) and whether anyone freezes.") + "),",
       "         ('art', " + R("You are the art director. Focus: craft against the brief and the supplied reference: the idea, composition and hierarchy of every shot at phone size, colour and light, " + S.ART_FOCUS + ", whether each gag's key pose has a clear silhouette, where the captions and the title cards fall on the picture, consistency with the series, and finish.") + ")]",
       '', tail, '']
open(f'{SP}/critic/configs/{st}1.py', 'w', encoding='utf-8').write('\n'.join(out))
print(f'configs/{st}1.py: {len(shots)} shots, {len(stills)} stills, {len(pnames)} strips')
for k, v in shots.items(): print(' ', k, v[:150])
