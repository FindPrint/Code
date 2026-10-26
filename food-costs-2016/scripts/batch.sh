#!/bin/bash
cd ~/workspace/food-costs-2016
run() {
  col="$1"; label="$2"
  python3 scripts/run_one.py "$col" "results/ctrl_$label" > "results_ctrl_$label.log" 2>&1
  echo "DONE $label $(date +%H:%M:%S)"
}
if [ -f "results/ctrl_Agency/run_summary.json" ]; then echo "SKIP Agency (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "agency_encoded" "Agency" & fi
if [ -f "results/ctrl_2015-10/run_summary.json" ]; then echo "SKIP 2015-10 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-10-01 00:00:00" "2015-10" & fi
if [ -f "results/ctrl_2015-11/run_summary.json" ]; then echo "SKIP 2015-11 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-11-01 00:00:00" "2015-11" & fi
if [ -f "results/ctrl_2015-12/run_summary.json" ]; then echo "SKIP 2015-12 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-12-01 00:00:00" "2015-12" & fi
if [ -f "results/ctrl_2016-01/run_summary.json" ]; then echo "SKIP 2016-01 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-01-01 00:00:00" "2016-01" & fi
if [ -f "results/ctrl_2016-02/run_summary.json" ]; then echo "SKIP 2016-02 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-02-01 00:00:00" "2016-02" & fi
if [ -f "results/ctrl_2016-03/run_summary.json" ]; then echo "SKIP 2016-03 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-03-01 00:00:00" "2016-03" & fi
if [ -f "results/ctrl_2016-04/run_summary.json" ]; then echo "SKIP 2016-04 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-04-01 00:00:00" "2016-04" & fi
if [ -f "results/ctrl_2016-05/run_summary.json" ]; then echo "SKIP 2016-05 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-05-01 00:00:00" "2016-05" & fi
if [ -f "results/ctrl_2016-06/run_summary.json" ]; then echo "SKIP 2016-06 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-06-01 00:00:00" "2016-06" & fi
if [ -f "results/ctrl_2016-07/run_summary.json" ]; then echo "SKIP 2016-07 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-07-01 00:00:00" "2016-07" & fi
if [ -f "results/ctrl_2016-08/run_summary.json" ]; then echo "SKIP 2016-08 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-08-01 00:00:00" "2016-08" & fi
if [ -f "results/ctrl_2016-09/run_summary.json" ]; then echo "SKIP 2016-09 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2016-09-01 00:00:00" "2016-09" & fi
if [ -f "results/ctrl_Cumulative/run_summary.json" ]; then echo "SKIP Cumulative (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "Cumulative Cost" "Cumulative" & fi
wait
echo "BATCH TERMINE"
