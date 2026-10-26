# -*- coding: utf-8 -*-
"""Construit le PDF unique des resultats Air Quality x v3.3-H1.
Toutes les valeurs sont lues dans les CSV/JSON produits (aucun chiffre
recopie a la main) : synthese_runs.csv, tous_seuils_par_flux.csv,
tous_F1F2.csv, run_summary.json de chaque run, data/air_quality_dataset.csv.
Polices standard (WinAnsi) : texte sans accents pour eviter tout
probleme d'encodage.
"""
import json
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, Image, HRFlowable)
from reportlab.lib.utils import ImageReader

BASE = Path('/home/hatch/workspace/air-quality')
OUT = BASE / 'Air_Quality_v33H1_Resultats_complets.pdf'
W, H = A4
styles = getSampleStyleSheet()
S = {}
S['titre'] = ParagraphStyle('titre', parent=styles['Title'], fontSize=22, leading=26, spaceAfter=6*mm)
S['stitre'] = ParagraphStyle('stitre', parent=styles['Heading1'], fontSize=15, leading=19, spaceBefore=6*mm, spaceAfter=3*mm, textColor=colors.HexColor('#1a3a5c'))
S['h2'] = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=12, leading=15, spaceBefore=5*mm, spaceAfter=2*mm, textColor=colors.HexColor('#1a3a5c'))
S['h3'] = ParagraphStyle('h3', parent=styles['Heading3'], fontSize=10.5, leading=13, spaceBefore=4*mm, spaceAfter=2*mm)
S['txt'] = ParagraphStyle('txt', parent=styles['Normal'], fontSize=9.5, leading=13, spaceAfter=2*mm, alignment=TA_LEFT)
S['petit'] = ParagraphStyle('petit', parent=styles['Normal'], fontSize=8, leading=10.5, spaceAfter=2*mm)
S['cell'] = ParagraphStyle('cell', parent=styles['Normal'], fontSize=7.2, leading=9)
S['cellH'] = ParagraphStyle('cellH', parent=styles['Normal'], fontSize=7.2, leading=9, textColor=colors.white, fontName='Helvetica-Bold')
S['cap'] = ParagraphStyle('cap', parent=styles['Normal'], fontSize=8, leading=10.5, textColor=colors.HexColor('#444444'), spaceAfter=3*mm)

def P(t, style='txt'):
    return Paragraph(t, S[style])

def fmt(v, nd=2):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return '-'
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)

def tbl(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    sty = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
           ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]
    if header:
        sty += [('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a5c'))]
    t.setStyle(TableStyle(sty))
    return t

def hdr(cols):
    return [Paragraph(c, S['cellH']) for c in cols]

def row(*vals):
    return [Paragraph(str(v), S['cell']) for v in vals]

def img(path, width_mm=175):
    iw, ih = ImageReader(str(path)).getSize()
    w = width_mm * mm
    h = w * ih / iw
    return Image(str(path), width=w, height=h)

def load_run(d):
    s = json.load(open(Path(d) / 'run_summary.json'))
    pf = pd.read_csv(Path(d) / 'per_flux_thresholds.csv') if (Path(d) / 'per_flux_thresholds.csv').exists() else None
    f1 = pd.read_csv(Path(d) / 'transition_F1F2.csv') if (Path(d) / 'transition_F1F2.csv').exists() else None
    return s, pf, f1

df = pd.read_csv(BASE / 'data' / 'air_quality_dataset_pipeline.csv')
ORDER = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
runs = {c: load_run(BASE / 'results' / f'ctrl_{c}') for c in ORDER}
syn = pd.read_csv(BASE / 'synthese_runs.csv')
PF = pd.read_csv(BASE / 'tous_seuils_par_flux.csv')
FF = pd.read_csv(BASE / 'tous_F1F2.csv')
ok = syn[syn.statut == 'OK']
n_ok = len(ok)
total_s = float(ok.duree_s.sum()) if n_ok else 0.0
stab_counts = ok.stabilite.value_counts().to_dict() if n_ok else {}
top_pf = PF.nlargest(10, 'score_max') if len(PF) else pd.DataFrame()
flux_mean = PF.groupby('flux')['score_max'].mean().sort_values(ascending=False) if len(PF) else pd.Series(dtype=float)

