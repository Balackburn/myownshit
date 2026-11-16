#!/usr/bin/env python3
"""round_config.py STORY PREV_ROUND ROUND DRAFT NUMBER "TITLE" NOTE_FILE [fix_file]

The config of review round ROUND of a story, ready for make_critic.py:
  1. next_config.py copies the config of round PREV_ROUND and bumps the round and the draft;
  2. the shot descriptions (SHOTS) are rewritten from the staging comments of scripts-fr/story_STORY.py (`# N: gloss of the line. staging...`),
     so the critics read what the shots show NOW, not what they showed before the correction pass;
  3. ROUND_NOTE is the text of NOTE_FILE (what changed since the last round), ROUND_LINE the standing line of a later round.
Optional fix_file: lines `S07<TAB>description` that replace a shot's description (when the script comment is stale).
Run from absurd-shorts/. Then: python3 make_critic.py <config>.
"""
import re, subprocess, sys
SP = '/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad'
story, prev, rnd, draft, num, title, note_file = sys.argv[1:8]
fix_file = sys.argv[8] if len(sys.argv) > 8 else None
r = subprocess.run(['python3', f'{SP}/tools/next_config.py', f'{SP}/critic/{story}{prev}', story, rnd, draft, num, title], capture_output=True, text=True)
if r.returncode: sys.exit(r.stdout + r.stderr)
src = open(f'scripts-fr/story_{story}.py', encoding='utf-8').read().split('\n')
out, i = {}, 0
while i < len(src):
    m = re.match(r'^# (\d+): (.*)', src[i])
    if m:
        n, txt = int(m.group(1)), m.group(2); i += 1
        while i < len(src) and src[i].startswith('#') and not re.match(r'^# \d+:', src[i]):
            txt += ' ' + src[i].lstrip('# ').strip(); i += 1
        out.setdefault(n, txt)
    else: i += 1
p = f'{SP}/critic/configs/{story}{rnd}.py'
s = open(p, encoding='utf-8').read(); ns = {}; exec(s, ns)
fixes = dict(l.rstrip('\n').split('\t', 1) for l in open(fix_file, encoding='utf-8') if '\t' in l) if fix_file else {}
new, missing = {}, []
for sid, old in ns['SHOTS'].items():
    n, q = int(sid[1:]), old.split('»:')[0] + '»:'
    if sid in fixes: new[sid] = f'{q} {fixes[sid]}'; continue
    if n not in out: new[sid] = old; missing.append(sid); continue
    t = re.sub(r'\s*\((?:pass|stills|review|cycle)[^)]*\)', '', out[n])    # the pass markers
    t = re.sub(r'^\.{2,}\s*', '', t)                                        # "...the second half of a line"
    t = re.sub(r'^[^.:]*?\.{1,3}\s+', '', t, count=1)                       # the gloss of the narration line, up to its full stop
    t = t.strip(); t = t[0].upper() + t[1:] if t else old.split('»:')[1].strip()
    new[sid] = f'{q} {t}'
a = s.index('SHOTS = {'); b = s.index('}\n', a) + 2
s = s[:a] + 'SHOTS = {\n' + ''.join(f' {sid!r}: {txt!r},\n' for sid, txt in new.items()) + '}\n' + s[b:]
note = ' '.join(open(note_file, encoding='utf-8').read().split())
ordn = {'2': 'second', '3': 'third', '4': 'fourth'}.get(rnd, rnd + 'th')
blk = f"\nROUND_NOTE = {note!r}\nROUND_LINE = 'This is the {ordn} review of this film: the brief says what changed since the last round; judge what the evidence shows, on its own merits.'\n"
s = re.sub(r"\nROUND_NOTE = .*?\nROUND_LINE = [^\n]*\n", lambda m: blk, s, flags=re.S) if 'ROUND_NOTE' in s else s + blk
open(p, 'w', encoding='utf-8').write(s)
ns = {}; exec(s, ns)
print(p, 'round', ns['ROUND'], 'draft', ns['DRAFT'], len(ns['SHOTS']), 'shots; kept old description for:', missing)
for k, v in ns['SHOTS'].items(): print(' ', k, v.split('»:')[1][:110])
