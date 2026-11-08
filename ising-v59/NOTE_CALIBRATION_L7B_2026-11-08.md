# Note de calibration — L7b-ROBUSTESSE, check walk-forward

**Date :** 8 novembre 2026, ~14h30
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Question :** pourquoi le verdict L7b est-il FRAGILE sur les 45 sorties de l'étape 1 ?
**Source des valeurs :** clé `adaptive_walk_forward` des `master_results.json` de `workspace/ising-v59/` (synth + fast Ising), lue par `/tmp/wf_extract.py`. Aucun nouveau run.

## 1. Ce que mesure le check

- Diagnostic : `adaptive_walk_forward`, méthode `rolling_window_reestimated_T0` (nouveauté v5.7).
- Paramètres : n = longueur de la série, fenêtre glissante = n/2, horizon 12, 5 folds.
- À chaque fold, T_0 est ré-estimé sur la fenêtre passée seulement (zéro fuite vérifiée selon la note) ; la série `t0_reestimated` (5 valeurs) est résumée par `t0_std`.
- Règle L7b lue dans les sorties : `stabilite_walkforward` PASS si t0_std ≤ 10, FAIL si t0_std > 20 (entre 10 et 20 : non observé ici).
- **v5.4.0 ne contient pas ce diagnostic** (clé `adaptive_walk_forward` absente de ses `master_results.json`, vérifié sur A_single_fast_off). Il n'existe donc **aucune référence antérieure** : le check n'a jamais passé ni échoué avant la v5.9.0f. Il est non calibré par construction.
- La note de non-fuite affirme que « le walk-forward expansif historique reste disponible sous walk_forward » — **la clé `walk_forward` est absente des sorties lues** (vérifié sur les 45 fichiers). Écart entre la note et le contenu réel, à signaler.

## 2. Séries t0_reestimated mesurées

### 2.1 Synthétique, jeu de base (200 points, fenêtre 100)

**Identique sur les 12 runs single du jeu de base** (fast/full/predict/analyze/stable/robust, off/on) :
`t0 = [89.0, 86.0, 64.0, 42.0, 20.0]`, t0_std = 29,397, span 69,0, directional_accuracy 20 %, mean_rmse 0,178.

Le check est donc **indépendant du mode** : il mesure une propriété des données + du diagnostic, pas du run. Les folds (A_single_fast_off) :

| Fold | Origine | Fenêtre (points) | Seuil ré-estimé | Test (contrôle min–max) | Direction juste ? |
|---|---|---|---|---|---|
| 1 | 100 | 0–100 | 89,0 | 49,87–56,02 | non |
| 2 | 122 | 22–122 | 86,0 | 61,53–66,97 | non |
| 3 | 144 | 44–144 | 64,0 | 71,55–79,66 | oui |
| 4 | 166 | 66–166 | 42,0 | 84,27–90,02 | non |
| 5 | 188 | 88–188 | 20,0 | 93,10–99,84 | non |

La série **décline de façon monotone** (89 → 20) pendant que la fenêtre glisse vers le haut de la rampe de contrôle. Le seuil ré-estimé dépend fortement de la position de la fenêtre.

### 2.2 Autres jeux synthétiques

| Jeu | t0_reestimated | t0_std | Direction |
|---|---|---|---|
| D_2000 (n=2000, fenêtre 1000) | [94,6 ; 72,7 ; 48,0 ; 23,3 ; 3,2] | 36,74 | 80 % |
| D_const (contrôle constant) | [50,5 ; 50,5 ; 50,5 ; 50,5 ; 50,5] | 0,0 | 80 % |
| D_nan (n=199) | [96,0 ; 86,0 ; 64,0 ; 42,0 ; 20,0] | 31,22 | 20 % |
| D_seed7_horizon5 | [89,0 ; 85,0 ; 61,0 ; 37,0 ; 13,0] | 32,25 | 60 % |
| C_all Flux1 | [62,0 ; 47,0 ; 24,77 ; 61,0 ; 35,0] | 16,23 | 20 % |
| C_all Flux2 | [57,0 ; 18,0 ; 72,0 ; 34,0 ; 39,0] | 20,94 | 0 % |
| C_all Target | [52,0 ; 34,0 ; 41,0 ; 54,0 ; 34,0] | 9,59 | 20 % |
| C_multi Flux1 | [83,0 ; 47,0 ; 24,77 ; 48,0 ; 18,0] | 25,45 | 60 % |

### 2.3 Ising fast (960 points, fenêtre 480)

| Contrôle | t0_reestimated | t0_std | Direction |
|---|---|---|---|
| fliprate / flip | [66,35 ; 41,98 ; 17,60 ; 35,94 ; 11,56] | 21,70 | 60 % |
| energy | [73,13 ; 48,75 ; 79,17 ; 75,31 ; 25,63] | 22,81 | 20 % |
| magnetization | [98,96 ; 66,15 ; 99,27 ; 96,56 ; 22,40] | 33,39 | 40 % |
| localvar | [99,27 ; 87,81 ; 64,48 ; 40,10 ; 16,35] | 34,00 | 20 % |
| susceptibility | [1,35 ; 1,35 ; 87,49 ; 98,65 ; 98,65] | 51,45 | 20 % |

Formes variées : dérive monotone (localvar), saut bimodal (susceptibility : 1,35 puis ~98), dispersion sans tendance (energy, magnetization). Toutes FAIL (> 20) sauf aucune.

## 3. Lecture

