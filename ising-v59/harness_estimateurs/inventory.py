# Inventaire des sorties v5.9.0f (étape 1) et v5.4.0 pour la lecture estimateurs.
# Lecture seule. Exclut ising-v59/ising/full/fliprate (run en cours).
import hashlib, json
from pathlib import Path
import pandas as pd

HOME = Path.home()
ESTIMATORS = ["Higuchi","DFA","Katz","Hurst","SampleEn","Petrosian","Sevcik","BoxCounting",
 "PermutationEntropy","CorrelationD2","GrassbergerProcaccia","InformationD1","VisibilityGraph",
 "TwoNN","DANCo","Fisher","LevinaBickel","PCAIntrinsic","LocalPCA","GraphDimension",
 "PersistentHomology","MFA","KolmogorovLZ","SpectralBeta","SpectralDimension","Hurst2mH",
 "Lyapunov","MultifractalDeltaAlpha","SingularityFmax"]

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def scan(version, base):
    out = []
    for dfp in sorted(Path(base).rglob("df_feat.csv")):
        rel = str(dfp.relative_to(base))
        if version == "v5.9.0f" and rel.startswith("ising/full/fliprate"):
            continue  # run en cours v59, ne pas lire
        d = Path(dfp).parent
        mr = d / "master_results.json"
        rec = {"version": version, "rel": rel, "dir": str(d),
               "sha_df_feat": sha256(dfp)}
        df = pd.read_csv(dfp)
        rec["n_rows"] = len(df)
        rec["progress_min"] = float(df["Progress"].min())
        rec["progress_max"] = float(df["Progress"].max())
        rec["n_cohorts_unique"] = sorted(set(df["N_cohorts"].tolist()))
        cols = [c for c in df.columns if c.endswith("_mean")]
        by_flux = {}
        for c in cols:
            fx, est = c[:-5].split("_", 1)
            by_flux.setdefault(fx, []).append(est)
        rec["fluxes"] = {fx: sorted(v) for fx, v in by_flux.items()}
        rec["estimators_ok"] = all(sorted(v) == sorted(ESTIMATORS) for v in by_flux.values())
        # NaN par estimateur (toutes flux confondues)
        rec["nan_total"] = int(df[[c for c in df.columns if c.endswith("_mean")]].isna().sum().sum())
        if mr.exists():
            mj = json.load(open(mr))
            rec["sha_master"] = sha256(mr)
            tm = mj.get("run_pipeline", {}).get("threshold_metadata", {})
            rec["opt_threshold"] = tm.get("opt_threshold")
            rec["mc"] = tm.get("opt_threshold")
            casc = mj.get("five_threshold_cascade", {})
            rec["T0"] = casc.get("T_0_Monte_Carlo_Central")
            rec["version_code"] = mj.get("version")
            rec["control"] = mj.get("metadata", {}).get("control")
            rec["target"] = mj.get("metadata", {}).get("target")
        else:
            rec["master_missing"] = True
        out.append(rec)
    return out

inv59 = scan("v5.9.0f", HOME/"workspace/ising-v59")
inv54 = scan("v5.4.0", HOME/"workspace/ising-v54")
# appariement par chemin relatif (synth/... ou ising/...)
m54 = {r["rel"]: r for r in inv54}
matched = []
for r in inv59:
    m = m54.get(r["rel"])
    if m:
        matched.append({"rel": r["rel"],
                        "df_identical": r["sha_df_feat"] == m["sha_df_feat"],
                        "master_identical": r.get("sha_master") == m.get("sha_master"),
                        "thr59": r.get("opt_threshold"), "thr54": m.get("opt_threshold"),
                        "T0_59": r.get("T0"), "T0_54": m.get("T0"),
                        "fluxes59": r["fluxes"], "fluxes54": m["fluxes"]})
json.dump({"v59": inv59, "v54": inv54, "matched": matched},
          open(HOME/"workspace/ising-v59/harness_estimateurs/inventory.json","w"), indent=2)
print("v59 outputs:", len(inv59), " v54 outputs:", len(inv54), " matched:", len(matched))
print("df_feat identiques v59/v54:", sum(1 for m in matched if m["df_identical"]), "/", len(matched))
print("master identiques:", sum(1 for m in matched if m["master_identical"]), "/", len(matched))
print("estimators_ok partout:", all(r["estimators_ok"] for r in inv59+inv54))
print("seuils differents:", [(m["rel"], m["thr59"], m["thr54"]) for m in matched if m["thr59"] != m["thr54"]])
print("T0 differents:", [(m["rel"], m["T0_59"], m["T0_54"]) for m in matched if m["T0_59"] != m["T0_54"]])
# cas (output, flux)
def ncases(inv): return sum(len(r["fluxes"]) for r in inv)
print("cases v59:", ncases(inv59), " cases v54:", ncases(inv54))
# N_cohorts : valeurs uniques sur un fichier ising et un synth
import collections
for r in inv59[:1] + [x for x in inv59 if x["rel"].startswith("ising/")][:1]:
    print(r["rel"], "N_cohorts uniq:", r["n_cohorts_unique"][:10], "n_rows:", r["n_rows"], "progress:", r["progress_min"], r["progress_max"])
