# -*- coding: utf-8 -*-
"""Lecture des 29 estimateurs loupe par loupe, lots v5.9.0f (étape 1) et v5.4.0.
Adaptation déclarée du protocole gelé workspace/hp-estimator-info/PROTOCOLE.md
(30 oct. 2026, loupes A/B/C + couche E) aux sorties v5.x.

ADAPTATIONS (déclarées, pas cachées) :
1. Séries : `df_feat.csv` (120 points de scan, colonnes <flux>_<est>_mean/_std,
   axe Progress 0-100) au lieu de `numerical_results.csv` (30 cohortes).
   `master_results.json` ne stocke AUCUNE série brute (seulement des résumés :
   dérivées, z, four-tests, consensus). df_feat.csv est la sortie vérifiée
   du même run, même dossier, relue seulement — jamais modifiée.
2. Cas : (sortie, flux). v59 : 143 cas (113 synth + 30 Ising) ; v54 : 178 cas
   (113 synth + 65 Ising). Consensus calculé par banc (synth / Ising) et global.
3. Loupe C : voir harness_C.py (coût) — exécutée par (sortie, flux) comme le
   protocole, avec les mêmes paramètres gelés.
4. Loupe D (ajout v5.x, déclarée) : lectures natives du pipeline par
   estimateur (classes, z, four-tests, dérivées de transition, consensus CSD)
   + comparaison v59 vs v54 valeur par valeur.
5. Couche E : reconstruction des cohortes tentée comme dans le harnais
   d'origine ; si elle ne vérifie pas exactement, abandonnée (protocole).

Garde-fous : étiquette pré/post = seuil propre du run (circularité déclarée) ;
Tc = 2,2692 descriptif post-hoc seulement ; aucun verdict « pas de signal »
sur une seule loupe ; lecture seule, aucun run pipeline, MEMORY.md non touché.
Exclut ising-v59/ising/full/fliprate (run en cours, non lu).
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HOME = Path.home()
OUT = Path(__file__).resolve().parent
TC_DESCRIPTIVE = 2.2692
ESTIMATORS = ["Higuchi", "DFA", "Katz", "Hurst", "SampleEn", "Petrosian",
              "Sevcik", "BoxCounting", "PermutationEntropy", "CorrelationD2",
              "GrassbergerProcaccia", "InformationD1", "VisibilityGraph",
              "TwoNN", "DANCo", "Fisher", "LevinaBickel", "PCAIntrinsic",
              "LocalPCA", "GraphDimension", "PersistentHomology", "MFA",
              "KolmogorovLZ", "SpectralBeta", "SpectralDimension", "Hurst2mH",
              "Lyapunov", "MultifractalDeltaAlpha", "SingularityFmax"]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ranks_with_nan(s):
    s = np.asarray(s, dtype=float)
    out = np.full(len(s), np.nan)
    m = np.isfinite(s)
    out[m] = stats.rankdata(s[m])
    return out


def pearson_pairwise(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    x, y = a[m], b[m]
    if x.std() == 0 or y.std() == 0:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def spearman_matrix(R):
    n = R.shape[1]
    M = np.full((n, n), np.nan)
    for i in range(n):
        M[i, i] = 1.0
        for j in range(i + 1, n):
            v = pearson_pairwise(R[:, i], R[:, j])
            M[i, j] = M[j, i] = v
    return M


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    s = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1))
                / (len(a) + len(b) - 2))
    if s == 0:
        return 0.0
    return float((b.mean() - a.mean()) / s)


def cliff_delta(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) == 0 or len(b) == 0:
        return np.nan
    gt = (b[:, None] > a[None, :]).sum()
    lt = (b[:, None] < a[None, :]).sum()
    return float((gt - lt) / (len(a) * len(b)))


def union_groups(pairs, n):
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
    return [sorted(g) for g in groups.values() if len(g) > 1]


def load_cases(version, base):
    """Charge tous les cas (sortie, flux) d'une version. Exclut le run en cours v59."""
    cases = []
    shas = {}
    for dfp in sorted(Path(base).rglob("df_feat.csv")):
        rel = str(dfp.relative_to(base))
        if version == "v5.9.0f" and rel.startswith("ising/full/fliprate"):
            continue
        d = Path(dfp).parent
        mr = d / "master_results.json"
        shas[rel + "/df_feat.csv"] = sha256(dfp)
        shas[rel + "/master_results.json"] = sha256(mr)
        df = pd.read_csv(dfp)
        mj = json.load(open(mr))
        thr = float(mj["run_pipeline"]["threshold_metadata"]["opt_threshold"])
        bench = "ising" if rel.startswith("ising/") else "synth"
        cols = [c for c in df.columns if c.endswith("_mean")]
        by_flux = {}
        for c in cols:
            fx, est = c[:-5].split("_", 1)
            by_flux.setdefault(fx, []).append(est)
        for fx, ests in by_flux.items():
            assert sorted(ests) == sorted(ESTIMATORS), (rel, fx, len(ests))
            X = np.column_stack([df[f"{fx}_{e}_mean"].values.astype(float)
                                 for e in ESTIMATORS])
            cases.append({
                "version": version, "rel": rel, "bench": bench, "flux": fx,
                "X": X, "progress": df["Progress"].values.astype(float),
                "threshold": thr, "master": mj, "dir": str(d),
            })
    return cases, shas


