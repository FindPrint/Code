# -*- coding: utf-8 -*-
import json, glob
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
BASE=Path('/home/hatch/workspace/earthquake-tsunami-v33fixed')
df=pd.read_csv(BASE/'data'/'earthquake_data_tsunami.csv')
cols=list(df.columns)
# plateaux
plat=[]
for c in cols:
    s=df[c].dropna(); vals=s.values; prog=100*stats.rankdata(vals)/len(vals)
    for v in sorted(set(vals)):
        plat.append({'controle':c,'valeur':v,'n':int((vals==v).sum()),'progress_plateau_pct':round(float(prog[vals==v].mean()),2)})
pd.DataFrame(plat).to_csv(BASE/'plateaux_controles.csv',index=False)
# synthese runs + per flux + F1F2
S=[]; PF=[]; F=[]
for p in sorted(glob.glob(str(BASE/'results'/'ctrl_*'/'run_summary.json'))):
    s=json.load(open(p)); c=s['control']
    if s['status']=='OK':
        pf=s.get('per_flux') or []
        ths=np.array([r['seuil_propre_pct'] for r in pf]); scs=np.array([r['score_max'] for r in pf if r['flux']!='ca'])
        near=int(np.sum(np.abs(ths-(s['mc_threshold_pct'] or 0))<=5))
        cv=s.get('controle_valeur_au_seuil_mc') or {}
        S.append({'controle':c,'statut':'OK','n_lignes':s['n_pts'],'n_valides_controle':s['n_valides_controle'],
          'seuil_MC_pct':round(s['mc_threshold_pct'],2),'seuil_defaut_pct':round(s['default_threshold_pct'],2),
          'seuil_MC_brut_pct':round(s['raw_mc_threshold_pct'],2),'seuil_defaut_brut_pct':round(s['raw_default_threshold_pct'],2),
          'seuil_rigide1001_pct':s['rigid_1001_threshold_pct'],
          'ecart_MC_moins_defaut':round(s['mc_threshold_pct']-s['default_threshold_pct'],2),
          'stabilite':s['stability_rating'],'stabilite_moy_pct':round(s['stability_mean'],2) if s['stability_mean'] else None,'stabilite_std':round(s['stability_std'],2),
          'score_MC':round(s['mc_score'],3),'w_MC':s['mc_w_size'],'n_candidats_MC':s['mc_n_candidates'],
          'scan_global_max':s.get('scan_max_score'),'scan_argmax_pct':s.get('scan_argmax_pct'),
          'valeur_controle_au_MC_mediane':cv.get('mediane'),
          'flux_propres_mediane_pct':round(float(np.median(ths)),2),'flux_propres_IQR_pct':round(float(np.percentile(ths,75)-np.percentile(ths,25)),2),
          'n_flux_a_pm5pts_du_MC':near,'score_propre_max':round(float(scs.max()),3) if len(scs) else None,
          'bruit':s.get('noise_label'),'duree_s':s['duration_s']})
        for r in pf: PF.append({'controle':c,**r})
        f=pd.read_csv(BASE/'results'/f'ctrl_{c}'/'transition_F1F2.csv'); f.insert(0,'controle',c); F.append(f)
    else:
        S.append({'controle':c,'statut':'ECHEC','n_lignes':None,'n_valides_controle':s['n_valides_controle'],
          'seuil_MC_pct':None,'seuil_defaut_pct':None,'seuil_MC_brut_pct':None,'seuil_defaut_brut_pct':None,'seuil_rigide1001_pct':None,
          'ecart_MC_moins_defaut':None,'stabilite':None,'stabilite_moy_pct':None,'stabilite_std':None,'score_MC':None,'w_MC':None,
          'n_candidats_MC':None,'scan_global_max':None,'scan_argmax_pct':None,'valeur_controle_au_MC_mediane':None,
          'flux_propres_mediane_pct':None,'flux_propres_IQR_pct':None,'n_flux_a_pm5pts_du_MC':None,'score_propre_max':None,
          'bruit':s.get('error'),'duree_s':s['duration_s']})
order={c:i for i,c in enumerate(cols)}
S=pd.DataFrame(S); S['o']=S.controle.map(order); S=S.sort_values('o').drop(columns='o')
S.to_csv(BASE/'synthese_runs.csv',index=False)
PF=pd.DataFrame(PF); PF['o']=PF.controle.map(order); PF=PF.sort_values(['o','flux']).drop(columns='o')
PF.to_csv(BASE/'tous_seuils_par_flux.csv',index=False)
pd.concat(F).to_csv(BASE/'tous_F1F2.csv',index=False)
print(S.to_string(index=False))
print("\nF1F2 'Tous' par run :")
FF=pd.concat(F); tous=FF[FF.flux=='Tous']
print(tous.pivot_table(index='controle',columns='estimateur',values='F1').round(4).to_string())
# recurrence: en tant que flux, score propre moyen/max par colonne
g=PF.groupby('flux')['score_max'].agg(['mean','max','count']).round(3).sort_values('mean',ascending=False)
print("\nScores propres en tant que flux (moy/max sur les runs ou la colonne est flux) :"); print(g.to_string())
