# -*- coding: utf-8 -*-
"""Pilote generique : pipeline v3.3-H1 (uploade) sur Food_Costs_2013_pipeline.csv.
Usage: python3 run_one.py <control_col> <outdir>
Contrôle EXCLU des flux (règle Porte D), mode stable, w80, cohen_d, graine 42.
Produit les exports du pipeline + run_summary.json + per_flux/landscape/F1F2.
"""
import sys, json, time, traceback
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, '/home/hatch/workspace/user/files')
import pipeline_autonome_v3_3_harmonic_v1 as pv3

BASE = Path('/home/hatch/workspace/food-costs-2016')
csv_path = BASE / 'data' / 'Food_Costs_2016_pipeline.csv'
control = sys.argv[1]
outdir = Path(sys.argv[2]).resolve()
outdir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(csv_path)
num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
assert control in num_cols, f"controle inconnu {control}"
flux_cols = [c for c in num_cols if c != control]
mapping = {'control_col': control, 'flux_mapping': {c: c for c in flux_cols}}
opt_cfg = {'w_size': 80, 'test': 'cohen_d', 'random_seed': 42,
           'full_triangulation': False}

t0 = time.time()
try:
    results, df_feat, fluxes, fluxes_ui = pv3.run_pipeline(
        data_source='custom', custom_file_path=str(csv_path),
        mapping=mapping, mode='stable', opt_cfg=opt_cfg)
except Exception as e:
    dt = time.time() - t0
    err = {'control': control, 'status': 'ECHEC', 'duration_s': round(dt, 1),
           'error_type': type(e).__name__, 'error': str(e),
           'n_valides_controle': int(df[control].notna().sum())}
    with open(outdir / 'run_summary.json', 'w', encoding='utf-8') as f:
        json.dump(err, f, ensure_ascii=False, indent=2)
    with open(outdir / 'error.txt', 'w', encoding='utf-8') as f:
        f.write(traceback.format_exc())
    print(json.dumps(err, ensure_ascii=False, indent=2))
    print(f"ECHEC {control} apres {dt:.1f}s : {e}")
    sys.exit(0)
dt = time.time() - t0

pv3.export_json_results(results, outdir / 'pipeline_results.json')
pv3.export_csv_results(df_feat, results['scores'], results['noise_diagnostic'],
                       outdir / 'numerical_results.csv')
pv3.export_text_report(results, outdir / 'text_report.txt')
main_threshold = results['metadata'].get('opt_threshold', 50)
try:
    pv3.plot_threshold_scan(results['scan_curve'], main_threshold,
                            outdir / 'threshold_scan.png')
    pv3.plot_noise_diagnostic(results['noise_diagnostic'],
                              outdir / 'noise_diagnostic.png')
except Exception as e:
    print(f"plot warning: {e}")
pd.DataFrame(results.get('scan_curve') or []).to_csv(outdir / 'scan_curve.csv', index=False)

md = results['metadata']
to = md.get('threshold_optimization') or {}
bc = to.get('best_config') or {}
stab = md.get('stability_report') or {}
nd = results.get('noise_diagnostic') or {}
scores = results.get('scores') or {}
q_summary = {}
try:
    for q, per in scores.items():
        vals = [v for v in per.values() if isinstance(v, (int, float))]
        if vals:
            q_summary[q] = round(float(np.mean(vals)), 3)
except Exception:
    pass
