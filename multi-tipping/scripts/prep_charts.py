# -*- coding: utf-8 -*-
"""Figures de synthèse pour le PDF (données sources uniquement)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

B = Path('/home/hatch/workspace/multi-tipping')
OUT = B / 'pdf_build'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3})

# 1) Courbes de scan globales superposées (courbes "défaut, traitées" du pipeline)
fig, ax = plt.subplots(figsize=(10, 5.2))
series = [
    ('Vague 1 AT (L=28, g42)', B / 'results_at_v33/scan_curve.csv'),
    ('AT graine 7', B / 'vague2/at_s7/scan_curve.csv'),
    ('AT graine 123', B / 'vague2/at_s123/scan_curve.csv'),
    ('AT L=36', B / 'vague2/at_L36/scan_curve.csv'),
    ('Nul B2 (décorrélé)', B / 'vague2/null2/scan_curve.csv'),
    ('Horloge q=6', B / 'vague2/clock/scan_curve.csv'),
]
for label, path in series:
    c = pd.read_csv(path).dropna(subset=['score'])
    ax.plot(c['candidate'], c['score'], label=label, linewidth=1.4)
ax.axvspan(50, 60, color='green', alpha=0.10)
ax.axvspan(62, 73, color='orange', alpha=0.10)
ax.set_xlabel('Seuil candidat (% de l’axe de progression, rang d’énergie)')
ax.set_ylabel('Score de séparation (Cohen d)')
ax.set_title('Courbes de scan globales — zones vertes/oranges : fenêtres AT gelées (50–60 % / 62–73 %)')
ax.legend(fontsize=8, ncol=2)
fig.tight_layout()
fig.savefig(OUT / 'chart_scan_curves.png', dpi=150)
plt.close(fig)

# 2) AT principal : aimantations moyennes par température
d = pd.read_csv(B / 'at_dataset.csv')
g = d.groupby('temperature').mean(numeric_only=True)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
axes[0].plot(g.index, g['magnetization_s'], label='magnetization_s')
axes[0].plot(g.index, g['magnetization_prod'], label='magnetization_prod')
axes[0].axvspan(4.6, 4.9, color='green', alpha=0.12)
axes[0].axvspan(5.2, 5.6, color='orange', alpha=0.12)
axes[0].set_xlabel('Température T'); axes[0].set_ylabel('Aimantation moyenne')
axes[0].set_title('AT L=28, graine 42 — chutes des aimantations'); axes[0].legend(fontsize=8)
axes[1].plot(g.index, g['energy'], color='purple')
axes[1].set_xlabel('Température T'); axes[1].set_ylabel('Énergie par site')
axes[1].set_title('Énergie (contrôle) — monotone en T')
fig.tight_layout()
fig.savefig(OUT / 'chart_at_fluxes_T.png', dpi=150)
plt.close(fig)

# 3) Horloge q=6 : aimantation et densité de vortex par température
d = pd.read_csv(B / 'clock6_dataset.csv')
g = d.groupby('temperature').mean(numeric_only=True)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
axes[0].plot(g.index, g['magnetization'])
axes[0].axvline(0.70, color='green', linestyle='--'); axes[0].axvline(0.88, color='orange', linestyle='--')
axes[0].set_xlabel('Température T'); axes[0].set_ylabel('Aimantation')
axes[0].set_title('Horloge q=6 — aimantation (pointillés : T1=0,70 / T2=0,88 publiés)')
axes[1].plot(g.index, g['vortex_density'], color='darkred')
axes[1].axvline(0.70, color='green', linestyle='--'); axes[1].axvline(0.88, color='orange', linestyle='--')
axes[1].set_xlabel('Température T'); axes[1].set_ylabel('Densité de vortex')
axes[1].set_title('Horloge q=6 — densité de vortex')
fig.tight_layout()
fig.savefig(OUT / 'chart_clock_T.png', dpi=150)
plt.close(fig)

# 4) Vérification des données AT par jeu : moyennes par T autour des transitions
rows = []
for name, path in [('AT vague 1', B / 'at_dataset.csv'),
                   ('AT graine 7', B / 'vague2/data/at_s7_dataset.csv'),
                   ('AT graine 123', B / 'vague2/data/at_s123_dataset.csv'),
                   ('AT L=36', B / 'vague2/data/at_L36_dataset.csv')]:
    dd = pd.read_csv(path)
    gg = dd.groupby('temperature').mean(numeric_only=True)
    def val(col, t):
        return round(float(gg.loc[t, col]), 3) if t in gg.index else None
    rows.append({'jeu': name,
                 'm_s@4.6': val('magnetization_s', 4.6), 'm_s@4.9': val('magnetization_s', 4.9),
                 'm_prod@4.9': val('magnetization_prod', 4.9), 'm_prod@5.3': val('magnetization_prod', 5.3),
                 'm_prod@5.6': val('magnetization_prod', 5.6),
                 'm_s_passe_sous_0.4_a_T': round(float(gg.index[gg['magnetization_s'] < 0.4][0]), 2) if (gg['magnetization_s'] < 0.4).any() else None,
                 'm_prod_passe_sous_0.4_a_T': round(float(gg.index[gg['magnetization_prod'] < 0.4][0]), 2) if (gg['magnetization_prod'] < 0.4).any() else None})
pd.DataFrame(rows).to_csv(OUT / 'verification_AT.csv', index=False)
print(pd.DataFrame(rows).to_string())
print('Figures écrites dans', OUT)
