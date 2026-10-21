#!/bin/bash
# Contact sheet of images with their file names: contact_sheet.sh out.jpg a.png b.png …  (6 columns, 320px cells)
FF=${FFMPEG:-ffmpeg}
# labels need the drawtext filter (Homebrew ffmpeg may lack it) → set FFMPEG_DRAWTEXT=/path/to/ffmpeg-with-drawtext,
# else any Homebrew ffmpeg that has it is used, else the sheet is made without labels (cell order is printed)
if ! $FF -hide_banner -filters 2>/dev/null | grep -q drawtext; then
  for c in ${FFMPEG_DRAWTEXT:-} $(ls /opt/homebrew/Cellar/ffmpeg*/*/bin/ffmpeg 2>/dev/null); do
    [ -x "$c" ] && $c -hide_banner -filters 2>/dev/null | grep -q drawtext && FF=$c && break; done; fi
$FF -hide_banner -filters 2>/dev/null | grep -q drawtext && LBL=1 || LBL=0
FONT=${FONT:-/System/Library/Fonts/Supplemental/Arial.ttf}
out=$1; shift; args=(); for f in "$@"; do args+=(-i "$f"); done; n=$#; cols=${COLS:-6}
fc=""; k=0; for f in "$@"; do t=$(basename "$f" | sed 's/\.[^.]*$//' | cut -c1-24 | tr -d "':"); fc+="[$k:v]scale=320:320:force_original_aspect_ratio=decrease,pad=320:340:(ow-iw)/2:20:color=gray$( [ $LBL = 1 ] && echo ",drawtext=fontfile=${FONT}:text=$t:x=4:y=2:fontsize=16:fontcolor=white")[v$k];"; [ $LBL = 0 ] && echo "cell $k: $t"; k=$((k+1)); done
ins=""; lay=""; for ((k=0;k<n;k++)); do ins+="[v$k]"; lay+="$(( (k%cols)*320 ))_$(( (k/cols)*340 ))|"; done
if [ "$n" -eq 1 ]; then $FF -v error -y "${args[@]}" -filter_complex "${fc%;}" -map "[v0]" -frames:v 1 "$out"; else
$FF -v error -y "${args[@]}" -filter_complex "${fc}${ins}xstack=inputs=${n}:layout=${lay%|}:fill=black" -frames:v 1 "$out"; fi
[ -s "$out" ] && echo "$out" || { echo "contact sheet failed" >&2; exit 1; }
