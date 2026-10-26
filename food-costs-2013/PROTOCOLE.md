# Protocole gelé — Food_Costs 2013 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1
Réglages gelés le 2026-10-26 avant le lot (choix de l'année par l'utilisateur à 11h22 HAE : commencer par 2013, un PDF pour 2013, puis les 3 autres années feront 3 autres PDF séparés ; proposition de réglages acceptée dans le même message). Précision d'honnêteté sur l'ordre : un pilote de faisabilité d'un seul run (contrôle Cumulative Cost, 8,3 s, réglages strictement identiques) a été lancé avant la rédaction de ce fichier (11h24), puis ce fichier a été rédigé à ~11h25, puis les 13 autres runs ont été lancés après. Le run pilote est conservé tel quel, ses réglages ayant été vérifiés identiques ; il n'a pas été relancé. Le lot a ensuite été interrompu par un redémarrage du service à 9/14 runs, puis repris par les seuls manquants grâce au design résumable (fin 11h27).

## Source
- URL utilisateur : https://www.kaggle.com/datasets/jpmiller/publicassistance
- Titre Kaggle : « US Public Food Assistance 1 - WIC », sous-titre : « Where does it come from, who spends it, who gets it. »
- Auteur affiché : JohnM (identifiant dans l'URL : jpmiller) ; mise à jour affichée : il y a 4 ans (17 avril 2023, d'après le rapport de téléchargement) ; version affichée : Version 9.
- Licence affichée : « Other (specified in description) » ; utilisabilité 9,41 ; étiquettes : Tabular, Social Issues and Advocacy.
- Le dataset complet compte 68 fichiers CSV (16 par dossier annuel WICAgencies2013ytd, 2014ytd, 2015ytd, 2016ytd, plus 4 fichiers est13_16us), 968 colonnes au total. Ce PDF ne porte QUE sur un seul de ces fichiers (voir ci-dessous) ; les années 2014, 2015, 2016 ne sont pas incluses ici.
- Contenu annoncé sur la page : programme WIC (femmes et enfants de moins de cinq ans à faible revenu et à risque nutritionnel), données de participation et de dépenses des programmes des États, exercices 2013–2016 (octobre 2012 à septembre 2016).

## Fichier retenu (2013)
- Chemin dans le dataset : `WICAgencies2013ytd/Food_Costs.csv`
- Fichier téléchargé via le navigateur (session Kaggle déjà active, compte GlobalZivotPrint, aucun achat, aucune création de compte) : archive complète du dataset (304 041 octets) + fichier individuel.
- Fichier original conservé : `data/Food_Costs_2013_original.csv` — 12 695 octets, SHA-256 `9933552f3403d28156eebd9252835bdabe4fffde14625bc068efa63c9c0a9f46`, identique à l'octet près au fichier téléchargé individuellement.
- Période couverte par les colonnes mensuelles : octobre 2012 à septembre 2013 (exercice WIC 2013).

## Inventaire vérifié AVANT run (structure, pas un résultat du pipeline)
- 92 lignes, 14 colonnes d'origine, ordre des lignes = ordre du fichier, sans tri.
- Colonnes d'origine : `State Agency or Indian Tribal Organization` (texte, 91 noms distincts), 12 colonnes mensuelles `2012-10-01 00:00:00` à `2013-09-01 00:00:00` (numériques), `Cumulative Cost` (stockée en texte dans le fichier : chiffres sans séparateur).
- Texas apparaît DEUX fois : une ligne entièrement vide (ligne 39) et une ligne réelle (ligne 40). Conséquence : chaque colonne mensuelle et Cumulative Cost ont 91 valeurs valides et 1 manquante (la ligne Texas vide), pas 92.
- Une seule valeur mensuelle négative, conservée telle quelle, non corrigée : Pennsylvania, novembre 2012, −550 874.
- Échelle très dispersée : coûts mensuels de ~1 000 à ~68 millions, Cumulative Cost de 50 949 à 791 184 631 (California, maximum) ; moyenne annuelle cumulée 52 208 937, médiane 10 214 707. Le pipeline travaille sur des rangs, pas sur les montants bruts : cette dispersion est signalée, pas corrigée.
- Fichier de travail `data/Food_Costs_2013_pipeline.csv` (92 lignes, 15 colonnes) : copie exacte des 14 colonnes d'origine PLUS une seule colonne dérivée, `agency_encoded`, et une seule conversion documentée :
  - `Cumulative Cost` convertie en nombre (to_numeric) : vérifié, après conversion elle égale exactement la somme des 12 mois pour chaque ligne (écart maximal 0,0), 91 valeurs valides, 1 manquante (Texas vide).
  - `agency_encoded` : codes 0–90 par ordre d'apparition dans le fichier (pandas factorize) — Connecticut 0, Maine 1, Massachusetts 2, …, Texas 39 (les deux lignes Texas portent le même code 39, donc un ex æquo), …, Inter-Tribal Council, NV 90. Table complète : `data/agency_encoded_mapping.json`. La colonne texte d'origine n'est JAMAIS passée directement au pipeline, ni en contrôle ni en flux.
