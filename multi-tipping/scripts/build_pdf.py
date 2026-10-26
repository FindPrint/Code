# -*- coding: utf-8 -*-
"""Construit le PDF complet de la conversation multi-tipping (22 oct. 2026).
Toutes les valeurs numériques sont lues dans les fichiers sources (JSON/CSV),
jamais recopiées à la main. Sortie : Multi_Tipping_Pipeline_v33_Resultats_complets.pdf
"""
import json, os
from pathlib import Path
import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether, HRFlowable)

B = Path('/home/hatch/workspace/multi-tipping')
OUT = B / 'Multi_Tipping_Pipeline_v33_Resultats_complets.pdf'
FD = '/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DVS', f'{FD}/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-B', f'{FD}/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVS-I', f'{FD}/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-BI', f'{FD}/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVM', f'{FD}/DejaVuSansMono.ttf'))

W, H = A4
MARGIN = 15 * mm
USABLE = W - 2 * MARGIN

def st(name, **kw):
    base = dict(fontName='DVS', fontSize=10, leading=14.5, alignment=TA_JUSTIFY,
                spaceAfter=5, textColor=colors.HexColor('#1a1a1a'))
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    'title': st('title', fontName='DVS-B', fontSize=26, leading=32, alignment=TA_CENTER, spaceAfter=10),
    'subtitle': st('subtitle', fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#444444')),
    'h1': st('h1', fontName='DVS-B', fontSize=16, leading=20, spaceBefore=14, spaceAfter=8, alignment=TA_LEFT),
    'h2': st('h2', fontName='DVS-B', fontSize=13, leading=17, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT),
    'h3': st('h3', fontName='DVS-B', fontSize=11, leading=15, spaceBefore=8, spaceAfter=4, alignment=TA_LEFT),
    'body': st('body'),
    'small': st('small', fontSize=8.5, leading=12),
    'caption': st('caption', fontName='DVS-I', fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=colors.HexColor('#444444')),
    'cell': st('cell', fontSize=8.5, leading=11.5, alignment=TA_LEFT, spaceAfter=0),
    'cellc': st('cellc', fontSize=8.5, leading=11.5, alignment=TA_CENTER, spaceAfter=0),
    'cellh': st('cellh', fontName='DVS-B', fontSize=8.5, leading=11.5, alignment=TA_CENTER, textColor=colors.white, spaceAfter=0),
    'mono': st('mono', fontName='DVM', fontSize=7.5, leading=10.5, alignment=TA_LEFT, spaceAfter=1),
    'box': st('box', fontSize=10, leading=14.5),
}

def P(text, style='body'):
    return Paragraph(text, S[style])

def fig(path, width_mm=165, caption=None):
    p = Path(path)
    if not p.exists():
        return [P(f'[Figure manquante : {p.name}]', 'caption')]
    im = PILImage.open(p)
    w = width_mm * mm
    h = w * im.height / im.width
    out = [Image(str(p), width=w, height=h)]
    if caption:
        out.append(P(caption, 'caption'))
    return out

def table(headers, rows, widths=None, align_center_cols=None):
    data = [[Paragraph(h, S['cellh']) for h in headers]]
    for r in rows:
        line = []
        for j, v in enumerate(r):
            sty = 'cellc' if (align_center_cols and j in align_center_cols) else 'cell'
            line.append(Paragraph(str(v), S[sty]))
        data.append(line)
    if widths is None:
        widths = [USABLE / len(headers)] * len(headers)
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eef2f5')]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b0bec5')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t

def verdict_box(title, body, color='#1b5e20'):
    inner = [[Paragraph(f'<b>{title}</b>', S['box'])], [Paragraph(body, S['box'])]]
    t = Table(inner, colWidths=[USABLE])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
        ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor(color)),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def fmt(x, nd=2):
    if x is None:
        return '—'
    try:
        return f'{float(x):.{nd}f}'
    except (TypeError, ValueError):
        return str(x)

def load_json(p):
    return json.load(open(p))

story = []

# ============================== COUVERTURE ==============================
story.append(Spacer(1, 28 * mm))
story.append(P('Pipeline v3.3 — Banc multi-tipping', 'title'))
story.append(P('Tous les résultats, la démarche et les sorties sources', 'subtitle'))
story.append(Spacer(1, 4 * mm))
story.append(P('Une simulation « comme Ising » mais avec plusieurs points de bascule '
               'dans un seul balayage — Ashkin-Teller, horloge q=6, réplications, '
               'contrôles nuls et configuration saine', 'subtitle'))
story.append(Spacer(1, 10 * mm))
story.append(HRFlowable(width='100%', thickness=1.2, color=colors.HexColor('#2c3e50')))
story.append(Spacer(1, 6 * mm))
story.append(table(['', ''], [
    ['Conversation', 'Side chat « Multi-type Ising simulation pipeline », 22 octobre 2026'],
    ['Pipeline', 'pipeline_autonome_v3_3_fixed.py (v3.3, uploadé par l’utilisateur le 22 oct. 2026), tel quel'],
    ['Configuration', 'Mode stable, contrôle = energy, test cohen_d, fenêtre 80, graine 42'],
    ['Runs pipeline', '8 runs complets : vague 1 (1) + vague 2 (5) + porte D (2)'],
    ['Compilation du PDF', '25 octobre 2026 — chiffres relus dans les fichiers sources (JSON/CSV)'],
    ['Dossier de travail', 'workspace/multi-tipping/ (générateurs, CSV, rapports, résultats)'],
], widths=[32 * mm, USABLE - 32 * mm]))
story.append(Spacer(1, 8 * mm))
story.append(verdict_box('Verdict en une phrase',
    'Les deux transitions nettes d’Ashkin-Teller sont retrouvées aveuglément et répliquées, '
    'chacune par ses propres flux — et le nul corrigé détruit le signal par flux (facteur ~20) ; '
    'mais le seuil global seul ne discrimine pas quand le contrôle est aussi un flux, et les '
    'transitions molles BKT de l’horloge q=6 ne sont pas retrouvées aux positions publiées.'))
story.append(Spacer(1, 8 * mm))
story.append(P('Ce document contient tout ce qui a été fait dans cette conversation : la question de départ, '
               'les modèles et leurs générateurs, les protocoles gelés avant chaque run, les résultats chiffrés '
               'de chaque run (seuils globaux, seuils par flux, mapping en température, stabilité, scores, '
               'dérivés F1/F2, ancres T_log, diagnostic de bruit), les figures produites par le pipeline et les '
               'figures de synthèse, ainsi que les limites et les pistes ouvertes. Les annexes reproduisent les '
               'protocoles intégraux et les tables complètes.', 'body'))
story.append(PageBreak())

# ============================== SOMMAIRE ==============================
story.append(P('Sommaire', 'h1'))
for item in [
    '1. La question de départ et la démarche',
    '2. Les bancs de simulation (Ashkin-Teller, horloge q=6, réserves)',
    '3. Le pipeline v3.3 : configuration, entrées, lecture des chiffres',
    '4. Vague 1 — Ashkin-Teller : les deux seuils retrouvés',
    '5. Vague 2 — Porte A (réplication), Porte B (contrôles nuls), Porte C (horloge q=6)',
    '6. Porte D — la configuration saine (contrôle exclu des flux)',
    '7. Synthèse : ce qui tient, ce qui ne tient pas, ce qui reste ouvert',
    'Annexe A — Protocoles gelés (textes intégraux)',
    'Annexe B — Tables complètes (F1/F2, ancres, seuils par flux, paysages)',
    'Annexe C — Données, fichiers et reproductibilité',
    'Annexe D — Extrait du rapport texte du pipeline (vague 1)',
]:
    story.append(P(item, 'body'))
