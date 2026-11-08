#!/bin/bash
# Run unique décisif : full/fliprate v5.9.0f (étape 2 du test étagé).
# Mêmes drapeaux et même journalisation que run_ising59.sh, un seul run.
# Lancé depuis le fil principal le 8 nov. 2026 à 14h13, sur délégation de Zackary
# (« À toi de voir », indisponible lun.–jeu. 2h–17h).
set -u
CODE="$HOME/workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py"
INPUT="$HOME/workspace/ising-v354/data/ising_classic_v354.csv"
BASE="$HOME/workspace/ising-v59/ising"
mkdir -p "$BASE"
mode=full; ctrl=fliprate
out="$BASE/${mode}/${ctrl}"
if [ -f "$out/master_results.json" ] && python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out/master_results.json" 2>/dev/null; then
  echo "$(date -Is) SKIP $mode/$ctrl" | tee -a "$BASE/run.log"; exit 0
fi
echo "$(date -Is) START $mode/$ctrl" | tee -a "$BASE/run.log"
start=$(date +%s)
timeout 21600 python3 "$CODE" --input "$INPUT" --mode "$mode" --control-mode single --control "$ctrl" --no-harmonic-validation --l7b-light --output "$out" >> "$BASE/run.log" 2>&1
rc=$?
end=$(date +%s)
echo "$(date -Is) END $mode/$ctrl rc=$rc duree_s=$((end-start))" | tee -a "$BASE/run.log"
