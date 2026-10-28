# -*- coding: utf-8 -*-
"""Figures de synthèse + PDF + zip du lot ising-derived EXT.
Sorties : figures_ext/fig_S1_temperatures.png, figures_ext/fig_S2_scan_curves.png,
Ising_derived_EXT_v35H1_Resultats_complets.pdf, ising_derived_ext_resultats.zip
(zip = fichiers EXT uniquement : docs, scripts, données étendues, runs_ext/,
figures_ext/ ; le lot 1 reste dans son propre zip/dossier).
"""
import hashlib
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
DERIVED = ['expmean_fliprate', 'expmean_localvar', 'rollvar_fliprate_40',
           'rollvar_localvar_40', 'rollmean_energy_40',
           'rollmean_magnetization_40', 'rollmean_fliprate_40',
           'rollmean_localvar_40']
NULLS = ['null_expmean_fliprate', 'null_rollvar_fliprate',
         'null_rollmean_mag', 'null_rollmean_localvar']
CONTROLS = DERIVED + NULLS
FAMILY = {c: 'expmean' for c in DERIVED[:2]}
FAMILY.update({c: 'rollvar' for c in DERIVED[2:4]})
FAMILY.update({c: 'rollmean' for c in DERIVED[4:]})
FAMILY.update({c: 'nul' for c in NULLS})
COLORS = {'expmean': 'darkgreen', 'rollvar': 'darkorange', 'rollmean': 'teal', 'nul': 'grey'}
TC = 2.269185314213
FIG = BASE / 'figures_ext'
FIG.mkdir(exist_ok=True)

summ = {}
for c in CONTROLS:
    summ[c] = json.loads((BASE / 'runs_ext' / c / 'run_summary.json').read_text(encoding='utf-8'))
synth = json.loads((BASE / 'synthese_derived_ext.json').read_text(encoding='utf-8'))
diag = json.loads((BASE / 'diagnostic_runs_ext.json').read_text(encoding='utf-8'))
by_ctrl = {r['controle']: r for r in synth['controles']}

# ---------- Figure S1 ----------
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
plt.title('Seuil Monte Carlo traduit en température, par contrôle (v3.5.4-H1) — extension')
for fam, col in COLORS.items():
    plt.scatter([], [], color=col, label=fam)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIG / 'fig_S1_temperatures.png', dpi=150)
plt.close()

# ---------- Figure S2 ----------
plt.figure(figsize=(11, 6))
for c in CONTROLS:
    sc = pd.read_csv(BASE / 'runs_ext' / c / 'scan_curve.csv').dropna(subset=['score']).sort_values('candidate')
    plt.plot(sc['candidate'], sc['score'], linewidth=1.0, label=c,
             color=COLORS[FAMILY[c]], alpha=0.85)
    plt.axvline(summ[c]['mc_threshold_pct'], color=COLORS[FAMILY[c]], alpha=0.3, linewidth=0.8)
plt.xlabel('Candidat seuil (% du rang du contrôle)')
plt.ylabel('Score de séparation')
plt.title('Courbes de scan — extension : 8 contrôles dérivés + 4 nuls')
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
    canvas.drawString(2 * cm, 1.1 * cm, 'Ising dérivés EXT × v3.5.4-H1 (Q6-A) — 28 oct. 2026 — dépôt privé FindPrint/Code')
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f'Page {doc.page}')
    canvas.restoreState()


