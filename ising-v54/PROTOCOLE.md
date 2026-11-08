# PROTOCOLE GELÉ — Test v5.4.0 (UNIVERSAL_LOG v5.4.0)

Date de gel : 7 novembre 2026, 14h15 HNE. Gelé avant tout run.
Demande : Zackary, 7 nov. 2026 14h14 HNE — « Pouvez-vous tester ce pipeline : »
(fichier joint `UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py`).

## 1. Code testé (original jamais modifié)

- Fichier : `workspace/user/files/UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py`
- SHA256 : `c1115e1c4803bc56d330e37e1adb7a6697ea5393c9a42678111dd76162fb05be`
- Taille : 503 675 octets, 10 675 lignes. Compilation : OK (`py_compile`).
- `VERSION = "v5.4"`, `VERSION_MASTER = "v5.4-CibleFixeNonSilencieuse"`.
- L'en-tête du fichier dit encore « UNIVERSAL_LOG v5.3 » (titre) : étiquetage
  incohérent, comme v4.2.5 avant. Le `VERSION` fait foi.
- Original intact : aucun run ne touche ce fichier ; les lanceurs le lisent
  seulement. Aucune copie modifiée du code (pas de variante workers : la
  formule MC reste `min(cpu_count, n_iterations, ...)` comme en v4.4.2,
  donc 4 workers effectifs dans cette VM — leçon w6 du 2 nov. toujours valable).

## 2. Audit statique (7 nov. 2026, avant runs)

- Cécité du chemin d'analyse : 11 occurrences de « temperature » dans le
  fichier, toutes hors chemin d'analyse — docstring FSS (ligne 8746),
  `param_name = "Temperature"` dans `finite_size_scaling_ising` (8766),
  générateur d'exemple `generate_example_ising_csv` (10378-10482) et sa ligne
  d'usage en exemple (10375). Aucune lecture d'une colonne Temperature dans
  `run_pipeline`, le scan ou la cascade.
- `finite_size_scaling_ising` : aucun appelant dans le chemin principal
  (démo synthétique, étiquetée comme telle dans sa docstring : logistique
  générée puis détectée, valide le détecteur de cascade, pas la physique).
  Contient Tc Onsager 2,269185 en dur, mais n'est pas appelée par le pipeline.
- `generate_example_ising_csv` : appelée seulement par le CLI
  `--generate-example-ising` (ligne 10481). Ne modifie ni le cœur ni le
  comportement par défaut.
- Couche CSD (v4.4.2) présente : 222 occurrences, `csd_consensus` calculé
  après le seuil dans le diagnostic de bruit.
- Pas de fonction `decompress_energy_flux`. Pas de seuils de repli
  [20, 35, 50, 65, 80].
- Q5 : l'en-tête dit toujours « Reporté, inchangé dans v4.2.1 (demande
  utilisateur) : Q5, FSS Ising… » — aucune affirmation d'acceptation.
- CLI compatible avec les lanceurs v4.4.2, plus `--target-mode
  {fixed,per_control}`, `--generate-example-ising`,
  `--example-ising-output`, `--example-ising-L`.
- `_MODE_TO_PIPE` = identité pour les 6 modes : full est un vrai mode.
- Changements v5.4 annoncés (en-tête, items 19-22) :
  (19) cible fixe par défaut en multi/all, jamais silencieuse (politique
  `fixed`, diagonale signalée par bloc `[CIBLE-FIXE-DIAGONALE]`) ;
  (20) avertissement contrôle non monotone, générique
  (`[AVERTISSEMENT-CONTROLE-NON-MONOTONE]`, `metadata.control_monotonicity`) ;
  (21) chaque seuil de cascade accompagné de sa valeur brute du contrôle
  (`cascade.thresholds_in_control_units`, `ambiguous=True` si non monotone) ;
  (22) exemple Ising réel + FSS étiquetée synthétique.
- Changements de défauts à noter :
  - `HARMONIC_VALIDATION_ENABLED` : False en v4.4.2 → **True en v5.4.0**,
    alors que la docstring d'en-tête dit encore « défaut False ».
    Les lanceurs passent `--harmonic-validation` / `--no-harmonic-validation`
    explicitement à chaque run, donc le lot reste comparable ; un run sans
    drapeau validerait désormais par défaut.
  - `DEFAULT_CONTROL_COLUMN` : 'Energy_Diff' (v4.x) → **'Time'**.
    Sans effet sur ce lot : chaque run passe `--control` explicitement.
- Diff vs v4.4.2 : 2 075 lignes (1 858 ajoutées, 217 retirées).

## 3. Périmètre (miroir exact du lot v4.4.2, pour comparabilité)

- Données synthétiques : `workspace/ising-v425-all-options/data/`
  (synth.csv, synth_nan.csv, synth_const.csv, synth_2000.csv,
  synth_short.csv ; mêmes fichiers que v4.2.9/v4.4.2).
