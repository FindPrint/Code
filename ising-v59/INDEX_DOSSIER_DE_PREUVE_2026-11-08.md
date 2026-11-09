# Index du dossier de preuve — lot v5.9.0f (L7a/L7b), étapes 1 à 3

**Date :** 8 novembre 2026
**Mise à jour :** 9 novembre 2026 — étapes 2 et 3 (full 6/6) terminées, diagnostic du ralentissement terminé ; ce push dépose ces ajouts.
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Règle :** chaque entrée dit ce que le fichier prouve, où il vit, et d'où viennent ses chiffres. Rien n'est résumé ici à la place du fichier : l'index pointe, il ne remplace pas.

## 1. Le code testé (original, jamais modifié)

| Fichier | Ce qu'il prouve |
|---|---|
| `workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py` — 13 013 lignes, 622 212 octets, SHA `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260` | C'est le code testé, et seulement lui. Cécité vérifiée avant runs : 12 occurrences temperature/onsager, toutes hors analyse (FSS sans appelant, générateur d'exemple, usage CLI). `CONTROL_MODE = "single"` par défaut (le piège v5.4.0 est corrigé). |

## 2. Le protocole (gelé avant les runs)

| Fichier | Ce qu'il prouve |
|---|---|
| `workspace/ising-v59/PROTOCOLE.md` (7 890 octets, gelé 8 nov. 11h51) | Le périmètre du test étagé : mêmes données que v5.4.0, graine 42, timeouts 1 200 s (synth) / 6 h (Ising), `--l7b-light` explicite partout, `--control-mode single`. Étape 1 = synth 31 + fast Ising 6 ; étape 2 = un seul run full/fliprate décisif ; étape 3 = suite, seulement sur go. Le lot complet n'est pas lancé d'un bloc. |

## 3. Les lanceurs (copies adaptées, code jamais touché)

| Fichier | Ce qu'il prouve |
|---|---|
| `workspace/ising-v59/run_synth59.sh`, `run_ising59_fast.sh`, `run_ising59.sh`, `run_v59.sh`, `run_full_fliprate59.sh`, `run_ising59_full.sh` | Comment chaque run a été lancé (drapeaux exacts, SKIP des runs terminés, journalisation START/END). `run_full_fliprate59.sh` = étape 2, un seul run. `run_ising59_full.sh` = étape 3, mode full × 6 contrôles (SKIP des terminés, « FULL DONE » à la fin). |

## 4. Les journaux d'exécution (la preuve brute que les runs ont eu lieu)

| Fichier | Ce qu'il prouve |
|---|---|
| `workspace/ising-v59/synth/run.log` — 31 END | Les 31 runs synth, avec durées et codes de retour (29 rc=0, D_short et D_missing_file rc=1 attendus). |
| `workspace/ising-v59/ising/run.log` — 12 END (fast 6 + full 6), « FULL DONE » 9 nov. 07h21 | Les 6 runs fast et les 6 runs full Ising, avec l'historique des 8 redémarrages VM pendant le lot (tentatives tuées à l'étape Monte Carlo, relances durables depuis le fil principal) et des 4 redémarrages après FULL DONE (~07h27, ~11h27, ~13h28, ~15h28), sans perte. |
| `workspace/ising-v59/runner_synth59.out`, `runner_ising59_fast.out`, `runner_full_fliprate59.out`, `runner_full_fliprate59b.out` | Les sorties des lanceurs (STDOUT/STDERR des runs). |

## 5. Les sorties par run (51 fichiers, 556 Mo synth + 240 Mo Ising)

