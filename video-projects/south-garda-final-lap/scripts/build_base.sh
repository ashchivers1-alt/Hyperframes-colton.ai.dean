#!/usr/bin/env bash
# Builds assets/base.mp4: the synced multicam cut (1080x1920, 30fps, no audio) and assets/commentary.wav.
# Timeline = live-stream time T. Onboard is 2.0s ahead of the stream (onboard = T + 2.0),
# measured from the start-line (onboard 4.0 / stream 2.0) and finish-line (72.5 / 70.5) crossings.
# Usage: scripts/build_base.sh   (run from the project folder)
set -euo pipefail
RAW="$HOME/Documents/Claude Video Studio/raw-media"
STREAM="$RAW/ScreenRecording_09-02-2026 08-55-52_1.MOV"
ONBOARD="$RAW/956eebb7ed7f4cfd9c44a0b1ef183afd.MP4"
OFFSET=2.0
END=73.3          # stream shows YouTube UI after ~73.5s
FREEZE_AT=70.55   # photo-finish frame on the stream

# Edit decision list: source start end (stream time)
EDL=(
  "S 0.0 4.0"
  "O 4.0 11.5"
  "S 11.5 14.0"
  "O 14.0 24.0"
  "S 24.0 29.5"
  "O 29.5 42.0"
  "S 42.0 47.5"
  "O 47.5 55.0"
  "S 55.0 62.5"
  "O 62.5 68.8"
  "S 68.8 $FREEZE_AT"
)

# Stream picture is x 252..2544 of the screen recording; cut the timing tower off the left.
S_CROP="crop=1808:1290:735:0"
# Onboard reel: 16:9 footage band at y=437; centre-crop to the same 1.40 aspect.
O_CROP="crop=568:405:76:437"
GRADE="eq=contrast=1.08:saturation=1.08:gamma=0.98"

inputs=(); fc=""; i=0
for row in "${EDL[@]}"; do
  read -r src a b <<<"$row"
  if [[ $src == S ]]; then f="$STREAM"; ss=$a; crop=$S_CROP; else f="$ONBOARD"; ss=$(echo "$a + $OFFSET" | bc); crop=$O_CROP; fi
  dur=$(echo "$b - $a" | bc)
  inputs+=(-ss "$ss" -t "$dur" -i "$f")
  pad=""
  [[ $i -eq $((${#EDL[@]} - 1)) ]] && pad=",tpad=stop_mode=clone:stop_duration=$(echo "$END - $FREEZE_AT" | bc)"
  fc+="[$i:v]$crop,fps=30,setpts=PTS-STARTPTS,$GRADE${pad},split[f$i][g$i];"
  fc+="[f$i]scale=1080:770:flags=lanczos,setsar=1[band$i];"
  fc+="[g$i]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.22:saturation=0.8,setsar=1[bg$i];"
  fc+="[bg$i][band$i]overlay=0:575[c$i];"
  i=$((i + 1))
done
for ((k = 0; k < i; k++)); do fc+="[c$k]"; done
fc+="concat=n=$i:v=1:a=0,format=yuv420p[v]"

ffmpeg -v error -y "${inputs[@]}" -filter_complex "$fc" -map "[v]" -an -c:v libx264 -preset medium -crf 16 -g 15 -movflags +faststart assets/base.mp4
ffmpeg -v error -y -ss 0 -t "$END" -i "$STREAM" -vn -ac 2 -ar 48000 assets/commentary.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/base.mp4
