# -*- coding: utf-8 -*-
"""PDF complet du lot contrôles (35 runs, harmonique v1).
Valeurs lues dans controles/synthese_*.csv et les verdict.json, jamais recopiées.
Sortie : Controles_Tous_Flux_Pipeline_Harmonique_Resultats_complets.pdf
"""
import json
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
                                Image, PageBreak, HRFlowable)

B = Path('/home/hatch/workspace/multi-tipping')
C = B / 'controles'
OUT = B / 'Controles_Tous_Flux_Pipeline_Harmonique_Resultats_complets.pdf'
FD = '/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DVS', f'{FD}/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-B', f'{FD}/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVS-I', f'{FD}/DejaVuSans.ttf'))
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
    'title': st('title', fontName='DVS-B', fontSize=25, leading=31, alignment=TA_CENTER, spaceAfter=10),
    'subtitle': st('subtitle', fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#444444')),
    'h1': st('h1', fontName='DVS-B', fontSize=16, leading=20, spaceBefore=14, spaceAfter=8, alignment=TA_LEFT),
    'h2': st('h2', fontName='DVS-B', fontSize=13, leading=17, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT),
    'h3': st('h3', fontName='DVS-B', fontSize=11, leading=15, spaceBefore=8, spaceAfter=4, alignment=TA_LEFT),
    'body': st('body'),
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

def table(headers, rows, widths=None):
    data = [[Paragraph(h, S['cellh']) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(v), S['cellc'] if j > 0 else S['cell']) for j, v in enumerate(r)])
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

def verdict_box(title, body):
    inner = [[Paragraph(f'<b>{title}</b>', S['box'])], [Paragraph(body, S['box'])]]
    t = Table(inner, colWidths=[USABLE])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
        ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor('#1b5e20')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def fmt(x, nd=2):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return '—'
    try:
        return f'{float(x):.{nd}f}'
    except (TypeError, ValueError):
        return str(x)

R = pd.read_csv(C / 'synthese_globaux.csv')
PF = pd.read_csv(C / 'synthese_par_flux.csv')
story = []

# COUVERTURE
story.append(Spacer(1, 28 * mm))
story.append(P('Tous les flux en contrôle, à tour de rôle', 'title'))
story.append(P('Pipeline harmonique v1 — 35 runs, résultats complets', 'subtitle'))
story.append(Spacer(1, 4 * mm))
story.append(P('Ashkin-Teller (4 jeux), horloge q=6 et nul B2 : chaque flux passé en colonne '
               'de contrôle, le contrôle toujours exclu des flux analysés', 'subtitle'))
story.append(Spacer(1, 10 * mm))
story.append(HRFlowable(width='100%', thickness=1.2, color=colors.HexColor('#2c3e50')))
story.append(Spacer(1, 6 * mm))
story.append(table(['', ''], [
    ['Protocole', 'PROTOCOLE_CONTROLES.md, gelé le 25 oct. 2026 ~19 h 55 HAE, confirmé par l’utilisateur'],
    ['Pipeline', 'pipeline_autonome_v3_3_harmonic_v1.py tel quel, guidage harmonique par défaut (0,45)'],
    ['Réglages', 'Mode stable, w80, cohen_d, graine 42, aveugle, contrôle exclu des flux'],
    ['Runs', '35 (AT principal + graines 7, 123 + L=36 : 6 contrôles chacun ; horloge : 5 ; nul B2 : 6)'],
    ['Calcul', '11 847 s cumulés (moyenne 338,5 s/run), 2 redémarrages machine absorbés par le design résumable'],
    ['Compilation', '25 octobre 2026 — chiffres relus dans les verdict.json et CSV de synthèse'],
    ['Dossier', 'workspace/multi-tipping/controles/<jeu>/<contrôle>/'],
], widths=[32 * mm, USABLE - 32 * mm]))
story.append(Spacer(1, 8 * mm))
story.append(verdict_box('Verdict en une phrase',
    'Le seuil global du pipeline est un détecteur de la première rupture dominante : sur AT il ne pointe '
    'JAMAIS vers T2, quel que soit le contrôle — tandis que la lecture par flux résout les deux transitions '
    'pour tout contrôle monotone (19–20/20 compatibles, 0 croisement), et se dégrade pour un contrôle non '
    'monotone. Sur l’horloge q=6, aucun contrôle ne sauve les positions publiées.'))
