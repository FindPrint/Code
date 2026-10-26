# Protocole gelé — Air Quality Dataset (Kaggle srisyra02) x pipeline v3.3-H1
Gelé le 2026-10-26 ~08h50 HAE, AVANT tout run.

## Source
- URL utilisateur : https://www.kaggle.com/datasets/srisyra02/air-quality-dataset
- Auteur affiché sur Kaggle : Srimathy Sivanessan, mise à jour il y a 13 jours
  (page consultée le 26 oct. 2026). Licence affichée : CC0 (domaine public).
- Fichier téléchargé via le navigateur (session Kaggle déjà active, aucun achat,
  aucune création de compte) : `data/air_quality_dataset.csv` — 59 976 octets
  (59,98 ko affichés par Kaggle), 1 seul fichier dans le dataset.
- SHA-256 du fichier téléchargé :
  aaf87134601406a882713a37e990b466945e680d9dd3ee00161ecf62b1ba1f97
- Description Kaggle (page) : mesures horaires de polluants et de météo en
  milieu urbain en Arabie saoudite, inspirées du dataset UCI Air Quality,
  avec une étiquette Source (Traffic, Industrial, Biomass) pour de la
  classification supervisée.

## Écart constaté AVANT run, entre la page Kaggle et le fichier réel
- Le fichier téléchargé NE contient NI Date, NI Time, NI étiquette Source,
  NI les colonnes capteurs PT08.S1–S5, NI RH/AH décrites sur la page.
- Il contient 10 colonnes numériques seulement : PM2.5, PM10, NOx, NO2, SO2,
  VOCs, CO, CO2, CH4, Temperature. La description de la page n'est donc PAS
  reprise comme description du fichier : le PDF décrira le fichier tel que
  téléchargé, et signalera cet écart.
- Valeurs négatives présentes dans le fichier réel, alors qu'il s'agit de
  concentrations : NOx min −0,08, NO2 min −1,94, SO2 min −1,10. Aucune
  correction appliquée : le fichier est utilisé tel quel, et ces valeurs
  sont signalées comme réserve (bruit de mesure, ou données synthétisées).

## Inventaire vérifié AVANT run (structure, pas un résultat du pipeline)
- 500 lignes, 10 colonnes, 0 valeur manquante.
- Toutes les colonnes sont numériques continues, chacune avec 500 valeurs
  uniques (aucun doublon, aucun palier discret) :
  PM2.5 (10,76–127,62 ; moy. 54,67), PM10 (12,93–171,59 ; moy. 84,70),
  NOx (−0,08–225,89 ; moy. 91,81), NO2 (−1,94–115,92 ; moy. 42,41),
  SO2 (−1,10–31,94 ; moy. 11,51), VOCs (27,56–231,93 ; moy. 112,19),
  CO (0,37–4,80 ; moy. 2,18), CO2 (366,06–558,92 ; moy. 439,29),
  CH4 (1,39–3,35 ; moy. 2,13), Temperature (19,58–39,78 ; moy. 30,45).
- Fichier de travail `data/air_quality_dataset_pipeline.csv` (500 lignes,
  10 colonnes) : copie exacte vérifiée (même SHA-256), aucune colonne
  dérivée, aucune colonne texte à encoder — toutes les colonnes d'origine
  sont déjà numériques. L'original est conservé tel quel.

## Runs : 10, un par colonne en contrôle
- Contrôles (10) : PM2.5, PM10, NOx, NO2, SO2, VOCs, CO, CO2, CH4,
  Temperature. Aucune colonne n'est sautée.
- Pipeline : `pipeline_autonome_v3_3_harmonic_v1.py` TEL QUEL (uploadé par
  l'utilisateur ce jour), mode stable, w_size 80, cohen_d, graine 42,
  HARMONIC_PROB 0,45 (défaut du fichier).
- Règle Porte D : la colonne de contrôle est EXCLUE des flux analysés.
  Chaque run analyse donc les 9 autres colonnes numériques comme flux,
  via flux_mapping explicite.
- Ordre des lignes : ordre du fichier d'origine, sans tri préalable.
- Aucun seuil attendu pré-enregistré : données réelles, pas de vérité
  terrain pour un « seuil critique » au sens du pipeline. Lecture =
  mesure descriptive : seuil global MC, seuil par défaut, seuils bruts,
  stabilité, scores Q, diagnostic bruit, ancres, seuils propres par flux
  (fonction de scan du pipeline, config MC du run), paysage (maxima
  locaux), F1/F2 post-seuil.
- Règle d'échec pré-enregistrée : contrôle avec moins de 80 valeurs
  valides = échec mesuré. Ici les 10 contrôles ont 500 valeurs valides :
  aucun échec prévisible par manque de points.
- Parallélisme : 2 runs maximum en simultané (plafond CPU/RAM de la VM).
- Pilote : `scripts/run_one.py` (adaptation directe du pilote
  breast-cancer : même structure, chemins et fichier changés, même
  extraction des résumés). Design résumable : un run déjà terminé
  (run_summary.json présent) n'est pas relancé.

## Réserves d'interprétation (gelées avant run)
- Pas de colonne temporelle dans le fichier réel : le « contrôle » est un
  axe de rang le long de la colonne, pas un temps. Aucune lecture causale
  ou temporelle, et aucune lecture « horaire » malgré la description de la
  page Kaggle.
- Aucune étiquette Source dans le fichier : aucune lecture par source
  d'émission n'est possible sur ce fichier.
- Valeurs négatives de NOx/NO2/SO2 : signalées, non corrigées.
- Aucune conclusion sanitaire ou réglementaire ne sera tirée des seuils :
  ce sont des mesures du pipeline sur ce fichier, pas des seuils de
  qualité de l'air.
