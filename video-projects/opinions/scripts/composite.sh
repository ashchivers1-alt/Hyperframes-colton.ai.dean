#!/usr/bin/env bash
# Behind-subject composite: back layer (index.html render) + Ash pasted on top via person matte.
# Front cards (#c4 11.75–15.1s, #c8 28.9–32.55s) sit at y≈1075–1295 (safe zone, just above Ash's captions): punch their box out of the matte so they stay in FRONT.
#   python3 -I scripts/run_rvm.py rvm.onnx assets/opinions.mp4 assets/opinions-matte-raw.mp4
#   python3 -I scripts/fix_matte.py assets/opinions-matte-raw.mp4 assets/opinions-matte.mp4
set -euo pipefail
back="$1"; out="$2"
ffmpeg -v error -y -i "$back" -i assets/opinions.mp4 -i assets/opinions-matte.mp4 -filter_complex \
  "[2:v]format=gray,drawbox=x=80:y=1030:w=920:h=300:color=black:t=fill:enable='between(t,3.65,8.85)+between(t,11.7,15.15)+between(t,16.0,21.3)+between(t,21.3,28.15)+between(t,28.85,35.0)'[m];[1:v]format=yuva420p[s];[s][m]alphamerge[fg];[0:v][fg]overlay=format=auto,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf "${CRF:-18}" -c:a copy -movflags +faststart "$out"
echo "$out"
