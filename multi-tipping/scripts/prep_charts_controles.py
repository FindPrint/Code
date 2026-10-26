# -*- coding: utf-8 -*-
"""Figures de synthèse pour le PDF contrôles (données sources uniquement)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

B = Path('/home/hatch/workspace/multi-tipping')
OUT = B / 'pdf_build_controles'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3})
R = pd.read_csv(B / 'controles/synthese_globaux.csv')
PF = pd.read_csv(B / 'controles/synthese_par_flux.csv')
AT = ['at', 'at_s7', 'at_s123', 'at_L36']
AT_CTRLS = ['magnetization_s', 'magnetization_tau', 'magnetization_prod',
            'energy', 'flip_rate', 'local_variance']
SHORT = {'magnetization_s': 'm_s', 'magnetization_tau': 'm_tau',
         'magnetization_prod': 'm_prod', 'energy': 'energy',
         'flip_rate': 'flip', 'local_variance': 'loc_var',
         'magnetization': 'mag', 'vortex_density': 'vortex'}

# 1) Globaux AT : T mappée par contrôle et par jeu
fig, ax = plt.subplots(figsize=(10, 5.0))
ax.axhspan(4.6, 4.9, color='green', alpha=0.12, label='T1 [4,6 ; 4,9]')
ax.axhspan(5.2, 5.6, color='orange', alpha=0.12, label='T2 [5,2 ; 5,6]')
for ds in AT:
    sub = R[R.dataset == ds]
    xs = [AT_CTRLS.index(c) for c in sub['control']]
    ax.scatter(xs, sub['global_T'], s=70, label=ds)
ax.set_xticks(range(len(AT_CTRLS)))
ax.set_xticklabels([SHORT[c] for c in AT_CTRLS])
ax.set_ylabel('Température mappée du seuil global')
ax.set_title('AT — seuil global mappé, par contrôle et par jeu (harmonique v1)')
ax.legend(fontsize=8, ncol=3)
fig.tight_layout(); fig.savefig(OUT / 'chart_ctrl_global_AT.png', dpi=150); plt.close(fig)

# 2) Globaux horloge
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.axhspan(0.62, 0.80, color='green', alpha=0.12, label='T1 [0,62 ; 0,80]')
ax.axhspan(0.82, 0.98, color='orange', alpha=0.12, label='T2 [0,82 ; 0,98]')
sub = R[R.dataset == 'clock']
ax.scatter(range(len(sub)), sub['global_T'], s=90, color='darkred')
ax.set_xticks(range(len(sub)))
ax.set_xticklabels([SHORT[c] for c in sub['control']])
ax.set_ylabel('Température mappée du seuil global')
ax.set_title('Horloge q=6 — seuil global mappé, par contrôle (aucun hit)')
fig.tight_layout(); fig.savefig(OUT / 'chart_ctrl_global_clock.png', dpi=150); plt.close(fig)

# 3) Moyennes des T propres par contrôle (AT)
pf = PF[PF.dataset.isin(AT)]
means = pf.groupby(['control', 'flux'])['T'].mean().unstack()
fig, ax = plt.subplots(figsize=(10, 5.0))
ax.axhspan(4.6, 4.9, color='green', alpha=0.10)
ax.axhspan(5.2, 5.6, color='orange', alpha=0.10)
for flux in ['magnetization_s', 'magnetization_tau', 'magnetization_prod', 'flip_rate', 'local_variance', 'energy']:
    if flux in means.columns:
        ax.plot([AT_CTRLS.index(c) for c in means.index], means[flux],
                marker='o', label=SHORT.get(flux, flux))
ax.set_xticks(range(len(AT_CTRLS)))
ax.set_xticklabels([SHORT[c] for c in AT_CTRLS])
ax.set_ylabel('T propre moyenne (4 jeux AT)')
ax.set_title('AT — T propre moyenne de chaque flux, selon le contrôle')
ax.legend(fontsize=8, ncol=3)
fig.tight_layout(); fig.savefig(OUT / 'chart_perflux_mean.png', dpi=150); plt.close(fig)
print('Figures écrites dans', OUT)
