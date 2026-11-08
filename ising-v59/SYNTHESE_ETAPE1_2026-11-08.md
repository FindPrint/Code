# Synthèse étape 1 — test v5.9.0f (L7a/L7b)

**Date :** 8 novembre 2026, 13h51 (fin de l'étape 1)
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Statut :** étape 1 terminée — synth 31/31 + fast Ising 6/6. Étape 2 (un run full/fliprate décisif) lancée 14h13, en cours.

## 1. Provenance

- **Code testé :** `workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py` — 13 013 lignes, 622 212 octets, SHA `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260`, jamais modifié, compilation OK.
  - `VERSION_MASTER = "v5.9.0-L7aL7b-CoherenceRobustesse"`, `VERSION = "v5.9.0"` (commentaire erroné « v5.8.0 », titre d'en-tête « v5.8 » — trois étiquettes, même incohérence que v5.4.0).
  - `CONTROL_MODE = "single"` (le piège v5.4.0 est corrigé), `DEFAULT_CONTROL_COLUMN = 'Time'`, `HARMONIC_VALIDATION_ENABLED = False`.
- **Code de référence :** v5.4.0, `workspace/user/files/UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py`, SHA `c1115e1c…`.
- **Données :** synth `workspace/ising-v425-all-options/data/` (graine 42) ; Ising `workspace/ising-v354/data/ising_classic_v354.csv` (960 lignes, SHA `9027dfd5…`, L=32, T = linspace(1.7, 3.3, 24), 40 snapshots/T, graine 42).
- **Protocole :** `workspace/ising-v59/PROTOCOLE.md` (gelé avant les runs). Lanceurs `run_synth59.sh`, `run_ising59_fast.sh` ; `--l7b-light` explicite partout, `--control-mode single`. Timeouts : 1 200 s (synth), 21 600 s (Ising).
- **Cécité :** vérifiée avant les runs — 12 occurrences de « temperature »/« onsager », toutes hors analyse (FSS sans appelant, générateur d'exemple, usage CLI). Aucune traduction en T dans cette synthèse, aucun verdict final.
- **Ce qui manque :** les 2 runs rc=1 attendus n'ont pas de `master_results.json` (D_short : série trop courte ; D_missing_file : fichier manquant). Les verdicts L7b en mode full (`--l7b-full`, graine/fenêtre/mélange) ne sont pas mesurés — le mode light ne les teste pas.

## 2. Durées — v5.9.0f contre v5.4.0

Toutes les durées sont lues dans `synth/run.log` et `ising/run.log` (champ `duree_s`). Références v5.4.0 : lot du 7–8 nov. 2026, mêmes données, même graine.

### 2.1 Synthétique (29 runs rc=0)

| Run | v5.9.0f (s) | v5.4.0 (s) | Écart |
|---|---|---|---|
| A_single_fast_off | 99 | 63 | +57 % |
| B_single_fast_on | 100 | 62 | +61 % |
| A_single_full_off | 447 | 415 | +8 % |
| B_single_full_on | 452 | 422 | +7 % |
| A_single_predict_off | 180 | 123 | +46 % |
| B_single_predict_on | 168 | 124 | +35 % |
| A_single_analyze_off | 198 | 155 | +28 % |
| B_single_analyze_on | 195 | 157 | +24 % |
| A_single_stable_off | 138 | 102 | +35 % |
| B_single_stable_on | 137 | 100 | +37 % |
| A_single_robust_off | 194 | 154 | +26 % |
| B_single_robust_on | 207 | 159 | +30 % |
| C_multi_fast_off | 192 | 116 | +66 % |
| C_multi_fast_on | 193 | 116 | +66 % |
| C_all_fast_off | 379 | 227 | +67 % |
| C_multi_stable_off | 263 | 184 | +43 % |
| C_multi_stable_on | 260 | 184 | +41 % |
| C_all_stable_off | 496 | 352 | +41 % |
| D_nan_fast_off | 70 | 63 | +11 % |
| D_const_fast_off | 87 | 50 | +74 % |
| D_const_fast_on | 89 | 52 | +71 % |
| D_const_stable_off | 116 | 69 | +68 % |
| D_const_robust_off | 131 | 93 | +41 % |
| D_missing_control | 100 | 61 | +64 % |
| D_target_eq_control | 99 | 62 | +60 % |
| D_no_control | 99 | 61 | +62 % |
| D_seed7_horizon5 | 61 | 60 | +2 % |
| D_domain_physics | 99 | 61 | +62 % |
| D_2000_fast_off | 206 | 147 | +40 % |

### 2.2 Ising fast (6 runs rc=0)

| Run | v5.9.0f (s) | v5.4.0 (s) | Écart |
|---|---|---|---|
| fast/fliprate | 254 | 203 | +25 % |
| fast/flip | 253 | 205 | +23 % |
| fast/energy | 264 | 212 | +25 % |
| fast/magnetization | 326 | 274 | +19 % |
| fast/localvar | 266 | 211 | +26 % |
| fast/susceptibility | 322 | 268 | +20 % |

**Constat : 35 runs rc=0 sur 35 plus lents.** Le ralentissement touche tous les modes. Budget workers confirmé dans les journaux : 3 workers, chunksize=5, plafond_prudent=3, BLAS/worker=1 (contre 4 workers en v5.4.0).

**Piste, non encore prouvée :** en fast, le Monte Carlo n'a que 12 itérations et `use_parallel` exige ≥ 20 itérations — le MC fast tourne donc en séquentiel dans les deux versions. Le changement de workers n'explique pas le ralentissement en fast (+57 à +61 %). Le surcoût vient d'ailleurs dans la v5.9.0f : nouveaux diagnostics (walk-forward glissant, télémétrie JSONL, dashboard HTML), L7b-light, poids de régime L7. À mesurer par profilage sur copies, jamais sur l'original.

## 3. Seuils — identiques à v5.4.0 sur les 35 runs

Seuil MC = `run_pipeline.threshold_metadata.opt_threshold` ; T_0 = `five_threshold_cascade.T_0_Monte_Carlo_Central`. Valeurs lues dans les `master_results.json`, vérifiées une par une.

- **Synth, jeu de base :** MC fast 56,73 %, full/predict/robust 68,03 %, analyze/stable 54,38 % ; T_0 49,42 % partout ; brut 48,8433 ambigu.
- **Synth, cas particuliers :** D_const MC 26,92 % (fast), 92,86 % (stable), 90,85 % (robust), T_0 68,49 %, brut 5,0 **non ambigu** — seule valeur brute non ambiguë du lot. D_seed7 MC 53,57 %, T_0 49,68 %. D_2000 MC 49,79 %, T_0 48,63 %.
- **Synth, multi/all :** ControlA 56,73 % / 49,42 % (fast), 54,38 % / 49,42 % (stable) ; Flux1 9,68 % / 44,41 % (fast), 10,71 % / 44,41 % (stable) ; Flux2 14,42 % / 87,60 % (fast), 17,86 % / 87,60 % (stable) ; Target 62,50 % / 25,83 % (fast), 60,71 % / 25,83 % (stable). Toutes valeurs brutes ambiguës.
- **Ising fast :** fliprate/flip MC 37,01 %, T_0 33,32 % ; energy MC 37,17 %, T_0 73,26 % ; magnetization MC 64,23 %, T_0 13,05 % ; localvar MC 37,50 %, T_0 60,64 % ; susceptibility MC 27,27 %, T_0 2,60 %. Bruts ambigus partout (fliprate 0,1622 ; flip 166,14 ; energy −0,8711 ; magnetization 0,0332 ; localvar 0,5751 ; susceptibility 0,0265).

**Constat : le chemin de calcul NumPy est inchangé** — l'en-tête promet des scores bit-à-bit identiques à v5.6, et les seuils mesurés sont identiques à v5.4.0 sur les 35 runs. La v5.9.0f ne déplace aucun seuil ; elle coûte plus cher à chaque run.

## 4. L7b-ROBUSTESSE (nouveauté v5.9.0f) — lecture des 45 sorties

Clé lue : `prediction_levels.L7b_robustesse` (mode `light`, sans re-run). 45 sorties lues : 23 single synth + 16 contrôles multi/all + 6 fast Ising.

### 4.1 Verdicts : 45/45 FRAGILE

Aucune sortie ROBUSTE, aucune INDÉTERMINÉE. La lecture unique : « Au moins un check light FAIL. Ne pas utiliser L7a seul pour décider. Passer en --l7b-full pour confirmer. »

### 4.2 Détail des checks

| Check | Règle lue dans le code / les sorties | Résultat sur les 45 sorties |
|---|---|---|
| `stabilite_horizon` | PASS si stabilité min ≥ 0,80 sur L1/L3/L5 | PASS presque partout (synth base 0,917 ; Ising susceptibility 0,833). FAIL sur D_const (0,75), D_2000, A/B analyze, C_all Flux1/Flux2/Target (stable), C_multi Flux1 (stable), fast/flip, fast/fliprate, fast/localvar. |
| `stabilite_walkforward` | FAIL si t0_std > 20 (écart-type de T_0 en walk-forward glissant) | **FAIL presque partout.** Synth base : t0_std = 29,4. Ising susceptibility : t0_std = 51,5. PASS seulement sur les runs D_const (t0_std = 0,0) et sur C_all Target (stable) et C_all_fast_off Target. |
| `coherence_interne` | FAIL si cible (L1) et régime (L3/L6) divergent | PASS presque partout. FAIL sur C_all Flux2 (fast et stable), C_all Target (fast et stable), fast/susceptibility (cible down, régime up, pénalité 0,2). |
| `note_graine_fenetre_melange` | Non testé en mode light | « Non testés en mode light. Utiliser --l7b-full pour graine / fenêtre / mélange / échelle. » sur les 45 sorties. |

### 4.3 Ce que cela veut dire, et ce que cela ne veut pas dire

- **Mesuré :** en mode light, le verdict est FRAGILE partout, et c'est presque toujours le check walk-forward qui le déclenche (t0_std > 20), alors même que le seuil T_0 est stable d'un mode à l'autre sur le même jeu (49,42 % en synth, valeurs Ising identiques à v5.4.0).
- **Question ouverte, non tranchée :** le seuil du check (t0_std ≤ 10 pour PASS, > 20 pour FAIL) est-il calibré, ou la cascade T_0 varie-t-elle réellement beaucoup d'une fenêtre glissante à l'autre ? La réponse exige soit le mode `--l7b-full` (4 re-runs), soit une lecture directe des séries walk-forward déjà calculées. **Ce n'est pas un verdict sur l'instrument** : un seul audit, en mode light, ne déclare rien sur le pipeline entier.
- **Nuance importante :** les runs D_const (contrôle constant) passent le walk-forward (t0_std = 0,0) mais échouent l'horizon (0,75) — les deux checks ne mesurent pas la même chose, et leurs échecs ne se recouvrent pas.

## 5. Ce qui suit

1. **Étape 2 (en cours) :** un run full/fliprate décisif, lancé 8 nov. 14h13 (`run_full_fliprate59.sh`, PID 40530), référence v5.4.0 : 5 679 s. Fin attendue ~16h00–16h15.
2. **Étape 3 (décision après l'étape 2) :** suite du lot (full, predict, analyze, stable, robust — 30 runs Ising). Non lancée.
3. **Diagnostic du ralentissement :** profilage comparé v5.4.0 / v5.9.0f sur copies, pour localiser le surcoût (dashboard, walk-forward, télémétrie, L7b-light, poids de régime).
4. **Calibration L7b :** lecture des séries walk-forward ; comparaison avec le diagnostic walk-forward de v5.4.0 si présent dans ses sorties.
5. **Publication :** ce dossier et cette synthèse sont destinés au dépôt privé FindPrint/Code (branche main), avec le protocole et les journaux.

## 6. Fichiers

- Protocole : `workspace/ising-v59/PROTOCOLE.md`
- Lanceurs : `workspace/ising-v59/run_synth59.sh`, `run_ising59_fast.sh`, `run_ising59.sh`, `run_v59.sh`, `run_full_fliprate59.sh`
- Journaux : `workspace/ising-v59/synth/run.log` (31 END), `workspace/ising-v59/ising/run.log` (6 END + ISING DONE 18:51:13 UTC)
- Sorties : `workspace/ising-v59/synth/<nom>/master_results.json`, `workspace/ising-v59/ising/fast/<contrôle>/master_results.json`
- Extraction L7b : `/tmp/l7b_extract.py` (script jetable ; les valeurs ci-dessus sont relues dans les `master_results.json`)
- Surveillance : cron `ising-v59-watch` (15 min, signale sans relancer)
