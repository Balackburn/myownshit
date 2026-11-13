#!/usr/bin/env python3
"""lint_comments.py FILE...: comments that swallowed code (a '#' put in the middle of a literal hides the rest of the line without a syntax error)"""
import io, re, sys, tokenize
bad = 0
for f in sys.argv[1:]:
    for tok in tokenize.generate_tokens(io.StringIO(open(f).read()).readline):
        if tok.type == tokenize.COMMENT and (re.search(r"'[A-Za-z_]+':\s*[\[\{'\d-]", tok.string) or re.search(r"\bk\(\d", tok.string) or re.search(r"\bP\('", tok.string) or re.search(r"\bact\('", tok.string) or re.search(r"\b[a-z_][a-z0-9_]*=\[\[?[-\d\[]", tok.string) or re.search(r"\b[a-z_][a-z0-9_]*=\{'", tok.string) or re.search(r"\b(drift|inside|lenses|margin)=[\(r]", tok.string) or re.search(r"\)\)\]\)\s*$", tok.string) or re.search(r";\s*[A-Za-z_][A-Za-z0-9_]*\s*=\s*[\[\{\d'(r-]", tok.string) or (re.search(r",\s*$", tok.string) and not tok.line.lstrip().startswith("#"))):   # (pass 3 of 52) '; NAME = ...' swallowed: a constant defined after a comment on the same line   # (pass 3 of 47) a comment ending in a comma: it swallowed the comma after the code (the replaced text ended before it)   # (final pass 46) a comment put after 'bottom=0.7,' swallowed 'inside=(...))])'   # (final pass 45) keyword arguments swallowed: gaze=[[...], lids={...}
            print(f'{f}:{tok.start[0]}: {tok.string[:140]}'); bad += 1
sys.exit(1 if bad else 0)