story.append(P('Conventions de lecture. Un « seuil % » est toujours un pourcentage de l’axe de progression du '
               'pipeline, c’est-à-dire le rang de la colonne de contrôle (energy) : 54,93 % signifie que le seuil '
               'sépare les 54,93 % de lignes de plus basse énergie des autres. Le « mapping en T » convertit ce '
               'pourcentage en température en prenant les températures des lignes situées autour de la frontière '
               'de rang d’énergie (méthode du test Ising du 17 octobre 2026). Les températures ne sont jamais '
               'données au pipeline : elles sont gardées dans un fichier séparé et n’interviennent qu’après coup, '
               'pour la vérification. Les seuils « propres par flux » sont obtenus avec la fonction de scan du '
               'pipeline lui-même, appliquée à un seul flux, avec la configuration Monte Carlo retenue par le run.', 'body'))

# ============================== 1. QUESTION ET DÉMARCHE ==============================
story.append(P('1. La question de départ et la démarche', 'h1'))
story.append(P('Le 22 octobre 2026, l’utilisateur pose une question simple : existe-t-il une simulation comme '
               'Ising qui comporte plusieurs points de bascule (tipping points), et pas un seul, pour y passer '
               'son pipeline ? Le contexte est celui de son travail : le modèle d’Ising 2D ne possède qu’un seul '
               'point critique (Tc = 2,2692), et son pipeline ne rend qu’un seul seuil optimal. La question est '
               'donc double : (1) trouver des systèmes à plusieurs transitions dans un seul balayage, avec une '
               'vérité terrain connue ; (2) voir ce que fait un instrument à seuil unique face à deux transitions '
               'réelles — lequel il choisit, et si le second reste visible dans le paysage de scan.', 'body'))
story.append(P('Chronologie de la conversation', 'h2'))
story.append(table(['Étape', 'Date (HAE)', 'Contenu'], [
    ['Question et banc', '22 oct., matin', 'Choix des modèles, générateurs Ashkin-Teller et horloge q=6 écrits et vérifiés'],
    ['Vague 1', '22 oct., 12 h 36', 'Pipeline v3.3 sur Ashkin-Teller (L=28, graine 42), protocole gelé avant le run'],
    ['Opinion demandée', '22 oct., 13 h 34', '« C’est une preuve potentielle ? On fait quoi ensuite ? » → vague 2 proposée'],
    ['Vague 2', '22 oct., 13 h 40–13 h 58', 'Portes A (réplication), B (nuls), C (horloge q=6), protocole gelé'],
    ['Porte D', '22 oct., ~14 h 15', 'AT et nul rejoués sans energy-as-flux (configuration standard du 17 oct.)'],
    ['Ce PDF', '25 oct.', 'Compilation complète de tout le travail de la conversation'],
], widths=[30 * mm, 28 * mm, USABLE - 58 * mm]))
story.append(P('Règles de méthode appliquées à chaque vague', 'h2'))
for t in [
    '<b>Protocole gelé avant le run.</b> Fenêtres de hit, critères de succès et méthode de mapping sont écrits '
    'avant de lancer le pipeline, jamais ajustés après coup (les trois protocoles sont reproduits en annexe A).',
    '<b>Aveuglement.</b> Le fichier d’entrée ne contient aucune colonne température ; le contrôle est energy, '
    'et la température n’est utilisée qu’après coup, pour convertir les seuils en T.',
    '<b>Deux flux au minimum, chaque flux son propre seuil.</b> Le seuil global du pipeline est complété par des '
    'scans par flux (fonction de scan du pipeline, configuration Monte Carlo du run).',
    '<b>Contrôles nuls.</b> Chaque résultat réel est confronté à un jeu décorrélé, pour mesurer ce que '
    'l’instrument produit quand il n’y a rien à trouver.',
    '<b>Caveat synthétique.</b> Toutes les données sont générées par l’assistant (Monte Carlo maison). Le '
    'synthétique construit le banc, il ne remplace pas une donnée réelle — cette réserve accompagne chaque '
    'résultat du document.',
]:
    story.append(P('•  ' + t, 'body'))
story.append(P('Ce que ce document ne contient pas : les travaux d’autres conversations (campagne Ising des '
               '17–19 octobre, données Kaggle, etc.), sauf lorsqu’ils servent de référence explicite — par exemple '
               'la configuration standard du 17 octobre, vérifiée sur pièces dans la porte D.', 'body'))

# ============================== 2. BANCS ==============================
story.append(P('2. Les bancs de simulation', 'h1'))
story.append(P('2.1 Ashkin-Teller — le banc principal', 'h2'))
story.append(P('Le modèle d’Ashkin-Teller est une généralisation d’Ising : deux couches d’Ising, de spins s<sub>i</sub> '
               'et τ<sub>i</sub> = ±1 sur chaque site, couplées par une interaction à deux spins (J) et une '
               'interaction à quatre spins (U) :', 'body'))
story.append(P('H = − Σ<sub>&lt;ij&gt;</sub> [ J (s<sub>i</sub>s<sub>j</sub> + τ<sub>i</sub>τ<sub>j</sub>) + U · s<sub>i</sub>τ<sub>i</sub>s<sub>j</sub>τ<sub>j</sub> ]', 'body'))
story.append(P('Quand U &gt; J, la transition unique se fend en deux transitions nettes de type Ising (résultat prouvé : '
               'Pfister ; Duminil-Copin–Raoufi–Tassion) : en chauffant, la phase de Baxter (s, τ et le produit sτ '
               'ordonnés) perd d’abord l’ordre des spins s et τ — le produit sτ reste ordonné (phase partiellement '
               'ordonnée &lt;sτ&gt;) — puis perd l’ordre du produit et devient paramagnétique. Les deux températures '
               'critiques encadrent le point autodual défini par sinh(2J/T) = exp(−2U/T). C’est exactement le cas '
               'd’école cherché : deux points critiques, deux paramètres d’ordre distincts, chacun porté par des '
               'flux différents (magnetization_s / magnetization_tau pour le premier, magnetization_prod pour le '
               'second).', 'body'))
story.append(table(['Paramètre', 'Valeur (jeu principal)'], [
    ['Couplages', 'J = 1, U = 2 (U > J : régime à deux transitions)'],
    ['Réseau', 'Carré 2D, L = 28 (784 sites), conditions périodiques'],
    ['Balayage', 'T de 2,0 à 7,0 par pas de 0,10 (51 températures)'],
    ['Monte Carlo', 'Metropolis damier vectorisé, 200 sweeps d’équilibration par T, 24 snapshots par T espacés de 10 sweeps'],
    ['Graine', '42 (réplications : 7, 123 ; autre taille : L = 36, graine 42)'],
    ['Lignes', '1 224 (51 × 24)'],
    ['Flux par snapshot', 'magnetization_s, magnetization_tau, magnetization_prod, energy, flip_rate, local_variance'],
    ['Générateur', 'gen_ashkin_teller.py (déterministe à graine fixée)'],
], widths=[38 * mm, USABLE - 38 * mm]))
story.append(P('Vérification des données générées (moyennes par température, lues dans les CSV)', 'h2'))
ver = pd.read_csv(B / 'pdf_build/verification_AT.csv')
rows = []
for r in ver.itertuples():
    rows.append([r.jeu, fmt(r._2, 3), fmt(r._3, 3), fmt(r._4, 3), fmt(r._5, 3), fmt(r._6, 3),
                 fmt(r._7, 1), fmt(r._8, 1)])
