#!/bin/bash
# Lot dérivés EXT : 8 contrôles dérivés + 4 nuls, max 2 en parallèle, reprise sur run_summary.json.
cd /home/hatch/workspace/ising-derived
declare -A FAM=( [expmean_fliprate]=expmean [expmean_localvar]=expmean [rollvar_fliprate_40]=rollvar [rollvar_localvar_40]=rollvar [rollmean_energy_40]=rollmean [rollmean_magnetization_40]=rollmean [rollmean_fliprate_40]=rollmean [rollmean_localvar_40]=rollmean [null_expmean_fliprate]=nul [null_rollvar_fliprate]=nul [null_rollmean_mag]=nul [null_rollmean_localvar]=nul )
declare -A CST=( [expmean_fliprate]="Moyenne expansive par bloc de 40, reset" [expmean_localvar]="Moyenne expansive par bloc de 40, reset" [rollvar_fliprate_40]="Var glissante fenetre 40, sans reset" [rollvar_localvar_40]="Var glissante fenetre 40, sans reset" [rollmean_energy_40]="Moyenne glissante fenetre 40, sans reset" [rollmean_magnetization_40]="Moyenne glissante fenetre 40, sans reset" [rollmean_fliprate_40]="Moyenne glissante fenetre 40, sans reset" [rollmean_localvar_40]="Moyenne glissante fenetre 40, sans reset" [null_expmean_fliprate]="Permutation default_rng(1234) de expmean_fliprate" [null_rollvar_fliprate]="Permutation default_rng(1234) de rollvar_fliprate_40" [null_rollmean_mag]="Permutation default_rng(1234) de rollmean_magnetization_40" [null_rollmean_localvar]="Permutation default_rng(1234) de rollmean_localvar_40" )
CONTROLS="expmean_fliprate expmean_localvar rollvar_fliprate_40 rollvar_localvar_40 rollmean_energy_40 rollmean_magnetization_40 rollmean_fliprate_40 rollmean_localvar_40 null_expmean_fliprate null_rollvar_fliprate null_rollmean_mag null_rollmean_localvar"
run_one() {
  local c="$1"
  local d="runs_ext/$c"
  if [ -f "$d/run_summary.json" ] && python3 -c "import json,sys; sys.exit(0 if json.load(open('$d/run_summary.json')).get('status')=='OK' else 1)" 2>/dev/null; then
    echo "$(date -u +%FT%TZ) SAUTE $c (déjà OK)" >> run_lot_ext.log; return 0
  fi
  rm -rf "$d"; mkdir -p "$d"
  echo "$(date -u +%FT%TZ) DÉBUT $c" >> run_lot_ext.log
  python3 run_one_derived_ext.py "$c" "$d" "${FAM[$c]}" "${CST[$c]}" > "$d/run.log" 2>&1
  echo "$(date -u +%FT%TZ) FIN $c (code $?) " >> run_lot_ext.log
}
export -f run_one
echo "$CONTROLS" | tr ' ' '\n' | xargs -P 2 -I{} bash -c 'run_one "$@"' _ {}
echo "$(date -u +%FT%TZ) LOT TERMINÉ" >> run_lot_ext.log
