# SYNTHÈSE — Lot UNIVERSAL_LOG mushroom RÉDUIT : 23/23 OK (30 oct. 2026)

## Verdict
Lot TERMINÉ le 30 oct. 2026 vers 19 h 23 (heure de Montréal) : **23/23
contrôles OK, 0 échec**. Vérifié run par run depuis chaque
`ctrl_<contrôle>/run_summary.json` (statut OK) — pas depuis le seul
`lot_progress.json` (qui marque les contrôles sautés « OK (déjà fait) »).

## Provenance
- Code : `workspace/user/files/UNIVERSAL_LOG.py`, VERSION v3.5.5-HP-v1,
  SHA-256 `2f58d414e636976737ecb35ae9285aa60eb9102346262e1d882f308b659e4479`,
  jamais modifié.
- Données : `data/mushrooms_reduced_2000.csv`, 2 000 × 23, sous-échantillon
  stratifié par class (graine 42) de `mushrooms_pipeline.csv`
  (SHA `fa6e5ceb…`), SHA-256
  `dee932631ad36ac0f23cae5f744ee02165764ced49bf5e0f9d1fa21458a9cfe8`.
- Paramètres : mode `stable`, w_size 80, test `cohen_d`, random_seed 42,
  full_triangulation False. Chaque contrôle exclu de ses propres flux.
- Historique : lot lancé 15 h 24, 4e redémarrage VM vers 17 h 27 (11/23 déjà
  OK, seul stalk-root perdu, ~2 min), reprise par saut des contrôles OK,
  fin 19 h 23. Calcul cumulé des runs : ~13 885 s (≈ 3 h 51).

## Seuils par contrôle (opt_threshold du pipeline, en %)
| Contrôle | Seuil (%) | Durée (s) | Note |
|---|---|---|---|
| class | 53,17 | 487,7 | |
| cap-shape | 77,93 | 741,6 | |
| cap-surface | 25,86 | 691,8 | |
| cap-color | 81,55 | 685,1 | |
| bruises | 38,92 | 519,6 | |
| odor | 56,21 | 686,1 | |
| gill-attachment | 55,50 | 458,6 | |
| gill-spacing | 57,23 | 956,9 | |
| gill-size | 19,63 | 591,5 | |
| gill-color | 99,37 | 222,4 | Seuil très haut |
| stalk-shape | 43,45 | 955,3 | |
| stalk-root | 20,75 | 315,3 | 589 manquants dans le réduit |
| stalk-surface-above-ring | 83,80 | 484,8 | |
| stalk-surface-below-ring | 81,51 | 492,2 | |
| stalk-color-above-ring | 98,10 | 160,9 | Seuil très haut |
| stalk-color-below-ring | 98,26 | 165,1 | Seuil très haut |
| veil-type | NaN | 2 385,3 | AUCUN seuil valide (voir ci-dessous) |
| veil-color | 57,92 | 407,1 | |
| ring-number | 55,52 | 822,9 | |
| ring-type | 90,67 | 469,9 | Seuil haut |
| spore-print-color | 98,89 | 165,0 | Seuil très haut |
| population | 96,46 | 296,5 | Seuil très haut |
| habitat | 69,83 | 723,7 | |

## Cas particulier : veil-type
- Statut OK mais **opt_threshold = NaN** : ni le Monte Carlo ni le scan par
  défaut n'ont produit de seuil valide ; le pipeline a basculé sur sa
  valeur de secours (52,5 %) pour le diagnostic bruit, et les analyses
  post-seuil ont été ignorées.
- Cohérent avec le pilote v3.5 (contrôle class) où veil-type était
  inclassable (AUC 0,500) : contrôle quasi constant, peu à couper.
- Conséquence : veil-type est EXCLU des loupes estimateur par seuil
  (cohortes non étiquetables), mais ses séries restent dans les sorties.

## Limites (dites, pas cachées)
- Sur le réduit, AUCUNE comparaison directe avec le pilote v3.5
  (autres lignes) : le lot se juge sur ses propres nuls et sa cohérence
  interne, pas contre le seuil pilote class de 52,75 %.
- Seuils = ceux du pipeline seul (Monte Carlo + scan), sans jugement
  physique : un seuil haut (98–99 %) décrit la position du maximum de
  contraste dans ce run, pas une criticité établie.
- Données = échantillons HYPOTHÉTIQUES du guide Audubon 1981, pas des
  spécimens mesurés ; couleurs/odeurs = mots humains.

## Suite
Loupes estimateur sur les sorties fraîches (mêmes loupes A/B/C que le
pilote mushroom, généralisées aux 23 runs × 22 flux, veil-type exclu),
puis rapport comparatif. Publication GitHub sur décision de Zackary.
