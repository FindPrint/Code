# Protocole gelé — Breast Cancer Dataset (Kaggle yasserh) x pipeline v3.3-H1
Gelé le 2026-10-25 ~21h50 HAE, AVANT tout run.

## Source
- URL utilisateur : https://www.kaggle.com/datasets/yasserh/breast-cancer-dataset
- Auteur affiché sur Kaggle : M Yasser H, mise à jour il y a 5 ans.
- Fichier téléchargé via le navigateur (session Kaggle déjà active, aucun achat) :
  `data/breast-cancer.csv` — 122 Ko sur disque (124,57 ko affichés par Kaggle,
  différence d'unité d'affichage), 1 seul fichier dans le dataset.
- SHA-256 du fichier téléchargé : b63d3d9085bad4c5531d2f012d875d820e130a2393acf7720cc173f998140c1e
- Description Kaggle : Breast Cancer Wisconsin (Diagnostic) Dataset ; objectif
  d'origine du dataset = classer les tumeurs en malignes (M) ou bénignes (B)
  à partir de mesures de noyaux cellulaires. Notre usage ici est DESCRIPTIF
  seulement (mesure du pipeline), pas une classification, pas un diagnostic,
  pas une conclusion médicale.

## Inventaire vérifié AVANT run (structure, pas un résultat du pipeline)
- 569 lignes, 32 colonnes d'origine, 0 valeur manquante.
- Colonnes d'origine : `id` (identifiant patient, 569 valeurs uniques),
  `diagnosis` (texte : B = 357, M = 212), et 30 mesures numériques :
  pour chacun des 10 caractères (radius, texture, perimeter, area, smoothness,
  compactness, concavity, concave points, symmetry, fractal_dimension) :
  `_mean`, `_se`, `_worst`.
- Toutes les mesures numériques sont continues (411 à 547 valeurs uniques).
- Fichier de travail `data/breast-cancer_pipeline.csv` (569 lignes, 33 colonnes) :
  copie exacte des 32 colonnes d'origine (vérifié valeur par valeur) PLUS une
  seule colonne dérivée, `diagnosis_encoded` (B = 0, M = 1 ; 357 zéros, 212 uns),
  parce que le pipeline n'accepte que des colonnes numériques. La colonne
  texte `diagnosis` n'est jamais passée directement au pipeline, ni en contrôle
  ni en flux. L'original `breast-cancer.csv` est conservé tel quel.

## Runs : 32, un par colonne en contrôle
- Contrôles (32) : `id`, les 30 mesures, `diagnosis_encoded`.
  Aucune colonne n'est sautée en contrôle : le texte `diagnosis` est couvert
  par son encodage binaire documenté ci-dessus.
- Pipeline : `pipeline_autonome_v3_3_harmonic_v1.py` TEL QUEL (uploadé par
  l'utilisateur ce jour), mode stable, w_size 80, cohen_d, graine 42,
  HARMONIC_PROB 0.45 (défaut du fichier).
- Règle Porte D : la colonne de contrôle est EXCLUE des flux analysés.
  Chaque run analyse donc les 31 autres colonnes numériques comme flux,
  via flux_mapping explicite.
- Ordre des lignes : ordre du fichier d'origine, sans tri préalable.
- Aucun seuil attendu pré-enregistré : données réelles, pas de vérité terrain
  pour un « seuil critique » au sens du pipeline. Lecture = mesure
  descriptive : seuil global MC, seuil par défaut, seuils bruts, stabilité,
  scores Q, diagnostic bruit, ancres, seuils propres par flux (fonction de
  scan du pipeline, config MC du run), paysage (maxima locaux), F1/F2
  post-seuil.
- Règle d'échec pré-enregistrée : contrôle avec moins de 80 valeurs valides
  = échec mesuré. Ici les 32 contrôles ont 569 valeurs valides : aucun
  échec prévisible par manque de points.
- Parallélisme : 2 runs maximum en simultané (plafond CPU/RAM de la VM).
- Pilote : `scripts/run_one.py` (adaptation directe du pilote
  earthquake-tsunami : même structure, module d'import changé pour la
  version harmonic_v1 uploadée, même extraction des résumés).

## Réserves d'interprétation (gelées avant run)
- Données transversales (569 patientes/patients, pas une série temporelle) :
  le « contrôle » est un axe de rang le long de la colonne, pas un temps.
  Aucune lecture causale ou temporelle.
- `id` est un identifiant, pas une mesure : ses runs sont lancés comme
  demandé (toutes les colonnes), lecture descriptive seulement.
- `diagnosis_encoded` est binaire : un seuil en % entre les deux paliers de
  rang sépare les mêmes deux groupes (B vs M) ; ne pas sur-interpréter la
  valeur exacte du % dans ce cas.
- Aucune conclusion médicale ne sera tirée des seuils : ce sont des mesures
  du pipeline sur ce fichier, pas des seuils cliniques.