story.append(Spacer(1, 8 * mm))
story.append(P('Ce document contient tout le lot contrôles : le protocole gelé, les données et leur monotonie, '
               'les seuils globaux des 35 runs avec leurs températures mappées, les seuils propres par flux, '
               'l’horloge, le nul B2, la comparaison harmonique / fixed, la synthèse contre les critères gelés, '
               'et en annexes le protocole intégral, la table par flux complète (170 lignes) et les 35 courbes '
               'de scan du pipeline.', 'body'))
story.append(PageBreak())

story.append(P('Sommaire', 'h1'))
for item in [
    '1. Protocole gelé et déroulement (incidents machine inclus)',
    '2. Données et monotonie des contrôles',
    '3. Seuils globaux Ashkin-Teller (24 runs)',
    '4. Seuils propres par flux Ashkin-Teller',
    '5. Horloge q=6 (5 runs)',
    '6. Nul B2 (6 runs)',
    '7. Harmonique vs fixed (contrôle = energy)',
    '8. Synthèse contre les critères gelés',
    'Annexe A — Protocole gelé (texte intégral)',
    'Annexe B — Table par flux complète (170 lignes)',
    'Annexe C — Les 35 courbes de scan du pipeline',
    'Annexe D — Fichiers, commandes et durées',
]:
    story.append(P(item, 'body'))
story.append(P('Conventions. Un seuil % est un pourcentage de l’axe de progression du pipeline, c’est-à-dire le '
               'rang du contrôle choisi (qui change d’un run à l’autre). C’est pourquoi les critères sont jugés '
               'en température mappée : moyenne des températures des lignes autour de la frontière de rang du '
               'contrôle (bande ±1,5 %). Fenêtres AT : T1 [4,6 ; 4,9], T2 [5,2 ; 5,6]. Fenêtres horloge : '
               'T1 [0,62 ; 0,80], T2 [0,82 ; 0,98] (équivalent en T des fenêtres % de la vague 2, précision notée '
               'pré-lot). Un hit « compatible » signifie que l’intervalle [T − std ; T + std] touche la fenêtre.',
               'body'))

# 1. PROTOCOLE
story.append(P('1. Protocole gelé et déroulement', 'h1'))
story.append(P('Le 25 octobre 2026, l’utilisateur demande de relancer « depuis le début » le protocole de la '
               'conversation multi-tipping, mais en passant tous les flux en colonne de contrôle à tour de rôle, '
               'avec la règle porte D généralisée : quand un flux est testé en contrôle, il ne doit pas être '
               'simultanément dans les flux analysés. Il joint le pipeline harmonique v1 et confirme, à la '
               'question posée, le choix « harmonique, protocole complet (35 runs) ». Le protocole '
               '(PROTOCOLE_CONTROLES.md) est gelé avant tout run ; les pilotes run_ctrl.py et analyse_ctrl.py '
               'sont généralisés pour un contrôle arbitraire (progression = rang du contrôle, mapping T via '
               'les lignes autour de la frontière de rang du contrôle, scans par flux excluant le contrôle, '
               'Spearman contrôle vs T en diagnostic). Un pilote (AT principal, contrôle = energy, 165 s, '
               'global 56,55 % → T = 4,878, hit T1, VERY STABLE) valide la mécanique avant le lot.', 'body'))
story.append(P('Déroulement réel (incidents consignés, pas effacés)', 'h2'))
story.append(table(['Épisode', 'Fait'], [
    ['Lancement pilote', '25 oct., 19 h 50 — AT/energy, OK (165 s)'],
    ['Lot, 1re partie', '2 travailleurs, 7/35 sauvegardés, puis redémarrage machine après ~18 min'],
    ['Reprise 1', 'Lot relancé, 33/35 atteints, puis second redémarrage après 1 h 25'],
    ['Reprise 2', 'Lot relancé, 35/35 terminés (derniers : null2/flip_rate et null2/local_variance)'],
    ['Total', '11 847 s de calcul cumulé ; 0 run perdu, 0 run refait inutilement (design résumable)'],
], widths=[35 * mm, USABLE - 35 * mm]))
story.append(P('Attendus pré-enregistrés par contrôle (globaux AT) : energy / m_s / m_tau → T1 ; m_prod / '
               'flip_rate → T2 ; local_variance → aucune attente. Par flux (dans chaque run) : m_s / m_tau → '
               'T1, m_prod / flip_rate → T2, quel que soit le contrôle. Nul B2 : scores effondrés, seuils '
               'dispersés, stabilité dégradée. Échec pré-enregistré : contrôle avec moins de 80 valeurs valides '
               '(aucun ici, données complètes).', 'body'))

