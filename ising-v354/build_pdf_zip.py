# -*- coding: utf-8 -*-
"""Figures de synthèse + PDF + zip du lot ising-v354.
Sorties : figures/fig_S1_temperatures.png, figures/fig_S2_scan_curves.png,
Ising_v354_v35H1_Resultats_complets.pdf, ising_v354_resultats.zip
(zip = arbre complet hors __pycache__, hors PDF et hors zip lui-même).
"""
import json
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

BASE = Path('/home/hatch/workspace/ising-v354')
CONTROLS = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar',
            'susceptibility']
TC = 2.269185314213
FIG = BASE / 'figures'
FIG.mkdir(exist_ok=True)

summ = {}
for c in CONTROLS:
    summ[c] = json.loads((BASE / 'runs' / c / 'run_summary.json').read_text(encoding='utf-8'))

# ---------- Figure S1 : températures au seuil MC ----------
plt.figure(figsize=(10, 5.2))
xs = np.arange(len(CONTROLS))
temps = [summ[c]['temperature_mediane_au_seuil_mc'] for c in CONTROLS]
scores = [summ[c]['mc_score'] for c in CONTROLS]
plt.axhline(TC, color='red', linestyle='--', linewidth=1.2, label='Tc Onsager = 2,2692')
grid_t = np.linspace(1.7, 3.3, 24)
for t in grid_t:
    plt.axhline(t, color='grey', alpha=0.15, linewidth=0.6)
plt.scatter(xs, temps, s=90, color='navy', zorder=3)
for x, t, s in zip(xs, temps, scores):
    plt.annotate(f'{t:.4f}\nscore {s:.3f}', (x, t), textcoords='offset points',
                 xytext=(0, 12), ha='center', fontsize=8)
plt.xticks(xs, CONTROLS)
plt.ylabel('Température médiane au seuil MC')
plt.ylim(2.0, 2.45)
plt.title('Seuil Monte Carlo traduit en température, par contrôle (v3.5.4-H1)')
plt.legend()
plt.tight_layout()
plt.savefig(FIG / 'fig_S1_temperatures.png', dpi=150)
plt.close()

# ---------- Figure S2 : courbes de scan superposées ----------
plt.figure(figsize=(10, 6))
for c in CONTROLS:
    sc = pd.read_csv(BASE / 'runs' / c / 'scan_curve.csv').dropna(subset=['score']).sort_values('candidate')
    plt.plot(sc['candidate'], sc['score'], linewidth=1.0, label=c)
    plt.axvline(summ[c]['mc_threshold_pct'], color='grey', alpha=0.4, linewidth=0.8)
plt.xlabel('Candidat seuil (% du rang du contrôle)')
plt.ylabel('Score de séparation')
plt.title('Courbes de scan (seuil traité, défaut) — 6 contrôles, plateau haut')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIG / 'fig_S2_scan_curves.png', dpi=150)
plt.close()
print('figures OK')

# ---------- PDF ----------
styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=15, spaceBefore=14, spaceAfter=6)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, leading=14)
SMALL = ParagraphStyle('Small', parent=styles['BodyText'], fontSize=8.5, leading=11)


def P(t, style=BODY):
    return Paragraph(t, style)


def tbl(data, widths, fs=8.5):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', fs),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', fs),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.drawString(2 * cm, 1.1 * cm, 'Ising classique 2D × v3.5.4-H1 (Q6-A) — 28 oct. 2026 — dépôt privé FindPrint/Code')
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f'Page {doc.page}')
    canvas.restoreState()


