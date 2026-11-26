#!/usr/bin/env python3
"""make_critic.py CONFIG: write a round-N critic folder (brief.md, words.md, build.sh; critic-instructions.md and the style reference copied from
a template folder) for a story from a config module (see configs/*.py). Shot windows, line timings and title-card times are read from the story's
JSON, timeline and cards.txt, so the brief cannot carry another episode's numbers."""
import json, os, shutil, sys, importlib.util
SP = '/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad'
ROOT = '/home/user/myownshit/absurd-shorts'
spec = importlib.util.spec_from_file_location('cfg', sys.argv[1]); cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
st, rnd = cfg.STORY, cfg.ROUND
C = f'{SP}/critic/{st}{rnd}'; os.makedirs(C, exist_ok=True)
T = f'{SP}/critic/{cfg.TEMPLATE}'
for f in ('critic-instructions.md', 'style_reference_previous_episode.jpg'): shutil.copy(f'{T}/{f}', f'{C}/{f}')
d = json.load(open(f'{ROOT}/scripts-fr/story_{st}.json', encoding='utf-8'))
shots = {sc['id']: (sc['start'], sc['start'] + sc['duration']) for sc in d['scenes']}
total = sum(sc['duration'] for sc in d['scenes'])
tl = json.load(open(f'{ROOT}/stories7/{st}/timeline.json', encoding='utf-8'))['lines']
plan = [(sc['id'], sc['lines'][0] if sc.get('lines') else None) for sc in d['scenes']]
cards_raw = open(f'{ROOT}/stories7/{st}/cards.txt', encoding='utf-8').read().strip()
cards = []
for c in __import__('re').split(r',(?=S\d+[a-z]*@)', cards_raw):   # a card's own text may hold a comma (0,01 €)
    sh, rest = c.split('@'); at, word = rest.split(':', 1); cards.append((word, shots[sh][0] + float(at), sh))
card_txt = ', '.join(f"{w} over {cfg.CARD_WHAT[w]} from {t:.2f} s" for w, t, _ in cards)
# which line each shot speaks (a shot that starts mid-line says the rest of it)
line_of = {}
for sid, (a, b) in shots.items():
    best = None
    for l in tl:
        ov = min(b, l['speech_end']) - max(a, l['speech_start'])
        if ov > 0.05 and (best is None or ov > best[0]): best = (ov, l)
    line_of[sid] = best[1] if best else None
words = ['# Words and timing (narration, French; English gloss in brackets)', '']
for l in tl:
    sh = [s for s, (a, b) in shots.items() if a < l['speech_end'] - 0.05 and b > l['speech_start'] + 0.05]
    win = ', '.join(f"{s} {shots[s][0]:.2f}-{shots[s][1]:.2f}" for s in sh)
    words.append(f"- {l['id']} {l['speech_start']:.2f}-{l['speech_end']:.2f} s: « {l['text']} » [{cfg.GLOSS[l['id']]}] (shot{'s' if len(sh) > 1 else ''} {win})")
open(f'{C}/words.md', 'w', encoding='utf-8').write('\n'.join(words) + '\n')
H = open(f'{T}/brief.md', encoding='utf-8').read().split('\n')
head = [x for x in H if x.startswith('**The request') or x.startswith('**What "this style" is')]
brief = ['# Brief', '', head[0], '', head[1], '',
         f"**Audience and channel:** French-speaking TikTok / Instagram Reels / YouTube Shorts viewers. 9:16 vertical, 1080x1920, 30 fps, about {total:.1f} s. "
         f"Captions sit at about 77-83 % of the frame height and the title cards near the top (7-18 %; {len(cards)} in this episode: {card_txt}), so the important "
         "picture content should avoid those two bands where possible.", '',
         "**Fixed choices (not to be changed):** the series style above (models, narrator voice, music bed), the story structure of the series (a hook naming the "
         "man and the absurd event, an institution that takes it literally, escalation, a twist, a dry aside) and the script of this episode (see words.md; the "
         "narration is already recorded, so each shot's length is set by its line).", '',
         f"**What is new in this episode (the thing to judge):** {cfg.NEW}", '',
         f"**Deliberate choices in this episode:** {cfg.CHOICES}", '',
         f"**This episode:** \"{cfg.TITLE}\". {cfg.SUMMARY}", '',
         '**The intended gags, shot by shot (judge what the evidence shows; times are the shot windows in the film):**', '']
for sid, (a, b) in shots.items():
    brief.append(f"- {sid} {a:.2f}-{b:.2f} s: {cfg.SHOTS[sid]}")
