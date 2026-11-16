#!/usr/bin/env bash
# Builds the vertical slow-mo base plate for the kart-crash reel from the screen recording.
# Layout: 4:5 landscape panel (crop 566x708 of the 1288x708 source, scaled to 1080x1351) centred on a
# blurred fill of the same footage. Ash = red-suit driver who gets launched (~2.00s in the source).
# Segments:
#   A  build-up      src 0.60-1.75 real time, crop pans to follow the pack
#   B  impact        src 1.75-2.15 at 0.25x (motion-interpolated)
#   C  freeze        src 2.02 held 1.5s   (ring + flash added in index.html)
#   D  aftermath     src 2.15-2.55 at 0.5x
#   E  replay        src 1.75-2.35 at 0.2x, tight crop on Ash
#   F  end hold      last replay frame 1.0s
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=assets/src60.mp4
T=renders/seg; mkdir -p $T
ENC="-c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -r 30 -an"

panel() { # $1 = crop filter producing a 4:5 frame -> vertical 1080x1920 with blurred fill
  echo "$1,split[a][b];[a]scale=1080:1351:flags=lanczos,unsharp=5:5:0.6[p];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.12:saturation=0.8[bg];[bg][p]overlay=0:(H-h)/2"
}
SLOW() { echo "minterpolate=fps=$1:mi_mode=mci:mc_mode=aobmc:vsbmc=1"; }

# A — build-up, pan from x=380 to x=0 over the first second
ffmpeg -v error -y -ss 0.60 -t 1.15 -i $SRC -filter_complex "$(panel "[0:v]crop=566:708:'max(0,380-380*t/1.0)':0")" $ENC $T/A.mp4
# B — impact slow-mo 4x
ffmpeg -v error -y -ss 1.75 -t 0.40 -i $SRC -filter_complex "[0:v]$(SLOW 240),setpts=4*PTS[s];$(panel "[s]crop=440:550:40:20")" $ENC $T/B.mp4
# C — freeze on the launch
ffmpeg -v error -y -ss 2.02 -i $SRC -frames:v 1 $T/freeze.png
ffmpeg -v error -y -loop 1 -t 1.5 -i $T/freeze.png -filter_complex "$(panel "[0:v]crop=360:450:90:60")" $ENC $T/C.mp4
# D — aftermath 2x slow
ffmpeg -v error -y -ss 2.15 -t 0.40 -i $SRC -filter_complex "[0:v]$(SLOW 120),setpts=2*PTS[s];$(panel "[s]crop=440:550:40:20")" $ENC $T/D.mp4
# E — replay focused on the driver Ash hits (white helmet, kart underneath Ash), very tight
VC="crop=240:300:180:150"
ffmpeg -v error -y -ss 1.74 -t 0.10 -i $SRC -filter_complex "[0:v]$(SLOW 400),setpts=6.67*PTS[s];$(panel "[s]$VC")" $ENC $T/E1.mp4
ffmpeg -v error -y -ss 1.84 -i $SRC -frames:v 1 $T/victim.png
ffmpeg -v error -y -loop 1 -t 1.4 -i $T/victim.png -filter_complex "$(panel "[0:v]$VC")" $ENC $T/E2.mp4
ffmpeg -v error -y -ss 1.84 -t 0.16 -i $SRC -filter_complex "[0:v]$(SLOW 400),setpts=6.67*PTS[s];$(panel "[s]$VC")" $ENC $T/E3.mp4
# F — hold last frame
ffmpeg -v error -y -sseof -0.05 -i $T/E3.mp4 -frames:v 1 -update 1 $T/last.png
ffmpeg -v error -y -loop 1 -t 1.0 -i $T/last.png $ENC $T/F.mp4

printf "file '%s'\n" A.mp4 B.mp4 C.mp4 D.mp4 E1.mp4 E2.mp4 E3.mp4 F.mp4 > $T/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $T/list.txt -c copy assets/base.mp4
for s in A B C D E1 E2 E3 F; do printf "%s %s\n" $s "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/$s.mp4)"; done
ffprobe -v error -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of compact assets/base.mp4