def loupe_A(cases, bench_filter=None):
    """Redondance. Retourne matrices par cas, consensus, nuls.
    Consensus primaire sur cas DISTINCTS (même X + même seuil = un seul cas) ;
    consensus sur tous les cas en sensibilité (les séries sont dupliquées entre
    sorties de même mode : df_feat.csv bit-identiques)."""
    sel = [c for c in cases if bench_filter is None or c["bench"] == bench_filter]
    mats, pair_real, pair_null = {}, [], []
    for c in sel:
        X, n_est = c["X"], len(ESTIMATORS)
        R = np.column_stack([ranks_with_nan(X[:, k]) for k in range(n_est)])
        M = spearman_matrix(R)
        mats[(c["rel"], c["flux"])] = M
        iu = np.triu_indices(n_est, k=1)
        pair_real.extend(np.abs(M[iu]).tolist())
        rng = np.random.default_rng(1234)
        for _ in range(20):
            Rp = np.column_stack([rng.permutation(R[:, k]) for k in range(n_est)])
            Mp = spearman_matrix(Rp)
            pair_null.extend(np.abs(Mp[iu]).tolist())
    pair_real = np.array([v for v in pair_real if np.isfinite(v)])
    pair_null = np.array([v for v in pair_null if np.isfinite(v)])

    def consensus(keys):
        n_est = len(ESTIMATORS)
        med_rho = np.full((n_est, n_est), np.nan)
        for i, j in itertools.combinations(range(n_est), 2):
            vals = [np.abs(mats[k][i, j]) for k in keys if np.isfinite(mats[k][i, j])]
            med_rho[i, j] = med_rho[j, i] = float(np.median(vals))
        pairs = [(i, j) for i, j in itertools.combinations(range(n_est), 2)
                 if np.isfinite(med_rho[i, j]) and med_rho[i, j] >= 0.90]
        groups = union_groups(pairs, n_est)
        return {"consensus_pairs": [[ESTIMATORS[i], ESTIMATORS[j]] for i, j in pairs],
                "consensus_groups": [[ESTIMATORS[i] for i in g] for g in groups],
                "n_distinct_signals": 29 - sum(len(g) - 1 for g in groups),
                "med_rho": med_rho}

    n_est = len(ESTIMATORS)
    per_est = {}
    for k, e in enumerate(ESTIMATORS):
        vals = [np.abs(mats[key][k, j]) for key in mats for j in range(n_est)
                if j != k and np.isfinite(mats[key][k, j])]
        per_est[e] = {"median_abs_rho": float(np.median(vals))}
    # cas distincts : même X (hash) + même seuil
    seen, distinct_keys = {}, []
    for c in sel:
        h = hashlib.sha256(np.ascontiguousarray(c["X"]).tobytes()).hexdigest()
        key = (h, round(c["threshold"], 9))
        if key not in seen:
            seen[key] = (c["rel"], c["flux"])
            distinct_keys.append((c["rel"], c["flux"]))
    cons_distinct = consensus(distinct_keys)
    cons_all = consensus(list(mats.keys()))
    for k, e in enumerate(ESTIMATORS):
        maxmed = float(np.nanmax([cons_distinct["med_rho"][k][j] for j in range(n_est)
                                  if j != k and np.isfinite(cons_distinct["med_rho"][k][j])]))
        per_est[e]["max_median_abs_rho"] = maxmed
        per_est[e]["singleton"] = bool(maxmed < 0.90)
    return {"n_cases": len(sel), "n_distinct_cases": len(distinct_keys),
            "pairs_real_median_abs_rho": float(np.median(pair_real)),
            "pairs_real_frac_ge_090": float((pair_real >= 0.90).mean()),
            "pairs_null_median_abs_rho": float(np.median(pair_null)),
            "pairs_null_frac_ge_090": float((pair_null >= 0.90).mean()),
            "consensus_distinct": {k: v for k, v in cons_distinct.items() if k != "med_rho"},
            "consensus_all": {k: v for k, v in cons_all.items() if k != "med_rho"},
            "per_estimator": per_est,
            "mats": {f"{k[0]}|{k[1]}": np.round(v, 6).tolist() for k, v in mats.items()},
            "distinct_keys": [f"{k[0]}|{k[1]}" for k in distinct_keys]}


