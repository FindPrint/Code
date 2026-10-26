# -*- coding: utf-8 -*-
"""Analyse post-run pour un contrôle arbitraire (pipeline harmonique v1).
Usage: python3 analyse_ctrl.py <fluxes.csv> <control> <temperature.csv|none> <outdir>
        <win1a,win1b> <win2a,win2b> <T1a,T1b> <T2a,T2b>
- Axe de progression = rang du contrôle (pas toujours energy).
- Mapping % -> T via les températures des lignes autour de la frontière de rang
  du contrôle (bande ±1,5 %).
- Scans par flux EXCLUANT le contrôle (règle porte D), avec la fonction de scan
  du pipeline harmonique et la config MC du run.
- Critères jugés en T mappée (fenêtres T1/T2 données en arguments).
- Diagnostic : corrélation de Spearman contrôle vs T (si températures dispo).
Produit : per_flux_thresholds.csv, verdict.json.
"""
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, '/home/hatch/workspace/user/files')
import pipeline_autonome_v3_3_harmonic_v1 as pv3

flux_path, control, temp_arg, outdir = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
win1 = tuple(float(x) for x in sys.argv[5].split(','))
win2 = tuple(float(x) for x in sys.argv[6].split(','))
T1w = tuple(float(x) for x in sys.argv[7].split(','))
T2w = tuple(float(x) for x in sys.argv[8].split(','))

df = pd.read_csv(flux_path)
n = len(df)
ctrl = df[control].values.astype(float)
progress = 100.0 * stats.rankdata(ctrl, method='average') / n
temp = None
if temp_arg != 'none':
    temp = pd.read_csv(temp_arg)['temperature'].values.astype(float)

summ = json.load(open(outdir / 'run_summary.json'))
W = int(summ.get('mc_w_size') or 137)
NC = int(summ.get('mc_n_candidates') or 660)
mode_cfg = {'n_est': 4, 'w_size': 80, 'test': 'cohen_d', 'min_grp': 4,
            'min_len': 80, 'boot': True, 'full_triangulation': False,
            'random_seed': 42}

def z(s):
    s = np.asarray(s, float)
    return (s - s.mean()) / s.std() if s.std() > 1e-10 else np.zeros_like(s)

order = np.argsort(ctrl, kind='stable')
temp_sorted = temp[order] if temp is not None else None
def map_T(pct, band=1.5):
    if temp_sorted is None:
        return None, None
    k = pct / 100.0 * n
    lo = max(0, int(k - band / 100 * n)); hi = min(n, int(k + band / 100 * n))
    w = temp_sorted[lo:hi]
    return round(float(w.mean()), 3), round(float(w.std()), 3)

def hit(T):
    if T is None:
        return None
    if T1w[0] <= T <= T1w[1]:
        return 'T1'
    if T2w[0] <= T <= T2w[1]:
        return 'T2'
    return 'hors'

spearman = None
if temp is not None:
    mask = ~np.isnan(ctrl) & ~np.isnan(temp)
    if mask.sum() > 10:
        spearman = round(float(stats.spearmanr(ctrl[mask], temp[mask]).statistic), 3)

rows = []
for col in df.columns:
    if col == control or not pd.api.types.is_numeric_dtype(df[col]):
        continue
    th, curve = pv3.scan_critical_threshold(
        {col: z(df[col].values)}, progress, mode_cfg,
        n_candidates=NC, w_size=W, min_grp=3)
    sc = pd.DataFrame(curve).dropna(subset=['score'])
    m, s = map_T(float(th))
    rows.append({'flux': col, 'seuil_propre_pct': round(float(th), 2),
                 'score_max': round(float(sc['score'].max()), 3),
                 'T_estime': m, 'T_std': s, 'hit_T': hit(m),
                 'dans_fenetre1_pct': bool(win1[0] <= th <= win1[1]),
                 'dans_fenetre2_pct': bool(win2[0] <= th <= win2[1])})
pf = pd.DataFrame(rows)
pf.to_csv(outdir / 'per_flux_thresholds.csv', index=False)

c = pd.DataFrame(json.load(open(outdir / 'pipeline_results.json'))['scan_curve']).dropna(subset=['score'])
def zone(a, b):
    v = c[(c.candidate >= a) & (c.candidate <= b)]['score']
    return round(float(v.mean()), 3) if len(v) else None

mc = summ.get('mc_threshold_pct')
mcT, mcTs = map_T(mc) if mc else (None, None)
verdict = {
    'dataset': flux_path.name, 'control': control,
    'spearman_control_T': spearman,
    'global_mc_pct': mc, 'global_mc_T': [mcT, mcTs], 'global_hit_T': hit(mcT),
    'global_in_fenetre1_pct': bool(mc and win1[0] <= mc <= win1[1]),
    'global_in_fenetre2_pct': bool(mc and win2[0] <= mc <= win2[1]),
    'stabilite': (summ.get('stability') or {}).get('rating'),
    'stabilite_std': (summ.get('stability') or {}).get('std'),
    'mc_score': summ.get('mc_score'),
    'flux_hit_T1': pf.loc[pf.hit_T == 'T1', 'flux'].tolist() if len(pf) else [],
    'flux_hit_T2': pf.loc[pf.hit_T == 'T2', 'flux'].tolist() if len(pf) else [],
    'paysage_zones': {'win1_pct': zone(*win1), 'win2_pct': zone(*win2),
                      'apres_win2': zone(win2[1] + 2, win2[1] + 14),
                      'loin_88_97': zone(88, 97),
                      'max_global': round(float(c['score'].max()), 3)},
    'per_flux': rows,
}
with open(outdir / 'verdict.json', 'w', encoding='utf-8') as f:
    json.dump(verdict, f, ensure_ascii=False, indent=2)
print(json.dumps(verdict, ensure_ascii=False, indent=2))
