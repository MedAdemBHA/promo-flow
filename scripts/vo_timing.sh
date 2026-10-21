#!/bin/bash
# Speech ranges from a VO wav (no whisper needed). vo_timing.sh file.wav [offset=0.4]
# coarse (-35dB, 0.25s) ≈ lines · fine (-30dB, 0.08s) ≈ words/commas. Times are shifted by the VO offset.
FF=${FFMPEG:-ffmpeg}; f=$1; off=${2:-0.4}
dur=$(${FFPROBE:-ffprobe} -v error -show_entries format=duration -of csv=p=0 "$f")
for mode in "coarse -35dB 0.25" "fine -30dB 0.08"; do set -- $mode
  echo "== $1 speech ranges (composition time, VO at +$off s, duration $dur s)"
  $FF -i "$f" -af silencedetect=noise=$2:d=$3 -f null - 2>&1 | grep -oE "silence_(start|end): [0-9.]+" | awk -v off=$off -v dur=$dur '
    /start/ {s=$2; if (s>0.05) printf "%.2f–%.2f  ", (e==""?0:e)+off, s+off} /end/ {e=$2} END {if (e<dur-0.05) printf "%.2f–%.2f", e+off, dur+off; print ""}'
done
