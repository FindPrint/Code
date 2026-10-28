# -*- coding: utf-8 -*-
"""Dossier diagnostique par run (lots dérivés 1 + EXT) : profil du flux
contrôle, scan, seuils propres, Q (moyennes par question + Q5/Q6-A par
flux), tests de bruit (proxy de variance + dérives par estimateur),
F1/F2 avant/après seuil, et flux témoins (même base / même famille /
autre famille) pour situer le seuil : même point, avant (onset) ou autre.
Lecture descriptive seulement ; T lue uniquement pour la description.
Sortie : diagnostic_runs_ext.json (ré-exécutable, ne lit que les runs OK).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

BASE = Path('/home/hatch/workspace/ising-derived')
TC = 2.269185314213
ORIGINALS = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar',
             'susceptibility']
RUNS = {'runs': ['expvar_energy', 'expvar_magnetization', 'expvar_fliprate',
                 'expvar_localvar', 'expmean_energy', 'expmean_magnetization',
                 'rollvar_magnetization_40', 'rollvar_energy_40',
                 'null_susceptibility', 'null_expvar_mag', 'null_rollvar_mag'],
        'runs_ext': ['expmean_fliprate', 'expmean_localvar',
                     'rollvar_fliprate_40', 'rollvar_localvar_40',
                     'rollmean_energy_40', 'rollmean_magnetization_40',
                     'rollmean_fliprate_40', 'rollmean_localvar_40',
                     'null_expmean_fliprate', 'null_rollvar_fliprate',
                     'null_rollmean_mag', 'null_rollmean_localvar']}

df1 = pd.read_csv(BASE / 'data' / 'ising_derived.csv')
dfx = pd.read_csv(BASE / 'data' / 'ising_derived_ext.csv')
temps = pd.read_csv(BASE / 'data' / 'ising_classic_v354_temperature.csv')['temperature'].values


def base_of(c):
    for p in ('expvar_', 'expmean_', 'rollvar_', 'rollmean_'):
        if c.startswith(p):
            b = c[len(p):]
            return b[:-3] if b.endswith('_40') else b
    return None


def fam_of(c):
    if c.startswith('null_'):
        return 'nul'
    for p in ('expvar_', 'expmean_', 'rollvar_', 'rollmean_'):
        if c.startswith(p):
            return p[:-1]
    return 'inconnu'


def counterpart(c):
    b = base_of(c)
    if c.startswith('expvar_'):
        return f'rollvar_{b}_40'
    if c.startswith('expmean_'):
        return f'rollmean_{b}_40'
    if c.startswith('rollvar_'):
        return f'expvar_{b}'
    if c.startswith('rollmean_'):
        return f'expmean_{b}'
    return None


def situe(t_run, t_autre):
    if t_autre is None or t_run is None:
        return None
    d = t_autre - t_run
    if abs(d) <= 0.07:
        return 'meme_point'
    return 'avant' if d < -0.20 else ('apres' if d > 0.20 else 'proche_autre')


def dossier(runs_dir, c):
    d = BASE / runs_dir / c
    sj = d / 'run_summary.json'
    if not sj.exists():
        return {'controle': c, 'lot': runs_dir, 'statut': 'EN COURS'}
    s = json.loads(sj.read_text(encoding='utf-8'))
    if s.get('status') != 'OK':
        return {'controle': c, 'lot': runs_dir, 'statut': s.get('status')}
    df = dfx if c in dfx.columns else df1
    x = df[c].values.astype(float)
    t_mc = s.get('temperature_mediane_au_seuil_mc')
    # --- profil du flux contrôle ---
    rho = float(stats.spearmanr(x, temps).statistic)
    bins = [(temps < 2.0), (temps >= 2.0) & (temps < TC),
            (temps >= TC) & (temps < 2.6), (temps >= 2.6)]
    med_par_bande = [round(float(np.median(x[m])), 4) if m.sum() else None for m in bins]
    order = np.argsort(x, kind='stable')
    dec = []
    for k in range(10):
        sl = order[k * 96:(k + 1) * 96]
        dec.append({'decile_rang': k + 1,
                    'mediane_flux': round(float(np.median(x[sl])), 4),
                    'mediane_T': round(float(np.median(temps[sl])), 4)})
    profil = {'n': len(x), 'min': round(float(x.min()), 4),
              'max': round(float(x.max()), 4),
              'mediane': round(float(np.median(x)), 4),
              'spearman_vs_T': round(rho, 4),
              'medianes_par_bande_T': med_par_bande,
              'bandes_T': ['<2.0', '2.0-Tc', 'Tc-2.6', '>=2.6'],
              'deciles_rang': dec,
              'valeur_au_seuil_mc': s.get('controle_valeur_au_seuil_mc')}
    # --- scan global ---
    sc = pd.DataFrame(json.loads((d / 'pipeline_results.json').read_text(encoding='utf-8'))['scan_curve'])
    sc = sc.dropna(subset=['score'])
    pk = pd.read_csv(d / 'landscape_peaks.csv')
    scan = {'score_max': round(float(sc['score'].max()), 4),
            'argmax_pct': round(float(sc.loc[sc['score'].idxmax(), 'candidate']), 2),
            'n_pics_55': len(pk), 'n_pics_forts_90': int((pk['rel_au_max'] >= 0.90).sum()),
            'fortes_T': sorted(pk.loc[pk['rel_au_max'] >= 0.90, 'temperature_mediane'].unique().tolist())}
    # --- seuils propres ---
    pf = pd.read_csv(d / 'per_flux_thresholds.csv')
    propres = {r['flux']: {'pct': round(float(r['seuil_propre_pct']), 2),
                           'T': round(float(r['temperature_mediane_au_seuil']), 4),
                           'delta_T_vs_MC': round(float(r['temperature_mediane_au_seuil']) - t_mc, 4) if t_mc else None}
               for _, r in pf.iterrows()}
    # --- Q ---
    pr = json.loads((d / 'pipeline_results.json').read_text(encoding='utf-8'))
    q_moy = {k: (round(float(v), 3) if v is not None else None)
             for k, v in s.get('scores_moyens_par_Q', {}).items()}
    q_flux = {}
    for qkey in ('Q5_Actif_Receptif', 'Q6_Actif_Receptif_Echelle'):
        per = pr['scores'].get(qkey, {})
        agg = {}
        for col, v in per.items():
            f = col.rsplit('_', 2)[0]
            agg.setdefault(f, []).append(float(v))
        q_flux[qkey] = {f: round(float(np.mean(v)), 3) for f, v in sorted(agg.items())}
    # --- bruit ---
    nd = pr['noise_diagnostic']
    bruit_flux = []
    for fd in nd['all_flux_diagnostics']:
        drifts = [(k, v['drift_mean']) for k, v in (fd.get('estimator_drift') or {}).items()
                  if isinstance(v, dict) and v.get('drift_mean') is not None]
        drifts.sort(key=lambda kv: kv[1], reverse=True)
        bruit_flux.append({'flux': fd['flux_name'],
                           'variance_proxy_score': round(float(fd['variance_proxy_score']), 3),
                           'drift_mediane': round(float(np.median([v for _, v in drifts])), 2) if drifts else None,
                           'drift_max_estimateur': drifts[0][0] if drifts else None,
                           'drift_max': round(float(drifts[0][1]), 2) if drifts else None})
    bruit = {'label': nd.get('diagnostic_label'),
             'proxy_moyen': round(float(nd['avg_variance_proxy_score']), 3),
             'proxy_max': round(float(nd['max_variance_proxy_score']), 3),
             'par_flux': bruit_flux}
    # --- F1/F2 ---
    f1 = pd.read_csv(d / 'transition_F1F2.csv') if (d / 'transition_F1F2.csv').exists() else pd.DataFrame()
    f1f2 = {}
    if len(f1):
        for flux, g in f1.groupby('flux'):
            ch = g[g['sign_change'] == True] if 'sign_change' in g else g.iloc[0:0]
            f1f2[flux] = {'n_estimateurs': len(g),
                          'n_sign_change': int(len(ch)),
                          'details': [{'estimateur': r['estimateur'],
                                       'F1_pre': (round(float(r['F1_pre']), 3) if pd.notna(r['F1_pre']) else None),
                                       'F1': (round(float(r['F1']), 3) if pd.notna(r['F1']) else None),
                                       'F2_pre': (round(float(r['F2_pre']), 3) if pd.notna(r['F2_pre']) else None),
                                       'F2': (round(float(r['F2']), 3) if pd.notna(r['F2']) else None)}
                                      for _, r in ch.iterrows()]}
    return {'controle': c, 'lot': runs_dir, 'statut': 'OK',
            'famille': fam_of(c), 'base': base_of(c),
            'seuil_mc_pct': round(float(s['mc_threshold_pct']), 2),
            'score_mc': round(float(s['mc_score']), 4),
            'stabilite': s.get('stability_rating'),
            'stab_moyenne': s.get('stability_mean'), 'stab_std': s.get('stability_std'),
            'temp_mc': round(float(t_mc), 4) if t_mc is not None else None,
            'classe_T': ('bande_Tc' if t_mc and abs(t_mc - TC) <= 0.07 else
                         ('onset_avant' if t_mc and t_mc <= TC - 0.20 else 'autre')),
            'profil_controle': profil, 'scan': scan,
            'seuils_propres': propres, 'Q_moyens': q_moy, 'Q5_Q6_par_flux': q_flux,
            'bruit': bruit, 'F1F2': f1f2,
            'n_F1F2_total': int(s.get('n_F1F2') or 0)}


all_runs = {}
for runs_dir, ctrls in RUNS.items():
    for c in ctrls:
        all_runs[c] = dossier(runs_dir, c)
ok = {c: r for c, r in all_runs.items() if r.get('statut') == 'OK'}

# --- témoins ---
for c, r in ok.items():
    temoins = {}
    cp = counterpart(c)
    if cp and cp in ok:
        temoins['meme_base_autre_construction'] = {
            'controle': cp, 'famille': ok[cp]['famille'],
            'seuil_mc_pct': ok[cp]['seuil_mc_pct'], 'score_mc': ok[cp]['score_mc'],
            'temp_mc': ok[cp]['temp_mc'],
            'situation': situe(r['temp_mc'], ok[cp]['temp_mc'])}
    for other in ok:
        if other == c or fam_of(other) != r['famille'] or base_of(other) == r['base']:
            continue
        temoins.setdefault('meme_famille_autres_bases', []).append(
            {'controle': other, 'base': base_of(other),
             'seuil_mc_pct': ok[other]['seuil_mc_pct'], 'score_mc': ok[other]['score_mc'],
             'temp_mc': ok[other]['temp_mc'],
             'situation': situe(r['temp_mc'], ok[other]['temp_mc'])})
    for other in ok:
        if other == c or fam_of(other) == r['famille'] or fam_of(other) == 'nul':
            continue
        if base_of(other) == r['base']:
            temoins.setdefault('autre_famille_meme_base', []).append(
                {'controle': other, 'famille': ok[other]['famille'],
                 'seuil_mc_pct': ok[other]['seuil_mc_pct'], 'score_mc': ok[other]['score_mc'],
                 'temp_mc': ok[other]['temp_mc'],
                 'situation': situe(r['temp_mc'], ok[other]['temp_mc'])})
    r['temoins'] = temoins

out = {'runs': all_runs, 'n_ok': len(ok), 'Tc_Onsager': TC}
(BASE / 'diagnostic_runs_ext.json').write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"DOSSIERS OK : {len(ok)}/{len(all_runs)}")
for c, r in all_runs.items():
    if r.get('statut') == 'OK':
        print(c, r['famille'], r['seuil_mc_pct'], r['score_mc'], r['stabilite'],
              'T', r['temp_mc'], r['classe_T'],
              '| bruit', r['bruit']['label'], r['bruit']['proxy_moyen'],
              '| F1F2 sign_change', sum(v['n_sign_change'] for v in r['F1F2'].values()))
    else:
        print(c, r['statut'])
