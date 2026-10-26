# -*- coding: utf-8 -*-
import json
from pathlib import Path
import pandas as pd
BASE=Path('/home/hatch/workspace/food-costs-2013')
syn=pd.read_csv(BASE/'synthese_runs.csv')
PF=pd.read_csv(BASE/'tous_seuils_par_flux.csv')
FF=pd.read_csv(BASE/'tous_F1F2.csv')
def short(c):
    if c=='agency_encoded': return 'Agency'
    if c=='Cumulative Cost': return 'Cumulative'
    return c[:7]
L=[]
L.append("# Food_Costs 2013 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1 — Rapport des 14 contrôles\n")
L.append("Protocole : `PROTOCOLE.md` (réglages gelés le 26 oct. 2026 avant le lot ; pilote de faisabilité Cumulative Cost à 11h24, mêmes réglages, puis protocole rédigé ~11h25, puis 13 autres runs ; lot interrompu par un redémarrage du service à 9/14, repris par les seuls manquants, terminé à 11h27).")
L.append("Pipeline uploadé, tel quel : mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse les 13 autres colonnes numériques. Source : `data/Food_Costs_2013_original.csv` (WICAgencies2013ytd/Food_Costs.csv, 92 lignes, 14 colonnes, exercice WIC 2013, octobre 2012 à septembre 2013). Fichier de travail : copie exacte + `agency_encoded` + Cumulative Cost convertie en nombre (vérifiée égale à la somme des 12 mois, écart 0). Aucun seuil attendu pré-enregistré : lecture descriptive seulement, aucune conclusion de politique publique, budgétaire ou nutritionnelle.\n")
L.append("## Écarts et pièges de structure (constatés avant / vérifiés sur le fichier)\n")
L.append("- Le dataset complet compte 68 fichiers, dont 4 fichiers nommés Food_Costs.csv (2013, 2014, 2015, 2016) : seul 2013 est traité ici, les 3 autres années feront 3 autres PDF séparés.")
L.append("- Texas apparaît deux fois : une ligne entièrement vide et une ligne réelle (Cumulative 303 294 654) ; chaque colonne mensuelle et Cumulative Cost ont donc 91 valeurs valides, pas 92.")
L.append("- Une seule valeur mensuelle négative, conservée telle quelle : Pennsylvania, novembre 2012, −550 874.")
L.append("- **Mountain Plains est une ligne d'agrégat** : 253 793 211, exactement la somme des 10 États et des 10 agences tribales du groupe Mountain Plains qui la précèdent dans le fichier (écart 0). Le total du fichier (4 751 013 254) double-compte donc 253,8 millions, et Mountain Plains figure à tort parmi les « 12 plus grandes ».")
L.append("- Cumulative Cost est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels.\n")
L.append("## Verdict en une ligne\n")
L.append(f"**14/14 runs terminés, 0 échec** (durée totale des runs : {syn.duree_s.sum():.1f} s, ~{syn.duree_s.mean():.0f} s par run). Stabilité (critère du pipeline) : VERY STABLE = 14. **Mais** cette note repose sur l'écart-type bootstrap (≈ 0, 7 valeurs bootstrap identiques), pas sur l'accord MC / moyenne bootstrap : écart de 28,79 points pour les 13 contrôles numériques et de 40,91 points pour Agency. La note VERY STABLE ne doit donc PAS être lue comme une confirmation du seuil MC.")
L.append("Les 13 contrôles numériques donnent exactement le même seuil MC, **87,88 %** (défaut 59,26 %, moyenne bootstrap 59,09 %). Agency donne **83,33 %** (défaut 29,63 %, moyenne bootstrap 42,42 %). 87,88 %, c'est la coupure après les 12 plus grandes agences, qui totalisent 62,6 % du total du fichier sur Cumulative Cost. Les courbes de scan montent régulièrement jusqu'à 87,88 % puis s'arrêtent (plus de score au-delà) : ce n'est pas un pic intérieur, c'est le bord de la zone calculable qui isole la queue des très grandes agences.\n")
L.append("## Synthèse par contrôle\n")
L.append("| contrôle | n | seuil MC % | défaut % | MC−défaut | moy. bootstrap % | MC−moy. | stabilité | score MC | scan max | valeur au MC (médiane) | durée s |")
L.append("|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|")
for r in syn.itertuples():
    L.append(f"| {short(r.controle)} | {int(r.n_lignes)} | {r.seuil_MC_pct:.2f} | {r.seuil_defaut_pct:.2f} | {r.ecart_MC_moins_defaut:+.2f} | {r.stabilite_moy_pct:.2f} | {r.ecart_MC_moins_moybootstrap:+.2f} | {r.stabilite} | {r.score_MC:.3f} | {r.scan_global_max:.3f} | {r.valeur_controle_au_MC_mediane:,.0f} | {r.duree_s:.1f} |")
