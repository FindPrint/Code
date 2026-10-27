# Provenance des données — Mushroom Classification × pipeline Tlog v3.4-H3

Règle permanente (27 oct. 2026, demande de l'utilisateur) : la
provenance est nommée partout, avec le maximum de sources et
d'informations, dans toutes les exécutions, demandes et publications,
anciennes et nouvelles.

## Source d'origine

- **Ouvrage :** *The Audubon Society Field Guide to North American
  Mushrooms* (1981), G. H. Lincoff (prés.), New York : Alfred A.
  Knopf, pages 500–525.
- **Donateur :** Jeff Schlimmer (Jeffrey Curtis Schlimmer),
  27 avril 1987. Thèse : *Concept acquisition through
  representational adjustment* (1987).
- **Dépôt :** UCI Machine Learning Repository, dataset « Mushroom »
  (n° 73), https://archive.ics.uci.edu/dataset/73/mushroom
- **Nature des lignes :** descriptions d'échantillons **hypothétiques**
  correspondant à **23 espèces** de champignons à lamelles des
  familles *Agaricus* et *Lepiota*. Ce ne sont PAS 8 124 spécimens
  mesurés sur le terrain : ce sont des combinaisons de traits
  possibles, tirées des descriptions du guide, espèce par espèce.
- **Classe :** chaque espèce est identifiée comme définitivement
  comestible, définitivement vénéneuse, ou de comestibilité inconnue
  et non recommandée ; cette dernière classe a été fusionnée avec
  la classe vénéneuse. Le guide déclare explicitement qu'il n'existe
  pas de règle simple pour déterminer la comestibilité d'un
  champignon. Aucune règle comestible/vénéneux ne doit donc être
  tirée de ce dataset.

## Miroir Kaggle utilisé pour ce lot

- Dataset Kaggle : `uciml/mushroom-classification`,
  https://www.kaggle.com/datasets/uciml/mushroom-classification
- Zip `mushroom-classification.zip` : 35 057 octets, SHA-256
  `4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081`
- Contenu : un seul CSV `mushrooms.csv` (dans l'archive, 20 sept.
  2019), 374 003 octets, SHA-256
  `f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c`
- Inventaire vérifié : 8 124 lignes × 23 colonnes, 0 doublon exact.
  Fichier de travail `data/mushrooms_pipeline.csv` : SHA-256
  `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`.
  Original préservé dans `data/raw/`.

## Comment les valeurs ont été produites

- **Couleurs et formes :** mots choisis à l'œil par l'auteur du guide
  (ex. cap-color : brown, buff, cinnamon, gray, green, pink, purple,
  red, white, yellow), codés par une lettre. Aucune mesure
  instrumentale (pas de spectrophotomètre, pas de RVB/Lab, pas de
  dosage de pigment). Les codes sont des étiquettes nominales.
- **Odeur :** 9 mots de nez humain (almond, anise, creosote, fishy,
  foul, musty, none, pungent, spicy). Aucune mesure chimique (pas de
  GC-MS, pas de dosage de composés volatils).
- **Valeurs manquantes :** seul marqueur `?`, dans `stalk-root`,
  2 480 lignes (30,5 %). En contrôle, ces lignes sont écartées
  (5 644 valides) ; en flux, NaN remplacé par la moyenne du flux.
- **veil-type :** constant `p` sur les 8 124 lignes dans ce fichier
  (le guide prévoit aussi `u` universel, absent du fichier).
- **Absents du dataset :** nom d'espèce, mesures (taille, poids),
  chimie (toxines, composés volatils), microscopie (taille des
  spores — seule la couleur de l'empreinte), ADN, date, lieu précis,
  saison, flux physiques (température, humidité, croissance) et
  biologiques (mycélium, substrat).

## Encodage appliqué dans ce lot

Chaque lettre → entier par ordre de première apparition dans la
colonne (`data/mapping_encodage.json`). `?` = vrai NaN, pas une
catégorie. Les seuils sont des coupes de rang sur cet ordre
arbitraire (plateaux de rang), jamais des grandeurs.
