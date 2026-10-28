#!/bin/bash
# Lot ising-v354 : 6 runs en rotation, max 2 en parallèle.
# Reprise : un run avec runs/<controle>/run_summary.json est sauté.
# Journal maître : run_lot.log (ce script est lancé détaché).
set -u
BASE=/home/hatch/workspace/ising-v354
cd "$BASE"
CONTROLS="fliprate flip energy magnetization localvar susceptibility"
run_one() {
  c="$1"
  out="runs/$c"
  if grep -q '"status": "OK"' "$out/run_summary.json" 2>/dev/null && [ -f "$out/per_flux_thresholds.csv" ]; then
    echo "$(date -u +%FT%TZ) SKIP $c (run terminé OK)" >> run_lot.log
    return 0
  fi
  mkdir -p "$out"
  echo "$(date -u +%FT%TZ) DÉBUT $c" >> run_lot.log
  python3 run_one_ising.py "$c" "$out" > "$out/run.log" 2>&1
  echo "$(date -u +%FT%TZ) FIN $c (code $?) " >> run_lot.log
}
export -f run_one
export BASE
printf '%s\n' $CONTROLS | xargs -P 2 -I{} bash -c 'run_one "$@"' _ {}
echo "$(date -u +%FT%TZ) LOT TERMINÉ" >> run_lot.log
