#!/bin/bash
# hf_only.sh STORY NUM "TITLE": the HyperFrames half of the final (out/story_STORY_3d.mp4 already rendered): project + mix + check + render.
# Use it alone when only this half failed (never re-render the 3D for that). HyperFrames refuses to start under 1 GB free disk.
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
S=$1; NUM=$2; TITLE=$3; SC=$PIPE/s7; P=$REPO/hyperframes/$NUM-$S
cd $ROOT || exit 1
mkdir -p $SC/$S
python3 $PIPELINE_DIR/make_project.py $S $P "$TITLE" >> $SC/queue2.log 2>&1 || { echo "$S PROJECT FAILED (see $SC/queue2.log)" >> $SC/queue.log; exit 1; }
cp out/story_${S}_3d.mp4 $P/assets/layer3d.mp4
pgrep -f 'hyperframes@0.9.13 render' > /dev/null || rm -rf /tmp/hyperframes-extract-cache-*/hfcache-*
(cd $P && export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt && npx --yes hyperframes@0.9.13 check --json > $SC/$S/check.json 2>/dev/null; mkdir -p renders && npx --yes hyperframes@0.9.13 render -o renders/$S.mp4 --fps 30 > $SC/$S/hf2.log 2>&1) && echo "$S DONE $P/renders/$S.mp4" >> $SC/queue.log || { echo "$S HF FAILED (see $SC/$S/hf2.log)" >> $SC/queue.log; exit 1; }