- Données Ising : `workspace/ising-v354/data/ising_classic_v354.csv`
  (SHA `9027dfd5…`, L=32, T = linspace(1.7, 3.3, 24), 40 snapshots/T,
  graine 42). Température dans un fichier SÉPARÉ, jamais lue par le pipeline.
  Traduction en T post-hoc dans le harnais, sans retour dans les paramètres.
- Graine 42 partout sauf D_seed7 (graine 7).
- Timeouts : synth 1 200 s/run, Ising 21 600 s (6 h)/run — mêmes que v4.4.2.
- Phase 1 — synthétique : 31 runs (A_single 6 modes × on/off, C_multi/C_all,
  D_nan, D_const ×4, D_missing_control, D_target_eq_control, D_no_control,
  D_seed7_horizon5, D_domain_physics, D_2000, D_short, D_missing_file).
  Les runs C_multi/C_all (sans --target) exercent la nouvelle politique
  cible-fixe ; D_target_eq_control exerce le cas diagonal.
- Phase 2 — Ising : 6 modes (fast, full, predict, analyze, stable, robust)
  × 6 contrôles (fliprate, flip, energy, magnetization, localvar,
  susceptibility) = 36 runs, `--no-harmonic-validation`, `--control <ctrl>`.
- Total : 67 runs. Marqueur de fin : ligne « V54 DONE » dans `ising/run.log`.

## 4. Lanceurs (résumables : SKIP si master_results.json valide)

- `run_synth54.sh`, `run_ising54.sh`, maître `run_v54.sh`.
- Vérifié par diff vs v4.4.2 : seuls le chemin du code et le dossier de base
  changent. Syntaxe `bash -n` OK.
- Lancement durable depuis le fil principal uniquement (`nohup` + `disown`).
  La surveillance ne relance jamais.

## 5. Surveillance

- Cron `ising-v54-watch` (15 min, modèle `ising-v44-watch`) : signale sans
  relancer, message seulement si vrai neuf, s'auto-supprime à « V54 DONE ».
- État : `~/workspace/goals/ising-pipeline-v4-evolution/hidden_files/ising-v54-watch-state.json`.
- Le lot v4.4.2 reste figé à 37/67, surveillance `ising-v44-watch` inchangée.

## 6. AMENDEMENT — 7 nov. 2026, 14h50 (avant toute synthèse, lot reparti de zéro)

Cause : le défaut d'en-tête `CONTROL_MODE` a changé — `"single"` en v4.4.2
(ligne 188) → **`"all"` en v5.4.0 (ligne 268)**. Le CLI ne retient
`--control` en single que si `--control-mode` est passé explicitement ;
sans lui, il retombe sur le défaut d'en-tête. Les lanceurs initiaux ne le
passaient pas : les 2 premiers runs (A_single_fast_off rc=0 234 s,
B_single_fast_on rc=0 235 s) ont donc tourné en mode **all** — boucle sur
les 4 colonnes numériques (ControlA, Target, Flux1, Flux2), sous-dossiers
par contrôle + `controls_summary.json`, pas de `master_results.json` à la
racine — et ne sont PAS comparables aux runs single de v4.4.2. Le 3e run
(A_single_full_off) a été tué par le redémarrage machine de ~14h38 avant
de finir, dans ce même mauvais mode.

Correction (code jamais touché, lanceurs seuls) : `--control-mode single`
ajouté explicitement à tous les runs single (12 A/B + 13 D en synthétique,
36 en Ising). Les runs C_multi / C_all gardaient déjà leur mode explicite.
Sorties des 3 runs supprimées (`A_single_fast_off`, `B_single_fast_on`,
`A_single_full_off`), `synth/run.log` réinitialisé avec note de correction,
état de surveillance remis à 0/0 (`dead_reported=false`). Le lot repart de
zéro en mode single, même périmètre, même protocole. La relance a aussi
validé le mécanisme SKIP : il ne se déclenche que sur `master_results.json`
à la racine, donc un run en mode all ne serait jamais skippé — autre raison
de repartir proprement plutôt que de continuer sur les sorties all.

## 7. Lecture des résultats (à la fin du lot)

- Comparaison v4.4.2 point par point : seuils MC fast (37,07 / 37,07 /
  37,56 / 63,41 / 37,80 / 21,22 %), cascades T_0 fast (33,32 / 33,32 /
  73,26 / 13,05 / 60,64 / 2,60 %), synthèse 31/31.
- Nouvelles clés à lire : `cascade.thresholds_in_control_units`,
  `metadata.control_monotonicity`, blocs `[CIBLE-FIXE-DIAGONALE]` et
  `[AVERTISSEMENT-CONTROLE-NON-MONOTONE]`, `target_policy` /
  `target_resolution` dans les métadonnées.
- Aucune traduction des seuils en T dans les messages de surveillance ;
  traduction post-hoc seulement dans la synthèse finale, avec la question
  garder/retirer la comparaison Tc toujours ouverte.
- Aucun verdict final avant la fin du lot. Aucun run mushroom dans ce lot.
