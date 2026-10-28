# PROTOCOLE GELÉ — Flux dérivés type susceptibility × v3.5.4-H1

**Gel : 28 octobre 2026, avant toute construction et avant tout run.
Aucune modification sans « go » explicite de l'utilisateur.
Question : l'utilisateur, 28 oct. 2026.**

*Frozen protocol — susceptibility-like derived fluxes × v3.5.4-H1.
Frozen 28 Oct 2026, before any build or run.*

## Question

Le pipeline trouve plus de seuils qu'il n'en présente (96–132 pics de
paysage et 5 seuils propres par run, un seul seuil MC présenté) et ne
peut pas dire, seul, si un seuil vient (a) de la construction du flux
(l'outil qui fabrique le flux), (b) de la machinerie du pipeline
(scan/MC), ou (c) d'un vrai seuil physique. Ce lot teste cette
attribution avec des flux construits comme `susceptibility`, depuis
les CSV déjà sauvés, et des nuls.

## Phase 1 (forensique, déjà faite, CSV sauvés uniquement)

`forensics_paysage.py` (28 oct. 2026) sur les 6 runs ising-v354 :
pics forts (rel ≥ 0,90) groupés sur 4 pas de grille contigus autour
de Tc (écart max entre T consécutives 0,0696 = un pas, sauf run
susceptibility : 0,1391) ; UNE seule bande haute par courbe de scan
(susceptibility : une bande + un point isolé à la même T) ; seuils
propres : 4 valeurs de T (2,1174 ×7, 2,1870 ×3, 2,2565 ×14,
2,3261 ×6), toutes à ≤ 0,21 de Tc. **Aucune deuxième masse séparée
dans les données sauvées.** La phase 2 teste si une deuxième masse
apparaît sous des contrôles type-χ, et d'où elle vient.

## Données (aucune nouvelle simulation, aucun T dans la construction)

- Source : `../ising-v354/data/ising_classic_v354.csv` (960 lignes ×
  6 flux, SHA `9027dfd5…`), mêmes lignes, même ordre.
- Le constructeur (`gen_derived.py`) ne lit JAMAIS le fichier
  température (vérifié par grep après construction). Les blocs sont
  définis par la POSITION des lignes (24 blocs de 40 lignes
  consécutives), jamais par des valeurs de T.
- Température : copie de `ising_classic_v354_temperature.csv` dans
  `data/` (SHA vérifié `4863b1de…`), lue APRÈS les runs par le
  harnais uniquement, pour la traduction des seuils (même méthode
  que le lot ising-v354 : médiane sur ±1,5 % autour du rang seuil).
- Le pipeline ne voit que le CSV dérivé + le `flux_mapping`
  (contrôle + 6 flux originaux). Les colonnes dérivées/nulles hors
  mapping ne sont jamais analysées (vérifié dans le code :
  `flux_map` détermine seul `fluxes`).

## Flux dérivés (formules gelées, sans T)

- `expvar_<X>`, X ∈ {energy, magnetization, fliprate, localvar} :
  par bloc de 40 lignes, k = 0..39 :
  Var(X[bloc..bloc+k], ddof=1) ; k = 0 → 0,0. (Construction
  miroir de χ : variance expansive à mémoire, réinitialisée par
  bloc. `flip` exclu : proportionnel à `fliprate`, identique après
  z-score.)
- `expmean_<X>`, X ∈ {energy, magnetization} : par bloc :
  Mean(X[bloc..bloc+k]).
- `rollvar_<X>_40`, X ∈ {magnetization, energy} : variance glissante
  arrière, fenêtre 40, min_periods=1, ddof=1, sur toute la série
  SANS réinitialisation (même idée de second moment, SANS mémoire
  expansive — le témoin de construction) ; première valeur → 0,0.
- Nuls (graine `default_rng(1234)`, permutation de la série entière,
  lien à T détruit, marginales conservées) :
  `null_susceptibility` (permutation de susceptibility),
  `null_expvar_mag` (permutation de expvar_magnetization),
  `null_rollvar_mag` (permutation de rollvar_magnetization_40).
- Fichier : `data/ising_derived.csv`, 960 lignes × 17 colonnes
  (6 originaux + 8 dérivés + 3 nuls), 0 NaN.

## Runs (11)

- Pipeline : v3.5.4-H1 (Q6-A), SHA `b54fcf66…`, mode stable, w80,
  cohen_d, graine 42, HARMONIC_PROB 0,45 (défaut), Theiler 1/φ
  planché (source fixe), `full_triangulation` False. Paramètres
  IDENTIQUES au lot ising-v354.
- Contrôles (11) : les 8 dérivés + les 3 nuls. Analysés (tous les
  runs) : les 6 flux ORIGINAUX (χ incluse comme flux analysé,
  jamais comme contrôle ici). Contrôle exclu des analysés.
- Clés actif/réactif : positionnelles, ordre fixe des originaux
  (2 premiers / 2 suivants), règle identique pour les 11 runs.
- Max 2 runs en parallèle. Harnais durable `run_one_derived.py`
  (mêmes exports + `run_summary.json` + champs `famille`,
  `construction`, `nul`). Pilote `run_lot_derived.sh` (saute un run
  terminé OK, relance les autres de zéro).
- Sorties par run : `runs/<controle>/` (mêmes 11 fichiers que le
  lot ising-v354).

## Règles de lecture (gelées AVANT les runs)

- **R1 — candidat deuxième seuil** : un groupe de pics forts
  (rel ≥ 0,90) dont les températures sont séparées de ≥ 0,20 du
  groupe principal (celui qui contient la T du seuil MC), présent
  dans ≥ 2 runs à contrôles dérivés, ET absent (aucun groupe de
  pics forts à cette T) dans le run nul correspondant.
- **R2 — construction** : candidat présent sous expvar/expmean
  mais absent sous rollvar sur le MÊME flux de base → artefact de
  construction (mémoire expansive).
- **R3 — pipeline** : candidat présent dans un run nul (contrôle
  permuté) à la même T → artefact de la machinerie (seuil sans
  lien à T).
- **R4 — candidat réel** : survit à R1+R2+R3 (plusieurs
  constructions, ≥ 2 contrôles, absent des nuls) ET à T séparée de
  ≥ 0,20 du groupe Tc → candidat deuxième seuil réel, À CONFIRMER
  par L=64 + 2e graine (hors de ce lot — limite nommée).
- **R5 — tout est rapporté** : les 11 runs, y compris échecs et
  valeurs éloignées de Tc ; aucun paramètre touché après les
  résultats ; aucun run écarté pour s'éloigner de Tc.

## Portes (données dérivées, avant les runs)

- D1 : 960 lignes, 17 colonnes, 0 NaN.
- D2 : les 6 colonnes originales sont bit-identiques à la source.
- D3 : expvar/expmean valent 0,0 / X[bloc] au premier rang de
  chaque bloc (réinitialisation vérifiée) ; rollvar première
  valeur 0,0.
- D4 : chaque nul est une permutation exacte de sa colonne source
  (valeurs triées identiques).
- D5 : le constructeur ne lit pas temperature.csv (grep) ; la copie
  température a le SHA attendu.

## Limites (gelées)

Une seule graine (42), une seule taille (L=32) ; les flux dérivés
héritent le bruit de la graine 42 ; rollvar traverse les frontières
de blocs par construction ; expvar/expmean utilisent la structure
en blocs (position des lignes, pas de valeurs de T) ; pas de L=64
dans ce lot ; lecture descriptive, aucune règle succès/échec
importée. La comparaison à Tc reste un jugement post-hoc étiqueté,
sans retour dans les paramètres (règle du 28 oct. 2026).
