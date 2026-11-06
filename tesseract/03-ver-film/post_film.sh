#!/bin/bash
# post_film.sh: Tesseract halves -> one 1080x1920 30 fps layer (denoised, lifted a touch) -> HyperFrames project copy with captions, cards, music
set -e
cd "$(dirname "$0")"
printf "file 'part1.mp4'\nfile 'part2.mp4'\n" > parts.txt
ffmpeg -v error -y -f concat -safe 0 -i parts.txt -c copy tess_raw.mp4
ffmpeg -v error -y -i tess_raw.mp4 -vf "hqdn3d=3:2.5:6:5,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,eq=saturation=1.12:contrast=1.05,fps=30" -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p layer3d_tess.mp4
P=/home/user/myownshit/hyperframes/35-ver-tesseract
rm -rf $P; mkdir -p $P; (cd /home/user/myownshit/hyperframes/35-ver && tar cf - --exclude=renders --exclude=node_modules .) | (cd $P && tar xf -)
cp layer3d_tess.mp4 $P/assets/layer3d.mp4
cd $P && export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt && mkdir -p renders && npx --yes hyperframes@0.9.13 render -o renders/ver_tesseract.mp4 --fps 30 > /tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/s7/ver/hf_tess.log 2>&1
echo "DONE $P/renders/ver_tesseract.mp4"
