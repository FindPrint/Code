# -*- coding: utf-8 -*-
"""Loupe A avec la règle de support DU PIPELINE (copie exacte de
compute_estimator_redundancy, lignes 5462-5501 du fichier v5.9.0f) :
par flux, dropna par paire, len >= 10 ET nunique >= 2 sur chaque série,
Spearman scipy, médiane inter-flux. Cas DISTINCTS seulement (même déduplication
que le harnais principal : hash de X + seuil). Lecture seule.
Compare le consensus obtenu avec celui du harnais (règle protocole : >= 3 paires).
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

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


def load_cases(version):
    base = HOME / "workspace" / ("ising-v59" if version == "v59" else "ising-v54")
    cases = []
    for dfp in sorted(base.rglob("df_feat.csv")):
        rel = str(dfp.relative_to(base))
        if "ising/full/fliprate" in rel:
            continue
        d = dfp.parent
        mr = d / "master_results.json"
        if not mr.exists():
            continue
        mj = json.load(open(mr))
        tm = mj.get("run_pipeline", {}).get("threshold_metadata", {})
        thr = tm.get("opt_threshold")
        casc = mj.get("five_threshold_cascade", {})
        T0 = casc.get("T_0_Monte_Carlo_Central")
        df = pd.read_csv(dfp)
        bench = "synth" if rel.startswith("synth/") else "ising"
        for c in [c for c in df.columns if c.endswith("_mean")]:
            flux = c[:-5].split("_", 1)[0]
            X = np.column_stack([df[f"{flux}_{e}_mean"].values.astype(float)
                                 for e in ESTIMATORS])
            h = hashlib.sha256(np.nan_to_num(X, nan=0.0).tobytes()
                               + str(thr).encode()).hexdigest()
            cases.append({"rel": rel, "flux": flux, "bench": bench, "X": X,
                          "thr": thr, "T0": T0, "hash": h})
    return cases


def spearman_pipeline_rule(X, fluxes_present):
    """X : (120, 29) pour UN flux. Règle pipeline : len>=10, nunique>=2, scipy."""
    n = len(ESTIMATORS)
    M = np.full((n, n), np.nan)
    for i in range(n):
        M[i, i] = 1.0
        for j in range(i + 1, n):
            a, b = X[:, i], X[:, j]
            m = np.isfinite(a) & np.isfinite(b)
            aa, bb = a[m], b[m]
            if len(aa) < 10 or len(np.unique(aa)) < 2 or len(np.unique(bb)) < 2:
                continue
            r = float(stats.spearmanr(aa, bb).statistic)
            if np.isfinite(r):
                M[i, j] = M[j, i] = r
    return M


def consensus_from_median(med, keep):
    kidx = [ESTIMATORS.index(e) for e in keep]
    sub = med[np.ix_(kidx, kidx)]
    pairs = [(a, b) for a, b in itertools.combinations(range(len(keep)), 2)
             if np.isfinite(sub[a, b]) and abs(sub[a, b]) >= 0.90]
    parent = list(range(len(keep)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    groups = {}
    for i in range(len(keep)):
        groups.setdefault(find(i), []).append(i)
    gl = [[keep[i] for i in sorted(g)] for g in groups.values() if len(g) > 1]
    return ([[keep[a], keep[b]] for a, b in pairs], gl,
            len(keep) - sum(len(g) - 1 for g in gl))


def main():
    out = {}
    for version in ("v59", "v54"):
        cases = load_cases(version)
        # déduplication par hash (X + seuil), comme le harnais principal
        seen, distinct = set(), []
        for c in cases:
            if c["hash"] not in seen:
                seen.add(c["hash"])
                distinct.append(c)
        print(f"{version}: {len(cases)} cas, {len(distinct)} distincts", flush=True)
        for tag, subset in (("synth", [c for c in distinct if c["bench"] == "synth"]),
                            ("ising", [c for c in distinct if c["bench"] == "ising"]),
                            ("global", distinct)):
            mats = []
            for c in subset:
                mats.append(spearman_pipeline_rule(c["X"], None))
            med = np.nanmedian(np.array(mats), axis=0)
            off = med[~np.eye(29, dtype=bool)]
            off = off[np.isfinite(off)]
            pairs, groups, n_sig = consensus_from_median(med, ESTIMATORS)
            keep = [e for e in ESTIMATORS if e not in DEGENERATE]
            pairs_r, groups_r, n_sig_r = consensus_from_median(med, keep)
            out[f"{version}_A_{tag}_pipeline_rule"] = {
                "n_distinct_cases": len(subset),
                "consensus_pairs": pairs, "consensus_groups": groups,
                "n_distinct_signals": n_sig,
                "restricted_pairs": pairs_r, "restricted_groups": groups_r,
                "n_distinct_signals_restricted": n_sig_r,
                "median_abs_rho": float(np.median(np.abs(off))),
                "frac_ge_0.90": float((np.abs(off) >= 0.90).mean())}
            print(f"{version} A {tag} (règle pipeline): paires={pairs} signaux={n_sig} | "
                  f"restreint={pairs_r} signaux={n_sig_r} | med|rho|={np.median(np.abs(off)):.3f} "
                  f"frac>=0.90={(np.abs(off) >= 0.90).mean():.4f}", flush=True)
    with open(OUT / "resultats_A_pipeline_rule.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("écrit resultats_A_pipeline_rule.json", flush=True)


if __name__ == "__main__":
    main()
