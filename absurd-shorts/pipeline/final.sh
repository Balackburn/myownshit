#!/bin/bash
# final.sh STORY NUM "TITLE": the delivery render through the priority lane, then QA (size, loudness, HyperFrames check, contact sheet) and the
# grey scan. Prints FINAL_READY at the end (also when a step failed: read the lines above it and $PIPE/s7/queue.log). Run it detached:
#   setsid nohup bash absurd-shorts/pipeline/final.sh STORY NUM "TITLE" > $PIPE/s7/STORY_final.log 2>&1 < /dev/null & disown
# About 1 h 40 on a 4-core container. Pre-test the mix first (see RUNBOOK.md).
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
S=$1; NUM=$2; TITLE=$3; [ -z "$TITLE" ] && { echo 'usage: final.sh STORY NUM "TITLE"'; exit 1; }
cd $ROOT || exit 1
LIMIT=4 bash $PIPELINE_DIR/runqP.sh "bash $PIPELINE_DIR/queue_one.sh $S $NUM \"$TITLE\" > $PIPE/s7/$S/q11.log 2>&1"
echo "queue_one exit ($S) $(date +%H:%M)"
if [ -z "$DRYRUN" ]; then
  bash $PIPELINE_DIR/qa.sh $S $NUM 2>&1 | tail -6
  python3 $PIPELINE_DIR/tools/grey_scan.py $REPO/hyperframes/$NUM-$S/renders/$S.mp4 2>&1 | tail -3
  tail -2 $PIPE/s7/queue.log
fi
echo FINAL_READY
