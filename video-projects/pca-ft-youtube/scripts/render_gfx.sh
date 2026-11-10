#!/bin/zsh
# render every comp in gfx/comps -> gfx/$OUT/<name>.mov (ProRes 4444 alpha, conformed to 23.976). usage: render_gfx.sh out1|out4k [names...]
cd "${0:A:h}/../gfx"; OUT=$1; shift; mkdir -p $OUT
render() {
  n=$1
  (cd comps/$n && npx --prefix "/Users/ashleychivers/Documents/Claude Video Studio" hyperframes render --format mov --fps 24 --quality draft --output ../../$OUT/$n-24.mov >/dev/null 2>&1) &&
  ffmpeg -nostdin -v error -y -i $OUT/$n-24.mov -vf "setpts=N/(24000/1001)/TB" -r 24000/1001 -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le $OUT/$n.mov &&
  rm $OUT/$n-24.mov && echo "done $n" || echo "FAIL $n"
}
names=($@); [ ${#names} -eq 0 ] && names=(${(f)"$(ls comps)"})
for n in $names; do render $n & while (( $(jobs -r | wc -l) >= 4 )); do sleep 2; done; done
wait; echo ALL DONE
