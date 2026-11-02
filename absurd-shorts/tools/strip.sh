#!/usr/bin/env bash
# strip.sh video.mp4 out.jpg start_s dur_s [fps] [cols]   -> consecutive frames tiled (motion QA)
v=$1; out=$2; ss=$3; d=$4; fps=${5:-6}; cols=${6:-12}
ffmpeg -v error -y -ss "$ss" -t "$d" -i "$v" -vf "fps=$fps,scale=150:-1,drawtext=text='%{pts\:flt}':x=2:y=2:fontsize=11:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${cols}x1" -frames:v 1 "$out"
