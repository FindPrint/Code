#!/bin/bash
cd ~/workspace/earthquake-tsunami-v33fixed
run() {
  c=$1
  python3 scripts/run_one.py "$c" "results/ctrl_$c" > "results_ctrl_$c.log" 2>&1
  echo "DONE $c $(date +%H:%M:%S)"
}
export -f run
printf "%s\n" cdi mmi sig nst dmin gap depth latitude longitude Year Month tsunami | xargs -P 2 -I{} bash -c 'run "$@"' _ {}
echo "BATCH TERMINE"
