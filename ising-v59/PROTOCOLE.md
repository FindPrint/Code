# PROTOCOLE — Test v5.9.0f (L7a/L7b) — lot gelé le 8 nov. 2026

## 0. Demande

Zackary, 8 nov. 11h48 : « Voici un nouvelle version qui devrai aller plus vite
je crois pouvez-vous la tester et me dire ce que tu en pense ». Fichier reçu :
`workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py`.

## 1. Fichier testé (jamais modifié)

- 13 013 lignes, 622 212 octets, SHA
  `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260`
  (vérifié à la réception), `python3 -m py_compile` OK.
- `VERSION_MASTER = "v5.9.0-L7aL7b-CoherenceRobustesse"`,
  `VERSION = "v5.9.0"` (calculé par split ; le commentaire dit « v5.8.0 »,
  erroné). Titre d'en-tête : « UNIVERSAL_LOG v5.8 ». **Trois étiquettes
  différentes** — même incohérence que v5.4.0 (titre v5.3 / VERSION v5.4).
  Le VERSION_MASTER fait foi.
- `CONTROL_MODE = "single"` (ligne 317) — le piège v5.4.0 (défaut « all »)
  est corrigé en v5.6 : le correctif v5.4.1 proposé le 7 nov. est désormais
  dans le code. `DEFAULT_CONTROL_COLUMN = 'Time'` (comme v5.4.0),
  `HARMONIC_VALIDATION_ENABLED = False` (comme v4.4.2 ; v5.4.0 avait True).
  Les lanceurs passent quand même `--control-mode single` explicitement
  partout (comparabilité, coût nul).

## 2. Audit avant runs (8 nov. 11h48–12h00)

### 2.1 Cécité du chemin d'analyse : TENUE

12 occurrences de « temperature » / « onsager », toutes hors analyse —
même motif que v5.4.0 : docstring FSS (ligne 10192) et
`param_name = "Temperature"` dans `finite_size_scaling_ising` (10212,
**aucun appelant** dans le chemin principal), générateur d'exemple
`generate_example_ising_csv` (12548–12606, appelé seulement via
`--generate-example-ising`), ligne d'usage CLI (12548). Aucune lecture
d'une colonne Temperature dans `run_pipeline`, le scan ou la cascade.

### 2.2 Nouveautés

