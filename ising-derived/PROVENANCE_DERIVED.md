# PROVENANCE — Flux dérivés type susceptibility × v3.5.4-H1

**Règle permanente (27 oct. 2026) : provenance toujours nommée.**

## Données

- **Nature des lignes : SIMULÉES puis DÉRIVÉES.** Les 6 flux originaux
  sont les 960 snapshots simulés du lot ising-v354 (L=32, graine 42).
  Les 11 colonnes ajoutées sont des transformations déterministes de
  ces CSV (formules gelées, `PROTOCOLE_DERIVED.md`), sans aucune
  valeur nouvelle, sans température, sans mesure.
- **Source :** `../ising-v354/data/ising_classic_v354.csv`, SHA-256
  `9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d`.
- **Constructeur :** `gen_derived.py`, écrit le 28 oct. 2026 par
  TagPrint (Muse) à la demande de Zackary Drasse-Ménard, SHA-256
  `f06aa42bfe5125dcbf0c2b2383f9d0ec8e408c178db8033491e120d02cb5c5aa`.
  Le constructeur ne lit jamais le fichier température (une seule
  lecture CSV : la source ; copie d'octets + SHA pour la température).
- **Fichier :** `data/ising_derived.csv`, SHA-256
  `10563d4d1405d09dac4eb468c1e44b59a27a028036ba1f6f729389fc55809c7b`
  (960 lignes × 17 colonnes, 0 NaN, 6 originaux bit-identiques).
- **Température :** copie de `ising_classic_v354_temperature.csv`,
  SHA-256 `4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4`,
  lue APRÈS les runs par le harnais uniquement.
- **Comment chaque valeur dérivée a été produite :** voir
  `PROTOCOLE_DERIVED.md` (expvar/expmean : statistique expansive par
  bloc de 40 lignes, réinitialisée ; rollvar : variance glissante
  fenêtre 40 sans réinitialisation ; nuls : permutation
  `default_rng(1234)` de la série entière).
- **Vérité terrain :** Tc d'Onsager = 2,2692, jugement post-hoc
  étiqueté uniquement (règle du 28 oct. 2026), sans retour dans les
  paramètres.
- **Ce qui manque :** pas de nouvelle simulation ; une seule graine ;
  une seule taille L ; pas de L=64 dans ce lot.

## Code pipeline

- `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1, Q6-A), SHA-256
  `b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d`
  (fichier dans `../pipeline-v35/`, intact, non modifié).
- Harnais : `run_one_derived.py` (adapté de
  `../ising-v354/run_one_ising.py` : mêmes exports, analysés fixés
  aux 6 originaux, SHA du dataset calculé à l'exécution).

## Exécutions

- Protocole gelé avant construction et runs :
  `PROTOCOLE_DERIVED.md` (28 oct. 2026).
- 11 runs (8 contrôles dérivés + 3 nuls), mode stable, w80,
  cohen_d, graine 42, HARMONIC_PROB 0,45, max 2 en parallèle.
  Journaux : `runs/<controle>/run.log`, journal maître
  `run_lot_derived.log`.
- Synthèse + attribution (règles R1–R5 gelées) : `RAPPORT_DERIVED.md`
  (après les runs). PDF + zip + publication GitHub selon la règle
  permanente.

## Livrables vérifiés (28 oct. 2026)

- PDF `Ising_derived_v35H1_Resultats_complets.pdf` — 15 pages A4,
  6 429 409 octets, SHA-256
  `0dcbdd685017b1f530f5999712b6657d06171ce019a0ca2f9a7a9c8f66367cde`
  (construit par `build_pdf_zip_derived.py` depuis la synthèse vérifiée).
- Zip `ising_derived_resultats.zip` — 158 fichiers, 11,5 Mo, SHA-256
  `a7e49e707c172ec03b6e68d9547e166466f3b8fa183a366f0a2612c9bc989865`
  (arbre complet hors PDF/zip/__pycache__, testzip OK).
- Publication : dépôt privé FindPrint/Code, branche main, dossier
  `ising-derived/` — texte par snapshot (14 commits + addendum),
  binaires par téléversement web
  (PDF + zip + 24 figures aux noms préfixés par contrôle, dossier
  `ising-derived/figures/`).
