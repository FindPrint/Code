# -*- coding: utf-8 -*-
"""
Générateur — modèle d'horloge q=6 (clock model) sur réseau carré 2D.
Cousin direct d'Ising (q=2), MAIS un seul balayage en température traverse
DEUX transitions BKT distinctes :
  - T1 ≈ 0.70 : ferro -> phase critique (quasi-ordre, vortex liés)
  - T2 ≈ 0.88 : phase critique -> paramagnétique (vortex libres)
  (CTMRG : T1=0.70, T2=0.88 ; littérature MC : fourchettes 0.68-0.75 / 0.88-0.92)

Sortie au même format que les bancs Ising de Zackary :
  - clock6_fluxes.csv      : les flux seuls (le contrôle = energy, monotone en T)
  - clock6_temperature.csv : T gardée À L'EXTÉRIEUR, repère de vérification seulement
  - clock6_dataset.csv     : combiné (temperature + flux + snapshot_id)

Flux par snapshot :
  magnetization  : module de l'aimantation vectorielle moyenne |( <cosθ>, <sinθ> )|
  energy         : énergie par site  -<cos(θi-θj)> sur les liens
  flip_rate      : fraction de propositions acceptées sur l'intervalle de mesure
  vortex_density : fraction de plaquettes portant un vortex (|winding| = 1)
  local_variance : variance inter-blocs (4x4) du module d'aimantation locale

Monte Carlo Metropolis damier (red-black), vectorisé numpy, graine fixe.
Balayage montant en T, configuration héritée d'un T au suivant (comme Ising).
"""
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
L = 24                      # réseau L x L
Q = 6                       # états d'horloge
T_MIN, T_MAX, N_T = 0.40, 1.20, 41      # grille T, pas de 0.02
N_EQ = 150                  # sweeps d'équilibration par T
N_SNAP = 24                 # snapshots par T  -> 41*24 = 984 lignes (≈ 960 Ising)
SNAP_EVERY = 10             # sweeps entre snapshots
OUT = Path(__file__).resolve().parent

rng = np.random.default_rng(SEED)
ANG = 2 * np.pi * np.arange(Q) / Q
COS, SIN = np.cos(ANG), np.sin(ANG)

# masque damier
ii, jj = np.indices((L, L))
BLACK = ((ii + jj) % 2 == 0)


def neighbours_sum_cos_sin(spins, parity):
    """Somme vectorielle des 4 voisins, décalages périodiques."""
    c, s = COS[spins], SIN[spins]
    nc = (np.roll(c, 1, 0) + np.roll(c, -1, 0) + np.roll(c, 1, 1) + np.roll(c, -1, 1))
    ns = (np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1))
    return nc, ns


def half_sweep(spins, T, parity_mask):
    nc, ns = neighbours_sum_cos_sin(spins, parity_mask)
    old = spins.copy()
    step = rng.choice([-1, 1], size=spins.shape)
    prop = (spins + step) % Q
    # ΔE = -[cos(θ'-θvois) - cos(θ-θvois)] sommée via produits scalaires
    dE = -((COS[prop] * nc + SIN[prop] * ns) - (COS[old] * nc + SIN[old] * ns))
    accept = (dE <= 0) | (rng.random(spins.shape) < np.exp(-np.maximum(dE, 0) / T))
    accept &= parity_mask
    spins[accept] = prop[accept]
    return accept.sum(), parity_mask.sum()


def sweep(spins, T):
    a1, n1 = half_sweep(spins, T, BLACK)
    a2, n2 = half_sweep(spins, T, ~BLACK)
    return (a1 + a2) / (n1 + n2)


def measure(spins, flip_rate):
    c, s = COS[spins], SIN[spins]
    mx, my = c.mean(), s.mean()
    magnetization = float(np.hypot(mx, my))
    # énergie par site : liens droite + bas, chaque lien compté une fois
    e = -(COS[spins] * np.roll(c, -1, 1) + SIN[spins] * np.roll(s, -1, 1)
          + COS[spins] * np.roll(c, -1, 0) + SIN[spins] * np.roll(s, -1, 0))
    energy = float(e.mean())  # 2 liens par site, chacun ≈ -1 à basse T -> E/site ≈ -2
    # vortex : somme des différences d'angle ramenées dans ]-pi, pi] sur chaque plaquette
    th = ANG[spins]
    def wrap(d):
        return (d + np.pi) % (2 * np.pi) - np.pi
    d1 = wrap(np.roll(th, -1, 1) - th)                    # bas-gauche -> bas-droite
    d2 = wrap(np.roll(np.roll(th, -1, 0), -1, 1) - np.roll(th, -1, 1))
    d3 = wrap(np.roll(th, -1, 0) - np.roll(np.roll(th, -1, 0), -1, 1))
    d4 = wrap(th - np.roll(th, -1, 0))
    winding = np.rint((d1 + d2 + d3 + d4) / (2 * np.pi))
    vortex_density = float(np.mean(winding != 0))
    # variance locale : blocs 4x4, module de l'aimantation de bloc
    b = L // 4
    cb = c.reshape(4, b, 4, b).mean(axis=(1, 3))
    sb = s.reshape(4, b, 4, b).mean(axis=(1, 3))
    local_variance = float(np.var(np.hypot(cb, sb)))
    return dict(magnetization=magnetization, energy=energy, flip_rate=float(flip_rate),
                vortex_density=vortex_density, local_variance=local_variance)


def main():
    spins = np.zeros((L, L), dtype=np.int64)   # départ ordonné à basse T
    rows, temps = [], []
    grid = np.linspace(T_MIN, T_MAX, N_T)
    for T in grid:
        for _ in range(N_EQ):
            sweep(spins, T)
        for _ in range(N_SNAP):
            fr = 0.0
            for _ in range(SNAP_EVERY):
                fr += sweep(spins, T)
            rows.append(measure(spins, fr / SNAP_EVERY))
            temps.append(round(float(T), 4))
        print(f"T={T:.2f} done", flush=True)
    flux = pd.DataFrame(rows, columns=["magnetization", "energy", "flip_rate",
                                       "vortex_density", "local_variance"])
    temp = pd.DataFrame({"temperature": temps})
    flux.to_csv(OUT / "clock6_fluxes.csv", index=False)
    temp.to_csv(OUT / "clock6_temperature.csv", index=False)
    full = temp.join(flux)
    full["snapshot_id"] = np.arange(len(full))
    full.to_csv(OUT / "clock6_dataset.csv", index=False)
    print(f"{len(flux)} lignes écrites dans {OUT}")


if __name__ == "__main__":
    main()
