#!/usr/bin/env bash
# Behind-the-subject composite.
#   1. index.html renders the BACK layer (footage + graphics + SFX)  -> renders/<name>-back.mp4
#   2. this script pastes Ash back on top using the person matte     -> renders/<name>.mp4
# Build the matte once (Robust Video Matting, rvm_mobilenetv3_fp32.onnx):
#   python3 -I scripts/run_rvm.py rvm.onnx assets/mtvideo.mp4 assets/mtvideo-matte.mp4
set -euo pipefail
back="$1"; out="$2"
ffmpeg -v error -y -i "$back" -i assets/mtvideo.mp4 -i assets/mtvideo-matte.mp4 -filter_complex \
  "[2:v]format=gray[m];[1:v]format=yuva420p[s];[s][m]alphamerge[fg];[0:v][fg]overlay=format=auto,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf "${CRF:-20}" -c:a copy -movflags +faststart "$out"
echo "$out"
