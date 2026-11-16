#!/bin/bash
# disk_guard.sh: every 5 min, if less than 1.6 GB is free, remove only copies that exist elsewhere: out/story_X_3d.mp4 byte-identical to a
# HyperFrames project's assets/layer3d.mp4, and out/work/story_X_render folders of stories whose final mp4 exists. (HyperFrames refuses to
# render under 1 GB free: the mower final failed on it.)
cd /home/user/myownshit
while true; do
  free=$(df -m /tmp | awk 'NR==2{print $4}')
  if [ "$free" -lt 1600 ]; then
    for f in absurd-shorts/out/story_*_3d.mp4; do
      [ -f "$f" ] || continue; s=$(basename "$f" _3d.mp4); s=${s#story_}
      d=$(ls -d hyperframes/[0-9]*-"$s" 2>/dev/null | head -1)
      if [ -n "$d" ] && [ -f "$d/renders/$s.mp4" ] && cmp -s "$f" "$d/assets/layer3d.mp4"; then rm -f -- "$f" && echo "$(date +%H:%M) removed $f (copy in $d/assets)"; fi
    done
    for w in absurd-shorts/out/work/story_*_render; do
      [ -d "$w" ] || continue; s=$(basename "$w" _render); s=${s#story_}
      d=$(ls -d hyperframes/[0-9]*-"$s" 2>/dev/null | head -1)
      if [ -n "$d" ] && [ -f "$d/renders/$s.mp4" ]; then rm -rf -- "$w" && echo "$(date +%H:%M) removed $w (final exists)"; fi
    done
    echo "$(date +%H:%M) free after: $(df -m /tmp | awk 'NR==2{print $4}') MB"
  fi
  sleep 300
done
