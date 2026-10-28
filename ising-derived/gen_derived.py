# -*- coding: utf-8 -*-
"""Construit ising_derived.csv depuis ising_classic_v354.csv (CSV sauvé).
NE LIT JAMAIS temperature.csv (vérifié par grep : aucune occurrence).
Blocs = 40 lignes consécutives (position, pas de valeurs de T).
Formules gelées : voir PROTOCOLE_DERIVED.md.
Sorties : data/ising_derived.csv (960 x 17) + data/ising_classic_v354_temperature.csv
(copie, SHA vérifié) + portes D1-D5.
"""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path('/home/hatch/workspace/ising-derived')
SRC = Path('/home/hatch/workspace/ising-v354/data/ising_classic_v354.csv')
TEMP_SRC = Path('/home/hatch/workspace/ising-v354/data/ising_classic_v354_temperature.csv')
OUT = BASE / 'data' / 'ising_derived.csv'
(BASE / 'data').mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SRC)
assert list(df.columns) == ['fliprate', 'flip', 'energy', 'magnetization',
                            'localvar', 'susceptibility']
assert len(df) == 960
BLOCK = 40
assert len(df) % BLOCK == 0
NB = len(df) // BLOCK

out = df.copy()


def expanding_stat(s, fn):
    vals = np.empty(len(s))
    for b in range(NB):
        seg = s[b * BLOCK:(b + 1) * BLOCK].values.astype(float)
        for k in range(BLOCK):
            vals[b * BLOCK + k] = fn(seg[:k + 1])
    return vals


def var1(a):
    return 0.0 if len(a) < 2 else float(np.var(a, ddof=1))


for x in ['energy', 'magnetization', 'fliprate', 'localvar']:
    out[f'expvar_{x}'] = expanding_stat(df[x], var1)
for x in ['energy', 'magnetization']:
    out[f'expmean_{x}'] = expanding_stat(df[x], lambda a: float(np.mean(a)))
for x in ['magnetization', 'energy']:
    rv = df[x].rolling(40, min_periods=1).var(ddof=1).values.astype(float)
    rv[0] = 0.0
    out[f'rollvar_{x}_40'] = rv

rng = np.random.default_rng(1234)
for src_col, null_col in [('susceptibility', 'null_susceptibility'),
                          ('expvar_magnetization', 'null_expvar_mag'),
                          ('rollvar_magnetization_40', 'null_rollvar_mag')]:
    out[null_col] = rng.permutation(out[src_col].values)

# --- Portes D1-D5 ---
assert out.shape == (960, 17), out.shape
assert int(out.isna().sum().sum()) == 0, 'NaN présents'
for c in df.columns:  # D2 : originaux bit-identiques
    assert np.array_equal(out[c].values, df[c].values), c
for x in ['energy', 'magnetization', 'fliprate', 'localvar']:  # D3a
    col = out[f'expvar_{x}'].values
    assert all(col[b * BLOCK] == 0.0 for b in range(NB)), x
for x in ['energy', 'magnetization']:  # D3b
    col = out[f'expmean_{x}'].values
    assert all(col[b * BLOCK] == df[x].values[b * BLOCK] for b in range(NB)), x
    assert out[f'rollvar_{x}_40'].values[0] == 0.0
for src_col, null_col in [('susceptibility', 'null_susceptibility'),  # D4
                          ('expvar_magnetization', 'null_expvar_mag'),
                          ('rollvar_magnetization_40', 'null_rollvar_mag')]:
    assert np.array_equal(np.sort(out[null_col].values), np.sort(out[src_col].values)), null_col

out.to_csv(OUT, index=False)
sha_out = hashlib.sha256(OUT.read_bytes()).hexdigest()

# Copie température + vérification SHA (lecture ici = copie de fichier, pas usage)
temp_bytes = TEMP_SRC.read_bytes()
sha_temp = hashlib.sha256(temp_bytes).hexdigest()
assert sha_temp == '4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4'
(BASE / 'data' / 'ising_classic_v354_temperature.csv').write_bytes(temp_bytes)

# D5 : une seule lecture CSV (la source) ; le fichier température n'est
# jamais parsé (copie d'octets + SHA seulement, aucune valeur lue).
src_text = Path(__file__).read_text(encoding='utf-8')
code_lines = [ln for ln in src_text.splitlines()
              if 'src_text' not in ln and 'code_lines' not in ln
              and not ln.strip().startswith('#')]
assert sum('read_csv(' in ln for ln in code_lines) == 1, 'plusieurs lectures CSV'

print('OK 960x17, 0 NaN, SHA dérivé :', sha_out)
print('SHA température (copie vérifiée) :', sha_temp)
print('Colonnes :', list(out.columns))
