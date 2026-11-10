#!/bin/zsh
# Stage reel video: graded, slow push-in per segment, Katka portrait on a blurred fill. Source = Resolve render of Ash's trimmed stage clips.
SRC=stage-raw.mp4
G="eq=contrast=1.08:saturation=1.12:gamma=0.97,colorbalance=rs=0.03:bs=-0.03:rh=0.02,unsharp=5:5:0.4,vignette=angle=0.35"
seg() { # name start dur
  ffmpeg -v error -y -ss $2 -t $3 -i $SRC -vf "fps=30,scale=w='1920*(1+0.07*t/$3)':h=-2:eval=frame,crop=1920:1080,${G},format=yuv420p" -an -c:v libx264 -crf 15 -preset medium s_$1.mp4
}
seg a 0 24.6333 & seg b 24.6333 13.9 & seg c 38.5333 23.3667 & seg d 61.9 30.0667 &
ffmpeg -v error -y -ss 91.9667 -t 31.4667 -i $SRC -filter_complex "[0:v]fps=30,crop=604:1080:658:0,split[a][b];[a]scale=1920:3434,crop=1920:1080,gblur=sigma=40,eq=brightness=-0.12:saturation=1.2[bg];[b]scale=w='604*(1+0.06*t/31.4667)':h=-2:eval=frame,crop=604:1080,${G}[fg];[bg][fg]overlay=(W-w)/2:0,vignette=angle=0.4,format=yuv420p[o]" -map "[o]" -an -c:v libx264 -crf 15 -preset medium s_e.mp4 &
wait
printf "file s_a.mp4\nfile s_b.mp4\nfile s_c.mp4\nfile s_d.mp4\nfile s_e.mp4\n" > list.txt
ffmpeg -v error -y -f concat -i list.txt -c copy stage-reel-video.mp4
ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 stage-reel-video.mp4