summary = {
    'dataset': 'Food_Costs_2016_pipeline.csv (Kaggle jpmiller/publicassistance, WICAgencies2016ytd/Food_Costs.csv, 92 lignes, 14 colonnes origine + agency_encoded, Cumulative Cost convertie en nombre)',
    'control': control, 'status': 'OK', 'mode': 'stable',
    'n_pts': md.get('n_pts'), 'n_flux': len(fluxes),
    'n_valides_controle': int(df[control].notna().sum()),
    'duration_s': round(dt, 1),
    'opt_threshold_pct': md.get('opt_threshold'),
    'mc_threshold_pct': bc.get('threshold'), 'mc_score': bc.get('score'),
    'mc_w_size': bc.get('w_size'), 'mc_n_candidates': bc.get('n_candidates'),
    'mc_min_grp': bc.get('min_grp'),
    'default_threshold_pct': to.get('default_threshold'),
    'raw_mc_threshold_pct': to.get('raw_mc_threshold'),
    'raw_default_threshold_pct': to.get('raw_default_threshold'),
    'rigid_1001_threshold_pct': to.get('rigid_1001_threshold'),
    'stability_rating': stab.get('rating'), 'stability_mean': stab.get('mean'),
    'stability_std': stab.get('std'),
    'noise_label': nd.get('diagnostic_label') or nd.get('label'),
    'scores_moyens_par_Q': q_summary,
}
with open(outdir / 'run_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

# ---------- Analyse post-run : seuils propres par flux ----------
# Le pipeline a déjà tourné ; ceci ne fait que relire avec sa propre fonction
# de scan et la config MC retenue, comme les analyses AT (22 oct.).
try:
    dfc = df.dropna(subset=[control]).reset_index(drop=True)
    n = len(dfc)
    progress = 100.0 * stats.rankdata(dfc[control].values, method='average') / n
    mode_cfg = {'n_est': 4, 'w_size': 80, 'test': 'cohen_d', 'min_grp': 4,
                'min_len': 80, 'boot': True, 'full_triangulation': False,
                'random_seed': 42}
    W = int(bc.get('w_size') or 80)
    NC = int(bc.get('n_candidates') or 100)
    MG = int(bc.get('min_grp') or 3)

    def z(s):
        s = np.asarray(s, float)
        s = np.where(np.isnan(s), np.nanmean(s), s) if np.any(np.isnan(s)) else s
        return (s - s.mean()) / s.std() if s.std() > 1e-10 else np.zeros_like(s)

    rows = []
    for col in flux_cols:
        th, curve = pv3.scan_critical_threshold(
            {col: z(dfc[col].values)}, progress, mode_cfg,
            n_candidates=NC, w_size=W, min_grp=MG)
        sc = pd.DataFrame(curve).dropna(subset=['score'])
        top = sc.nlargest(3, 'score')
        rows.append({'flux': col, 'seuil_propre_pct': round(float(th), 2),
                     'score_max': round(float(top['score'].iloc[0]), 3) if len(top) else None,
                     'top3_candidats': [round(float(x), 1) for x in top['candidate']] if len(top) else []})
    pd.DataFrame(rows).to_csv(outdir / 'per_flux_thresholds.csv', index=False)
    summary['per_flux'] = rows

    # Paysage : maxima locaux de la courbe de scan globale (traitée, défaut)
    c = pd.DataFrame(results.get('scan_curve') or []).dropna(subset=['score']).sort_values('candidate')
    peaks = []
    if len(c) > 2:
        x, y = c['candidate'].values, c['score'].values
        for i in range(1, len(x) - 1):
            if y[i] >= y[i - 1] and y[i] > y[i + 1] and y[i] >= 0.55 * y.max():
                peaks.append({'candidat_pct': round(float(x[i]), 2),
                              'score': round(float(y[i]), 3),
                              'rel_au_max': round(float(y[i] / y.max()), 3)})
        summary['landscape_peaks'] = peaks
        summary['scan_max_score'] = round(float(y.max()), 3)
        summary['scan_argmax_pct'] = round(float(x[int(np.argmax(y))]), 2)
    pd.DataFrame(peaks).to_csv(outdir / 'landscape_peaks.csv', index=False)

    # Valeur du contrôle à la frontière du seuil MC (médiane des valeurs
    # dont le rang encadre le seuil) — lecture descriptive.
    if bc.get('threshold') is not None:
        order = np.argsort(dfc[control].values, kind='stable')
        sorted_ctrl = dfc[control].values[order]
        k = float(bc['threshold']) / 100.0 * n
        lo = max(0, int(k - 0.015 * n)); hi = min(n, int(k + 0.015 * n))
        win = sorted_ctrl[lo:hi]
        if len(win):
            summary['controle_valeur_au_seuil_mc'] = {
                'mediane': round(float(np.median(win)), 3),
                'moyenne': round(float(np.mean(win)), 3),
                'std': round(float(np.std(win)), 3)}

    # F1/F2 post-seuil
    ta = results.get('transition_analysis') or {}
    trows = []
    for est, per in ta.items():
        if isinstance(per, dict):
            for flux, v in per.items():
                if isinstance(v, dict) and v.get('status') == 'success':
                    trows.append({'estimateur': est, 'flux': flux,
                                  'F1': v.get('first_derivative'),
                                  'F2': v.get('second_derivative'),
                                  'signe': v.get('sign'), 'ordre': v.get('order')})
    pd.DataFrame(trows).to_csv(outdir / 'transition_F1F2.csv', index=False)
    summary['n_F1F2'] = len(trows)
    with open(outdir / 'run_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
except Exception as e:
    print(f"analyse post-run warning: {e}")
    traceback.print_exc()

print(json.dumps({k: summary.get(k) for k in
                  ['control', 'status', 'n_pts', 'opt_threshold_pct', 'mc_threshold_pct',
                   'default_threshold_pct', 'raw_mc_threshold_pct', 'stability_rating',
                   'stability_std', 'duration_s']}, ensure_ascii=False, indent=2, default=str))
print(f"DUREE {dt:.1f}s -> {outdir}")