story = []
story.append(P('Ising classique 2D × pipeline v3.5.4-H1 (Q6-A)', H1))
story.append(P('Lot ising-v354 — 28 octobre 2026. Synthèse vérifiée. Protocole gelé avant exécution (PROTOCOLE.md). Provenance complète (PROVENANCE.md). Pipeline SHA-256 <i>b54fcf66…</i>. Données SHA-256 <i>9027dfd5…</i>, températures <i>4863b1de…</i>.', SMALL))
story.append(P('Verdict', H1))
story.append(P('<b>6/6 runs OK, 0 échec, 0 avertissement, 0 repli.</b> Sur une simulation physique à transition connue (Tc d’Onsager = 2,2692), le pipeline désigne la même frontière physique depuis chaque lentille : 5 contrôles sur 6 traduisent leur seuil Monte Carlo à <b>T = 2,2565</b> (ΔT = −0,013, un pas de grille sous Tc), scores MC 0,736–0,762, stabilités bootstrap VERY STABLE (moyennes à 0,14–1,36 point du seuil MC). L’exception est le contrôle <i>susceptibility</i> (T = 2,1174, ΔT = −0,152), biaisée par sa construction (fenêtre expansive à mémoire). <i>flip</i> et <i>fliprate</i> sont bit-identiques, comme leur proportionnalité exacte l’exigeait.'))
story.append(P('C’est la validation la plus forte de l’instrument sur un système à vérité terrain connue : le banc Ashkin-Teller était un générateur d’agent, celui-ci est une simulation physique avec un Tc exact. Réserves : calibration de Q6-A, plateau des courbes de scan, taille unique L = 32 — elles ne retirent rien à la convergence observée.', BODY))
story.append(P('Données et protocole', H1))
story.append(P('Générateur <i>gen_ising_classic_v354.py</i> (SHA 24069e4e…), adapté de <i>gen_ising_proxy.py</i>. L = 32, J = 1, limites périodiques, Metropolis checkerboard, graine 42, T = linspace(1,7, 3,3, 24), 1 500 sweeps d’équilibration, 40 snapshots par T, GAP 50. 960 lignes × 6 flux (<i>fliprate, flip, energy, magnetization, localvar, susceptibility</i>), 0 NaN. Température en CSV séparé, jamais lu par le pipeline. Portes P1–P4 passées : chute de |m| entre T = 2,2565 et 2,3957 (Tc encadré), Spearman(T, énergie) = 1,0, pic de χ à T = 2,3261 (écart 0,057). Mode stable, w80, cohen_d, graine 42, HARMONIC_PROB 0,45, Theiler 1/φ planché (source fixe). Contrôle exclu des flux. Max 2 runs en parallèle. Lot total 6 min 38 s, 123–128 s par run.', BODY))
story.append(P('Seuils Monte Carlo par contrôle', H1))
hdr = ['Contrôle', 'Seuil MC %', 'Score', 'Défaut %', 'Stabilité', 'Moy. ± std', 'T au seuil', 'ΔT vs Tc']
rows = [hdr]
for c in CONTROLS:
    s = summ[c]
    rows.append([c, f"{s['mc_threshold_pct']:.2f}", f"{s['mc_score']:.4f}", f"{s['default_threshold_pct']:.2f}",
                 s['stability_rating'], f"{s['stability_mean']:.2f} ± {s['stability_std']:.2f}",
                 f"{s['temperature_mediane_au_seuil_mc']:.4f}", f"{s['temperature_mediane_au_seuil_mc'] - TC:+.4f}"])
story.append(tbl(rows, [3.0 * cm, 2.0 * cm, 1.6 * cm, 1.8 * cm, 2.6 * cm, 2.6 * cm, 1.9 * cm, 1.9 * cm]))
story.append(P('Configurations MC retenues : règle <i>uniform</i> dans les 6 runs, w_size 100 ou 118, n_candidates 605–790, min_grp 5–9. Source : <i>monte_carlo</i> partout. Le rigide-1001 et le MC brut coïncident avec le MC retenu à ≤ 0,35 point : la coupure est dans les données, pas dans l’optimiseur.', BODY))
story.append(Image(str(FIG / 'fig_S1_temperatures.png'), width=17 * cm, height=8.84 * cm))
story.append(P('Figure S1 — Température médiane au seuil MC par contrôle. Ligne rouge : Tc d’Onsager. Cinq contrôles tombent sur le même pas de grille (2,2565).', SMALL))
story.append(Image(str(FIG / 'fig_S2_scan_curves.png'), width=17 * cm, height=10.2 * cm))
story.append(P('Figure S2 — Courbes de scan superposées (traits gris : seuils MC). Plateau haut : le pourcentage exact est mou (±3 points), la bande de température est robuste.', SMALL))
story.append(P('Seuils propres par flux (% puis températures)', H1))
pf = {}
for c in CONTROLS:
    d = pd.read_csv(BASE / 'runs' / c / 'per_flux_thresholds.csv')
    for _, r in d.iterrows():
        pf.setdefault(r['flux'], {})[c] = (float(r['seuil_propre_pct']), float(r['temperature_mediane_au_seuil']))
