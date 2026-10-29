#!/usr/bin/env bash
# usage: render_par.sh <comp.html> <out.mp4> <W> <H> <fps> <dur> <workers>
COMP=$1; OUT=$2; W=$3; H=$4; FPS=$5; DUR=$6; N=$7
FR=$(python -c "print(round($DUR*$FPS))"); PER=$(( (FR + N - 1) / N ))
DIR=$(dirname "$OUT"); : > "$DIR/_segs.txt"; pids=()
for ((i=0;i<N;i++)); do
  F0=$((i*PER)); F1=$(((i+1)*PER)); [ $F1 -gt $FR ] && F1=$FR; [ $F0 -ge $F1 ] && break
  T0=$(python -c "print($F0/$FPS)"); T1=$(python -c "print($F1/$FPS)")
  node render.mjs "$COMP" "$DIR/_seg$i.mp4" --w $W --h $H --fps $FPS --from $T0 --to $T1 > "$DIR/_seg$i.log" 2>&1 &
  pids+=($!); echo "file '_seg$i.mp4'" >> "$DIR/_segs.txt"
done
fail=0; for p in "${pids[@]}"; do wait $p || fail=1; done
[ $fail = 1 ] && { echo "a worker failed"; tail -3 "$DIR"/_seg*.log; exit 1; }
(cd "$DIR" && ffmpeg -y -loglevel error -f concat -safe 0 -i _segs.txt -c copy -movflags +faststart "$(basename "$OUT")") && rm -f "$DIR"/_seg*.mp4 "$DIR"/_seg*.log "$DIR/_segs.txt"
echo "ALL DONE $OUT"
