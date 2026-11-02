#!/usr/bin/env python3
"""Absolute time of a line / word in a timed v3 script: python3 tools/when.py out/work/<name>/script.timed.json g36:nuit g29 g30.end ..."""
import json, re, sys, unicodedata
d = json.load(open(sys.argv[1]))
L = {l['id']: l for s in d['scenes'] for l in s['lines']}
norm = lambda w: ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if unicodedata.category(c) != 'Mn' and (c.isalnum() or c in "'"))
out = []
for e in sys.argv[2:]:
    m = re.match(r"^([A-Za-z]\w*?)(?:#(\d+)|:([^.+\-]+))?(\.end|\.mid)?([+-][\d.]+)?$", e)
    l = L[m.group(1)]; a, b = l['start'], l['end']; ws = l.get('words', [])
    if m.group(2) or m.group(3):
        w = ws[int(m.group(2))] if m.group(2) else next(x for x in ws if norm(m.group(3)) in norm(x['w']))
        a, b = w['s'], w['e']
    t = b if m.group(4) == '.end' else (a + b) / 2 if m.group(4) == '.mid' else a
    if m.group(5): t += float(m.group(5))
    out.append(f'{t:.2f}')
print(','.join(out))