fluxes = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar', 'susceptibility']
for kind, idx in (('Seuils propres (%)', 0), ('Températures médianes', 1)):
    story.append(P(kind, H2))
    data = [['Flux \\ Contrôle'] + CONTROLS]
    for f in fluxes:
        data.append([f] + [('—' if f == c else f'{pf[f][c][idx]:.2f}' if idx == 0 else f'{pf[f][c][idx]:.4f}') for c in CONTROLS])
    story.append(tbl(data, [2.9 * cm] + [2.37 * cm] * 6, fs=8))
story.append(P('20 des 30 seuils propres traduisent T = 2,2565 ou 2,3261 (les deux pas de grille qui encadrent Tc). Le flux <i>susceptibility</i> a un seuil propre invariant (25,22 %, T = 2,1174) sous les 5 contrôles.', BODY))
story.append(P('Questions Q1–Q6 (moyennes par run)', H1))
hdr = ['Contrôle', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6-A']
rows = [hdr]
qkeys = {'Q1': 'Q1_Calme_vs_Chaos', 'Q2': 'Q2_Tension_Seuil', 'Q3': 'Q3_Agressivite',
         'Q4': 'Q4_Persistence', 'Q5': 'Q5_Active_Reactive', 'Q6': 'Q6_Active_Reactive_Scaled'}
for c in CONTROLS:
    q = summ[c]['scores_moyens_par_Q']
    rows.append([c] + [f"{q[qkeys[k]]:.3f}" for k in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']])
story.append(tbl(rows, [3.2 * cm] + [2.36 * cm] * 6))
story.append(P('Q1 = Q3 dans chaque run (fait déjà observé au pilote v3.5). Q6-A fonctionne mécaniquement mais ses magnitudes (51–248) ne sont pas comparables à Q5 (6–9) : la référence moyenne mise à l’échelle est très lisse, ce qui gonfle le d de Cohen. Lecture intra-Q6 uniquement ; calibration non établie par un seul lot.', BODY))
story.append(P('Analyse', H1))
story.append(P('<b>Convergence.</b> Cinq lentilles désignent la même température à un pas de grille près, scores MC serrés (0,758–0,762), bootstraps d’accord (0,14–1,36 point — contre 97,69 points pour <i>odor</i> sur mushroom). Bandes à ≥ 95 % du maximum : 6 à 13 points de %.', BODY))
story.append(P('<b>Exception <i>susceptibility</i>.</b> Fenêtre expansive intra-bloc : χ repart de 0 à chaque bloc et croît — 24 dents de scie. Rangs distordus dès la construction, seuil 0,07–0,15 trop bas, score de scan le plus faible (max 2,66, médiane 1,00). Biais nommé : un flux cumulatif ne doit pas servir de contrôle sans mention. Comme flux analysé, il reste informatif (dérive la plus forte).', BODY))
story.append(P('<b>F1/F2.</b> 174 lignes par run (29 estimateurs × 5 flux + « Tous ») ; changements de signe 105–131 (60–75 %). « Tous » : 25/29 (run fliprate). Réfractaires : famille des dimensions (TwoNN, LevinaBickel, DANCo, Fisher, D2/GP, InformationD1, GraphDimension, homologie) + SingularityFmax (saturée à 1,000) + KolmogorovLZ/MFA. Non tranché : insensibilité réelle ou saturation.', BODY))
story.append(P('<b>Bruit et dérive.</b> Proxy de variance modéré (5 runs), coloré CSD (magnetization) ; scores moyens 0,727–0,813. Dérives standardisées au bruit blanc : médianes 1,4–8,5, aucune référence dégénérée ; χ dérive le plus (7,5–8,5, max 44–54 via PermutationEntropy) ; PCAIntrinsic porte le max ailleurs (15–26).', BODY))
story.append(P('<b>Données continues.</b> NaN dans df_feat : 0 % pour 25 estimateurs ; Spectral 6,7 %, Lyapunov 2,0 %, TwoNN 2,7 % — contre 32 %/21 %/20 % sur mushroom. La métastabilité liée aux liens exacts ne se déclenche presque pas ici.', BODY))
story.append(P('Opinion', H1))
story.append(P('Le pipeline fait, sur ce test, ce qu’il prétend faire : trouver une coupure qui influence le système, depuis chaque lentille indépendamment. Ne pas sur-vendre : (1) Q6-A sort des nombres, pas encore une échelle ; (2) le % est mou, la bande de température est la mesure ; (3) une seule taille, une seule graine — l’écart −0,013 peut être un effet de taille finie. Suite logique : L = 64 + seconde graine, puis réel-vs-nul loupe par loupe, χ gardée comme flux analysé.', BODY))
story.append(P('Limites et fichiers', H1))
story.append(P('L = 32 fini ; χ par fenêtre expansive ; <i>flip</i>/<i>fliprate</i> exactement proportionnels (vérifié bit-identique) ; contrôles lus en rangs ; une seule graine ; pas de champ ; pas d’étude en taille finie. Lecture descriptive sur données simulées. Fichiers : PROTOCOLE.md, PROVENANCE.md, RAPPORT.md, synthese.json, gen_ising_classic_v354.py, data/ (2 CSV), run_one_ising.py, run_lot.sh, synthese.py, runs/&lt;contrôle&gt;/ (11 fichiers par run), figures/. Hachages : §8 de RAPPORT.md.', BODY))
story.append(PageBreak())
story.append(P('Figures du pipeline (par contrôle)', H1))
for c in CONTROLS:
    story.append(P(f'Contrôle : {c} — seuil MC {summ[c]["mc_threshold_pct"]:.2f} %, score {summ[c]["mc_score"]:.4f}, T = {summ[c]["temperature_mediane_au_seuil_mc"]:.4f}', H2))
    story.append(Image(str(BASE / 'runs' / c / 'threshold_scan.png'), width=16 * cm, height=9.6 * cm))
    story.append(Image(str(BASE / 'runs' / c / 'noise_diagnostic.png'), width=16 * cm, height=9.6 * cm))

pdf_path = BASE / 'Ising_v354_v35H1_Resultats_complets.pdf'
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title='Ising classique 2D × v3.5.4-H1 — Résultats complets',
                        author='TagPrint (Muse) pour Zackary Drasse-Ménard')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF OK :', pdf_path)

# ---------- ZIP ----------
zip_path = BASE / 'ising_v354_resultats.zip'
import hashlib
exclude_dirs = {'__pycache__'}
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(BASE.rglob('*')):
        if p.is_dir() or p.name == zip_path.name or p.name == pdf_path.name:
            continue
        if any(part in exclude_dirs for part in p.parts):
            continue
        z.write(p, p.relative_to(BASE).as_posix())
print('ZIP OK :', zip_path)
print('SHA-256 PDF :', hashlib.sha256(pdf_path.read_bytes()).hexdigest())
print('SHA-256 ZIP :', hashlib.sha256(zip_path.read_bytes()).hexdigest())
import os
print('Tailles : PDF %.1f Mo, ZIP %.1f Mo' % (pdf_path.stat().st_size / 1e6, zip_path.stat().st_size / 1e6))
