#!/bin/zsh
# Render every graphics comp at 3840x2160 (24 fps, times pre-scaled by 1/1.001) and conform to 23.976 ProRes 4444 in gfx/out4k/.
cd "${0:A:h}/../gfx"
mkdir -p out4k
render() {
  n=$1
  (cd comps/$n && npx --prefix "/Users/ashleychivers/Documents/Claude Video Studio" hyperframes render --format mov --fps 24 --output ../../out4k/$n-24.mov >/dev/null 2>&1) &&
  ffmpeg -v error -y -i out4k/$n-24.mov -vf "setpts=N/(24000/1001)/TB" -r 24000/1001 -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le out4k/$n.mov &&
  rm out4k/$n-24.mov && echo "done $n" || echo "FAIL $n"
}
names=(${(f)"$(ls comps | grep -v '^g12_natty$')"})
for n in $names; do
  render $n &
  while (( $(jobs -r | wc -l) >= 3 )); do sleep 2; done
done
wait
echo ALL DONE
