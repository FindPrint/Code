# PROTOCOLE — Lot UNIVERSAL_LOG mushroom RÉDUIT (gelé le 30 oct. 2026)

## Décision
Zackary, 30 oct. 2026 : après l'annulation du lot plein (2 redémarrages VM
tuant des runs de ~74 min), dataset plus léger = MUSHROOM RÉDUIT.
Le périmètre « tous les contrôles » reste : 23 contrôles, un run par colonne.

## Construction du dataset réduit (dérivé, pas une nouvelle source)
- Source : `workspace/mushroom-v34/data/mushrooms_pipeline.csv`, 8 124 × 23,
  SHA-256 `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`
  (Kaggle uciml/mushroom-classification ; échantillons HYPOTHÉTIQUES du
  guide Audubon 1981, couleurs/odeurs = mots humains).
- Méthode : sous-échantillon STRATIFIÉ par `class`, graine 42, proportions
  conservées, puis mélangé (graine 42). Mêmes 23 colonnes, même encodage
  (ordre d'apparition), aucun nettoyage ajouté.
- Résultat : `data/mushrooms_reduced_2000.csv`, 2 000 × 23,
  SHA-256 `dee932631ad36ac0f23cae5f744ee02165764ced49bf5e0f9d1fa21458a9cfe8`.
- Classes : class 1 = 1 036 (51,8 %), class 0 = 964 (48,2 %) — comme le plein
  (4 208 / 3 916).
- Manquants : seule `stalk-root` en a, 589 (29,5 %), comme le plein
  (2 480, 30,5 %). Aucune autre colonne touchée.

## Code et paramètres (identiques au lot plein annulé)
- Code : `workspace/user/files/UNIVERSAL_LOG.py`, VERSION v3.5.5-HP-v1,
  SHA-256 `2f58d414e636976737ecb35ae9285aa60eb9102346262e1d882f308b659e4479`,
  JAMAIS modifié (version gardée, décision du 30 oct.).
- Paramètres : mode `stable`, w_size 80, test `cohen_d`, random_seed 42,
  full_triangulation False.
- Contrôle EXCLU des flux analysés (décret) ; les 22 autres colonnes sont
  les flux.

## Déroulement
- 23 contrôles, dans l'ordre du CSV : class (en premier — sert aussi de
  MESURE DE DURÉE, référence plein : ~74 min/run), cap-shape, cap-surface,
  cap-color, bruises, odor, gill-attachment, gill-spacing, gill-size,
  gill-color, stalk-shape, stalk-root, stalk-surface-above-ring,
  stalk-surface-below-ring, stalk-color-above-ring, stalk-color-below-ring,
  veil-type, veil-color, ring-number, ring-type, spore-print-color,
  population, habitat.
- SÉQUENTIEL, un run à la fois. Dossiers : `ctrl_<contrôle>/` par run.
- Exports par run : pipeline_results.json, numerical_results.csv,
  text_report.txt, scan_curve.csv, threshold_scan.png, noise_diagnostic.png,
  run_summary.json (statut OK/ECHEC + SHA code et données).

## Reprise après interruption (règle)
- Un run interrompu ne compte pas (sorties en fin de run seulement) : il
  est relancé à l'identique.
- Un contrôle dont le `run_summary.json` indique OK est SAUTÉ à la relance.
- Un contrôle en ECHEC est noté dans lot.log et ne bloque pas les suivants.

## Après le lot
- Synthèse vérifiée des 23 runs, loupes estimateur sur les sorties
  fraîches, rapport comparatif, publication GitHub sur décision de Zackary.
- La comparaison _mean vs pilote v3.5 ne porte que sur le plein : sur le
  réduit, la comparaison directe au pilote n'est PAS applicable (autres
  lignes) ; le réduit se juge sur ses propres nuls et sa cohérence interne.
