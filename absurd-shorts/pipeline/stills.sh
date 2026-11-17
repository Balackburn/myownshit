#!/bin/bash
# stills.sh STORY NAME "t1,t2,..."|cams : regenerate story_STORY.json from the .py, render stills at those times (432x768, final look) through the
# priority lane, copy the contact sheet to $PIPE/s7/STORY/NAME.jpg (single stills stay in out/work/story_STORY/stills/). Use it for every
# staging/correction check: stills are minutes, a draft is half an hour.
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
S=$1; NAME=$2; T=$3; [ -z "$T" ] && { echo 'usage: stills.sh STORY NAME "t1,t2,..."|cams'; exit 1; }
O=$PIPE/s7/$S; mkdir -p $O; cd $ROOT || exit 1
python3 scripts-fr/story_$S.py > $O/gen.log 2>&1 || { tail -5 $O/gen.log; exit 1; }
LIMIT=4 bash $PIPELINE_DIR/runqP.sh "node render/render3.mjs scripts-fr/story_$S.json --timed --w 432 --h 768 --stills $T --workers 1 > $O/st_$NAME.log 2>&1" > /dev/null
cp out/work/story_$S/cams.jpg $O/$NAME.jpg 2>/dev/null && echo "$O/$NAME.jpg" || { tail -5 $O/st_$NAME.log; exit 1; }
