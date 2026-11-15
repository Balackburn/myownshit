#!/bin/bash
# every minute: the draft renders (15 fps) and the browsers under them at nice 15, so the finals keep the processor
end=$(( $(date +%s) + 6*3600 ))
while [ $(date +%s) -lt $end ]; do
  for p in $(pgrep -f "render/render3.mjs .*--fps 15"); do
    renice -n 15 -p $p >/dev/null 2>&1
    for c in $(pgrep -P $p); do renice -n 15 -p $c >/dev/null 2>&1; for g in $(pgrep -P $c); do renice -n 15 -p $g >/dev/null 2>&1; done; done
  done
  sleep 60
done
