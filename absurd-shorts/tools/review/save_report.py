#!/usr/bin/env python3
"""save_report.py TASK_OUTPUT_JSONL OUT_MD: write the report a critic agent handed back (its SubagentHandback tool_use input) to OUT_MD"""
import json, sys
src, out = sys.argv[1], sys.argv[2]
rep = None
for line in open(src, errors='replace'):
    try: ev = json.loads(line)
    except Exception: continue
    msg = ev.get('message') or {}
    for c in (msg.get('content') or []) if isinstance(msg.get('content'), list) else []:
        if isinstance(c, dict) and c.get('type') == 'tool_use' and c.get('name') == 'SubagentHandback':
            inp = c.get('input') or {}
            rep = inp.get('report') or inp.get('text') or inp.get('message') or json.dumps(inp, ensure_ascii=False)
if rep is None: sys.exit('no SubagentHandback found')
open(out, 'w').write(rep.rstrip() + '\n'); print(out, len(rep), 'chars;', rep.splitlines()[0])
