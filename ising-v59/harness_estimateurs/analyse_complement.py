# -*- coding: utf-8 -*-
"""Analyses complémentaires sur resultats_ABDE.json (+ resultats_C.json si présent).
- Consensus A restreint aux estimateurs non dégénérés (médiane de valeurs
  uniques >= 20 ; exclus : Lyapunov, MFA, KolmogorovLZ, SingularityFmax).
- Tableaux B par estimateur et par banc.
- Comparaison D v59 vs v54 valeur par valeur sur les 45 sorties appariées.
- Distribution des verdicts L7b (v59) et t0_std walk-forward.
- Recoupement : matrice de redondance propre au pipeline (estimator_redundancy.json)
  vs médiane de mes matrices par cas pour A_single_fast_off.
- Dégénérescence par banc (valeurs uniques / finies par estimateur).
Lecture seule.
"""
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

HOME = Path.home()
OUT = HOME / "workspace" / "ising-v59" / "harness_estimateurs"
ESTIMATORS = ["Higuchi", "DFA", "Katz", "Hurst", "SampleEn", "Petrosian",
              "Sevcik", "BoxCounting", "PermutationEntropy", "CorrelationD2",
              "GrassbergerProcaccia", "InformationD1", "VisibilityGraph",
              "TwoNN", "DANCo", "Fisher", "LevinaBickel", "PCAIntrinsic",
              "LocalPCA", "GraphDimension", "PersistentHomology", "MFA",
              "KolmogorovLZ", "SpectralBeta", "SpectralDimension", "Hurst2mH",
              "Lyapunov", "MultifractalDeltaAlpha", "SingularityFmax"]
DEGENERATE = ["Lyapunov", "MFA", "KolmogorovLZ", "SingularityFmax"]


def union_groups(pairs, n, names):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in pairs:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [[names[i] for i in sorted(g)] for g in groups.values() if len(g) > 1]


