# -*- coding: utf-8 -*-
"""Pilote générique : pipeline v3.3 tel quel sur un CSV de flux.
Usage: python3 run_v33_generic.py <fluxes.csv> <outdir>
Contrôle = energy (aussi flux), mode stable, graine 42 — identique vague 1.
"""
import sys, json, time
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/hatch/workspace/user/files')
import pipeline_autonome_v3_3_fixed as pv3

csv_path = Path(sys.argv[1]).resolve()
outdir = Path(sys.argv[2]).resolve()
outdir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(csv_path)
num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
control = 'energy'
assert control in num_cols, f"pas de colonne energy dans {csv_path}"
mapping = {'control_col': control, 'flux_mapping': {c: c for c in num_cols}}
opt_cfg = {'w_size': 80, 'test': 'cohen_d', 'random_seed': 42,
           'full_triangulation': False}

t0 = time.time()
results, df_feat, fluxes, fluxes_ui = pv3.run_pipeline(
    data_source='custom', custom_file_path=str(csv_path),
    mapping=mapping, mode='stable', opt_cfg=opt_cfg)
dt = time.time() - t0

pv3.export_json_results(results, outdir / 'pipeline_results.json')
pv3.export_csv_results(df_feat, results['scores'], results['noise_diagnostic'],
                       outdir / 'numerical_results.csv')
pv3.export_text_report(results, outdir / 'text_report.txt')
main_threshold = results['metadata'].get('opt_threshold', 50)
pv3.plot_threshold_scan(results['scan_curve'], main_threshold,
                        outdir / 'threshold_scan.png')
pv3.plot_noise_diagnostic(results['noise_diagnostic'],
                          outdir / 'noise_diagnostic.png')
pd.DataFrame(results.get('scan_curve') or []).to_csv(outdir / 'scan_curve.csv', index=False)

md = results['metadata']
to = md.get('threshold_optimization') or {}
bc = to.get('best_config') or {}
summary = {
    'dataset': csv_path.name, 'control': control, 'n_pts': md.get('n_pts'),
    'duration_s': round(dt, 1),
    'opt_threshold_pct': md.get('opt_threshold'),
    'mc_threshold_pct': bc.get('threshold'), 'mc_score': bc.get('score'),
    'mc_w_size': bc.get('w_size'), 'mc_n_candidates': bc.get('n_candidates'),
    'default_threshold_pct': to.get('default_threshold'),
    'raw_mc_threshold_pct': to.get('raw_mc_threshold'),
    'raw_default_threshold_pct': to.get('raw_default_threshold'),
    'stability': md.get('stability_report'),
    'noise_label': (results.get('noise_diagnostic') or {}).get('diagnostic_label'),
}
with open(outdir / 'run_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
print(f"DUREE {dt:.1f}s -> {outdir}")