story = []
story.append(P('Ising 2D : extension dérivés — factoriel complet, famille rollmean, nuls × v3.5.4-H1 (Q6-A)', H1))
story.append(P('Lot ising-derived-ext — 28 octobre 2026. Synthèse vérifiée (synthese_derived_ext.py). Protocole gelé avant construction et runs (PROTOCOLE_DERIVED_EXT.md). Provenance complète (PROVENANCE_DERIVED_EXT.md). Pipeline SHA-256 <i>b54fcf66…</i>. Données étendues SHA-256 <i>bae505d4…</i>, températures <i>4863b1de…</i>. Le pipeline ne voit jamais T ni Tc ; traduction en T post-hoc dans le harnais ; comparaison à Tc descriptive.', SMALL))
story.append(P('Verdict', H1))
story.append(P('<b>12/12 runs OK, 0 échec, 0 avertissement, 0 repli. Aucune deuxième masse.</b> Familles <b>moyenne</b> (expmean ×2 + rollmean ×4) → <b>T = 2,2565</b>, scores 0,760–0,767, tous VERY STABLE. Famille <b>variance</b> (rollvar ×2) → <b>T = 1,77–1,84</b>, scores 0,772–0,871 : le pied du régime. <b>4 nuls</b> : 2 normaux (0,56–0,60) et <b>2 alarmants (0,7095 et 0,7218, MODERATELY STABLE)</b> — le score global seul ne distingue pas le réel du nul ; l’amplitude du scan, Q4 et le proxy de bruit le font, proprement, sur les 23 runs. Attribution poolée (16 dérivés + 7 nuls) : un seul candidat secondaire (T = 2,6739), <b>artefact confirmé</b> (R1+R2+R3).'))
story.append(P('Données et protocole', H1))
story.append(P('Dataset <i>ising_derived_ext.csv</i> (960 lignes × 29 colonnes, 0 NaN), construit par <i>gen_derived_ext.py</i> (SHA <i>6170c25c…</i>) depuis <i>ising_derived.csv</i> (SHA <i>10563d4d…</i>), <b>sans aucune valeur de T</b>. 17 colonnes du lot 1 préservées octet pour octet (porte E2) + 12 colonnes : complétion du factoriel (expmean ×2, rollvar ×2), famille rollmean ×4, nuls ×4 (permutation <i>default_rng(1234)</i>, mêmes indices que le lot 1, vérifié). Portes E1–E7 passées. Exclusions gelées : <i>flip</i> (= 1024 × <i>fliprate</i>), <i>susceptibility</i> comme base (non monotone), racines des variances, autres fenêtres. Mode stable, w80, cohen_d, graine 42, HARMONIC_PROB 0,45, Theiler 1/φ planché. Analysés fixés aux 6 originaux (χ incluse). Max 2 en parallèle. Lot total 22 min 25 s.', BODY))
story.append(P('Anomalie de métadonnées (sans effet sur les runs) : champs <i>famille</i>/<i>construction</i> vides dans les <i>run_summary.json</i> (tableaux associatifs bash non exportés aux sous-shells <i>xargs</i>) ; la synthèse re-dérive la famille du préfixe du nom.', BODY))
story.append(P('Seuils Monte Carlo par contrôle', H1))
hdr = ['Contrôle', 'Famille', 'Seuil MC %', 'Score', 'Stabilité', 'Moy. ± std', 'T au seuil', 'ΔT vs Tc']
rows = [hdr]
for c in CONTROLS:
    s = summ[c]
    rows.append([c, FAMILY[c], f"{s['mc_threshold_pct']:.2f}", f"{s['mc_score']:.4f}",
                 s['stability_rating'],
                 f"{s['stability_mean']:.2f} ± {s['stability_std']:.2f}",
                 f"{s['temperature_mediane_au_seuil_mc']:.4f}", f"{s['temperature_mediane_au_seuil_mc'] - TC:+.4f}"])
story.append(tbl(rows, [3.4 * cm, 1.5 * cm, 1.7 * cm, 1.3 * cm, 2.5 * cm, 2.5 * cm, 1.6 * cm, 1.5 * cm], fs=7.5))
story.append(Image(str(FIG / 'fig_S1_temperatures.png'), width=17 * cm, height=8.68 * cm))
story.append(P('Figure S1 — Température médiane au seuil MC par contrôle. Ligne rouge : Tc d’Onsager. Les moyennes pointent sur Tc, les variances pointent bas, les nuls se dispersent (dont deux à score élevé).', SMALL))
story.append(Image(str(FIG / 'fig_S2_scan_curves.png'), width=17 * cm, height=9.27 * cm))
story.append(P('Figure S2 — Courbes de scan superposées. Les nuls (gris) ont des courbes plates (max 0,18–0,33) contre 0,74–3,77 pour les dérivés.', SMALL))
story.append(P('Paysage et attribution (R1–R5, 23 runs poolés)', H1))
story.append(P('Aucun des 16 runs dérivés n’a de masse secondaire séparée (≥ 0,20 du groupe principal). Candidat unique : T = 2,6739 — 1 seul run dérivé (expvar_energy), présent dans 3/7 nuls (R3), absent sous rollvar_energy_40 (R2) → <b>artefact</b>. Les autres candidats secondaires sont dans des runs nuls uniquement. Aucun candidat réel (R4).', BODY))
story.append(P('Seuils propres par flux analysé (températures médianes)', H1))
fluxes = ['fliprate', 'flip', 'energy', 'magnetization', 'localvar', 'susceptibility']
mat = synth['matrice_temperatures_seuils_propres']
for group, cols in (('Contrôles dérivés', DERIVED), ('Nuls', NULLS)):
    story.append(P(group, H2))
    data = [['Flux \\ Contrôle'] + cols]
    for f in fluxes:
        data.append([f] + [('—' if f == c else f"{mat[c][f]:.4f}") for c in cols])
    w = [2.6 * cm] + [(14.4 / len(cols)) * cm] * len(cols)
    story.append(tbl(data, w, fs=7.5))
