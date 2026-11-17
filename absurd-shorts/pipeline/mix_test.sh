#!/bin/bash
# mix_test.sh STORY: the mix alone (narration + music bed + effect cues), exactly as make_project.py calls it, in a few seconds. Run it before
# every final render: a cue written wrong (e.g. a rain cue without its duration) otherwise fails the final after the 1 h 40 3D render.
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
S=$1; [ -z "$S" ] && { echo "usage: mix_test.sh STORY"; exit 1; }
O=$PIPE/s7/$S/mixtest; mkdir -p $O
python3 $SKILL_SCRIPTS/mix.py $ROOT/stories7/$S/timeline.json $ROOT/stories7/$S/cues.json $O --bed $PIPELINE_DIR/assets/instrumental.wav --bed-from 17.7 --bed-len 6.0 && \
  ffmpeg -nostats -hide_banner -i $O/mix.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 && echo MIX_OK || echo MIX_FAILED
