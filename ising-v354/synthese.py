# -*- coding: utf-8 -*-
"""Synthèse vérifiée du lot ising-v354 (6 runs en rotation).
Lit run_summary.json + per_flux_thresholds.csv + landscape_peaks.csv +
transition_F1F2.csv de chaque run. Tolère les runs manquants (marqués
EN COURS) pour tester le script avant la fin du lot. Recalcule
indépendamment la traduction température du seuil MC et vérifie
l'exclusion du contrôle + l'identité flip/fliprate.
Sortie : synthese.json + tableau imprimé.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

BASE = Path('/home/hatch/workspace/ising-v354')
CONTROLS = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar',
            'susceptibility']
TC = 2.269185314213

df = pd.read_csv(BASE / 'data' / 'ising_classic_v354.csv')
temps = pd.read_csv(BASE / 'data' / 'ising_classic_v354_temperature.csv')['temperature'].values
assert len(temps) == len(df)


def temp_au_seuil(control, pct):
    vals = df[control].values
    order = np.argsort(vals, kind='stable')
    n = len(vals)
    k = float(pct) / 100.0 * n
    lo = max(0, int(k - 0.015 * n))
    hi = min(n, int(k + 0.015 * n))
    return float(np.median(temps[order[lo:hi]]))


rows = []
mat_pct = {}
mat_temp = {}
checks = []
for c in CONTROLS:
    d = BASE / 'runs' / c
    sj = d / 'run_summary.json'
    if not sj.exists():
        rows.append({'controle': c, 'statut': 'EN COURS'})
        continue
    s = json.loads(sj.read_text(encoding='utf-8'))
    if s.get('status') != 'OK':
        rows.append({'controle': c, 'statut': s.get('status'),
                     'erreur': s.get('error')})
        continue
    # Exclusion du contrôle : les flux analysés ne doivent pas le contenir.
    assert c not in s['fluxes_analyses'], f'contrôle {c} présent dans les flux !'
    assert len(s['fluxes_analyses']) == 5
    # Traduction température recalculée indépendamment.
    t_recalc = temp_au_seuil(c, s['mc_threshold_pct'])
    t_harness = s.get('temperature_mediane_au_seuil_mc')
    checks.append({'controle': c, 'temp_harness': t_harness,
                   'temp_recalculee': round(t_recalc, 4),
                   'ecart': abs(t_harness - t_recalc) if t_harness is not None else None})
    # Le harnais arrondit à 4 décimales : tolérance 1e-4, pas 1e-9.
    assert t_harness is None or abs(t_harness - t_recalc) < 1e-4
    pf = pd.read_csv(d / 'per_flux_thresholds.csv')
    assert list(pf['flux']) == s['fluxes_analyses'] or set(pf['flux']) == set(s['fluxes_analyses'])
    for _, r in pf.iterrows():
        mat_pct.setdefault(r['flux'], {})[c] = float(r['seuil_propre_pct'])
        mat_temp.setdefault(r['flux'], {})[c] = float(r['temperature_mediane_au_seuil'])
    f1f2 = pd.read_csv(d / 'transition_F1F2.csv') if (d / 'transition_F1F2.csv').exists() else pd.DataFrame()
    rows.append({
        'controle': c, 'statut': 'OK',
        'seuil_mc_pct': round(float(s['mc_threshold_pct']), 4),
        'score_mc': round(float(s['mc_score']), 4),
        'seuil_defaut_pct': round(float(s['default_threshold_pct']), 4) if s.get('default_threshold_pct') is not None else None,
        'seuil_mc_brut_pct': round(float(s['raw_mc_threshold_pct']), 4) if s.get('raw_mc_threshold_pct') is not None else None,
        'rigid_1001_pct': round(float(s['rigid_1001_threshold_pct']), 4) if s.get('rigid_1001_threshold_pct') is not None else None,
        'stabilite': s.get('stability_rating'),
        'stab_moyenne': round(float(s['stability_mean']), 4) if s.get('stability_mean') is not None else None,
        'stab_std': round(float(s['stability_std']), 4) if s.get('stability_std') is not None else None,
        'duree_s': s.get('duration_s'),
        'temp_mc': round(float(t_harness), 4) if t_harness is not None else None,
        'delta_T_vs_Tc': round(float(t_harness) - TC, 4) if t_harness is not None else None,
        'bruit': s.get('noise_label'),
        'n_pics_paysage': len(s.get('landscape_peaks') or []),
        'scan_argmax_pct': s.get('scan_argmax_pct'),
        'temp_argmax': s.get('temperature_mediane_au_argmax'),
        'n_F1F2': s.get('n_F1F2'),
        'theiler': s.get('theiler'),
        'Q_moyens': s.get('scores_moyens_par_Q'),
        'seuils_propres': {r['flux']: round(float(r['seuil_propre_pct']), 2) for _, r in pf.iterrows()},
    })

# Identité flip / fliprate (proportionnalité exacte -> mêmes seuils/scores).
done = {r['controle']: r for r in rows if r.get('statut') == 'OK'}
if 'flip' in done and 'fliprate' in done:
    a, b = done['flip'], done['fliprate']
    ident = (a['seuil_mc_pct'] == b['seuil_mc_pct'] and a['score_mc'] == b['score_mc'])
    print('IDENTITÉ flip/fliprate (seuil+score MC) :', ident,
          a['seuil_mc_pct'], a['score_mc'])
    checks.append({'controle': 'flip_vs_fliprate', 'identiques': bool(ident)})

out = {'controles': rows, 'matrice_seuils_propres_pct': mat_pct,
       'matrice_temperatures_seuils_propres': mat_temp,
       'verifications': checks, 'Tc_Onsager': TC,
       'n_termines': sum(1 for r in rows if r.get('statut') == 'OK')}
(BASE / 'synthese.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(pd.DataFrame(rows).to_string(index=False))
print('\nMATRICE seuils propres (%) : lignes=flux, colonnes=contrôle')
print(pd.DataFrame(mat_pct).to_string())
print('\nMATRICE températures médianes aux seuils propres')
print(pd.DataFrame(mat_temp).to_string())
print('\nVÉRIFICATIONS :', json.dumps(checks, ensure_ascii=False))
print('TERMINÉS : %d/6' % out['n_termines'])
