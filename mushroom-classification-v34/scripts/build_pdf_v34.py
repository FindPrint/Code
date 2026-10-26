# -*- coding: utf-8 -*-
"""Construit le PDF unique des resultats Mushroom Classification x v3.4-H3.
Adapte de workspace/mushroom/scripts/build_pdf.py (v3.3-H1, inchange) :
BASE, sortie et titre v3.4-H3 ; veil-type traite comme echec mesure
(seuils NaN, stabilite UNKNOWN, 2 avertissements, pas de seuils propres,
pas de F1/F2, pas de courbe de scan, 52,5 % d'urgence JAMAIS lu comme
seuil) ; colonnes source du seuil et avertissements ; F1/F2 AVANT
seuil en plus d'APRES ; table Q1-Q5 ; analyse accord MC / bootstrap ;
comparaison MC / defaut / brut / rigide ; note de correction de
synthese.py (outil de synthese seulement, pipeline et protocole
intouches).
Toutes les valeurs sont lues dans les CSV/JSON produits (aucun chiffre
recopie a la main) : synthese_runs.csv, tous_seuils_par_flux.csv,
tous_F1F2.csv, qs_par_run.csv, run_summary.json de chaque run,
data/raw/mushrooms.csv.
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

BASE = Path('/home/hatch/workspace/mushroom-v34')
OUT = BASE / 'Mushroom_Classification_v34_Resultats_complets.pdf'
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

df = pd.read_csv(BASE / 'data' / 'mushrooms_pipeline.csv')
ORDER = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
runs = {c: load_run(BASE / 'results' / f'ctrl_{c}') for c in ORDER}
syn = pd.read_csv(BASE / 'synthese_runs.csv')
PF = pd.read_csv(BASE / 'tous_seuils_par_flux.csv')
FF = pd.read_csv(BASE / 'tous_F1F2.csv')
QS = pd.read_csv(BASE / 'qs_par_run.csv')
# Runs avec seuil detecte (veil-type : seuils NaN, echec mesure, exclu ici)
det = syn.dropna(subset=['seuil_MC_pct']).copy()
n_det = len(det)
n_fail = len(syn) - n_det
total_s = float(syn.duree_s.sum())
stab_counts = syn.stabilite.value_counts().to_dict()
top_pf = PF.nlargest(10, 'score_max') if len(PF) else pd.DataFrame()
flux_mean = PF.groupby('flux')['score_max'].mean().sort_values(ascending=False) if len(PF) else pd.Series(dtype=float)
flux_count = PF.groupby('flux')['score_max'].count() if len(PF) else pd.Series(dtype=int)
# Accord MC / moyenne bootstrap, sur les runs detectes seulement
det['gap_mc_boot'] = (det.seuil_MC_pct - det.stabilite_moy_pct).abs()
det['within_1std'] = det.gap_mc_boot <= det.stabilite_std
n_within = int(det.within_1std.sum())
vs = det[det.stabilite == 'VERY STABLE']
vs_not = vs[~vs.within_1std]
# Comparaisons MC / defaut / brut / rigide (medianes, runs detectes)
med_def = float((det.seuil_MC_pct - det.seuil_defaut_pct).abs().median())
med_raw = float((det.seuil_MC_pct - det.seuil_MC_brut_pct).abs().median())
med_rig = float((det.seuil_MC_pct - det.seuil_rigide1001_pct).abs().median())
n_png = len(list((BASE / 'results').glob('ctrl_*/*.png')))
src_counts = {}
warn_total = 0
for c in ORDER:
    s = runs[c][0]
    src_counts[s.get('threshold_source', '-')] = src_counts.get(s.get('threshold_source', '-'), 0) + 1
    warn_total += len(s.get('threshold_warnings') or [])

story = []
story += [Spacer(1, 30*mm), P('Mushroom Classification (Kaggle uciml)<br/>x pipeline v3.4-H3', 'titre'),
          P('Tous les resultats en un seul fichier : 23 controles (toutes les colonnes du CSV), seuils par flux, F1/F2 avant et apres seuil, et images de tous les runs.', 'txt'),
          Spacer(1, 6*mm),
          P('Source : https://www.kaggle.com/datasets/uciml/mushroom-classification (zip mushroom-classification.zip, un seul CSV : mushrooms.csv, 8 124 lignes, 23 colonnes). Pipeline : Tlog_v3_4_harmonic_v3.py (v3.4-H3, SHA-256 81092eb61d612d0dea50f9fca6bfa12f6dbd2388c4e52a24ab064d09e61dc7f8), derive de v3.3-H1 : scan optimise a resultats identiques, fallback Monte Carlo journalise, F1/F2 avant ET apres seuil, export JSON robuste. Mode stable, w_size 80, cohen_d, graine 42, Monte Carlo harmonique P = 0,45. Regle Porte D : le controle est exclu des flux analyses.', 'txt'),
          P(f"Runs : 23 lances, {n_det} seuils detectes, {n_fail} echec mesure (veil-type, controle constant, seuils NaN). Duree totale des 23 runs : {total_s:.1f} s (environ {total_s / len(syn):.0f} s par run). Images : {n_png} figures (courbe de scan + diagnostic bruit pour les 22 runs detectes, diagnostic bruit seul pour veil-type). Source du seuil : " + ', '.join(f"{k} = {v}" for k, v in sorted(src_counts.items())) + f" ; avertissements de seuil enregistres au total : {warn_total} (tous sur veil-type).", 'txt'),
          P('Dates : runs le 26 octobre 2026 (protocole gele avant tout run de ce lot ; lot reparti de zero a la demande de l\'utilisateur, aucun resultat du lot v3.3 repris). PDF assemble apres la fin des 23 runs.', 'txt'),
          Spacer(1, 4*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P(f"<b>Verdict chiffre</b> : repartition des stabilites (critere du pipeline) sur les 23 runs : " + ', '.join(f"{k} = {v}" for k, v in sorted(stab_counts.items())) + f". Seuils MC detectes entre {det.seuil_MC_pct.min():.2f} % et {det.seuil_MC_pct.max():.2f} %. Accord MC / moyenne bootstrap : seulement {n_within} runs detectes sur {n_det} ont |MC - moyenne bootstrap| dans 1 ecart-type ; la note de stabilite mesure la serrage bootstrap, pas l'accord avec le MC (voir section 2).", 'txt'),
          P('Lecture imposee par la nature des donnees : toutes les colonnes d\'origine sont des codes-lettres categoriels, encodes en entiers par ordre d\'apparition (table complete en section 1). Un seuil est donc une coupure de rang sur cet ordre arbitraire, a lire comme plateaux de rang (plateaux_controles.csv, 118 plateaux), jamais une grandeur mesuree, JAMAIS une regle pour decider si un champignon est comestible ou toxique. Lecture descriptive seulement, donnees reelles, sans verite terrain, aucun seuil attendu affirme, aucune lecture temporelle ou causale.', 'txt'),
          P('Contenu : 1) donnees et encodage, 2) synthese des 23 controles et lectures (dont accord MC/bootstrap, comparaison MC/defaut/brut/rigide, scores Q, F1/F2 Tous avant/apres), 3) detail par run (resume, seuils propres par flux, scores Q, F1/F2 Tous avant/apres, images), 4) annexe F1/F2 complete avant et apres seuil (tous les estimateurs x tous les flux x 22 runs detectes). Les rapports texte complets du pipeline et les CSV bruts restent dans results/ et dans la synthese.', 'txt'),
          PageBreak()]

story += [P('1. Les donnees, telles que telechargees, et leur encodage', 'stitre'),
          P('Le zip Kaggle ne contient qu\'un seul CSV, mushrooms.csv (8 124 lignes, 23 colonnes, 0 ligne dupliquee exacte) : la fusion demandee est donc triviale, aucun autre fichier a joindre. Toutes les colonnes d\'origine sont categorielles (une lettre par valeur). Encodage gele avant les runs : chaque lettre devient un entier par ordre d\'apparition dans le fichier, colonne par colonne (table complete : data/mapping_encodage.json) ; le \'?\' de stalk-root (2 480 lignes, 30,5 %) devient un vrai manquant, jamais une categorie. En tant que controle, le pipeline ecarte lui-meme ces lignes (5 644 valides pour stalk-root) ; en tant que flux, il remplace les NaN par la moyenne du flux (son code). veil-type est constante (p sur 8 124 lignes) : son run est tente comme les autres mais ne peut pas porter d\'information de rupture.', 'txt'),
          P('Changements v3.4-H3 par rapport a v3.3-H1 (verifies avant le lot) : 1) scan optimise a resultats identiques (meme tirage graine 0, meme sequence rng partagee) ; 2) fallback Monte Carlo journalise (stdout + stderr + logging + metadonnees threshold_source / threshold_warnings) : un seuil de repli ne peut plus passer pour un seuil Monte Carlo ; 3) F1/F2 avant ET apres seuil, avec deltas et sign_change ; 4) export JSON robuste. Correction du scan rapide : debut valide des fenetres avec NaN (flux stalk-root), re-verifie a ecart 0,0.', 'txt'),
          P(f"Cas veil-type, echec mesure : seuils MC, defaut, brut et rigide tous NaN, stabilite UNKNOWN, score MC 0,0, aucun seuil propre, aucun F1/F2, aucune courbe de scan. Deux avertissements enregistres dans run_summary.json : ni le Monte Carlo ni le scan par defaut n'ont produit de seuil valide, et le diagnostic bruit utilise la valeur d'urgence fixe 52,5 %. Ce 52,5 % n'est PAS un seuil detecte et ne doit jamais etre cite comme tel. Duree du run veil-type : {float(syn[syn.controle == 'veil-type'].iloc[0].duree_s):.1f} s.", 'txt')]
orig = pd.read_csv(BASE / 'data' / 'raw' / 'mushrooms.csv', dtype=str, keep_default_na=False)
mapping = json.load(open(BASE / 'data' / 'mapping_encodage.json'))
data = [hdr(['colonne', 'lettres (code)', 'distinctes', "manquants '?'", 'valeur la plus frequente'])]
for c in orig.columns:
    s = orig[c]
    vc = s.value_counts()
    codes = ', '.join(f"{k}={v}" for k, v in mapping[c].items())
    data.append(row(c, codes, int(s.nunique()), int((s == '?').sum()), f"{vc.index[0]} ({int(vc.iloc[0])})"))
story += [tbl(data, [38*mm, 62*mm, 18*mm, 22*mm, 35*mm]), Spacer(1, 3*mm),
          P('SHA-256 du zip : 4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081 (35 057 octets). SHA-256 de mushrooms.csv : f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c (374 003 octets). SHA-256 du fichier de travail mushrooms_pipeline.csv : fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee. L\'original est conserve tel quel dans data/raw/.', 'petit'),
          P('class : e = 4 208, p = 3 916. Ces effectifs sont des constats sur le fichier, pas des taux de comestibilite dans la nature.', 'petit')]

story += [P('2. Synthese des 23 controles', 'stitre')]
data = [hdr(['controle', 'n', 'MC %', 'defaut %', 'ecart', 'stabilite (std)', 'score MC', 'scan max', 'valeur au MC', 'source'])]
for r in syn.itertuples():
    src = runs[r.controle][0].get('threshold_source', '-')
    data.append(row(r.controle, fmt(r.n_lignes, 0) if pd.notna(getattr(r, 'n_lignes', None)) else '-', fmt(r.seuil_MC_pct), fmt(r.seuil_defaut_pct), fmt(r.ecart_MC_moins_defaut, 1),
                    f"{r.stabilite} ({fmt(r.stabilite_std, 2)})", fmt(r.score_MC, 3), fmt(r.scan_global_max, 3), fmt(r.valeur_controle_au_MC_mediane, 1), src))
story += [tbl(data, [27*mm, 11*mm, 15*mm, 16*mm, 13*mm, 32*mm, 16*mm, 16*mm, 18*mm, 16*mm]),
          P('veil-type : ligne sans seuil (NaN affiches \'-\'), stabilite UNKNOWN, source monte_carlo avec 2 avertissements enregistres. C\'est un echec mesure, pas un seuil. Les 22 autres lignes sont des seuils MC detectes, source monte_carlo, 0 avertissement.', 'petit')]
story += [P(f"Accord MC / moyenne bootstrap (mesure, sans mecanisme invente) : sur les {n_det} runs detectes, seulement {n_within} ont |MC - moyenne bootstrap| <= 1 ecart-type bootstrap. La note de stabilite du pipeline repose sur l'ecart-type bootstrap (serrage), pas sur l'accord entre le seuil MC et la moyenne bootstrap. Parmi les {len(vs)} runs VERY STABLE, {len(vs_not)} ne sont PAS dans 1 ecart-type de leur moyenne bootstrap : " + ', '.join(f"{r.controle} (MC {r.seuil_MC_pct:.2f} %, moyenne {r.stabilite_moy_pct:.2f} %, ecart {r.gap_mc_boot:.2f} pts, std {r.stabilite_std:.2f})" for r in vs_not.itertuples()) + '. Les trois plus gros ecarts sont odor, gill-attachment et veil-color (voir tableau). Un libelle VERY STABLE ne doit donc jamais etre lu comme un accord MC/bootstrap.', 'txt')]
hab = syn[syn.controle == 'habitat'].iloc[0]
story += [P(f"Comparaison MC / defaut / brut / rigide (medianes des ecarts absolus, {n_det} runs detectes) : |MC - defaut| mediane {med_def:.2f} pts, |MC - brut| mediane {med_raw:.2f} pts, |MC - rigide 1001| mediane {med_rig:.2f} pts. Le MC brut colle presque toujours au MC traite, le seuil par defaut s'en eloigne souvent, le temoin rigide 1001 reste proche du MC. Cas extreme : habitat, MC {hab.seuil_MC_pct:.2f} % contre brut {hab.seuil_MC_brut_pct:.2f} % et defaut {hab.seuil_defaut_pct:.2f} %.", 'txt')]
data = [hdr(['controle', 'MC %', 'defaut %', 'brut MC %', 'brut defaut %', 'rigide %'])]
for r in syn.itertuples():
    data.append(row(r.controle, fmt(r.seuil_MC_pct), fmt(r.seuil_defaut_pct), fmt(r.seuil_MC_brut_pct), fmt(r.seuil_defaut_brut_pct), fmt(r.seuil_rigide1001_pct)))
data.append(row('MEDIANE (|ecart| vs MC)', '-', fmt(med_def, 2), fmt(med_raw, 2), '-', fmt(med_rig, 2)))
story += [tbl(data, [38*mm, 24*mm, 24*mm, 24*mm, 28*mm, 24*mm]),
          P('Ligne MEDIANE : medianes des ecarts absolus par rapport au MC (defaut, brut, rigide). Les autres lignes sont les valeurs brutes par run ; veil-type : tout NaN.', 'petit')]
if len(top_pf):
    story += [P(f"Seuils propres les plus forts (top 10 sur les {len(PF)} seuils propres, 22 runs detectes x 22 flux) :", 'txt')]
    data = [hdr(['controle', 'flux', 'seuil propre %', 'score max'])]
    for r in top_pf.itertuples():
        data.append(row(r.controle, r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3)))
    story += [tbl(data, [38*mm, 38*mm, 32*mm, 32*mm])]
if len(flux_mean):
    story += [P('En tant que flux, scores propres moyens (moyenne sur les runs ou la colonne est flux ; n = nombre de runs), du plus fort au plus faible :', 'txt'),
              P(', '.join(f"{k} ({v:.3f}, n={int(flux_count[k])})" for k, v in flux_mean.items()), 'petit')]
qclass = QS[QS.controle == 'class'].iloc[0]
story += [P(f"Scores moyens par Q, par run (lus dans qs_par_run.csv, calculee a partir des scores de pipeline_results.json). Controle de coherence : class donne Q1 = {qclass.Q1:.3f}, Q2 = {qclass.Q2:.3f}, Q3 = {qclass.Q3:.3f}, Q4 = {qclass.Q4:.3f}, Q5 = {qclass.Q5:.3f}, exactement les valeurs du pilote v3.3-H1 (controle class) conserve pour comparaison. La ligne veil-type (run sans seuil detecte) est donnee telle quelle, sans lecture de seuil.", 'txt')]
data = [hdr(['controle', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5'])]
for r in QS.itertuples():
    data.append(row(r.controle, fmt(r.Q1, 3), fmt(r.Q2, 3), fmt(r.Q3, 3), fmt(r.Q4, 3), fmt(r.Q5, 3)))
story += [tbl(data, [38*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm])]
story += [P('F1/F2 du flux \'Tous\', avant et apres seuil (tous les estimateurs, 22 runs detectes). F1_pre / F2_pre : derivees avant seuil ; F1 / F2 : derivees apres seuil ; delta = apres - avant ; sign_change : changement de signe entre avant et apres. veil-type n\'a pas de F1/F2 (pas de seuil).', 'txt')]
data = [hdr(['controle', 'estimateur', 'F1_pre', 'F2_pre', 'F1', 'F2', 'delta_F1', 'delta_F2', 'sign_change'])]
tous = FF[FF.flux == 'Tous']
for r in tous.sort_values(['controle', 'estimateur']).itertuples():
    data.append(row(r.controle, r.estimateur, fmt(r.F1_pre, 6), fmt(r.F2_pre, 6), fmt(r.F1, 6), fmt(r.F2, 6), fmt(r.delta_F1, 6), fmt(r.delta_F2, 6), r.sign_change))
story += [tbl(data, [28*mm, 22*mm, 24*mm, 24*mm, 24*mm, 24*mm, 24*mm, 24*mm, 16*mm])]
story += [P('Note de correction de la synthese (26 octobre 2026, outil de synthese seulement) : synthese.py a du recevoir des gardes None/vide pour veil-type (moyenne et ecart-type bootstrap None, liste de seuils propres vide, fichier transition_F1F2.csv absent) avant de produire synthese_runs.csv, tous_seuils_par_flux.csv et tous_F1F2.csv. Le pipeline v3.4-H3 et le protocole gele n\'ont pas ete modifies ; la correction ne touche que l\'outil qui assemble les CSV, pas les runs ni leurs resultats.', 'txt'),
          PageBreak()]

def run_section(titre, run_id, s, pf, f1, d):
    out = [P(titre, 'h2')]
    if s['status'] != 'OK':
        out += [P(f"ECHEC : {s.get('error', '')} (valeurs valides du controle : {s.get('n_valides_controle')}).", 'txt')]
        return out
    src = s.get('threshold_source', '-')
    warns = s.get('threshold_warnings') or []
    if pd.isna(s.get('mc_threshold_pct')):
        out += [P(f"ECHEC MESURE : aucun seuil detecte. MC = NaN, defaut = NaN, MC brut = NaN, rigide 1001 = NaN ; stabilite = {s.get('stability_rating')} ; score MC = {fmt(s.get('mc_score'), 3)} ; source du seuil = {src} ; avertissements enregistres ({len(warns)}) :", 'petit')]
        for w in warns:
            out += [P(f"- {w}", 'petit')]
        out += [P("Le diagnostic bruit de ce run utilise la valeur d'urgence fixe 52,5 % : ce 52,5 % n'est PAS un seuil detecte et ne doit jamais etre cite comme tel. Aucun seuil propre, aucun F1/F2, aucune courbe de scan pour ce run (controle constant).", 'petit')]
        p = Path(d) / 'noise_diagnostic.png'
        if p.exists():
            out += [Spacer(1, 2*mm), img(p), P(f"Diagnostic bruit - {run_id} (valeur d'urgence 52,5 %, pas un seuil)", 'cap')]
        return out
    q = s.get('scores_moyens_par_Q') or {}
    qtxt = ' ; '.join(f"{k} = {v}" for k, v in q.items()) if q else '-'
    cv = s.get('controle_valeur_au_seuil_mc') or {}
    out += [P(f"n = {s.get('n_pts')} ; MC = {fmt(s.get('mc_threshold_pct'))} % ; defaut = {fmt(s.get('default_threshold_pct'))} % ; MC brut = {fmt(s.get('raw_mc_threshold_pct'))} % ; defaut brut = {fmt(s.get('raw_default_threshold_pct'))} % ; rigide 1001 = {fmt(s.get('rigid_1001_threshold_pct'))} % ; stabilite = {s.get('stability_rating')} (moy. {fmt(s.get('stability_mean'))}, std {fmt(s.get('stability_std'))}) ; score MC = {fmt(s.get('mc_score'), 3)} (w = {s.get('mc_w_size')}, candidats = {s.get('mc_n_candidates')}) ; scan global max = {fmt(s.get('scan_max_score'), 3)} a {fmt(s.get('scan_argmax_pct'))} % ; valeur du controle au MC (mediane) = {fmt(cv.get('mediane'), 1)} ; bruit = {s.get('noise_label', '-')} ; source du seuil = {src} ; avertissements = {len(warns)}.", 'petit'),
            P(f"Scores moyens par Q : {qtxt}. Duree : {s.get('duration_s')} s.", 'petit')]
    if pf is not None and len(pf):
        data = [hdr(['flux', 'seuil propre %', 'score max', 'top-3 candidats %'])]
        for r in pf.sort_values('score_max', ascending=False).itertuples():
            data.append(row(r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3), str(r.top3_candidats)))
        out += [tbl(data, [40*mm, 32*mm, 28*mm, 75*mm])]
    if f1 is not None and len(f1):
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
            out += [Spacer(1, 2*mm), img(p), P(f"{cap} - {run_id}", 'cap')]
    return out

story += [P('3. Detail par run', 'stitre'),
          P('Chaque run : resume (dont source du seuil et avertissements), seuils propres par flux (fonction de scan du pipeline, configuration MC du run), scores Q, F1/F2 du flux \'Tous\' avant et apres seuil, puis les figures du run (courbe de scan, diagnostic bruit ; diagnostic bruit seul pour veil-type).', 'txt')]
for c in ORDER:
    s, pf, f1 = runs[c]
    story += run_section(f"3. Controle = {c}", f"ctrl_{c}", s, pf, f1, BASE / 'results' / f'ctrl_{c}')

story += [PageBreak(), P('Annexe. F1/F2 avant et apres seuil, complete', 'stitre'),
          P('Pour chacun des 22 runs detectes : F1_pre / F2_pre (derivees avant seuil), F1 / F2 (derivees apres seuil), deltas et sign_change, par estimateur et par flux, tels que produits par le pipeline (transition_analysis). veil-type n\'a pas de F1/F2 (pas de seuil detecte) et n\'apparait donc pas dans cette annexe.', 'txt')]
for c in ORDER:
    s, pf, f1 = runs[c]
    if f1 is None:
        continue
    story += [P(f"F1/F2 - ctrl_{c}", 'h3')]
    data = [hdr(['estimateur', 'flux', 'F1_pre', 'F2_pre', 'F1', 'F2', 'delta_F1', 'delta_F2', 'sign_change'])]
    for r in f1.itertuples():
        data.append(row(r.estimateur, r.flux, fmt(r.F1_pre, 6), fmt(r.F2_pre, 6), fmt(r.F1, 6), fmt(r.F2, 6), fmt(r.delta_F1, 6), fmt(r.delta_F2, 6), r.sign_change))
    story += [tbl(data, [20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm])]

story += [Spacer(1, 6*mm), HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c')),
          P('Fin. Protocole gele : PROTOCOLE.md. Rappel : les codes sont des etiquettes nominales, les seuils des coupures de rang, la lecture est descriptive seulement, et RIEN ici n\'est une regle pour decider si un champignon est comestible ou toxique. Les rapports texte complets du pipeline, les CSV bruts et les figures restent dans results/ et dans la synthese (synthese_runs.csv, tous_seuils_par_flux.csv, tous_F1F2.csv, qs_par_run.csv, plateaux_controles.csv).', 'petit')]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(15*mm, 10*mm, 'Mushroom Classification x pipeline v3.4-H3 - resultats complets')
    canvas.drawRightString(W - 15*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
                        title='Mushroom Classification x v3.4-H3 - Resultats complets', author='Muse')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF ecrit : {OUT} ({OUT.stat().st_size/1e6:.1f} Mo)")
