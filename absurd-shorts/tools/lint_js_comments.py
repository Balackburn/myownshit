#!/usr/bin/env python3
"""lint_js_comments.py FILE...: lines where a // comment after code seems to have swallowed code (a call statement `x.y(...);` inside the comment).
Cycle 16: a comment pasted in the middle of a line in props_valise.js hid `hatch.position.set(...); g.add(hatch);` and the tunnel never showed."""
import re, sys
bad = 0
for f in sys.argv[1:]:
    for n, line in enumerate(open(f, encoding='utf-8'), 1):
        i = line.find('//')
        if i <= 0 or not line[:i].strip() or line[:i].count("'") % 2 or line[:i].count('`') % 2 or line[:i].count('"') % 2: continue
        tail = line[i + 2:]
        if re.search(r"[\w\]\)]\.[A-Za-z_]\w*\([^()]*\)\s*;", tail) or re.search(r"\b(const|let|var)\s+\w+\s*=", tail):
            print(f'{f}:{n}: {tail.strip()[:120]}'); bad += 1
sys.exit(1 if bad else 0)