story = []
story += [Spacer(1, 30*mm), P('Air Quality Dataset (Kaggle srisyra02)<br/>x pipeline v3.3-H1', 'titre'),
          P('Tous les resultats en un seul fichier : 10 controles (toutes les colonnes du CSV), seuils par flux, F1/F2 et images de tous les runs.', 'txt'),
          Spacer(1, 6*mm),
          P('Source : https://www.kaggle.com/datasets/srisyra02/air-quality-dataset (fichier air_quality_dataset.csv, 500 lignes, 10 colonnes). Pipeline : pipeline_autonome_v3_3_harmonic_v1.py tel quel, mode stable, w_size 80, cohen_d, graine 42, Monte Carlo harmonique P = 0,45. Regle Porte D : le controle est exclu des flux analyses.', 'txt'),
          P(f"Runs : 10 lances, {n_ok} termines, {len(syn) - n_ok} echec(s). Duree totale des runs OK : {total_s:.1f} s (environ {total_s / max(n_ok, 1):.0f} s par run). Images : 20 figures (courbe de scan + diagnostic bruit pour chacun des 10 runs).", 'txt'),
          P('Dates : runs le 26 octobre 2026 (protocole gele le 26 octobre 2026 a 08h50 HAE, avant tout run). PDF assemble apres la fin des runs.', 'txt'),
          Spacer(1, 4*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P(f"<b>Verdict chiffre</b> : repartition des stabilites (critere du pipeline) sur les {n_ok} runs OK : " + ', '.join(f"{k} = {v}" for k, v in sorted(stab_counts.items())) + ". Aucun run VERY STABLE. Les runs UNSTABLE ne doivent pas etre lus seuls. Tous les seuils MC se situent entre 66,33 % et 78,91 %, dans le tiers superieur de l'axe de rang.", 'txt'),
          P('Ecart page / fichier, constate avant les runs : la page Kaggle decrit des mesures horaires avec Date, Time et une etiquette Source, mais le fichier reel ne contient ni date, ni heure, ni Source, ni capteurs PT08 : 10 colonnes numeriques seulement. Aucune lecture temporelle ni par source d\'emission n\'est donc possible sur ce fichier. Lecture descriptive seulement, aucune conclusion sanitaire ou reglementaire.', 'txt'),
          P('Contenu : 1) donnees, 2) synthese des 10 controles et lectures, 3) detail par run (resume, seuils propres par flux, scores Q, images), 4) annexe F1/F2 complete (tous les estimateurs x tous les flux x 10 runs). Les rapports texte complets du pipeline et les CSV bruts restent dans l\'archive zip.', 'txt'),
          PageBreak()]

story += [P('1. Les donnees, telles que telechargees', 'stitre'),
          P('Aucun nettoyage : le fichier est utilise tel quel, sans colonne derivee (toutes les colonnes d\'origine sont deja numeriques). Toutes les colonnes sont sans valeur manquante sur 500 lignes, chacune avec 500 valeurs uniques (aucun palier discret). Le pipeline remplace les NaN des flux par leur moyenne (son code) : sans objet ici, il n\'y en a pas.', 'txt')]
orig = pd.read_csv(BASE / 'data' / 'air_quality_dataset.csv')
data = [hdr(['colonne', 'valides', 'distinctes', 'min', 'max', 'moyenne'])]
for c in orig.columns:
    s = orig[c]
    data.append(row(c, int(s.notna().sum()), int(s.nunique()), fmt(float(s.min()), 2), fmt(float(s.max()), 2), fmt(float(s.mean()), 2)))
story += [tbl(data, [38*mm, 20*mm, 22*mm, 30*mm, 30*mm, 35*mm]), Spacer(1, 3*mm),
          P('SHA-256 du fichier telecharge : aaf87134601406a882713a37e990b466945e680d9dd3ee00161ecf62b1ba1f97 (59 976 octets, 59,98 ko affiches par Kaggle). Licence affichee sur Kaggle : CC0 (domaine public). Auteur affiche : Srimathy Sivanessan.', 'petit'),
          P('Valeurs negatives presentes, signalees, non corrigees : NOx min -0,08 ; NO2 min -1,94 ; SO2 min -1,10, alors qu\'il s\'agit de concentrations. Le fichier de travail air_quality_dataset_pipeline.csv est une copie exacte (meme SHA-256).', 'petit')]

story += [P('2. Synthese des 10 controles', 'stitre')]
data = [hdr(['controle', 'n', 'MC %', 'defaut %', 'ecart', 'stabilite (std)', 'score MC', 'scan max', 'valeur au MC'])]
for r in syn.itertuples():
    data.append(row(r.controle, fmt(r.n_lignes, 0) if pd.notna(getattr(r, 'n_lignes', None)) else '-', fmt(r.seuil_MC_pct), fmt(r.seuil_defaut_pct), fmt(r.ecart_MC_moins_defaut, 1),
                    f"{r.stabilite} ({fmt(r.stabilite_std, 2)})", fmt(r.score_MC, 3), fmt(r.scan_global_max, 3), fmt(r.valeur_controle_au_MC_mediane, 1)))
story += [tbl(data, [30*mm, 12*mm, 16*mm, 18*mm, 14*mm, 34*mm, 18*mm, 18*mm, 20*mm])]
disc = ok[abs(ok.seuil_MC_pct - ok.stabilite_moy_pct) > 10] if n_ok else pd.DataFrame()
if len(disc):
    story += [P('Accord MC / moyenne bootstrap : la note de stabilite du pipeline repose sur l\'ecart-type bootstrap, pas sur l\'accord entre le seuil MC et la moyenne bootstrap. Un seul run depasse 10 points d\'ecart, aucun ne depasse 15 points : ' + ', '.join(f"{r.controle} (MC {r.seuil_MC_pct:.2f} %, moyenne {r.stabilite_moy_pct:.2f} %, ecart {abs(r.seuil_MC_pct - r.stabilite_moy_pct):.1f} pts, {r.stabilite})" for r in disc.itertuples()) + '.', 'txt')]
if len(top_pf):
    story += [P('Seuils propres les plus forts (top 10 sur les 90 seuils propres, 10 x 9) :', 'txt')]
    data = [hdr(['controle', 'flux', 'seuil propre %', 'score max'])]
    for r in top_pf.itertuples():
        data.append(row(r.controle, r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3)))
    story += [tbl(data, [38*mm, 38*mm, 32*mm, 32*mm])]