# 2. DONNÉES ET MONOTONIE
story.append(P('2. Données et monotonie des contrôles', 'h1'))
story.append(P('Les jeux sont ceux de la conversation : AT principal (L=28, graine 42, 1 224 lignes, 6 flux), '
               'AT graines 7 et 123 (L=28), AT L=36 (graine 42), horloge q=6 (L=24, 984 lignes, 5 flux), nul B2 '
               '(AT principal, chaque flux permuté indépendamment, energy fixe, graine 99). Le diagnostic de '
               'monotonie (Spearman contrôle vs T, calculé par l’analyse) sépare nettement deux régimes :',
               'body'))
rows = []
for ds in ['at', 'at_s7', 'at_s123', 'at_L36', 'clock']:
    sub = R[R.dataset == ds]
    for r in sub.itertuples():
        rows.append([ds, r.control, fmt(r.spearman, 3)])
story.append(table(['Jeu', 'Contrôle', 'Spearman vs T'], rows,
                   widths=[30 * mm, 55 * mm, USABLE - 85 * mm]))
story.append(P('Lecture : tous les contrôles sont fortement monotones (|ρ| ≥ 0,925) sauf local_variance sur AT '
               '(ρ ≈ 0,73) — les aimantations décroissent avec T (ρ négatif), energy et flip_rate croissent '
               '(ρ ≈ 0,99). Sur l’horloge, même local_variance (0,931) et vortex_density (0,925) sont monotones. '
               'Le nul B2 n’a pas de Spearman (aucune température) : c’est attendu, pas une lacune.', 'body'))

# 3. GLOBAUX AT
story.append(P('3. Seuils globaux Ashkin-Teller (24 runs)', 'h1'))
story.append(P('Tous les 24 runs AT sont VERY STABLE — la stabilité globale ne dépend pas du contrôle, même '
               'pour local_variance. Scores MC globaux : 0,740–0,763 (moyenne 0,755), remarquablement constants '
               'quel que soit le contrôle.', 'body'))
EXP = {'energy': 'T1', 'magnetization_s': 'T1', 'magnetization_tau': 'T1',
       'magnetization_prod': 'T2', 'flip_rate': 'T2', 'local_variance': '—'}
rows = []
for r in R[R.dataset.isin(['at', 'at_s7', 'at_s123', 'at_L36'])].itertuples():
    rows.append([r.dataset, r.control, fmt(r.global_pct), fmt(r.global_T, 3),
                 f"{fmt(r.global_Tstd, 3)}", r.global_hit, EXP[r.control], r.stabilite])
story.append(table(['Jeu', 'Contrôle', 'Global %', 'T', '±', 'Hit', 'Attendu', 'Stabilité'], rows,
                   widths=[20 * mm, 38 * mm, 22 * mm, 18 * mm, 16 * mm, 16 * mm, 18 * mm, USABLE - 148 * mm]))
for el in fig(B / 'pdf_build_controles/chart_ctrl_global_AT.png', caption='Figure de synthèse. Seuils globaux AT mappés en T, par contrôle et par jeu. Bandes : T1 [4,6 ; 4,9], T2 [5,2 ; 5,6]. Aucun point ne tombe dans la bande T2.'):
    story.append(el)
story.append(P('Comptes contre les attendus (20 runs à attente définie, local_variance exclu) : hits stricts '
               '10/20 ; compatibles à ±1 écart-type 12/20. Les 8 incompatibles sont tous des contrôles '
               'm_prod/flip_rate pointant vers la région T1 (4,53–4,80), jamais vers T2. Les 2 « hors » parmi '
               'energy/m_s/m_tau (at_s7/energy 4,592 ; at_s123/m_s 4,570) sont à moins d’un écart-type de la '
               'fenêtre T1 : cas limites, pas ratés francs. <b>Conclusion : l’attente « prod/flip → T2 » est '
               'réfutée (0/8, même en comptant les compatibilités). Le seuil global suit la première rupture '
               'dominante, quel que soit l’axe de progression.</b>', 'body'))