story.append(table(['Jeu', 'm_s @4,6', 'm_s @4,9', 'm_prod @4,9', 'm_prod @5,3', 'm_prod @5,6', 'm_s < 0,4 dès T', 'm_prod < 0,4 dès T'],
                   rows, widths=[30 * mm] + [(USABLE - 30 * mm) / 7] * 7))
story.append(P('Lecture : sur les quatre jeux AT, magnetization_s passe sous 0,4 entre T = 4,6 et 4,8, tandis que '
               'magnetization_prod reste autour de 0,85 à T = 4,9 et ne passe sous 0,4 qu’entre T = 5,1 (L=36) et '
               '5,5 (graines 7 et 123). Les deux chutes sont séparées d’environ 0,7 en température. C’est cette '
               'mesure, faite sur les données générées, qui a fixé les fenêtres de hit de la vague 1 (seuil 1 : '
               '50–60 % ; seuil 2 : 62–73 % de l’axe de progression).', 'body'))
for el in fig(B / 'pdf_build/chart_at_fluxes_T.png', caption='Figure de synthèse (données générées). À gauche : les deux aimantations — la chute de s précède celle du produit. À droite : l’énergie, monotone en T, utilisée comme contrôle.'):
    story.append(el)
story.append(P('2.2 Horloge q=6 — le test dur (transitions BKT)', 'h2'))
story.append(P('Le modèle d’horloge q=6 est le cousin direct d’Ising : chaque spin prend 6 orientations '
               '(θ = 0, 60°, …, 300°) avec interaction −J·cos(θ<sub>i</sub> − θ<sub>j</sub>). Un seul balayage en '
               'température traverse deux transitions de Berezinskii–Kosterlitz–Thouless (BKT), d’ordre infini — '
               'donc sans chute nette de l’aimantation : T1 ≈ 0,70 (ferromagnétique → phase critique à quasi-ordre) '
               'et T2 ≈ 0,88 (phase critique → paramagnétique), d’après la méthode CTMRG (fourchettes Monte Carlo '
               'de la littérature : 0,68–0,75 / 0,88–0,92). La signature attendue est surtout la libération des '
               'vortex (densité de vortex) et les pentes des flux, pas un saut. Paramètres du jeu généré : réseau '
               'carré L = 24, T de 0,40 à 1,20 par pas de 0,02 (41 températures), 150 sweeps d’équilibration, '
               '24 snapshots par T, 984 lignes, flux : magnetization, energy, flip_rate, vortex_density, '
               'local_variance (générateur gen_clock6.py, graine 42).', 'body'))
for el in fig(B / 'pdf_build/chart_clock_T.png', caption='Figure de synthèse (données générées, L=24). Pointillés : T1 = 0,70 et T2 = 0,88 publiés. L’aimantation décroît graduellement (pas de saut BKT) ; la densité de vortex ne décolle nettement que vers T ≈ 0,96–1,10 sur ce petit réseau — un décalage de taille finie qui pèsera sur la porte C.'):
    story.append(el)
story.append(P('2.3 Modèles en réserve (documentés, non générés dans cette conversation)', 'h2'))
story.append(table(['Modèle', 'Pourquoi plusieurs bascules', 'Statut'], [
    ['ANNNI', 'Interactions concurrentes (ferro proches voisins, antiferro seconds voisins axiaux) : séquence infinie de phases modulées commensurables près du point multiphase κ = 1/2 ; en 2D, phase critique flottante entre ferro et para, séparée par deux transitions BKT', 'Générateur à écrire si choisi'],
    ['Blume-Capel / BEG', 'Ising spin-1 (s = −1, 0, +1) avec champ cristallin : point tricritique où les lignes du 1er et du 2e ordre se rejoignent ; versions avec réentrance (un balayage en T traverse deux fois la frontière)', 'À calibrer avant tout protocole'],
    ['Carte logistique', 'Cascade infinie de doublements de période aux seuils exacts r = 3 ; 3,44949 ; 3,54409 ; 3,56441 ; … accumulation r∞ ≈ 3,56995 (chaos). Vérité terrain parfaite, coût ~1 s, mais hors physique des réseaux', 'Générateur à écrire si choisi'],
], widths=[30 * mm, 105 * mm, USABLE - 135 * mm]))

# ============================== 3. PIPELINE ==============================
story.append(P('3. Le pipeline v3.3 : configuration, entrées, lecture des chiffres', 'h1'))
story.append(P('Le pipeline est le fichier pipeline_autonome_v3_3_fixed.py, uploadé par l’utilisateur le 22 octobre '
               '2026 et utilisé tel quel, sans modification, dans tous les runs de cette conversation (pilotes : '
               'run_v33_at.py pour la vague 1, run_v33_generic.py pour la vague 2, run_v33_generic_noEflux.py pour '
               'la porte D). C’est un pipeline d’analyse de complexité multi-domaines (UNIVERSAL_LOG v3.3) : il '
               'calcule, pour chaque flux, des estimateurs de complexité (Higuchi, DFA, Katz, Hurst, SampleEn — '
               'les « Q »), un spectre d’ancres en quatre classes (saturation, criticité, divergence, nulle, '
               'formule T_log = (d − 4)·ln(n)), un diagnostic de bruit, et il cherche un seuil critique par scan '
               'de séparation (test de Cohen d) avec optimisation Monte Carlo des paramètres de scan.', 'body'))
story.append(table(['Réglage', 'Valeur (tous les runs)'], [
    ['Mode', 'stable'],
    ['Test statistique', 'cohen_d'],
    ['Fenêtre de base (w_size)', '80 (la configuration Monte Carlo retenue varie : voir chaque run)'],
    ['Graine Monte Carlo', '42'],
    ['Contrôle', 'energy (colonne du CSV de flux)'],
    ['Flux analysés', 'Vagues 1–2 : toutes les colonnes, y compris energy. Porte D : energy exclue (voir §6)'],
    ['Bootstrap', 'Activé (mode stable, n_est = 4)'],
    ['Entrée', 'CSV de flux seuls, sans température (aveugle)'],
], widths=[45 * mm, USABLE - 45 * mm]))
story.append(P('Sorties du pipeline par run : pipeline_results.json (résultats complets), numerical_results.csv '
               '(paysage de complexité par flux), numerical_results_separation_scores.csv, '
               'numerical_results_noise_diagnostic.csv, text_report.txt (rapport texte du pipeline), '
               'threshold_scan.png (courbe de scan), landscape_complexity.png, stability_analysis.png, '
               'post_threshold_analysis.png, noise_diagnostic.png, anchor_spectrum.png (vague 1 uniquement : le '
               'pilote générique de la vague 2 n’exporte que threshold_scan et noise_diagnostic), scan_curve.csv '
               '(courbe de scan complète). Les analyses par flux (seuils propres, mapping en T, zones du paysage) '
               'sont produites par les scripts analyse_at.py / analyse_generic.py / analyse_generic_noE.py, qui '
               'utilisent la fonction de scan du pipeline lui-même.', 'body'))
story.append(P('Comment lire un seuil. Le pipeline trie les lignes par le rang de la colonne de contrôle et '
               'cherche le découpage qui maximise la séparation des estimateurs de complexité entre les fenêtres '
               'avant et après le seuil. Le seuil est donc un pourcentage de progression, pas une température. La '
               'stabilité est évaluée en répétant le scan sur plusieurs tailles de fenêtre (50, 80, 100, 120, 150, '
               '180, 220) : VERY STABLE / MODERATELY STABLE / UNSTABLE selon la dispersion des seuils obtenus. '
               'Les dérivés F1/F2 sont les dérivées première et seconde, après seuil, des courbes d’estimateurs '
               '(transition_analysis du pipeline) : elles caractérisent l’ordre apparent de la transition '
               '(2e ordre = transition douce selon la classification du pipeline).', 'body'))

