#!/bin/bash
# Matrice 2 — test de l'hypothese multi-horizons (v5.6, defaut 1..12).
# --horizons "7" = un seul horizon = comportement legacy v5.4.0 pour L1/L3/L5/L6.
# Resumable comme run_matrix.sh.
set -u
P="$HOME/workspace/ising-v59/profilage"
DATA="$HOME/workspace/ising-v425-all-options/data/synth.csv"
LOG="$P/matrix2.log"
mkdir -p "$P/out"
run() {
  local name="$1"; shift
  local out="$P/out/$name"
  if [ -f "$out/master_results.json" ] && python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out/master_results.json" 2>/dev/null; then
    echo "$(date -Is) SKIP $name" | tee -a "$LOG"; return 0
  fi
  echo "$(date -Is) START $name : $*" | tee -a "$LOG"
  local start end rc
  start=$(date +%s)
  timeout 600 "$@" --output "$out" >> "$LOG" 2>&1
  rc=$?
  end=$(date +%s)
  echo "$(date -Is) END $name rc=$rc duree_s=$((end-start))" | tee -a "$LOG"
}
run m11_v590_h7 python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light --horizons "7"
run m12_v590_h13612 python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light --horizons "1,3,6,12"
run m13_v590_h7_alloff python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --no-l7b --no-adaptive-walk-forward --no-dashboard --no-telemetry --no-regime-weights --horizons "7"
echo "$(date -Is) MATRIX2 DONE" | tee -a "$LOG"
