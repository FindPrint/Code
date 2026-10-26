# -*- coding: utf-8 -*-
"""
Générateur — modèle d'Ashkin-Teller symétrique 2D (deux Ising couplés).
H = -Σ_<ij> [ J (s_i s_j + τ_i τ_j) + U · s_i τ_i s_j τ_j ],  J=1, U=2 (U > J :
deux transitions nettes — Baxter -> phase partielle <sτ> -> paramagnétique).

Usage: python3 gen_ashkin_teller.py [--seed 42] [--L 28] [--prefix at] [--outdir .]
Défauts = jeu de la vague 1 (graine 42, L=28, préfixe at).
Sorties : <prefix>_fluxes.csv, <prefix>_temperature.csv (T externe), <prefix>_dataset.csv
Metropolis damier, vectorisé numpy, balayage montant hérité.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

J, U = 1.0, 2.0
T_MIN, T_MAX, N_T = 2.0, 7.0, 51
N_EQ, N_SNAP, SNAP_EVERY = 200, 24, 10

L = 28
rng = np.random.default_rng(42)
ii, jj = np.indices((L, L))
BLACK = ((ii + jj) % 2 == 0)


def nsum(a):
    return (np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1))


def update_layer(x, other, T):
    acc_total, n_total = 0, 0
    for mask in (BLACK, ~BLACK):
        ox = other * x
        h = J * nsum(x) + U * other * nsum(ox)
        dE = 2.0 * x * h
        accept = (dE <= 0) | (rng.random(x.shape) < np.exp(-np.maximum(dE, 0) / T))
        accept &= mask
        x[accept] *= -1
        acc_total += int(accept.sum()); n_total += int(mask.sum())
    return acc_total / n_total


def sweep(s, tau, T):
    return 0.5 * (update_layer(s, tau, T) + update_layer(tau, s, T))


def measure(s, tau, flip_rate):
    p = s * tau
    e_bond = J * (s * np.roll(s, -1, 1) + tau * np.roll(tau, -1, 1)) \
           + J * (s * np.roll(s, -1, 0) + tau * np.roll(tau, -1, 0)) \
           + U * (p * np.roll(p, -1, 1) + p * np.roll(p, -1, 0))
    b = L // 4
    blocks = s[:b * 4, :b * 4].reshape(4, b, 4, b).mean(axis=(1, 3))
    return dict(magnetization_s=float(abs(s.mean())),
                magnetization_tau=float(abs(tau.mean())),
                magnetization_prod=float(abs(p.mean())),
                energy=float(-e_bond.mean()),
                flip_rate=float(flip_rate),
                local_variance=float(np.var(blocks)))


def main():
    global L, rng, BLACK
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--L', type=int, default=28)
    ap.add_argument('--prefix', default='at')
    ap.add_argument('--outdir', default='.')
    a = ap.parse_args()
    L = a.L
    rng = np.random.default_rng(a.seed)
    ii, jj = np.indices((L, L))
    BLACK = ((ii + jj) % 2 == 0)
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    s = np.ones((L, L), dtype=np.int64)
    tau = np.ones((L, L), dtype=np.int64)
    rows, temps = [], []
    for T in np.linspace(T_MIN, T_MAX, N_T):
        for _ in range(N_EQ):
            sweep(s, tau, T)
        for _ in range(N_SNAP):
            fr = 0.0
            for _ in range(SNAP_EVERY):
                fr += sweep(s, tau, T)
            rows.append(measure(s, tau, fr / SNAP_EVERY))
            temps.append(round(float(T), 4))
    cols = ["magnetization_s", "magnetization_tau", "magnetization_prod",
            "energy", "flip_rate", "local_variance"]
    flux = pd.DataFrame(rows, columns=cols)
    temp = pd.DataFrame({"temperature": temps})
    flux.to_csv(out / f"{a.prefix}_fluxes.csv", index=False)
    temp.to_csv(out / f"{a.prefix}_temperature.csv", index=False)
    full = temp.join(flux); full["snapshot_id"] = np.arange(len(full))
    full.to_csv(out / f"{a.prefix}_dataset.csv", index=False)
    print(f"{a.prefix}: {len(flux)} lignes (seed={a.seed}, L={L}) -> {out}")


if __name__ == "__main__":
    main()
