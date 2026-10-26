#!/bin/bash
cd ~/workspace/food-costs-2014
run() {
  col="$1"; label="$2"
  python3 scripts/run_one.py "$col" "results/ctrl_$label" > "results_ctrl_$label.log" 2>&1
  echo "DONE $label $(date +%H:%M:%S)"
}
if [ -f "results/ctrl_Agency/run_summary.json" ]; then echo "SKIP Agency (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "agency_encoded" "Agency" & fi
if [ -f "results/ctrl_2013-10/run_summary.json" ]; then echo "SKIP 2013-10 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2013-10-01 00:00:00" "2013-10" & fi
if [ -f "results/ctrl_2013-11/run_summary.json" ]; then echo "SKIP 2013-11 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2013-11-01 00:00:00" "2013-11" & fi
if [ -f "results/ctrl_2013-12/run_summary.json" ]; then echo "SKIP 2013-12 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2013-12-01 00:00:00" "2013-12" & fi
if [ -f "results/ctrl_2014-01/run_summary.json" ]; then echo "SKIP 2014-01 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-01-01 00:00:00" "2014-01" & fi
if [ -f "results/ctrl_2014-02/run_summary.json" ]; then echo "SKIP 2014-02 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-02-01 00:00:00" "2014-02" & fi
if [ -f "results/ctrl_2014-03/run_summary.json" ]; then echo "SKIP 2014-03 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-03-01 00:00:00" "2014-03" & fi
if [ -f "results/ctrl_2014-04/run_summary.json" ]; then echo "SKIP 2014-04 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-04-01 00:00:00" "2014-04" & fi
if [ -f "results/ctrl_2014-05/run_summary.json" ]; then echo "SKIP 2014-05 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-05-01 00:00:00" "2014-05" & fi
if [ -f "results/ctrl_2014-06/run_summary.json" ]; then echo "SKIP 2014-06 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-06-01 00:00:00" "2014-06" & fi
if [ -f "results/ctrl_2014-07/run_summary.json" ]; then echo "SKIP 2014-07 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-07-01 00:00:00" "2014-07" & fi
if [ -f "results/ctrl_2014-08/run_summary.json" ]; then echo "SKIP 2014-08 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-08-01 00:00:00" "2014-08" & fi
if [ -f "results/ctrl_2014-09/run_summary.json" ]; then echo "SKIP 2014-09 (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "2014-09-01 00:00:00" "2014-09" & fi
if [ -f "results/ctrl_Cumulative/run_summary.json" ]; then echo "SKIP Cumulative (deja termine)"; else while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 5; done; run "Cumulative Cost" "Cumulative" & fi
wait
echo "BATCH TERMINE"