def loupe_B(cases, bench_filter=None):
    """Contraste pré/post au seuil propre du run + nuls permutés."""
    sel = [c for c in cases if bench_filter is None or c["bench"] == bench_filter]
    B_real, B_null = {}, {}
    for c in sel:
        thr = c["threshold"]
        pre = c["progress"] < thr
        post = ~pre
        for ei, e in enumerate(ESTIMATORS):
            s = c["X"][:, ei]
            key = (c["rel"], c["flux"], e)
            B_real[key] = {"cohen_d": cohen_d(s[pre], s[post]),
                           "cliff": cliff_delta(s[pre], s[post]),
                           "n_pre": int(np.isfinite(s[pre]).sum()),
                           "n_post": int(np.isfinite(s[post]).sum()),
                           "n_nan": int(np.isnan(s).sum())}
            rng = np.random.default_rng(1234)
            null_d = []
            for _ in range(20):
                sp = rng.permutation(s)
                null_d.append(cohen_d(sp[pre], sp[post]))
            B_null[key] = [v for v in null_d if np.isfinite(v)]
    per_est = {}
    # cas distincts (même X + même seuil) pour la médiane primaire
    seen, distinct_keys = {}, []
    for c in sel:
        h = hashlib.sha256(np.ascontiguousarray(c["X"]).tobytes()).hexdigest()
        key = (h, round(c["threshold"], 9))
        if key not in seen:
            seen[key] = (c["rel"], c["flux"])
            distinct_keys.append((c["rel"], c["flux"]))
    for e in ESTIMATORS:
        ds = [abs(B_real[k]["cohen_d"]) for k in B_real if k[2] == e
              and np.isfinite(B_real[k]["cohen_d"])]
        cs = [abs(B_real[k]["cliff"]) for k in B_real if k[2] == e
              and np.isfinite(B_real[k]["cliff"])]
        nds = [abs(v) for k in B_null if k[2] == e for v in B_null[k]]
        ds_d = [abs(B_real[(r, f, e)]["cohen_d"]) for (r, f) in distinct_keys
                if np.isfinite(B_real[(r, f, e)]["cohen_d"])]
        cs_d = [abs(B_real[(r, f, e)]["cliff"]) for (r, f) in distinct_keys
                if np.isfinite(B_real[(r, f, e)]["cliff"])]
        per_est[e] = {"median_abs_d": float(np.median(ds)),
                      "median_abs_d_distinct": float(np.median(ds_d)),
                      "median_abs_cliff": float(np.median(cs)),
                      "median_abs_cliff_distinct": float(np.median(cs_d)),
                      "median_abs_d_null": float(np.median(nds)),
                      "median_nan": float(np.median(
                          [B_real[k]["n_nan"] for k in B_real if k[2] == e]))}
    return {"n_cases": len(sel), "n_distinct_cases": len(distinct_keys),
            "per_estimator": per_est,
            "per_case": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in B_real.items()}}


