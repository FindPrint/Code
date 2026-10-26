#!/bin/bash
# Vague 2 — portes A (réplication AT), B (nul), C (horloge q=6).
# Protocole gelé : PROTOCOLE_VAGUE2.md. Séquentiel, journalisé, continue sur erreur.
BASE=/home/hatch/workspace/multi-tipping
V=$BASE/vague2
mkdir -p $V/data $V/at_s7 $V/at_s123 $V/at_L36 $V/null $V/clock
cd $BASE
step() { echo "=== [$(date +%H:%M:%S)] $* ==="; }

step "GEN AT seed 7"
python3 gen_ashkin_teller.py --seed 7 --L 28 --prefix at_s7 --outdir $V/data
step "GEN AT seed 123"
python3 gen_ashkin_teller.py --seed 123 --L 28 --prefix at_s123 --outdir $V/data
step "GEN AT L36 seed 42"
python3 gen_ashkin_teller.py --seed 42 --L 36 --prefix at_L36 --outdir $V/data
step "GEN NUL (lignes melangees, graine 99)"
python3 -c "
import pandas as pd
d = pd.read_csv('$BASE/at_fluxes.csv')
d.sample(frac=1.0, random_state=99).to_csv('$V/data/at_null_fluxes.csv', index=False)
print('null:', len(d), 'lignes')
"

run() { # $1 fluxes $2 temp|none $3 outdir $4 win1 $5 win2 $6 nom
  step "PIPELINE $6"
  python3 run_v33_generic.py "$1" "$3" > "$3/driver.log" 2>&1
  echo "driver exit=$? $6"
  step "ANALYSE $6"
  python3 analyse_generic.py "$1" "$2" "$3" "$4" "$5" > "$3/analyse.log" 2>&1
  echo "analyse exit=$? $6"
}

run $V/data/at_s7_fluxes.csv   $V/data/at_s7_temperature.csv   $V/at_s7   50,60 62,73 AT_seed7
run $V/data/at_s123_fluxes.csv $V/data/at_s123_temperature.csv $V/at_s123 50,60 62,73 AT_seed123
run $V/data/at_L36_fluxes.csv  $V/data/at_L36_temperature.csv  $V/at_L36  50,60 62,73 AT_L36
run $V/data/at_null_fluxes.csv none                            $V/null    50,60 62,73 NUL
run $BASE/clock6_fluxes.csv    $BASE/clock6_temperature.csv    $V/clock   30,46 52,68 HORLOGE

step "VAGUE 2 TERMINEE"
