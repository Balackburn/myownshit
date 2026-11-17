#!/bin/bash
# draft.sh STORY N: draft N of a story (480x854, 15 fps, one browser) through the fair queue, then the freeze check and the grey scan.
# Output: $PIPE/s7/STORY/draftN.mp4 (+ .log). Prints STORY_DN_READY at the end. Run it detached:
#   setsid nohup bash absurd-shorts/pipeline/draft.sh STORY N > $PIPE/s7/STORY_dN.log 2>&1 < /dev/null & disown
# DRYRUN=1 prints the render command instead of running it.
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
S=$1; N=$2; [ -z "$S" ] || [ -z "$N" ] && { echo "usage: draft.sh STORY N"; exit 1; }
O=$PIPE/s7/$S; mkdir -p $O
cd $ROOT || exit 1
python3 scripts-fr/story_$S.py > $O/script_d$N.log 2>&1 || { echo "story_$S.py FAILED (see $O/script_d$N.log)"; exit 1; }
bash $PIPELINE_DIR/runq.sh "node render/render3.mjs scripts-fr/story_$S.json --timed --w 480 --h 854 --fps 15 --workers 1 --out $O/draft$N.mp4 > $O/draft$N.log 2>&1"
if [ -z "$DRYRUN" ]; then
  python3 tools/freeze_check.py $O/draft$N.mp4 scripts-fr/story_$S.json 2>&1 | tail -6
  python3 $PIPELINE_DIR/tools/grey_scan.py $O/draft$N.mp4 2>&1 | tail -3
fi
echo "$(echo $S | tr a-z A-Z)_D${N}_READY"
