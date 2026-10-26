# -*- coding: utf-8 -*-
"""Pilote : lance le VRAI pipeline v3.3 (pipeline_autonome_v3_3_fixed.py)
sur le banc Ashkin-Teller, contrôle = energy (aussi flux, règle utilisateur).
Aveugle : le fichier d'entrée at_fluxes.csv ne contient AUCUNE température.
Usage: python3 run_v33_at.py
"""
import sys, json, time
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/hatch/workspace/user/files')
import pipeline_autonome_v3_3_fixed as pv3

BASE = Path('/home/hatch/workspace/multi-tipping')
csv_path = BASE / 'at_fluxes.csv'
outdir = BASE / 'results_at_v33'
outdir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(csv_path)
num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
control = 'energy'
assert control in num_cols
mapping = {'control_col': control, 'flux_mapping': {c: c for c in num_cols}}
opt_cfg = {'w_size': 80, 'test': 'cohen_d', 'random_seed': 42,
           'full_triangulation': False}

t0 = time.time()
results, df_feat, fluxes, fluxes_ui = pv3.run_pipeline(
    data_source='custom', custom_file_path=str(csv_path),
    mapping=mapping, mode='stable', opt_cfg=opt_cfg)
dt = time.time() - t0

# Exports (miroir du main() du pipeline)
pv3.export_json_results(results, outdir / 'pipeline_results.json')
pv3.export_csv_results(df_feat, results['scores'], results['noise_diagnostic'],
                       outdir / 'numerical_results.csv')
pv3.export_text_report(results, outdir / 'text_report.txt')
main_threshold = results['metadata'].get('opt_threshold', 50)
pv3.plot_threshold_scan(results['scan_curve'], main_threshold,
                        outdir / 'threshold_scan.png')
pv3.plot_noise_diagnostic(results['noise_diagnostic'],
                          outdir / 'noise_diagnostic.png')
pv3.plot_complexity_landscape(df_feat, fluxes, main_threshold,
                              outdir / 'landscape_complexity.png')
if results.get('transition_analysis'):
    pv3.plot_post_threshold_analysis(results['transition_analysis'],
                                     outdir / 'post_threshold_analysis.png')
if results.get('anchor_spectrum'):
    pv3.plot_anchor_spectrum(results['anchor_spectrum'],
                             outdir / 'anchor_spectrum.png')
if results['metadata'].get('stability_report'):
    pv3.plot_stability_analysis(results['metadata']['stability_report'],
                                outdir / 'stability_analysis.png')

# Courbe de scan complète (paysage) en CSV pour analyse du second seuil
sc = results.get('scan_curve') or []
pd.DataFrame(sc).to_csv(outdir / 'scan_curve.csv', index=False)

md = results['metadata']
summary = {
    'dataset': csv_path.name, 'control': control, 'mode': 'stable',
    'n_pts': md.get('n_pts'), 'n_flux': len(fluxes),
    'duration_s': round(dt, 1),
    'opt_threshold_pct': md.get('opt_threshold'),
    'threshold_optimization': md.get('threshold_optimization'),
    'stability_report': md.get('stability_report'),
}
with open(outdir / 'run_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps(summary, ensure_ascii=False, indent=2, default=str)[:3000])
print(f"DUREE {dt:.1f}s -> {outdir}")
