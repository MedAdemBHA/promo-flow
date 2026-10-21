#!/bin/bash
# One row of 6 frames per clip, stacked: video_strip.sh out.jpg a.mp4 b.mp4 …
FF=${FFMPEG:-ffmpeg}; out=$1; shift; tmp=$(mktemp -d); i=0; ins=()
for f in "$@"; do $FF -v error -y -i "$f" -vf "fps=1,scale=-2:220,pad=ceil(iw/2)*2:220,tile=6x1" -frames:v 1 "$tmp/$i.jpg"; echo "row $i: $(basename "$f")"; ins+=(-i "$tmp/$i.jpg"); i=$((i+1)); done
if [ $i -eq 1 ]; then cp "$tmp/0.jpg" "$out"; else $FF -v error -y "${ins[@]}" -filter_complex "vstack=inputs=$i" "$out" 2>/dev/null || \
  $FF -v error -y "${ins[@]}" -filter_complex "$(for ((k=0;k<i;k++)); do printf "[%d:v]scale=1600:-2[s%d];" $k $k; done)$(for ((k=0;k<i;k++)); do printf "[s%d]" $k; done)vstack=inputs=$i" "$out"; fi
rm -rf "$tmp"; echo "$out"
