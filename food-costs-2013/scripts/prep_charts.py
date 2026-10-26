# -*- coding: utf-8 -*-
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
BASE=Path('/home/hatch/workspace/food-costs-2013')
FIG=BASE/'figures'; FIG.mkdir(exist_ok=True)
syn=pd.read_csv(BASE/'synthese_runs.csv')
PF=pd.read_csv(BASE/'tous_seuils_par_flux.csv')
labels={'agency_encoded':'Agency','Cumulative Cost':'Cumulative'}
def short(c):
    if c in labels: return labels[c]
    return c[:7]  # YYYY-MM
syn['short']=syn.controle.map(short)
# 1. MC vs bootstrap mean
fig,ax=plt.subplots(figsize=(10,4.2))
x=np.arange(len(syn))
ax.bar(x, syn.seuil_MC_pct, color='#1a3a5c', label='Seuil MC')
ax.scatter(x, syn.stabilite_moy_pct, color='#c0392b', marker='D', s=45, label='Moyenne bootstrap')
ax.scatter(x, syn.seuil_defaut_pct, color='#e67e22', marker='x', s=60, label='Seuil par defaut')
ax.set_xticks(x); ax.set_xticklabels(syn.short, rotation=45, ha='right', fontsize=8)
ax.set_ylabel('% de rang'); ax.set_ylim(0,100); ax.legend(fontsize=8); ax.grid(axis='y', alpha=.3)
ax.set_title('Food_Costs 2013 : seuil MC, seuil par defaut et moyenne bootstrap, par controle')
fig.tight_layout(); fig.savefig(FIG/'seuils_MC_vs_bootstrap.png', dpi=200); plt.close(fig)
# 2. scan curves overlay
fig,ax=plt.subplots(figsize=(10,4.5))
DIR={'agency_encoded':'ctrl_Agency','Cumulative Cost':'ctrl_Cumulative'}
for c in syn.controle:
    d=DIR.get(c)
    if d is None:
        d='ctrl_'+c[:7]
    sc=pd.read_csv(BASE/'results'/d/'scan_curve.csv').dropna()
    if c=='agency_encoded':
        ax.plot(sc.candidate, sc.score, color='#c0392b', lw=2, label='Agency (controle)')
    elif c=='Cumulative Cost':
        ax.plot(sc.candidate, sc.score, color='#1a3a5c', lw=2, label='Cumulative Cost')
    else:
        ax.plot(sc.candidate, sc.score, color='#7f8c8d', lw=0.7, alpha=.6)
ax.axvline(87.88, color='#1a3a5c', ls='--', lw=1, label='MC 87,88 % (controles numeriques)')
ax.set_xlabel('Candidat (% de rang)'); ax.set_ylabel('Score de scan'); ax.grid(alpha=.3); ax.legend(fontsize=8)
ax.set_title('Courbes de scan globales : montee reguliere vers 87,88 %, sans pic interieur')
fig.tight_layout(); fig.savefig(FIG/'scan_curves_overlay.png', dpi=200); plt.close(fig)
# 3. mean per-flux score
g=PF.groupby('flux')['score_max'].mean().sort_values(ascending=False)
g.index=[short(c) for c in g.index]
fig,ax=plt.subplots(figsize=(10,4.2))
ax.bar(g.index, g.values, color=['#c0392b' if i=='Agency' else '#1a3a5c' for i in g.index])
ax.set_ylabel('Score propre moyen'); ax.set_xticklabels(g.index, rotation=45, ha='right', fontsize=8); ax.grid(axis='y', alpha=.3)
ax.set_title('En tant que flux : score propre moyen (13 runs ou la colonne est flux)')
fig.tight_layout(); fig.savefig(FIG/'scores_propres_moyens.png', dpi=200); plt.close(fig)
# 4. sorted cumulative, log scale, cut after top 11
df=pd.read_csv(BASE/'data'/'Food_Costs_2013_pipeline.csv')
s=df.dropna(subset=['Cumulative Cost']).sort_values('Cumulative Cost', ascending=False).reset_index(drop=True)
fig,ax=plt.subplots(figsize=(10,4.5))
ax.plot(np.arange(1,len(s)+1), s['Cumulative Cost'], marker='.', ms=4, color='#1a3a5c')
ax.set_yscale('log'); ax.axvline(12.5, color='#c0392b', ls='--', lw=1.5, label='Coupure MC : apres les 12 plus grandes')
ax.set_xlabel('Rang decroissant (1 = California, la plus grande)'); ax.set_ylabel('Cumulative Cost (echelle log)')
ax.grid(alpha=.3, which='both'); ax.legend(fontsize=8)
ax.set_title('Cumulative Cost 2013 triee : les 12 premieres = 62,6 % du total du fichier')
fig.tight_layout(); fig.savefig(FIG/'cumulative_triee_log.png', dpi=200); plt.close(fig)
print("charts:", sorted(p.name for p in FIG.iterdir()))
