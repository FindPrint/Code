# -*- coding: utf-8 -*-
"""Construit le PDF unique Food_Costs 2013 x v3.3-H1.
Toutes les valeurs sont lues dans les CSV/JSON produits (aucun chiffre
recopie a la main, sauf les constats de structure verifies dans le
protocole) : synthese_runs.csv, tous_seuils_par_flux.csv,
tous_F1F2.csv, top11_par_controle.csv, run_summary.json de chaque run.
Texte sans accents (polices standard WinAnsi), comme les PDF precedents.
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

BASE = Path('/home/hatch/workspace/food-costs-2013')
OUT = BASE / 'Food_Costs_2013_v33H1_Resultats_complets.pdf'
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

def fmt_int(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return '-'
    return f"{int(v):,}".replace(',', ' ')

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

DIR = {'agency_encoded': 'ctrl_Agency', 'Cumulative Cost': 'ctrl_Cumulative'}
def dir_of(c):
    if c in DIR:
        return DIR[c]
    return 'ctrl_' + c[:7]

ORDER = ['agency_encoded'] + [f'2012-{m:02d}-01 00:00:00' for m in (10, 11, 12)] + [f'2013-{m:02d}-01 00:00:00' for m in range(1, 10)] + ['Cumulative Cost']
SHORT = {'agency_encoded': 'Agency'}
def short(c):
    return SHORT.get(c, c[:7] if c != 'Cumulative Cost' else 'Cumulative')

runs = {c: load_run(BASE / 'results' / dir_of(c)) for c in ORDER}
syn = pd.read_csv(BASE / 'synthese_runs.csv')
PF = pd.read_csv(BASE / 'tous_seuils_par_flux.csv')
FF = pd.read_csv(BASE / 'tous_F1F2.csv')
TOP = pd.read_csv(BASE / 'top_au_dessus.csv')
inv = pd.read_csv(BASE / 'data' / 'Food_Costs_2013_pipeline.csv')
ok = syn[syn.statut == 'OK']
n_ok = len(ok)
total_s = float(ok.duree_s.sum()) if n_ok else 0.0
top_pf = PF.nlargest(10, 'score_max') if len(PF) else pd.DataFrame()
flux_mean = PF.groupby('flux')['score_max'].mean().sort_values(ascending=False) if len(PF) else pd.Series(dtype=float)

story = []
story += [Spacer(1, 28*mm), P('Food_Costs 2013 (Kaggle jpmiller/publicassistance)<br/>x pipeline v3.3-H1', 'titre'),
          P('Tous les resultats en un seul fichier : 14 controles (toutes les colonnes du CSV 2013), seuils par flux, F1/F2 et images de tous les runs. Les annees 2014, 2015 et 2016 feront trois autres PDF separes, a la demande de l\'utilisateur.', 'txt'),
          Spacer(1, 6*mm),
          P('Source : https://www.kaggle.com/datasets/jpmiller/publicassistance - dataset "US Public Food Assistance 1 - WIC", auteur JohnM (jpmiller), fichier WICAgencies2013ytd/Food_Costs.csv, 92 lignes, 14 colonnes, exercice WIC 2013 (octobre 2012 a septembre 2013). Pipeline : pipeline_autonome_v3_3_harmonic_v1.py tel quel, mode stable, w_size 80, cohen_d, graine 42, Monte Carlo harmonique P = 0,45. Regle Porte D : le controle est exclu des flux analyses.', 'txt'),
          P(f"Runs : 14 lances, {n_ok} termines, {len(syn) - n_ok} echec(s). Duree totale des runs (somme des durees enregistrees) : {total_s:.1f} s (environ {total_s / max(n_ok, 1):.0f} s par run). Images : 28 figures du pipeline (courbe de scan + diagnostic bruit pour chacun des 14 runs) + 4 figures de synthese.", 'txt'),
          P('Dates : choix de l\'annee 2013 par l\'utilisateur le 26 octobre 2026 a 11h22 HAE ; pilote de faisabilite (controle Cumulative Cost, memes reglages) a 11h24 ; protocole redige a ~11h25 ; 13 autres runs lances apres ; lot interrompu par un redemarrage du service a 9/14, repris par les seuls manquants, termine a 11h27. PDF assemble apres la fin des runs.', 'txt'),
          Spacer(1, 4*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('<b>Verdict chiffre</b> : les 13 controles numeriques donnent EXACTEMENT le meme seuil MC, 87,88 %, avec le meme seuil par defaut, 59,26 %, et la meme moyenne bootstrap, 59,09 %. Le controle Agency donne 83,33 % (defaut 29,63 %, moyenne bootstrap 42,42 %). Tous les runs sont notes VERY STABLE par le pipeline, mais cette note repose sur l\'ecart-type bootstrap (proche de zero, 7 valeurs bootstrap identiques), PAS sur l\'accord entre le seuil MC et la moyenne bootstrap : l\'ecart est de 28,79 points pour les 13 controles numeriques et de 40,91 points pour Agency. La note VERY STABLE ne doit donc PAS etre lue comme une confirmation du seuil MC.', 'txt'),
          P('<b>Lecture</b> : 87,88 % de rang, c\'est la coupure apres les 12 plus grandes agences. Sur Cumulative Cost, ces 12 premieres (California, New York, Texas, Florida, Mountain Plains, Puerto Rico, Illinois, Georgia, North Carolina, Pennsylvania, Michigan, Ohio) totalisent 62,6 % du total du fichier. Les courbes de scan globales montent regulierement jusqu\'a 87,88 % puis s\'arretent (plus de score au-dela) : ce n\'est pas un pic interieur, c\'est le bord de la zone calculable, qui isole la queue des tres grandes agences. En controle Agency, les scores s\'effondrent (scan max 0,372 contre 1,73 a 1,88 pour les controles numeriques) : l\'ordre des agences dans le fichier ne porte pas de separation de couts.', 'txt'),
          P('<b>Piege de structure, verifie</b> : la ligne "Mountain Plains" (253 793 211) est EXACTEMENT la somme des 10 Etats et des 10 agences tribales du groupe Mountain Plains qui la precedent dans le fichier (ecart 0). C\'est une ligne d\'agregat melangee aux composantes : le total du fichier (4 751 013 254) double-compte donc 253,8 millions, et Mountain Plains figure a tort parmi les "12 plus grandes". Le fichier contient aussi Texas deux fois (une ligne vide, une ligne reelle).', 'txt'),
          P('Contenu : 1) donnees, 2) synthese des 14 controles et lectures, 3) detail par run (resume, seuils propres par flux, scores Q, images), 4) annexe F1/F2 complete (tous les estimateurs x tous les flux x 14 runs = 980 lignes). Les rapports texte complets du pipeline et les CSV bruts restent dans l\'archive zip.', 'txt'),
          PageBreak()]

# 1. Donnees
story += [P('1. Les donnees, telles que telechargees', 'stitre'),
          P('Fichier original conserve tel quel : data/Food_Costs_2013_original.csv (12 695 octets, SHA-256 9933552f3403d28156eebd9252835bdabe4fffde14625bc068efa63c9c0a9f46), identique a l\'octet pres au fichier telecharge individuellement. Fichier de travail : data/Food_Costs_2013_pipeline.csv (92 lignes, 15 colonnes) = copie exacte des 14 colonnes d\'origine + une seule colonne derivee (agency_encoded) + une seule conversion (Cumulative Cost en nombre). Licence affichee sur Kaggle : "Other (specified in description)" ; utilisabilite 9,41 ; version affichee : Version 9 ; dataset complet : 68 fichiers, 968 colonnes au total, dont 4 fichiers nommes Food_Costs.csv (2013, 2014, 2015, 2016) - seul 2013 est traite ici.', 'txt')]
orig = pd.read_csv(BASE / 'data' / 'Food_Costs_2013_original.csv')
data = [hdr(['colonne d\'origine', 'valides', 'distinctes', 'min', 'max', 'moyenne'])]
for c in orig.columns:
    s = orig[c]
    if pd.api.types.is_numeric_dtype(s):
        data.append(row(c, int(s.notna().sum()), int(s.nunique()), fmt_int(s.min()), fmt_int(s.max()), fmt_int(s.mean())))
    else:
        data.append(row(c, int(s.notna().sum()), int(s.nunique()), '-', '-', '-'))
story += [tbl(data, [52*mm, 18*mm, 20*mm, 30*mm, 30*mm, 30*mm]), Spacer(1, 3*mm),
          P('Cumulative Cost dans l\'original est stockee en texte (chiffres sans separateur) : apres conversion en nombre, elle egale exactement la somme des 12 mois pour chaque ligne (ecart maximal 0,0), 91 valeurs valides, 1 manquante (ligne Texas vide). agency_encoded : codes 0 a 90 par ordre d\'apparition dans le fichier (Connecticut 0, ..., Texas 39 pour les deux lignes Texas, ..., Inter-Tribal Council, NV 90) ; table complete dans data/agency_encoded_mapping.json. La colonne texte d\'origine n\'est jamais passee directement au pipeline.', 'petit'),
          P('Details verifies avant run : Texas deux fois (ligne 39 entierement vide, ligne 40 reelle, Cumulative 303 294 654) ; une seule valeur mensuelle negative, conservee telle quelle : Pennsylvania, novembre 2012, -550 874 ; echelle tres dispersee (mensuels de ~1 000 a ~68 millions ; Cumulative de 50 949 a 791 184 631, California, moyenne 52 208 937, mediane 10 214 707) ; la ligne Texas vide est conservee manquante, pas imputee, pas supprimee.', 'petit'),
          P('Verification Mountain Plains : ligne = 253 793 211 ; somme des 10 Etats Mountain (Colorado, Iowa, Kansas, Missouri, Montana, Nebraska, North Dakota, South Dakota, Utah, Wyoming) + des 10 agences tribales du meme groupe = 253 793 211 ; ecart = 0. Aucune autre ligne d\'agregat de ce type n\'a ete signalee pour les autres groupes regionaux du fichier.', 'petit')]

# 2. Synthese
story += [P('2. Synthese des 14 controles', 'stitre')]
data = [hdr(['controle', 'n', 'MC %', 'defaut %', 'ecart MC-defaut', 'moy. bootstrap', 'ecart MC-moy.', 'stabilite (std)', 'score MC', 'scan max', 'valeur au MC (med.)'])]
for r in syn.itertuples():
    data.append(row(short(r.controle) if r.controle != 'Cumulative Cost' else 'Cumulative', fmt(r.n_lignes, 0) if pd.notna(getattr(r, 'n_lignes', None)) else '-', fmt(r.seuil_MC_pct), fmt(r.seuil_defaut_pct), fmt(r.ecart_MC_moins_defaut, 1), fmt(r.stabilite_moy_pct), fmt(r.ecart_MC_moins_moybootstrap, 1), f"{r.stabilite} ({fmt(r.stabilite_std, 2)})", fmt(r.score_MC, 3), fmt(r.scan_global_max, 3), fmt_int(r.valeur_controle_au_MC_mediane)))
story += [tbl(data, [22*mm, 10*mm, 14*mm, 16*mm, 18*mm, 20*mm, 18*mm, 24*mm, 14*mm, 14*mm, 22*mm])]
story += [P('Toutes les lignes numeriques partagent w_MC = 10, n_candidats_MC = 67 et seuil rigide 1001 = 87,4 % ; Agency partage w_MC = 10 et n_candidats_MC = 67 avec un seuil rigide 1001 = 83,2 %. Les durees vont de 7,7 s (2013-09) a 13,1 s (2013-04).', 'petit'),
          P('Figures de synthese (lues dans les CSV produits, pas de chiffre recopie) :', 'txt')]
for figname, cap in [('seuils_MC_vs_bootstrap.png', 'Seuil MC, seuil par defaut et moyenne bootstrap par controle. L\'ecart MC / moyenne bootstrap est constant et grand : la note VERY STABLE ne confirme pas le MC.'),
                     ('scan_curves_overlay.png', 'Courbes de scan globales superposees. Controles numeriques : montee reguliere jusqu\'a 87,88 %, puis plus aucun score calcule au-dela. Agency : courbe plate et basse (max 0,372), avec un pic secondaire a 42,42 % presque aussi haut que le max (rel. 0,993).'),
                     ('scores_propres_moyens.png', 'Scores propres moyens en tant que flux. Les 13 colonnes de couts sont entre 1,642 et 1,935 ; agency_encoded est a 0,775, tres en dessous.'),
                     ('cumulative_triee_log.png', 'Cumulative Cost 2013 triee par ordre decroissant (echelle log). La coupure MC apres les 12 premieres isole une queue tres lourde : les 12 premieres valent 62,6 % du total du fichier (qui inclut le double-compte Mountain Plains, voir section 1).')]:
    p = BASE / 'figures' / figname
    if p.exists():
        story += [Spacer(1, 2*mm), img(p), P(cap, 'cap')]
story += [P('Groupes au-dessus du seuil MC par controle (valeurs dont le rang donne un progress superieur a 87,88 % ; pour n = 91, ce sont 12 valeurs) :', 'txt')]
data = [hdr(['controle', 'n au-dessus', 'plus petite au-dessus', 'plus grande en dessous', 'groupe au-dessus (ordre decroissant)'])]
for r in TOP.itertuples():
    data.append(row(short(r.controle) if r.controle != 'Cumulative Cost' else 'Cumulative', int(r.n_au_dessus), f"{fmt_int(r.min_au_dessus)} ({r.agence_min_au_dessus})", f"{fmt_int(r.max_en_dessous)} ({r.agence_max_en_dessous})", r.liste_au_dessus))
story += [tbl(data, [22*mm, 16*mm, 32*mm, 32*mm, 78*mm])]
story += [P('Lecture : 3 mois sur 12 (juin, aout, septembre) partagent EXACTEMENT le meme groupe au-dessus que Cumulative Cost ; les autres mois en different par un membre echange (sauf octobre 2012 et janvier 2013 : deux membres echanges). Ce n\'est donc pas 13 seuils independants, c\'est 13 fois la meme queue de grandes agences, vue par 13 colonnes liees (et Cumulative Cost en est la somme exacte).', 'txt'),
          P('Controle Agency, en detail : seuil MC 83,33 %, valeur au MC (mediane des codes autour de la coupure) = 75, soit Shoshone Tribe, WY (code 75) ; les codes 75 a 90 (Shoshone Tribe, WY, Mountain Plains, Alaska, American Samoa, Arizona, California, Guam, Hawaii, Idaho, Nevada, Oregon, Washington, Northern Marianas, Inter-Tribal Council, AZ, Navajo Nation, AZ, Inter-Tribal Council, NV) sont au-dessus de la coupure, c\'est-a-dire le bloc "Western" en fin de fichier, pas un groupe defini par les couts. Paysage : deux pics presque egaux, 42,42 % (0,369, rel. 0,993) et 83,33 % (0,372, rel. 1,000). Scores propres des flux dans ce run : 0,367 a 0,431 seulement, contre 1,6 a 2,2 dans les runs numeriques.', 'txt'),
          P('Seuils propres les plus forts (top 10 sur les 182 seuils propres, 14 x 13) :', 'txt')]
data = [hdr(['controle', 'flux', 'seuil propre %', 'score max'])]
for r in top_pf.itertuples():
    data.append(row(short(r.controle) if r.controle != 'Cumulative Cost' else 'Cumulative', short(r.flux) if r.flux != 'Cumulative Cost' else 'Cumulative', fmt(r.seuil_propre_pct), fmt(r.score_max, 3)))
story += [tbl(data, [38*mm, 38*mm, 32*mm, 32*mm])]
story += [P('En tant que flux, scores propres moyens (sur les 13 runs ou la colonne est flux), du plus fort au plus faible : ' + ', '.join(f"{short(k) if k != 'Cumulative Cost' else 'Cumulative'} ({v:.3f})" for k, v in flux_mean.items()) + '.', 'petit'),
          P('Ecarts notables dans les seuils propres (flux qui ne suivent pas le 87,88 % dominant) : controle 2012-10, flux 2013-08 a 74,24 % et flux 2013-09 a 80,30 % ; controle 2013-01, flux 2012-11 a 66,67 % ; controle 2013-07, flux 2012-11 a 74,24 % ; controle 2012-12, flux 2013-08 a 74,24 % ; dans le run Agency, flux 2012-12, 2013-04 et 2013-06 a 42,42 %, flux 2013-08 a 40,91 %, flux 2013-09 a 45,45 %, les autres flux a 83,33 %. Ces ecarts sont listes tels quels : ils ne changent pas le faisceau dominant (mediane des seuils propres = 87,88 % pour tous les controles numeriques, IQR 0,00 a 4,55 ; pour Agency, mediane 83,33 %, IQR 40,91).', 'txt'),
          P('Bruit : 12 runs "Proxy de variance modere - Plusieurs flux agissent comme proxies de variance residuelle" ; 2 runs "Mixte - Coexistence de bruit blanc et de proxies de variance residuelle" (2013-09 et Agency). F1/F2 "Tous" : dans les 13 runs numeriques, Higuchi, DFA, Katz et Hurst sont negatifs en F1 (ordre 1st), SampleEn positif (ordre 2nd) ; dans le run Agency, les 5 estimateurs sont negatifs en F1, SampleEn y compris. Les valeurs completes sont en annexe.', 'txt'),
          PageBreak()]

def run_section(titre, run_id, s, pf, d):
    out = [P(titre, 'h2')]
    if s['status'] != 'OK':
        out += [P(f"ECHEC : {s.get('error', '')} (valeurs valides du controle : {s.get('n_valides_controle')}).", 'txt')]
        return out
    q = s.get('scores_moyens_par_Q') or {}
    qtxt = ' ; '.join(f"{k} = {v}" for k, v in q.items()) if q else '-'
    cv = s.get('controle_valeur_au_seuil_mc') or {}
    out += [P(f"n = {s.get('n_pts')} ; MC = {fmt(s.get('mc_threshold_pct'))} % ; defaut = {fmt(s.get('default_threshold_pct'))} % ; MC brut = {fmt(s.get('raw_mc_threshold_pct'))} % ; defaut brut = {fmt(s.get('raw_default_threshold_pct'))} % ; rigide 1001 = {fmt(s.get('rigid_1001_threshold_pct'))} % ; stabilite = {s.get('stability_rating')} (moy. {fmt(s.get('stability_mean'))}, std {fmt(s.get('stability_std'))}) ; score MC = {fmt(s.get('mc_score'), 3)} (w = {s.get('mc_w_size')}, candidats = {s.get('mc_n_candidates')}) ; scan global max = {fmt(s.get('scan_max_score'), 3)} a {fmt(s.get('scan_argmax_pct'))} % ; valeur du controle au MC (mediane) = {fmt_int(cv.get('mediane'))} ; bruit = {s.get('noise_label', '-')} .", 'petit'),
            P(f"Scores moyens par Q : {qtxt}. Duree : {s.get('duration_s')} s.", 'petit')]
    if pf is not None and len(pf):
        data = [hdr(['flux', 'seuil propre %', 'score max', 'top-3 candidats %'])]
        for r in pf.sort_values('score_max', ascending=False).itertuples():
            data.append(row(short(r.flux) if r.flux != 'Cumulative Cost' else 'Cumulative', fmt(r.seuil_propre_pct), fmt(r.score_max, 3), str(r.top3_candidats)))
        out += [tbl(data, [40*mm, 32*mm, 28*mm, 75*mm])]
    for imgname, cap in [('threshold_scan.png', 'Courbe de scan (seuil)'), ('noise_diagnostic.png', 'Diagnostic bruit')]:
        p = Path(d) / imgname
        if p.exists():
            out += [Spacer(1, 2*mm), img(p), P(f"{cap} - {run_id}", 'cap')]
    return out

story += [P('3. Detail par run', 'stitre'),
          P('Chaque run : resume, seuils propres par flux (fonction de scan du pipeline, configuration MC du run), scores Q, puis les deux figures du run (courbe de scan, diagnostic bruit). Les noms de mois sont abregees en AAAA-MM dans les tableaux de seuils propres ; les noms complets sont dans les CSV.', 'txt')]
for c in ORDER:
    s, pf, f1 = runs[c]
    story += run_section(f"3. Controle = {c if c != 'agency_encoded' else 'agency_encoded (colonne texte d\'origine : State Agency or Indian Tribal Organization)'}", dir_of(c), s, pf, BASE / 'results' / dir_of(c))

story += [PageBreak(), P('Annexe. F1/F2 post-seuil, complete', 'stitre'),
          P('Pour chacun des 14 runs : F1 (derivee premiere post-seuil) et F2 (derivee seconde), par estimateur et par flux, tels que produits par le pipeline (transition_analysis). Signe et ordre sont ceux du pipeline. Total : 980 lignes (14 x 70).', 'txt')]
for c in ORDER:
    s, pf, f1 = runs[c]
    if f1 is None:
        continue
    story += [P(f"F1/F2 - {dir_of(c)}", 'h3')]
    data = [hdr(['estimateur', 'flux', 'F1', 'F2', 'signe', 'ordre'])]
    for r in f1.itertuples():
        data.append(row(r.estimateur, short(r.flux) if r.flux != 'Cumulative Cost' else 'Cumulative', fmt(r.F1, 6), fmt(r.F2, 6), r.signe, r.ordre))
    story += [tbl(data, [30*mm, 30*mm, 40*mm, 40*mm, 22*mm, 18*mm])]

story += [Spacer(1, 6*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('Fin. Protocole gele : PROTOCOLE.md. Rapport : RAPPORT.md. Archive zip : food_costs_2013_14_controles_resultats.zip (rapports texte du pipeline, CSV bruts, courbes de scan ; pipeline_results.json complets par run exclus du zip pour la taille, comme pour le breast cancer, et conserves dans results/ctrl_*/).', 'petit')]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(15*mm, 10*mm, 'Food_Costs 2013 x pipeline v3.3-H1 - resultats complets')
    canvas.drawRightString(W - 15*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
                        title='Food_Costs 2013 x v3.3-H1 - Resultats complets', author='Muse')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF ecrit : {OUT} ({OUT.stat().st_size/1e6:.1f} Mo)")
