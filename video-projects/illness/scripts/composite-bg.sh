#!/usr/bin/env bash
# Background swap: put Ash (person matte) over a background plate, then point the composition at it.
#   python3 -I scripts/run_rvm.py rvm.onnx assets/illness.mp4 assets/illness-matte.mp4
#   python3 -I scripts/fix_matte.py assets/illness-matte.mp4 assets/illness-matte-fixed.mp4
#   scripts/composite-bg.sh assets/bg/snow-path.mp4 assets/illness-snow.mp4
#   VIDEO=illness-snow python3 -I scripts/build.py   (then render)
set -euo pipefail
ffmpeg -v error -y -i "$1" -i assets/illness.mp4 -i assets/illness-matte-fixed.mp4 -filter_complex \
  "[2:v]format=gray[m];[1:v]eq=brightness=0.03,format=yuva420p[s];[s][m]alphamerge[fg];[0:v][fg]overlay=format=auto:shortest=1,format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 16 -preset medium -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart "$2"
echo "$2"
