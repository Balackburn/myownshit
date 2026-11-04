#!/usr/bin/env bash
# render_samples.sh PROJECT.tsrct SHOTS.json OUTDIR [PER_SHOT=3] [ONLY=S1,S3] [RENDERER=raster]
# Renders the same sample instants compare.py uses (PER_SHOT evenly spaced frames per shot) as OUTDIR/t_<ms>.png
# with `tsrct preview` (no labels, document resolution). Then: compare.py --cand-frames OUTDIR ...
set -euo pipefail
P=$1; S=$2; O=$3; K=${4:-3}; ONLY=${5:-}; R=${6:-raster}
T=${TSRCT:-$HOME/.local/share/Tesseract/bin/tsrct}
mkdir -p "$O"
python3 - "$S" "$K" "$ONLY" <<'PY' > "$O/times.txt"
import json, sys
spec = json.load(open(sys.argv[1])); k = int(sys.argv[2]); only = set(filter(None, sys.argv[3].split(',')))
fps = spec['reference'].get('fps', 30)
for s in spec['shots']:
    if only and s['id'] not in only: continue
    f0, f1 = s['frames']
    for i in range(k): print(round((f0 + (f1 - f0) * (i + 0.5) / k)) / fps)
PY
while read -r t; do
  ms=$(python3 -c "print(int(round($t*1000)))")
  # a hair after the frame start so a sample on a cut frame renders the new shot
  tt=$(python3 -c "print(f'{$t + 0.001:.4f}')")
  TESSERACT_CALLER=agent-skill TESSERACT_SKILL=tesseract-3d "$T" preview --project "$P" --time "$tt" --output "$O/t_$ms.png" --renderer "$R" >/dev/null 2>>"$O/render.log" || echo "failed at $t" >> "$O/render.log"
done < "$O/times.txt"
ls "$O"/t_*.png | wc -l
