# Protocole gelé — Mushroom Classification × pipeline v3.4-H3
# Lot reparti de zéro le 26 octobre 2026, à la demande de l'utilisateur

## Demande
Télécharger tous les CSV du dataset Kaggle `uciml/mushroom-classification`,
les fusionner en un seul CSV, passer le pipeline sur chaque colonne (flux)
en colonne de contrôle, une après l'autre, et livrer tous les résultats,
sources, démarche et informations dans un seul PDF incluant les images.
Pipeline utilisé : le NOUVEAU pipeline `Tlog_v3_4_harmonic_v3.py`.
Lot reparti de zéro : aucun résultat du lot v3.3 n'est repris dans ce lot.

## Source de données (vérifiée, identique au téléchargement du 26 oct. 2026)
- Dataset Kaggle : https://www.kaggle.com/datasets/uciml/mushroom-classification
- Fichier téléchargé : `mushroom-classification.zip`, 35 057 octets,
  SHA-256 `4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081`
- Contenu : UN SEUL CSV, `mushrooms.csv` (374 003 octets, daté 2019-09-20
  dans l'archive), SHA-256 `f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c`.
  La « fusion » est donc triviale : aucun autre fichier à joindre, aucune
  ligne ajoutée ni retirée. Le fichier de travail n'est PAS re-téléchargé
  pour ce lot : il est recopié et ses empreintes re-vérifiées identiques.
- Inventaire : 8 124 lignes × 23 colonnes, 0 ligne exactement dupliquée.
  Toutes les colonnes sont des codes catégoriels à une lettre, aucune
  numérique d'origine : class, cap-shape, cap-surface, cap-color, bruises,
  odor, gill-attachment, gill-spacing, gill-size, gill-color, stalk-shape,
  stalk-root, stalk-surface-above-ring, stalk-surface-below-ring,
  stalk-color-above-ring, stalk-color-below-ring, veil-type, veil-color,
  ring-number, ring-type, spore-print-color, population, habitat.
- class : e = 4 208, p = 3 916.
- stalk-root : '?' sur 2 480 lignes (30,5 %) — seul marqueur de manquant.
- veil-type : constante ('p' sur les 8 124 lignes).

## Encodage (nécessaire, le pipeline n'accepte que du numérique)
- Chaque lettre → entier par ordre de première apparition dans le fichier,
  par colonne. Table complète : `data/mapping_encodage.json`.
  Exemples : class p=0, e=1 ; odor p=0, a=1, l=2, n=3, f=4, c=5, y=6, s=7, m=8 ;
  veil-type p=0 (seule valeur).
- '?' de stalk-root n'est PAS une catégorie : encodé comme vrai manquant
  (NaN). Conséquence, par le code même du pipeline : en contrôle, le
  pipeline supprime ces lignes (5 644 valides pour stalk-root) ; en flux,
  le pipeline remplace NaN par la moyenne du flux avant z-score.
- Fichier de travail : `data/mushrooms_pipeline.csv` (8 124 × 23, numérique),
  SHA-256 `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`.
  Original préservé dans `data/raw/`.

## Pipeline (gelé avant tout run de ce lot)
- Fichier : `workspace/user/files/Tlog_v3_4_harmonic_v3.py`
  SHA-256 `81092eb61d612d0dea50f9fca6bfa12f6dbd2388c4e52a24ab064d09e61dc7f8`
  (version corrigée du 26 oct. : début valide des fenêtres avec NaN).
  Dérivé de `pipeline_autonome_v3_3_harmonic_v1.py` (v3.3-H1, intact).
- Changements v3.4-H3 par rapport à v3.3-H1 :
  1. Scan optimisé à résultats identiques (groupes non concaténés, même
     tirage graine 0, même séquence rng partagée g1/g2). Vérifié :
     pilote traité, seuil 52,75 %, écart maximal 0,0 sur 801 candidats ;
     flux brut stalk-root seul, écart 0,0 après correction.
  2. Fallback Monte Carlo journalisé (stdout + stderr + logging +
     métadonnées `threshold_source` / `threshold_warnings` + rapport) :
     un seuil de repli ne peut plus passer pour un seuil Monte Carlo.
     Seuil d'urgence 52,5 % du diagnostic bruit (seuil NaN) également
     journalisé.
  3. F1/F2 avant ET après seuil (champs `first_derivative_pre`,
     `second_derivative_pre` + deltas post-pré + `sign_change`) ; les
     champs post existants sont inchangés.
  4. Export JSON robuste (tuples, ensembles, tableaux numpy sanitizés).
- Réglages : mode stable, w_size initial 80, test cohen_d, graine 42,
  HARMONIC_PROB 0,45 (défaut du fichier, non surchargé),
  full_triangulation False.
- 23 runs, un par colonne en contrôle, dans l'ordre du fichier, contrôle
  EXCLU des flux analysés (règle Porte D), ordre original des lignes
  (le pipeline range le contrôle lui-même).

## Design résumable et règles d'échec
- Un run avec `run_summary.json` présent est sauté ; un run tué en cours
  (redémarrage VM, arrêt volontaire) est jeté et relancé de zéro, jamais
  compté. Les dossiers vides des runs interrompus du lot v3.3 ne sont
  pas repris.
- Règle d'échec pré-enregistrée : contrôle avec < 80 valeurs valides =
  échec mesuré (aucun attendu ici : minimum 5 644 valides, stalk-root).
- Le run veil-type est tenté comme les autres ; son résultat est
  enregistré tel quel, jamais lu comme un détecteur (flux constant).

## Réserves d'interprétation (gelées)
- Les codes encodés sont des étiquettes nominales, pas des grandeurs :
  un seuil est une coupure de rang sur un ordre arbitraire (apparition),
  à lire comme plateaux de rang.
- JAMAIS une règle pour décider si un champignon est comestible.
  Le PDF le dira explicitement.
- Aucune lecture temporelle ou causale (aucune colonne de temps).
- Lecture descriptive seulement : données réelles, sans vérité terrain,
  aucun seuil attendu n'est affirmé.
- Détail complet exigé dans les rapports : seuils sur tous les flux,
  dérivés F1/F2 avant et après seuil, seuils MC / par défaut / brut /
  témoin 1001, stabilité vérifiée contre la moyenne bootstrap.

## Lot v3.3 arrêté (traçabilité)
- Le lot v3.3 lancé à 14h56 a été arrêté le 26 oct. vers 16h28 à la
  demande de repartir de zéro avec la v3.4. Les runs cap-shape,
  cap-surface, cap-color, bruises, odor, gill-attachment ont été tués
  avant tout fichier de sortie (dossiers vides) : rien n'est perdu,
  rien n'est repris. Le pilote v3.3 (contrôle class, terminé 14h35)
  reste conservé séparément dans `workspace/mushroom/results/ctrl_class/`,
  uniquement pour comparaison, hors de ce lot.

## Livrables (dossier mushroom-v34/)
- Par contrôle : `results/ctrl_<colonne>/` (run_summary, scan_curve,
  per_flux_thresholds, transition_F1F2 avec pré+post, text_report,
  pipeline_results.json, figures threshold_scan et noise_diagnostic).
- Synthèse : `synthese_runs.csv`, `tous_seuils_par_flux.csv`,
  `tous_F1F2.csv`, `plateaux_controles.csv`.
- Final : `Mushroom_Classification_v34_Resultats_complets.pdf`,
  `RAPPORT.md`, zip des résultats (pipeline_results.json exclus du zip,
  conservés dans results/).
