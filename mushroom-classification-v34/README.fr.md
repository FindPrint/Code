# Classification des champignons × pipeline Tlog v3.4-H3

**Version française — [English version](README.md)**

Analyse descriptive de seuils de régime sur le dataset Kaggle Mushroom
Classification, avec le pipeline autonome Tlog v3.4-H3, une colonne à la
fois en colonne de contrôle. Ce dépôt est la trace, la mémoire et la
preuve de cette exécution : code, données, protocole gelé, scripts,
vérifications, et — au fur et à mesure — résultats et figures.

> **État (26 oct. 2026, ~16h35 HAE) :** lot v3.4 reparti de zéro.
> Première paire en cours : `class` + `cap-shape`. 0/23 runs terminés
> dans ce lot. Les résultats seront poussés ici à chaque point d'étape
> et à la fin. Le lot v3.3 a été arrêté avant tout fichier de sortie
> (voir `docs/PROTOCOLE.md`) ; le pilote v3.3 `class` est conservé à
> part pour comparaison seulement, et n'est PAS compté dans ce lot.

## Ce que c'est — et ce que ce n'est pas

- **C'est :** une mesure descriptive. Pour chaque contrôle, le pipeline
  cherche un seuil critique (Monte Carlo guidé harmonique), rapporte
  la stabilité (bootstrap), les seuils par flux, et les dérivées F1/F2
  avant ET après le seuil.
- **Ce n'est pas :** une règle pour décider si un champignon est
  comestible. Les codes encodés sont des étiquettes nominales, pas des
  grandeurs ; un seuil est une coupure de rang sur un ordre arbitraire
  (première apparition), à lire comme plateaux de rang. Aucune lecture
  temporelle ou causale (aucune colonne de temps).
- **Aucune vérité terrain affirmée :** données réelles, aucun seuil
  attendu n'est affirmé.

## Démarrage rapide (test en quelques minutes)

```bash
python3 -m pip install -r requirements.txt
# Démo rapide : 1 contrôle, mode fast, 10 itérations Monte Carlo
python3 scripts/demo.py
# Lot complet (23 contrôles, mode stable, ~heures) : voir scripts/batch_v34.sh
bash scripts/batch_v34.sh
# Un contrôle, ex. class, mode stable :
python3 scripts/run_one_v34.py class results/ctrl_class
```

`scripts/demo.py` tourne sur les données fournies en mode fast ; c'est
le test rapide pour les pairs. Le lot complet utilise le mode stable,
graine 42, Cohen d, fenêtre initiale 80, probabilité harmonique 0,45
(voir `docs/PROTOCOLE.md`).

## Contenu du dépôt

```
pipeline/   Tlog_v3_4_harmonic_v3.py      (français, référence)
            Tlog_v3_4_harmonic_v3_en.py   (anglais, logique identique)
data/       mushrooms_pipeline.csv        (fichier de travail encodé, 8124x23)
            mapping_encodage.json         (lettre -> entier, première apparition)
            raw/mushrooms.csv             (CSV Kaggle original)
docs/       PROTOCOL.md / PROTOCOLE.md    (protocole gelé, EN/FR)
            METHODOLOGY.md / METHODOLOGIE.md
            VERIFICATION.md               (vérifications scan + repli + F1/F2)
            TRACEABILITY.md               (règle de traçabilité systématique)
scripts/    run_one_v34.py, batch_v34.sh, synthese.py, demo.py
results/    sorties par contrôle (ajoutées au fur et à mesure du lot)
```

## Source des données

- Dataset Kaggle `uciml/mushroom-classification` :
  https://www.kaggle.com/datasets/uciml/mushroom-classification
- Fichier téléchargé : `mushroom-classification.zip` (35 057 octets),
  SHA-256 `4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081`
- Le zip contient UN SEUL CSV (`mushrooms.csv`, 374 003 octets,
  SHA-256 `f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c`),
  donc la « fusion » est triviale : aucun autre fichier à joindre,
  aucune ligne ajoutée ni retirée.
