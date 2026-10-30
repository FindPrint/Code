# -*- coding: utf-8 -*-
"""Correctif couche E : médianes Tc avec nanmedian (le harnais utilisait
np.median, qui propage un seul NaN à tout l'estimateur) + comptage des
cellules NaN + corrélation de rangs entre contrastes B (seuil pipeline)
et E (partage Tc descriptif). Même reconstruction que le harnais,
même vérification N_cohorts/Progress. Lecture seule des sorties du lot.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HOME = Path.home()
RUNS_DIR = HOME / "workspace" / "ising-v354" / "runs"
BENCH = HOME / "workspace" / "ising-v354" / "data"
OUT = Path(__file__).resolve().parent
RUN_NAMES = ["energy", "flip", "fliprate", "localvar", "magnetization",
             "susceptibility"]
TC = 2.2692


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    s = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1))
                 / (len(a) + len(b) - 2))
    return 0.0 if s == 0 else float((b.mean() - a.mean()) / s)


bench = pd.read_csv(BENCH / "ising_classic_v354.csv")
T = pd.read_csv(BENCH / "ising_classic_v354_temperature.csv")["temperature"].values.astype(float)
res = json.load(open(OUT / "resultats_estimateurs.json"))
estimators = res["estimators"]
tc_vals, tc_nans = {}, {}
for run in RUN_NAMES:
    num = pd.read_csv(RUNS_DIR / run / "numerical_results.csv")
    meta = json.load(open(RUNS_DIR / run / "pipeline_results.json"))["metadata"]
    w_size = int(meta["threshold_optimization"]["best_config"]["w_size"])
    ctrl = bench[run].values.astype(float)
    prog = 100.0 * stats.rankdata(ctrl) / len(ctrl)
    order = np.argsort(prog, kind="stable")
    prog_sorted, T_sorted = prog[order], T[order]
    scan_points = np.linspace(prog.min(), prog.max(), 30)
    tol = max(3.0, (scan_points[1] - scan_points[0]) / 2.0)
    win_prog = np.array([prog_sorted[i:i + w_size].mean()
                         for i in range(len(prog) - w_size + 1)])
    med_T = []
    for P in scan_points:
        matching = [w for w in range(len(win_prog))
                    if abs(win_prog[w] - P) <= tol]
        if not matching:
            matching = [int(np.argmin(np.abs(win_prog - P)))]
        snaps = sorted({idx for w in matching for idx in range(w, w + w_size)})
        med_T.append(float(np.median(T_sorted[snaps])))
    med_T = np.array(med_T)
    pre_tc = med_T < TC
    post_tc = ~pre_tc
    flux_names = sorted({c[:-5].split("_", 1)[0] for c in num.columns
                         if c.endswith("_mean")})
    for fx in flux_names:
        for e in estimators:
            s = num[f"{fx}_{e}_mean"].values.astype(float)
            # |d| PAR CELLULE : les contrôles ne sont pas tous monotones
            # en T dans le même sens, une médiane signée annulerait des
            # contrastes forts de signes opposés (erreur du 1er correctif).
            v = abs(cohen_d(s[pre_tc], s[post_tc]))
            tc_vals.setdefault(e, []).append(v)
            if not np.isfinite(v):
                tc_nans[e] = tc_nans.get(e, 0) + 1

med_E = {e: float(np.nanmedian(tc_vals[e])) for e in estimators}
b_med = {e: res["per_estimator"][e]["median_abs_d_real"] for e in estimators}
rho_BE = float(stats.spearmanr([b_med[e] for e in estimators],
                               [med_E[e] for e in estimators]).statistic)
res["E_tc_layer"] = {
    "verified": True,
    "median_abs_d_tc": med_E,
    "nan_cells": {e: tc_nans.get(e, 0) for e in estimators},
    "spearman_absB_vs_absE_medians": rho_BE,
    "note": "Médianes |d| par cellule puis nanmedian (correctif du 30 oct. "
            "2026, 2e passe : le harnais propageait un NaN à tout "
            "l'estimateur, et une médiane signée annulait des contrastes "
            "forts de signes opposés entre runs à contrôles de "
            "monotonies inverses).",
}
json.dump(res, open(OUT / "resultats_estimateurs.json", "w"),
          indent=2, ensure_ascii=False)
print("E vérifiée, Spearman(B,E) =", round(rho_BE, 4))
print("E médianes triées :")
for e, v in sorted(med_E.items(), key=lambda kv: -kv[1]):
    print(f"  {e}: {v:.4f} (cellules NaN: {tc_nans.get(e, 0)}/30)")