def main():
    res = json.load(open(OUT / "resultats_ABDE.json"))
    out = {}
    # ---- 1. Consensus restreint (sans dégénérés) ----
    keep = [e for e in ESTIMATORS if e not in DEGENERATE]
    kidx = [ESTIMATORS.index(e) for e in keep]
    for ver in ("v59", "v54"):
        for tag in ("synth", "ising", "global"):
            mats = res[f"{ver}_A_{tag}_mats"]
            distinct = res[f"{ver}_A_{tag}"]["distinct_keys"]
            med = np.full((len(keep), len(keep)), np.nan)
            for a, b in itertools.combinations(range(len(keep)), 2):
                vals = []
                for key in distinct:
                    M = np.array(mats[key])
                    v = abs(M[kidx[a], kidx[b]])
                    if np.isfinite(v):
                        vals.append(v)
                med[a, b] = med[b, a] = float(np.median(vals))
            pairs = [(a, b) for a, b in itertools.combinations(range(len(keep)), 2)
                     if np.isfinite(med[a, b]) and med[a, b] >= 0.90]
            groups = union_groups(pairs, len(keep), keep)
            out[f"{ver}_A_{tag}_restricted"] = {
                "excluded": DEGENERATE,
                "consensus_pairs": [[keep[a], keep[b]] for a, b in pairs],
                "consensus_groups": groups,
                "n_distinct_signals_restricted": len(keep) - sum(len(g) - 1 for g in groups)}
            print(f"{ver} A {tag} restreint: paires={out[f'{ver}_A_{tag}_restricted']['consensus_pairs']} "
                  f"signaux={out[f'{ver}_A_{tag}_restricted']['n_distinct_signals_restricted']}/25")
    # ---- 2. Tableaux B ----
    for ver in ("v59", "v54"):
        for tag in ("synth", "ising", "global"):
            pe = res[f"{ver}_B_{tag}"]["per_estimator"]
            rows = sorted(pe.items(), key=lambda kv: -kv[1]["median_abs_d_distinct"])
            out[f"{ver}_B_{tag}_ranking"] = [
                {"estimateur": e, "median_abs_d_distinct": round(v["median_abs_d_distinct"], 4),
                 "median_abs_cliff_distinct": round(v["median_abs_cliff_distinct"], 4),
                 "median_abs_d_null": round(v["median_abs_d_null"], 4),
                 "median_nan": v["median_nan"]} for e, v in rows]
            print(f"{ver} B {tag} top5:", [(e, v["median_abs_d_distinct"]) for e, v in rows[:5]],
                  " bottom3:", [(e, v["median_abs_d_distinct"]) for e, v in rows[-3:]])
    # ---- 3. Comparaison D v59 vs v54 ----
    d59, d54 = res["v59_D"], res["v54_D"]
    fields = ["class", "cross_z", "raw_median", "z", "T_log", "ft_step1_ratio",
              "ft_step1_q5", "ft_step2_delta_corr", "ft_step3_hurst_mean",
              "ft_step4_delta_slope", "ft_n_valid", "ta_d1", "ta_d2",
              "ta_delta_d1", "ta_sign_change", "csd_class", "csd_n_valid",
              "csd_trend_variance", "csd_trend_ar1", "csd_trend_absolute_skewness"]
    diffs = {}
    n_compared = 0
    for key in d59:
        if key not in d54:
            continue
        for e in ESTIMATORS:
            a, b = d59[key]["estimators"][e], d54[key]["estimators"][e]
            for f in fields:
                va, vb = a.get(f), b.get(f)
                n_compared += 1
                if va is None and vb is None:
                    continue
                if va is None or vb is None or (isinstance(va, float) and isinstance(vb, float)
                                                and not np.isclose(va, vb, rtol=0, atol=0)):
                    if not (isinstance(va, float) and isinstance(vb, float) and va == vb):
                        diffs.setdefault(f, []).append((key, e, va, vb))
                elif va != vb:
                    diffs.setdefault(f, []).append((key, e, va, vb))
    out["D_v59_vs_v54"] = {"n_compared": n_compared,
                           "n_diffs": sum(len(v) for v in diffs.values()),
                           "diffs_by_field": {f: len(v) for f, v in diffs.items()},
                           "diffs": {f: v[:10] for f, v in diffs.items()}}
    print("D comparaisons:", n_compared, "différences:", sum(len(v) for v in diffs.values()),
          {f: len(v) for f, v in diffs.items()})
    # L7b verdicts (v59)
    l7b = {}
    t0std = []
    for key, rec in d59.items():
        l7b[rec.get("l7b_verdict")] = l7b.get(rec.get("l7b_verdict"), 0) + 1
        if rec.get("awf_t0_std") is not None:
            t0std.append(rec["awf_t0_std"])
    out["L7b_v59"] = {"verdicts": l7b,
                      "awf_t0_std_median": float(np.median(t0std)) if t0std else None,
                      "awf_t0_std_min": float(np.min(t0std)) if t0std else None,
                      "awf_t0_std_max": float(np.max(t0std)) if t0std else None}
    print("L7b v59:", l7b, "t0_std médiane:", out["L7b_v59"]["awf_t0_std_median"])
    # classes par estimateur (v59, médiane des cas)
    for ver in ("v59", "v54"):
        D = res[f"{ver}_D"]
        cls = {}
        for e in ESTIMATORS:
            c = {}
            for rec in D.values():
                cl = rec["estimators"][e].get("class")
                c[cl] = c.get(cl, 0) + 1
            cls[e] = c
        out[f"{ver}_classes"] = cls
    # ---- 4. Recoupement redondance pipeline vs mes matrices ----
    red = json.load(open(HOME / "workspace" / "ising-v59" / "synth" / "A_single_fast_off"
                         / "estimator_redundancy.json"))
    pipe_med = np.array(red["spearman_median_by_flux"])
    mats = res["v59_A_synth_mats"]
    keys = [k for k in mats if k.startswith("synth/A_single_fast_off/df_feat.csv|")]
    mine = np.nanmedian(np.array([np.array(mats[k]) for k in keys]), axis=0)
    diff = np.abs(pipe_med - mine)
    m = np.isfinite(diff)
    out["recoupement_redondance"] = {
        "run": "synth/A_single_fast_off", "n_fluxes": len(keys),
        "max_abs_diff": float(np.nanmax(diff)),
        "median_abs_diff": float(np.nanmedian(diff)),
        "n_pairs_diff_gt_0.01": int((diff[m] > 0.01).sum())}
    print("recoupement redondance: max|diff|=%.4f med|diff|=%.4f paires>0.01: %d"
          % (out["recoupement_redondance"]["max_abs_diff"],
             out["recoupement_redondance"]["median_abs_diff"],
             out["recoupement_redondance"]["n_pairs_diff_gt_0.01"]))
    # ---- 5. Dégénérescence par banc ----
    import glob
    for bench, pat in (("synth", str(HOME / "workspace" / "ising-v59" / "synth" / "**" / "df_feat.csv")),
                       ("ising", str(HOME / "workspace" / "ising-v59" / "ising" / "**" / "df_feat.csv"))):
        st = {e: {"n_fin": [], "n_uniq": []} for e in ESTIMATORS}
        for p in glob.glob(pat, recursive=True):
            if "full/fliprate" in p:
                continue
            df = pd.read_csv(p)
            for c in [c for c in df.columns if c.endswith("_mean")]:
                e = c[:-5].split("_", 1)[1]
                s = df[c].values.astype(float)
                f = s[np.isfinite(s)]
                st[e]["n_fin"].append(len(f))
                st[e]["n_uniq"].append(len(np.unique(f)))
        out[f"degeneracy_{bench}"] = {
            e: {"median_n_fin": float(np.median(v["n_fin"])),
                "median_n_uniq": float(np.median(v["n_uniq"])),
                "min_n_uniq": int(np.min(v["n_uniq"]))}
            for e, v in st.items()}
    # ---- 6. Couche E ----
    for ver in ("v59", "v54"):
        E = res.get(f"{ver}_E", {})
        out[f"{ver}_E_summary"] = E
        if E.get("verified"):
            from scipy import stats as _st
            b = res[f"{ver}_B_ising"]["per_estimator"]
            xs = [b[e]["median_abs_d_distinct"] for e in ESTIMATORS]
            ys = [E["median_abs_d_tc"][e] for e in ESTIMATORS]
            rho = _st.spearmanr(xs, ys).statistic
            out[f"{ver}_E_summary"]["spearman_B_vs_Tc"] = float(rho)
            print(f"{ver} E vérifiée, Spearman(B,Tc)={rho:.3f}")
        else:
            print(f"{ver} E non vérifiée:", E.get("error"), E.get("tried", [])[:2])
    with open(OUT / "resultats_complement.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("écrit resultats_complement.json")


if __name__ == "__main__":
    main()
