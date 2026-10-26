# -*- coding: utf-8 -*-
import json, glob
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
BASE=Path('/home/hatch/workspace/food-costs-2013')
df=pd.read_csv(BASE/'data'/'Food_Costs_2013_pipeline.csv')
# ordre d'affichage = ordre du fichier d'origine
order_cols=['agency_encoded']+[c for c in df.columns if c.startswith('2012') or c.startswith('2013-')]+['Cumulative Cost']
label_of={
 'ctrl_Agency':'agency_encoded',
 'ctrl_2012-10':'2012-10-01 00:00:00','ctrl_2012-11':'2012-11-01 00:00:00','ctrl_2012-12':'2012-12-01 00:00:00',
 'ctrl_2013-01':'2013-01-01 00:00:00','ctrl_2013-02':'2013-02-01 00:00:00','ctrl_2013-03':'2013-03-01 00:00:00',
 'ctrl_2013-04':'2013-04-01 00:00:00','ctrl_2013-05':'2013-05-01 00:00:00','ctrl_2013-06':'2013-06-01 00:00:00',
 'ctrl_2013-07':'2013-07-01 00:00:00','ctrl_2013-08':'2013-08-01 00:00:00','ctrl_2013-09':'2013-09-01 00:00:00',
 'ctrl_Cumulative':'Cumulative Cost'}
# plateaux (valeurs repetees)
plat=[]
for c in order_cols:
    s=df[c].dropna(); vals=s.values; prog=100*stats.rankdata(vals, method='average')/len(vals)
    for v in sorted(set(vals)):
        n=int((vals==v).sum())
        if n>1:
            plat.append({'controle':c,'valeur':v,'n':n,'progress_plateau_pct':round(float(prog[vals==v].mean()),2)})
pd.DataFrame(plat).to_csv(BASE/'plateaux_controles.csv',index=False)
# synthese runs + per flux + F1F2
S=[]; PF=[]; F=[]
for dirname, c in label_of.items():
    p=BASE/'results'/dirname/'run_summary.json'
    s=json.load(open(p))
    assert s['control']==c, (dirname, s['control'], c)
    if s['status']=='OK':
        pf=s.get('per_flux') or []
        ths=np.array([r['seuil_propre_pct'] for r in pf]); scs=np.array([r['score_max'] for r in pf])
        near=int(np.sum(np.abs(ths-(s['mc_threshold_pct'] or 0))<=5))
        cv=s.get('controle_valeur_au_seuil_mc') or {}
        S.append({'controle':c,'label':dirname.replace('ctrl_',''),'statut':'OK','n_lignes':s['n_pts'],'n_valides_controle':s['n_valides_controle'],
          'seuil_MC_pct':round(s['mc_threshold_pct'],2),'seuil_defaut_pct':round(s['default_threshold_pct'],2),
          'seuil_MC_brut_pct':round(s['raw_mc_threshold_pct'],2),'seuil_defaut_brut_pct':round(s['raw_default_threshold_pct'],2),
          'seuil_rigide1001_pct':s['rigid_1001_threshold_pct'],
          'ecart_MC_moins_defaut':round(s['mc_threshold_pct']-s['default_threshold_pct'],2),
          'ecart_MC_moins_moybootstrap':round(s['mc_threshold_pct']-s['stability_mean'],2) if s.get('stability_mean') else None,
          'stabilite':s['stability_rating'],'stabilite_moy_pct':round(s['stability_mean'],2) if s['stability_mean'] else None,'stabilite_std':round(s['stability_std'],6) if s.get('stability_std') is not None else None,
          'score_MC':round(s['mc_score'],3),'w_MC':s['mc_w_size'],'n_candidats_MC':s['mc_n_candidates'],
          'scan_global_max':s.get('scan_max_score'),'scan_argmax_pct':s.get('scan_argmax_pct'),
          'valeur_controle_au_MC_mediane':cv.get('mediane'),
          'flux_propres_mediane_pct':round(float(np.median(ths)),2),'flux_propres_IQR_pct':round(float(np.percentile(ths,75)-np.percentile(ths,25)),2),
          'n_flux_a_pm5pts_du_MC':near,'score_propre_max':round(float(scs.max()),3) if len(scs) else None,
          'score_propre_median':round(float(np.median(scs)),3) if len(scs) else None,
          'bruit':s.get('noise_label'),'duree_s':s['duration_s']})
        for r in pf: PF.append({'controle':c,'label':dirname.replace('ctrl_',''),**r})
        f=pd.read_csv(BASE/'results'/dirname/'transition_F1F2.csv'); f.insert(0,'controle',c); f.insert(1,'label',dirname.replace('ctrl_','')); F.append(f)
    else:
        S.append({'controle':c,'label':dirname.replace('ctrl_',''),'statut':'ECHEC','n_lignes':None,'n_valides_controle':s['n_valides_controle'],
          'seuil_MC_pct':None,'seuil_defaut_pct':None,'seuil_MC_brut_pct':None,'seuil_defaut_brut_pct':None,'seuil_rigide1001_pct':None,
          'ecart_MC_moins_defaut':None,'ecart_MC_moins_moybootstrap':None,'stabilite':None,'stabilite_moy_pct':None,'stabilite_std':None,'score_MC':None,'w_MC':None,
          'n_candidats_MC':None,'scan_global_max':None,'scan_argmax_pct':None,'valeur_controle_au_MC_mediane':None,
          'flux_propres_mediane_pct':None,'flux_propres_IQR_pct':None,'n_flux_a_pm5pts_du_MC':None,'score_propre_max':None,'score_propre_median':None,
          'bruit':s.get('error'),'duree_s':s['duration_s']})