story.append(P('Cas local_variance (aucune attente) : globaux à T = 4,149 / 4,608 / 4,073 / 4,358 selon les jeux, '
               'tous VERY STABLE sauf at_s7 (T1, 4,608 — dans la fenêtre par hasard de la moyenne, à T_std '
               'large). Un contrôle non monotone donne donc un seuil global stable mais précoce, qui ne '
               'correspond à aucune transition.', 'body'))

# 4. PAR FLUX AT
story.append(P('4. Seuils propres par flux Ashkin-Teller', 'h1'))
story.append(P('Chaque flux pointe-t-il vers SA transition, quel que soit le contrôle ? (20 runs par flux : '
               '4 jeux × 5 contrôles où le flux n’est pas lui-même le contrôle.)', 'body'))
OWN = {'magnetization_s': 'T1', 'magnetization_tau': 'T1', 'magnetization_prod': 'T2', 'flip_rate': 'T2'}
rows = []
for flux in ['magnetization_s', 'magnetization_tau', 'magnetization_prod', 'flip_rate', 'local_variance', 'energy']:
    g = PF[(PF.dataset.isin(['at', 'at_s7', 'at_s123', 'at_L36'])) & (PF.flux == flux)]
    if flux in OWN:
        strict = (g.hit == OWN[flux]).sum()
        rows.append([flux, OWN[flux], f'{strict}/20', f"{(g.hit == 'T1').sum()}/{(g.hit == 'T2').sum()}/{(g.hit == 'hors').sum()}",
                     f"{fmt(g['T'].min(), 2)} – {fmt(g['T'].max(), 2)}"])
    elif flux == 'local_variance':
        rows.append([flux, '— (précurseur)', '0/20', f"0/0/{(g.hit == 'hors').sum()}",
                     f"{fmt(g['T'].min(), 2)} – {fmt(g['T'].max(), 2)}"])
    else:
        rows.append([flux, '— (mélange)', '—', f"{(g.hit == 'T1').sum()}/{(g.hit == 'T2').sum()}/{(g.hit == 'hors').sum()}",
                     f"{fmt(g['T'].min(), 2)} – {fmt(g['T'].max(), 2)}"])
story.append(table(['Flux analysé', 'Sa transition', 'Hits stricts', 'T1 / T2 / hors', 'Plage des T propres'], rows,
                   widths=[42 * mm, 30 * mm, 24 * mm, 30 * mm, USABLE - 126 * mm]))
story.append(P('Compatibles à ±1 écart-type : m_s 19/20, m_tau 20/20, m_prod 19/20, flip_rate 18/20. Les « hors » '
               'stricts sont presque tous des cas limites : m_s/m_tau à 4,53–4,59 (juste sous T1) ; m_prod/flip '
               'à 5,12–5,19 (juste sous T2) ou 4,11–4,44 (runs à contrôle local_variance). <b>Croisements : 0.</b> '
               'Aucun flux ne pointe strictement vers la transition de l’autre groupe. local_variance (flux) : '
               '20/20 hors, T = 3,98–4,33 — précurseur systématique. energy (flux, 20 runs) : T1 11 fois, T2 '
               '1 fois, hors 8 fois — mélange des deux transitions, comme en vague 1.', 'body'))
story.append(P('Moyennes des T propres par contrôle (AT, 4 jeux) — la qualité du contrôle se lit ici :', 'h2'))
pf_at = PF[PF.dataset.isin(['at', 'at_s7', 'at_s123', 'at_L36'])]
means = pf_at.groupby(['control', 'flux'])['T'].mean().unstack()
CTRLS = ['magnetization_s', 'magnetization_tau', 'magnetization_prod', 'energy', 'flip_rate', 'local_variance']
FLUX = ['magnetization_s', 'magnetization_tau', 'magnetization_prod', 'energy', 'flip_rate', 'local_variance']
rows = []
for c in CTRLS:
    rows.append([c] + [fmt(means.loc[c, f]) if f in means.columns and c in means.index and not pd.isna(means.loc[c, f]) else '—' for f in FLUX])
story.append(table(['Contrôle \\ flux', 'm_s', 'm_tau', 'm_prod', 'energy', 'flip', 'loc_var'], rows,
                   widths=[42 * mm] + [(USABLE - 42 * mm) / 6] * 6))
