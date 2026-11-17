#!/bin/bash
# runq.sh "cmd" ...: fair render queue (copy of runq4.sh). Each waiter writes a ticket (start time + pid, content "wait") in $PIPE/runq.tickets; it
# starts only when a slot is free AND its ticket is the oldest still waiting whose pid is alive. Load = running render3 processes, a final render
# (story_X_render.json, three browsers) counting as three; threshold 4 (with a final running, one draft may run beside it).
# DRYRUN=1 prints the commands instead of running them.
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
Q=$PIPE/runq.tickets; mkdir -p $Q
exec 9>$PIPE/runq.lock
for c in "$@"; do
  if [ -n "$DRYRUN" ]; then echo "DRYRUN runq: $c"; continue; fi
  T=$Q/$(date +%s%N)-$$; echo wait > $T
  sleep 10
  while true; do
    flock 9
    head=""
    for f in $(ls $Q | sort); do
      if [ "$(cat $Q/$f)" = "wait" ] && kill -0 "${f##*-}" 2>/dev/null; then head=$Q/$f; break; fi
    done
    if [ "$head" = "$T" ] && [ "$(( $(pgrep -fc "^node render/render3.mjs") + 2 * $(pgrep -fc "^node render/render3.mjs scripts-fr/story_[a-z]*_render.json") ))" -lt 4 ]; then
      echo done > $T; echo "start $(date +%H:%M): $c"; bash -c "$c" & pid=$!; sleep 25; flock -u 9; wait $pid; echo "done $(date +%H:%M): $c"; break
    fi
    flock -u 9; sleep 20
  done
done
