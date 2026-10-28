# -*- coding: utf-8 -*-
"""Synthèse + attribution du lot dérivés, règles R1-R5 gelées (PROTOCOLE_DERIVED.md).
Lit run_summary.json + landscape_peaks.csv + per_flux_thresholds.csv +
transition_F1F2.csv + pipeline_results.json (bruit/dérive) des 11 runs.
Tolère les runs manquants (EN COURS).
R1 : groupe de pics forts (rel>=0,90) séparé de >=0,20 du groupe principal,
  présent dans >=2 runs dérivés, absent des nuls correspondants.
R2 : présent sous expvar/expmean, absent sous rollvar (même base) -> construction.
R3 : présent dans un nul à la même T -> pipeline.
R4 : survit à R1+R2+R3 -> candidat réel (à confirmer L=64 + 2e graine).
Sortie : synthese_derived.json + tableaux imprimés.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path('/home/hatch/workspace/ising-derived')
CONTROLS = ['expvar_energy', 'expvar_magnetization', 'expvar_fliprate',
            'expvar_localvar', 'expmean_energy', 'expmean_magnetization',
            'rollvar_magnetization_40', 'rollvar_energy_40',
            'null_susceptibility', 'null_expvar_mag', 'null_rollvar_mag']
ORIGINALS = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar',
             'susceptibility']
TC = 2.269185314213

df = pd.read_csv(BASE / 'data' / 'ising_derived.csv')
temps = pd.read_csv(BASE / 'data' / 'ising_classic_v354_temperature.csv')['temperature'].values
assert len(temps) == len(df)


def temp_au_seuil(control, pct):
    order = np.argsort(df[control].values, kind='stable')
    n = len(df)
    k = float(pct) / 100.0 * n
    lo = max(0, int(k - 0.015 * n))
    hi = min(n, int(k + 0.015 * n))
    return float(np.median(temps[order[lo:hi]]))


def clusters(temps_uniques, t_mc, seuil_sep=0.20):
    """Groupes de T séparés par >2 pas de grille (0,1391) ; groupe principal
    = celui qui contient (ou est le plus proche de) T@MC."""
    u = sorted(set(round(float(t), 4) for t in temps_uniques))
    if not u:
        return [], None
    groups, cur = [], [u[0]]
    for t in u[1:]:
        if t - cur[-1] > 0.1391:
            groups.append(cur)
            cur = [t]
        else:
            cur.append(t)
    groups.append(cur)
    main = min(groups, key=lambda g: min(abs(t - t_mc) for t in g))
    others = []
    for g in groups:
        if g is main:
            continue
        dmin = min(abs(a - b) for a in g for b in main)
        if dmin >= seuil_sep:
            others.append({'temps': g, 'distance_groupe_principal': round(dmin, 4)})
    return groups, {'principal': main, 'candidats_secondaires': others}


rows, fortes, mat_pct, mat_temp = [], {}, {}, {}
for c in CONTROLS:
    d = BASE / 'runs' / c
    sj = d / 'run_summary.json'
    if not sj.exists():
        rows.append({'controle': c, 'statut': 'EN COURS'})
        continue
    s = json.loads(sj.read_text(encoding='utf-8'))
    if s.get('status') != 'OK':
        rows.append({'controle': c, 'statut': s.get('status'), 'erreur': s.get('error')})
        continue
    assert s['fluxes_analyses'] == ORIGINALS and c not in ORIGINALS
    t_mc = s.get('temperature_mediane_au_seuil_mc')
    t_recalc = temp_au_seuil(c, s['mc_threshold_pct'])
    assert t_mc is None or abs(t_mc - t_recalc) < 1e-4
    pk = pd.read_csv(d / 'landscape_peaks.csv')
    fort = pk[pk['rel_au_max'] >= 0.90]
    fortes[c] = sorted(fort['temperature_mediane'].unique().tolist())
    groups, cl = clusters(fortes[c], t_mc)
    pf = pd.read_csv(d / 'per_flux_thresholds.csv')
    for _, r in pf.iterrows():
        mat_pct.setdefault(r['flux'], {})[c] = float(r['seuil_propre_pct'])
        mat_temp.setdefault(r['flux'], {})[c] = float(r['temperature_mediane_au_seuil'])
    f1 = pd.read_csv(d / 'transition_F1F2.csv') if (d / 'transition_F1F2.csv').exists() else pd.DataFrame()
    pr = json.loads((d / 'pipeline_results.json').read_text(encoding='utf-8'))
    drifts = []
    for fd in pr['noise_diagnostic']['all_flux_diagnostics']:
        dm = [v['drift_mean'] for v in (fd.get('estimator_drift') or {}).values()
              if isinstance(v, dict) and v.get('drift_mean') is not None]
        drifts.append(float(np.median(dm)) if dm else None)
    rows.append({
        'controle': c, 'statut': 'OK', 'famille': s.get('famille'),
        'seuil_mc_pct': round(float(s['mc_threshold_pct']), 2),
        'score_mc': round(float(s['mc_score']), 4),
        'seuil_defaut_pct': round(float(s['default_threshold_pct']), 2) if s.get('default_threshold_pct') is not None else None,
        'stabilite': s.get('stability_rating'),
        'stab_moyenne': round(float(s['stability_mean']), 2) if s.get('stability_mean') is not None else None,
        'stab_std': round(float(s['stability_std']), 2) if s.get('stability_std') is not None else None,
        'duree_s': s.get('duration_s'),
        'temp_mc': round(float(t_mc), 4) if t_mc is not None else None,
        'delta_T_vs_Tc': round(float(t_mc) - TC, 4) if t_mc is not None else None,
        'bruit': s.get('noise_label'),
        'drift_mediane_flux': [round(x, 2) if x is not None else None for x in drifts],
        'n_pics': len(pk), 'n_pics_forts': len(fort),
        'groupes_pics_forts': groups, 'groupe_principal': cl['principal'],
        'candidats_secondaires': cl['candidats_secondaires'],
        'scan_argmax_pct': s.get('scan_argmax_pct'),
        'n_F1F2': s.get('n_F1F2'),
        'F1F2_sign_change': int(f1['sign_change'].sum()) if len(f1) and 'sign_change' in f1 else None,
        'Q_moyens': s.get('scores_moyens_par_Q'),
    })

# --- Attribution croisée R1/R2/R3 (sur les runs terminés) ---
done = {r['controle']: r for r in rows if r.get('statut') == 'OK'}
nuls = {c: fortes[c] for c in ['null_susceptibility', 'null_expvar_mag', 'null_rollvar_mag'] if c in fortes}
candidats = {}
for c, r in done.items():
    if r.get('famille') == 'nul':
        continue
    for cand in r.get('candidats_secondaires', []):
        key = tuple(cand['temps'])
        candidats.setdefault(key, {'runs': [], 'temps': cand['temps']})
        candidats[key]['runs'].append(c)
attribution = []
for key, v in candidats.items():
    ts = v['temps']
    dans_nuls = [nc for nc, nt in nuls.items()
                 if any(min(abs(t - u) for u in nt) <= 0.0696 for t in ts)]
    base = None
    if 'magnetization' in '_'.join(v['runs']):
        base = 'magnetization'
    elif 'energy' in '_'.join(v['runs']):
        base = 'energy'
    roll_present = None
    if base:
        rc = f'rollvar_{base}_40'
        if rc in fortes:
            roll_present = any(min(abs(t - u) for u in fortes[rc]) <= 0.0696 for t in ts)
    attribution.append({
        'temps_candidats': ts, 'runs_derives': v['runs'],
        'n_runs_derives': len(v['runs']),
        'present_dans_nuls': dans_nuls,
        'present_sous_rollvar_meme_base': roll_present,
        'verdict_R1': len(v['runs']) >= 2 and not dans_nuls,
        'verdict_R2_construction': (roll_present is False),
        'verdict_R3_pipeline': bool(dans_nuls),
    })

out = {'controles': rows, 'matrice_seuils_propres_pct': mat_pct,
       'matrice_temperatures_seuils_propres': mat_temp,
       'pics_forts_par_run': fortes, 'attribution_candidats': attribution,
       'Tc_Onsager': TC, 'n_termines': sum(1 for r in rows if r.get('statut') == 'OK')}
(BASE / 'synthese_derived.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(pd.DataFrame([{k: r.get(k) for k in ['controle', 'statut', 'famille', 'seuil_mc_pct', 'score_mc', 'stabilite', 'temp_mc', 'delta_T_vs_Tc', 'n_pics_forts', 'groupe_principal', 'candidats_secondaires']} for r in rows]).to_string(index=False))
print('\nATTRIBUTION :', json.dumps(attribution, ensure_ascii=False, indent=1))
print('TERMINÉS : %d/11' % out['n_termines'])
