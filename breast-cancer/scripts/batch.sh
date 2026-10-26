#!/bin/bash
# Lancer les 31 controles restants (radius_mean deja pilote) - 2 en parallele max.
# Ne pas lancer tant que le pilote radius_mean tourne (sinon 3 simultanes).
cd ~/workspace/breast-cancer
run() {
  c="$1"
  python3 scripts/run_one.py "$c" "results/ctrl_$c" > "results_ctrl_$c.log" 2>&1
  echo "DONE $c $(date +%H:%M:%S)"
}
controls=(
  id texture_mean perimeter_mean area_mean smoothness_mean compactness_mean
  concavity_mean "concave points_mean" symmetry_mean fractal_dimension_mean
  radius_se texture_se perimeter_se area_se smoothness_se compactness_se
  concavity_se "concave points_se" symmetry_se fractal_dimension_se
  radius_worst texture_worst perimeter_worst area_worst smoothness_worst
  compactness_worst concavity_worst "concave points_worst" symmetry_worst
  fractal_dimension_worst diagnosis_encoded
)
for c in "${controls[@]}"; do
  if [ -f "results/ctrl_$c/run_summary.json" ]; then
    echo "SKIP $c (deja termine)"
    continue
  fi
  while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 10; done
  run "$c" &
done
wait
echo "BATCH TERMINE"
