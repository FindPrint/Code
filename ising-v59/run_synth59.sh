#!/bin/bash
set -u
CODE="$HOME/workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py"
DATA="$HOME/workspace/ising-v425-all-options/data"
BASE="$HOME/workspace/ising-v59/synth"
mkdir -p "$BASE"
run() {
  local name="$1"; shift
  local out="$BASE/$name"
  if [ -f "$out/master_results.json" ] && python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out/master_results.json" 2>/dev/null; then
    echo "$(date -Is) SKIP $name" | tee -a "$BASE/run.log"; return 0
  fi
  echo "$(date -Is) START $name" | tee -a "$BASE/run.log"
  local start end rc
  start=$(date +%s)
  timeout 1200 python3 "$CODE" "$@" --output "$out" >> "$BASE/run.log" 2>&1
  rc=$?
  end=$(date +%s)
  echo "$(date -Is) END $name rc=$rc duree_s=$((end-start))" | tee -a "$BASE/run.log"
}
for mode in fast full predict analyze stable robust; do
  run "A_single_${mode}_off" --input "$DATA/synth.csv" --mode "$mode" --control-mode single --control ControlA --no-harmonic-validation --l7b-light
  run "B_single_${mode}_on" --input "$DATA/synth.csv" --mode "$mode" --control-mode single --control ControlA --harmonic-validation --l7b-light
done
for mode in fast stable; do
  run "C_multi_${mode}_off" --input "$DATA/synth.csv" --mode "$mode" --control-mode multi --controls "ControlA,Flux1" --no-harmonic-validation --l7b-light
  run "C_multi_${mode}_on" --input "$DATA/synth.csv" --mode "$mode" --control-mode multi --controls "ControlA,Flux1" --harmonic-validation --l7b-light
  run "C_all_${mode}_off" --input "$DATA/synth.csv" --mode "$mode" --control-mode all --no-harmonic-validation --l7b-light
done
run "D_nan_fast_off" --input "$DATA/synth_nan.csv" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
run "D_const_fast_off" --input "$DATA/synth_const.csv" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
run "D_const_fast_on" --input "$DATA/synth_const.csv" --mode fast --control-mode single --control ControlA --harmonic-validation --l7b-light
run "D_const_stable_off" --input "$DATA/synth_const.csv" --mode stable --control-mode single --control ControlA --no-harmonic-validation --l7b-light
run "D_const_robust_off" --input "$DATA/synth_const.csv" --mode robust --control-mode single --control ControlA --no-harmonic-validation --l7b-light
run "D_missing_control" --input "$DATA/synth.csv" --mode fast --control-mode single --control Inexistant --no-harmonic-validation --l7b-light
run "D_target_eq_control" --input "$DATA/synth.csv" --mode fast --control-mode single --control ControlA --target ControlA --no-harmonic-validation --l7b-light
run "D_no_control" --input "$DATA/synth.csv" --mode fast --control-mode single --no-harmonic-validation --l7b-light
run "D_seed7_horizon5" --input "$DATA/synth.csv" --mode fast --control-mode single --control ControlA --seed 7 --horizon 5 --no-harmonic-validation --l7b-light
run "D_domain_physics" --input "$DATA/synth.csv" --mode fast --control-mode single --control ControlA --domain physics --no-harmonic-validation --l7b-light
run "D_2000_fast_off" --input "$DATA/synth_2000.csv" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
run "D_short" --input "$DATA/synth_short.csv" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
run "D_missing_file" --input "$DATA/nonexistent.csv" --mode fast --control-mode single --control ControlA --no-harmonic-validation --l7b-light
echo "$(date -Is) SYNTH DONE" | tee -a "$BASE/run.log"
