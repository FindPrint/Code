# -*- coding: utf-8 -*-
"""Run Ising v3.5.4 : Tlog_v3_5_4_harmonic_v1.py sur ising_classic_v354.csv.
Usage: python3 run_one_ising.py <control_col> <outdir>
Contrôle EXCLU des flux (règle Porte D), mode stable, w80, cohen_d, graine 42.
Produit les exports du pipeline + run_summary.json + per_flux/landscape/F1F2
+ traduction température du seuil (temperature.csv séparé, lecture après coup).
Adapté de pilote/run_one_v35.py (mêmes exports et analyses post-run).
"""
import sys, json, time, traceback
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, '/home/hatch/workspace/pipeline-v35')
import Tlog_v3_5_4_harmonic_v1 as pv3

BASE = Path('/home/hatch/workspace/ising-v354')
csv_path = BASE / 'data' / 'ising_classic_v354.csv'
temp_path = BASE / 'data' / 'ising_classic_v354_temperature.csv'
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
    'pipeline': 'v3.5.4-H1 Tlog_v3_5_4_harmonic_v1.py (Q6-A)',
    'pipeline_sha256': 'b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d',
    'dataset': 'ising_classic_v354.csv (Ising 2D simulé L=32, graine 42, voir PROTOCOLE.md)',
    'dataset_sha256': '9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d',
    'temperature_sha256': '4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4',
    'control': control, 'status': 'OK', 'mode': 'stable',
    'fluxes_analyses': flux_cols,
    'active_keys': flux_cols[:2], 'reactive_keys': flux_cols[2:4],
    'ni_actif_ni_reactif': flux_cols[4:],
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
    'theiler': to.get('theiler'),
    'threshold_source': md.get('threshold_source'),
    'threshold_warnings': md.get('threshold_warnings'),
    'scan_fast_fallback_log': to.get('scan_fast_fallback_log'),
    'stability_rating': stab.get('rating'), 'stability_mean': stab.get('mean'),
    'stability_std': stab.get('std'),
    'noise_label': nd.get('diagnostic_label') or nd.get('label'),
    'scores_moyens_par_Q': q_summary,
}
with open(outdir / 'run_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

# ---------- Analyse post-run : seuils propres par flux + traduction température ----------
try:
    dfc = df.dropna(subset=[control]).reset_index(drop=True)
    temps = pd.read_csv(temp_path)['temperature'].values
    assert len(temps) == len(dfc), 'temperature.csv / données : longueurs différentes'
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

    def temperature_au_seuil(pct):
        # Température médiane des lignes dont le rang du contrôle encadre le seuil.
        order = np.argsort(dfc[control].values, kind='stable')
        k = float(pct) / 100.0 * n
        lo = max(0, int(k - 0.015 * n)); hi = min(n, int(k + 0.015 * n))
        win = temps[order[lo:hi]]
        return round(float(np.median(win)), 4) if len(win) else None

    rows = []
    for col in flux_cols:
        th, curve = pv3.scan_critical_threshold(
            {col: z(dfc[col].values)}, progress, mode_cfg,
            n_candidates=NC, w_size=W, min_grp=MG)
        sc = pd.DataFrame(curve).dropna(subset=['score'])
        top = sc.nlargest(3, 'score')
        rows.append({'flux': col, 'seuil_propre_pct': round(float(th), 2),
                     'temperature_mediane_au_seuil': temperature_au_seuil(th),
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
                              'rel_au_max': round(float(y[i] / y.max()), 3),
                              'temperature_mediane': temperature_au_seuil(x[i])})
        summary['landscape_peaks'] = peaks
        summary['scan_max_score'] = round(float(y.max()), 3)
        summary['scan_argmax_pct'] = round(float(x[int(np.argmax(y))]), 2)
        summary['temperature_mediane_au_argmax'] = temperature_au_seuil(x[int(np.argmax(y))])
    pd.DataFrame(peaks).to_csv(outdir / 'landscape_peaks.csv', index=False)

    # Traduction température du seuil MC + valeur du contrôle au seuil
    if bc.get('threshold') is not None:
        summary['temperature_mediane_au_seuil_mc'] = temperature_au_seuil(bc['threshold'])
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
                if isinstance(v, dict) and (v.get('status') == 'success' or v.get('status_pre') == 'success'):
                    trows.append({'estimateur': est, 'flux': flux,
                                  'F1': v.get('first_derivative'),
                                  'F2': v.get('second_derivative'),
                                  'signe': v.get('sign'), 'ordre': v.get('order'),
                                  'F1_pre': v.get('first_derivative_pre'),
                                  'F2_pre': v.get('second_derivative_pre'),
                                  'signe_pre': v.get('sign_pre'), 'ordre_pre': v.get('order_pre'),
                                  'delta_F1': v.get('delta_first_derivative'),
                                  'delta_F2': v.get('delta_second_derivative'),
                                  'sign_change': v.get('sign_change'),
                                  'status_post': v.get('status'), 'status_pre': v.get('status_pre'),
                                  'points_count_pre': v.get('points_count_pre')})
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