| Contenu | Ce qu'il prouve |
|---|---|
| `workspace/ising-v59/synth/*/master_results.json` (39 sorties) + `workspace/ising-v59/ising/fast/*/master_results.json` (6 sorties) + `workspace/ising-v59/ising/full/*/master_results.json` (6 sorties) | Les valeurs de chaque run : seuil MC (`run_pipeline.threshold_metadata.opt_threshold`), T_0 de cascade (`five_threshold_cascade.T_0_Monte_Carlo_Central`), valeurs brutes, L7b, walk-forward, estimateurs. **51 fichiers (39 synth + 6 fast + 6 full)** — la matière première de toutes les lectures (les 45 de l'étape 1 = 143 cas (sortie, flux) dans la lecture des estimateurs ; les 6 full ajoutent les valeurs comparées à v5.4.0 dans la synthèse full). |

## 6. Les lectures (vérifiées, une par une)

| Fichier | Ce qu'il prouve |
|---|---|
| `workspace/ising-v59/SYNTHESE_ETAPE1_2026-11-08.md` (10 101 octets, 8 nov. ~14h20) | **Étape 1 : 35 runs rc=0, tous plus lents que v5.4.0 (+2 % à +74 % synth, +19 % à +26 % fast Ising), tous les seuils identiques.** Tableau des durées run par run, seuils, § L7b, suites. |
| `workspace/ising-v59/NOTE_CALIBRATION_L7B_2026-11-08.md` (9 430 octets, 8 nov. ~14h30, §6 ~14h40) | **Pourquoi L7b dit FRAGILE partout :** séries walk-forward mesurées (base [89, 86, 64, 42, 20], std 29,4, identique sur les 12 runs single), puis mécanique lue dans le code (lignes 9811, 9246, 10783+) : l'axe est renormalisé par fenêtre, la dérive est la signature géométrique attendue d'une transition unique. Le check n'est pas calibré (v5.4.0 ne l'a pas). |
| `workspace/ising-v59/LECTURE_ESTIMATEURS_2026-11-08.md` (38 966 octets, 8 nov. 16h00) + `workspace/ising-v59/resultats_estimateurs.csv` (29 lignes, 62 colonnes) + `workspace/ising-v59/harness_estimateurs/` (scripts + JSONs) | **26 signaux distincts / 29** (mêmes 3 paires duplicata que v3.5.4), saturation à 2 estimateurs en Ising, **Lyapunov = artefact**, **v5.9.0f ≡ v5.4.0 sur la couche estimateurs** (df_feat.csv bit-identiques 45/45 ; 0 différence sur 82 940 comparaisons). Couche E abandonnée (cohortes non vérifiées). |
| `workspace/ising-v59/FICHE_INSTRUMENT_2026-11-08.md` (4 409 octets, 8 nov. 16h01) | L'instrument en une page : règles, mesures, limites, état du test, provenance. |
| `workspace/ising-v59/SYNTHESE_FULL_2026-11-09.md` (7 023 octets, 9 nov. 08h15) | **Étape 3 : full 6/6, seuils identiques à v5.4.0 point par point, durées à ±1 min (total 35 345 s vs 35 333 s, +12 s).** Tableau run par run, nuit des redémarrages, rappel L7b, décisions à Zackary. |
| `workspace/ising-v59/DIAGNOSTIC_RALENTISSEMENT_2026-11-09.md` (11 036 octets, 9 nov. 07h52) + `workspace/ising-v59/profilage/` (pilotes, matrices, profils) | **Cause du ralentissement : multi-horizons v5.6 par défaut 1..12.** Mesuré sur copies : v5.4.0 63 s, v5.9.0f défaut 101 s, `--horizons "7"` 65 s, seuils identiques. Les dumps binaires cProfile (`prof540.out`, `prof590.out`) restent locaux (snapshot GitHub = UTF-8 seulement) ; leurs rendus texte (`prof540.txt`, `prof590.txt`, top 40 cumulatif) sont déposés. |

## 7. La référence de comparaison — v5.4.0 (lot arrêté)

| Fichier | Ce qu'il prouve |
|---|---|
| `workspace/user/files/UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py` — SHA `c1115e1c…` | Le code de référence, jamais modifié. |
| `workspace/ising-v54/PROTOCOLE.md` + `workspace/ising-v54/SYNTHESE_PARTIELLE_2026-11-08.md` (11 678 octets) | Protocole miroir et synthèse partielle du lot arrêté à 13/36 le 8 nov. 11h38 (23 runs non mesurés : predict 5/6, analyze, stable, robust 6/6). Full v5.4.0 = robust v4.2.9 sur les 4 contrôles comparables. |
| `workspace/ising-v54/synth/*/master_results.json` + `ising/*/*/master_results.json` (52 fichiers) | Les valeurs de référence : durées (full/fliprate 5 679 s) et seuils comparés run par run dans la synthèse étape 1. |
| `workspace/ising-v54/v5.4.1-correction-CONTROL_MODE.patch` (1 975 octets) | Le correctif du piège `CONTROL_MODE = "all"` — prêt, vérifié sur copie, **sans réponse** (question posée le 7 nov. ~16h11, ne pas reproposer). Le défaut est corrigé dans v5.9.0f. |

## 8. Ce qui manque (dit explicitement, pas caché)

- **Étape 2 TERMINÉE** (full/fliprate 8 nov. 18h28, 5 690 s, seuils identiques à v5.4.0).
- **Étape 3 (full) TERMINÉE 6/6** (9 nov. 07h21). Restent reportés : predict/analyze/stable/robust, 24 runs — décision de Zackary en attente (bilan du 9 nov.).
- **Couche E abandonnée** dans la lecture des estimateurs : comparaison à Tc non vérifiée exactement, donc absente.
- **Nul permuté L7b** : pas encore fait — c'est la confirmation définitive de l'analyse géométrique.
- **Publication GitHub : ce push dépose la synthèse full, le diagnostic et le profilage (étapes 2 et 3).** Sorties brutes (834 Mo) hors dépôt, comme pour l'étape 1 : ne déposer que les lectures, protocoles et journaux, pas les `master_results.json`.
