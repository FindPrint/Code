# -*- coding: utf-8 -*-
"""Orchestrateur du lot UNIVERSAL_LOG mushroom RÉDUIT : 23 contrôles,
class en premier (sert de mesure de durée).
SÉQUENTIEL et REPRENABLE : un contrôle dont run_summary.json indique OK
est sauté ; un run interrompu est relancé à l'identique à la prochaine
exécution de ce script ; un ECHEC ne bloque pas les contrôles suivants.
Usage : python3 run_lot.py  (log : lot.log, état : lot_progress.json)
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

LOTDIR = Path(__file__).resolve().parent
CSV_PATH = LOTDIR / 'data' / 'mushrooms_reduced_2000.csv'


def log(msg):
    line = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
    print(line, flush=True)
    with open(LOTDIR / 'lot.log', 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def main():
    header = list(pd.read_csv(CSV_PATH, nrows=0).columns)
    assert len(header) == 23, f'colonnes attendues 23, trouvées {len(header)}'
    log(f'Lot réduit : 23 contrôles, ordre CSV : {header}')
    results = {}
    failed = []
    for ctrl in header:
        outdir = LOTDIR / f'ctrl_{ctrl}'
        outdir.mkdir(parents=True, exist_ok=True)
        summ_path = outdir / 'run_summary.json'
        if summ_path.exists():
            try:
                if json.loads(summ_path.read_text(encoding='utf-8')).get('status') == 'OK':
                    log(f'SKIP {ctrl} (déjà OK)')
                    results[ctrl] = 'OK (déjà fait)'
                    continue
            except Exception:
                pass
        log(f'START {ctrl}')
        t0 = time.time()
        with open(outdir / 'run.log', 'w', encoding='utf-8') as lf:
            subprocess.run([sys.executable, str(LOTDIR / 'run_one_control.py'),
                            ctrl, str(outdir)], stdout=lf, stderr=subprocess.STDOUT)
        dt = time.time() - t0
        try:
            st = json.loads(summ_path.read_text(encoding='utf-8')).get('status')
        except Exception:
            st = 'INCONNU (pas de run_summary)'
        log(f'END {ctrl} : {st} en {dt:.1f}s')
        results[ctrl] = st
        if st != 'OK':
            failed.append(ctrl)
        (LOTDIR / 'lot_progress.json').write_text(
            json.dumps({'results': results, 'failed': failed},
                       ensure_ascii=False, indent=2), encoding='utf-8')
    log(f'Lot réduit terminé. Échecs : {failed if failed else "aucun"}')
    print(json.dumps({'results': results, 'failed': failed},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
