#!/bin/bash
# Test 1 encodage alphabetique : class, odor, cap-surface. 2 en parallele, resumable.
cd /home/hatch/workspace/mushroom-tests/encodage
run_one() {
  c=$1
  if [ -f "results/ctrl_$c/run_summary.json" ]; then echo "SKIP $c (deja termine)"; return; fi
  python3 scripts/run_one_alpha.py "$c" "results/ctrl_$c" > "results_ctrl_$c.log" 2>&1
  echo "DONE $c $(date '+%H:%M:%S')"
}
export -f run_one 2>/dev/null || true
( run_one class & run_one odor & wait )
run_one cap-surface
echo "BATCH ALPHA TERMINE"
