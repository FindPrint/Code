#!/bin/bash
cd ~/workspace/food-costs-2013
run() {
  col="$1"; label="$2"
  python3 scripts/run_one.py "$col" "results/ctrl_$label" > "results_ctrl_$label.log" 2>&1
  echo "DONE $label $(date +%H:%M:%S)"
}
# ordre du fichier, Cumulative deja fait en pilote
declare -A M=(
  [Agency]="agency_encoded"
  [2012-10]="2012-10-01 00:00:00"
  [2012-11]="2012-11-01 00:00:00"
  [2012-12]="2012-12-01 00:00:00"
  [2013-01]="2013-01-01 00:00:00"
  [2013-02]="2013-02-01 00:00:00"
  [2013-03]="2013-03-01 00:00:00"
  [2013-04]="2013-04-01 00:00:00"
  [2013-05]="2013-05-01 00:00:00"
  [2013-06]="2013-06-01 00:00:00"
  [2013-07]="2013-07-01 00:00:00"
  [2013-08]="2013-08-01 00:00:00"
  [2013-09]="2013-09-01 00:00:00"
)
for label in Agency 2012-10 2012-11 2012-12 2013-01 2013-02 2013-03 2013-04 2013-05 2013-06 2013-07 2013-08 2013-09; do
  if [ -f "results/ctrl_$label/run_summary.json" ]; then
    echo "SKIP $label (deja termine)"
    continue
  fi
  while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done
  run "${M[$label]}" "$label" &
done
wait
echo "BATCH TERMINE"
