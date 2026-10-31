# -*- coding: utf-8 -*-
"""Harnais « information en plus par estimateur » sur le lot réduit
UNIVERSAL_LOG (23 runs, 2 000 lignes). Protocole gelé :
workspace/mushroom-universal-reduced/PROTOCOLE_LOUPES_LOT.md (30 oct. 2026).
Lecture seule des sorties du lot, aucun nouveau run pipeline.
Généralisation du harnais pilote mushroom (1 run × 22 flux) :
22 runs × 22 flux = 484 cas ; veil-type EXCLU comme contrôle
(seuil NaN → cohortes non étiquetables), inclus comme flux.
Mêmes paramètres gelés (Spearman ≥0,90 ; Cohen/Cliff ; logistique IRLS
L2 1,0, CV 5 plis graine 42, max 5, AUC ; nuls 20, graines 1234/4321).
"""
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

LOTDIR = Path(__file__).resolve().parent
OUT = LOTDIR


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ranks_with_nan(s):
    """Rangs moyens sur valeurs finies, NaN conservés."""
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
    """R : matrice rangs (n_cohortes x n_est), NaN possibles."""
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


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def fit_logreg(X, y, l2=1.0, iters=25):
    """X déjà standardisé, sans intercept. Retourne w avec intercept."""
    Xb = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = sigmoid(Xb @ w)
        W = p * (1 - p) + 1e-8
        g = Xb.T @ (p - y)
        g[1:] += l2 * w[1:]
        H = (Xb * W[:, None]).T @ Xb
        H[1:, 1:] += l2 * np.eye(Xb.shape[1] - 1)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, g, rcond=None)[0]
        w = w - step
        if np.max(np.abs(step)) < 1e-6:
            break
    return w