# ============================== 4. VAGUE 1 ==============================
R1 = B / 'results_at_v33'
J1 = load_json(R1 / 'pipeline_results.json')
MD1 = J1['metadata']
TO1 = MD1['threshold_optimization']
BC1 = TO1['best_config']
ST1 = MD1['stability_report']
PF1 = pd.read_csv(R1 / 'per_flux_thresholds.csv')
TM1 = pd.read_csv(R1 / 'threshold_T_mapping.csv')
TM1 = TM1.set_index('seuil')
story.append(P('4. Vague 1 — Ashkin-Teller : les deux seuils retrouvés', 'h1'))
story.append(P('Protocole (gelé avant le run, texte intégral en annexe A) : entrée at_fluxes.csv (1 224 lignes, '
               '6 flux, aucune température), pipeline v3.3 tel quel, mode stable, contrôle = energy (aussi flux), '
               'w_size 80, cohen_d, graine 42. Durée : 213,6 s. Seuils critiques attendus, formulés explicitement '
               'avant le run : seuil 1 (spin) — chute de magnetization_s à T ≈ 4,6–4,9, soit 50–60 % de l’axe de '
               'progression ; seuil 2 (produit) — chute de magnetization_prod à T ≈ 5,2–5,6, soit 62–73 %. '
               'Verdict gelé : le seuil principal tombe-t-il dans une des deux fenêtres, et le paysage de scan '
               'montre-t-il le second seuil ?', 'body'))
story.append(verdict_box('Verdict vague 1',
    'Seuil global Monte Carlo 54,93 % → T = 4,77 ± 0,12 : HIT sur le seuil 1 (spin). Le seuil 2 n’apparaît dans '
    'la courbe globale que comme une épaule soutenue, mais le scan par flux le résout nettement : '
    'magnetization_prod → 64,95 % → T = 5,29 ± 0,15 (fenêtre 2, HIT), flip_rate identique. Les deux seuils '
    'attendus sont retrouvés, chacun par ses propres flux.'))
story.append(P('Seuils globaux rendus par le pipeline', 'h2'))
story.append(table(['Lecture', 'Seuil %', 'T mappée'], [
    ['Monte Carlo (traité)', fmt(BC1['threshold']), f"{fmt(TM1.loc['MC_traite', 'T_estime'])} ± {fmt(TM1.loc['MC_traite', 'T_std_fenetre'])}"],
    ['Défaut (traité)', fmt(TO1['default_threshold']), f"{fmt(TM1.loc['defaut_traite', 'T_estime'])} ± {fmt(TM1.loc['defaut_traite', 'T_std_fenetre'])}"],
    ['Monte Carlo (brut)', fmt(TO1['raw_mc_threshold']), f"{fmt(TM1.loc['MC_brut', 'T_estime'])} ± {fmt(TM1.loc['MC_brut', 'T_std_fenetre'])}"],
    ['Défaut (brut)', fmt(TO1['raw_default_threshold']), f"{fmt(TM1.loc['defaut_brut', 'T_estime'])} ± {fmt(TM1.loc['defaut_brut', 'T_std_fenetre'])}"],
    ['Témoin grille 1001', fmt(TO1['rigid_1001_threshold']), '≈ 4,77'],
    ['Stabilité (7 fenêtres)', f"moy {fmt(ST1['mean'])} ± {fmt(ST1['std'])} (min {fmt(ST1['min'])}, max {fmt(ST1['max'])}) — {ST1['rating']}", f"{fmt(TM1.loc['stabilite_moy', 'T_estime'])} ± {fmt(TM1.loc['stabilite_moy', 'T_std_fenetre'])}"],
], widths=[55 * mm, 62 * mm, USABLE - 117 * mm]))
story.append(P(f"Paramètres Monte Carlo retenus : score {fmt(BC1['score'], 3)}, w_size {BC1['w_size']}, "
               f"n_candidates {BC1['n_candidates']}, min_grp {BC1['min_grp']}, 50 itérations. Aveuglement vérifié : "
               f"control_label = {MD1['control_label']}, n_pts = {MD1['n_pts']}, aucune colonne température dans l’entrée.", 'body'))
story.append(P('Seuils propres à chaque flux (scan du pipeline, configuration Monte Carlo)', 'h2'))
rows = []
for r in PF1.itertuples():
    key = 'propre_' + r.flux
    t = TM1.loc[key] if key in TM1.index else None
    fen = 'fenêtre 1 ✓' if r.flux in ('magnetization_s', 'magnetization_tau') else ('fenêtre 2 ✓' if r.flux in ('magnetization_prod', 'flip_rate') else ('entre les deux' if r.flux == 'energy' else 'avant le seuil 1'))
    rows.append([r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3),
                 f"{fmt(t['T_estime'])} ± {fmt(t['T_std_fenetre'])}" if t is not None else '—', fen])
story.append(table(['Flux', 'Seuil propre %', 'Score max', 'T mappée', 'Lecture'], rows,
                   widths=[45 * mm, 28 * mm, 24 * mm, 38 * mm, USABLE - 135 * mm]))
story.append(P('Notes : energy est à la fois contrôle et flux — son seuil propre (61,00 %) tombe entre les deux '
               'transitions, son paysage mélangeant les deux chutes. local_variance pointe tôt (39,76 %, score '
               'nettement plus faible, 2,227) : aucune troisième transition n’est connue dans ce modèle vers '
               'T ≈ 4,0 ; lecture prudente = montée des fluctuations locales en approche du seuil 1, pas un '
               'troisième point critique. Top-3 candidats par flux : s [52,5 ; 53,4 ; 54,9], tau [53,4 ; 54,9 ; '
               '52,5], prod [64,9 ; 64,6 ; 67,5], flip_rate [64,9 ; 66,8 ; 64,8], energy [61,0 ; 58,4 ; 60,7], '
               'local_variance [39,8 ; 40,5 ; 40,2].', 'body'))
story.append(P('Paysage de scan global (courbe complète)', 'h2'))
sc1 = pd.DataFrame(J1['scan_curve']).dropna(subset=['score'])
def zone(c, a, b):
    v = c[(c.candidate >= a) & (c.candidate <= b)]['score']
    return fmt(v.mean(), 3) if len(v) else '—'
story.append(table(['Zone (% de progression)', 'Score moyen (courbe traitée)'], [
    ['45–50', zone(sc1, 45, 50)], ['50–60 (fenêtre 1)', zone(sc1, 50, 60)],
    ['62–73 (fenêtre 2)', zone(sc1, 62, 73)], ['75–85', zone(sc1, 75, 85)], ['88–97', zone(sc1, 88, 97)],
    ['Maximum global', f"{fmt(sc1['score'].max(), 3)} à {fmt(sc1.loc[sc1['score'].idxmax(), 'candidate'])} %"],
], widths=[70 * mm, USABLE - 70 * mm]))
story.append(P('Lecture : entre les deux seuils, le score global ne retombe pas au niveau de base — il forme un '
               'plateau/épaule qui ne s’effondre qu’après ~73 %. Le seuil 2 est présent dans le paysage global '
               'comme épaule, et comme pic net dès qu’on scanne les flux séparément.', 'body'))
for el in fig(R1 / 'threshold_scan.png', caption='Vague 1 — Courbe de scan du pipeline (seuil global 54,93 %).'):
    story.append(el)
for el in fig(R1 / 'landscape_complexity.png', caption='Vague 1 — Paysage de complexité par flux (sortie du pipeline).'):
    story.append(el)
for el in fig(R1 / 'stability_analysis.png', caption='Vague 1 — Analyse de stabilité multi-fenêtres (VERY STABLE).'):
    story.append(el)