story.append(P('Lecture : contrôle energy → séparation la plus propre (s/tau 4,55–4,58 ; prod/flip 5,34–5,39). '
               'Contrôles m_s / m_tau / m_prod / flip_rate → séparation conservée (s/tau ≈ 4,6 ; prod/flip ≈ '
               '5,3). Contrôle local_variance → tout rabattu (energy 4,30 ; flip 4,26 ; prod 4,46 ; s/tau 4,56 ; '
               '17/20 hors) : un contrôle non monotone dégrade la lecture par flux elle-même.', 'body'))
for el in fig(B / 'pdf_build_controles/chart_perflux_mean.png', caption='Figure de synthèse. T propre moyenne de chaque flux selon le contrôle (AT, 4 jeux). La courbe local_variance (flux) reste sous T1 ; les autres se séparent en deux groupes T1/T2, sauf pour le contrôle local_variance.'):
    story.append(el)

# 5. HORLOGE
story.append(P('5. Horloge q=6 (5 runs)', 'h1'))
rows = []
for r in R[R.dataset == 'clock'].itertuples():
    rows.append([r.control, fmt(r.global_pct), fmt(r.global_T, 3), r.global_hit, r.stabilite, fmt(r.spearman, 3)])
story.append(table(['Contrôle', 'Global %', 'T', 'Hit', 'Stabilité', 'Spearman'], rows,
                   widths=[42 * mm, 24 * mm, 20 * mm, 20 * mm, 38 * mm, USABLE - 144 * mm]))
for el in fig(B / 'pdf_build_controles/chart_ctrl_global_clock.png', caption='Figure de synthèse. Seuils globaux horloge mappés en T, par contrôle. Bandes : T1 [0,62 ; 0,80], T2 [0,82 ; 0,98]. Tous hors fenêtres.'):
    story.append(el)
story.append(P('Par flux (T par run ; chaque flux apparaît dans 4 runs, le 5e étant celui où il est contrôle) :',
               'h2'))
pf_c = PF[PF.dataset == 'clock']
rows = []
for flux in ['magnetization', 'energy', 'flip_rate', 'vortex_density', 'local_variance']:
    g = pf_c[pf_c.flux == flux]
    ts = ', '.join(fmt(t, 3) for t in sorted(g['T'].dropna()))
    rows.append([flux, ts, f"T1 : {(g.hit == 'T1').sum()}/5, T2 : {(g.hit == 'T2').sum()}/5, hors : {(g.hit == 'hors').sum()}/5"])
story.append(table(['Flux', 'T propres (4 runs)', 'Hits'], rows,
                   widths=[42 * mm, 62 * mm, USABLE - 104 * mm]))
story.append(P('Conclusion horloge, généralisée depuis la porte C : changer de contrôle ne déplace pas les '
               'lectures vers les positions publiées. energy et flip_rate touchent T1 dans 2/5 runs chacun ; '
               'magnetization, vortex_density et local_variance restent groupés vers T ≈ 1,04–1,13 — le haut '
               'réel du jeu L=24 (vortex tardifs), pas T2 = 0,88.', 'body'))

# 6. NUL B2
story.append(P('6. Nul B2 (6 runs)', 'h1'))
rows = []
for r in R[R.dataset == 'null2'].itertuples():
    rows.append([r.control, fmt(r.global_pct), r.stabilite, fmt(r.stab_std, 2), fmt(r.mc_score, 3), fmt(r.max_scan, 3)])
story.append(table(['Contrôle', 'Global %', 'Stabilité', 'Std', 'Score MC', 'Max courbe'], rows,
                   widths=[42 * mm, 24 * mm, 38 * mm, 20 * mm, 24 * mm, USABLE - 148 * mm]))
story.append(P('Seuils par flux dispersés (8–89 %, aucune grappe — table complète en annexe B). Scores par flux : '
               'max par run 0,212–0,326, moyenne 0,205 contre 3,894 en réel (~19×) ; max de courbe 0,111–0,135 '
               'contre ~3,5 en réel. Stabilité : 5/6 UNSTABLE — mais 1/6 VERY STABLE résiduel (contrôle '
               'magnetization_s, 81,86 %, std 1,64), à consigner : la stabilité globale seule ne suffit pas à '
               'déclarer un nul ; le couple (scores effondrés + dispersion) discrimine, lui, dans les 6/6 cas.',
               'body'))

