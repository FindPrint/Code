# -*- coding: utf-8 -*-
"""CSV une-ligne-par-estimateur : synthèse des loupes A, B, C, D pour v5.9.0f / v5.4.0.
Colonnes : estimateur, classe native, consensus (paire ou -), médiane |d| Ising/synth
(v59), médiane |d| nul, NaN médian, cross_z médian, T_log médian, ft1_ratio médian,
sélection C (nb de cas, pas médian, gain médian) par banc, AUC médiane C par pas.
Lecture seule sur les JSON de résultats. Si resultats_C.json est absent, les
colonnes C restent vides.
"""
import json
from pathlib import Path

import numpy as np

HOME = Path.home()
OUT = HOME / "workspace" / "ising-v59" / "harness_estimateurs"
ESTIMATORS = ["Higuchi", "DFA", "Katz", "Hurst", "SampleEn", "Petrosian",
              "Sevcik", "BoxCounting", "PermutationEntropy", "CorrelationD2",
              "GrassbergerProcaccia", "InformationD1", "VisibilityGraph",
              "TwoNN", "DANCo", "Fisher", "LevinaBickel", "PCAIntrinsic",
              "LocalPCA", "GraphDimension", "PersistentHomology", "MFA",
              "KolmogorovLZ", "SpectralBeta", "SpectralDimension", "Hurst2mH",
              "Lyapunov", "MultifractalDeltaAlpha", "SingularityFmax"]
PAIRS = {"Hurst": "Hurst2mH", "Hurst2mH": "Hurst",
         "CorrelationD2": "GrassbergerProcaccia",
         "GrassbergerProcaccia": "CorrelationD2",
         "SpectralBeta": "SpectralDimension", "SpectralDimension": "SpectralBeta"}
DEGENERATE = {"Lyapunov", "MFA", "KolmogorovLZ", "SingularityFmax"}


def med(v):
    v = [x for x in v if x is not None and isinstance(x, (int, float)) and np.isfinite(x)]
    return float(np.median(v)) if v else None


def main():
    res = json.load(open(OUT / "resultats_ABDE.json"))
    comp = json.load(open(OUT / "resultats_complement.json"))
    try:
        resC = json.load(open(OUT / "resultats_C.json"))
    except FileNotFoundError:
        resC = None
    D59 = res["v59_D"]
    b_ising = {r["estimateur"]: r for r in comp["v59_B_ising_ranking"]}
    b_synth = {r["estimateur"]: r for r in comp["v59_B_synth_ranking"]}
    deg = comp["degeneracy_synth"], comp["degeneracy_ising"]
    rows = []
    for e in ESTIMATORS:
        recs = [D59[k]["estimators"][e] for k in D59]
        cls = recs[0]["class"]
        tl = []
        for r in recs:
            x = r.get("T_log")
            if isinstance(x, dict):
                x = x.get("T_log")
            if isinstance(x, (int, float)) and np.isfinite(x):
                tl.append(x)
        row = {
            "estimateur": e,
            "degénéré": "oui" if e in DEGENERATE else "non",
            "classe_native": cls,
            "paire_consensus": PAIRS.get(e, "-"),
            "d_Ising_v59": round(b_ising[e]["median_abs_d_distinct"], 3),
            "d_synth_v59": round(b_synth[e]["median_abs_d_distinct"], 3),
            "d_nul_Ising_v59": round(b_ising[e]["median_abs_d_null"], 3),
            "NaN_médian_Ising": b_ising[e]["median_nan"],
            "NaN_médian_synth": b_synth[e]["median_nan"],
            "n_uniques_médian_synth": deg[0][e]["median_n_uniq"],
            "n_uniques_médian_Ising": deg[1][e]["median_n_uniq"],
            "cross_z_médian": round(med([r.get("cross_z") for r in recs]), 3)
            if med([r.get("cross_z") for r in recs]) is not None else None,
            "T_log_médian": round(float(np.median(tl)), 3) if tl else None,
            "ft1_ratio_médian": round(med([r.get("ft_step1_ratio") for r in recs]), 3),
        }
        if resC is not None:
            for ver in ("v59", "v54"):
                for tag in ("ising", "synth"):
                    pe = resC[f"{ver}_C_{tag}"]["per_estimator"][e]
                    row[f"C_{ver}_{tag}_n_sélections"] = pe["selection_count"]
                    row[f"C_{ver}_{tag}_pas_médian"] = pe["median_selection_step"]
                    row[f"C_{ver}_{tag}_gain_médian"] = (
                        round(pe["median_gain_at_selection"], 3)
                        if pe["median_gain_at_selection"] is not None else None)
            for ver in ("v59", "v54"):
                for tag in ("ising", "synth", "global"):
                    curve = resC[f"{ver}_C_{tag}"]["auc_curve_median"]
                    for i, a in enumerate(curve):
                        row[f"AUC_{ver}_{tag}_pas{i}"] = round(a, 3)
        rows.append(row)
    import csv
    out_path = HOME / "workspace" / "ising-v59" / "resultats_estimateurs.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"écrit {out_path} ({len(rows)} lignes, C={'oui' if resC else 'non'})")


if __name__ == "__main__":
    main()
