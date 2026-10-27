# -*- coding: utf-8 -*-
"""Test 3 — Corrélations entre flux dominants (aucun run pipeline).
Protocole gelé (PROTOCOLE_TESTS.md) : Spearman sur valeurs encodées
(origine) + V de Cramér sur codes bruts (lettres), matrice complète
23 × 23, top 15 paires, focus pré-enregistré sur le trio
stalk-color-above-ring / stalk-color-below-ring / ring-type, plus
taux d'accord exact entre les deux colonnes stalk-color.
Interprétation gelée : une forte corrélation retire l'indépendance
des témoignages, ne prouve pas la circularité.
Exécution APRÈS le test 2 (ne pas lancer en parallèle des runs).
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

BASE = Path('/home/hatch/workspace/mushroom-tests/correlations')
SRC_ENC = Path('/home/hatch/workspace/mushroom-v34/data/mushrooms_pipeline.csv')
SRC_RAW = Path('/home/hatch/workspace/mushroom-v34/data/raw/mushrooms.csv')
OUT = BASE / 'results'
OUT.mkdir(parents=True, exist_ok=True)

df_enc = pd.read_csv(SRC_ENC)
df_raw = pd.read_csv(SRC_RAW)
assert list(df_enc.columns) == list(df_raw.columns)
cols = list(df_enc.columns)
assert len(cols) == 23, cols

# --- Spearman (encodage origine, paires complètes) ---
spear = df_enc[cols].corr(method='spearman', min_periods=1)

# --- V de Cramér (codes bruts, paires complètes) ---
def cramer_v(a, b):
    ct = pd.crosstab(a, b)
    chi2 = stats.chi2_contingency(ct, correction=False)[0]
    n = ct.values.sum()
    r, k = ct.shape
    denom = n * max(min(r - 1, k - 1), 1)
    return float(np.sqrt(chi2 / denom)) if denom > 0 else 0.0

cramer = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols)
for i, c1 in enumerate(cols):
    for c2 in cols[i + 1:]:
        pair = df_raw[[c1, c2]].dropna()
        v = cramer_v(pair[c1], pair[c2])
        cramer.loc[c1, c2] = v
        cramer.loc[c2, c1] = v

spear.to_csv(OUT / 'spearman_matrix.csv')
cramer.to_csv(OUT / 'cramer_matrix.csv')

def top_pairs(mat, measure, n_top=15):
    rows = []
    for i, c1 in enumerate(cols):
        for c2 in cols[i + 1:]:
            rows.append({'paire': f'{c1} / {c2}', 'flux1': c1, 'flux2': c2,
                         measure: round(float(mat.loc[c1, c2]), 3)})
    return pd.DataFrame(rows).sort_values(
        measure, key=lambda s: s.abs(), ascending=False).head(n_top)

top_s = top_pairs(spear, 'spearman')
top_c = top_pairs(cramer, 'cramer_v')
top_s.to_csv(OUT / 'top15_spearman.csv', index=False)
top_c.to_csv(OUT / 'top15_cramer.csv', index=False)

# --- Focus pré-enregistré : trio + accord exact stalk-color ---
trio = ['stalk-color-above-ring', 'stalk-color-below-ring', 'ring-type']
focus = {
    'spearman_trio': {f'{a}/{b}': round(float(spear.loc[a, b]), 3)
                      for i, a in enumerate(trio) for b in trio[i + 1:]},
    'cramer_trio': {f'{a}/{b}': round(float(cramer.loc[a, b]), 3)
                    for i, a in enumerate(trio) for b in trio[i + 1:]},
    'accord_exact_stalk_color_pct': round(
        100.0 * float((df_raw['stalk-color-above-ring']
                       == df_raw['stalk-color-below-ring']).mean()), 2),
    'n_lignes': len(df_raw),
}
with open(OUT / 'trio_focus.json', 'w', encoding='utf-8') as f:
    json.dump(focus, f, ensure_ascii=False, indent=2)

summary = {
    'dataset_encode': {'path': str(SRC_ENC),
                       'sha256': hashlib.sha256(SRC_ENC.read_bytes()).hexdigest()},
    'dataset_brut': {'path': str(SRC_RAW),
                     'sha256': hashlib.sha256(SRC_RAW.read_bytes()).hexdigest()},
    'n_lignes': len(df_raw), 'n_colonnes': len(cols),
    'top15_spearman': top_s.to_dict('records'),
    'top15_cramer': top_c.to_dict('records'),
    'focus_trio': focus,
}
with open(OUT / 'correlations_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(json.dumps({'top_spearman': top_s.to_dict('records')[:5],
                  'top_cramer': top_c.to_dict('records')[:5],
                  'focus': focus}, ensure_ascii=False, indent=2))
print('TEST 3 TERMINE (matrices + top15 + focus ecrits)')