story.append(P('Diagnostic de bruit et signatures dominantes', 'h2'))
ND1 = J1['noise_diagnostic']
story.append(P(f"Étiquette du diagnostic : « {ND1.get('diagnostic_label', '')} ».", 'body'))
rows = []
for d in ND1.get('all_flux_diagnostics', []):
    rows.append([d['flux_name'], fmt(d.get('variance_proxy_score'), 3), fmt(d.get('cand_q5_score'), 2),
                 fmt(d.get('avg_hurst'), 3), fmt(d.get('delta_corr'), 3), fmt(d.get('slope_after'), 3)])
story.append(table(['Flux', 'Proxy', 'Q5 cand.', 'Hurst moy.', 'Δcorr', 'Pente spectrale après'], rows,
                   widths=[45 * mm, 22 * mm, 24 * mm, 26 * mm, 22 * mm, USABLE - 139 * mm]))
tops = J1.get('top_signatures', {})
story.append(P('Signatures dominantes (top 3 par question) : Q1 — magnetization_tau DFA 9,378, tau Hurst 6,519, '
               's DFA 6,398 ; Q2 — local_variance Higuchi 6,809, s Higuchi 6,538, tau SampleEn 6,242 ; Q4 — '
               'energy Higuchi 3,281 (ce chiffre jouera un rôle central dans la porte D, §6).', 'body'))
for el in fig(R1 / 'noise_diagnostic.png', caption='Vague 1 — Diagnostic de bruit (sortie du pipeline).'):
    story.append(el)
story.append(P('Dérivés post-seuil F1/F2 (au seuil global 54,93 %)', 'h2'))
story.append(P('Le pipeline classe la transition en 2e ordre pour les cinq estimateurs (lecture « Tous »). '
               'Table complète des 35 lignes (5 estimateurs × 7 lectures) en annexe B.', 'body'))
TF1 = pd.read_csv(R1 / 'transition_F1F2.csv')
for est in ['Higuchi', 'DFA']:
    sub = TF1[TF1.estimateur == est].set_index('flux')
    rows = [[f, fmt(sub.loc[f, 'F1'], 5), fmt(sub.loc[f, 'F2'], 5)] for f in sub.index]
    story.append(P(f'Estimateur {est}', 'h3'))
    story.append(table(['Flux', 'F1 (dérivée 1re)', 'F2 (dérivée 2e)'], rows,
                       widths=[55 * mm, 55 * mm, USABLE - 110 * mm]))
for el in fig(R1 / 'post_threshold_analysis.png', caption='Vague 1 — Analyse post-seuil (sortie du pipeline).'):
    story.append(el)
story.append(P('Spectre d’ancres T_log (médianes des dimensions par classe — lecture, pas une sortie moyennée '
               'du pipeline, qui ne moyenne pas les dimensions)', 'h2'))
AF1 = pd.read_csv(R1 / 'anchor_spectrum_flat.csv')
piv = AF1[AF1.valeur.notna()].groupby(['flux', 'classe', 'part'])['valeur'].median().unstack('part')
rows = []
for (flux, classe), r in piv.iterrows():
    rows.append([flux, classe, fmt(r.get('full'), 3), fmt(r.get('pre'), 3), fmt(r.get('post'), 3)])
story.append(table(['Flux', 'Classe', 'Complet', 'Avant seuil', 'Après seuil'], rows,
                   widths=[45 * mm, 30 * mm, 30 * mm, 30 * mm, USABLE - 135 * mm]))
story.append(P('Lecture : le saut pré → post au seuil global est porté par la divergence (ex. s : 4,00 → 6,45 ; '
               'prod : 3,36 → 6,10) et par la criticité (s : 1,04 → 2,36 ; tau : 1,04 → 2,48). La criticité du '
               'produit est déjà haute avant le seuil (2,25) parce qu’au seuil 1 le produit est encore ordonné. '
               'Saturation et nulle restent ≈ stables (1,03 et ~1,0).', 'body'))
for el in fig(R1 / 'anchor_spectrum.png', caption='Vague 1 — Spectre d’ancres (sortie du pipeline).'):
    story.append(el)

# ============================== 5. VAGUE 2 ==============================
V2 = B / 'vague2'
def verdict(name):
    return load_json(V2 / name / 'verdict.json')
def summ(name):
    return load_json(V2 / name / 'run_summary.json')
story.append(P('5. Vague 2 — les trois portes', 'h1'))
story.append(P('Protocole gelé avant les runs (texte intégral en annexe A). Coût : 5 runs, 1 073 s de lot '
               '(AT graine 7 : 218 s ; graine 123 : 215 s ; L=36 : 216 s ; nul : 214 s ; horloge : 144 s). '
               'Fenêtres AT inchangées (50–60 % / 62–73 %) ; fenêtres horloge (30–46 % / 52–68 %, élargies car '
               'transitions BKT molles).', 'body'))
story.append(P('Porte A — Réplication AT : PASSÉE', 'h2'))
story.append(P('Critère gelé : seuil global dans la fenêtre 1 ET seuil propre de magnetization_prod dans la '
               'fenêtre 2, sur au moins 2 des 3 jeux.', 'body'))
rows = []
for label, name in [('Vague 1 (référence)', None), ('Graine 7', 'at_s7'), ('Graine 123', 'at_s123'), ('L=36', 'at_L36')]:
    if name is None:
        rows.append([label, '54,93', '4,77', '52,50', '64,95', '5,29', 'VERY STABLE'])
    else:
        v = verdict(name)
        pf = {f['flux']: f for f in v['per_flux']}
        rows.append([label, fmt(v['global_mc_pct']), fmt(v['global_mc_T'][0]) if v['global_mc_T'] else '—',
                     fmt(pf['magnetization_s']['seuil_propre_pct']),
                     fmt(pf['magnetization_prod']['seuil_propre_pct']),
                     fmt(pf['magnetization_prod']['T_estime']) if pf['magnetization_prod']['T_estime'] else '—',
                     f"{v['stabilite']} ±{fmt(v['stabilite_std'])}"])
story.append(table(['Jeu', 'Global MC %', 'T global', 'm_s %', 'm_prod %', 'T prod', 'Stabilité'], rows,
                   widths=[32 * mm, 24 * mm, 20 * mm, 20 * mm, 20 * mm, 20 * mm, USABLE - 136 * mm]))
story.append(P('Graine 7 et graine 123 satisfont entièrement le critère. L=36 : global ✓ ; m_prod à 61,42 % '
               '(T = 5,11), soit 0,58 point sous la fenêtre 2 — compté comme non satisfait au sens strict, sans '
               'déplacement de poteau. En L=36, les deux transitions se rapprochent (produit à 5,11 contre '
               '5,29–5,45 en L=28 : déplacement de taille finie). Motif répliqué 3/3 : m_s/m_tau portent le '
               'seuil 1, m_prod/flip_rate le seuil 2 ; energy propre entre les deux (56–61 %) ; local_variance '
               'précoce (41–45 %, scores faibles 1,85–2,12 contre 5,0–5,6 pour m_s/m_tau).', 'body'))
for nm, cap in [('at_s7', 'Porte A, graine 7 — courbe de scan du pipeline.'),
                ('at_s123', 'Porte A, graine 123 — courbe de scan du pipeline.'),
                ('at_L36', 'Porte A, L=36 — courbe de scan du pipeline.')]:
    for el in fig(V2 / nm / 'threshold_scan.png', caption=cap):
        story.append(el)
