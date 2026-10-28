# -*- coding: utf-8 -*-
"""Extension dérivés : 8 colonnes dérivées + 4 nulls, SANS température.
Lit UNIQUEMENT data/ising_derived.csv (lot 1). Protocole gelé :
PROTOCOLE_DERIVED_EXT.md. Portes E1-E7 exécutées ici, échec = exit 1.
"""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path('/home/hatch/workspace/ising-derived')
SRC = BASE / 'data' / 'ising_derived.csv'
OUT = BASE / 'data' / 'ising_derived_ext.csv'
BLOCK = 40

df = pd.read_csv(SRC)
n = len(df)
assert n == 960, n
orig_cols = list(df.columns)
assert len(orig_cols) == 17, orig_cols

blocks = np.arange(n) // BLOCK


def exp_stat(s, kind):
    out = np.empty(n)
    for b in range(n // BLOCK):
        seg = s[b * BLOCK:(b + 1) * BLOCK].astype(float)
        if kind == 'mean':
            out[b * BLOCK:(b + 1) * BLOCK] = pd.Series(seg).expanding().mean().values
        else:
            v = pd.Series(seg).expanding().var(ddof=1).values
            v[0] = 0.0
            out[b * BLOCK:(b + 1) * BLOCK] = v
    return out


def roll_stat(s, kind):
    ser = pd.Series(s.astype(float))
    if kind == 'mean':
        return ser.rolling(BLOCK, min_periods=1).mean().values
    v = ser.rolling(BLOCK, min_periods=1).var(ddof=1).values
    v[0] = 0.0
    return v


new = {}
new['expmean_fliprate'] = exp_stat(df['fliprate'].values, 'mean')
new['expmean_localvar'] = exp_stat(df['localvar'].values, 'mean')
new['rollvar_fliprate_40'] = roll_stat(df['fliprate'].values, 'var')
new['rollvar_localvar_40'] = roll_stat(df['localvar'].values, 'var')
for base in ['energy', 'magnetization', 'fliprate', 'localvar']:
    new[f'rollmean_{base}_40'] = roll_stat(df[base].values, 'mean')

rng = np.random.default_rng(1234)
perm = rng.permutation(n)
new['null_expmean_fliprate'] = new['expmean_fliprate'][perm]
new['null_rollvar_fliprate'] = new['rollvar_fliprate_40'][perm]
new['null_rollmean_mag'] = new['rollmean_magnetization_40'][perm]
new['null_rollmean_localvar'] = new['rollmean_localvar_40'][perm]

for k, v in new.items():
    df[k] = v

# Écriture en préservant les 17 colonnes d'origine OCTET POUR OCTET :
# on repart des lignes texte du fichier source et on ajoute les nouvelles
# colonnes (repr = round-trip exact), sans jamais reformater l'original.
src_lines = SRC.read_text(encoding='utf-8').splitlines()
assert len(src_lines) == 961, len(src_lines)
new_keys = list(new.keys())
header = src_lines[0] + ',' + ','.join(new_keys)
out_lines = [header]
for i, line in enumerate(src_lines[1:]):
    out_lines.append(line + ',' + ','.join(repr(float(new[k][i])) for k in new_keys))
OUT.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
print('écrit :', OUT, df.shape)

# ---------- Portes E1-E7 ----------
chk = pd.read_csv(OUT)
ok = True


def gate(name, cond, detail=''):
    global ok
    print(('PASS' if cond else 'FAIL'), name, detail)
    ok = ok and bool(cond)


gate('E1 dimensions+NaN', chk.shape == (960, 29) and int(chk.isna().sum().sum()) == 0,
     str(chk.shape))
gate('E2 17 colonnes lot1 intactes (texte octet-pour-octet)',
     all(l1.split(',')[:17] == l2.split(',')[:17]
         for l1, l2 in zip(SRC.read_text(encoding='utf-8').splitlines(),
                           OUT.read_text(encoding='utf-8').splitlines())))
gate('E3 roll sans reset (idx40 fenetre [1..40])',
     np.isclose(chk['rollvar_fliprate_40'].values[40],
                pd.Series(df['fliprate'].values[1:41]).var(ddof=1))
     and np.isclose(chk['rollmean_energy_40'].values[40],
                    df['energy'].values[1:41].mean()))
gate('E4 expmean reset par bloc',
     np.isclose(chk['expmean_fliprate'].values[40], df['fliprate'].values[40])
     and np.isclose(chk['expmean_localvar'].values[80], df['localvar'].values[80]))
gate('E5 nuls = permutations exactes',
     all(np.array_equal(np.sort(chk[nc].values), np.sort(chk[sc].values))
         for nc, sc in [('null_expmean_fliprate', 'expmean_fliprate'),
                        ('null_rollvar_fliprate', 'rollvar_fliprate_40'),
                        ('null_rollmean_mag', 'rollmean_magnetization_40'),
                        ('null_rollmean_localvar', 'rollmean_localvar_40')]))
gate('E6 pas de colonne temperature', 'temperature' not in chk.columns)
gate('E7 exclusions (flip=1024*fliprate)',
     np.array_equal(pd.read_csv(SRC)['flip'].values,
                    pd.read_csv(SRC)['fliprate'].values * 1024))

sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
print('SHA-256 ising_derived_ext.csv :', sha)
print('SHA-256 gen_derived_ext.py :', hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
raise SystemExit(0 if ok else 1)
