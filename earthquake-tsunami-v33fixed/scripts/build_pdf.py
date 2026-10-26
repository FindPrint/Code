# -*- coding: utf-8 -*-
"""Construit le PDF unique des resultats Earthquake/Tsunami x v3.3 FIXED.
Adapte de earthquake-tsunami/scripts/build_pdf.py (meme structure, meme venv ReportLab).
Sources : run_summary.json / per_flux_thresholds.csv / transition_F1F2.csv
de chaque run + syntheses CSV. Polices standard (WinAnsi) : texte sans accents
pour eviter tout probleme d'encodage.
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

BASE = Path('/home/hatch/workspace/earthquake-tsunami-v33fixed')
OUT = BASE / 'Earthquake_Tsunami_v33FIXED_Resultats_complets.pdf'
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

ORDER = ['magnitude', 'cdi', 'mmi', 'sig', 'nst', 'dmin', 'gap', 'depth', 'latitude', 'longitude', 'Year', 'Month', 'tsunami']
runs = {c: load_run(BASE / 'results' / f'ctrl_{c}') for c in ORDER}

story = []
# ---------------- Couverture ----------------
story += [Spacer(1, 30*mm), P('Global Earthquake Tsunami Risk Assessment (Kaggle)<br/>x pipeline v3.3 FIXED', 'titre'),
          P('Tous les resultats en un seul fichier : 13 controles (toutes les colonnes du CSV), seuils par flux, F1/F2 et images de tous les runs.', 'txt'),
          Spacer(1, 6*mm),
          P('Source : https://www.kaggle.com/datasets/ahmeduzaki/global-earthquake-tsunami-risk-assessment-dataset (fichier earthquake_data_tsunami.csv, 782 lignes, 13 colonnes). Pipeline : pipeline_autonome_v3_3_fixed.py tel quel, mode stable, w_size 80, cohen_d, graine 42, Monte Carlo classique (sans guidage harmonique). Regle Porte D : le controle est exclu des flux analyses.', 'txt'),
          P('Runs : 13 lances, 13 termines, 0 echec. Duree totale 5 506,4 s (environ 424 s par run). Images : 26 figures (courbe de scan + diagnostic bruit pour chacun des 13 runs).', 'txt'),
          P('Dates : runs le 25 octobre 2026 (protocole gele a 13h45 HAE, avant tout run. PDF assemble le 25 octobre 2026.', 'txt'),
          Spacer(1, 4*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('<b>Verdict</b> : seuls 2 runs sont VERY STABLE selon le critere du pipeline : dmin (44,37 %) et Year (47,41 %). 7 runs sont UNSTABLE (magnitude, cdi, nst, gap, latitude, longitude, Month) et ne doivent pas etre lus seuls. Deux faisceaux se repetent : intensite haute ~85-92 % (magnitude / sig / cdi / mmi) et faisceau dmin-Year-nst-tsunami ~42-53 %, aux scores propres les plus forts, mais en partie porte par des plateaux de zeros (voir reserves).', 'txt'),
          P('Contenu : 1) donnees, 2) synthese des 13 controles et lectures, 3) detail par run (resume, seuils propres par flux, scores Q, images), 4) annexe F1/F2 complete (tous les estimateurs x tous les flux x 13 runs). Les rapports texte complets du pipeline et les CSV bruts restent dans l\'archive zip d\'origine.', 'txt'),
          PageBreak()]

# ---------------- 1. Donnees ----------------
story += [P('1. Les donnees, telles que telechargees', 'stitre'),
          P('Aucun nettoyage : le fichier est utilise tel quel. Toutes les colonnes sont numeriques, 0 valeur manquante sur 782 lignes. Le pipeline remplace les NaN des flux par leur moyenne (son code) : sans objet ici, il n\'y en a pas.', 'txt')]
df = pd.read_csv(BASE / 'data' / 'earthquake_data_tsunami.csv')
data = [hdr(['colonne', 'valides', 'distinctes', 'min', 'max', 'moyenne'])]
for c in df.columns:
    s = df[c]
    data.append(row(c, int(s.notna().sum()), int(s.nunique()), fmt(float(s.min()), 2), fmt(float(s.max()), 2), fmt(float(s.mean()), 2)))
story += [tbl(data, [30*mm, 22*mm, 24*mm, 30*mm, 30*mm, 34*mm]), Spacer(1, 3*mm),
          P('Faits de structure mesures avant les runs : dmin = 0 sur 405 lignes (51,8 %) ; nst = 0 sur 365 lignes (46,7 %) ; tsunami binaire (0 : 478 lignes, 61,1 % ; 1 : 304 lignes, 38,9 %) ; cdi 10 valeurs (0 : 27,1 %) ; mmi 9 valeurs ; Month 12 valeurs ; magnitude 24 valeurs ; Year 22 valeurs (2001-2022).', 'petit'),
          P('Paliers de rang (valeur : % moyen de rang) : tsunami 0 : 30,63 / 1 : 80,63 ; cdi 0 : 13,62 / 1 : 28,07 / 2 : 29,86 / 3 : 33,76 / 4 : 40,73 / 5 : 51,53 / 6 : 63,30 / 7 : 74,42 / 8 : 86,13 / 9 : 95,84 ; mmi 1 : 0,13 / 2 : 0,45 / 3 : 3,26 / 4 : 11,38 / 5 : 26,02 / 6 : 48,08 / 7 : 74,42 / 8 : 92,14 / 9 : 98,27 ; Month 1 : 4,54 / 2 : 13,04 / 3 : 21,10 / 4 : 30,05 / 5 : 38,68 / 6 : 45,08 / 7 : 51,34 / 8 : 59,27 / 9 : 68,73 / 10 : 78,26 / 11 : 87,79 / 12 : 96,48. Tableau complet : plateaux_controles.csv (archive zip). Pour un controle discret, tout seuil entre deux paliers separe exactement les memes deux groupes.', 'petit')]

# ---------------- 2. Synthese ----------------
story += [P('2. Synthese des 13 controles', 'stitre')]
syn = pd.read_csv(BASE / 'synthese_runs.csv')
data = [hdr(['controle', 'n', 'MC %', 'defaut %', 'ecart', 'stabilite (std)', 'score MC', 'scan max', 'valeur au MC'])]
for r in syn.itertuples():
    data.append(row(r.controle, int(r.n_lignes), fmt(r.seuil_MC_pct), fmt(r.seuil_defaut_pct), fmt(r.ecart_MC_moins_defaut, 1),
                    f"{r.stabilite} ({fmt(r.stabilite_std, 2)})", fmt(r.score_MC, 3), fmt(r.scan_global_max, 3), fmt(r.valeur_controle_au_MC_mediane, 1)))
story += [tbl(data, [20*mm, 12*mm, 16*mm, 18*mm, 16*mm, 34*mm, 18*mm, 18*mm, 28*mm])]
story += [P('Lecture : les desaccords MC/defaut les plus forts sont Month (-39,27 : MC 39,12 contre defaut 78,39) et tsunami (-23,17 : MC 56,34 contre defaut 79,50). Paysages les plus plats : Month (scan max 0,124), magnitude (0,285), gap (0,303). Les plus forts : longitude (0,831, mais seuil en bordure a 1,83 % et UNSTABLE), dmin (0,775), Year (0,670), nst (0,651).', 'petit'),
          P('En tant que flux, les scores propres moyens les plus forts sont Year (1,013 ; max 2,426), nst (1,002 ; max 2,847), tsunami (0,821 ; max 2,053), dmin (0,700) ; les plus faibles : Month (0,282) et gap (0,368).', 'txt'),
          P('Faisceau intensite haute : magnitude (MC 89,62 %) avec sig 86,56 % (1,029), mmi 92,37 % (0,712), cdi 92,06 % (0,595) ; cdi (MC 80,31 %) avec sig 80,92 % (1,162) et mmi 81,07 % (1,142) ; mmi (MC 10,30 %) avec sig 91,60 % (1,104) ; depth (MC 91,95 %) avec mmi 91,95 % (1,331). Coupure descriptive "gros seismes" (magnitude mediane ~7,6 au seuil), pas une magnitude critique demontree.', 'txt'),
          P('Faisceau dmin-Year-nst-tsunami : dmin (MC 44,37 %, VERY STABLE) avec nst 44,37 % (2,761) et Year 49,45 % (2,426) ; Year (MC 47,41 %, VERY STABLE) avec nst 52,12 % (2,847, le plus fort du banc) et tsunami 44,58 % (2,053) ; nst (MC 49,45 %) avec Year 38,67 % (2,152) et tsunami 49,45 % (1,756) ; tsunami (MC 56,34 %) avec nst 80,31 % (1,754) et Year 79,28 % (1,581).', 'txt'),
          P('Reserves : (1) dmin = 0 a 51,8 % : le seuil MC 44,37 % tombe a l\'interieur du plateau de zeros, il ne separe pas "dmin = 0" de "dmin &gt; 0" (frontiere a 51,8 %). Son VERY STABLE ne doit pas etre lu comme un seuil physique sur dmin. (2) nst = 0 a 46,7 % : le seuil 49,45 % est juste au-dessus de la frontiere zero/non-zero, donc a peu pres "pas de station" contre "stations presentes". (3) tsunami binaire : le seuil 56,34 % ne separe pas 0 de 1, il tombe entre les plateaux 30,63 % et 80,63 % (valeur mediane au seuil : 0). (4) latitude/longitude sont un ordre geographique, pas une progression : le seuil longitude a 1,83 % isole environ 14 evenements extremes ouest (mediane -178,15). (5) Year : 47,41 % correspond a l\'annee 2013, mediane de couverture 2001-2022, coupure temporelle descriptive.', 'txt'),
          PageBreak()]


# ---------------- Flux informationnels, a part ----------------
story += [P('2b. Flux informationnels, a part', 'stitre'),
          P('Definition gelee avant les runs : Year, Month (temps), latitude, longitude (lieu), tsunami (etiquette 0/1). Les 8 autres colonnes restent dans le groupe principal. La separation est faite a la synthese : les runs contiennent tous les flux, pour ne pas changer le protocole. Donnees brutes : flux_informationnels_donnees.csv (5 colonnes, 782 lignes). Seuils propres ci-dessous : seuils_flux_informationnels.csv (60 lignes : chaque flux informationnel dans les 12 runs ou il est flux).', 'txt'),
          P('En tant que flux, scores propres moyens : Year 1,013 (max 2,426), tsunami 0,821 (max 2,053), latitude 0,480 (max 1,196), longitude 0,468 (max 0,971), Month 0,282 (max 0,717). Autrement dit : Year et tsunami portent les signaux informationnels les plus forts du banc, Month le plus faible, latitude/longitude au milieu. Les plus forts en detail : Year 49,45 % (2,426) en controle dmin ; tsunami 44,58 % (2,053) en controle Year et 42,79 % (1,598) en controle dmin.', 'txt')]
_inf = pd.read_csv(BASE / 'seuils_flux_informationnels.csv')
_data = [hdr(['controle', 'flux informationnel', 'seuil propre %', 'score max', 'top-3 candidats %'])]
for _r in _inf.sort_values(['flux', 'controle']).itertuples():
    _data.append(row(_r.controle, _r.flux, fmt(_r.seuil_propre_pct), fmt(_r.score_max, 3), str(_r.top3_candidats)))
story += [tbl(_data, [28*mm, 38*mm, 30*mm, 24*mm, 60*mm]), PageBreak()]

# ---------------- Detail par run ----------------
def run_section(titre, run_id, s, pf, d):
    out = [P(titre, 'h2')]
    if s['status'] != 'OK':
        out += [P(f"ECHEC : {s.get('error', '')} (valeurs valides du controle : {s.get('n_valides_controle')}).", 'txt')]
        return out
    q = s.get('scores_moyens_par_Q') or {}
    qtxt = ' ; '.join(f"{k} = {v}" for k, v in q.items()) if q else '-'
    cv = s.get('controle_valeur_au_seuil_mc') or {}
    out += [P(f"n = {s.get('n_pts')} ; MC = {fmt(s.get('mc_threshold_pct'))} % ; defaut = {fmt(s.get('default_threshold_pct'))} % ; MC brut = {fmt(s.get('raw_mc_threshold_pct'))} % ; defaut brut = {fmt(s.get('raw_default_threshold_pct'))} % ; rigide 1001 = {fmt(s.get('rigid_1001_threshold_pct'))} % ; stabilite = {s.get('stability_rating')} (moy. {fmt(s.get('stability_mean'))}, std {fmt(s.get('stability_std'))}) ; score MC = {fmt(s.get('mc_score'), 3)} (w = {s.get('mc_w_size')}, candidats = {s.get('mc_n_candidates')}) ; scan global max = {fmt(s.get('scan_max_score'), 3)} a {fmt(s.get('scan_argmax_pct'))} % ; valeur du controle au MC (mediane) = {fmt(cv.get('mediane'), 1)} ; bruit = {s.get('noise_label', '-')}.", 'petit'),
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

# ---------------- Annexe F1/F2 ----------------
story += [PageBreak(), P('Annexe. F1/F2 post-seuil, complete', 'stitre'),
          P('Pour chacun des 13 runs : F1 (derivee premiere post-seuil) et F2 (derivee seconde), par estimateur et par flux, tels que produits par le pipeline (transition_analysis). Signe et ordre sont ceux du pipeline. 65 lignes par run, 845 au total.', 'txt')]
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
          P('Fin. Protocole gele : PROTOCOLE.md. Rapport d\'origine : RAPPORT.md. Archive zip : earthquake_tsunami_v33fixed_13_controles_resultats.zip (rapports texte du pipeline, CSV bruts, courbes de scan).', 'petit')]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(15*mm, 10*mm, 'Earthquake / Tsunami x pipeline v3.3 FIXED - resultats complets')
    canvas.drawRightString(W - 15*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
                        title='Earthquake / Tsunami x v3.3-H1 - Resultats complets', author='Muse')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF ecrit : {OUT} ({OUT.stat().st_size/1e6:.1f} Mo)")
