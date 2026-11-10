#!/bin/bash
# word-level whisper on a window: words.sh clip start end
cd "$(dirname "$0")/.."; c=$1; s=$(echo "$2-4" | bc); [ $(echo "$s<0"|bc) = 1 ] && s=0; d=$(echo "$3-$s+4" | bc)
o=src/win/${c}_$2; ffmpeg -nostdin -v error -y -ss $s -t $d -i src/aud/$c.wav $o.wav
whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-medium.en.bin --prompt 'Umm, err, uh. Right, go on, push.' -t 3 -ml 1 -sow -oj -of $o -f $o.wav >/dev/null 2>&1
python3 -c "
import json;d=json.load(open('$o.json'));s=$s
print('== $c $2-$3', ' '.join(f\"{x['text'].strip()}@{s+x['offsets']['from']/1000:.1f}\" for x in d['transcription'] if x['text'].strip()))"
