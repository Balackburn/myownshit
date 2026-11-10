#!/bin/bash
# motion_check.sh STORY FIRST_SHOT LAST_SHOT [OUTDIR] [W=360]: draft re-render of a run of shots (cheaper shadows, --range) and one
# filmstrip per shot (every second frame, time inside the shot on each tile) -> OUTDIR/strip_<shot>.jpg and OUTDIR/<story>_<first>.mp4.
# The way to judge timing, anticipation and readability of a gag in about a minute instead of rendering the film.
#   bash tools/motion_check.sh trou S02 S05 /tmp/strips
set -e
S=$1; A=$2; B=$3; OUT=${4:-out/motion}; W=${5:-360}
cd "$(dirname "$0")/.."; mkdir -p "$OUT"
R=$(python3 -c "
import json; d={s['id']:s for s in json.load(open('scripts-fr/story_$S.json'))['scenes']}
print(f\"{d['$A']['start']:.4f}:{d['$B']['start']+d['$B']['duration']:.4f}\")")
cp scripts-fr/story_$S.json scripts-fr/story_${S}_mc_$A.json
node render/render3.mjs scripts-fr/story_${S}_mc_$A.json --timed --w $W --h $((W*16/9)) --fps 30 --workers 3 --draft --range $R --out "$OUT/${S}_$A.mp4" > "$OUT/${S}_$A.log" 2>&1 || { rm -f scripts-fr/story_${S}_mc_$A.json; tail -5 "$OUT/${S}_$A.log"; exit 1; }
rm -f scripts-fr/story_${S}_mc_$A.json
python3 tools/shot_strips.py "$OUT/${S}_$A.mp4" scripts-fr/story_$S.json "$OUT" --range $R
