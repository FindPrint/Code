# -*- coding: utf-8 -*-
"""Harnais du test discriminateur bruit-information HP sur le banc Ising.
Protocole gelé : workspace/hp-noise-test/PROTOCOLE.md (30 oct. 2026).
Lecture seule des sources et des données. Fonction testée importée du
fichier unique consolidé (copie de la fonction v3.7.0, équivalence
vérifiée le 30 oct. 2026 dans verification_uni.json).
"""
import hashlib
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
import pandas as pd

HOME = Path.home()
BENCH = HOME / "workspace" / "ising-v354" / "data"
UNI = HOME / "workspace" / "hp-cascade-test" / "Tlog_v3_7_0_HP_uni_v1.py"
OUT = Path(__file__).resolve().parent

SHAS = {
    BENCH / "ising_classic_v354.csv":
        "9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d",
    BENCH / "ising_classic_v354_temperature.csv":
        "4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4",
    UNI: "45dadb940e6743c4b0f63475c1eb1ad5c2271c5d100ff11ca419f620cc73dc8c",
}
REPERE_T = 2.2565


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    for path, sha in SHAS.items():
        got = sha256(path)
        assert got == sha, f"SHA {path.name} : {got} != {sha}"

    mod = SourceFileLoader("tlog_uni_noise", str(UNI)).load_module()
    analyze = mod.analyze_noise_information_content

    df = pd.read_csv(BENCH / "ising_classic_v354.csv")
    tdf = pd.read_csv(BENCH / "ising_classic_v354_temperature.csv")
    assert len(df) == 960 and len(tdf) == 960
    assert not df.isna().any().any()
    T = tdf["temperature"].values.astype(float)
    M = df["magnetization"].values.astype(float)

    order = np.argsort(T, kind="stable")
    Ts, Ms = T[order], M[order]
    t_vals = np.array(sorted(set(Ts)))
    assert len(t_vals) == 24
    # Bloc repère : 9e bloc (indice 8). 2,2565 est la valeur ARRONDIS
    # du point de grille 2,2565217… : le repère est donc identifié
    # comme le bloc le plus proche de 2,2565, et le partage
    # pré (8 blocs) / repère (1) / post (15) est celui du protocole.
    idx_repere = int(np.argmin(np.abs(t_vals - REPERE_T)))
    assert idx_repere == 8, (idx_repere, t_vals[idx_repere])
    assert abs(t_vals[8] - REPERE_T) < 1e-3, t_vals[8]

    # Résidus : snapshot moins moyenne de son bloc
    resid = np.empty_like(Ms)
    block_id = np.empty(len(Ms), dtype=int)
    for i, tv in enumerate(t_vals):
        mask = Ts == tv
        resid[mask] = Ms[mask] - Ms[mask].mean()
        block_id[mask] = i

    R_all = resid
    R_pre = resid[block_id < 8]
    R_post = resid[block_id > 8]
    assert len(R_all) == 960 and len(R_pre) == 320 and len(R_post) == 600

    series = {"R_all": R_all, "R_pre": R_pre, "R_post": R_post}
    rng_p = np.random.default_rng(1234)
    for i in range(20):
        series[f"perm_null_{i:02d}"] = rng_p.permutation(R_all)
    mu, sd = float(np.mean(R_all)), float(np.std(R_all))
    rng_g = np.random.default_rng(4321)
    for i in range(20):
        series[f"gauss_null_{i:02d}"] = rng_g.normal(mu, sd, 960)

    runs = []
    for label, s in series.items():
        out = analyze(np.asarray(s, dtype=float))
        out["serie"] = label
        runs.append(out)

    def get(label, key):
        for r in runs:
            if r["serie"] == label:
                return r[key]
        raise KeyError(label)

    perm = [r for r in runs if r["serie"].startswith("perm_null")]
    gauss = [r for r in runs if r["serie"].startswith("gauss_null")]
    summary = {
        "R_all": {k: get("R_all", k) for k in
                  ("is_informative", "hurst_exponent", "kurtosis", "skewness",
                   "jarque_bera_p_value", "fractal_length_ratio", "spectral_entropy")},
        "R_pre": {k: get("R_pre", k) for k in
                  ("is_informative", "hurst_exponent", "kurtosis", "skewness",
                   "jarque_bera_p_value", "fractal_length_ratio", "spectral_entropy")},
        "R_post": {k: get("R_post", k) for k in
                   ("is_informative", "hurst_exponent", "kurtosis", "skewness",
                    "jarque_bera_p_value", "fractal_length_ratio", "spectral_entropy")},
        "perm_hurst_min": float(min(r["hurst_exponent"] for r in perm)),
        "perm_hurst_median": float(np.median([r["hurst_exponent"] for r in perm])),
        "perm_hurst_max": float(max(r["hurst_exponent"] for r in perm)),
        "perm_entropy_min": float(min(r["spectral_entropy"] for r in perm)),
        "perm_entropy_median": float(np.median([r["spectral_entropy"] for r in perm])),
        "perm_entropy_max": float(max(r["spectral_entropy"] for r in perm)),
        "perm_informative_count": sum(1 for r in perm if r["is_informative"]),
        "perm_jb_p_equals_real": all(
            r["jarque_bera_p_value"] == get("R_all", "jarque_bera_p_value") for r in perm),
        "gauss_informative_count": sum(1 for r in gauss if r["is_informative"]),
        "gauss_hurst_min": float(min(r["hurst_exponent"] for r in gauss)),
        "gauss_hurst_median": float(np.median([r["hurst_exponent"] for r in gauss])),
        "gauss_hurst_max": float(max(r["hurst_exponent"] for r in gauss)),
        "gauss_jb_p_min": float(min(r["jarque_bera_p_value"] for r in gauss)),
        "gauss_jb_p_median": float(np.median([r["jarque_bera_p_value"] for r in gauss])),
        "gauss_jb_p_max": float(max(r["jarque_bera_p_value"] for r in gauss)),
        "R_all_mean": mu,
        "R_all_std": sd,
    }

    with open(OUT / "resultats_noise.json", "w", encoding="utf-8") as f:
        json.dump({"runs": runs, "summary": summary}, f, indent=2, ensure_ascii=False)
    pd.DataFrame(runs).to_csv(OUT / "resultats_noise.csv", index=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
