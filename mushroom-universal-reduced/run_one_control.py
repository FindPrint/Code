# -*- coding: utf-8 -*-
"""Run UNIVERSAL_LOG (v3.5.5-HP-v1, fichier fourni par Zackary, jamais
modifié) sur mushrooms_reduced_2000.csv, pour UN contrôle donné.
Mêmes paramètres que le lot plein annulé, seul le dataset change.
Usage : python3 run_one_control.py <controle> <dossier_sortie>
"""
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

CONTROL = sys.argv[1]
OUTDIR = Path(sys.argv[2])
OUTDIR.mkdir(parents=True, exist_ok=True)
CODE_PATH = Path('/home/hatch/workspace/user/files/UNIVERSAL_LOG.py')
CSV_PATH = Path('/home/hatch/workspace/mushroom-universal-reduced/data/mushrooms_reduced_2000.csv')

# Import RÉEL sous son vrai nom (comme le pilote) : le Monte Carlo
# multiprocessus pickle les workers par nom de module, un nom synthétique
# (SourceFileLoader) fait échouer le run en 1,6 s (PicklingError).
sys.path.insert(0, '/home/hatch/workspace/user/files')
import UNIVERSAL_LOG as mod

df = pd.read_csv(CSV_PATH)
num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
assert CONTROL in num_cols, 'controle inconnu'
flux_cols = [c for c in num_cols if c != CONTROL]
mapping = {'control_col': CONTROL, 'flux_mapping': {c: c for c in flux_cols}}
opt_cfg = {'w_size': 80, 'test': 'cohen_d', 'random_seed': 42,
           'full_triangulation': False}

t0 = time.time()
try:
    results, df_feat, fluxes, fluxes_ui = mod.run_pipeline(
        data_source='custom', custom_file_path=str(CSV_PATH),
        mapping=mapping, mode='stable', opt_cfg=opt_cfg)
except Exception as e:
    dt = time.time() - t0
    err = {'control': CONTROL, 'status': 'ECHEC', 'duration_s': round(dt, 1),
           'error_type': type(e).__name__, 'error': str(e),
           'n_valides_controle': int(df[CONTROL].notna().sum())}
    (OUTDIR / 'run_summary.json').write_text(
        json.dumps(err, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUTDIR / 'error.txt').write_text(traceback.format_exc(), encoding='utf-8')
    print(json.dumps(err, ensure_ascii=False, indent=2))
    print(f'ECHEC {CONTROL} apres {dt:.1f}s : {e}')
    sys.exit(0)
dt = time.time() - t0

mod.export_json_results(results, OUTDIR / 'pipeline_results.json')
mod.export_csv_results(df_feat, results['scores'], results['noise_diagnostic'],
                       OUTDIR / 'numerical_results.csv')
mod.export_text_report(results, OUTDIR / 'text_report.txt')
main_threshold = results['metadata'].get('opt_threshold', 50)
try:
    mod.plot_threshold_scan(results['scan_curve'], main_threshold,
                            OUTDIR / 'threshold_scan.png')
    mod.plot_noise_diagnostic(results['noise_diagnostic'],
                              OUTDIR / 'noise_diagnostic.png')
except Exception as e:
    print(f'plot warning: {e}')
pd.DataFrame(results.get('scan_curve') or []).to_csv(
    OUTDIR / 'scan_curve.csv', index=False)

md = results['metadata']
to = md.get('threshold_optimization') or {}
bc = to.get('best_config') or {}
summary = {
    'pipeline': 'UNIVERSAL_LOG v3.5.5-HP-v1',
    'code_sha256': '2f58d414e636976737ecb35ae9285aa60eb9102346262e1d882f308b659e4479',
    'code_path': str(CODE_PATH),
    'dataset': 'mushrooms_reduced_2000.csv (sous-échantillon stratifié class, graine 42, de mushrooms_pipeline.csv)',
    'data_sha256': 'dee932631ad36ac0f23cae5f744ee02165764ced49bf5e0f9d1fa21458a9cfe8',
    'control': CONTROL, 'status': 'OK', 'mode': 'stable',
    'n_pts': md.get('n_pts'), 'n_flux': len(fluxes),
    'opt_threshold': md.get('opt_threshold'),
    'w_size_best': bc.get('w_size'),
    'duration_s': round(dt, 1),
}
(OUTDIR / 'run_summary.json').write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
print(f'OK {CONTROL} en {dt:.1f}s, seuil {md.get("opt_threshold")}')
