# -*- coding: utf-8 -*-
"""Analyse générique post-run (le pipeline n'a jamais vu la température).
Usage: python3 analyse_generic.py <fluxes.csv> <temperature.csv|none> <outdir> <win1a,win1b> <win2a,win2b>
Produit : per_flux_thresholds.csv, verdict.json (seuils propres par flux avec la
fonction de scan du pipeline et la config MC du run, mapping % -> T si dispo,
zones du paysage global, drapeaux de hit contre les fenêtres gelées).
"""
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, '/home/hatch/workspace/user/files')
import pipeline_autonome_v3_3_fixed as pv3

flux_path, temp_arg, outdir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
win1 = tuple(float(x) for x in sys.argv[4].split(','))
win2 = tuple(float(x) for x in sys.argv[5].split(','))

df = pd.read_csv(flux_path)
n = len(df)
energy = df['energy'].values
progress = 100.0 * stats.rankdata(energy, method='average') / n
temp = None
if temp_arg != 'none':
    temp = pd.read_csv(temp_arg)['temperature'].values

summ = json.load(open(outdir / 'run_summary.json'))
W = int(summ.get('mc_w_size') or 137)
NC = int(summ.get('mc_n_candidates') or 660)
mode_cfg = {'n_est': 4, 'w_size': 80, 'test': 'cohen_d', 'min_grp': 4,
            'min_len': 80, 'boot': True, 'full_triangulation': False,
            'random_seed': 42}

def z(s):
    s = np.asarray(s, float)
    return (s - s.mean()) / s.std() if s.std() > 1e-10 else np.zeros_like(s)

order = np.argsort(energy, kind='stable')
temp_sorted = temp[order] if temp is not None else None
def map_T(pct, band=1.5):
    if temp_sorted is None:
        return None, None
    k = pct / 100.0 * n
    lo = max(0, int(k - band / 100 * n)); hi = min(n, int(k + band / 100 * n))
    w = temp_sorted[lo:hi]
    return round(float(w.mean()), 3), round(float(w.std()), 3)

rows = []
for col in df.columns:
    th, curve = pv3.scan_critical_threshold(
        {col: z(df[col].values)}, progress, mode_cfg,
        n_candidates=NC, w_size=W, min_grp=3)
    sc = pd.DataFrame(curve).dropna(subset=['score'])
    m, s = map_T(float(th))
    rows.append({'flux': col, 'seuil_propre_pct': round(float(th), 2),
                 'score_max': round(float(sc['score'].max()), 3),
                 'T_estime': m, 'T_std': s,
                 'dans_fenetre1': bool(win1[0] <= th <= win1[1]),
                 'dans_fenetre2': bool(win2[0] <= th <= win2[1])})
pf = pd.DataFrame(rows)
pf.to_csv(outdir / 'per_flux_thresholds.csv', index=False)

# Paysage global : zones de la courbe de scan (défaut, traitée)
c = pd.DataFrame(json.load(open(outdir / 'pipeline_results.json'))['scan_curve']).dropna(subset=['score'])
def zone(a, b):
    v = c[(c.candidate >= a) & (c.candidate <= b)]['score']
    return round(float(v.mean()), 3) if len(v) else None

mc = summ.get('mc_threshold_pct')
verdict = {
    'dataset': flux_path.name,
    'global_mc_pct': mc,
    'global_mc_T': map_T(mc) if mc else None,
    'global_in_fenetre1': bool(mc and win1[0] <= mc <= win1[1]),
    'global_in_fenetre2': bool(mc and win2[0] <= mc <= win2[1]),
    'stabilite': (summ.get('stability') or {}).get('rating'),
    'stabilite_std': (summ.get('stability') or {}).get('std'),
    'mc_score': summ.get('mc_score'),
    'flux_fenetre1': pf.loc[pf.dans_fenetre1, 'flux'].tolist(),
    'flux_fenetre2': pf.loc[pf.dans_fenetre2, 'flux'].tolist(),
    'paysage_zones': {'win1': zone(*win1), 'win2': zone(*win2),
                      'apres_win2': zone(win2[1] + 2, win2[1] + 14),
                      'loin_88_97': zone(88, 97),
                      'max_global': round(float(c['score'].max()), 3)},
    'per_flux': rows,
}
with open(outdir / 'verdict.json', 'w', encoding='utf-8') as f:
    json.dump(verdict, f, ensure_ascii=False, indent=2)
print(json.dumps(verdict, ensure_ascii=False, indent=2))
