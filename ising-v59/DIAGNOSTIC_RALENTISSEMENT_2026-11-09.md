# Diagnostic du ralentissement v5.9.0f — profilage comparé sur copies

**Date :** 9 novembre 2026, 12h24–12h50 (heure de Montréal)
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Statut :** cause identifiée et mesurée — multi-horizons L1/L3/L5 (v5.6), pas les nouveaux diagnostics.

## 0. Verdict

**Le ralentissement de l'étape 1 vient des multi-horizons v5.6 (défaut 1..12) : L1, L3 et L5 sont calculés 12 fois au lieu d'une, et chaque horizon supplémentaire coûte ~3,3 s sur le cas synthétique (≈ +4,7 s sur Ising fast, n=960).** Revenir à un seul horizon (`--horizons "7"`) ramène le run de 101 s à 65 s, soit la durée v5.4.0 (63 s) à 2 s près — seuils identiques. **Le surcoût est fixe par run, pas proportionnel : il disparaît en full** (moins de 1 % d'un run de ~95 min), ce qui explique que le mode full ne montre aucun ralentissement.

Les suspects initiaux sont innocentés par la mesure : walk-forward adaptatif ~2 s, dashboard ~1 s, télémétrie ~1 s, poids de régime ~1 s, L7b-light ~0 s — tous drapeaux coupés ensemble, le run reste à 100 s. Le budget workers (3 au lieu de 4) ne joue pas non plus : le MC fast est séquentiel dans les deux versions (12 itérations < 20), et le scan comme `run_pipeline` coûtent pareil dans les deux profils.

## 1. Provenance

- **Originaux (jamais modifiés, SHA revérifiés à la fin du diagnostic) :**
  - v5.4.0 : `workspace/user/files/UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py` — SHA `c1115e1c4803bc56d330e37e1adb7a6697ea5393c9a42678111dd76162fb05be`
  - v5.9.0f : `workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py` — SHA `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260`
- **Copies exécutées :** `workspace/ising-v59/profilage/v540.py`, `v590f.py` (SHA identiques aux originaux). Aucune écriture dans `workspace/user/files/`.
- **Cas mesuré :** A_single_fast_off — `--input workspace/ising-v425-all-options/data/synth.csv --mode fast --control-mode single --control ControlA --no-harmonic-validation` (+ `--l7b-light` en v5.9.0f, comme le lot). Entrée synthétique, 200 points, graine 42.
- **Références du lot (étape 1, 8 nov.) :** v5.4.0 A_single_fast_off 63 s ; v5.9.0f 99 s. Les baselines mesurées ici reproduisent ces valeurs (63 s et 101 s).
- **Outils :** pilotes résumables `workspace/ising-v59/profilage/run_matrix.sh` (m01–m10) et `run_matrix2.sh` (m11–m13), journaux `matrix.log` / `matrix2.log`, sorties `out/m01…m13/master_results.json`, profils cProfile `prof540.out` / `prof590.out`.
- **Incident :** un redémarrage VM ~12h27 a tué la première tentative de profil (v540 en cours, dossier partiel nettoyé) ; la matrice a été relancée ensuite sans perte, pilote résumable.
- **Ce qui manque :** une seule répétition par cas (bruit machine ±2 s estimé d'après les répétitions du lot) ; le coût par horizon en Ising fast n'a pas été re-mesuré ici, il est déduit des écarts du lot (+48 à +55 s sur 11 horizons, soit ~+4,7 s/horizon à n=960).

## 2. Mesures — durées murales, cas A_single_fast_off

Toutes les durées sont des secondes murales lues dans `matrix.log` / `matrix2.log` (champ `duree_s`, `timeout 600`). Seuils relus dans chaque `master_results.json` : **MC 56,73 % et T_0 49,42 % identiques sur les 13 runs** (y compris `--horizons "7"` et tous les drapeaux coupés). Les drapeaux ne déplacent aucun seuil ; `--no-adaptive-walk-forward` rend seulement le verdict L7b INDETERMINE (pas de données walk-forward), au lieu de FRAGILE.

| Run | Configuration | Durée (s) | Écart vs v5.4.0 |
|---|---|---|---|
| m01 | v5.4.0, référence | 63 | — |
| m02 | v5.9.0f, défaut (12 horizons) | 101 | +38 s (+60 %) |
| m03 | v5.9.0f + `--no-adaptive-walk-forward` | 99 | +36 s |
| m04 | v5.9.0f + `--no-l7b` | 101 | +38 s |
| m05 | v5.9.0f + `--no-dashboard` | 100 | +37 s |
| m06 | v5.9.0f + `--no-telemetry` | 100 | +37 s |
| m07 | v5.9.0f + `--no-regime-weights` | 100 | +37 s |
| m08 | v5.9.0f, tous les drapeaux coupés | 100 | +37 s |
| **m11** | **v5.9.0f + `--horizons "7"` (1 horizon)** | **65** | **+2 s** |
| m12 | v5.9.0f + `--horizons "1,3,6,12"` (4 horizons) | 75 | +12 s |
| m13 | v5.9.0f + `--horizons "7"` + tous les drapeaux coupés | 62 | −1 s |

**Loi mesurée (cas synth, n=200) : durée ≈ 65 s + 3,3 s × (n_horizons − 1).** 1 horizon → 65 s, 4 horizons → 75 s, 12 horizons → 101 s. L'ajustement est exact à ±1 s. En Ising fast (n=960), les écarts du lot donnent ~+4,7 s par horizon supplémentaire.

## 3. Mécanisme — lecture du code et profils cProfile

### 3.1 Ce qui a changé en v5.6 : les niveaux L1/L3/L5/L6 en 12 horizons

- `HORIZONS_DEFAULT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]` (v590f, ligne 333) ; `--horizon` et `--horizons` ont pour défaut `None`, donc **le lot a tourné en 12 horizons sans le demander**. L'en-tête l'annonce d'ailleurs (ligne 332) : « compter +15-30 s » — la mesure donne +38 s sur ce cas.
- v5.4.0 : L1 = un appel `level_target_universal` mono-horizon ; L3 = `level_regime(data, horizon, …)` ; L5 = `level_complexity(data, horizon, …)` — un horizon chacun.
- v5.9.0f : le dispatcher appelle le cœur mono-horizon **12 fois** (L1 : `_level_target_single_horizon` ; L3 : `level_regime` ; L5 : `level_complexity` ; L6 : boucle arithmétique bon marché sur la courbe de scan).

### 3.2 Où part le temps — profils cProfile (m09/m10)

cProfile gonfle les durées (~×1,6 : 106 s et 164 s au lieu de 63 s et 101 s), mais la répartition est parlante. Totaux profilés : v540 104,3 s ; v590 163,6 s (+59,3 s).

| Fonction (temps cumulé) | v5.4.0 | v5.9.0f | Lecture |
|---|---|---|---|
| `level_target_universal` (L1) | 4,57 s (1 appel) | 55,37 s (1 appel, 12 horizons) | **×12,1 — contributeur dominant** |
| `level_complexity` (L5) | 0,66 s (1 appel) | 17,26 s (13 appels) | ×26 — contributeur secondaire |
| `level_regime` (L3) | 0,02 s | 0,72 s | négligeable |
| `run_pipeline` | 49,63 s | 49,01 s | identique |
| scan (courbe) | 7,15 s | 6,69 s | identique |
| `write_interactive_dashboard` | — | 0,66 s | négligeable |
| `adaptive_walk_forward_validation` | — | 0,01 s | négligeable |
| `level_robustness_L7b_light` | — | 0,00 s | nul |

À l'intérieur de L1, le coût est presque entièrement `_evaluate_predictive_mc_complexity_paths` : **48 appels / 4,51 s en v540 → 576 appels / 54,76 s en v590 (×12)**. Chaque appel recalcule les 29 estimateurs (`apply_complexity` → `_compute_extra_estimators` → `_safe_call`) sur des chemins MC : `_compute_extra_estimators` passe de 10 563 appels / 26,88 s à 21 651 appels / 63,52 s ; `visibility_graph_dimension`, `danco_dimension`, `mfdfa_spectrum`, `graph_cluster_dimension` doublent tous (503 → 1 031 appels). Le `run_pipeline` principal (360 appels `apply_complexity`, ~30 s) est **identique** dans les deux versions — le surcoût vient uniquement de la répétition par horizon.

Répartition estimée du surcoût mural (+38 s, cas synth) : **L1 ≈ +32 s (≈ 85 %)**, **L5 ≈ +10 s (≈ 25 %, ordre de grandeur d'après le profil — la somme dépasse +38 s parce que cProfile gonfle inégalement les petites fonctions)**, L3 + dashboard + télémétrie + walk-forward + L7b ≈ +1 s au total.

### 3.3 Pourquoi le full ne ralentit pas

Le surcoût est **additif et fixe par run** (~+36 s en synth fast, ~+52 s en Ising fast), pas proportionnel à la durée du run : il ne dépend que du nombre d'horizons et de la taille des séries, pas du mode. En full, le scan Monte Carlo (~95 min) domine tellement que +40 s représentent moins de 1 % — invisible dans les écarts mesurés du lot full (−58 s à +57 s, moyenne +2 s). C'est cohérent avec les deux échelles : le ralentissement est réel en fast/synth, indétectable en full.

### 3.4 Suspects écartés (mesuré, pas déduit)

- **Budget workers 3 vs 4 + BLAS à 1 thread** : le MC fast est séquentiel dans les deux versions (12 itérations < 20 pour `use_parallel`) ; le scan et `run_pipeline` coûtent pareil dans les deux profils. Le changement de workers n'explique rien en fast.
- **Walk-forward adaptatif** : 5 cascades analytiques par run, 0,01 s au profil, −2 s en ablation (bruit).
- **L7b-light** : audit en lecture seule sur L1/L3/L5/L7, 0,00 s au profil, 0 s en ablation.
- **Dashboard HTML** : 0,66 s au profil (import plotly + écriture), −1 s en ablation.
- **Télémétrie JSONL** : ~7 émissions par run, −1 s en ablation.
- **Poids de régime L7** : arithmétique sur dictionnaires, −1 s en ablation.
- **Démarrage / imports** : `python3 v540.py --help` 1,5 s ; `v590f.py --help` 1,7 s — écart < 0,5 s.
- **Numba-heavy** : désactivé par défaut dans les deux cas ; la porte (`_run_numba_heavy_gate`) n'est pas exécutée quand le drapeau est off (`_use_numba_heavy` retourne False immédiatement).

## 4. Recommandation

- **Le multi-horizons est une fonctionnalité délibérée de v5.6, pas un bug** : il donne le consensus L1/L3/L5 sur 12 horizons et la stabilité inter-horizons lue par L7b. Son prix est ~3,3 s par horizon sur une série de 200 points (~4,7 s à n=960). **Pour les balayages fast/synth, passer `--horizons "7"` (un seul horizon, comportement legacy) rend à v5.9.0f sa vitesse v5.4.0 sans déplacer aucun seuil** (MC/T_0 vérifiés identiques). `--horizons "1,3,6,12"` est un compromis (75 s, consensus sur 4 horizons).
- **Pour les runs full, ne rien changer** : le surcoût est < 1 % et invisible ; garder le défaut 1..12.
- **Ne pas couper les petits drapeaux pour la vitesse** : `--no-dashboard`, `--no-telemetry`, `--no-l7b`, `--no-regime-weights`, `--no-adaptive-walk-forward` ne gagnent rien (≤ 2 s ensemble) et `--no-adaptive-walk-forward` rend L7b INDETERMINE. Le seul levier qui compte est `--horizons`.
- **Décision à Zackary** : le défaut 12 horizons vaut-il +38 s par run fast ? Si oui, le lot actuel reste comparable tel quel ; si non, figer `--horizons "7"` dans les lanceurs fast/synth (les lanceurs full n'en ont pas besoin).

## 5. À part — bug cosmétique trouvé en passant

`python3 v590f.py --help` plante : `ValueError: unsupported format character 'm' (0x6d) at index 59` — un `%` non échappé dans un texte d'aide argparse (probablement `--max-workers` ou un texte contenant « % »). Sans effet sur les runs (l'aide n'est jamais appelée par les lanceurs), à corriger d'un `%` → `%%` dans une prochaine version.

## 6. Fichiers

- Rapport : `workspace/ising-v59/DIAGNOSTIC_RALENTISSEMENT_2026-11-09.md` (ce fichier)
- Pilotes : `workspace/ising-v59/profilage/run_matrix.sh`, `run_matrix2.sh` ; journaux `matrix.log`, `matrix2.log`
- Sorties : `workspace/ising-v59/profilage/out/m01…m13/master_results.json` ; profils `prof540.out`, `prof590.out`
- Copies : `workspace/ising-v59/profilage/v540.py`, `v590f.py` (SHA = originaux, vérifiés inchangés en fin de diagnostic)
- Références : `workspace/ising-v59/SYNTHESE_ETAPE1_2026-11-08.md` (§2 durées), `workspace/ising-v59/PROTOCOLE.md` (§2.2)
