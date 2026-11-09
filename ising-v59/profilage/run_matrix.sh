#!/bin/bash
# Matrice de mesures profilage v5.9.0f vs v5.4.0 — cas A_single_fast_off (synth.csv, 200 pts).
# Resumable : saute un cas si master_results.json valide existe deja.
# Usage : nohup bash run_matrix.sh > matrix.log 2>&1 < /dev/null & disown
set -u
P="$HOME/workspace/ising-v59/profilage"
DATA="$HOME/workspace/ising-v425-all-options/data/synth.csv"
LOG="$P/matrix.log"
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
# Baselines (sans profil)
run m01_v540_base python3 "$P/v540.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation
run m02_v590_default python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
# Ablations v590f, un suspect a la fois
run m03_v590_noawf python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light --no-adaptive-walk-forward
run m04_v590_nol7b python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --no-l7b
run m05_v590_nodash python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light --no-dashboard
run m06_v590_notel python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light --no-telemetry
run m07_v590_noregime python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light --no-regime-weights
run m08_v590_alloff python3 "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --no-l7b --no-adaptive-walk-forward --no-dashboard --no-telemetry --no-regime-weights
# Profils cProfile (hotspots ; durees enflees, ne pas comparer aux baselines)
run m09_v540_prof python3 -m cProfile -o "$P/prof540.out" "$P/v540.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation
run m10_v590_prof python3 -m cProfile -o "$P/prof590.out" "$P/v590f.py" --input "$DATA" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
echo "$(date -Is) MATRIX DONE" | tee -a "$LOG"
