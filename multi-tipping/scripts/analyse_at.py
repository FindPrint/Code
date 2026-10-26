# -*- coding: utf-8 -*-
"""Analyse post-run AT (le pipeline, lui, n'a jamais vu la température) :
1) seuil propre à CHAQUE flux, avec la fonction de scan du pipeline v3.3
   et la configuration Monte Carlo retenue (w=137, 660 candidats, min_grp=3) ;
2) maxima locaux de la courbe de scan (paysage) — le 2e seuil est-il visible ?
3) mapping seuil % -> T par la frontière de rang d'énergie (méthode Ising) ;
4) extraction F1/F2 post-seuil et spectre d'ancres par flux.
"""
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, '/home/hatch/workspace/user/files')
import pipeline_autonome_v3_3_fixed as pv3

BASE = Path('/home/hatch/workspace/multi-tipping')
OUT = BASE / 'results_at_v33'

df = pd.read_csv(BASE / 'at_fluxes.csv')
temp = pd.read_csv(BASE / 'at_temperature.csv')['temperature'].values
energy = df['energy'].values
n = len(df)
progress = 100.0 * stats.rankdata(energy, method='average') / n

mode_cfg = {'n_est': 4, 'w_size': 80, 'test': 'cohen_d', 'min_grp': 4,
            'min_len': 80, 'boot': True, 'full_triangulation': False,
            'random_seed': 42}

def z(s):
    s = np.asarray(s, float)
    return (s - s.mean()) / s.std() if s.std() > 1e-10 else np.zeros_like(s)

# --- 1) Seuil par flux (fonction du pipeline, config MC) ---
rows = []
curves = {}
for col in df.columns:
    th, curve = pv3.scan_critical_threshold(
        {col: z(df[col].values)}, progress, mode_cfg,
        n_candidates=660, w_size=137, min_grp=3)
    curves[col] = curve
    sc = pd.DataFrame(curve)
    top = sc.dropna(subset=['score']).nlargest(3, 'score')
    rows.append({'flux': col, 'seuil_propre_pct': round(float(th), 2),
                 'score_max': round(float(top['score'].iloc[0]), 3),
                 'top3_candidats': [round(float(x), 1) for x in top['candidate']]})
    print(f"{col:20s} seuil propre = {th:6.2f}%  score={top['score'].iloc[0]:.3f}")
pf = pd.DataFrame(rows)
pf.to_csv(OUT / 'per_flux_thresholds.csv', index=False)
pd.DataFrame(curves[df.columns[0]]).to_csv(OUT / 'scan_curve_exemple.csv', index=False)

# --- 2) Paysage : maxima locaux de la courbe de scan globale (défaut) ---
res = json.load(open(OUT / 'pipeline_results.json'))
def local_maxima(curve, label):
    c = pd.DataFrame(curve).dropna(subset=['score']).sort_values('candidate')
    x, y = c['candidate'].values, c['score'].values
    peaks = []
    for i in range(1, len(x) - 1):
        if y[i] >= y[i-1] and y[i] > y[i+1]:
            peaks.append({'courbe': label, 'candidat_pct': round(float(x[i]), 2),
                          'score': round(float(y[i]), 3),
                          'rel_au_max': round(float(y[i] / y.max()), 3)})
    return peaks, float(y.max()), float(x[np.argmax(y)])

all_peaks = []
for label, key in [('defaut_traite', None), ('mc_default_curve', 'default_scan_curve'),
                   ('brut_defaut', 'raw_default_scan_curve')]:
    curve = res['scan_curve'] if key is None else res['metadata']['threshold_optimization'][key]
    pk, mx, amx = local_maxima(curve, label)
    print(f"\n[{label}] max global {mx:.3f} à {amx:.1f}% ; maxima locaux >= 55% du max :")
    for p in pk:
        if p['rel_au_max'] >= 0.55:
            print("   ", p); all_peaks.append(p)
pd.DataFrame(all_peaks).to_csv(OUT / 'landscape_peaks.csv', index=False)

# --- 3) Mapping seuil % -> T (frontière de rang d'énergie) ---
order = np.argsort(energy, kind='stable')
temp_sorted = temp[order]
def map_T(pct, band=1.5):
    k = pct / 100.0 * n
    lo = max(0, int(k - band / 100 * n)); hi = min(n, int(k + band / 100 * n))
    win = temp_sorted[lo:hi]
    return round(float(win.mean()), 3), round(float(win.std()), 3)

targets = {'MC_traite': 54.93, 'defaut_traite': 53.66, 'MC_brut': 54.16,
           'defaut_brut': 52.20, 'stabilite_moy': 54.89}
targets.update({f"propre_{r.flux}": r.seuil_propre_pct for r in pf.itertuples()})
mrows = []
for name, pct in targets.items():
    m, s = map_T(pct)
    mrows.append({'seuil': name, 'pct': pct, 'T_estime': m, 'T_std_fenetre': s})
    print(f"{name:26s} {pct:6.2f}%  ->  T = {m:.2f} ± {s:.2f}")
pd.DataFrame(mrows).to_csv(OUT / 'threshold_T_mapping.csv', index=False)

# --- 4) F1/F2 post-seuil par estimateur x flux ---
ta = res['transition_analysis']
trows = []
for est, per in ta.items():
    for flux, v in per.items():
        if isinstance(v, dict) and v.get('status') == 'success':
            trows.append({'estimateur': est, 'flux': flux,
                          'F1': v['first_derivative'], 'F2': v['second_derivative'],
                          'signe': v['sign'], 'ordre': v['order']})
pd.DataFrame(trows).to_csv(OUT / 'transition_F1F2.csv', index=False)
print("\nF1/F2 extraits :", len(trows), "lignes")

# --- 5) Spectre d'ancres par flux (aperçu) ---
asp = res.get('anchor_spectrum') or {}
print("\nanchor_spectrum keys:", list(asp.keys()))
with open(OUT / 'anchor_spectrum.json', 'w', encoding='utf-8') as f:
    json.dump(asp, f, ensure_ascii=False, indent=1, default=str)
for fr in asp.get('fluxes', []):
    print(" flux:", fr['flux'], "| full:", len(fr.get('full', [])), "ancres")
print("\nAnalyse terminée ->", OUT)