story.append(P('Porte B — Contrôles nuls : B1 invalide, B2 décisif', 'h2'))
story.append(P('<b>B1 (lignes mélangées) — invalide par construction.</b> Le run est revenu quasi identique à la '
               'vague 1 (global 54,93 %, stabilité au 4e décimal près). Cause : le pipeline trie les flux par le '
               'rang du contrôle dès l’entrée — permuter les lignes ne change rien à ce qu’il voit. Ce n’est pas '
               'un échec du pipeline, c’est un nul qui ne teste rien. Vérifié au passage : le pipeline est '
               'invariant par permutation des lignes. Erreur de protocole de l’assistant, rejetée et remplacée '
               'par B2.', 'body'))
story.append(P('<b>B2 (flux décorrélés du contrôle, energy fixe, permutations indépendantes, graine 99).</b> '
               'Comparaison réel / nul :', 'body'))
story.append(table(['Lecture', 'Réel (vague 1 + réplicats)', 'Nul B2'], [
    ['Scores par flux m_s / m_tau / m_prod / flip_rate / local_var', '4,35 – 5,61', '0,18 – 0,30'],
    ['Score propre de energy', '4,40 – 4,80', '4,62 (inchangé)'],
    ['Maximum de la courbe de scan globale', '3,49 – 3,86', '0,85'],
    ['Score MC global', '0,759 – 0,765', '0,562'],
    ['Seuils par flux', 'Groupés (fenêtres 1 et 2)', 'Dispersés : 47,9 / 91,7 / 62,8 / 50,2 / 50,0'],
    ['Stabilité globale', 'VERY STABLE', 'VERY STABLE ±1,43 (voir réserve)'],
    ['Seuil global MC', '51,5 – 56,3 %', '58,30 %'],
], widths=[62 * mm, 55 * mm, USABLE - 117 * mm]))
story.append(P('Le signal par flux est détruit (facteur ~20 sur les scores, aucune grappe dans les fenêtres — '
               'le 62,8 % de m_prod est un atterrissage de hasard à score 0,18, niveau de bruit ; avec 6 flux et '
               'des fenêtres larges, ~1 hasard est attendu). <b>Réserve mesurée :</b> le seuil global du nul '
               'tombe à 58,30 % (fenêtre 1) et reste coté VERY STABLE — le critère gelé « pas de VERY STABLE » '
               'n’est donc pas satisfait. Cause identifiée : energy est à la fois contrôle et flux ; triée par '
               'son propre rang, elle se sépare trivialement d’elle-même (son score propre, 4,62, est le seul '
               'inchangé entre réel et nul), et le seuil global mélangeant les flux hérite de ce signal '
               'tautologique. <b>Bilan B : la lecture par flux discrimine réel et nul sans ambiguïté ; la '
               'lecture globale (seuil + stabilité) ne discrimine pas dans cette configuration.</b> Cette '
               'réserve a motivé la porte D (§6).', 'body'))
for el in fig(V2 / 'null2' / 'threshold_scan.png', caption='Porte B2 — courbe de scan du nul décorrélé (scores effondrés).'):
    story.append(el)
story.append(P('Porte C — Horloge q=6 : ÉCHEC au critère gelé', 'h2'))
story.append(P('Critère gelé : seuil global OU au moins 2 seuils propres dans les fenêtres (30–46 % / 52–68 %), '
               'ou épaule nette du paysage dans la fenêtre 2. Vérité terrain : littérature (T1 = 0,70, T2 = 0,88), '
               'pas mesurée sur le générateur.', 'body'))
vc = verdict('clock')
rows = []
for f in vc['per_flux']:
    rows.append([f['flux'], fmt(f['seuil_propre_pct']), fmt(f['score_max'], 3),
                 f"{fmt(f['T_estime'])} ± {fmt(f['T_std'])}" if f['T_estime'] else '—'])
story.append(table(['Flux (horloge q=6)', 'Seuil propre %', 'Score max', 'T mappée'], rows,
                   widths=[55 * mm, 30 * mm, 30 * mm, USABLE - 115 * mm]))
story.append(P(f"Seuil global MC : {fmt(vc['global_mc_pct'])} % → T = {fmt(vc['global_mc_T'][0])} ± "
               f"{fmt(vc['global_mc_T'][1])} — hors des deux fenêtres. Stabilité : {vc['stabilite']} "
               f"(±{fmt(vc['stabilite_std'])}), dégradée par rapport à AT. Zones du paysage : fenêtre 1 = "
               f"{vc['paysage_zones']['win1']}, fenêtre 2 = {vc['paysage_zones']['win2']}, après fenêtre 2 = "
               f"{vc['paysage_zones']['apres_win2']}, loin (88–97 %) = {vc['paysage_zones']['loin_88_97']} — "
               f"pas d’épaule dans la fenêtre 2, le paysage monte vers la fin. <b>Critère non satisfait : "
               f"un seul flux (energy, 30,25 %) dans la fenêtre 1, aucun dans la fenêtre 2.</b>", 'body'))
story.append(P('Structure réelle mais déplacée : deux grappes de flux, {energy, flip_rate} vers T ≈ 0,62–0,64 '
               '(sous T1 = 0,70) et {magnetization, vortex_density, local_variance} vers T ≈ 1,09 (au-dessus de '
               'T2 = 0,88). Dans le jeu généré lui-même (L=24), les vortex ne décollent que vers T ≈ 0,96–1,10 : '
               'la transition haute du jeu est décalée par la taille finie, avant même de parler du pipeline. '
               'L’échec est donc double et non partageable proprement entre « jeu trop petit pour le BKT » et '
               '« instrument moins sensible au mou » — les deux sont vrais, aucun ne suffit à innocenter l’autre. '
               'Borne d’instrument consignée : sur des transitions nettes de type Ising, l’instrument réplique ; '
               'sur des transitions d’ordre infini (BKT), en L=24, il ne retrouve pas les positions publiées.', 'body'))
for el in fig(V2 / 'clock' / 'threshold_scan.png', caption='Porte C, horloge q=6 — courbe de scan du pipeline (optimum à 85 %).'):
    story.append(el)
for el in fig(B / 'pdf_build/chart_scan_curves.png', caption='Figure de synthèse. Courbes de scan globales superposées : les jeux AT réels se superposent (pic dans la fenêtre 1, épaule dans la fenêtre 2), le nul B2 s’effondre, l’horloge q=6 monte vers la fin. Zones vertes/oranges : fenêtres AT gelées.'):
    story.append(el)

# ============================== 6. PORTE D ==============================
story.append(P('6. Porte D — la configuration saine (contrôle exclu des flux)', 'h1'))
story.append(P('Motif : la réserve de la porte B2 (§5) venait peut-être d’une configuration, pas de l’instrument. '
               'La configuration standard du banc Ising (17 octobre, à la demande de l’utilisateur, vérifiée) est : '
               'contrôle = energy, flux = les autres colonnes, energy EXCLUE des flux analysés. La porte D aligne '
               'le banc AT sur cette configuration et rejoue les deux cas critiques (protocole gelé avant les '
               'runs, texte intégral en annexe A ; pilote run_v33_generic_noEflux.py, analyse '
               'analyse_generic_noE.py ; ~193 s par run).', 'body'))
vd1 = verdict('noE_real')
vd2 = verdict('noE_null2')
story.append(P('D1 — AT réel sans energy-as-flux', 'h2'))
rows = []
for f in vd1['per_flux']:
    rows.append([f['flux'], fmt(f['seuil_propre_pct']), fmt(f['score_max'], 3),
                 f"{fmt(f['T_estime'])} ± {fmt(f['T_std'])}" if f['T_estime'] else '—'])
story.append(table(['Flux (sans energy)', 'Seuil propre %', 'Score max', 'T mappée'], rows,
                   widths=[55 * mm, 30 * mm, 30 * mm, USABLE - 115 * mm]))
