# -*- coding: utf-8 -*-
"""Test 2 — Nul propre : construit les 3 CSV nuls.
Protocole gelé (PROTOCOLE_TESTS.md) : encodage d'origine, colonne de
contrôle permutée indépendamment des flux avec
np.random.default_rng(1234).permutation, flux intacts, fréquences
marginales du contrôle conservées. Un CSV par contrôle (seule la
colonne de contrôle est permutée dans chacun).
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path('/home/hatch/workspace/mushroom-tests/nul')
SRC = Path('/home/hatch/workspace/mushroom-v34/data/mushrooms_pipeline.csv')

df = pd.read_csv(SRC)
controls = ['class', 'odor', 'cap-surface']
meta = {'source': str(SRC),
        'source_sha256': hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'seed': 1234, 'method': 'np.random.default_rng(1234).permutation',
        'n_rows': len(df), 'files': {}}

for control in controls:
    rng = np.random.default_rng(1234)
    perm = rng.permutation(len(df))
    out = df.copy()
    out[control] = df[control].values[perm]
    path = BASE / 'data' / f'mushrooms_null_{control}.csv'
    out.to_csv(path, index=False)
    meta['files'][control] = {
        'path': str(path.relative_to(BASE)),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'permutation_sha256': hashlib.sha256(perm.tobytes()).hexdigest(),
        'permutation_first10': [int(x) for x in perm[:10]],
    }
    # Vérifications : flux intacts, marginales conservées, permutation non triviale
    assert all(out[c].equals(df[c]) for c in df.columns if c != control), control
    assert out[control].value_counts(dropna=False).sort_index().equals(
        df[control].value_counts(dropna=False).sort_index()), control
    assert not np.array_equal(perm, np.arange(len(df))), control
    print(f"{control}: OK sha={meta['files'][control]['sha256'][:12]}... "
          f"perm_sha={meta['files'][control]['permutation_sha256'][:12]}...")

with open(BASE / 'data' / 'null_meta.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
np.save(BASE / 'data' / 'permutation_indices.npy',
        np.random.default_rng(1234).permutation(len(df)))
print('null_meta.json + permutation_indices.npy écrits')