def auc_score(y_true, y_score):
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    r = stats.rankdata(np.concatenate([pos, neg]))
    rp = r[:len(pos)].sum()
    return float((rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def stratified_folds(y, n_splits, seed):
    rng = np.random.default_rng(seed)
    folds = [[] for _ in range(n_splits)]
    for cls in (0, 1):
        idx = np.where(y == cls)[0]
        rng.shuffle(idx)
        for k, ix in enumerate(idx):
            folds[k % n_splits].append(ix)
    return [np.array(f) for f in folds if len(f) > 0]


def cv_auc(X, y, seed=42):
    """AUC-CV 5 plis stratifiés, standardisation intra-pli (train)."""
    if len(np.unique(y)) < 2:
        return np.nan
    folds = stratified_folds(y, 5, seed)
    aucs = []
    for f in folds:
        test_idx = f
        train_idx = np.setdiff1d(np.arange(len(y)), test_idx)
        if len(np.unique(y[train_idx])) < 2 or len(np.unique(y[test_idx])) < 2:
            continue
        mu = X[train_idx].mean(axis=0)
        sd = X[train_idx].std(axis=0)
        sd = np.where(sd == 0, 1.0, sd)
        w = fit_logreg((X[train_idx] - mu) / sd, y[train_idx])
        Xb = np.column_stack([np.ones(len(test_idx)),
                              (X[test_idx] - mu) / sd])
        aucs.append(auc_score(y[test_idx], sigmoid(Xb @ w)))
    aucs = [a for a in aucs if np.isfinite(a)]
    return float(np.mean(aucs)) if aucs else np.nan


def forward_selection(X, y, max_steps=5, seed=42):
    """X : (n_cohortes x n_est), NaN possibles. Retourne ordre, AUCs, gains."""
    n_est = X.shape[1]
    selected = []
    aucs = [0.5]
    remaining = list(range(n_est))
    for _ in range(max_steps):
        best, best_auc = None, -np.inf
        for cand in remaining:
            cols = selected + [cand]
            sub = X[:, cols]
            mask = np.all(np.isfinite(sub), axis=1)
            if mask.sum() < 10 or len(np.unique(y[mask])) < 2:
                continue
            a = cv_auc(sub[mask], y[mask], seed=seed)
            if np.isfinite(a) and a > best_auc:
                best, best_auc = cand, a
        if best is None:
            break
        selected.append(best)
        aucs.append(best_auc)
        remaining.remove(best)
    gains = [aucs[i + 1] - aucs[i] for i in range(len(selected))]
    return selected, aucs[1:], gains


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


def main():
    # ---- Chargement, SHA, noms d'estimateurs ----
    # Runs inclus : run_summary OK + seuil fini (veil-type exclu : NaN).
    run_data = {}
    shas = {}
    excluded = []
    for rundir in sorted(LOTDIR.glob("ctrl_*")):
        run = rundir.name[len("ctrl_"):]
        summ = json.load(open(rundir / "run_summary.json"))
        num_path = rundir / "numerical_results.csv"
        res_path = rundir / "pipeline_results.json"
        shas[f"{run}/numerical_results.csv"] = sha256(num_path)
        shas[f"{run}/pipeline_results.json"] = sha256(res_path)
        thr = summ.get("opt_threshold")
        if summ.get("status") != "OK" or thr is None or not math.isfinite(float(thr)):
            excluded.append({"run": run, "status": summ.get("status"),
                             "opt_threshold": thr,
                             "reason": "seuil non fini ou statut non OK"})
            continue
        num = pd.read_csv(num_path)
        assert "Progress" in num.columns, (run, "colonne Progress absente")
        run_data[run] = {
            "num": num,
            "opt_threshold": float(thr),
            "progress": num["Progress"].values.astype(float),
        }
    print(f"Runs inclus : {len(run_data)} ; exclus : {excluded}")
    # Flux analysés par run = colonnes _mean ; les noms de flux utilisent
    # des tirets, pas '_' : découpe sur le premier '_'.
    all_estimators = None
    for run, rd in run_data.items():
        cols = [c for c in rd["num"].columns if c.endswith("_mean")]
        est_by_flux = {}
        for c in cols:
            fx, est = c[:-5].split("_", 1)
            est_by_flux.setdefault(fx, set()).add(est)
        est_by_flux = {fx: sorted(v) for fx, v in est_by_flux.items()}
        for fx, ests in est_by_flux.items():
            assert len(ests) == 29, (run, fx, len(ests))
        rd["fluxes"] = est_by_flux
        est_set = {tuple(sorted(v)) for v in est_by_flux.values()}
        assert len(est_set) == 1, (run, "noms d'estimateurs non uniformes")
        names = sorted(next(iter(est_set)))
        if all_estimators is None:
            all_estimators = names
        assert names == all_estimators, (run, "noms différents d'un run à l'autre")
    estimators = all_estimators
    n_est = len(estimators)
    n_cases = sum(len(rd["fluxes"]) for rd in run_data.values())
    print(f"Estimateurs vérifiés : {n_est} — cas (run, flux) : {n_cases}")

    # ---- Loupe A : redondance ----
    A_real, A_null = {}, {}
    pair_real, pair_null = [], []
    for run, rd in run_data.items():
        for fx, ests in rd["fluxes"].items():
            X = np.column_stack([rd["num"][f"{fx}_{e}_mean"].values
                                 for e in ests])
            R = np.column_stack([ranks_with_nan(X[:, k]) for k in range(n_est)])
            M = spearman_matrix(R)
            key = (run, fx)
            A_real[key] = M
            iu = np.triu_indices(n_est, k=1)
            pair_real.extend(np.abs(M[iu]).tolist())
            rng = np.random.default_rng(1234)
            null_vals = []
            for _ in range(20):
                Rp = np.column_stack([rng.permutation(R[:, k])
                                      for k in range(n_est)])
                Mp = spearman_matrix(Rp)
                null_vals.extend(np.abs(Mp[iu]).tolist())
            A_null[key] = null_vals
            pair_null.extend(null_vals)
    pair_real = np.array([v for v in pair_real if np.isfinite(v)])
    pair_null = np.array([v for v in pair_null if np.isfinite(v)])

    # Groupes consensus : médiane |ρ| ≥ 0,90 à travers les cas
    med_rho = np.full((n_est, n_est), np.nan)
    for i, j in itertools.combinations(range(n_est), 2):
        vals = [np.abs(A_real[k][i, j]) for k in A_real
                if np.isfinite(A_real[k][i, j])]
        med_rho[i, j] = med_rho[j, i] = float(np.median(vals))
    consensus_pairs = [(i, j) for i, j in itertools.combinations(range(n_est), 2)
                       if np.isfinite(med_rho[i, j]) and med_rho[i, j] >= 0.90]
    consensus_groups = union_groups(consensus_pairs, n_est)
    per_est = {}
    for k, e in enumerate(estimators):
        vals = [np.abs(A_real[key][k, j]) for key in A_real for j in range(n_est)
                if j != k and np.isfinite(A_real[key][k, j])]
        maxmed = float(np.nanmax([med_rho[k, j] for j in range(n_est)
                                  if j != k and np.isfinite(med_rho[k, j])]))
        per_est[e] = {
            "median_abs_rho_real": float(np.median(vals)),
            "max_median_abs_rho": maxmed,
            "consensus_singleton": bool(maxmed < 0.90),
        }

    # ---- Loupe B : contrastes + nuls ----
    B_real, B_null = {}, {}
    for run, rd in run_data.items():
        thr = rd["opt_threshold"]
        pre = rd["progress"] < thr
        post = ~pre
        for fx, ests in rd["fluxes"].items():
            for ei, e in enumerate(ests):
                s = rd["num"][f"{fx}_{e}_mean"].values.astype(float)
                key = (run, fx, e)
                B_real[key] = {
                    "cohen_d": cohen_d(s[pre], s[post]),
                    "cliff": cliff_delta(s[pre], s[post]),
                    "n_pre": int(np.isfinite(s[pre]).sum()),
                    "n_post": int(np.isfinite(s[post]).sum()),
                    "n_nan": int(np.isnan(s).sum()),
                }
                rng = np.random.default_rng(1234)
                null_d = []
                for _ in range(20):
                    sp = rng.permutation(s)
                    null_d.append(cohen_d(sp[pre], sp[post]))
                B_null[key] = [v for v in null_d if np.isfinite(v)]
    for e in estimators:
        ds = [abs(B_real[k]["cohen_d"]) for k in B_real if k[2] == e
              and np.isfinite(B_real[k]["cohen_d"])]
        nds = [abs(v) for k in B_null if k[2] == e for v in B_null[k]]
        per_est[e]["median_abs_d_real"] = float(np.median(ds))
        per_est[e]["median_abs_d_null"] = float(np.median(nds))
        per_est[e]["median_nan_cohorts"] = float(np.median(
            [B_real[k]["n_nan"] for k in B_real if k[2] == e]))

    # ---- Loupe C : gain incrémental, par (run, flux) ----
    C_real, C_null = {}, {}
    for run, rd in run_data.items():
        thr = rd["opt_threshold"]
        y = (rd["progress"] >= thr).astype(int)
        for fx, ests in rd["fluxes"].items():
            X = np.column_stack([rd["num"][f"{fx}_{e}_mean"].values
                                 for e in ests])
            sel, aucs, gains = forward_selection(X, y)
            C_real[(run, fx)] = {
                "selected": [ests[i] for i in sel],
                "aucs": aucs,
                "gains": gains,
            }
            rng = np.random.default_rng(4321)
            null_gains = []
            for _ in range(20):
                yp = rng.permutation(y)
                _, _, g = forward_selection(X, yp)
                null_gains.append(g)
            C_null[(run, fx)] = null_gains
    for e in estimators:
        steps, gains_at_sel = [], []
        for (run, fx), cr in C_real.items():
            if e in cr["selected"]:
                steps.append(cr["selected"].index(e) + 1)
                gains_at_sel.append(cr["gains"][cr["selected"].index(e)])
        null_step1 = [C_null[k][p][0] for k in C_null for p in range(20)
                      if len(C_null[k][p]) > 0]
        per_est[e]["selection_count"] = len(steps)
        per_est[e]["median_selection_step"] = (float(np.median(steps))
                                               if steps else None)
        per_est[e]["median_gain_at_selection"] = (float(np.median(gains_at_sel))
                                                  if gains_at_sel else None)
        per_est[e]["null_step1_gain_median"] = float(np.median(null_step1))
        per_est[e]["null_step1_gain_p95"] = float(np.percentile(null_step1, 95))

    # ---- Couche E : INAPPLICABLE sur mushroom (pas de Tc) ----
    E = {"applicable": False,
         "reason": "Aucune vérité terrain sur mushroom ; couche supprimée, "
                   "pas remplacée (voir PROTOCOLE_LOUPES_LOT.md)."}
    # Dégénérescence par (run, flux) : séries à <10 cohortes finies sur 30
    flux_degeneracy = {}
    for run, rd in run_data.items():
        for fx, ests in rd["fluxes"].items():
            deg = []
            for e in ests:
                s_ = rd["num"][f"{fx}_{e}_mean"].values.astype(float)
                if np.isfinite(s_).sum() < 10:
                    deg.append(e)
            flux_degeneracy[f"{run}|{fx}"] = deg

    out = {
        "shas": shas,
        "runs_inclus": sorted(run_data.keys()),
        "runs_exclus": excluded,
        "n_cases": n_cases,
        "estimators": estimators,
        "A_summary": {
            "pairs_real_median_abs_rho": float(np.median(pair_real)),
            "pairs_real_frac_ge_090": float((pair_real >= 0.90).mean()),
            "pairs_null_median_abs_rho": float(np.median(pair_null)),
            "pairs_null_frac_ge_090": float((pair_null >= 0.90).mean()),
            "consensus_pairs": [[estimators[i], estimators[j]]
                                for i, j in consensus_pairs],
            "consensus_groups": [[estimators[i] for i in g]
                                 for g in consensus_groups],
        },
        "per_estimator": per_est,
        "C_real": {f"{r}|{f}": v for (r, f), v in C_real.items()},
        "E_tc_layer": E,
        "flux_degeneracy": flux_degeneracy,
    }
    with open(OUT / "resultats_estimateurs_lot.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for e in estimators:
        p = per_est[e]
        rows.append({
            "estimateur": e,
            "median_abs_rho_reel": round(p["median_abs_rho_real"], 4),
            "max_median_abs_rho": round(p["max_median_abs_rho"], 4),
            "singleton_consensus": p["consensus_singleton"],
            "median_abs_d_reel": round(p["median_abs_d_real"], 4),
            "median_abs_d_nul": round(p["median_abs_d_null"], 4),
            "median_nan_cohortes": p["median_nan_cohorts"],
            f"selections_sur_{n_cases}": p["selection_count"],
            "pas_median_selection": p["median_selection_step"],
            "gain_median_selection": (round(p["median_gain_at_selection"], 4)
                                      if p["median_gain_at_selection"] is not None else None),
            "nul_gain_pas1_median": round(p["null_step1_gain_median"], 4),
            "nul_gain_pas1_p95": round(p["null_step1_gain_p95"], 4),
        })
    pd.DataFrame(rows).to_csv(OUT / "resultats_estimateurs_lot.csv", index=False)
    print(json.dumps({"runs_inclus": len(run_data), "n_cases": n_cases,
                      "A_summary": out["A_summary"],
                      "E_tc_layer": E}, indent=2, ensure_ascii=False))
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
