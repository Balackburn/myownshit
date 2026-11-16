#!/bin/bash
# runqP.sh "cmd" ...: the priority lane of runq3.sh (same lock, same count of renders): it polls every 3 s instead of every 30 s, so a final or a
# short stills job takes the next free slot before the waiting drafts; LIMIT (default 3) lets a short stills job run as a fourth render
# (17 Nov) the load counts a final render (story_X_render.json, three browsers) as three renders: two finals and nine stills at once ran the
# session out of memory (the browser of the mower final was killed after two hours)
SP=/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad
LIMIT=${LIMIT:-3}
exec 9>$SP/s7/runq.lock
for c in "$@"; do
  while true; do
    flock 9
    if [ "$(( $(pgrep -fc "^node render/render3.mjs") + 2 * $(pgrep -fc "^node render/render3.mjs scripts-fr/story_[a-z]*_render.json") ))" -lt "$LIMIT" ]; then
      echo "start $(date +%H:%M): $c"; bash -c "$c" & pid=$!; sleep 25; flock -u 9; wait $pid; echo "done $(date +%H:%M): $c"; break
    fi
    flock -u 9; sleep 3
  done
done