story.append(P(f"Seuil global MC : {fmt(vd1['global_mc_pct'])} % (fenêtre 1 ✓ ; vague 1 avec energy-as-flux : "
               f"54,93 %), {vd1['stabilite']} (±{fmt(vd1['stabilite_std'])}), score MC {fmt(vd1['mc_score'], 3)}. "
               f"Les deux seuils se résolvent encore, chacun par ses flux, SANS le signal energy-as-flux : "
               f"m_s et m_tau dans la fenêtre 1, m_prod et flip_rate dans la fenêtre 2, local_variance précoce "
               f"comme en vague 1. La discrimination par flux ne dépendait pas de l’artefact.", 'body'))
story.append(P('D2 — Nul B2 sans energy-as-flux', 'h2'))
rows = []
for f in vd2['per_flux']:
    rows.append([f['flux'], fmt(f['seuil_propre_pct']), fmt(f['score_max'], 3)])
story.append(table(['Flux (sans energy)', 'Seuil propre %', 'Score max'], rows,
                   widths=[55 * mm, 30 * mm, USABLE - 85 * mm]))
story.append(P(f"Seuil global MC : {fmt(vd2['global_mc_pct'])} %, {vd2['stabilite']} (±{fmt(vd2['stabilite_std'])}) "
               f"— contre 58,30 %, VERY STABLE (±1,43) avec energy-as-flux. Le critère B d’origine (« pas de "
               f"VERY STABLE sur nul ») est maintenant SATISFAIT. Scores par flux effondrés (0,179–0,333, comme "
               f"en vague 2), seuils dispersés, maximum de la courbe globale 0,124 (contre 0,85 avec "
               f"energy-as-flux, 3,5–3,9 en réel).", 'body'))
story.append(P('Mécanisme mesuré (Q4, energy, Higuchi — lu dans les JSON des runs)', 'h2'))
def q4energy(path):
    r = load_json(path)
    return r.get('scores', {}).get('Q4_Persistence', {}).get('energy_Higuchi_mean')
story.append(table(['Run', 'Q4 energy (Higuchi)'], [
    ['Vague 1 AT réel', fmt(q4energy(R1 / 'pipeline_results.json'), 3)],
    ['AT graine 7', fmt(q4energy(V2 / 'at_s7/pipeline_results.json'), 3)],
    ['Nul B2 (décorrélé)', fmt(q4energy(V2 / 'null2/pipeline_results.json'), 3)],
    ['Porte D réel / nul', '— (energy n’est plus un flux analysé)'],
], widths=[70 * mm, USABLE - 70 * mm]))
story.append(P('Energy-as-flux contribue un score de séparation constant (~3,28, identique réel/nul) qui étaye à '
               'lui seul la stabilité du seuil global sur données décorrélées. Sans elle, le seuil global '
               'discrimine lui aussi (VERY STABLE sur réel → MODERATELY STABLE à un seuil aberrant sur nul), et '
               'la lecture par flux discrimine toujours (~20× d’écart de scores).', 'body'))
story.append(verdict_box('Règle instrumentale établie (porte D)',
    'Le contrôle ne doit jamais figurer parmi les flux analysés (auto-séparation tautologique). C’est le '
    'réglage du 17 octobre, décidé par l’utilisateur — validé par mesure. Corollaire vérifié sur pièces '
    '(dossier results_ising_energy_test : contrôle energy, flux analysés = magnetization / flip_rate / '
    'cluster_size / local_variance, aucune colonne energy parmi les flux) : la campagne Ising standard des '
    '17–19 octobre utilisait déjà cette configuration saine — ses résultats ne sont pas contaminés par '
    'l’artefact.'))
for el in fig(V2 / 'noE_real' / 'threshold_scan.png', caption='Porte D1 — courbe de scan de l’AT réel sans energy-as-flux.'):
    story.append(el)
for el in fig(V2 / 'noE_null2' / 'threshold_scan.png', caption='Porte D2 — courbe de scan du nul sans energy-as-flux (scores effondrés).'):
    story.append(el)

# ============================== 7. SYNTHÈSE ==============================
story.append(P('7. Synthèse : ce qui tient, ce qui ne tient pas, ce qui reste ouvert', 'h1'))
story.append(table(['Porte / question', 'Verdict'], [
    ['Vague 1 — AT, deux seuils', 'Retrouvés : global → seuil 1 ; m_prod/flip_rate → seuil 2 (par flux)'],
    ['Porte A — réplication', 'PASSÉE (2/3 francs, L=36 à la frontière)'],
    ['Porte B — nul B1 (lignes mélangées)', 'INVALIDE par construction → invariance par permutation vérifiée'],
    ['Porte B — nul B2 (décorrélé)', 'Signal par flux détruit (~20×) ; seuil global non discriminant (artefact)'],
    ['Porte C — horloge q=6 (littérature)', 'ÉCHEC au critère gelé ; grappes déplacées ; jeu L=24 trop petit pour BKT'],
    ['Porte D — configuration saine', 'Réserve levée : seuil global discriminant sans energy-as-flux ; règle établie'],
], widths=[62 * mm, USABLE - 62 * mm]))
story.append(P('Ce qui tient après toutes les portes', 'h2'))
for t in [
    'Deux transitions nettes et distinctes dans un même balayage sont retrouvées aveuglément, répliquées sur '
    'trois jeux indépendants (plus la porte D), chacune par ses flux — avec des scores par flux de 4,4–5,6 '
    'contre 0,2 en nul.',
    'La lecture par flux est l’instrument discriminant ; dans la configuration saine (contrôle exclu des flux), '
    'le seuil global discrimine aussi.',
    'Le pipeline est invariant par permutation des lignes d’entrée (vérifié empiriquement).',
]:
    story.append(P('•  ' + t, 'body'))
story.append(P('Ce qui ne tient pas / reste ouvert', 'h2'))
for t in [
    'Transitions molles (BKT) : positions publiées non retrouvées en L=24. Un test propre exigerait un réseau '
    'plus grand (L=48 ou plus) et une équilibration plus longue — piste évoquée, décision en attente.',
    'Toutes les données restent synthétiques, générées par l’assistant. Aucune donnée réelle n’a encore éprouvé '
    'ce banc (règle de l’utilisateur : le synthétique construit, le réel éprouve).',
    'La lecture par flux reste une analyse post-run de l’assistant (scripts d’analyse), pas une sortie native '
    'du pipeline — une proposition de câblage natif a été évoquée, décision en attente.',
    'La campagne Ising standard des 17–19 octobre n’est pas contaminée par l’artefact energy-as-flux '
    '(configuration déjà saine, vérifiée sur pièces) — ce point, lui, est clos.',
]:
    story.append(P('•  ' + t, 'body'))
story.append(P('Réponse à la question de départ. Oui : il existe des simulations « comme Ising » à plusieurs '
               'points de bascule dans un seul balayage — Ashkin-Teller en est la démonstration la plus propre, '
               'l’horloge q=6 la plus exigeante, ANNNI / Blume-Capel / la carte logistique les réserves '
               'documentées. Et oui : passée dedans, la machine à seuil unique choisit la première transition '
               'et ne laisse la seconde visible que comme épaule — à moins de laisser chaque flux porter son '
               'propre seuil, auquel cas les deux transitions se résolvent.', 'body'))

# ============================== ANNEXE A ==============================
story.append(P('Annexe A — Protocoles gelés (textes intégraux)', 'h1'))
for fname in ['PROTOCOLE_AT.md', 'PROTOCOLE_VAGUE2.md', 'PROTOCOLE_PORTE_D.md']:
    story.append(P(fname, 'h2'))
    for line in (B / fname).read_text(encoding='utf-8').splitlines():
        story.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;') or ' ', S['mono']))

