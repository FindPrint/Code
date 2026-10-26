# Protocole gelé — Food_Costs 2016 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1
Gelé le 2026-10-26, AVANT les runs de 2016 (répétition exacte du protocole 2013, seule l'année change ; choix utilisateur du 26 oct. 2026 : 2014, puis 2015 et 2016, chacun avec son PDF séparé).

## Source
- URL : https://www.kaggle.com/datasets/jpmiller/publicassistance
- Titre Kaggle : « US Public Food Assistance 1 - WIC », auteur JohnM (jpmiller) ; licence affichée : « Other (specified in description) ».
- Dataset complet : 68 fichiers CSV, dont 4 fichiers nommés Food_Costs.csv (2013, 2014, 2015, 2016). Ce protocole ne porte QUE sur 2016.

## Fichier retenu (2016)
- Chemin dans le dataset : `WICAgencies2016ytd/Food_Costs.csv`
- Fichier original conservé : `data/Food_Costs_2016_original.csv` — 12662 octets, SHA-256 `bca57e0b1c26f05bef42dadc3da6a28ebb7c60ff28782061d52994827dd64402` (extrait de l'archive complète déjà téléchargée le 26 oct. 2026, session Kaggle GlobalZivotPrint, aucun achat, aucune création de compte).
- Période couverte par les colonnes mensuelles : 2015-10 a 2016-09 (exercice WIC 2016).

## Inventaire vérifié AVANT run
- 92 lignes, 14 colonnes d'origine, ordre des lignes = ordre du fichier, sans tri.
- Colonnes d'origine : `State Agency or Indian Tribal Organization` (texte, 91 noms distincts), 12 colonnes mensuelles, `Cumulative Cost` (stockée en texte dans le fichier).
- Valeurs valides par colonne mensuelle et Cumulative Cost : 91 (voir inventaire JSON pour chaque colonne) ; lignes en double et valeurs négatives : voir sortie du pilote (reprise dans le PDF).
- Fichier de travail `data/Food_Costs_2016_pipeline.csv` (92 lignes, 15 colonnes) : copie exacte des colonnes d'origine PLUS `agency_encoded` (codes 0–90 par ordre d'apparition, pandas factorize) et conversion de Cumulative Cost en nombre (vérifiée égale à la somme des 12 mois, écart maximal 0.0). SHA-256 du fichier de travail : `58c07de6ff4f066ff60316ff9e1b8712a7f567e60227acd0a3e0dc67069af7ec`. La colonne texte d'origine n'est JAMAIS passée directement au pipeline.
- Mountain Plains : ligne = 223486855.0 ; somme des 10 États + 10 agences tribales du groupe = 223,486,855 ; écart = 0.0 (à confirmer dans le PDF selon le signe : 0 = agrégat exact comme en 2013).

## Runs : 14, un par colonne en contrôle
- Contrôles (14, dans l'ordre du fichier) : `agency_encoded` (pour la colonne texte d'origine), les 12 mois, `Cumulative Cost`. Aucune colonne n'est sautée : 14 sur 14.
- Pipeline : `pipeline_autonome_v3_3_harmonic_v1.py` TEL QUEL, mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45 (défaut).
- Règle Porte D : la colonne de contrôle est EXCLUE des flux analysés. Chaque run analyse donc les 13 autres colonnes numériques comme flux, via flux_mapping explicite.
- Ordre des lignes : ordre du fichier d'origine, sans tri préalable.
- Aucun seuil attendu pré-enregistré : lecture descriptive seulement.
- Règle d'échec pré-enregistrée : contrôle avec moins de 80 valeurs valides = échec mesuré.
- Parallélisme : 2 runs maximum en simultané. Pilote : `scripts/run_one.py` (adaptation du pilote 2013). Design résumable : un run déjà terminé (run_summary.json présent) n'est pas relancé.

## Réserves d'interprétation (gelées avant run, mêmes que 2013)
- Petit n (~92 lignes) : avec w_size 80, les fenêtres sont très larges par rapport à n (scan plafonné à n//2) ; prudence accrue, pas de classement direct des scores avec les séries à grand n.
- Les lignes sont des agences/États, pas une série temporelle : le contrôle est un axe de rang, pas un temps.
- Cumulative Cost est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels.
- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier, pas un seuil géographique ou économique.
- Aucune conclusion de politique publique, budgétaire ou nutritionnelle ne sera tirée des seuils.
