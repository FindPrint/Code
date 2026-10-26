# Protocole gelé — Earthquake / Tsunami (Kaggle ahmeduzaki) x pipeline v3.3 FIXED
Gelé le 2026-10-25 ~13h45 HAE, AVANT tout run de cette série.

## Ce qui change par rapport à la série précédente (25 oct., matin)
- SEUL le pipeline change : `pipeline_autonome_v3_3_fixed.py` (v3.3, Monte Carlo
  classique) à la place de `pipeline_autonome_v3_3_harmonic_v1_1_omg2.py` (v3.3-H1,
  Monte Carlo harmonique guidé P = 0,45). Tout le reste est identique, pour que
  la comparaison fixed vs harmonic soit propre.
- Données identiques : `data/earthquake_data_tsunami.csv` (copie du fichier déjà
  téléchargé le matin), 782 lignes, 13 colonnes, toutes numériques, 0 manquant.

## Ce qui ne change pas (« même protocole »)
- 13 runs, un par colonne en contrôle.
- Mode stable, w_size 80, cohen_d, graine 42 (défauts du fichier fixed, identiques
  à ceux du fichier harmonic).
- Règle Porte D : la colonne de contrôle est EXCLUE des flux analysés.
  Chaque run analyse donc les 12 autres colonnes comme flux — y compris les
  flux informationnels, pour ne pas changer le protocole en cours de route.
- Aucun seuil attendu pré-enregistré : lecture descriptive seulement.

## Séparation des flux informationnels (demande du 25 oct., après-midi)
- Définition retenue, écrite avant les runs : un flux est « informationnel /
  contexte » quand il ne mesure pas le séisme lui-même mais son contexte ou
  son étiquette : **Year, Month (temps), latitude, longitude (lieu),
  tsunami (étiquette 0/1)**.
- Les 8 autres colonnes (magnitude, cdi, mmi, sig, nst, dmin, gap, depth)
  restent dans le groupe principal, comme mesures / indices de l'événement.
- Conséquence pratique, sans effet sur les runs : la séparation se fait à la
  SYNTHÈSE, pas pendant les runs. Deux CSV à part seront livrés :
  (1) `flux_informationnels_donnees.csv` — les 5 colonnes brutes, 782 lignes ;
  (2) `seuils_flux_informationnels.csv` — les seuils propres de ces 5 colonnes
  en tant que flux, dans les 12 runs où chacune est flux (60 lignes).
  Le PDF complet contiendra en plus une section dédiée à ces flux.
- Si l'utilisateur voulait une autre liste (par exemple inclure nst, dmin, gap,
  sig, cdi, mmi comme dérivés / métadonnées), la séparation peut être refaite
  sans relancer les runs, puisque tous les flux sont présents dans chaque run.
- Réserves déjà connues, inchangées : tsunami binaire (plateaux 30,63 % /
  80,63 %), cdi / mmi / Month discrets à paliers de rang, dmin = 0 à 51,8 %,
  nst = 0 à 46,7 %, latitude / longitude = ordre géographique, pas progression.
