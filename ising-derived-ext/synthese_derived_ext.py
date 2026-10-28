# -*- coding: utf-8 -*-
"""Synthèse + attribution du lot dérivés EXT, règles R1-R5 gelées
(PROTOCOLE_DERIVED_EXT.md). Lit runs_ext/ (12 runs) + runs/ du lot 1
(11 runs, paysages poolés : 7 nuls pour R3, 16 runs dérivés pour R1).
R2 généralisée : paires expansive<->glissante (expvar<->rollvar,
expmean<->rollmean), même base ; non applicable sous contrôle glissant.
Sortie : synthese_derived_ext.json + tableaux imprimés.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path('/home/hatch/workspace/ising-derived')
NEW_CONTROLS = ['expmean_fliprate', 'expmean_localvar', 'rollvar_fliprate_40',
                'rollvar_localvar_40', 'rollmean_energy_40',
                'rollmean_magnetization_40', 'rollmean_fliprate_40',
                'rollmean_localvar_40', 'null_expmean_fliprate',
                'null_rollvar_fliprate', 'null_rollmean_mag',
                'null_rollmean_localvar']
LOT1_CONTROLS = ['expvar_energy', 'expvar_magnetization', 'expvar_fliprate',
                 'expvar_localvar', 'expmean_energy', 'expmean_magnetization',
                 'rollvar_magnetization_40', 'rollvar_energy_40',
                 'null_susceptibility', 'null_expvar_mag', 'null_rollvar_mag']
ORIGINALS = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar',
             'susceptibility']
TC = 2.269185314213
EXT_SHA = 'bae505d4c5e5e0f4faff2571515b872c67eb01545ebb367ff1203735cded34b4'

df = pd.read_csv(BASE / 'data' / 'ising_derived_ext.csv')
temps = pd.read_csv(BASE / 'data' / 'ising_classic_v354_temperature.csv')['temperature'].values
assert len(temps) == len(df)
import hashlib
assert hashlib.sha256((BASE / 'data' / 'ising_derived_ext.csv').read_bytes()).hexdigest() == EXT_SHA


def temp_au_seuil(control, pct):
    order = np.argsort(df[control].values, kind='stable')
    n = len(df)
    k = float(pct) / 100.0 * n
    lo = max(0, int(k - 0.015 * n))
    hi = min(n, int(k + 0.015 * n))
    return float(np.median(temps[order[lo:hi]]))


def clusters(temps_uniques, t_mc, seuil_sep=0.20):
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


def base_of(control):
    for prefix in ('expvar_', 'expmean_', 'rollvar_', 'rollmean_'):
        if control.startswith(prefix):
            b = control[len(prefix):]
            return b[:-3] if b.endswith('_40') else b
    return None


def rolling_counterpart(control):
    b = base_of(control)
    if control.startswith('expvar_'):
        return f'rollvar_{b}_40'
    if control.startswith('expmean_'):
        return f'rollmean_{b}_40'
    return None


def read_run(runs_dir, c):
    d = BASE / runs_dir / c
    sj = d / 'run_summary.json'
    if not sj.exists():
        return {'controle': c, 'statut': 'EN COURS'}
    s = json.loads(sj.read_text(encoding='utf-8'))
    if s.get('status') != 'OK':
        return {'controle': c, 'statut': s.get('status'), 'erreur': s.get('error')}
    assert s['fluxes_analyses'] == ORIGINALS and c not in ORIGINALS
    # Famille : les champs famille/construction des run_summary.json sont
    # VIDES (bug du lot : tableaux associatifs bash non exportés aux
    # sous-shells xargs — métadonnée uniquement, les runs ne sont pas
    # affectés). On la re-dérive du préfixe du nom, jamais du champ vide.
    if c.startswith('null_'):
        fam = 'nul'
    elif c.startswith('expvar_'):
        fam = 'expvar'
    elif c.startswith('expmean_'):
        fam = 'expmean'
    elif c.startswith('rollvar_'):
        fam = 'rollvar'
    elif c.startswith('rollmean_'):
        fam = 'rollmean'
    else:
        fam = s.get('famille') or 'inconnu'
    t_mc = s.get('temperature_mediane_au_seuil_mc')
    if runs_dir == 'runs_ext':
        t_recalc = temp_au_seuil(c, s['mc_threshold_pct'])
        assert t_mc is None or abs(t_mc - t_recalc) < 1e-4
    pk = pd.read_csv(d / 'landscape_peaks.csv')
    fort = pk[pk['rel_au_max'] >= 0.90]
    fortes = sorted(fort['temperature_mediane'].unique().tolist())
    groups, cl = clusters(fortes, t_mc)
    pf = pd.read_csv(d / 'per_flux_thresholds.csv')
    mat_pct, mat_temp = {}, {}
    for _, r in pf.iterrows():
        mat_pct[r['flux']] = float(r['seuil_propre_pct'])
        mat_temp[r['flux']] = float(r['temperature_mediane_au_seuil'])
    f1 = pd.read_csv(d / 'transition_F1F2.csv') if (d / 'transition_F1F2.csv').exists() else pd.DataFrame()
    pr = json.loads((d / 'pipeline_results.json').read_text(encoding='utf-8'))
    drifts = []
    for fd in pr['noise_diagnostic']['all_flux_diagnostics']:
        dm = [v['drift_mean'] for v in (fd.get('estimator_drift') or {}).values()
              if isinstance(v, dict) and v.get('drift_mean') is not None]
        drifts.append(float(np.median(dm)) if dm else None)
    return {
        'controle': c, 'statut': 'OK', 'famille': fam,
        'lot': runs_dir,
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
        'fortes': fortes,
        'groupes_pics_forts': groups, 'groupe_principal': cl['principal'],
        'candidats_secondaires': cl['candidats_secondaires'],
        'scan_argmax_pct': s.get('scan_argmax_pct'),
        'n_F1F2': s.get('n_F1F2'),
        'F1F2_sign_change': int(f1['sign_change'].sum()) if len(f1) and 'sign_change' in f1 else None,
        'Q_moyens': s.get('scores_moyens_par_Q'),
        'mat_pct': mat_pct, 'mat_temp': mat_temp,
    }


rows = [read_run('runs_ext', c) for c in NEW_CONTROLS]
lot1 = [read_run('runs', c) for c in LOT1_CONTROLS]
done = {r['controle']: r for r in rows + lot1 if r.get('statut') == 'OK'}
null_names = [c for c in NEW_CONTROLS + LOT1_CONTROLS if c.startswith('null_')]
nuls = {c: done[c]['fortes'] for c in null_names if c in done}
derived = {c: r for c, r in done.items() if r.get('famille') != 'nul'}

candidats = {}
for c, r in derived.items():
    for cand in r.get('candidats_secondaires', []):
        key = tuple(cand['temps'])
        candidats.setdefault(key, {'runs': [], 'temps': cand['temps']})
        candidats[key]['runs'].append(c)
attribution = []
for key, v in candidats.items():
    ts = v['temps']
    dans_nuls = [nc for nc, nt in nuls.items()
                 if any(min(abs(t - u) for u in nt) <= 0.0696 for t in ts)]
    roll_checks = {}
    for rc_run in v['runs']:
        cp = rolling_counterpart(rc_run)
        if cp is None:
            roll_checks[rc_run] = None
        elif cp in done:
            roll_checks[rc_run] = any(min(abs(t - u) for u in done[cp]['fortes']) <= 0.0696 for t in ts)
        else:
            roll_checks[rc_run] = 'EN COURS'
    attribution.append({
        'temps_candidats': ts, 'runs_derives': v['runs'],
        'n_runs_derives': len(v['runs']),
        'present_dans_nuls': dans_nuls,
        'present_sous_glissant_meme_base': roll_checks,
        'verdict_R1': len(v['runs']) >= 2 and not dans_nuls,
        'verdict_R2_construction': any(vv is False for vv in roll_checks.values()),
        'verdict_R3_pipeline': bool(dans_nuls),
    })

mat_pct = {r['controle']: r['mat_pct'] for r in rows if r.get('statut') == 'OK'}
mat_temp = {r['controle']: r['mat_temp'] for r in rows if r.get('statut') == 'OK'}
out = {'controles': rows, 'lot1_controles': lot1,
       'matrice_seuils_propres_pct': mat_pct,
       'matrice_temperatures_seuils_propres': mat_temp,
       'pics_forts_par_run': {c: r['fortes'] for c, r in done.items()},
       'attribution_candidats': attribution,
       'Tc_Onsager': TC, 'n_termines': sum(1 for r in rows if r.get('statut') == 'OK')}
(BASE / 'synthese_derived_ext.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(pd.DataFrame([{k: r.get(k) for k in ['controle', 'statut', 'famille', 'seuil_mc_pct', 'score_mc', 'stabilite', 'temp_mc', 'delta_T_vs_Tc', 'n_pics_forts', 'groupe_principal', 'candidats_secondaires']} for r in rows]).to_string(index=False))
print('\nATTRIBUTION :', json.dumps(attribution, ensure_ascii=False, indent=1))
print('TERMINÉS (ext) : %d/12' % out['n_termines'])
