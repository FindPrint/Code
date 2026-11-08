# -*- coding: utf-8 -*-
"""Loupe C, variante sans les 4 estimateurs dégénérés (Lyapunov, MFA,
KolmogorovLZ, SingularityFmax) : la saturation à 1 estimateur sur le banc
synthétique survit-elle sans l'artefact Lyapunov ? Mêmes paramètres gelés
(logistique IRLS, CV 5 plis graine 42, gloutonne max 5, 20 nuls graine 4321),
Pool(2). Cas distincts synthétiques v59 (= v54, df_feat bit-identiques).
Lecture seule.
"""
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path.home() / "workspace" / "hp-estimator-info"))
sys.path.insert(0, str(Path.home() / "workspace" / "ising-v59" / "harness_estimateurs"))
from harness_estimator_info import forward_selection  # noqa: E402
from harness_lecture_v59 import ESTIMATORS, load_cases  # noqa: E402
import harness_C as HC  # noqa: E402
import json

HOME = Path.home()
OUT = HOME / "workspace" / "ising-v59" / "harness_estimateurs"
DEGENERATE = {"Lyapunov", "MFA", "KolmogorovLZ", "SingularityFmax"}
KEEP = [e for e in ESTIMATORS if e not in DEGENERATE]
KIDX = [ESTIMATORS.index(e) for e in KEEP]


def work_restricted(dc):
    X = dc["X"][:, KIDX]
    y = dc["y"]
    sel, aucs, gains = forward_selection(X, y)
    rng = np.random.default_rng(4321)
    null_gains = []
    for _ in range(20):
        yp = rng.permutation(y)
        _, _, g = forward_selection(X, yp)
        null_gains.append(g)
    return {"rep": dc["rep"], "bench": dc["bench"], "ver": dc["ver"],
            "members": dc["members"],
            "selected": [KEEP[i] for i in sel],
            "aucs": aucs, "gains": gains, "null_gains": null_gains}


def main():
    cases59, _ = load_cases("v5.9.0f", HOME / "workspace" / "ising-v59")
    prog_map = {(c["rel"], c["flux"]): c["progress"] for c in cases59}
    todo = []
    for dc in HC.distinct_cases(cases59):
        if dc["bench"] != "synth":
            continue
        dc = dict(dc)
        rel, flux, bench = dc["rep"]
        dc["y"] = (prog_map[(rel, flux)] >= dc["threshold"]).astype(int)
        dc["ver"] = "v59"
        todo.append(dc)
    print(f"cas distincts synth à traiter (sans dégénérés) : {len(todo)}", flush=True)
    with Pool(2) as pool:
        results = pool.map(work_restricted, todo)
    curve = [0.5]
    for step in range(5):
        vals = [r["aucs"][step] for r in results if len(r["aucs"]) > step]
        curve.append(float(np.median(vals)))
    null_step1 = [g[0] for r in results for g in r["null_gains"] if len(g) > 0]
    from collections import Counter
    pas1 = Counter(r["selected"][0] for r in results if r["selected"])
    a1 = [r["aucs"][0] for r in results]
    out = {"n_distinct_cases": len(results),
           "auc_curve_median": curve,
           "null_step1_gain_median": float(np.median(null_step1)),
           "null_step1_gain_p95": float(np.percentile(null_step1, 95)),
           "pas1": dict(pas1.most_common()),
           "auc_pas1_median": float(np.median(a1)),
           "auc_pas1_min": float(min(a1)),
           "auc_pas1_n_eq_1": int(sum(1 for a in a1 if a == 1.0)),
           "per_distinct_case": results}
    with open(OUT / "resultats_C_sans_degeneres.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"synth sans dégénérés: cas={len(results)} AUC={[round(x,3) for x in curve]} "
          f"nul pas1 med={np.median(null_step1):.3f} p95={np.percentile(null_step1,95):.3f}", flush=True)
    print(f"pas1: {dict(pas1.most_common())}", flush=True)
    print(f"AUC pas1: médiane={np.median(a1):.3f} min={min(a1):.3f} n==1.0: {sum(1 for a in a1 if a==1.0)}/{len(a1)}", flush=True)
    print("écrit resultats_C_sans_degeneres.json", flush=True)


if __name__ == "__main__":
    main()
