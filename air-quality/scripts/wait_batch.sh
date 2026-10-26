#!/bin/bash
# Attend la fin du lot air-quality (BATCH TERMINE dans batch.log), max 3h.
for i in $(seq 1 180); do
  if grep -q "BATCH TERMINE" ~/workspace/air-quality/batch.log 2>/dev/null; then
    echo "LOT TERMINE"
    cat ~/workspace/air-quality/batch.log
    echo "--- run_summary.json presents ---"
    ls ~/workspace/air-quality/results/*/run_summary.json 2>/dev/null
    python3 -c "
import json, glob
for p in sorted(glob.glob('/home/hatch/workspace/air-quality/results/*/run_summary.json')):
    s=json.load(open(p)); print(s.get('control'), s.get('status'), 'MC', s.get('mc_threshold_pct'), 'stab', s.get('stability_rating'), 'duree', s.get('duration_s'))
"
    exit 0
  fi
  sleep 60
done
echo "TIMEOUT 3h - etat actuel:"
cat ~/workspace/air-quality/batch.log 2>/dev/null
ls ~/workspace/air-quality/results/*/run_summary.json 2>/dev/null
exit 1
