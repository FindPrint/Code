#!/bin/bash
cd ~/workspace/air-quality
run() {
  c="$1"
  python3 scripts/run_one.py "$c" "results/ctrl_$c" > "results_ctrl_$c.log" 2>&1
  echo "DONE $c $(date +%H:%M:%S)"
}
controls=(PM2.5 PM10 NOx NO2 SO2 VOCs CO CO2 CH4 Temperature)
for c in "${controls[@]}"; do
  if [ -f "results/ctrl_$c/run_summary.json" ]; then
    echo "SKIP $c (deja termine)"
    continue
  fi
  while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 10; done
  run "$c" &
done
wait
echo "BATCH TERMINE"