- Fichier de travail `mushrooms_pipeline.csv`, SHA-256
  `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`.
- 8 124 lignes × 23 colonnes catégorielles à une lettre. `class` :
  e=4 208, p=3 916. `stalk-root` : `?` sur 2 480 lignes (30,5 %),
  encodé comme vrai manquant (NaN). `veil-type` : constante (`p` partout).

## Pipeline v3.4-H3 — changements par rapport à v3.3-H1

1. **Scan rapide, résultats identiques.** Le scan v3.3 concaténait
   toutes les fenêtres glissantes (~n_windows × w_size valeurs par flux
   et par candidat) alors que `separation_score()` ne gardait ensuite
   que 1 000 tirages (graine 0). Le scan rapide retrouve chaque valeur
   tirée par arithmétique d'indices (fenêtre = indice // w_size,
   décalage = indice % w_size ; cas NaN via tableau des valeurs valides
   et cumuls par fenêtre) et reproduit exactement le tirage, y compris
   la séquence rng(0) partagée par les deux groupes. Vérifié : pilote
   traité, seuil 52,75 %, écart maximal 0,0 sur 801 candidats, 5,8 s
   contre ~48 s par scan ; `stalk-root` brut seul, écart 0,0 après
   correction d'un début de fenêtre avec NaN (voir
   `docs/VERIFICATION.md`).
2. **Repli Monte Carlo journalisé.** Quand le Monte Carlo ne produisait
   aucune configuration valide, le seuil par défaut était déjà utilisé,
   mais en silence à plusieurs endroits (cas brut, rapport texte,
   itérations ratées non comptées, valeur d'urgence 52,5 % du diagnostic
   bruit). Désormais chaque repli est imprimé (stdout + stderr),
   journalisé, et enregistré dans les métadonnées (`threshold_source`,
   `threshold_warnings`) et dans le rapport texte. Un seuil de repli ne
   peut plus passer pour un seuil Monte Carlo.
3. **F1/F2 avant ET après seuil.** `transition_analysis` ne calculait
   que l'après-seuil. La v3.4 ajoute, avec la même méthode (polyfit
   degré 2 sur Progress centrée), l'avant-seuil
   (`first_derivative_pre` / `second_derivative_pre`), plus les écarts
   post-pré et `sign_change`. Les champs post sont inchangés pour
   compatibilité v3.3.
4. **Export JSON robuste** (tuples, ensembles, tableaux numpy sanitizés).

Empreinte du fichier pipeline (français, corrigé le 26 oct.) :
`81092eb61d612d0dea50f9fca6bfa12f6dbd2388c4e52a24ab064d09e61dc7f8`

## Environnement

Python 3.12.3, numpy 1.26.4, pandas 2.1.4, scipy 1.11.4,
matplotlib 3.6.3 (plus seaborn). Voir `requirements.txt`.
Machine du lot : conteneur 2 vCPU, 7,7 Go RAM, pas de swap — d'où le
scan rapide et le design résumable (un run avec `run_summary.json`
est sauté ; un run interrompu est jeté et relancé de zéro, jamais compté).

## Licence — en attente de la décision de l'auteur

Aucun fichier de licence n'est inclus pour l'instant, exprès : l'auteur
n'en a pas encore choisi une. En attendant, ce dépôt privé est partagé
pour lecture, test et reproduction par les pairs invités seulement —
pas de redistribution, pas d'usage commercial, pas de miroir public
sans permission écrite de l'auteur. Voir `LICENSE-NOTE.md`.

## Traçabilité (règle systématique)

Depuis le 26 oct. 2026, ce modèle de traçabilité s'applique à TOUS les
codes, exécutions et projets faits avec Muse, pas seulement à ce lot —
voir `docs/TRACEABILITY.md` : protocole gelé avant les runs, empreintes
du code et des données, sorties par run, synthèse, PDF, et mises à jour
du dépôt aux points d'étape et à la fin, comme mémoire et preuve.
