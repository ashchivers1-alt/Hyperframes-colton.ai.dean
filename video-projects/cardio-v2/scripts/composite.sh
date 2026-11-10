#!/usr/bin/env bash
# Mixed-style composite.
#   1. index.html renders the BACK layer (footage + graphics + B-roll + SFX)  -> renders/<name>-back.mp4
#   2. Ash is pasted back on top with the person matte, so the headroom type and B-roll sit behind him.
#   3. While the front explainer card is up (24.95–34.85s) its box is cut out of the matte,
#      so the card stays in FRONT of him.
# Build the matte once (Robust Video Matting, rvm_mobilenetv3_fp32.onnx):
#   python3 -I scripts/run_rvm.py rvm.onnx assets/cardio.mp4 assets/cardio-matte.mp4
set -euo pipefail
back="$1"; out="$2"
ffmpeg -v error -y -i "$back" -i assets/cardio.mp4 -i assets/cardio-matte.mp4 -filter_complex \
  "[2:v]format=gray,drawbox=x=80:y=1380:w=920:h=440:color=black:t=fill:enable='between(t,24.95,34.85)'[m];[1:v]format=yuva420p[s];[s][m]alphamerge[fg];[0:v][fg]overlay=format=auto,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf "${CRF:-20}" -c:a copy -movflags +faststart "$out"
echo "$out"