- SHA-256 du fichier de travail : `685707f263fac7c00e078f89d5c1c2a02b4620046bf75d71519af0cfaf9fd09f`.

## Runs : 14, un par colonne en contrôle
- Contrôles (14, dans l'ordre du fichier) : `agency_encoded` (pour la colonne texte d'origine), `2012-10-01`, `2012-11-01`, `2012-12-01`, `2013-01-01`, `2013-02-01`, `2013-03-01`, `2013-04-01`, `2013-05-01`, `2013-06-01`, `2013-07-01`, `2013-08-01`, `2013-09-01`, `Cumulative Cost`.
- Aucune colonne n'est sautée : 14 sur 14, comme demandé.
- Pipeline : `pipeline_autonome_v3_3_harmonic_v1.py` TEL QUEL (uploadé par l'utilisateur), mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45 (défaut du fichier).
- Règle Porte D : la colonne de contrôle est EXCLUE des flux analysés. Chaque run analyse donc les 13 autres colonnes numériques comme flux, via flux_mapping explicite.
- Ordre des lignes : ordre du fichier d'origine, sans tri préalable.
- Aucun seuil attendu pré-enregistré : données réelles, pas de vérité terrain pour un « seuil critique » au sens du pipeline. Lecture = mesure descriptive : seuil global MC, seuil par défaut, seuils bruts, stabilité, scores Q, diagnostic bruit, ancres, seuils propres par flux (fonction de scan du pipeline, config MC du run), paysage (maxima locaux), F1/F2 post-seuil.
- Règle d'échec pré-enregistrée : contrôle avec moins de 80 valeurs valides = échec mesuré. Ici les 14 contrôles ont 91 ou 92 valeurs valides : aucun échec prévisible par manque de points.
- Parallélisme : 2 runs maximum en simultané (plafond CPU/RAM de la VM).
- Pilote : `scripts/run_one.py` (adaptation directe du pilote air-quality : même structure, chemins et fichier changés, même extraction des résumés). Design résumable : un run déjà terminé (run_summary.json présent) n'est pas relancé.

## Réserves d'interprétation (gelées avant run)
- Petit n : 92 lignes seulement (91 valides par contrôle numérique), contre 500–569 dans les séries précédentes. Avec w_size 80, les fenêtres du pipeline sont très larges par rapport à n (la fonction de scan plafonne d'ailleurs w_size à n//2) : les seuils et stabilités de cette série sont à lire avec plus de prudence que ceux des séries à grand n, et la comparaison directe des scores avec les séries précédentes n'est pas un classement de qualité.
- Les lignes sont des agences/États, pas une série temporelle : le « contrôle » est un axe de rang le long de la colonne, pas un temps. Aucune lecture causale ou temporelle, même pour les colonnes mensuelles (les mois sont ici des colonnes, pas des lignes).
- `Cumulative Cost` est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels, et un seuil sur Cumulative Cost ne peut pas être lu comme une preuve indépendante d'un seuil mensuel.
- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier (regroupement géographique du fichier), pas un seuil géographique, économique ou administratif.
- La ligne Texas vide est conservée telle quelle (manquante), pas imputée, pas supprimée.
- Aucune conclusion de politique publique, budgétaire ou nutritionnelle ne sera tirée des seuils : ce sont des mesures du pipeline sur ce fichier, pas des seuils d'aide alimentaire.