brief += ['', cfg.ROUND_NOTE]
open(f'{C}/brief.md', 'w', encoding='utf-8').write('\n'.join(brief) + '\n')
L = ','.join(f"{n}:{t}" for n, t, _ in cfg.STILLS)
CARD = ','.join(n for n, _, c in cfg.STILLS if c)
D = {n: desc for n, _, desc in [(n, t, cfg.STILL_DESC[n]) for n, t, _ in cfg.STILLS]}
pairs = ','.join(cfg.PAIRS)
M = [(f"motion_{p.split('+')[0]}_{p.split('+')[-1]}.jpg" if '+' in p else f'motion_{p}.jpg', cfg.PAIR_DESC[p]) for p in cfg.PAIRS]   # critic_final names a strip by its first and last shot (S01_S03 for S01+S02+S03)
V = f'{SP}/s7/{st}/draft{cfg.DRAFT}.mp4'
bs = f'''#!/bin/bash
# build.sh: the evidence of review {rnd} of « {cfg.TITLE} » (story {cfg.NUMBER}) from draft {cfg.DRAFT}: overview sheets, motion strips, stills, evidence.txt, prompts
# (the stills are taken from the draft itself, 576x1024 in the final look without captions, with the band lines drawn on; nothing is rendered; written by make_critic.py)
SP={SP}; C=$SP/critic/{st}{rnd}; V={V}
cd {ROOT} || exit 1
L="{L}"
CARD="{CARD}"
if [ "$1" = "stills" ]; then
python3 - "$V" "$C" "$L" "$CARD" <<'PY'
import sys, cv2
V, C, L, CARD = sys.argv[1:5]; card = set(CARD.split(',')) if CARD else set()
c = cv2.VideoCapture(V); NF = int(c.get(cv2.CAP_PROP_FRAME_COUNT)); FR = round(c.get(cv2.CAP_PROP_FPS) or 30)
for x in L.split(','):
    nm, t = x.split(':'); f = min(NF - 1, round(float(t) * FR)); c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = c.read()
    if not ok: print('could not read', nm, t); continue
    im = cv2.resize(im, (576, 1024), interpolation=cv2.INTER_AREA); h, w = im.shape[:2]
    for k in (0.77, 0.83): cv2.line(im, (0, int(h * k)), (w, int(h * k)), (255, 0, 255), 1)
    if nm in card:
        for k in (0.07, 0.18): cv2.line(im, (0, int(h * k)), (w, int(h * k)), (255, 255, 0), 1)
    cv2.imwrite(f'{{C}}/frame_{{nm}}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 92]); print('still', nm, t, 'frame', f)
print(len(L.split(',')), 'stills')
PY
echo STILLS_DONE; exit 0
fi
python3 $SP/tools/critic_final.py {st} $V $C "{pairs}" "x:1.0" > $C/critic_final.log 2>&1; rm -f $C/frame_x.jpg
python3 - "$C" "$L" "$CARD" <<'PY'
import sys, os, json
C, L, CARD = sys.argv[1:4]; card = set(CARD.split(','))
D = json.loads({json.dumps(json.dumps(D, ensure_ascii=False))})
M = json.loads({json.dumps(json.dumps(M, ensure_ascii=False))})
ev = [f"{{C}}/overview_60pct.jpg — one frame per shot ({min(shots)}-{max(shots)}) at 60 % of each shot, from the 576x1024 draft (no captions, no title card)",
      f"{{C}}/overview_85pct.jpg — one frame per shot ({min(shots)}-{max(shots)}) at 85 % of each shot, from the draft"]
ev += [f"{{C}}/{{f}} — {{d}}" for f, d in M]
for x in L.split(','):
    nm, t = x.split(':'); cd = '; cyan lines = title card band' if nm in card else ''
    ev.append(f"{{C}}/frame_{{nm}}.jpg — full frame at {{float(t):.2f}} s ({{D[nm]}}), from the draft (final look, no captions); magenta lines = caption band{{cd}}")
ev.append(f"{{C}}/style_reference_previous_episode.jpg — series reference: one frame per shot of a previous episode as delivered (captions and title cards on; older flat look, older rigid puppets)")
missing = [e.split(' — ')[0] for e in ev if not os.path.exists(e.split(' — ')[0]) or os.path.getsize(e.split(' — ')[0]) == 0]
open(f'{{C}}/evidence.txt', 'w').write('\\n'.join(f'E{{i + 1}} {{e}}' for i, e in enumerate(ev)) + '\\n')
print(len(ev), 'evidence items; missing:', missing)
ROLES = json.loads({json.dumps(json.dumps(cfg.ROLES, ensure_ascii=False))})
for role, focus in ROLES:
    p = [focus, f"First read in full: {{C}}/critic-instructions.md, {{C}}/brief.md , {{C}}/words.md.", {json.dumps(cfg.ROUND_LINE)},
         "Open every image listed below with your image-viewing tool before scoring, or reply `Cannot view images` with no score.",
         f"Open only the files listed here and frames you render; write only to {{C}}-frames/{{role}}.",
         "Do not load the Tesseract skills or their references, or change the project or deliverable. You have no way to render more frames for this piece: list any open question under Not evaluated.",
         "Reply in the form in critic-instructions.md, listing Viewed items by ID. Return the whole report as your final message (do not rely on writing a report file).",
         "Evidence:", open(f'{{C}}/evidence.txt').read()]
    open(f'{{C}}/prompt_{{role}}.txt', 'w').write('\\n'.join(p))
PY
ls $C | wc -l; tail -2 $C/critic_final.log
'''
open(f'{C}/build.sh', 'w', encoding='utf-8').write(bs)
miss = [s for s in shots if s not in cfg.SHOTS]
print(C, 'written;', len(shots), 'shots,', len(tl), 'lines,', len(cards), 'cards; shots without a description:', miss)
