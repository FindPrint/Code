# -*- coding: utf-8 -*-
"""Synthèse vérifiée des 3 tests diagnostics mushroom v3.4.
Lit run_summary.json + per_flux_thresholds.csv + transition_F1F2.csv
des runs encodage (ALPHA) et nul, et les run_summary du lot d'origine.
Aucun chiffre recopié à la main. Produit les CSV de synthèse + les
figures de comparaison + les heatmaps de corrélations (test 3).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path('/home/hatch/workspace/mushroom-tests')
V34 = Path('/home/hatch/workspace/mushroom-v34')
CONTROLS = ['class', 'odor', 'cap-surface']
OUT = BASE / 'synthese'
OUT.mkdir(exist_ok=True)
FIG = BASE / 'figures'
FIG.mkdir(exist_ok=True)


def load(d):
    return json.load(open(Path(d) / 'run_summary.json'))


rows, pf_rows, ff_rows, qs_rows = [], [], [], []
for c in CONTROLS:
    orig = load(V34 / 'results' / f'ctrl_{c}')
    alpha = load(BASE / 'encodage' / 'results' / f'ctrl_{c}')
    nul = load(BASE / 'nul' / 'results' / f'ctrl_{c}')
    d_mc = round(alpha['mc_threshold_pct'] - orig['mc_threshold_pct'], 2)
    d_sc = round(alpha['mc_score'] - orig['mc_score'], 3)
    d_nul = round(nul['mc_score'] - orig['mc_score'], 3)
    rows.append({
        'controle': c,
        'orig_MC_pct': orig['mc_threshold_pct'], 'orig_score': orig['mc_score'],
        'orig_defaut_pct': orig['default_threshold_pct'],
        'orig_brut_pct': orig['raw_mc_threshold_pct'],
        'orig_rigide_pct': orig['rigid_1001_threshold_pct'],
        'orig_stabilite': orig['stability_rating'],
        'orig_stab_moy': orig['stability_mean'], 'orig_stab_std': orig['stability_std'],
        'orig_duree_s': orig['duration_s'],
        'alpha_MC_pct': alpha['mc_threshold_pct'], 'alpha_score': alpha['mc_score'],
        'alpha_defaut_pct': alpha['default_threshold_pct'],
        'alpha_brut_pct': alpha['raw_mc_threshold_pct'],
        'alpha_rigide_pct': alpha['rigid_1001_threshold_pct'],
        'alpha_stabilite': alpha['stability_rating'],
        'alpha_stab_moy': alpha['stability_mean'], 'alpha_stab_std': alpha['stability_std'],
        'alpha_duree_s': alpha['duration_s'],
        'delta_MC_alpha': d_mc, 'delta_score_alpha': d_sc,
        'verdict_encodage': 'SENSIBLE' if (abs(d_mc) > 5 or abs(d_sc) > 0.05) else 'ROBUSTE',
        'nul_MC_pct': nul['mc_threshold_pct'], 'nul_score': nul['mc_score'],
        'nul_defaut_pct': nul['default_threshold_pct'],
        'nul_brut_pct': nul['raw_mc_threshold_pct'],
        'nul_rigide_pct': nul['rigid_1001_threshold_pct'],
        'nul_stabilite': nul['stability_rating'],
        'nul_stab_moy': nul['stability_mean'], 'nul_stab_std': nul['stability_std'],
        'nul_duree_s': nul['duration_s'],
        'delta_score_nul': d_nul,
        'seuil_distinguabilite': round(orig['mc_score'] - 0.05, 3),
        'verdict_nul': ('INDISTINGUABLE' if nul['mc_score'] >= orig['mc_score'] - 0.05
                        else 'DISTINGUABLE'),
    })
    for tag, s, d in [('ALPHA', alpha, BASE / 'encodage' / 'results' / f'ctrl_{c}'),
                      ('NUL', nul, BASE / 'nul' / 'results' / f'ctrl_{c}')]:
        pf = pd.read_csv(d / 'per_flux_thresholds.csv')
        for r in pf.itertuples():
            pf_rows.append({'test': tag, 'controle': c, 'flux': r.flux,
                            'seuil_propre_pct': r.seuil_propre_pct,
                            'score_max': r.score_max})
        ff = pd.read_csv(d / 'transition_F1F2.csv')
        for r in ff.itertuples():
            ff_rows.append({'test': tag, 'controle': c, 'estimateur': r.estimateur,
                            'flux': r.flux, 'F1': r.F1, 'F2': r.F2,
                            'F1_pre': r.F1_pre, 'F2_pre': r.F2_pre,
                            'delta_F1': r.delta_F1, 'delta_F2': r.delta_F2,
                            'sign_change': r.sign_change})
        q = s.get('scores_moyens_par_Q') or {}
        qs_rows.append({'test': tag, 'controle': c,
                        'Q1': q.get('Q1_Calme_vs_Chaos'),
                        'Q2': q.get('Q2_Tension_Seuil'),
                        'Q3': q.get('Q3_Agressivite'),
                        'Q4': q.get('Q4_Persistence'),
                        'Q5': q.get('Q5_Actif_Receptif')})

comp = pd.DataFrame(rows)
comp.to_csv(OUT / 'comparaison_controles.csv', index=False)
pd.DataFrame(pf_rows).to_csv(OUT / 'tous_seuils_par_flux_tests.csv', index=False)
pd.DataFrame(ff_rows).to_csv(OUT / 'tous_F1F2_tests.csv', index=False)
pd.DataFrame(qs_rows).to_csv(OUT / 'qs_tests.csv', index=False)
print(f"comparaison: {len(comp)} lignes, verdicts encodage: {comp.verdict_encodage.tolist()}, verdicts nul: {comp.verdict_nul.tolist()}")
print(f"seuils propres: {len(pf_rows)} lignes, F1F2: {len(ff_rows)} lignes, Q: {len(qs_rows)} lignes")

# --- Figures de comparaison ---
x = np.arange(len(CONTROLS))
w = 0.27
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(x - w, comp.orig_score, w, label='Réel (origine)')
ax.bar(x, comp.alpha_score, w, label='Encodage alphabétique')
ax.bar(x + w, comp.nul_score, w, label='Nul (permutation)')
for i, r in comp.iterrows():
    for xi, v in [(x[i] - w, r.orig_score), (x[i], r.alpha_score), (x[i] + w, r.nul_score)]:
        ax.text(xi, v + 0.015, f'{v:.3f}', ha='center', fontsize=9)
ax.set_xticks(x, CONTROLS); ax.set_ylabel('Score MC'); ax.set_ylim(0, 0.8)
ax.set_title('Scores MC : réel vs encodage alphabétique vs nul')
ax.legend(); fig.tight_layout(); fig.savefig(FIG / 'fig_scores_comparaison.png', dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(x - w, comp.orig_MC_pct, w, label='Réel (origine)')
ax.bar(x, comp.alpha_MC_pct, w, label='Encodage alphabétique')
ax.bar(x + w, comp.nul_MC_pct, w, label='Nul (permutation)')
for i, r in comp.iterrows():
    for xi, v in [(x[i] - w, r.orig_MC_pct), (x[i], r.alpha_MC_pct), (x[i] + w, r.nul_MC_pct)]:
        ax.text(xi, v + 2, f'{v:.1f}', ha='center', fontsize=9)
ax.set_xticks(x, CONTROLS); ax.set_ylabel('Seuil MC (%)'); ax.set_ylim(0, 115)
ax.set_title('Seuils MC : réel vs encodage alphabétique vs nul')
ax.legend(); fig.tight_layout(); fig.savefig(FIG / 'fig_seuils_comparaison.png', dpi=150); plt.close(fig)

# --- Heatmaps test 3 ---
for name, fname in [('spearman_matrix.csv', 'heatmap_spearman.png'),
                    ('cramer_matrix.csv', 'heatmap_cramer.png')]:
    m = pd.read_csv(BASE / 'correlations' / 'results' / name, index_col=0)
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(m.values, cmap='RdBu_r' if 'spearman' in name else 'viridis',
                   vmin=-1 if 'spearman' in name else 0, vmax=1)
    ax.set_xticks(range(len(m.columns)), m.columns, rotation=90, fontsize=7)
    ax.set_yticks(range(len(m.index)), m.index, fontsize=7)
    ax.set_title(('Spearman (encodage origine)' if 'spearman' in name
                  else 'V de Cramér (codes bruts)') + ' — 23 x 23')
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout(); fig.savefig(FIG / fname, dpi=150); plt.close(fig)
    print(fname, 'écrit', m.shape)
print('Figures écrites dans', FIG)
