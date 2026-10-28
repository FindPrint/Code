# -*- coding: utf-8 -*-
"""Figures de synthèse + PDF + zip du lot ising-derived.
Sorties : figures/fig_S1_temperatures.png, figures/fig_S2_scan_curves.png,
Ising_derived_v35H1_Resultats_complets.pdf, ising_derived_resultats.zip
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

BASE = Path('/home/hatch/workspace/ising-derived')
DERIVED = ['expvar_energy', 'expvar_magnetization', 'expvar_fliprate',
           'expvar_localvar', 'expmean_energy', 'expmean_magnetization',
           'rollvar_magnetization_40', 'rollvar_energy_40']
NULLS = ['null_susceptibility', 'null_expvar_mag', 'null_rollvar_mag']
CONTROLS = DERIVED + NULLS
FAMILY = {c: 'expvar' for c in DERIVED[:4]}
FAMILY.update({c: 'expmean' for c in DERIVED[4:6]})
FAMILY.update({c: 'rollvar' for c in DERIVED[6:]})
FAMILY.update({c: 'nul' for c in NULLS})
COLORS = {'expvar': 'navy', 'expmean': 'darkgreen', 'rollvar': 'darkorange', 'nul': 'grey'}
TC = 2.269185314213
FIG = BASE / 'figures'
FIG.mkdir(exist_ok=True)

summ = {}
for c in CONTROLS:
    summ[c] = json.loads((BASE / 'runs' / c / 'run_summary.json').read_text(encoding='utf-8'))
synth = json.loads((BASE / 'synthese_derived.json').read_text(encoding='utf-8'))
by_ctrl = {r['controle']: r for r in synth['controles']}

# ---------- Figure S1 : températures au seuil MC, par famille ----------
plt.figure(figsize=(11, 5.6))
xs = np.arange(len(CONTROLS))
temps = [summ[c]['temperature_mediane_au_seuil_mc'] for c in CONTROLS]
scores = [summ[c]['mc_score'] for c in CONTROLS]
plt.axhline(TC, color='red', linestyle='--', linewidth=1.2, label='Tc Onsager = 2,2692')
for t in np.linspace(1.7, 3.3, 24):
    plt.axhline(t, color='grey', alpha=0.12, linewidth=0.6)
for x, t, s, c in zip(xs, temps, scores, CONTROLS):
    plt.scatter([x], [t], s=90, color=COLORS[FAMILY[c]], zorder=3)
    plt.annotate(f'{t:.4f}\nscore {s:.3f}', (x, t), textcoords='offset points',
                 xytext=(0, 12), ha='center', fontsize=7.5)
plt.xticks(xs, [c.replace('_', '\n') for c in CONTROLS], fontsize=7.5)
plt.ylabel('Température médiane au seuil MC')
plt.ylim(1.70, 2.75)
plt.title('Seuil Monte Carlo traduit en température, par contrôle (v3.5.4-H1) — 2 familles + nuls')
for fam, col in COLORS.items():
    plt.scatter([], [], color=col, label=fam)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIG / 'fig_S1_temperatures.png', dpi=150)
plt.close()

# ---------- Figure S2 : courbes de scan superposées ----------
plt.figure(figsize=(11, 6))
for c in CONTROLS:
    sc = pd.read_csv(BASE / 'runs' / c / 'scan_curve.csv').dropna(subset=['score']).sort_values('candidate')
    plt.plot(sc['candidate'], sc['score'], linewidth=1.0, label=c,
             color=COLORS[FAMILY[c]], alpha=0.85)
    plt.axvline(summ[c]['mc_threshold_pct'], color=COLORS[FAMILY[c]], alpha=0.3, linewidth=0.8)
plt.xlabel('Candidat seuil (% du rang du contrôle)')
plt.ylabel('Score de séparation')
plt.title('Courbes de scan — 8 contrôles dérivés + 3 nuls')
plt.legend(fontsize=7, ncol=2)
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
    canvas.drawString(2 * cm, 1.1 * cm, 'Ising dérivés × v3.5.4-H1 (Q6-A) — 28 oct. 2026 — dépôt privé FindPrint/Code')
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f'Page {doc.page}')
    canvas.restoreState()


story = []
story.append(P('Ising 2D : flux dérivés type susceptibility, témoins et nuls × v3.5.4-H1 (Q6-A)', H1))
story.append(P('Lot ising-derived — 28 octobre 2026. Synthèse vérifiée (synthese_derived.py). Protocole gelé avant construction et runs (PROTOCOLE_DERIVED.md). Provenance complète (PROVENANCE_DERIVED.md). Pipeline SHA-256 <i>b54fcf66…</i>. Données dérivées SHA-256 <i>10563d4d…</i>, températures <i>4863b1de…</i>. Le pipeline ne voit jamais T ni Tc ; traduction en T post-hoc dans le harnais ; comparaison à Tc descriptive.', SMALL))
story.append(P('Verdict', H1))
story.append(P('<b>11/11 runs OK, 0 échec, 0 avertissement, 0 repli. Pas de deuxième seuil critique.</b> Chacun des 8 runs dérivés n’a qu’une seule masse de pics forts. Deux familles de loupes : les contrôles de <b>variance</b> (expvar ×4 + rollvar ×2, avec ou sans mémoire expansive) placent le seuil à <b>T = 1,84–1,98</b> (ΔT −0,29 à −0,43), scores 0,672–0,824 — le pied du régime de fluctuations ; les contrôles de <b>moyenne expansive</b> (expmean ×2) retrouvent <b>T = 2,2565</b> (ΔT −0,013), scores 0,762–0,763 — le seuil du lot original. Le pic isolé à T = 2,6739 (un seul run) est un <b>artefact</b> : il échoue R1, apparaît dans 2 nuls (R3) et disparaît sous rollvar (R2). Les 3 <b>nuls</b> produisent quand même un seuil (scores 0,556–0,567, UNSTABLE, T dispersées) : c’est la calibration de ce que vaut un seuil sans signal.'))
story.append(P('Données et protocole', H1))
story.append(P('Données construites depuis <i>ising_classic_v354.csv</i> (960 lignes, SHA <i>9027dfd5…</i>) <b>sans aucune valeur de T</b> (constructeur <i>gen_derived.py</i>, SHA <i>f06aa42b…</i>, vérifié : une seule lecture CSV, la source). 6 originaux bit-identiques + 8 dérivés + 3 nuls, 960 lignes × 17 colonnes, 0 NaN. Blocs = 24 blocs de 40 lignes consécutives (position). <i>expvar</i> : variance expansive ddof=1 par bloc (k=0 → 0,0) ; <i>expmean</i> : moyenne expansive par bloc ; <i>rollvar_40</i> : variance glissante arrière, fenêtre 40, sans réinitialisation ; nuls : permutation <i>default_rng(1234)</i> de la série entière. Portes D1–D5 passées. Mode stable, w80, cohen_d, graine 42, HARMONIC_PROB 0,45, Theiler 1/φ planché (source fixe). Analysés fixés aux 6 originaux (χ incluse, jamais contrôle). Max 2 en parallèle. Lot total 17 min 34 s, 128–220 s par run.', BODY))
story.append(P('Seuils Monte Carlo par contrôle', H1))
hdr = ['Contrôle', 'Famille', 'Seuil MC %', 'Score', 'Règle', 'Stabilité', 'Moy. ± std', 'T au seuil', 'ΔT vs Tc']
rows = [hdr]
rules = {'expvar_energy': 'sqrt2'}
for c in CONTROLS:
    s = summ[c]
    rows.append([c, FAMILY[c], f"{s['mc_threshold_pct']:.2f}", f"{s['mc_score']:.4f}",
                 rules.get(c, 'uniform'), s['stability_rating'],
                 f"{s['stability_mean']:.2f} ± {s['stability_std']:.2f}",
                 f"{s['temperature_mediane_au_seuil_mc']:.4f}", f"{s['temperature_mediane_au_seuil_mc'] - TC:+.4f}"])
story.append(tbl(rows, [3.4 * cm, 1.5 * cm, 1.7 * cm, 1.3 * cm, 1.4 * cm, 2.4 * cm, 2.4 * cm, 1.6 * cm, 1.4 * cm], fs=7.5))
story.append(P('Source : <i>monte_carlo</i> partout. Deux passes MC par run ; la 2e passe ne monte pas toujours le score (null_susceptibility : 0,651 → 0,567). Scores réels 0,672–0,824 ; scores nuls 0,556–0,567, sans chevauchement. Le libellé de stabilité mesure la dispersion bootstrap, pas l’accord avec le MC.', BODY))
story.append(Image(str(FIG / 'fig_S1_temperatures.png'), width=17 * cm, height=8.68 * cm))
story.append(P('Figure S1 — Température médiane au seuil MC par contrôle, colorée par famille. Ligne rouge : Tc d’Onsager. Les variances pointent bas, les moyennes pointent sur Tc, les nuls se dispersent.', SMALL))
story.append(Image(str(FIG / 'fig_S2_scan_curves.png'), width=17 * cm, height=9.27 * cm))
story.append(P('Figure S2 — Courbes de scan superposées. Les nuls (gris) ont des courbes plus plates et plus bruyantes.', SMALL))
story.append(P('Paysage : une seule masse par run (pics forts, rel ≥ 0,90)', H1))
hdr = ['Contrôle', 'Pics forts', 'Groupe principal (T)', 'Masse secondaire ≥ 0,20 ?']
rows = [hdr]
for c in CONTROLS:
    r = by_ctrl[c]
    grp = r['groupe_principal']
    gtxt = f"{min(grp):.4f}–{max(grp):.4f}" if len(grp) > 1 else f"{grp[0]:.4f}"
    sec = '; '.join(f"[{min(x['temps']):.4f}–{max(x['temps']):.4f}]" for x in r['candidats_secondaires']) or 'non'
    rows.append([c, str(r['n_pics_forts']), gtxt, sec])
story.append(tbl(rows, [3.6 * cm, 1.8 * cm, 4.2 * cm, 7.4 * cm], fs=8))
story.append(P('Attribution du candidat 2,6739 (expvar_energy) : R1 — 1 seul run dérivé (≥ 2 requis) ; R2 — absent sous rollvar_energy_40 (pics forts : [1,8391] uniquement) ; R3 — présent dans null_susceptibility et null_rollvar_mag. <b>Rejeté : artefact de construction + machinerie.</b> Aucun autre candidat secondaire dans les runs dérivés.', BODY))
story.append(P('Seuils propres par flux analysé (températures médianes)', H1))
pf = {}
for c in CONTROLS:
    d = pd.read_csv(BASE / 'runs' / c / 'per_flux_thresholds.csv')
    for _, r in d.iterrows():
        pf.setdefault(r['flux'], {})[c] = float(r['temperature_mediane_au_seuil'])
fluxes = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar', 'susceptibility']
for group, cols in (('Contrôles dérivés', DERIVED), ('Nuls', NULLS)):
    story.append(P(group, H2))
    data = [['Flux \\ Contrôle'] + cols]
    for f in fluxes:
        data.append([f] + [('—' if f == c else f"{pf[f][c]:.4f}") for c in cols])
    w = [2.6 * cm] + [(14.4 / len(cols)) * cm] * len(cols)
    story.append(tbl(data, w, fs=7.5))
story.append(P('Les 5 flux non-χ ont un seuil propre identique au seuil MC du run (même % à 2 décimales) dans les 8 runs dérivés ; sous les nuls, ils se dispersent. χ comme flux analysé ne suit JAMAIS le seuil du run (T 2,1174–2,4652, % 27,48–93,55) : sa coupure propre est haute et dispersée, dans les runs dérivés comme dans les nuls.', BODY))
story.append(P('Questions Q1–Q6 (moyennes par run)', H1))
hdr = ['Contrôle', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6-A']
rows = [hdr]
qkeys = {'Q1': 'Q1_Calme_vs_Chaos', 'Q2': 'Q2_Tension_Seuil', 'Q3': 'Q3_Agressivite',
         'Q4': 'Q4_Persistence', 'Q5': 'Q5_Active_Reactive', 'Q6': 'Q6_Active_Reactive_Scaled'}
for c in CONTROLS:
    q = summ[c]['scores_moyens_par_Q']
    rows.append([c] + [f"{q[qkeys[k]]:.3f}" for k in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']])
story.append(tbl(rows, [3.8 * cm] + [2.2 * cm] * 6, fs=8))
story.append(P('Q6-A : 39–221 (dérivés) contre 87–119 (nuls) — chevauchement, ne sépare pas réel et nul. Q5 : 6,7–11,6 (dérivés) contre 11,1–15,9 (nuls) — les nuls sont plus hauts. Ni Q5 ni Q6-A ne calibrent le réel contre le nul ici. F1/F2 : changements de signe 102–135 (dérivés) contre 158–162 (nuls). Bruit : proxy de variance modéré sur les 11 runs, dérives médianes 4,0–8,0, aucune référence dégénérée.', BODY))
story.append(P('Opinion', H1))
story.append(P('1) <b>Pas de deuxième point critique</b> : Ising 2D à champ nul n’en a qu’un (théorème), et 8 loupes dérivées confirment l’absence de deuxième masse. 2) <b>La famille basse est une vraie lecture</b> : six contrôles de variance, avec ou sans mémoire, lisent l’onset des fluctuations à T 1,84–1,98. Changer la loupe (premier → second moment) change le seuil lu. 3) <b>χ comme contrôle (lot original, T 2,1174) se situe entre les deux familles</b> — variance normalisée par T, loupe hybride. 4) <b>Le nul calibre l’instrument</b> : un seuil isolé à score ~0,56 et UNSTABLE ne prouve rien. 5) Suite logique : L = 64 + 2e graine pour confirmer la famille basse et mesurer si l’écart se resserre ; puis réel-vs-nul loupe par loupe sur les 29 estimateurs.', BODY))
story.append(P('Limites et fichiers', H1))
story.append(P('Lecture descriptive seulement. Une seule taille (L=32), une seule graine (42). Comparaison à Tc = jugement descriptif post-hoc (question garder/retirer : toujours ouverte). Fichiers : PROTOCOLE_DERIVED.md, PROVENANCE_DERIVED.md, RAPPORT_DERIVED.md, synthese_derived.json, gen_derived.py, run_one_derived.py, run_lot_derived.sh, synthese_derived.py, data/ (2 CSV), runs/&lt;contrôle&gt;/ (13 fichiers par run), figures/.', BODY))
story.append(PageBreak())
story.append(P('Figures du pipeline (par contrôle)', H1))
for c in CONTROLS:
    story.append(P(f"Contrôle : {c} ({FAMILY[c]}) — seuil MC {summ[c]['mc_threshold_pct']:.2f} %, score {summ[c]['mc_score']:.4f}, T = {summ[c]['temperature_mediane_au_seuil_mc']:.4f}", H2))
    story.append(Image(str(BASE / 'runs' / c / 'threshold_scan.png'), width=16 * cm, height=9.6 * cm))
    story.append(Image(str(BASE / 'runs' / c / 'noise_diagnostic.png'), width=16 * cm, height=9.6 * cm))

pdf_path = BASE / 'Ising_derived_v35H1_Resultats_complets.pdf'
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title='Ising dérivés × v3.5.4-H1 — Résultats complets',
                        author='TagPrint (Muse) pour Zackary Drasse-Ménard')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF OK :', pdf_path)

# ---------- ZIP ----------
zip_path = BASE / 'ising_derived_resultats.zip'
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
print('Tailles : PDF %.1f Mo, ZIP %.1f Mo' % (pdf_path.stat().st_size / 1e6, zip_path.stat().st_size / 1e6))
print('Fichiers zip :', len(zipfile.ZipFile(zip_path).namelist()))
