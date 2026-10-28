# Conception gelée — Q6 : Actif vs Réceptif standardisé (v3.5.4)

Gelée le 28 oct. 2026, AVANT toute modification. Décisions de
l'utilisateur (28 oct.) : (a) Q5 déplacé ACCEPTÉ tel quel ;
(c) la version standardisée devient Q6, question séparée,
jamais un remplacement de Q5. Nouveau fichier
`Tlog_v3_5_4_harmonic_v1.py`, copie de v3.5.3-H1
(SHA `f2580464…`), v3.5.3 / v3.5.2 / v3.5 / v3.4 intacts.
Livré AVANT exécution (aucun run/pilote).

## Rappel du mécanisme Q5 (lu dans le code, 28 oct. 2026)

Q5 est la seule question qui compare chaque colonne à une
moyenne calculée sur les AUTRES colonnes : `act_avg` = moyenne
ligne par ligne de toutes les colonnes des flux actifs,
`react_avg` = idem côté réceptif ; Q5[colonne] =
`separation_score` (Cohen d) entre la colonne et la moyenne du
groupe opposé (les flux ni actifs ni réceptifs comparent à la
moyenne des deux). Q1–Q4 comparent chaque colonne à elle-même
ou flux par flux : elles ne bougent pas quand on ajoute des
colonnes. En v3.5 la moyenne porte sur 1 278 colonnes de 29
estimateurs d'échelles incommensurables (~1 à ~112), dominée
par les plus grandes magnitudes — d'où le déplacement de Q5
même pour les 5 historiques. Q5 accepté : il répond
désormais à « séparation contre la moyenne des 29 ».

## Définition gelée de Q6

Fonction module `_q6_scores(df_feat, feature_cols, fluxes,
active_keys, reactive_keys, stat_test, min_grp)`, même
embranchement que Q5, avec UNE différence : chaque colonne
est standardisée AVANT les moyennes de groupe.

- Standardisation par colonne, sur valeurs non-NaN :
  moyenne `nanmean`, écart-type `nanstd` **ddof=0**
  (convention du pipeline, comme `apply_complexity`).
  Colonne sans moyenne/écart-type fini, ou écart-type
  < 1e-12 (constante) → série nulle.
- Moyennes de groupe : moyennes ligne par ligne (pandas,
  NaN ignorés) des colonnes standardisées actives /
  réceptives.
- Q6[colonne] = `separation_score(colonne standardisée,
  moyenne standardisée du groupe opposé)`, NaN → 0,0
  (comme Q5). Groupes vides → tous 0,0 (comme Q5).
- Clés : `Q6_Active_Reactive_Standardized` et
  `Q6_Actif_Receptif_Standardise` (même dictionnaire, comme
  Q5). Exclue de `top_signatures` comme Q5 (seule la clé
  française y figure, comme Q5 aujourd'hui).
- Q5 : TOUCHÉ À RIEN. Graphiques : inchangés (la liste des
  questions du paysage reste à 5). F1/F2, scan, MC,
  normalisation : inchangés.

## Propriétés à vérifier (avant toute exécution)

- X1 : v3.5.4 charge ; SHA v3.5.3 inchangé ; diff limité
  (fonction + appel + exclusion + en-tête).
- X2 : invariance d'échelle — multiplier une colonne par 100
  ne change AUCUNE valeur Q6 (tolérance 1e-12).
- X3 : sur colonnes déjà standardisées, Q6 égale la logique
  Q5 appliquée aux mêmes colonnes (même embranchement).
- X4 : colonne constante et colonne tout-NaN → Q6 0,0,
  sans exception ; groupes vides → tous 0,0.
- X5 : Q1–Q5, F1/F2, scores : code inchangé (diff vérifié).

## AMENDEMENT — DÉFINITION CORRIGÉE Q6-A (28 oct. 2026, choix utilisateur)

L'utilisateur choisit l'option A : **on ne centre pas, on
divise seulement par l'écart-type**. Cette section remplace
la définition « standardisation complète » ci-dessous pour
la construction livrée ; la section dégénérescence est
conservée comme trace.

- Mise à l'échelle seule : pour chaque colonne,
  `écart-type = nanstd(colonne, ddof=0)` (convention du
  pipeline, comme le z-score de `apply_complexity`) ;
  colonne mise à l'échelle = `colonne / écart-type`,
  SANS soustraire la moyenne. Les NaN sont conservés.
- Colonne dégénérée (moyenne/écart-type non finis, ou
  écart-type < 1e-12 : constante) → série de zéros
  (contribution nulle, n'empoisonne pas la moyenne).
- Moyennes de groupe : moyennes ligne par ligne (pandas,
  NaN ignorés) sur les colonnes mises à l'échelle, même
  branchement que Q5 (actifs / réceptifs / ni l'un ni
  l'autre → moyenne des deux moyennes).
- Q6[colonne] = `separation_score` (colonne mise à
  l'échelle, moyenne opposée mise à l'échelle), NaN → 0,0 ;
  groupes vides → tout à 0,0.
- Clés : `Q6_Active_Reactive_Scaled` et
  `Q6_Actif_Receptif_Echelle` (même dict, comme Q5) ;
  exclues de `top_signatures` comme Q5 ; Q5 inchangé ;
  tracés inchangés ; F1/F2, scan, MC, normalisation
  inchangés.
- Propriétés exigées (vérifications non vacues) :
  invariance par changement d'échelle d'une colonne
  (×100 → Q6 inchangé) ; valeurs NON nulles sur données
  à moyennes distinctes ; Q6 ≠ Q5 (nouvelle question,
  pas une copie) ; Q6 = logique Q5 appliquée à des
  colonnes pré-mises à l'échelle (écart ~1e-12).

## DÉGÉNÉRESCENCE CONSTATÉE (28 oct. 2026, avant livraison)

La v3.5.4 construite selon cette conception est DÉGÉNÉRÉE et
n'a PAS été livrée. Mesure : sur frame synthétique, TOUTES les
valeurs Q6 valent 0,0 (2e-16). Mécanisme vérifié dans le code :
`separation_score` = |Cohen d| = différence des MOYENNES
divisée par l'écart-type poolé. Après standardisation
complète (centrage + échelle), chaque colonne a moyenne 0 et
chaque moyenne de groupe a moyenne 0 : Q6 ≡ 0 par
construction. Les vérifications X2/X3/X4 « passaient »
vacuement (0 = 0). La standardisation tue exactement ce que
la statistique de Q5 mesure. Définitions corrigées proposées
à l'utilisateur (choix en attente) :
- Q6-A : mise à l'échelle seule (diviser par l'écart-type,
  SANS centrer) — même statistique, la moyenne de groupe
  n'est plus dominée, les niveaux relatifs subsistent.
- Q6-B : z-score complet + delta de Cliff (rangs) —
  insensible à l'échelle, sensible à la forme, statistique
  différente.
- Q6-C : z-score complet + distance de forme
  (moyenne |z_colonne − moyenne_groupe|) — dissimilarité
  d'évolution en unités standard, hors famille séparation.

## Ouvert

- Choix de la définition corrigée (A, B ou C) par
  l'utilisateur, puis reconstruction + livraison.
- Comparaison Q5/Q6 sur run complet : seulement sur go
  explicite (pilote). Aucun run lancé avec v3.5.4.
