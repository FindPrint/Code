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
- Synthèse vérifiée : `RAPPORT.md` (après les runs). PDF + zip +
  publication GitHub selon la règle permanente.