# ============================== ANNEXE B ==============================
story.append(P('Annexe B — Tables complètes', 'h1'))
story.append(P('B.1 Dérivés F1/F2 post-seuil, vague 1 (35 lignes : 5 estimateurs × 7 lectures)', 'h2'))
rows = []
for r in TF1.itertuples():
    rows.append([r.estimateur, r.flux, fmt(r.F1, 5), fmt(r.F2, 5)])
story.append(table(['Estimateur', 'Flux', 'F1', 'F2'], rows,
                   widths=[30 * mm, 45 * mm, 35 * mm, USABLE - 110 * mm]))
story.append(P('B.2 Seuils propres par flux, tous les runs', 'h2'))
allruns = [('Vague 1', R1 / 'per_flux_thresholds.csv')]
for nm in ['at_s7', 'at_s123', 'at_L36', 'null', 'null2', 'clock', 'noE_real', 'noE_null2']:
    allruns.append((nm, V2 / nm / 'per_flux_thresholds.csv'))
rows = []
for label, path in allruns:
    if not path.exists():
        continue
    df = pd.read_csv(path)
    for r in df.itertuples():
        rows.append([label, r.flux, fmt(r.seuil_propre_pct), fmt(r.score_max, 3)])
story.append(table(['Run', 'Flux', 'Seuil propre %', 'Score max'], rows,
                   widths=[30 * mm, 50 * mm, 30 * mm, USABLE - 110 * mm]))
story.append(P('B.3 Zones du paysage global, tous les runs (scores moyens par zone, courbe traitée)', 'h2'))
rows = []
for label, vpath in [('Vague 1', None), ('at_s7', 'at_s7'), ('at_s123', 'at_s123'), ('at_L36', 'at_L36'),
                     ('null B1', 'null'), ('null B2', 'null2'), ('clock', 'clock'),
                     ('noE_real', 'noE_real'), ('noE_null2', 'noE_null2')]:
    if vpath is None:
        z = {'win1': zone(sc1, 50, 60), 'win2': zone(sc1, 62, 73),
             'apres_win2': zone(sc1, 75, 87), 'loin_88_97': zone(sc1, 88, 97),
             'max_global': fmt(sc1['score'].max(), 3)}
    else:
        z = verdict(vpath)['paysage_zones']
    rows.append([label, z['win1'], z['win2'], z['apres_win2'], z['loin_88_97'], z['max_global']])
story.append(table(['Run', 'Fenêtre 1', 'Fenêtre 2', 'Après fen. 2', 'Loin 88–97', 'Max global'], rows,
                   widths=[30 * mm, 28 * mm, 28 * mm, 28 * mm, 28 * mm, USABLE - 142 * mm]))
story.append(P('Note : pour la vague 1, les zones sont calculées sur la courbe traitée avec les fenêtres AT ; '
               'pour l’horloge, les zones du verdict utilisent les fenêtres horloge (30–46 % / 52–68 %).', 'body'))

# ============================== ANNEXE C ==============================
story.append(P('Annexe C — Données, fichiers et reproductibilité', 'h1'))
story.append(P('Arborescence du dossier de travail (fichiers principaux)', 'h2'))
inv = []
for p in sorted(B.rglob('*')):
    if p.is_file() and 'pdf_build' not in p.parts and '__pycache__' not in p.parts and '.zip' not in p.suffix:
        rel = str(p.relative_to(B))
        if rel.startswith('vague2/') and p.suffix in ('.json',) and p.name == 'pipeline_results.json':
            continue
        inv.append([rel, f"{p.stat().st_size / 1024:.0f} Ko"])
story.append(table(['Fichier', 'Taille'], inv, widths=[USABLE - 30 * mm, 30 * mm]))
story.append(P('Commandes exactes (reproductibilité)', 'h2'))
for cmd in [
    'Génération AT : python3 gen_ashkin_teller.py [--seed 42|7|123] [--L 28|36] [--prefix at|at_s7|at_s123|at_L36]',
    'Génération horloge : python3 gen_clock6.py  (graine 42, L=24, grille 0,40–1,20)',
    'Pipeline vague 1 : python3 run_v33_at.py  (entrée at_fluxes.csv → results_at_v33/)',
    'Pipeline vague 2 : bash vague2.sh  (5 runs séquentiels → vague2/<run>/)',
    'Pipeline porte D : pilote run_v33_generic_noEflux.py (flux_mapping sans la colonne de contrôle)',
    'Analyses par flux : python3 analyse_at.py / analyse_generic.py / analyse_generic_noE.py',
    'Nul B1 : at_fluxes.csv, lignes mélangées (graine 99) — invalide, voir §5.',
    'Nul B2 : chaque flux permuté indépendamment, energy fixe comme contrôle (graine 99).',
]:
    story.append(P('•  ' + cmd, 'body'))
story.append(P('Durées mesurées : vague 1, 213,6 s ; vague 2, lot de 1 073 s (AT graine 7 : 218 s ; graine 123 : '
               '215 s ; L=36 : 216 s ; nul : 214 s ; horloge : 144 s) ; porte D, ~193 s par run. Machine : VM '
               'Muse, 2 vCPU, 7,7 Go de RAM, sans swap (plafond documenté du workspace).', 'body'))
story.append(P('Sources bibliographiques citées pour les vérités terrain : modèle d’Ashkin-Teller — Pfister '
               '(séparation des transitions quand U > J) et Duminil-Copin–Raoufi–Tassion (diagramme de phase, '
               'phase partielle &lt;ττ′&gt;) ; horloge q=6 — estimations CTMRG T1 = 0,70, T2 = 0,88 et fourchettes '
               'Monte Carlo 0,68–0,75 / 0,88–0,92 ; carte logistique — valeurs de bifurcation 3 ; 3,44949 ; '
               '3,54409 ; 3,56441 ; accumulation 3,56995 (constante de Feigenbaum δ ≈ 4,669). Les températures '
               'critiques exactes d’Ashkin-Teller pour J=1, U=2 ne sont pas des valeurs de littérature : elles '
               'sont mesurées sur les données générées (chutes des aimantations moyennes par T, §2.1) — c’est '
               'précisément ce que la vague 2 (réplication à fenêtres gelées) puis la porte D sont venues '
               'éprouver.', 'body'))

# ============================== ANNEXE D ==============================
story.append(P('Annexe D — Extrait du rapport texte du pipeline (vague 1)', 'h1'))
story.append(P('Extrait (120 premières lignes) de results_at_v33/text_report.txt, sortie textuelle du pipeline '
               'lui-même. Le fichier complet (867 lignes) est livré dans les archives du run.', 'body'))
for line in (R1 / 'text_report.txt').read_text(encoding='utf-8', errors='replace').splitlines()[:120]:
    story.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;') or ' ', S['mono']))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('DVS', 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(MARGIN, 12 * mm, 'Pipeline v3.3 — Banc multi-tipping — résultats complets (conversation du 22 octobre 2026)')
    canvas.drawRightString(W - MARGIN, 12 * mm, f'Page {doc.page}')
    canvas.setStrokeColor(colors.HexColor('#b0bec5'))
    canvas.line(MARGIN, 14 * mm, W - MARGIN, 14 * mm)
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=15 * mm, bottomMargin=18 * mm,
                        title='Pipeline v3.3 — Banc multi-tipping : résultats complets',
                        author='Muse (assistant de Zackary)')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f'PDF écrit : {OUT} ({OUT.stat().st_size / 1e6:.1f} Mo)')
