#!/bin/bash
# whisper medium.en with filler prompt; srt-ish output per clip
cd "$(dirname "$0")/.."
for n in "$@"; do
  whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-medium.en.bin --prompt 'Umm, err, uh. Right, go on, push.' -t 4 -oj -of src/tr/$n -f src/aud/$n.wav >/dev/null 2>&1 && echo done $n
done
