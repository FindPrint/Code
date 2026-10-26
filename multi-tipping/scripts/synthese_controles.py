# -*- coding: utf-8 -*-
"""Synthèse du lot contrôles (35 runs, harmonique v1) contre les critères gelés.
Lit tous les verdict.json + run_summary.json, imprime les tables et sauve
controles/synthese.json (utilisé par le rapport et le PDF)."""
import json
from pathlib import Path
import pandas as pd

B = Path('/home/hatch/workspace/multi-tipping')
C = B / 'controles'
AT = ['at', 'at_s7', 'at_s123', 'at_L36']
AT_CTRLS = ['magnetization_s', 'magnetization_tau', 'magnetization_prod',
            'energy', 'flip_rate', 'local_variance']
CLOCK_CTRLS = ['magnetization', 'energy', 'flip_rate', 'vortex_density', 'local_variance']
EXPECTED = {'energy': 'T1', 'magnetization_s': 'T1', 'magnetization_tau': 'T1',
            'magnetization_prod': 'T2', 'flip_rate': 'T2', 'local_variance': None}
OWN = {'magnetization_s': 'T1', 'magnetization_tau': 'T1', 'magnetization_prod': 'T2',
       'flip_rate': 'T2'}

rows, pfrows = [], []
for ds in AT + ['clock', 'null2']:
    ctrls = CLOCK_CTRLS if ds == 'clock' else AT_CTRLS
    for ctrl in ctrls:
        od = C / ds / ctrl
        v = json.load(open(od / 'verdict.json'))
        s = json.load(open(od / 'run_summary.json'))
        rows.append({'dataset': ds, 'control': ctrl, 'global_pct': v['global_mc_pct'],
                     'global_T': v['global_mc_T'][0], 'global_Tstd': v['global_mc_T'][1],
                     'global_hit': v['global_hit_T'], 'stabilite': v['stabilite'],
                     'stab_std': v['stabilite_std'], 'mc_score': v['mc_score'],
                     'spearman': v['spearman_control_T'],
                     'duree_s': s['duration_s'], 'mc_w': s['mc_w_size'],
                     'max_scan': v['paysage_zones']['max_global']})
        for f in v['per_flux']:
            pfrows.append({'dataset': ds, 'control': ctrl, 'flux': f['flux'],
                           'pct': f['seuil_propre_pct'], 'score': f['score_max'],
                           'T': f['T_estime'], 'Tstd': f['T_std'], 'hit': f['hit_T']})
R = pd.DataFrame(rows)
PF = pd.DataFrame(pfrows)
R.to_csv(C / 'synthese_globaux.csv', index=False)
PF.to_csv(C / 'synthese_par_flux.csv', index=False)

print('=== GLOBAUX AT (T mappée, hit) ===')
print(R[R.dataset.isin(AT)][['dataset', 'control', 'global_pct', 'global_T', 'global_hit', 'stabilite', 'spearman']].to_string(index=False))
print('\n=== GLOBAUX HORLOGE ===')
print(R[R.dataset == 'clock'][['control', 'global_pct', 'global_T', 'global_hit', 'stabilite', 'spearman']].to_string(index=False))
print('\n=== GLOBAUX NUL B2 ===')
print(R[R.dataset == 'null2'][['control', 'global_pct', 'stabilite', 'stab_std', 'mc_score', 'max_scan']].to_string(index=False))

print('\n=== Attendus globaux AT (contrôle -> T attendue) ===')
sub = R[R.dataset.isin(AT)].copy()
sub['attendu'] = sub['control'].map(EXPECTED)
ok = sub[sub.attendu.notna()]
print(f"hits attendus : {(ok.global_hit == ok.attendu).sum()}/{len(ok)}")
print('détail des écarts :')
print(ok[ok.global_hit != ok.attendu][['dataset', 'control', 'global_T', 'global_hit', 'attendu']].to_string(index=False))

print('\n=== Par flux AT : le flux pointe-t-il vers SA transition ? (m_s/m_tau->T1, m_prod/flip->T2) ===')
pf = PF[PF.dataset.isin(AT)].copy()
pf['attendu'] = pf['flux'].map(OWN)
pf2 = pf[pf.attendu.notna()]
for flux, g in pf2.groupby('flux'):
    print(f"{flux}: {(g.hit == g.attendu).sum()}/{len(g)} vers {g.attendu.iloc[0]} "
          f"(T1:{(g.hit=='T1').sum()}, T2:{(g.hit=='T2').sum()}, hors:{(g.hit=='hors').sum()})")
print('\nlocal_variance (aucune attente) :', pf[pf.flux == 'local_variance']['hit'].value_counts().to_dict())
print('energy comme flux (n’existe plus : contrôle exclu) :', len(pf[pf.flux == 'energy']), 'lignes (attendu 0)')

print('\n=== Horloge par flux ===')
pfc = PF[PF.dataset == 'clock']
for flux, g in pfc.groupby('flux'):
    print(f"{flux}: T1:{(g.hit=='T1').sum()}/5, T2:{(g.hit=='T2').sum()}/5, hors:{(g.hit=='hors').sum()}/5, "
          f"T={sorted([t for t in g['T'] if t is not None])}")

print('\n=== Nul B2 par flux : scores ===')
pfn = PF[PF.dataset == 'null2']
print('score max par run :', pfn.groupby('control')['score'].max().round(3).to_dict())
print('score moyen tous flux :', round(pfn['score'].mean(), 3))
pfr = PF[PF.dataset.isin(AT)]
print('score moyen tous flux AT réel :', round(pfr['score'].mean(), 3))
print('stabilité nul :', R[R.dataset == 'null2']['stabilite'].value_counts().to_dict())
print('stabilité AT réel :', R[R.dataset.isin(AT)]['stabilite'].value_counts().to_dict())
print('stabilité horloge :', R[R.dataset == 'clock']['stabilite'].value_counts().to_dict())

print('\n=== Spearman contrôle vs T ===')
print(R[['dataset', 'control', 'spearman']].to_string(index=False))
print('\nDurée totale runs (s) :', int(R['duree_s'].sum()), '| moyenne :', round(R['duree_s'].mean(), 1))
print('Scores MC globaux AT :', R[R.dataset.isin(AT)]['mc_score'].describe().round(3).to_dict())

json.dump({'globaux': R.to_dict('records'), 'par_flux': PF.to_dict('records')},
          open(C / 'synthese.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print('\nSynthèse sauvée dans controles/synthese.json')