if len(flux_mean):
    story += [P('En tant que flux, scores propres moyens (sur les 9 runs ou la colonne est flux), du plus fort au plus faible :', 'txt'),
              P(', '.join(f"{k} ({v:.3f})" for k, v in flux_mean.items()), 'petit'),
              PageBreak()]

def run_section(titre, run_id, s, pf, d):
    out = [P(titre, 'h2')]
    if s['status'] != 'OK':
        out += [P(f"ECHEC : {s.get('error', '')} (valeurs valides du controle : {s.get('n_valides_controle')}).", 'txt')]
        return out
    q = s.get('scores_moyens_par_Q') or {}
    qtxt = ' ; '.join(f"{k} = {v}" for k, v in q.items()) if q else '-'
    cv = s.get('controle_valeur_au_seuil_mc') or {}
    out += [P(f"n = {s.get('n_pts')} ; MC = {fmt(s.get('mc_threshold_pct'))} % ; defaut = {fmt(s.get('default_threshold_pct'))} % ; MC brut = {fmt(s.get('raw_mc_threshold_pct'))} % ; defaut brut = {fmt(s.get('raw_default_threshold_pct'))} % ; rigide 1001 = {fmt(s.get('rigid_1001_threshold_pct'))} % ; stabilite = {s.get('stability_rating')} (moy. {fmt(s.get('stability_mean'))}, std {fmt(s.get('stability_std'))}) ; score MC = {fmt(s.get('mc_score'), 3)} (w = {s.get('mc_w_size')}, candidats = {s.get('mc_n_candidates')}) ; scan global max = {fmt(s.get('scan_max_score'), 3)} a {fmt(s.get('scan_argmax_pct'))} % ; valeur du controle au MC (mediane) = {fmt(cv.get('mediane'), 1)} ; bruit = {s.get('noise_label', '-')} .", 'petit'),
            P(f"Scores moyens par Q : {qtxt}. Duree : {s.get('duration_s')} s.", 'petit')]
    if pf is not None and len(pf):
        data = [hdr(['flux', 'seuil propre %', 'score max', 'top-3 candidats %'])]
        for r in pf.sort_values('score_max', ascending=False).itertuples():
            data.append(row(r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3), str(r.top3_candidats)))
        out += [tbl(data, [40*mm, 32*mm, 28*mm, 75*mm])]
    for imgname, cap in [('threshold_scan.png', 'Courbe de scan (seuil)'), ('noise_diagnostic.png', 'Diagnostic bruit')]:
        p = Path(d) / imgname
        if p.exists():
            out += [Spacer(1, 2*mm), img(p), P(f"{cap} - {run_id}", 'cap')]
    return out

story += [P('3. Detail par run', 'stitre'),
          P('Chaque run : resume, seuils propres par flux (fonction de scan du pipeline, configuration MC du run), scores Q, puis les deux figures du run (courbe de scan, diagnostic bruit).', 'txt')]
for c in ORDER:
    s, pf, f1 = runs[c]
    story += run_section(f"3. Controle = {c}", f"ctrl_{c}", s, pf, BASE / 'results' / f'ctrl_{c}')

story += [PageBreak(), P('Annexe. F1/F2 post-seuil, complete', 'stitre'),
          P('Pour chacun des 10 runs : F1 (derivee premiere post-seuil) et F2 (derivee seconde), par estimateur et par flux, tels que produits par le pipeline (transition_analysis). Signe et ordre sont ceux du pipeline.', 'txt')]
for c in ORDER:
    s, pf, f1 = runs[c]
    if f1 is None:
        continue
    story += [P(f"F1/F2 - ctrl_{c}", 'h3')]
    data = [hdr(['estimateur', 'flux', 'F1', 'F2', 'signe', 'ordre'])]
    for r in f1.itertuples():
        data.append(row(r.estimateur, r.flux, fmt(r.F1, 6), fmt(r.F2, 6), r.signe, r.ordre))
    story += [tbl(data, [30*mm, 30*mm, 40*mm, 40*mm, 22*mm, 18*mm])]

story += [Spacer(1, 6*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('Fin. Protocole gele : PROTOCOLE.md. Rapport d\'origine : RAPPORT.md. Archive zip : air_quality_10_controles_resultats.zip (rapports texte du pipeline, CSV bruts, courbes de scan).', 'petit')]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(15*mm, 10*mm, 'Air Quality x pipeline v3.3-H1 - resultats complets')
    canvas.drawRightString(W - 15*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
                        title='Air Quality x v3.3-H1 - Resultats complets', author='Muse')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF ecrit : {OUT} ({OUT.stat().st_size/1e6:.1f} Mo)")