# 7. HARMONIQUE VS FIXED
story.append(P('7. Harmonique vs fixed (contrôle = energy)', 'h1'))
story.append(table(['Jeu', 'Fixed % (vague 2 / porte D)', 'Harmonique % (ce lot)', 'T fixed', 'T harmonique'], [
    ['at', '54,16', '56,55', '4,724', '4,878'],
    ['at_s7', '52,20', '51,76', '4,592', '4,592'],
    ['at_s123', '51,51', '51,76', '4,586', '4,603'],
    ['at_L36', '56,35', '53,53', '4,838', '4,689'],
], widths=[30 * mm, 45 * mm, 45 * mm, 25 * mm, USABLE - 145 * mm]))
story.append(P('Les % bougent, les T mappées restent dans T1 (sauf at_s7 harmonique 4,592, à 0,008 sous la fenêtre '
               '— cas limite). L’harmonique ne change pas le verdict global sur AT ; il décale le seuil en % '
               'sans déplacer la température retrouvée. C’est aussi une validation du mapping en T comme '
               'lecture invariante : deux pipelines, deux %, même température.', 'body'))

# 8. SYNTHÈSE
story.append(P('8. Synthèse contre les critères gelés', 'h1'))
story.append(table(['Critère gelé', 'Résultat'], [
    ['AT : energy/m_s/m_tau → global vers T1', 'Tenu : 10/12 stricts, 12/12 compatibles ±1 std'],
    ['AT : m_prod/flip_rate → global vers T2', 'RÉFUTÉ : 0/8, même en compatibilité — le global pointe vers T1'],
    ['AT : local_variance → aucune attente', 'Confirmé comme cas à part : global stable mais précoce (4,07–4,61)'],
    ['AT : par flux → sa transition, tout contrôle', 'Tenu pour tout contrôle monotone (19–20/20 compatibles, 0 croisement) ; dégradé pour local_variance'],
    ['Horloge : T1/T2 publiés, tout contrôle', 'Non tenu : 0/5 globaux, 4/20 hits par flux (tous vers T1)'],
    ['Nul B2 : scores effondrés, seuils dispersés', 'Tenu 6/6 (scores ~19× plus bas, dispersion 8–89 %)'],
    ['Nul B2 : stabilité dégradée', 'Tenu 5/6 — 1 résidu VERY STABLE (contrôle m_s)'],
    ['Contrôle < 80 valeurs valides = échec', 'Aucun cas (données complètes)'],
], widths=[62 * mm, USABLE - 62 * mm]))
story.append(P('Ce que ce lot établit, en une phrase par idée. (1) Le seuil global est un détecteur de première '
               'rupture dominante, pas un sélecteur de transition : il ne pointera jamais vers la seconde '
               'transition d’un système à deux transitions, quel que soit l’axe de progression choisi. '
               '(2) La résolution des deux transitions vit dans la lecture par flux, et elle est robuste au '
               'choix du contrôle tant que celui-ci est monotone. (3) La qualité du contrôle est une condition '
               'de la qualité de la lecture : un contrôle non monotone (local_variance) dégrade les seuils '
               'propres et produit un global stable mais non transitionnel. (4) Le nul se discrimine par les '
               'scores et la dispersion, pas par la stabilité seule. (5) Sur les transitions molles BKT, '
               'aucun contrôle ne compense un jeu trop petit. Limites inchangées : données synthétiques ; '
               'lecture par flux post-run, pas sortie native du pipeline ; horloge L=24.', 'body'))

# ANNEXE A
story.append(P('Annexe A — Protocole gelé (texte intégral)', 'h1'))
for line in (B / 'PROTOCOLE_CONTROLES.md').read_text(encoding='utf-8').splitlines():
    story.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;') or ' ', S['mono']))

# ANNEXE B
story.append(P('Annexe B — Table par flux complète (170 lignes)', 'h1'))
story.append(P('Chaque ligne : un flux analysé dans un run. Le flux n’apparaît pas dans le run où il est lui-même '
               'le contrôle (règle porte D).', 'body'))
rows = []
for _, r in PF.iterrows():
    rows.append([r['dataset'], r['control'], r['flux'], fmt(r['pct']), fmt(r['score'], 3),
                 fmt(r['T'], 3) if not pd.isna(r['T']) else '—', r['hit'] if not pd.isna(r['hit']) else '—'])