def loupe_D(cases):
    """Lectures natives v5.x par estimateur, par sortie. Compare v59/v54 ensuite."""
    out = {}
    for c in cases:
        mj = c["master"]
        hts = mj.get("holographic_tension_state", {})
        pe = hts.get("per_estimator", {})
        zl = hts.get("relative_layer", {}).get("z_by_estimator", {})
        tl = hts.get("geometric_layer", {}).get("T_log_by_estimator", {})
        nd = mj.get("run_pipeline", {}).get("noise_diagnostic", {})
        ft = nd.get("estimator_four_tests", {}).get("by_flux", {})
        ta = mj.get("run_pipeline", {}).get("transition_analysis", {})
        csc = nd.get("csd_estimator_consensus", {}).get("estimator_results", [])
        csc_map = {(r.get("flux_name"), r.get("estimator")): r for r in csc
                   if isinstance(r, dict)}
        pl = mj.get("prediction_levels", {})
        l7b = pl.get("L7b_robustesse", {}) if isinstance(pl, dict) else {}
        awf = mj.get("adaptive_walk_forward", {})
        rec = {"rel": c["rel"], "flux": c["flux"],
               "l7b_verdict": l7b.get("verdict"),
               "awf_t0_std": awf.get("t0_std"),
               "awf_t0_reestimated": awf.get("t0_reestimated"),
               "estimators": {}}
        for e in ESTIMATORS:
            d = {"class": pe.get(e, {}).get("estimator_class"),
                 "cross_z": pe.get(e, {}).get("cross_z"),
                 "raw_median": pe.get(e, {}).get("raw_median"),
                 "z": zl.get(e),
                 "T_log": tl.get(e)}
            # four-tests, trajectoire de l'estimateur lui-même
            traj = ft.get(c["flux"], {}).get(e, {}).get("trajectories", {}).get("estimator", {})
            steps = traj.get("steps", {})
            d["ft_step1_ratio"] = steps.get("step1", {}).get("candidate_to_white_ratio")
            d["ft_step1_q5"] = steps.get("step1", {}).get("candidate_q5_score")
            d["ft_step2_delta_corr"] = steps.get("step2", {}).get("delta_corr")
            d["ft_step3_hurst_mean"] = steps.get("step3", {}).get("hurst_mean")
            d["ft_step4_delta_slope"] = steps.get("step4", {}).get("delta_slope")
            d["ft_n_valid"] = traj.get("n_valid")
            # transition_analysis : dérivées par flux
            t = ta.get(e, {}).get(c["flux"], {}) if isinstance(ta.get(e), dict) else {}
            d["ta_d1"] = t.get("first_derivative")
            d["ta_d2"] = t.get("second_derivative")
            d["ta_delta_d1"] = t.get("delta_first_derivative")
            d["ta_sign_change"] = t.get("sign_change")
            # consensus CSD : tendances par fenêtre
            cr = csc_map.get((c["flux"], e), {})
            d["csd_class"] = cr.get("estimator_class")
            d["csd_n_valid"] = cr.get("n_valid")
            ws = cr.get("window_statistics", [])
            if ws:
                idx = np.arange(len(ws))
                for stat in ("variance", "ar1", "absolute_skewness"):
                    vals = np.array([w.get(stat) for w in ws], dtype=float)
                    m = np.isfinite(vals)
                    if m.sum() >= 3 and np.std(vals[m]) > 0:
                        r = stats.spearmanr(idx[m], vals[m]).statistic
                        d[f"csd_trend_{stat}"] = float(r)
                    else:
                        d[f"csd_trend_{stat}"] = None
            rec["estimators"][e] = d
        out[f"{c['rel']}|{c['flux']}"] = rec
    return out


