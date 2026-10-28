# -*- coding: utf-8 -*-
"""Générateur Ising classique 2D — lot ising-v354 (protocole gelé 28 oct. 2026).

Adapté de workspace/gen_ising_proxy.py (mêmes sweep checkerboard,
energy_per_spin, local_variance, L, températures, graine, EQ/GAP).
6 flux : fliprate, flip, energy, magnetization (|m|), localvar,
susceptibility (fenêtre expansive intra-bloc, m signée interne).
Température dans un CSV SÉPARÉ, même ordre de lignes.
Sorties : data/ising_classic_v354.csv + data/ising_classic_v354_temperature.csv
Portes P1-P4 imprimées ; sortie non nulle si une porte échoue.
"""
import csv
import hashlib
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.ndimage import uniform_filter

BASE = Path('/home/hatch/workspace/ising-v354')
OUT = BASE / 'data'
OUT.mkdir(parents=True, exist_ok=True)

L = 32
N = L * L
Ts = np.linspace(1.7, 3.3, 24)
N_SNAP = 40
SEED = 42
EQ_SWEEPS = 1500
GAP_SWEEPS = 50
TC_ONSAGER = 2.269185314213  # 2*ln(1+sqrt(2))

rng = np.random.default_rng(SEED)
_CHESS = (np.indices((L, L)).sum(axis=0) % 2)


def sweep(spins, T, flips=None):
    """Un sweep checkerboard Metropolis. Retourne nb de flips."""
    nflip = 0
    for color in (0, 1):
        mask = _CHESS == color
        nb = (np.roll(spins, 1, 0) + np.roll(spins, -1, 0) +
              np.roll(spins, 1, 1) + np.roll(spins, -1, 1))
        dE = 2 * spins * nb
        acc = (dE <= 0) | (rng.random((L, L)) < np.exp(-dE / T))
        do = mask & acc
        spins[do] *= -1
        nflip += int(do.sum())
    if flips is not None:
        flips.append(nflip)
    return nflip


def energy_per_spin(spins):
    nb = (np.roll(spins, 1, 0) + np.roll(spins, 1, 1))
    return float(-(spins * nb).sum() / N)


def local_variance(spins):
    # Variance du voisinage 3x3, moyennée sur les sites (gen_ising_proxy.py).
    f = spins.astype(float)
    m = uniform_filter(f, size=3, mode='wrap')
    m2 = uniform_filter(f ** 2, size=3, mode='wrap')
    return float((m2 - m ** 2).mean())


COLS = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar',
        'susceptibility']
rows = []
tref = []
for T in Ts:
    spins = rng.choice([-1, 1], size=(L, L))
    for _ in range(EQ_SWEEPS):
        sweep(spins, float(T))
    m_signed_hist = []
    for _ in range(N_SNAP):
        flips = []
        for _ in range(GAP_SWEEPS):
            sweep(spins, float(T), flips)
        flip = float(np.mean(flips))
        e = energy_per_spin(spins)
        m_signed = float(spins.mean())
        m_signed_hist.append(m_signed)
        lv = local_variance(spins)
        if len(m_signed_hist) >= 2:
            chi = float(N * np.var(m_signed_hist, ddof=1) / float(T))
        else:
            chi = 0.0
        rows.append([flip / N, flip, e, abs(m_signed), lv, chi])
        tref.append(float(T))

A = np.array(rows)
assert A.shape == (24 * N_SNAP, 6), A.shape

csv_path = OUT / 'ising_classic_v354.csv'
with open(csv_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for i in range(len(rows)):
        w.writerow({k: float(A[i, j]) for j, k in enumerate(COLS)})

tmp_path = OUT / 'ising_classic_v354_temperature.csv'
with open(tmp_path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['temperature'])
    for t in tref:
        w.writerow([t])

# ---------- Portes P1-P4 ----------
ok = True
blocks = A.reshape(24, N_SNAP, 6)
mag_block = blocks[:, :, 3].mean(axis=1)
drops = np.where(np.diff(mag_block) < -0.15)[0]
p1 = len(drops) > 0 and Ts[drops[0]] < TC_ONSAGER < Ts[drops[-1] + 1]
print('P1 chute |m| entre T=%.4f et T=%.4f, Tc encadré: %s'
      % (Ts[drops[0]], Ts[drops[-1] + 1], p1) if len(drops) else 'P1 ÉCHEC : aucune chute')
ok &= bool(p1)
from scipy import stats as _st
rho = _st.spearmanr(Ts, blocks[:, :, 2].mean(axis=1)).statistic
p2 = rho > 0.9
print('P2 Spearman(T, énergie par bloc) = %.4f (>0.9: %s)' % (rho, p2))
ok &= bool(p2)
chi_block = blocks[:, :, 5].mean(axis=1)
t_pic = float(Ts[int(np.argmax(chi_block))])
p3 = abs(t_pic - TC_ONSAGER) <= 0.15
print('P3 pic susceptibilité à T=%.4f, |écart Tc|=%.4f (<=0.15: %s)'
      % (t_pic, abs(t_pic - TC_ONSAGER), p3))
ok &= bool(p3)
p4 = (len(rows) == 960 and len(tref) == 960 and not np.isnan(A).any()
      and len(np.unique(A, axis=0)) == 960)
print('P4 960 lignes, 6 colonnes, 0 NaN, 0 doublon exact: %s' % p4)
ok &= bool(p4)
for p, h in ((csv_path, None), (tmp_path, None)):
    pass
print('SHA-256 données:', hashlib.sha256(csv_path.read_bytes()).hexdigest())
print('SHA-256 températures:', hashlib.sha256(tmp_path.read_bytes()).hexdigest())
print('lignes:', len(rows), '| colonnes:', len(COLS))
sys.exit(0 if ok else 1)