story.append(P('Les 5 flux non-χ s’accordent au seuil MC du run dans les 8 runs dérivés ; χ ne suit jamais le run. Sous les nuls, dispersion — sauf null_rollmean_localvar (5/6 à 2,1870 = seuil MC) : l’accord seuils propres = MC ne sépare pas ce nul ; l’amplitude du scan, Q4 et le proxy, oui.', BODY))
story.append(P('Dossier diagnostique : Q, bruit, F1/F2 — réel contre nul (23 runs)', H1))
hdr = ['Contrôle', 'MC %', 'Score', 'Stab.', 'T', 'Q1', 'Q2', 'Q4', 'Q5', 'Q6-A', 'Proxy', 'F1F2', 'Scan max']
rows = [hdr]
all_diag = diag['runs']
order = ['expvar_energy', 'expvar_magnetization', 'expvar_fliprate', 'expvar_localvar',
         'expmean_energy', 'expmean_magnetization', 'rollvar_magnetization_40',
         'rollvar_energy_40', 'null_susceptibility', 'null_expvar_mag',
         'null_rollvar_mag'] + CONTROLS
for c in order:
    r = all_diag[c]
    q = r['Q_moyens']
    f1 = sum(v['n_sign_change'] for v in r['F1F2'].values())
    stab = {'VERY STABLE': 'VS', 'MODERATELY STABLE': 'MS', 'UNSTABLE': 'U'}.get(r['stabilite'], '?')
    rows.append([c, f"{r['seuil_mc_pct']:.2f}", f"{r['score_mc']:.3f}", stab,
                 f"{r['temp_mc']:.4f}", f"{q.get('Q1_Calme_vs_Chaos', 0):.2f}",
                 f"{q.get('Q2_Tension_Seuil', 0):.2f}", f"{q.get('Q4_Persistence', 0):.2f}",
                 f"{q.get('Q5_Actif_Receptif', 0):.1f}", f"{q.get('Q6_Actif_Receptif_Echelle', 0):.0f}",
                 f"{r['bruit']['proxy_moyen']:.3f}", str(f1), f"{r['scan']['score_max']:.2f}"])