order={c:i for i,c in enumerate(order_cols)}
S=pd.DataFrame(S); S['o']=S.controle.map(order); S=S.sort_values('o').drop(columns='o')
S.to_csv(BASE/'synthese_runs.csv',index=False)
PF=pd.DataFrame(PF); PF['o']=PF.controle.map(order); PF=PF.sort_values(['o','flux']).drop(columns='o')
PF.to_csv(BASE/'tous_seuils_par_flux.csv',index=False)
pd.concat(F).to_csv(BASE/'tous_F1F2.csv',index=False)
print(S.to_string(index=False))
print("\nTotal duree:", S.duree_s.sum(), "s ; n F1F2:", sum(len(x) for x in F), "n per_flux:", len(PF))
print("\nScores propres en tant que flux (moy/max) :")
g=PF.groupby('flux')['score_max'].agg(['mean','max','count']).round(3).sort_values('mean',ascending=False)
print(g.to_string())
print("\nSeuils propres en tant que flux (mediane/IQR) :")
g2=PF.groupby('flux')['seuil_propre_pct'].agg(['median',lambda x: np.percentile(x,75)-np.percentile(x,25),'min','max']).round(2)
print(g2.to_string())
# top agences par controle + verification Mountain Plains
tops=[]
for c in order_cols:
    if c=='agency_encoded': continue
    s=df.dropna(subset=[c]).sort_values(c, ascending=False)
    top11=list(s.iloc[:11,0]); v11=s.iloc[10][c]; v12=s.iloc[11][c]
    tops.append({'controle':c,'top11':'; '.join(top11),'valeur_11e':v11,'valeur_12e':v12,'part_top11_cumul':None})
pd.DataFrame(tops).to_csv(BASE/'top11_par_controle.csv',index=False)
mountain_states=['Colorado','Iowa','Kansas','Missouri','Montana','Nebraska','North Dakota','South Dakota','Utah','Wyoming']
tribal_mountain=['Ute Mountain Ute Tribe, CO','Omaha Sioux, NE','Santee Sioux, NE','Winnebago Tribe, NE','Standing Rock Sioux Tribe, ND','Three Affiliated Tribes, ND','Cheyenne River Sioux, SD','Rosebud Sioux, SD','Northern Arapahoe, WY','Shoshone Tribe, WY']
comp=df[df.iloc[:,0].isin(mountain_states+tribal_mountain)]['Cumulative Cost'].sum()
mp=float(df[df.iloc[:,0]=='Mountain Plains']['Cumulative Cost'].iloc[0])
print(f"\nMountain Plains: ligne={mp:,.0f} somme composantes (10 Etats + 10 tribus)={comp:,.0f} ecart={mp-comp:,.0f}")
print("Plateaux (valeurs repetees):", plat)
