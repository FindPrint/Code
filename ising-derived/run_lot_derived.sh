#!/bin/bash
# Lot dérivés : 8 contrôles dérivés + 3 nuls, max 2 en parallèle, reprise sur run_summary.json.
cd /home/hatch/workspace/ising-derived
declare -A FAM=( [expvar_energy]=expvar [expvar_magnetization]=expvar [expvar_fliprate]=expvar [expvar_localvar]=expvar [expmean_energy]=expmean [expmean_magnetization]=expmean [rollvar_magnetization_40]=rollvar [rollvar_energy_40]=rollvar [null_susceptibility]=nul [null_expvar_mag]=nul [null_rollvar_mag]=nul )
declare -A CST=( [expvar_energy]="Var expansive ddof=1 par bloc de 40, reset" [expvar_magnetization]="Var expansive ddof=1 par bloc de 40, reset" [expvar_fliprate]="Var expansive ddof=1 par bloc de 40, reset" [expvar_localvar]="Var expansive ddof=1 par bloc de 40, reset" [expmean_energy]="Moyenne expansive par bloc de 40, reset" [expmean_magnetization]="Moyenne expansive par bloc de 40, reset" [rollvar_magnetization_40]="Var glissante fenetre 40, sans reset" [rollvar_energy_40]="Var glissante fenetre 40, sans reset" [null_susceptibility]="Permutation default_rng(1234) de susceptibility" [null_expvar_mag]="Permutation default_rng(1234) de expvar_magnetization" [null_rollvar_mag]="Permutation default_rng(1234) de rollvar_magnetization_40" )
CONTROLS="expvar_energy expvar_magnetization expvar_fliprate expvar_localvar expmean_energy expmean_magnetization rollvar_magnetization_40 rollvar_energy_40 null_susceptibility null_expvar_mag null_rollvar_mag"
run_one() {
  local c="$1"
  local d="runs/$c"
  if [ -f "$d/run_summary.json" ] && python3 -c "import json,sys; sys.exit(0 if json.load(open('$d/run_summary.json')).get('status')=='OK' else 1)" 2>/dev/null; then
    echo "$(date -u +%FT%TZ) SAUTE $c (déjà OK)" >> run_lot_derived.log; return 0
  fi
  rm -rf "$d"; mkdir -p "$d"
  echo "$(date -u +%FT%TZ) DÉBUT $c" >> run_lot_derived.log
  python3 run_one_derived.py "$c" "$d" "${FAM[$c]}" "${CST[$c]}" > "$d/run.log" 2>&1
  echo "$(date -u +%FT%TZ) FIN $c (code $?) " >> run_lot_derived.log
}
export -f run_one
echo "$CONTROLS" | tr ' ' '\n' | xargs -P 2 -I{} bash -c 'run_one "$@"' _ {}
echo "$(date -u +%FT%TZ) LOT TERMINÉ" >> run_lot_derived.log