L.append("")
L.append("## Groupes au-dessus du seuil MC par contrôle\n")
TOP=pd.read_csv(BASE/'top_au_dessus.csv')
for r in TOP.itertuples():
    L.append(f"- {short(r.controle)} ({int(r.n_au_dessus)} au-dessus) : plus petite au-dessus = {r.min_au_dessus:,.0f} ({r.agence_min_au_dessus}), plus grande en dessous = {r.max_en_dessous:,.0f} ({r.agence_max_en_dessous}) — {r.liste_au_dessus}.")
L.append("")
L.append("3 mois sur 12 (juin, août, septembre) partagent exactement le même groupe au-dessus que Cumulative Cost ; les autres mois en diffèrent par un membre échangé (sauf octobre 2012 et janvier 2013 : deux membres échangés). Ce n'est donc pas 13 seuils indépendants, c'est 13 fois la même queue de grandes agences.\n")
L.append("## Seuils propres par flux (top 10 de tout le banc, 182 seuils)\n")
for r in PF.nlargest(10,'score_max').itertuples():
    L.append(f"- contrôle {short(r.controle)} : flux {short(r.flux)} {r.seuil_propre_pct:.2f} % (score {r.score_max:.3f}).")
L.append("")
L.append("En tant que flux (moyenne sur les 13 runs où la colonne est flux) :")
g=PF.groupby('flux')['score_max'].agg(['mean','max']).sort_values('mean',ascending=False)
for k,v in g.iterrows():
    L.append(f"- {short(k)} : moyenne {v['mean']:.3f}, max {v['max']:.3f}.")
L.append("")
L.append("## Seuils propres par flux (top 3 par run)\n")
L.append("| contrôle (MC %) | flux 1 | flux 2 | flux 3 |")
L.append("|---|---|---|---|")
for c in syn.controle:
    pf=PF[PF.controle==c].nlargest(3,'score_max')
    cells=[f"{short(r.flux)} {r.seuil_propre_pct:.2f} % ({r.score_max:.3f})" for r in pf.itertuples()]
    mc=syn[syn.controle==c].iloc[0].seuil_MC_pct
    L.append(f"| {short(c)} ({mc:.2f} %) | {' | '.join(cells)} |")
L.append("")
L.append("Détail complet des 182 seuils propres (14 × 13) : `tous_seuils_par_flux.csv`.\n")
L.append("## Scores Q moyens par run\n")
for dirname in ['ctrl_Agency']+[f'ctrl_2012-{m:02d}' for m in (10,11,12)]+[f'ctrl_2013-{m:02d}' for m in range(1,10)]+['ctrl_Cumulative']:
    s=json.load(open(BASE/'results'/dirname/'run_summary.json'))
    q=s.get('scores_moyens_par_Q') or {}
    L.append(f"- {dirname.replace('ctrl_','')} : " + ', '.join(f"{k} = {v}" for k,v in q.items()))
L.append("")
L.append("## Dérivées F1/F2 post-seuil, flux « Tous »\n")
tous=FF[FF.flux=='Tous'].pivot_table(index='controle',columns='estimateur',values='F1')
L.append(tous.round(4).to_string())
L.append("")
L.append("Détail complet (980 lignes) : `tous_F1F2.csv`.\n")
L.append("## Réserves (gelées avant les runs, rappelées ici)\n")
L.append("- Petit n : 92 lignes seulement (91 valides par contrôle numérique), contre 500–569 dans les séries précédentes. Avec w_size 80, les fenêtres sont très larges par rapport à n (la fonction de scan plafonne w_size à n//2) : prudence accrue, pas de classement direct des scores avec les séries à grand n.")
L.append("- Les lignes sont des agences/États, pas une série temporelle : le contrôle est un axe de rang, pas un temps, même pour les colonnes mensuelles (les mois sont des colonnes, pas des lignes).")
L.append("- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier (bloc Western en fin de fichier au-dessus de 83,33 %), pas un seuil géographique ou économique.")
L.append("- Aucune conclusion de politique publique, budgétaire ou nutritionnelle tirée des seuils : mesures du pipeline sur ce fichier.")
(Path(BASE/'RAPPORT.md')).write_text('\n'.join(L), encoding='utf-8')
print("RAPPORT ecrit")