def couche_E(cases_ising, bench_csv, temp_csv):
    """Tentative de reconstruction cohortes -> T médiane (Ising seulement).
    Vérification exacte exigée (N_cohorts et Progress retrouvés), sinon abandon.
    cases_ising : tous les cas (sortie, flux) du banc ; vérification une fois par sortie."""
    import pandas as pd
    bench = pd.read_csv(bench_csv)
    temp = pd.read_csv(temp_csv)
    T = temp["temperature"].values.astype(float)
    assert len(T) == len(bench), (len(T), len(bench))
    tried = []
    E = {"verified": False, "tried": tried}
    by_rel = {}
    for c in cases_ising:
        by_rel.setdefault(c["rel"], []).append(c)
    n_runs = 0
    for rel, rel_cases in sorted(by_rel.items()):
        c0 = rel_cases[0]
        ctrl_name = c0["master"]["metadata"]["control"]
        if ctrl_name not in bench.columns:
            return {"verified": False, "error": f"controle {ctrl_name} absent du banc"}
        w_sizes = sorted({c0["master"]["run_pipeline"]["threshold_metadata"].get("w_size"),
                          c0["master"]["metadata"]["parameters"]["modes"]
                          .get(c0["master"]["run_pipeline"]["threshold_metadata"].get("mode"), {})
                          .get("w_size")})
        w_sizes = [w for w in w_sizes if isinstance(w, int) and w > 0]
        ctrl = bench[ctrl_name].values.astype(float)
        prog = 100.0 * stats.rankdata(ctrl) / len(ctrl)
        order = np.argsort(prog, kind="stable")
        prog_sorted = prog[order]
        T_sorted = T[order]
        scan_points = np.linspace(0.0, 100.0, 120)
        ok = None
        for w in w_sizes:
            win_prog = np.array([prog_sorted[i:i + w].mean()
                                 for i in range(len(prog) - w + 1)])
            tol = 3.0
            counts = np.array([int(((np.abs(win_prog - P) <= tol)).sum())
                               for P in scan_points])
            df = pd.read_csv(Path(c0["dir"]) / "df_feat.csv")
            expected = df["N_cohorts"].values.astype(int)
            prog_ok = bool(np.allclose(df["Progress"].values, scan_points, atol=1e-9))
            match = bool(np.array_equal(counts, expected))
            tried.append({"rel": rel, "w_size": w, "tol": tol,
                          "counts_match": match, "progress_match": prog_ok})
            if match and prog_ok:
                ok = (w, win_prog)
                break
        if ok is None:
            return {"verified": False, "tried": tried,
                    "error": "aucun w_size ne reproduit N_cohorts exactement"}
        w, win_prog = ok
        med_T = []
        for P in scan_points:
            matching = np.where(np.abs(win_prog - P) <= 3.0)[0]
            snaps = sorted({idx for ww in matching for idx in range(ww, ww + w)})
            med_T.append(float(np.median(T_sorted[snaps])))
        med_T = np.array(med_T)
        pre_tc = med_T < TC_DESCRIPTIVE
        post_tc = ~pre_tc
        for c in rel_cases:
            for ei, e in enumerate(ESTIMATORS):
                s = c["X"][:, ei]
                E.setdefault("tc_contrasts", {}).setdefault(e, []).append(
                    abs(cohen_d(s[pre_tc], s[post_tc])))
        n_runs += 1
    if n_runs == len(by_rel) and by_rel:
        E["verified"] = True
        E["n_runs_verified"] = n_runs
        E["median_abs_d_tc"] = {e: float(np.median(v))
                                for e, v in E["tc_contrasts"].items()}
    return E


def main():
    cases59, shas59 = load_cases("v5.9.0f", HOME / "workspace" / "ising-v59")
    cases54, shas54 = load_cases("v5.4.0", HOME / "workspace" / "ising-v54")
    print(f"cas v59: {len(cases59)} (synth {sum(1 for c in cases59 if c['bench']=='synth')}, "
          f"ising {sum(1 for c in cases59 if c['bench']=='ising')})")
    print(f"cas v54: {len(cases54)} (synth {sum(1 for c in cases54 if c['bench']=='synth')}, "
          f"ising {sum(1 for c in cases54 if c['bench']=='ising')})")
    res = {"shas": {"v59": shas59, "v54": shas54}, "estimators": ESTIMATORS}
    for ver, cases in (("v59", cases59), ("v54", cases54)):
        for bench in ("synth", "ising", None):
            tag = bench or "global"
            A = loupe_A(cases, bench)
            B = loupe_B(cases, bench)
            res[f"{ver}_A_{tag}"] = {k: v for k, v in A.items() if k != "mats"}
            res[f"{ver}_A_{tag}_mats"] = A["mats"]
            res[f"{ver}_B_{tag}"] = B
            print(f"{ver} {tag}: A cas={A['n_cases']} distincts={A['n_distinct_cases']} "
                  f"paires consensus(distincts)={A['consensus_distinct']['consensus_pairs']} "
                  f"signaux={A['consensus_distinct']['n_distinct_signals']} "
                  f"med|rho|={A['pairs_real_median_abs_rho']:.3f} "
                  f"(nul {A['pairs_null_median_abs_rho']:.3f}) frac>=0.90={A['pairs_real_frac_ge_090']:.4f} "
                  f"(nul {A['pairs_null_frac_ge_090']:.4f})")
        D = loupe_D(cases)
        res[f"{ver}_D"] = D
        print(f"{ver} D: {len(D)} sorties-flux lues")
    # Couche E : Ising v59 (6 sorties) et v54 (13 sorties)
    for ver, cases in (("v59", cases59), ("v54", cases54)):
        ising_cases = [c for c in cases if c["bench"] == "ising"]
        E = couche_E(ising_cases, HOME / "workspace" / "ising-v354" / "data" / "ising_classic_v354.csv",
                     HOME / "workspace" / "ising-v354" / "data" / "ising_classic_v354_temperature.csv")
        res[f"{ver}_E"] = E
        print(f"{ver} E: verified={E.get('verified')} runs={E.get('n_runs_verified')} "
              f"tried={E.get('tried', [])[:2]}")
    with open(OUT / "resultats_ABDE.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print("écrit resultats_ABDE.json")


if __name__ == "__main__":
    main()
