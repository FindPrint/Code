# -*- coding: utf-8 -*-
"""Loupe C — gain incrémental par estimateur, lots v5.9.0f (étape 1) et v5.4.0.
Méthode gelée du protocole hp-estimator-info/PROTOCOLE.md (30 oct. 2026) :
régression logistique IRLS numpy (L2=1,0), standardisation intra-pli,
CV 5 plis stratifiés graine 42, sélection gloutonne max 5 pas, métrique AUC,
20 permutations d'étiquettes par cas (graine 4321) pour les nuls.
Par (sortie, flux), comme le protocole.

ADAPTATION DÉCLARÉE : les séries sont massivement dupliquées entre sorties
(df_feat.csv bit-identiques entre runs de même mode : 45 fichiers v59 ->
24 distincts). La sélection est calculée UNE FOIS par cas distinct
(même matrice X + même seuil), puis rapportée à tous les cas qui le
partagent. Le consensus (sélections, pas médian, gains) porte sur les cas
distincts ; le nombre de cas totaux est rappelé. Sans cette déduplication,
le coût serait ~3x (321 cas x 21 sélections x ~1,1 s).
Multiprocessing Pool(2) pour limiter la contention avec le run full/fliprate
en cours (prioritaire). Lecture seule, aucun run pipeline.
"""
import hashlib
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path.home() / "workspace" / "hp-estimator-info"))
sys.path.insert(0, str(Path.home() / "workspace" / "ising-v59" / "harness_estimateurs"))
from harness_estimator_info import forward_selection  # noqa: E402
from harness_lecture_v59 import ESTIMATORS, load_cases  # noqa: E402

HOME = Path.home()
OUT = Path(__file__).resolve().parent


def distinct_cases(cases):
    seen = {}
    for c in cases:
        h = hashlib.sha256(np.ascontiguousarray(c["X"]).tobytes()).hexdigest()
        key = (h, round(c["threshold"], 9))
        seen.setdefault(key, {"rep": (c["rel"], c["flux"], c["bench"]),
                              "members": [], "X": c["X"],
                              "threshold": c["threshold"], "bench": c["bench"]})
        seen[key]["members"].append((c["rel"], c["flux"]))
    return list(seen.values())


def work(dc):
    X = dc["X"]
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
            "selected": [ESTIMATORS[i] for i in sel],
            "aucs": aucs, "gains": gains, "null_gains": null_gains}


def main():
    cases59, _ = load_cases("v5.9.0f", HOME / "workspace" / "ising-v59")
    cases54, _ = load_cases("v5.4.0", HOME / "workspace" / "ising-v54")
    jobs = []
    for ver, cases in (("v59", cases59), ("v54", cases54)):
        for dc in distinct_cases(cases):
            dc = dict(dc)
            # retrouver progress : le seuil s'applique sur l'axe Progress
            dc["y"] = None
            jobs.append((ver, dc))
    # rattacher y (progress) : on le recalcule depuis le cas représentant
    # (load_cases ne conserve pas progress dans distinct_cases ; on le relit)
    prog_map = {}
    for ver, cases in (("v59", cases59), ("v54", cases54)):
        for c in cases:
            prog_map[(ver, c["rel"], c["flux"])] = c["progress"]
    todo = []
    for ver, dc in jobs:
        rel, flux, bench = dc["rep"]
        dc["y"] = (prog_map[(ver, rel, flux)] >= dc["threshold"]).astype(int)
        dc["ver"] = ver
        todo.append(dc)
    print(f"cas distincts à traiter : {len(todo)} "
          f"(v59 {sum(1 for d in todo if d['ver']=='v59')}, "
          f"v54 {sum(1 for d in todo if d['ver']=='v54')})", flush=True)
    with Pool(2) as pool:
        results = pool.map(work, todo)
    out = {"per_distinct_case": results}
    # agrégation par estimateur et par version/banc
    for ver in ("v59", "v54"):
        for bench in ("synth", "ising", None):
            tag = bench or "global"
            sel_cases = [r for r in results if r["ver"] == ver and
                         (bench is None or r["bench"] == bench)]
            aucs_med = []
            for r in sel_cases:
                aucs_med.append(r["aucs"])
            # courbe AUC médiane par pas (pas 0 = 0,5)
            maxlen = max((len(a) for a in aucs_med), default=0)
            curve = [0.5]
            for step in range(maxlen):
                vals = [a[step] for a in aucs_med if len(a) > step]
                curve.append(float(np.median(vals)))
            null_step1 = [g[0] for r in sel_cases for g in r["null_gains"] if len(g) > 0]
            per_est = {}
            for e in ESTIMATORS:
                steps, gains_at = [], []
                for r in sel_cases:
                    if e in r["selected"]:
                        i = r["selected"].index(e)
                        steps.append(i + 1)
                        gains_at.append(r["gains"][i])
                per_est[e] = {
                    "selection_count": len(steps),
                    "n_cases": len(sel_cases),
                    "median_selection_step": float(np.median(steps)) if steps else None,
                    "median_gain_at_selection": float(np.median(gains_at)) if gains_at else None,
                }
            out[f"{ver}_C_{tag}"] = {
                "n_distinct_cases": len(sel_cases),
                "auc_curve_median": curve,
                "null_step1_gain_median": float(np.median(null_step1)),
                "null_step1_gain_p95": float(np.percentile(null_step1, 95)),
                "per_estimator": per_est}
            print(f"{ver} C {tag}: cas={len(sel_cases)} courbe AUC={ [round(x,3) for x in curve] } "
                  f"nul pas1 med={np.median(null_step1):.3f} p95={np.percentile(null_step1,95):.3f}",
                  flush=True)
    with open(OUT / "resultats_C.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("écrit resultats_C.json", flush=True)


if __name__ == "__main__":
    main()