story.append(tbl(rows, [3.1 * cm, 1.1 * cm, 1.1 * cm, 0.8 * cm, 1.4 * cm, 0.9 * cm, 1.1 * cm, 0.9 * cm, 1.0 * cm, 1.1 * cm, 1.1 * cm, 1.0 * cm, 1.4 * cm], fs=7))
story.append(P('Séparent proprement réel et nul : amplitude du scan (0,74–3,77 contre 0,18–0,33), Q4 (0,37–1,59 contre 0,11–0,17), proxy de bruit (0,61–0,84 contre 0,32–0,44). Ne séparent pas : score MC, Q5, Q6-A, libellé de stabilité. F1/F2 : appui seulement (102–163 contre 158–176). Q2 : moyenne fragile (expvar_energy 14,275, dominée par quelques colonnes). Détail complet par run : <i>diagnostic_runs_ext.json</i>.', BODY))
story.append(P('Cas rollvar_fliprate_40', H2))
story.append(P('Flux en bosse (Spearman vs T +0,14 ; médianes par bande 0,0000 / 0,0002 / 0,0004 / 0,0001) : il mesure l’allumage des fluctuations. Seuil propre unanime des 5 flux non-χ à 9,50 % / T 1,8391. Témoins : expvar_fliprate 1,9087 (même point), rollvar_energy/localvar 1,84/1,77 (même famille), expmean/rollmean_fliprate 2,2565 (après). Q2 3,454, proxy 0,609, 112 changements de signe. <b>Onset avant, lu par toute la famille variance.</b>', BODY))
story.append(P('Opinion', H1))
story.append(P('1) <b>Pas de deuxième point critique</b> — 16 loupes, 4 familles, 2 constructions, 7 nuls. 2) <b>Deux lectures, un seul système</b> : moyennes → transition, variances → pied. 3) <b>Le score global ne suffit plus</b> : 2 nuls sur 7 dépassent 0,70. La calibration passe par l’amplitude du scan, Q4 et le proxy — loupe par loupe. 4) <b>χ analysée seulement</b>, jamais contrôle sans mention du biais. 5) Suite : L=64 + 2e graine, puis réel-vs-nul loupe par loupe sur les 29 estimateurs.', BODY))
story.append(P('Limites et fichiers', H1))
story.append(P('Lecture descriptive seulement. Une seule taille (L=32), une seule graine (42), une seule fenêtre glissante (40). Comparaison à Tc descriptive (question ouverte). Fichiers : PROTOCOLE_DERIVED_EXT.md, PROVENANCE_DERIVED_EXT.md, RAPPORT_DERIVED_EXT.md, synthese_derived_ext.json, diagnostic_runs_ext.json, gen_derived_ext.py, run_one_derived_ext.py, run_lot_ext.sh, synthese_derived_ext.py, diagnostic_runs_ext.py, build_pdf_zip_derived_ext.py, data/ising_derived_ext.csv, runs_ext/&lt;contrôle&gt;/ (11 fichiers par run), figures_ext/.', BODY))
story.append(PageBreak())
story.append(P('Figures du pipeline (par contrôle)', H1))
for c in CONTROLS:
    story.append(P(f"Contrôle : {c} ({FAMILY[c]}) — seuil MC {summ[c]['mc_threshold_pct']:.2f} %, score {summ[c]['mc_score']:.4f}, T = {summ[c]['temperature_mediane_au_seuil_mc']:.4f}", H2))
    story.append(Image(str(BASE / 'runs_ext' / c / 'threshold_scan.png'), width=16 * cm, height=9.6 * cm))
    story.append(Image(str(BASE / 'runs_ext' / c / 'noise_diagnostic.png'), width=16 * cm, height=9.6 * cm))

pdf_path = BASE / 'Ising_derived_EXT_v35H1_Resultats_complets.pdf'
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title='Ising dérivés EXT × v3.5.4-H1 — Résultats complets',
                        author='TagPrint (Muse) pour Zackary Drasse-Ménard')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF OK :', pdf_path)

# ---------- ZIP (fichiers EXT uniquement) ----------
zip_path = BASE / 'ising_derived_ext_resultats.zip'
include_files = ['PROTOCOLE_DERIVED_EXT.md', 'PROVENANCE_DERIVED_EXT.md',
                 'RAPPORT_DERIVED_EXT.md', 'synthese_derived_ext.json',
                 'diagnostic_runs_ext.json', 'gen_derived_ext.py',
                 'run_one_derived_ext.py', 'run_lot_ext.sh',
                 'run_lot_ext.log', 'synthese_derived_ext.py',
                 'diagnostic_runs_ext.py', 'build_pdf_zip_derived_ext.py',
                 'data/ising_derived_ext.csv',
                 'data/ising_classic_v354_temperature.csv']
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for rel in include_files:
        p = BASE / rel
        if p.exists():
            z.write(p, rel)
    for p in sorted((BASE / 'runs_ext').rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            z.write(p, p.relative_to(BASE).as_posix())
    for p in sorted(FIG.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(BASE).as_posix())
print('ZIP OK :', zip_path)
print('SHA-256 PDF :', hashlib.sha256(pdf_path.read_bytes()).hexdigest())
print('SHA-256 ZIP :', hashlib.sha256(zip_path.read_bytes()).hexdigest())
print('Tailles : PDF %.1f Mo, ZIP %.1f Mo' % (pdf_path.stat().st_size / 1e6, zip_path.stat().st_size / 1e6))
print('Fichiers zip :', len(zipfile.ZipFile(zip_path).namelist()))
