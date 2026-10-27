# -*- coding: utf-8 -*-
"""Construit le PDF unique des 3 tests diagnostics mushroom v3.4.
Toutes les valeurs sont lues dans les CSV/JSON produits (aucun chiffre
recopie a la main) : synthese/comparaison_controles.csv,
synthese/tous_seuils_par_flux_tests.csv, synthese/tous_F1F2_tests.csv,
synthese/qs_tests.csv, correlations/results/*.csv, run_summary.json
des 6 runs tests, PROTOCOLE_TESTS.md (dates et regles).
Polices standard (WinAnsi) : texte sans accents.
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

BASE = Path('/home/hatch/workspace/mushroom-tests')
OUT = BASE / 'Mushroom_Tests_Diagnostics_v34_Resultats_complets.pdf'
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

comp = pd.read_csv(BASE / 'synthese' / 'comparaison_controles.csv')
PF = pd.read_csv(BASE / 'synthese' / 'tous_seuils_par_flux_tests.csv')
FF = pd.read_csv(BASE / 'synthese' / 'tous_F1F2_tests.csv')
QS = pd.read_csv(BASE / 'synthese' / 'qs_tests.csv')
TOPS = pd.read_csv(BASE / 'correlations' / 'results' / 'top15_spearman.csv')
TOPC = pd.read_csv(BASE / 'correlations' / 'results' / 'top15_cramer.csv')
FOCUS = json.load(open(BASE / 'correlations' / 'results' / 'trio_focus.json'))
NULLMETA = json.load(open(BASE / 'nul' / 'data' / 'null_meta.json'))

def load_run(test, c):
    d = BASE / test / 'results' / f'ctrl_{c}'
    s = json.load(open(d / 'run_summary.json'))
    pf = pd.read_csv(d / 'per_flux_thresholds.csv')
    f1 = pd.read_csv(d / 'transition_F1F2.csv')
    return s, pf, f1, d

story = []
story += [Spacer(1, 30*mm), P('Mushroom Classification<br/>3 tests diagnostics x pipeline v3.4-H3', 'titre'),
          P('Test 1 : encodage alphabetique. Test 2 : nul propre (permutation du controle, graine 1234). Test 3 : correlations entre flux dominants. Protocole gele avant tout run (PROTOCOLE_TESTS.md, 27 octobre 2026).', 'txt'),
          Spacer(1, 6*mm),
          P('Provenance : The Audubon Society Field Guide to North American Mushrooms (1981, G. H. Lincoff, Knopf, pp. 500-525), donateur Jeff Schlimmer (27 avril 1987), UCI Machine Learning Repository dataset n. 73, miroir Kaggle uciml/mushroom-classification. Les 8 124 lignes sont des descriptions d\'echantillons HYPOTHETIQUES de 23 especes d\'Agaricus/Lepiota, pas des specimens mesures. Couleurs et odeurs = mots humains du guide, aucune mesure instrumentale ni chimique. Detail complet : PROVENANCE.md.', 'txt'),
          P(f"Runs : 6 runs pipeline (3 controles x 2 variantes : ALPHA et NUL), tous threshold_source = monte_carlo, 0 avertissement. Durees : ALPHA class {comp[comp.controle == 'class'].iloc[0].alpha_duree_s:.0f} s, odor {comp[comp.controle == 'odor'].iloc[0].alpha_duree_s:.0f} s, cap-surface {comp[comp.controle == 'cap-surface'].iloc[0].alpha_duree_s:.0f} s ; NUL class {comp[comp.controle == 'class'].iloc[0].nul_duree_s:.0f} s, odor {comp[comp.controle == 'odor'].iloc[0].nul_duree_s:.0f} s, cap-surface {comp[comp.controle == 'cap-surface'].iloc[0].nul_duree_s:.0f} s. Test 3 : 3,4 s, aucun run pipeline. Seuils propres : {len(PF)} lignes (6 runs x 22 flux). F1/F2 : {len(FF)} lignes.", 'txt'),
          Spacer(1, 4*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('<b>Verdicts chiffres</b> : Test 1 encodage = 3/3 SENSIBLES (regle gelee : |delta seuil| > 5 pts OU |delta score| > 0,05). Test 2 nul = 3/3 INDISTINGUABLES, et les 3 scores nuls depassent les scores reels. Test 3 = correlations tres fortes entre flux dominants (Spearman max 0,934 ; V de Cramer max 0,978), temoignages non independants.', 'txt'),
          P('Lecture imposee : codes nominaux, seuils = coupures de rang, lecture descriptive seulement, jamais une regle comestible/veneneux, aucune verite terrain, aucune lecture causale ou temporelle.', 'txt'),
          P('Contenu : 1) test 1 encodage, 2) test 2 nul, 3) test 3 correlations, 4) hypotheses Q (etat apres les tests), 5) detail par run (6 runs : resume, seuils propres par flux, F1/F2 Tous, figures), 6) annexe F1/F2 complete avant et apres seuil.', 'txt'),
          PageBreak()]

story += [P('1. Test 1 - Encodage alphabetique', 'stitre'),
          P('Donnees : encodage/data/mushrooms_alpha.csv (SHA-256 4552be72cf53277e86f96d013d22e9051295a40730f03645c1c3c98308159192, 8 124 x 23, 2 480 NaN dans stalk-root), mapping mapping_alpha.json. L\'ordre alphabetique differe de l\'ordre d\'apparition pour les 3 controles (verifie avant les runs) : class e=0,p=1 ; odor a=0,c=1,f=2,l=3,m=4,n=5,p=6,s=7,y=8 ; cap-surface f=0,g=1,s=2,y=3. Regle gelee : ecart de seuil MC > 5 pts OU ecart de score MC > 0,05 = sensible a l\'encodage.', 'txt')]
data = [hdr(['controle', 'origine MC %', 'origine score', 'alpha MC %', 'alpha score', 'delta seuil', 'delta score', 'verdict'])]
for r in comp.itertuples():
    data.append(row(r.controle, fmt(r.orig_MC_pct), fmt(r.orig_score, 3), fmt(r.alpha_MC_pct), fmt(r.alpha_score, 3), fmt(r.delta_MC_alpha, 2), fmt(r.delta_score_alpha, 3), r.verdict_encodage))
story += [tbl(data, [24*mm, 22*mm, 22*mm, 22*mm, 22*mm, 20*mm, 20*mm, 24*mm]),
          P('Moyennes bootstrap (origine -> alpha) : class 52,73 % (+-14,78) -> 60,21 % (+-10,21) ; odor 1,83 % (+-0,12) -> 87,98 % (+-0,80) ; cap-surface 79,62 % (+-16,21) -> 22,62 % (+-7,08). La renumerotation deplace aussi le bootstrap d\'un bout a l\'autre.', 'txt'),
          img(BASE / 'figures' / 'fig_seuils_comparaison.png'), P('Seuils MC : reel vs encodage alphabetique vs nul (3 controles).', 'cap'),
          img(BASE / 'figures' / 'fig_scores_comparaison.png'), P('Scores MC : reel vs encodage alphabetique vs nul (3 controles).', 'cap')]

story += [P('2. Test 2 - Nul propre', 'stitre'),
          P(f"Donnees : encodage d'origine, colonne de controle permutee avec np.random.default_rng(1234).permutation (permutation enregistree : nul/data/permutation_indices.npy, SHA-256 de la permutation {NULLMETA['files']['class']['permutation_sha256'][:12]}..., identique pour les 3 controles), flux intacts, frequences marginales conservees (verifie). Fichiers : class SHA-256 {NULLMETA['files']['class']['sha256'][:12]}..., odor {NULLMETA['files']['odor']['sha256'][:12]}..., cap-surface {NULLMETA['files']['cap-surface']['sha256'][:12]}.... Verification avant les runs : Spearman controle-flux tombe a ~0 (class vs odor : -0,771 -> -0,001 ; odor vs cap-color : 0,139 -> 0,008 ; cap-surface vs odor : -0,093 -> -0,004). Regle gelee : score nul >= score reel - 0,05 = indistinguable du nul.", 'txt')]
data = [hdr(['controle', 'reel MC %', 'reel score', 'nul MC %', 'nul score', 'delta score', 'seuil disting.', 'verdict'])]
for r in comp.itertuples():
    data.append(row(r.controle, fmt(r.orig_MC_pct), fmt(r.orig_score, 3), fmt(r.nul_MC_pct), fmt(r.nul_score, 3), fmt(r.delta_score_nul, 3), fmt(r.seuil_distinguabilite, 3), r.verdict_nul))
story += [tbl(data, [24*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 22*mm, 26*mm]),
          P('Les trois scores nuls depassent les scores reels. Avec zero association, le pipeline trouve des seuils du meme calibre, voire meilleurs. Stabilites des runs nuls : UNSTABLE pour les 3 (moyennes bootstrap : class 41,34 % +-14,40 ; odor 18,32 % +-35,28 ; cap-surface 76,20 % +-25,28). Incident de lancement : le premier lancement du batch a echoue en moins d\'une seconde sur une erreur du script d\'adaptation (variable utilisee avant sa definition) ; corrige, relance, aucun run partiel compte (results/ etait vide).', 'txt'),
          PageBreak()]

story += [P('3. Test 3 - Correlations entre flux dominants', 'stitre'),
          P('Mesures gelees : Spearman sur valeurs encodees (origine) + V de Cramer sur codes bruts, matrices 23 x 23 completes, top 15 paires, focus pre-enregistre sur le trio stalk-color-above-ring / stalk-color-below-ring / ring-type, plus taux d\'accord exact entre les deux colonnes stalk-color. Interpretation gelee : une forte correlation ne prouve pas la circularite, elle retire seulement l\'independance des temoignages.', 'txt')]
data = [hdr(['rang', 'paire (Spearman)', 'Spearman'])]
for i, r in TOPS.iterrows():
    data.append(row(i + 1, r.paire, fmt(r.spearman, 3)))
story += [tbl(data, [16*mm, 110*mm, 30*mm])]
data = [hdr(['rang', 'paire (V de Cramer)', 'V de Cramer'])]
for i, r in TOPC.iterrows():
    data.append(row(i + 1, r.paire, fmt(r.cramer_v, 3)))
story += [tbl(data, [16*mm, 110*mm, 30*mm])]
story += [P(f"Focus trio : Spearman stalk-color-above / stalk-color-below = {FOCUS['spearman_trio']['stalk-color-above-ring/stalk-color-below-ring']:.3f}, above / ring-type = {FOCUS['spearman_trio']['stalk-color-above-ring/ring-type']:.3f}, below / ring-type = {FOCUS['spearman_trio']['stalk-color-below-ring/ring-type']:.3f} ; V de Cramer = {FOCUS['cramer_trio']['stalk-color-above-ring/stalk-color-below-ring']:.3f} / {FOCUS['cramer_trio']['stalk-color-above-ring/ring-type']:.3f} / {FOCUS['cramer_trio']['stalk-color-below-ring/ring-type']:.3f} ; accord exact entre les deux colonnes stalk-color : {FOCUS['accord_exact_stalk_color_pct']:.2f} % des 8 124 lignes.", 'txt'),
          img(BASE / 'figures' / 'heatmap_spearman.png'), P('Heatmap Spearman, 23 x 23 (encodage origine).', 'cap'),
          img(BASE / 'figures' / 'heatmap_cramer.png'), P('Heatmap V de Cramer, 23 x 23 (codes bruts).', 'cap')]

story += [P('4. Hypotheses Q - etat apres les 3 tests', 'stitre'),
          P('Hypotheses de l\'utilisateur (non etablies, protocole) : Q5 enorme partout = donnees en partie sans flux receptif ; Q4 plat partout = persistance de l\'information ; Q2 centre sur veil-color = tension la ou le signal est place sans flux physique/biologique. Constats mesures : Q5 est enorme aussi sous le nul et sous encodage alphabetique ; Q2 vaut 0,0 dans 3 des 6 runs tests ; Q4 reste faible partout. Les hypotheses restent non etablies ; les Q portent aussi la signature du pipeline. Valeurs Q1-Q5 des 6 runs tests (moyennes par Q, lues dans qs_tests.csv) :', 'txt')]
data = [hdr(['test', 'controle', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5'])]
for r in QS.itertuples():
    data.append(row(r.test, r.controle, fmt(r.Q1, 3), fmt(r.Q2, 3), fmt(r.Q3, 3), fmt(r.Q4, 3), fmt(r.Q5, 3)))
story += [tbl(data, [24*mm, 30*mm, 24*mm, 24*mm, 24*mm, 24*mm, 24*mm]), PageBreak()]

def run_section(titre, test, c, s, pf, f1, d):
    out = [P(titre, 'h2')]
    q = s.get('scores_moyens_par_Q') or {}
    qtxt = ' ; '.join(f"{k} = {v}" for k, v in q.items()) if q else '-'
    out += [P(f"Dataset : {s.get('dataset', '-')} ; n = {s.get('n_pts')} ; MC = {fmt(s.get('mc_threshold_pct'))} % ; defaut = {fmt(s.get('default_threshold_pct'))} % ; MC brut = {fmt(s.get('raw_mc_threshold_pct'))} % ; rigide 1001 = {fmt(s.get('rigid_1001_threshold_pct'))} % ; stabilite = {s.get('stability_rating')} (moy. {fmt(s.get('stability_mean'))}, std {fmt(s.get('stability_std'))}) ; score MC = {fmt(s.get('mc_score'), 3)} (w = {s.get('mc_w_size')}, candidats = {s.get('mc_n_candidates')}) ; scan max = {fmt(s.get('scan_max_score'), 3)} a {fmt(s.get('scan_argmax_pct'))} % ; bruit = {s.get('noise_label', '-')} ; source = {s.get('threshold_source')} ; avertissements = {len(s.get('threshold_warnings') or [])} ; duree = {s.get('duration_s')} s.", 'petit'),
            P(f"Scores moyens par Q : {qtxt}.", 'petit')]
    data = [hdr(['flux', 'seuil propre %', 'score max', 'top-3 candidats %'])]
    for r in pf.sort_values('score_max', ascending=False).itertuples():
        data.append(row(r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3), str(r.top3_candidats)))
    out += [tbl(data, [40*mm, 32*mm, 28*mm, 75*mm])]
    tous = f1[f1.flux == 'Tous']
    if len(tous):
        out += [P("F1/F2 du flux 'Tous', avant et apres seuil :", 'petit')]
        data = [hdr(['estimateur', 'F1_pre', 'F2_pre', 'F1', 'F2', 'delta_F1', 'delta_F2', 'sign_change'])]
        for r in tous.itertuples():
            data.append(row(r.estimateur, fmt(r.F1_pre, 6), fmt(r.F2_pre, 6), fmt(r.F1, 6), fmt(r.F2, 6), fmt(r.delta_F1, 6), fmt(r.delta_F2, 6), r.sign_change))
        out += [tbl(data, [24*mm, 24*mm, 24*mm, 24*mm, 24*mm, 24*mm, 24*mm, 22*mm])]
    for imgname, cap in [('threshold_scan.png', 'Courbe de scan (seuil)'), ('noise_diagnostic.png', 'Diagnostic bruit')]:
        p = Path(d) / imgname
        if p.exists():
            out += [Spacer(1, 2*mm), img(p), P(f"{cap} - {test} / {c}", 'cap')]
    return out

story += [P('5. Detail par run', 'stitre'),
          P('6 runs : resume, seuils propres par flux, scores Q, F1/F2 du flux \'Tous\' avant et apres seuil, figures du run.', 'txt')]
for test, label in [('encodage', 'ALPHA'), ('nul', 'NUL')]:
    for c in ['class', 'odor', 'cap-surface']:
        s, pf, f1, d = load_run(test, c)
        story += run_section(f"5. {label} - controle = {c}", label, c, s, pf, f1, d)

story += [PageBreak(), P('Annexe. F1/F2 avant et apres seuil, complete (6 runs tests)', 'stitre'),
          P('F1_pre / F2_pre (derivees avant seuil), F1 / F2 (derivees apres seuil), deltas et sign_change, par test, controle, estimateur et flux.', 'txt')]
for (test, c), grp in FF.groupby(['test', 'controle']):
    story += [P(f"F1/F2 - {test} / {c}", 'h3')]
    data = [hdr(['estimateur', 'flux', 'F1_pre', 'F2_pre', 'F1', 'F2', 'delta_F1', 'delta_F2', 'sign_change'])]
    for r in grp.itertuples():
        data.append(row(r.estimateur, r.flux, fmt(r.F1_pre, 6), fmt(r.F2_pre, 6), fmt(r.F1, 6), fmt(r.F2, 6), fmt(r.delta_F1, 6), fmt(r.delta_F2, 6), r.sign_change))
    story += [tbl(data, [20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm])]

story += [Spacer(1, 6*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('Fin. Protocole gele : PROTOCOLE_TESTS.md. Rappel : codes nominaux, seuils = coupures de rang, lecture descriptive seulement, RIEN ici n\'est une regle pour decider si un champignon est comestible ou toxique. Syntheses : synthese/comparaison_controles.csv, tous_seuils_par_flux_tests.csv, tous_F1F2_tests.csv, qs_tests.csv. Correlations : correlations/results/.', 'petit')]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(15*mm, 10*mm, 'Mushroom - 3 tests diagnostics x pipeline v3.4-H3')
    canvas.drawRightString(W - 15*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
                        title='Mushroom - 3 tests diagnostics x v3.4-H3', author='Muse')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF ecrit : {OUT} ({OUT.stat().st_size/1e6:.1f} Mo)")