1. **Le seul PASS du check sur 45 sorties est un contrôle constant** (D_const, t0_std = 0,0) — un cas dégénéré. Tous les contrôles réels échouent. C'est une signature de calibration suspecte : un check qui ne passe que quand il n'y a rien à mesurer.
2. **Le check compare des seuils ré-estimés dans des fenêtres différentes** (positions différentes sur la rampe) avec une barre fixe (≤ 10). Sur le jeu de base, la dérive monotone 89 → 20 suffit à elle seule à faire échouer le check, alors que le seuil global T_0 (49,42 %) est identique d'un mode à l'autre.
3. **La précision directionnelle est basse** (20 % sur le jeu de base, 0 % sur Flux2) : le pronostic walk-forward se trompe de sens 4 fois sur 5 sur le jeu de base. C'est une deuxième mesure d'instabilité, indépendante du t0_std.
4. **Aucune référence v5.4.0** : on ne peut pas dire si 29,4 est « normal » pour cet instrument — le diagnostic n'existait pas. Le FRAGILE systématique est donc une propriété du nouveau diagnostic autant que des données.

## 4. Questions ouvertes (à trancher)

- **(a)** La mécanique exacte du `train_threshold` ré-estimé par fenêtre — lire le code (`adaptive_walk_forward` dans le fichier v5.9.0f, copie seulement) pour dire si la dérive 89 → 20 est attendue pour une rampe de contrôle, ou si elle révèle une vraie instabilité de la cascade.
- **(b)** La barre (≤ 10 PASS / > 20 FAIL) est-elle calibrée sur quoi que ce soit ? Aucune justification trouvée dans les sorties. Un nul permuté donnerait la référence : si le nul échoue pareil, le check ne sépare rien.
- **(c)** Le mode `--l7b-full` (graine/fenêtre/mélange, 4 re-runs) changerait-il le verdict ? Non mesuré — coût ~3–4× un run.
- **(d)** La clé `walk_forward` (expansif historique) annoncée par la note est absente : documentation ou code ?

## 5. Ce que cela ne veut pas dire

Ce n'est pas un verdict sur l'instrument. Un seul audit, en mode light, non calibré, sans référence antérieure, ne déclare rien sur le pipeline entier. Il signale une question de mesure — la calibration du check — pas une propriété établie du système.

## 6. Mécanique lue dans le code (8 nov. ~14h35, lecture seule, original intact)

Fonctions lues dans `universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py` (aucune modification) :

- **`adaptive_walk_forward_validation` (ligne 9811)** : fenêtre = 50 % de n (100 points pour n=200, 480 pour n=960), horizon 12 (défaut 15 en signature, 12 dans les sorties), 5 origines régulièrement espacées. À chaque fold, le train est la fenêtre [t−W, t) et **l'axe de progression est recalculé sur cette fenêtre seulement** : `compute_time_aligned_progress(c_tr)` puis `compute_5_threshold_cascade(p_tr, z_tr)`. Le T_0 de chaque fold est donc exprimé **dans les coordonnées locales de sa fenêtre**, pas dans celles de la série entière.
- **`compute_time_aligned_progress` (ligne 9246)** : pour un contrôle monotone (|Spearman| ≥ 0,20), la progression est le **rang percentile dans la série passée en argument**, 0–100 (inversée si décroissant). Pour un flux non monotone (|Spearman| < 0,20), c'est l'action cumulative |dJ|, 0–100 dans la fenêtre. Dans les deux cas, l'axe est **renormalisé par fenêtre**.
- **Règle L7b (ligne 10783+)** : walk-forward PASS si t0_std ≤ 10 ; FAIL si 10 < t0_std ≤ 20 (« moyennement variable ») et si t0_std > 20 (« très variable »). Seul l'intervalle ≤ 10 passe. Horizon : PASS si stabilité min ≥ 0,80 ; FAIL si < 0,50 et si 0,50–0,80. Cohérence : FAIL si désaccord ou pénalité ≥ 0,20. **Verdict : un seul check FAIL → FRAGILE** ; un INDETERMINE (sans FAIL) → INDÉTERMINÉ ; tous PASS → ROBUSTE. Le diagnostic lui-même définit `t0_stable` à t0_std ≤ 5,0 (ligne 9931) — encore plus strict.
- **Dérive 89 → 20 expliquée géométriquement.** Sur le jeu de base, le seuil global est T_0 = 49,42 %, soit une transition vers le point ~99 sur 200. Fenêtres : [0,100), [22,122), [44,144), [66,166), [88,188). Position locale attendue de la transition dans chaque fenêtre : ~99 %, 77 %, 55 %, 33 %, 11 %. Mesuré : 89, 86, 64, 42, 20 — même déclin monotone, décalé d'environ +9 points (lissage σ=3,0 + estimation Monte Carlo de la cascade). **La dérive est la signature géométrique attendue d'une transition unique vue par des fenêtres glissantes à axe renormalisé** : quand la fenêtre passe la transition, le seuil local glisse du haut vers le bas de la fenêtre. Le décalage de ~+9 n'est pas dérivé exactement — la forme monotone, elle, est expliquée.
- **Conséquence :** tel qu'implémenté, le check walk-forward échoue sur tout système à transition unique localisée sur une rampe — précisément ce que le pipeline est construit pour détecter — et ne passe que sur un contrôle sans transition (D_const, std 0,0). Ce n'est pas une mesure de fragilité de l'instrument, c'est une propriété de la construction du check. La confirmation définitive exigerait un nul (contrôle permuté : même dérive attendue si c'est la géométrie qui la produit) ou une série synthétique avec transition à une autre position (la dérive doit suivre la position).
- Pour les contrôles Ising (flux non monotones), l'axe est l'action cumulative par fenêtre : même logique locale ; le saut bimodal de susceptibility ([1,35 ; 1,35 ; 87,49 ; 98,65 ; 98,65]) correspond aux fenêtres qui enjambent le pic de susceptibilité.