- **L7a-COHERENCE** : vote existant (`level_coherence_universal`), inchangé.
- **L7b-ROBUSTESSE** (nouveau) : audit, ne vote jamais UP/DOWN, ne change
  jamais L7a. Trois modes CLI : `--l7b-light` (défaut, sans re-run),
  `--l7b-full` / `--l7b` (4 re-runs : graine + fenêtre 80 % + mélange + log —
  l'aide dit « ~3-4x un run »), `--no-l7b` (désactivé, L7a seul comme v5.8.0).
  **Le lot passe `--l7b-light` explicitement partout** : le full est exclu
  du test de vitesse (il multiplierait le coût par 3–4).
- **v5.6** : défauts alignés sur la doc (CONTROL_MODE single,
  HARMONIC_VALIDATION_ENABLED False).
- **v5.7 — budget workers** (le levier de vitesse par défaut) : défaut
  max(1, cpu−1) borné par la RAM (`WORKER_RAM_FRACTION`,
  `WORKER_RESERVE_CORES = 1`) ; chaque worker épingle BLAS/Numba à 1 thread
  (initializer du pool) ; chunksize adaptatif ; ordre des itérations
  inchangé (map ordonné, graine = seed + itération). Ici : **3 workers**
  au lieu de 4 en v5.4.0. `--max-workers` (nouveau) permet un dépassement
  explicite, respecté mais signalé.
- **v5.7 — Numba-heavy** : noyaux Katz / DFA / distances GP, DÉSACTIVÉS par
  défaut. `--numba-heavy` les active seulement si un contrôle d'écart sur
  séries fixes passe ; sinon chemin NumPy conservé, refus journalisé.
  **Non utilisé dans ce lot** (défaut = chemin NumPy v5.6 bit-à-bit selon
  l'en-tête, item 23).
- **v5.7 — autres** : walk-forward glissant (diagnostic, à côté de
  l'existant), poids de régime L7 (`--no-regime-weights` revient au vote
  v5.6), générateurs d'exemple Lorenz / Kuramoto / logistique, télémétrie
  JSONL (`telemetry.jsonl`), dashboard HTML optionnel (`--no-dashboard`
  pour le couper — laissé par défaut ici).
- Paramètres des modes **IDENTIQUES à v5.4.0** (mêmes n_bootstrap,
  window_scan, optimization_iterations, w_size, tests). Le scan et la
  cascade par défaut devraient donc reproduire v5.4.0 — à vérifier
  empiriquement sur fast.
- Diff vs v5.4.0 : 2 544 lignes changées (couches v5.5 → v5.9).
- `_MODE_TO_PIPE` = identité pour les 6 modes (full vrai mode).
- CLI compatible avec les lanceurs v5.4.0, plus `--l7b-*`, `--max-workers`,
  `--numba-heavy`, `--no-dashboard`, `--no-regime-weights`.

### 2.3 Avis avant mesure (à confirmer par les durées)

Le seul levier de vitesse actif par défaut est le budget workers (3 au lieu
de 4, BLAS à 1 thread) + chunksize adaptatif. Sur cette VM (quota 2 vCPU,
`cpu_count` = 4), v5.4.0 faisait tourner 4 workers pouvant chacun lancer des
threads BLAS — sur-souscription plausible. Réduire le thrashing peut
réellement accélérer l'étape Monte Carlo. Mais ce n'est qu'une hypothèse :
**la vitesse se mesure, elle ne se déduit pas du code.** Si l'accélération
attendue venait de Numba, le test par défaut ne la verra pas (désactivé).
Le test décisif est la durée d'un run full Ising (v5.4.0 : 5 679 s pour
full/fliprate).

## 3. Périmètre du test (miroir v5.4.0, ÉTAGÉ)

Le lot v5.4.0 vient d'être arrêté le 8 nov. 11h38 parce que les modes lents
prennent ~95 min/run et que le lot complet prendrait des jours. **Ce lot ne
lance donc pas les 67 runs d'un bloc.**

- **Étape 1 (lancée 8 nov.)** : synth 31 runs + fast Ising 6 runs.
  Lanceurs : `run_synth59.sh`, `run_ising59_fast.sh`.
- **Étape 2 (point de décision, pas lancée sans go)** : UN run full Ising
  (full/fliprate) comme test décisif de vitesse vs 5 679 s (v5.4.0).
  Lanceur complet `run_ising59.sh` prêt (36 runs, résumable).
- **Étape 3 (seulement sur go de Zackary)** : suite du lot (full, predict,
  analyze, stable, robust).

Mêmes données que v5.4.0 : synth `workspace/ising-v425-all-options/data/`
(graine 42), Ising `workspace/ising-v354/data/ising_classic_v354.csv`
(SHA `9027dfd5…`). Mêmes timeouts : 1 200 s (synth), 21 600 s = 6 h (Ising).
Marqueur de fin : « V59 DONE » dans `ising/run.log` (écrit par le maître
`run_v59.sh` seulement si le lot complet est lancé — ne pas le chercher
après l'étape 1).

Références v5.4.0 pour la comparaison des durées (Ising) :
fast 203/205/212/274/211/268 s ; full 5 679/5 631/5 802/5 927/5 708/6 586 s ;
predict/fliprate 5 637 s. Synth v5.4.0 : A_single_fast 63 s, A_single_full
415 s, A/B predict 123/124 s, analyze 155/157 s, stable 102/100 s,
robust 154/159 s (total mur 66 min 38 s).

## 4. Lanceurs (copies v54 adaptées, code jamais touché)

- `run_synth59.sh` : 31 runs, `--control-mode single` partout (C_multi /
  C_all gardent leur mode), `--l7b-light` sur les 18 lignes d'appel.
- `run_ising59_fast.sh` : fast × 6 contrôles, `--control-mode single
  --control "$ctrl" --no-harmonic-validation --l7b-light`.
- `run_ising59.sh` : les 36 runs Ising (6 modes × 6 contrôles), mêmes
  drapeaux, SKIP si `master_results.json` valide.
- `run_v59.sh` : maître (synth puis Ising, « V59 DONE »).
- Vérifié : `bash -n` OK sur les 4 ; aucun `--l7b-full` / `--l7b ` nulle
  part ; CODE = nouveau fichier, BASE = `ising-v59`.

## 5. Surveillance

Cron `ising-v59-watch` (15 min, owner `goal:ising-pipeline-v4-evolution`,
livraison fil principal), état
`~/workspace/goals/ising-pipeline-v4-evolution/hidden_files/ising-v59-watch-state.json`.
Même modèle que v54/v44 : signale sans jamais relancer, message seulement
si vrai neuf (nouveau END ou run mort), s'auto-supprime à la fin du lot
(marqueur « V59 DONE »). Ne pas relancer depuis la surveillance.

## 6. Lecture des résultats (à la fin de chaque étape)

Comparaison v5.4.0 point par point (MC, T_0, brut, durées) + nouvelles clés
v5.9 : `L7a_coherence` / `L7b_robustesse` (verdict ROBUSTE/FRAGILE/
INDETERMINE, mode light), `worker_budget` (télémétrie : workers choisis,
safe_cap, BLAS/worker), `thresholds_in_control_units`,
`control_monotonicity`, blocs `[CIBLE-FIXE-DIAGONALE]` /
`[AVERTISSEMENT-CONTROLE-NON-MONOTONE]`. Aucune traduction en T, aucun
avis final avant la fin de l'étape concernée. Question garder/retirer la
comparaison Tc : toujours ouverte.
