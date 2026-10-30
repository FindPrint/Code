# -*- coding: utf-8 -*-
"""Vérification d'équivalence du fichier unique candidat vs la chaîne reçue.
Compare, sur les mêmes entrées : cascade 5 seuils (série V1 du test),
discriminateur bruit-information (série fixe), et présence des fonctions
clés. Échec = le candidat ne remplace pas la chaîne.
"""
import json
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HOME = Path.home()
USER_FILES = HOME / "workspace" / "user" / "files"
TEST = Path(__file__).resolve().parent

chain = SourceFileLoader("tlog_v37_chain",
                         str(USER_FILES / "Tlog_v3_7_0_HP_v3.py")).load_module()
uni = SourceFileLoader("tlog_v37_uni",
                       str(TEST / "Tlog_v3_7_0_HP_uni_v1.py")).load_module()

# Série V1 du test : aimantation moyenne par T, p = rangs %
df = pd.read_csv(HOME / "workspace" / "ising-v354" / "data" / "ising_classic_v354.csv")
tdf = pd.read_csv(HOME / "workspace" / "ising-v354" / "data" / "ising_classic_v354_temperature.csv")
T = tdf["temperature"].values.astype(float)
M = df["magnetization"].values.astype(float)
order = np.argsort(T, kind="stable")
Ts, Ms = T[order], M[order]
t_vals = np.array(sorted(set(Ts)))
m_mean = np.array([Ms[Ts == tv].mean() for tv in t_vals])
p24 = 100.0 * stats.rankdata(t_vals, method="average") / len(t_vals)

c1 = chain.compute_5_threshold_cascade(p24, m_mean)
c2 = uni.compute_5_threshold_cascade(p24, m_mean)
cascade_equal = c1 == c2

rng = np.random.default_rng(0)
serie_fixe = rng.normal(0, 1, 200)
n1 = chain.analyze_noise_information_content(serie_fixe)
n2 = uni.analyze_noise_information_content(serie_fixe)
noise_equal = n1 == n2

keys = ["run_pipeline", "decompress_energy_flux", "detect_multi_thresholds",
        "compute_time_aligned_progress", "detect_order_saliency",
        "fit_regime_attractor", "predict_regime_attractor",
        "complexity_guided_mc_paths", "run_multilevel_v3",
        "level_next_threshold_v3", "compute_5_threshold_cascade",
        "analyze_noise_information_content", "main", "main_v1", "main_v2"]
presence = {k: hasattr(uni, k) for k in keys}

report = {
    "cascade_equal": bool(cascade_equal),
    "cascade_chain": c1,
    "cascade_uni": c2,
    "noise_equal": bool(noise_equal),
    "noise_chain": n1,
    "noise_uni": n2,
    "presence_uni": presence,
    "uni_VERSION": getattr(uni, "VERSION", None),
}
with open(TEST / "verification_uni.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(json.dumps({k: report[k] for k in
                  ("cascade_equal", "noise_equal", "presence_uni", "uni_VERSION")},
                 indent=2, ensure_ascii=False))
if not (cascade_equal and noise_equal and all(presence.values())):
    sys.exit(1)
print("ÉQUIVALENCE VÉRIFIÉE")
