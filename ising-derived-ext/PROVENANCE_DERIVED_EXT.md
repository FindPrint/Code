# PROVENANCE — Extension dérivés (factoriel complet + rollmean + nuls)

**Règle permanente (27 oct. 2026) : provenance toujours nommée.**
Extension du lot `ising-derived` (PROTOCOLE_DERIVED.md, 11 runs) :
protocole gelé `PROTOCOLE_DERIVED_EXT.md` (28 oct. 2026, avant
construction et runs).

## Données

- **Nature des lignes : SIMULÉES, DÉRIVÉES, puis ÉTENDUES.** Les 17
  premières colonnes sont les colonnes du lot 1, préservées octet pour
  octet (vérifié porte E2). Les 12 colonnes ajoutées sont des
  transformations déterministes de ces CSV, sans aucune valeur
  nouvelle, sans température, sans mesure.
- **Source :** `data/ising_derived.csv`, SHA-256
  `10563d4d1405d09dac4eb468c1e44b59a27a028036ba1f6f729389fc55809c7b`
  (960 lignes × 17 colonnes, elle-même dérivée de
  `../ising-v354/data/ising_classic_v354.csv`, SHA-256 `9027dfd5…`).
- **Constructeur :** `gen_derived_ext.py`, écrit le 28 oct. 2026 par
  TagPrint (Muse) à la demande de Zackary Drasse-Ménard, SHA-256
  `6170c25c78a961be32f7a214c28b4a2521d910f443407d2292962f12c5abbd0b`.
  Le constructeur ne lit QUE le fichier source (une seule lecture CSV ;
  aucune référence au fichier température — porte E6).
- **Fichier :** `data/ising_derived_ext.csv`, SHA-256
  `bae505d4c5e5e0f4faff2571515b872c67eb01545ebb367ff1203735cded34b4`
  (960 lignes × 29 colonnes, 0 NaN).
- **Température :** copie de `ising_classic_v354_temperature.csv`,
  SHA-256 `4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4`,
  lue APRÈS les runs par le harnais uniquement (traduction des seuils).
- **Comment chaque valeur nouvelle a été produite :** voir
  `PROTOCOLE_DERIVED_EXT.md` (expmean : moyenne expansive par bloc de
  40, reset ; rollvar : variance glissante fenêtre 40, ddof=1, sans
  reset, première valeur → 0,0 ; rollmean : moyenne glissante fenêtre
  40, sans reset ; nuls : permutation `default_rng(1234)` de la série
  entière, mêmes indices que le lot 1).
- **Exclusions :** `flip` (= 1024 × `fliprate` exactement, rangs
  identiques), `susceptibility` comme base (Spearman vs T +0,3860,
  non monotone), racines des variances (rangs identiques, Spearman 1,0).
- **Vérité terrain :** Tc d'Onsager = 2,2692, jugement post-hoc
  étiqueté uniquement, sans retour dans les paramètres.
- **Ce qui manque :** pas de nouvelle simulation ; une seule graine ;
  une seule taille L ; pas de L=64 dans ce lot ; pas d'autres fenêtres.

## Code pipeline

- `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1, Q6-A), SHA-256
  `b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d`
  (fichier dans `../pipeline-v35/`, intact, non modifié).
- Harnais : `run_one_derived_ext.py` (copie de `run_one_derived.py`,
  seuls les chemins changent : dataset étendu, sorties `runs_ext/`).

## Livrables et publication (28 oct. 2026)

- Rapport : `RAPPORT_DERIVED_EXT.md` ; synthèse : `synthese_derived_ext.json` ;
  dossier diagnostique : `diagnostic_runs_ext.json`.
- PDF 16 pages : `Ising_derived_EXT_v35H1_Resultats_complets.pdf`,
  SHA-256 `98b142a0d9ce1ffc44a9ffb85ffcc69d360203a464278cea39b6bd49a3136cad`
  (6,7 Mo).
- Zip : `ising_derived_ext_resultats.zip`, 172 fichiers,
  SHA-256 `6c7cde6b70eca9dcecd88ffbc5a695050362d5019f5fd7896fd6935c96f6d128`
  (12,5 Mo).
- Dépôt privé FindPrint/Code, branche main, dossier `ising-derived-ext/` :
  texte 15 commits snapshot (tête `c5e563c0…`, registre sync vérifié) ;
  figures 26 PNG préfixés, commit web `3e72b3f…` (dossier `figures/`,
  vérifié par relecture) ; PDF + zip, commit web `8b85980a…` (vérifié par
  relecture, sans Release).

- 12 runs (8 contrôles dérivés + 4 nuls), mode stable, w80,
  cohen_d, graine 42, HARMONIC_PROB 0,45, max 2 en parallèle.
  Journaux : `runs_ext/<controle>/run.log`, journal maître
  `run_lot_ext.log`.
- Synthèse + attribution (règles R1–R5 gelées, 7 nuls poolés) :
  `RAPPORT_DERIVED_EXT.md` (après les runs). PDF + zip + publication
  GitHub selon la règle permanente.
