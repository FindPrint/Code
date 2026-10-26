#!/bin/bash
cd "$(dirname "$0")/.."  # repo root (portable)
run() {
  c="$1"
  python3 scripts/run_one_v34.py "$c" "results/ctrl_$c" > "results_ctrl_$c.log" 2>&1
  echo "DONE $c $(date +%H:%M:%S)"
}
controls=(class cap-shape cap-surface cap-color bruises odor gill-attachment gill-spacing gill-size gill-color stalk-shape stalk-root stalk-surface-above-ring stalk-surface-below-ring stalk-color-above-ring stalk-color-below-ring veil-type veil-color ring-number ring-type spore-print-color population habitat)
for c in "${controls[@]}"; do
  if [ -f "results/ctrl_$c/run_summary.json" ]; then
    echo "SKIP $c (deja termine)"
    continue
  fi
  while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 10; done
  run "$c" &
done
wait
echo "BATCH V34 TERMINE"
