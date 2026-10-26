#!/bin/bash
cd ~/workspace/food-costs-2015
run() {
  col="$1"; label="$2"
  python3 scripts/run_one.py "$col" "results/ctrl_$label" > "results_ctrl_$label.log" 2>&1
  echo "DONE $label $(date +%H:%M:%S)"
}
if [ -f "results/ctrl_Agency/run_summary.json" ]; then echo "SKIP Agency (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "agency_encoded" "Agency" & fi
if [ -f "results/ctrl_2014-10/run_summary.json" ]; then echo "SKIP 2014-10 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-10-01 00:00:00" "2014-10" & fi
if [ -f "results/ctrl_2014-11/run_summary.json" ]; then echo "SKIP 2014-11 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-11-01 00:00:00" "2014-11" & fi
if [ -f "results/ctrl_2014-12/run_summary.json" ]; then echo "SKIP 2014-12 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-12-01 00:00:00" "2014-12" & fi
if [ -f "results/ctrl_2015-01/run_summary.json" ]; then echo "SKIP 2015-01 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-01-01 00:00:00" "2015-01" & fi
if [ -f "results/ctrl_2015-02/run_summary.json" ]; then echo "SKIP 2015-02 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-02-01 00:00:00" "2015-02" & fi
if [ -f "results/ctrl_2015-03/run_summary.json" ]; then echo "SKIP 2015-03 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-03-01 00:00:00" "2015-03" & fi
if [ -f "results/ctrl_2015-04/run_summary.json" ]; then echo "SKIP 2015-04 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-04-01 00:00:00" "2015-04" & fi
if [ -f "results/ctrl_2015-05/run_summary.json" ]; then echo "SKIP 2015-05 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-05-01 00:00:00" "2015-05" & fi
if [ -f "results/ctrl_2015-06/run_summary.json" ]; then echo "SKIP 2015-06 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-06-01 00:00:00" "2015-06" & fi
if [ -f "results/ctrl_2015-07/run_summary.json" ]; then echo "SKIP 2015-07 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-07-01 00:00:00" "2015-07" & fi
if [ -f "results/ctrl_2015-08/run_summary.json" ]; then echo "SKIP 2015-08 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-08-01 00:00:00" "2015-08" & fi
if [ -f "results/ctrl_2015-09/run_summary.json" ]; then echo "SKIP 2015-09 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2015-09-01 00:00:00" "2015-09" & fi
if [ -f "results/ctrl_Cumulative/run_summary.json" ]; then echo "SKIP Cumulative (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "Cumulative Cost" "Cumulative" & fi
wait
echo "BATCH TERMINE"
