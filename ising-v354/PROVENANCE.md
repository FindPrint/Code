# PROVENANCE — Ising classique 2D × v3.5.4-H1

**Règle permanente (27 oct. 2026) : provenance toujours nommée, avec le
maximum de sources et d'informations.**

## Données

- **Nature des lignes : SIMULÉES.** 960 snapshots d'une simulation
  Monte Carlo Metropolis (Ising 2D), pas des spécimens ni des mesures.
  Aucune donnée réelle, aucune mesure instrumentale.
- **Générateur :** `gen_ising_classic_v354.py`, écrit le 28 oct. 2026
  par TagPrint (Muse) à la demande de Zackary Drasse-Ménard, par
  adaptation de `workspace/gen_ising_proxy.py` (mêmes fonctions
  `sweep`, `energy_per_spin`, `local_variance`, mêmes L, températures,
  graine, EQ/GAP — code éprouvé, vérifié physiquement en octobre 2026).
  SHA-256 du générateur :
  `24069e4e5e0d5f323d79796a9dd6ceed9d307f53bcb3db2fd7764647a9f4ba21`
  (fichier non modifié après la génération).
  SHA-256 du protocole gelé :
  `43092635dff9bed6933ed7e8d8adb0328ead5b3a180a3d6ec038683ce24b353d`.
- **Paramètres :** L = 32, J = 1, limites périodiques, checkerboard
  Metropolis, graine `default_rng(42)`, T = linspace(1.7, 3.3, 24),
  1 500 sweeps d'équilibration, 40 snapshots par T, GAP 50 sweeps.
- **Fichiers :**
  - `data/ising_classic_v354.csv` — SHA-256
    `9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d`
    (960 lignes × 6 colonnes, 0 NaN).
  - `data/ising_classic_v354_temperature.csv` — SHA-256
    `4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4`
    (960 lignes, 1 colonne `temperature`, même ordre).
- **Comment chaque valeur a été produite :** voir §3 du `PROTOCOLE.md`
  (définitions gelées des 6 flux). `susceptibility` utilise la m
  signée interne au générateur (fenêtre expansive intra-bloc) ;
  `magnetization` est |m| ; `flip`/`fliprate` sont exactement
  proportionnels (redondance voulue).
- **Vérité terrain :** Tc d'Onsager = 2,2692 (réseau carré infini,
  J = 1). Réseau fini L = 32 : transition arrondie, pic de χ décalé
  (mesuré : 2,3261, écart 0,057) — attendu, pas une erreur.
- **Ce qui manque :** pas de mesures réelles ; pas de champ magnétique ;
  une seule taille L (pas d'étude en taille finie) ; pas de dynamique
  hors équilibre ; pas de réplique indépendante (une seule graine).

## Code pipeline

- `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1, Q6-A), SHA-256
  `b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d`,
  dérivé de v3.5.3-H1 (SHA `f2580464…`, intact), lui-même dérivé de
  v3.4-H3 (SHA `81092eb6…`, intact). Conception Q6-A :
  `CONCEPTION_Q6_v354.md` (amendement du 28 oct. 2026).
- Harnais : `run_one_ising.py` (adapté de `pilote/run_one_v35.py`,
  mêmes exports et mêmes analyses post-run + traduction température).

## Exécutions

- Protocole gelé avant génération et runs : `PROTOCOLE.md` (28 oct. 2026).
- 6 runs en rotation (contrôle exclu des flux), mode stable, w80,
  cohen_d, graine 42, HARMONIC_PROB 0,45, max 2 en parallèle.
  Journaux : `runs/<controle>/run.log`, journal maître `run_lot.log`.
- Synthèse vérifiée : `RAPPORT.md` (après les runs, 28 oct. 2026),
  produite par `synthese.py` (traduction température recalculée
  indépendamment, exclusion du contrôle vérifiée, identité
  flip/fliprate vérifiée) et relue contre les sorties brutes.

## Publication (28 oct. 2026)

- **Dépôt :** FindPrint/Code (privé), branche `main`, dossier
  `ising-v354/`. Entrée ajoutée en tête de `PROJECTS.md`.
- **PDF :** `Ising_v354_v35H1_Resultats_complets.pdf`, SHA-256
  `6bf5f07297e4e35e7d214b5bb4c62b6d9bbee3674811c24c8872dc12a81f7413`,
  2,8 Mo (rapport + 2 figures de synthèse + 12 figures du pipeline).
- **Zip :** `ising_v354_resultats.zip`, SHA-256
  `3b1ef0d37dec542019562741ec3dd93e4ed49faa33ab88666f1513e243e50238`,
  95 fichiers (arbre complet : protocole, provenance, rapport,
  données, générateur, code pipeline + conception Q6, harnais,
  synthèse, sorties des 6 runs ; hors PDF, hors figures préfixées
  temporaires).
- **Texte (7 commits snapshot, 82 fichiers) :** tête avant
  `b6b1ce30…` ; docs `902584b1…`, fliprate `e7c54d52…`, flip
  `00927394…`, energy `7bb7c40f…`, magnetization `0593608a…`,
  localvar `6d4681fe…`, susceptibility `0d1397ce…`. Incident :
  une première tentative à 10,05 Mo a été rejetée (HTTP 413) —
  les lots ont été refaits à ≤ 3,3 Mo. Vérifié par relecture
  (`get_file_contents` : RAPPORT.md, run_summary.json susceptibility).
- **Binaires (4 commits via l'interface web GitHub, vérifiés par
  listage) :** dossier figures `5ddf0b17…`, PDF + zip `da91051d…`,
  figures `0402ccf…`, restauration préfixée `1aa52f17…`.
  Incident : le premier téléversement des figures a écrasé les
  fichiers de même nom (6 `threshold_scan.png` et 6
  `noise_diagnostic.png` partageant les mêmes chemins) — seule la
  paire susceptibility subsistait. Les 12 figures ont été
  restaurées sous noms préfixés (`<contrôle>_threshold_scan.png`,
  `<contrôle>_noise_diagnostic.png`), vérifiées une à une dans le
  listage (17 fichiers dans `figures/`, dont les 2 fichiers sans
  préfixe laissés en place — doublons de la paire susceptibility
  préfixée). Les figures restent aussi dans le zip.
- Cet addendum a été poussé au dépôt dans un commit snapshot séparé
  le 28 oct. 2026, après les 11 commits ci-dessus.
