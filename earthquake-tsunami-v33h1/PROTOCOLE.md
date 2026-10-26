# Protocole gelé — Global Earthquake Tsunami Risk Assessment (Kaggle ahmeduzaki) x pipeline v3.3-H1
Gelé le 2026-10-25 ~10h52 HAE, AVANT tout run.

## Source
- URL utilisateur : https://www.kaggle.com/datasets/ahmeduzaki/global-earthquake-tsunami-risk-assessment-dataset
- Fichier téléchargé via l'API publique Kaggle : kaggle.zip -> earthquake_data_tsunami.csv
  (782 lignes, 13 colonnes, un seul CSV dans l'archive)
  magnitude, cdi, mmi, sig, nst, dmin, gap, depth, latitude, longitude, Year, Month, tsunami
- Nettoyage : AUCUN. Fichier utilisé tel quel (earthquake_data_tsunami.csv).
  Toutes les colonnes sont déjà numériques, 0 valeur manquante sur les 782 lignes.

## Fait mesuré avant run (structure, pas un résultat du pipeline)
- 782 lignes >= 80 requis : aucun échec prévisible par manque de points de contrôle.
- Contrôles discrets / à paliers de rang (réserve d'interprétation, comme Heart Attack) :
  tsunami binaire (0 = 61,1 %, 1 = 38,9 %) -> un seuil en % entre les paliers
  sépare les mêmes deux groupes ; cdi (10 valeurs, 0 = 27,1 %), mmi (9 valeurs),
  Month (12 valeurs), Year (22 valeurs), magnitude (24 valeurs).
- latitude/longitude sont géographiques, pas des axes de progression temporelle :
  elles sont quand même lancées en contrôle, comme demandé (les 13 colonnes),
  lecture descriptive seulement.

## Runs : 13, un par colonne en contrôle
- Pipeline : pipeline_autonome_v3_3_harmonic_v1_1_omg2.py TEL QUEL (uploadé ce jour),
  mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0.45 (défaut du fichier).
- Règle Porte D (mesurée le 22 oct.) : la colonne de contrôle est EXCLUE des flux
  analysés (pas d'auto-séparation tautologique). Chaque run analyse donc les 12 autres
  colonnes comme flux, via flux_mapping explicite.
- Aucun seuil attendu pré-enregistré : données réelles, pas de vérité terrain pour un
  "seuil critique" au sens du pipeline. Lecture = mesure descriptive : seuil global MC,
  seuil par défaut, seuils bruts, stabilité, scores Q, diagnostic bruit, ancres,
  seuils propres par flux (fonction de scan du pipeline, config MC du run),
  paysage (maxima locaux), F1/F2 post-seuil.
- Pilote : scripts/run_one.py (adaptation directe de heart-attack/scripts/run_one.py :
  même module d'import changé pour la version _1_omg2, même chemin de données,
  même extraction des résumés). 2 runs en parallèle maximum (plafond CPU/RAM de la VM).
