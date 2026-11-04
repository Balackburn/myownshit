#!/usr/bin/env bash
# render_video.sh PROJECT.tsrct REF.mp4 START_S END_S OUT.mp4 [FPS=15]
# Playable progress video: renders the replica frame by frame with `tsrct preview` (canvas resolution, so a half-size
# draft build renders ~4x faster than `export`, which never goes below 720p), encodes it, and writes
# OUT.mp4 = reference | replica side by side over the same span, with the reference's sound.
set -euo pipefail
P=$1; REF=$2; A=$3; B=$4; OUT=$5; F=${6:-15}
T=${TSRCT:-$HOME/.local/share/Tesseract/bin/tsrct}
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT
n=$(python3 -c "import math; print(int(math.floor(($B-$A)*$F + 1e-6)))")
# 2 previews in parallel: the raster renderer leaves cores idle (about 9 s fixed cost per frame on Mesa lavapipe)
seq 0 $((n-1)) | xargs -P ${JOBS:-2} -I{} sh -c 't=$(python3 -c "print(f\"{'"$A"' + {}/'"$F"' + 0.001:.4f}\")"); TESSERACT_CALLER=agent-skill TESSERACT_SKILL=tesseract-3d "'"$T"'" preview --project "'"$P"'" --time "$t" --output "'"$D"'/f_$(printf %05d {}).png" >/dev/null 2>>"'"$D"'/err.log" || echo "frame {} failed" >&2'

H=$(python3 -c "from PIL import Image; print(Image.open('$D/f_00000.png').size[1])")
ffmpeg -v error -y -framerate $F -i "$D/f_%05d.png" -c:v libx264 -pix_fmt yuv420p -crf 18 "$D/replica.mp4"
ffmpeg -v error -y -ss $A -t $(python3 -c "print($B-$A)") -i "$REF" -i "$D/replica.mp4" \
  -filter_complex "[0:v]fps=$F,scale=-2:$H[r];[1:v]scale=-2:$H[c];[r][c]hstack=inputs=2,drawtext=text='reference | replica':x=10:y=10:fontcolor=white:fontsize=$((H/40)):box=1:boxcolor=black@0.4[v]" \
  -map "[v]" -map 0:a? -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a aac -b:a 128k -shortest "$OUT"
echo "$OUT"
