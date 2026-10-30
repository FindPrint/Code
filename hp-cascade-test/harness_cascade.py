# -*- coding: utf-8 -*-
"""Harnais du test cascade v3.7.0-HP-v3 sur le banc Ising v3.5.4.
Protocole gelé : workspace/hp-cascade-test/PROTOCOLE.md (30 oct. 2026).
Lecture seule des sources et des données. La cascade ne voit que des
rangs % et des séries y ; T ne sert qu'au harnais (construction +
conversion descriptive %->T après coup).
"""
import hashlib
import json
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HOME = Path.home()
USER_FILES = HOME / "workspace" / "user" / "files"
BENCH = HOME / "workspace" / "ising-v354" / "data"
OUT = Path(__file__).resolve().parent

HP_FILES = {
    "Tlog_v3_5_5_HP_v1.py": "24e6549536091bb1b1429856a3b42607a5e7328851a6061f209b4610ed87de6e",
    "Tlog_v3_6_0_HP_v2.py": "7a6948483e8995370ed0c581dd97215bcb1d2ad7dfeed5b29a95cb37f40c31c1",
    "Tlog_v3_7_0_HP_v3.py": "8527b92ccd2eda0ad3b0205eb63fe380cc0046741132d2e81bcc13dff14056fc",
}
DATA_FILES = {
    "ising_classic_v354.csv": "9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d",
    "ising_classic_v354_temperature.csv": "4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4",
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_files():
    for name, sha in HP_FILES.items():
        got = sha256(USER_FILES / name)
        assert got == sha, f"SHA HP {name} : {got} != {sha}"
    for name, sha in DATA_FILES.items():
        got = sha256(BENCH / name)
        assert got == sha, f"SHA données {name} : {got} != {sha}"


def pct_to_T(pct, p_axis, t_values):
    """Conversion descriptive %->T par interpolation (harnais seulement)."""
    return float(np.interp(pct, p_axis, t_values))


def run_one(cascade, label, p_axis, y_series, t_values):
    out = cascade(np.asarray(p_axis, dtype=float),
                  np.asarray(y_series, dtype=float))
    zones = out.get("zones", [])
    rec = {
        "serie": label,
        "status": out.get("status"),
        "T_-2_pct": out.get("T_-2_F2_pre_onset"),
        "T_-1_pct": out.get("T_-1_F1_pre_inflection"),
        "T_0_pct": out.get("T_0_Monte_Carlo_Central"),
        "T_+1_pct": out.get("T_+1_F1_post_deceleration"),
        "T_+2_pct": out.get("T_+2_F2_post_attractor"),
        "zones_pct": zones,
        "ordered_5_zones": bool(len(zones) == 5 and all(
            zones[i] < zones[i + 1] for i in range(4))),
        "max_F1_velocity": out.get("max_F1_velocity"),
        "max_F2_curvature": out.get("max_F2_curvature"),
        "smooth_sigma": out.get("smooth_sigma"),
    }
    if t_values is not None and rec["T_0_pct"] is not None:
        rec["T_0_T"] = pct_to_T(rec["T_0_pct"], p_axis, t_values)
    return rec


def main():
    check_files()

    # Import de la cascade via la chaîne reçue (v3.7.0 -> v3.6.0 -> v3.5.5)
    v3 = SourceFileLoader("tlog_v37_test",
                          str(USER_FILES / "Tlog_v3_7_0_HP_v3.py")).load_module()
    cascade = v3.compute_5_threshold_cascade

    df = pd.read_csv(BENCH / "ising_classic_v354.csv")
    tdf = pd.read_csv(BENCH / "ising_classic_v354_temperature.csv")
    assert len(df) == 960 and len(tdf) == 960
    assert not df.isna().any().any()
    T = tdf["temperature"].values.astype(float)
    M = df["magnetization"].values.astype(float)

    # Moyennes par T (24 groupes de 40 snapshots)
    order = np.argsort(T, kind="stable")
    T_sorted = T[order]
    M_sorted = M[order]
    t_vals = np.array(sorted(set(T_sorted)))
    assert len(t_vals) == 24
    m_mean = np.array([M_sorted[T_sorted == tv].mean() for tv in t_vals])
    p24 = 100.0 * stats.rankdata(t_vals, method="average") / len(t_vals)

    # E_thermal, formule de la décompression (harnais, pas pipeline)
    def e_thermal(t_arr, m_arr):
        e = t_arr / 4.0 * (1.0 - m_arr + 0.2)
        e = (e - np.nanmin(e)) / (np.nanmax(e) - np.nanmin(e) + 1e-9)
        return np.clip(e, 0, 1)

    results = []
    # V1 primaire
    results.append(run_one(cascade, "V1_magnetization_per_T", p24, m_mean, t_vals))
    # V1b robustesse : snapshots
    p960 = 100.0 * stats.rankdata(T_sorted, method="average") / len(T_sorted)
    results.append(run_one(cascade, "V1b_magnetization_snapshots", p960,
                           M_sorted, None))
    # V2 E_thermal réel
    e_real = e_thermal(t_vals, m_mean)
    results.append(run_one(cascade, "V2_E_thermal_real", p24, e_real, t_vals))
    # V3 : M mélangé, T intact (graine 7)
    rng7 = np.random.default_rng(7)
    e_v3 = e_thermal(t_vals, rng7.permutation(m_mean))
    results.append(run_one(cascade, "V3_E_thermal_M_shuffled", p24, e_v3, t_vals))
    # V4 : T mélangé, M intact (graine 8)
    rng8 = np.random.default_rng(8)
    e_v4 = e_thermal(rng8.permutation(t_vals), m_mean)
    results.append(run_one(cascade, "V4_E_thermal_T_shuffled", p24, e_v4, t_vals))
    # V5 : 20 nuls par permutation de V1 (graine 1234)
    rng = np.random.default_rng(1234)
    null_t0 = []
    for i in range(20):
        rec = run_one(cascade, f"V5_null_perm_{i:02d}", p24,
                      rng.permutation(m_mean), t_vals)
        results.append(rec)
        null_t0.append(rec["T_0_T"])

    null_t0 = np.array(null_t0)
    real_t0 = results[0]["T_0_T"]
    summary = {
        "V1_T_0_T": real_t0,
        "V1_ordered_5_zones": results[0]["ordered_5_zones"],
        "null_T_0_T_median": float(np.median(null_t0)),
        "null_T_0_T_min": float(np.min(null_t0)),
        "null_T_0_T_max": float(np.max(null_t0)),
        "null_ordered_5_zones_count": sum(
            1 for r in results if r["serie"].startswith("V5") and r["ordered_5_zones"]),
        "null_count": 20,
        "real_rank_among_21": int((null_t0 < real_t0).sum()) + 1,
        "reference_lot_v354_T": 2.2565,
        "Tc_Onsager": 2.2692,
    }

    with open(OUT / "resultats_cascade.json", "w", encoding="utf-8") as f:
        json.dump({"runs": results, "summary": summary}, f, indent=2,
                  ensure_ascii=False)
    rows = pd.DataFrame(results)
    rows.to_csv(OUT / "resultats_cascade.csv", index=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    for r in results:
        print(f"{r['serie']:28s} status={r['status']} "
              f"T_0_pct={r['T_0_pct']} T_0_T={r.get('T_0_T')} "
              f"ordered={r['ordered_5_zones']} zones={r['zones_pct']}")


if __name__ == "__main__":
    main()
