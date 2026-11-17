#!/bin/bash
# runqP.sh "cmd" ...: the priority lane of runq.sh (same lock, same load count). It polls every 3 s instead of every 20 s, so a final or a short
# stills job takes the next free slot before waiting drafts. Threshold LIMIT + 1 (LIMIT default 3): one stills job may run beside a final and a
# draft. A final counts as three renders (two finals plus stills at once ran a session out of memory). DRYRUN=1 prints instead of running.
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
LIMIT=${LIMIT:-3}
exec 9>$PIPE/runq.lock
for c in "$@"; do
  if [ -n "$DRYRUN" ]; then echo "DRYRUN runqP: $c"; continue; fi
  while true; do
    flock 9
    if [ "$(( $(pgrep -fc "^node render/render3.mjs") + 2 * $(pgrep -fc "^node render/render3.mjs scripts-fr/story_[a-z]*_render.json") ))" -lt "$((LIMIT + 1))" ]; then
      echo "start $(date +%H:%M): $c"; bash -c "$c" & pid=$!; sleep 25; flock -u 9; wait $pid; echo "done $(date +%H:%M): $c"; break
    fi
    flock -u 9; sleep 3
  done
done
