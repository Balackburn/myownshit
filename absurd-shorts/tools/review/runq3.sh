#!/bin/bash
# runq3.sh "cmd" ...: like runq2.sh, but the check-and-start is serialised by a lock (two chains polling at once both started: four renders ran),
# and the lock is held for 25 s after a start so the new render shows up in the count before the next chain looks
SP=/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad
exec 9>$SP/s7/runq.lock
for c in "$@"; do
  sleep 10
  while true; do
    flock 9
    if [ "$(pgrep -fc "^node render/render3.mjs")" -lt 3 ]; then
      echo "start $(date +%H:%M): $c"; bash -c "$c" & pid=$!; sleep 25; flock -u 9; wait $pid; echo "done $(date +%H:%M): $c"; break
    fi
    flock -u 9; sleep 30
  done
done
