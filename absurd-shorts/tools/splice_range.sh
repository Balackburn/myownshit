#!/bin/bash
# splice_range.sh BASE.mp4 SEG.mp4 T0 OUT.mp4: replace the part of BASE that starts at T0 (seconds) with SEG (a --range render of the same
# film, same size and frame rate), frame-accurate (one re-encode at crf 16). Use it to re-render one shot instead of the whole film:
#   node render/render3.mjs scripts-fr/story_x.json --timed --w 1080 --h 1920 --range 12.30:14.10 --out out/x_s09.mp4
#   bash tools/splice_range.sh out/story_x_3d.mp4 out/x_s09.mp4 12.30 out/story_x_3d_new.mp4
set -e
BASE=$1; SEG=$2; T0=$3; OUT=$4
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$BASE"); FPS=$(python3 -c "print(round(eval('$FPS')))")
N0=$(python3 -c "print(round($T0 * $FPS))"); NS=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$SEG"); N1=$((N0 + NS))
NB=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$BASE")
if [ "$N0" -gt 0 ]; then A="[0:v]trim=end_frame=$N0,setpts=PTS-STARTPTS[a];"; AL="[a]"; n=1; else A=""; AL=""; n=0; fi
if [ "$N1" -lt "$NB" ]; then C="[0:v]trim=start_frame=$N1,setpts=PTS-STARTPTS[c];"; CL="[c]"; n=$((n + 1)); else C=""; CL=""; fi
ffmpeg -v error -y -i "$BASE" -i "$SEG" -filter_complex "${A}[1:v]setpts=PTS-STARTPTS[b];${C}${AL}[b]${CL}concat=n=$((n + 1)):v=1[v]" -map "[v]" -r $FPS -c:v libx264 -pix_fmt yuv420p -preset medium -crf 16 "$OUT"
echo "spliced frames $N0..$N1 of $NB -> $OUT ($(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$OUT") frames)"