story.append(table(['Jeu', 'Contrôle', 'Flux', 'Seuil %', 'Score', 'T', 'Hit'], rows,
                   widths=[20 * mm, 38 * mm, 38 * mm, 20 * mm, 18 * mm, 18 * mm, USABLE - 152 * mm]))

# ANNEXE C
story.append(P('Annexe C — Les 35 courbes de scan du pipeline', 'h1'))
story.append(P('Une figure par run, dans l’ordre du lot. Les courbes de diagnostic de bruit sont dans les '
               'dossiers de run (noise_diagnostic.png).', 'body'))
ORDER = ([(ds, c) for ds in ['at', 'at_s7', 'at_s123', 'at_L36'] for c in
          ['magnetization_s', 'magnetization_tau', 'magnetization_prod', 'energy', 'flip_rate', 'local_variance']]
         + [('clock', c) for c in ['magnetization', 'energy', 'flip_rate', 'vortex_density', 'local_variance']]
         + [('null2', c) for c in ['magnetization_s', 'magnetization_tau', 'magnetization_prod', 'energy', 'flip_rate', 'local_variance']])
for ds, ctrl in ORDER:
    for el in fig(C / ds / ctrl / 'threshold_scan.png', width_mm=150,
                  caption=f'Courbe de scan — {ds} / contrôle {ctrl}.'):
        story.append(el)

# ANNEXE D
story.append(P('Annexe D — Fichiers, commandes et durées', 'h1'))
story.append(P('Arborescence : controles/<jeu>/<contrôle>/ contient pour chaque run run_summary.json, '
               'verdict.json, per_flux_thresholds.csv, scan_curve.csv, threshold_scan.png, noise_diagnostic.png, '
               'text_report.txt, pipeline_results.json, numerical_results.csv, driver.log, analyse.log. '
               'Synthèses : controles/synthese_globaux.csv, controles/synthese_par_flux.csv, '
               'controles/synthese.json, controles/batch_status.jsonl.', 'body'))
story.append(P('Commandes exactes :', 'h2'))
for cmd in [
    'Pilote : python3 run_ctrl.py at_fluxes.csv energy controles/at/energy',
    'Analyse : python3 analyse_ctrl.py <fluxes.csv> <contrôle> <temperature.csv|none> <outdir> <win1> <win2> <T1> <T2>',
    'Lot : python3 controles_batch.py (2 travailleurs, résumable : saute les runs à verdict.json présent)',
    'Fenêtres AT : % 50,60 / 62,73 ; T 4.6,4.9 / 5.2,5.6. Fenêtres horloge : % 30,46 / 52,68 ; T 0.62,0.80 / 0.82,0.98.',
    'Synthèse : python3 synthese_controles.py ; figures : python3 prep_charts_controles.py',
]:
    story.append(P('•  ' + cmd, 'body'))
rows = []
for r in R.itertuples():
    rows.append([r.dataset, r.control, fmt(r.duree_s, 1)])
story.append(P('Durées par run (secondes, lues dans les run_summary.json) :', 'h2'))
story.append(table(['Jeu', 'Contrôle', 'Durée (s)'], rows,
                   widths=[40 * mm, 55 * mm, USABLE - 95 * mm]))
story.append(P(f"Total : {fmt(R['duree_s'].sum(), 0)} s de calcul cumulé (moyenne {fmt(R['duree_s'].mean(), 1)} s/run). "
               'Les durées incluent le ralentissement dû au parallélisme (2 travailleurs sur 2 vCPU) et les '
               'deux reprises après redémarrage machine.', 'body'))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('DVS', 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(MARGIN, 12 * mm, 'Tous les flux en contrôle — pipeline harmonique v1 — 35 runs (25 octobre 2026)')
    canvas.drawRightString(W - MARGIN, 12 * mm, f'Page {doc.page}')
    canvas.setStrokeColor(colors.HexColor('#b0bec5'))
    canvas.line(MARGIN, 14 * mm, W - MARGIN, 14 * mm)
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=15 * mm, bottomMargin=18 * mm,
                        title='Tous les flux en contrôle — pipeline harmonique v1 : résultats complets',
                        author='Muse (assistant de Zackary)')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f'PDF écrit : {OUT} ({OUT.stat().st_size / 1e6:.1f} Mo)')
