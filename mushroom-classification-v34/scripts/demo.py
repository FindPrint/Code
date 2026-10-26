# -*- coding: utf-8 -*-
"""Quick peer test (EN/FR): run the v3.4 pipeline in fast mode on the
provided mushroom data, control = class, 10 Monte Carlo iterations.
Prints the threshold, its source, and F1/F2 before/after for one
estimator/flux. Full lot: see batch_v34.sh (stable mode, 23 controls).

Test rapide pour les pairs : pipeline v3.4 en mode fast, controle =
class, 10 iterations Monte Carlo. Affiche le seuil, sa source, et les
F1/F2 avant/apres pour un estimateur/flux.
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'pipeline'))
import Tlog_v3_4_harmonic_v3 as pv3

csv_path = BASE / 'data' / 'mushrooms_pipeline.csv'
import pandas as pd
df = pd.read_csv(csv_path)
control = 'class'
flux_cols = [c for c in df.columns if c != control]
mapping = {'control_col': control, 'flux_mapping': {c: c for c in flux_cols}}
opt_cfg = {'w_size': 80, 'test': 'cohen_d', 'random_seed': 42,
           'full_triangulation': False, 'auto_optimize_threshold': True,
           'optimization_iterations': 10, 'harmonic_prob': 0.45}

results, _, _, _ = pv3.run_pipeline(
    data_source='custom', custom_file_path=str(csv_path),
    mapping=mapping, mode='fast', opt_cfg=opt_cfg)
md = results['metadata']
print(f"Threshold / Seuil: {md.get('opt_threshold')}%")
print(f"Source: {md.get('threshold_source')}")
print(f"Warnings / Alertes: {md.get('threshold_warnings')}")
ta = results.get('transition_analysis') or {}
for est, per in ta.items():
    for flux, v in per.items():
        print(f"{est}/{flux}: F1_post={v.get('first_derivative')} "
              f"F2_post={v.get('second_derivative')} "
              f"F1_pre={v.get('first_derivative_pre')} "
              f"F2_pre={v.get('second_derivative_pre')}")
        break
    break
print("Demo OK — full lot: bash scripts/batch_v34.sh")
