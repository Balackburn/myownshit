#!/bin/bash
# runq4.sh "cmd" ...: runq3.sh served in arrival order. Each waiter writes a ticket (a file named by its start time and pid, content "wait") in
# runq.tickets; it starts only when a slot is free AND its ticket is the oldest one still waiting whose pid is alive (with flock alone the order
# was random: a draft waited 9 h while later ones started). A started ticket is marked "done"; nothing is deleted.
SP=/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad
Q=$SP/s7/runq.tickets; mkdir -p $Q
exec 9>$SP/s7/runq.lock
for c in "$@"; do
  T=$Q/$(date +%s%N)-$$; echo wait > $T
  sleep 10
  while true; do
    flock 9
    head=""
    for f in $(ls $Q | sort); do
      if [ "$(cat $Q/$f)" = "wait" ] && kill -0 "${f##*-}" 2>/dev/null; then head=$Q/$f; break; fi
    done
    if [ "$head" = "$T" ] && [ "$(pgrep -fc "^node render/render3.mjs")" -lt 3 ]; then
      echo done > $T; echo "start $(date +%H:%M): $c"; bash -c "$c" & pid=$!; sleep 25; flock -u 9; wait $pid; echo "done $(date +%H:%M): $c"; break
    fi
    flock -u 9; sleep 20
  done
done
