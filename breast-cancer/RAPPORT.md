# Breast Cancer Dataset (Kaggle yasserh) x pipeline v3.3-H1 — Rapport des 32 contrôles

Protocole gelé avant les runs : `PROTOCOLE.md` (25 oct. 2026 ~21h50 HAE).
Pipeline uploadé ce jour-là, tel quel : mode stable, w_size 80, cohen_d, graine 42,
HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse
les 31 autres colonnes numériques. Source : `data/breast-cancer.csv`, 569 lignes,
32 colonnes, 0 valeur manquante ; fichier de travail `data/breast-cancer_pipeline.csv`
ajoute seulement `diagnosis_encoded` (B = 0, M = 1). Aucun seuil attendu pré-enregistré :
lecture descriptive seulement, pas de vérité terrain, aucune conclusion médicale.

## Verdict en une ligne

**32/32 runs terminés, 0 échec(s)** (durée totale des runs OK : 16605.7 s, ~519 s par run). Stabilités (critère du pipeline) : MODERATELY STABLE = 12, UNSTABLE = 20.
Aucun run VERY STABLE selon le critère du pipeline.
Les runs UNSTABLE ne doivent pas être lus seuls.

## Synthèse par contrôle

| contrôle | seuil MC % | défaut % | MC−défaut | stabilité | ± | score MC | scan max | valeur au seuil (médiane) | durée s |
|---|---:|---:|---:|---|---:|---:|---:|---|---:|
| id | 71.28 | 7.84 | +63.44 | UNSTABLE | 29.45 | 0.646 | 0.209 | 8711561.0 | 541.8 |
| radius_mean | 84.02 | 84.31 | -0.30 | MODERATELY STABLE | 4.64 | 0.596 | 1.125 | 18.01 | 328.8 |
| texture_mean | 52.92 | 52.16 | +0.76 | UNSTABLE | 8.54 | 0.520 | 0.563 | 19.1 | 550.4 |
| perimeter_mean | 84.21 | 81.57 | +2.64 | MODERATELY STABLE | 4.43 | 0.577 | 1.306 | 118.7 | 543.5 |
| area_mean | 81.21 | 76.86 | +4.35 | MODERATELY STABLE | 3.75 | 0.574 | 1.141 | 930.9 | 562.0 |
| smoothness_mean | 19.37 | 8.24 | +11.14 | UNSTABLE | 8.24 | 0.502 | 0.510 | 0.084 | 544.3 |
| compactness_mean | 76.67 | 80.78 | -4.11 | UNSTABLE | 20.21 | 0.552 | 0.933 | 0.132 | 554.7 |
| concavity_mean | 68.68 | 67.84 | +0.84 | MODERATELY STABLE | 3.79 | 0.552 | 1.131 | 0.109 | 546.4 |
| concave points_mean | 68.68 | 81.96 | -13.28 | UNSTABLE | 6.83 | 0.553 | 1.122 | 0.061 | 560.7 |
| symmetry_mean | 90.73 | 88.24 | +2.49 | UNSTABLE | 24.65 | 0.491 | 0.688 | 0.216 | 540.9 |
| fractal_dimension_mean | 88.98 | 91.37 | -2.39 | UNSTABLE | 5.96 | 0.459 | 0.525 | 0.071 | 525.7 |
| radius_se | 86.39 | 87.45 | -1.06 | MODERATELY STABLE | 4.93 | 0.554 | 0.951 | 0.647 | 545.9 |
| texture_se | 15.47 | 8.63 | +6.84 | UNSTABLE | 6.74 | 0.465 | 0.315 | 0.72 | 517.1 |
| perimeter_se | 80.80 | 92.16 | -11.35 | UNSTABLE | 10.51 | 0.551 | 0.854 | 3.854 | 523.3 |
| area_se | 86.39 | 85.88 | +0.51 | MODERATELY STABLE | 4.22 | 0.563 | 1.118 | 74.85 | 519.3 |
| smoothness_se | 8.02 | 92.16 | -84.14 | UNSTABLE | 30.68 | 0.456 | 0.424 | 0.004 | 534.6 |
| compactness_se | 47.73 | 9.02 | +38.71 | UNSTABLE | 20.50 | 0.515 | 0.783 | 0.02 | 541.5 |
| concavity_se | 44.53 | 37.65 | +6.89 | UNSTABLE | 10.45 | 0.554 | 0.835 | 0.022 | 518.3 |
| concave points_se | 34.77 | 9.02 | +25.75 | MODERATELY STABLE | 3.83 | 0.526 | 0.777 | 0.009 | 517.5 |
| symmetry_se | 97.73 | 17.25 | +80.47 | MODERATELY STABLE | 4.01 | 0.529 | 0.720 | 0.042 | 485.3 |
| fractal_dimension_se | 35.21 | 38.43 | -3.23 | UNSTABLE | 14.35 | 0.535 | 0.616 | 0.003 | 560.0 |
| radius_worst | 78.19 | 81.96 | -3.78 | UNSTABLE | 8.48 | 0.606 | 1.223 | 19.85 | 550.4 |
| texture_worst | 44.28 | 34.51 | +9.77 | UNSTABLE | 6.38 | 0.501 | 0.532 | 24.54 | 537.2 |
| perimeter_worst | 83.21 | 78.82 | +4.38 | UNSTABLE | 6.06 | 0.600 | 1.339 | 142.0 | 541.3 |
| area_worst | 85.71 | 81.57 | +4.15 | MODERATELY STABLE | 4.88 | 0.579 | 1.343 | 1535.0 | 501.7 |
| smoothness_worst | 16.01 | 12.55 | +3.46 | UNSTABLE | 37.00 | 0.493 | 0.507 | 0.109 | 522.5 |
| compactness_worst | 76.41 | 78.43 | -2.02 | UNSTABLE | 10.74 | 0.539 | 0.874 | 0.345 | 520.6 |
| concavity_worst | 73.93 | 63.14 | +10.80 | UNSTABLE | 6.43 | 0.548 | 1.059 | 0.379 | 541.5 |
| concave points_worst | 69.72 | 68.24 | +1.49 | MODERATELY STABLE | 4.61 | 0.542 | 1.194 | 0.149 | 507.1 |
| symmetry_worst | 93.06 | 92.16 | +0.90 | MODERATELY STABLE | 5.90 | 0.531 | 0.758 | 0.377 | 523.2 |
| fractal_dimension_worst | 80.83 | 84.31 | -3.48 | UNSTABLE | 8.11 | 0.515 | 0.692 | 0.096 | 527.4 |
| diagnosis_encoded | 58.53 | 56.47 | +2.06 | MODERATELY STABLE | 3.78 | 0.575 | 1.050 | 0.0 | 270.8 |

## Stabilité : ce qui tient, ce qui ne tient pas

- **MODERATELY STABLE (12)** : radius_mean 84.02 % (±4.64), perimeter_mean 84.21 % (±4.43), area_mean 81.21 % (±3.75), concavity_mean 68.68 % (±3.79), radius_se 86.39 % (±4.93), area_se 86.39 % (±4.22), concave points_se 34.77 % (±3.83), symmetry_se 97.73 % (±4.01), area_worst 85.71 % (±4.88), concave points_worst 69.72 % (±4.61), symmetry_worst 93.06 % (±5.90), diagnosis_encoded 58.53 % (±3.78).
- **UNSTABLE (20)** : id 71.28 % (±29.45), texture_mean 52.92 % (±8.54), smoothness_mean 19.37 % (±8.24), compactness_mean 76.67 % (±20.21), concave points_mean 68.68 % (±6.83), symmetry_mean 90.73 % (±24.65), fractal_dimension_mean 88.98 % (±5.96), texture_se 15.47 % (±6.74), perimeter_se 80.80 % (±10.51), smoothness_se 8.02 % (±30.68), compactness_se 47.73 % (±20.50), concavity_se 44.53 % (±10.45), fractal_dimension_se 35.21 % (±14.35), radius_worst 78.19 % (±8.48), texture_worst 44.28 % (±6.38), perimeter_worst 83.21 % (±6.06), smoothness_worst 16.01 % (±37.00), compactness_worst 76.41 % (±10.74), concavity_worst 73.93 % (±6.43), fractal_dimension_worst 80.83 % (±8.11).

## Accord seuil MC / moyenne bootstrap (lecture critique de la stabilité)

La note de stabilité du pipeline repose sur l’écart-type bootstrap, pas sur l’accord
entre le seuil MC et la moyenne bootstrap. Les runs suivants ont un écart > 15 points :
- id : MC 71.28 %, moyenne bootstrap 54.36 %, écart 16.9 pts, note UNSTABLE (±29.45).
- smoothness_se : MC 8.02 %, moyenne bootstrap 71.72 %, écart 63.7 pts, note UNSTABLE (±30.68).
- compactness_se : MC 47.73 %, moyenne bootstrap 29.03 %, écart 18.7 pts, note UNSTABLE (±20.50).
- concavity_se : MC 44.53 %, moyenne bootstrap 27.01 %, écart 17.5 pts, note UNSTABLE (±10.45).
- concave points_se : MC 34.77 %, moyenne bootstrap 16.67 %, écart 18.1 pts, note MODERATELY STABLE (±3.83).
- symmetry_se : MC 97.73 %, moyenne bootstrap 17.60 %, écart 80.1 pts, note MODERATELY STABLE (±4.01).
- smoothness_worst : MC 16.01 %, moyenne bootstrap 47.55 %, écart 31.5 pts, note UNSTABLE (±37.00).

Cas pièges : `symmetry_se` est noté MODERATELY STABLE (±4,01) alors que sa moyenne bootstrap
(17,60 %) est à 80 points du MC (97,73 %) ; `concave points_se` est noté MODERATELY STABLE
(±3,83) avec un écart de 18,1 points (MC 34,77 %, moyenne 16,67 %). À l’inverse, les runs où
MC et moyenne bootstrap s’accordent à moins de 7 points ET avec un écart-type < 6 sont :
radius_mean, perimeter_mean, area_mean, concavity_mean, radius_se, area_se, area_worst,
concave points_worst, symmetry_worst, diagnosis_encoded.

## Seuils propres par flux (top 10 de tout le banc)

- contrôle perimeter_mean : flux area_mean 83.21 % (score 3.879).
- contrôle area_worst : flux radius_worst 83.96 % (score 3.750).
- contrôle perimeter_mean : flux radius_mean 83.21 % (score 3.714).
- contrôle perimeter_worst : flux radius_worst 83.21 % (score 3.671).
- contrôle perimeter_worst : flux area_worst 81.95 % (score 3.629).
- contrôle area_worst : flux perimeter_worst 81.95 % (score 3.591).
- contrôle perimeter_mean : flux radius_worst 83.96 % (score 3.359).
- contrôle perimeter_mean : flux perimeter_worst 83.96 % (score 3.293).
- contrôle perimeter_worst : flux perimeter_mean 81.45 % (score 3.293).
- contrôle area_worst : flux perimeter_mean 77.19 % (score 3.273).

En tant que flux (moyenne sur les 31 runs où la colonne est flux) :
- diagnosis_encoded : moyenne 1.459, max 3.215.
- concave points_mean : moyenne 1.412, max 2.714.
- radius_worst : moyenne 1.392, max 3.750.
- perimeter_worst : moyenne 1.392, max 3.591.
- concave points_worst : moyenne 1.388, max 2.576.
- perimeter_mean : moyenne 1.327, max 3.293.
- concavity_mean : moyenne 1.319, max 2.364.
- radius_mean : moyenne 1.310, max 3.714.
- area_worst : moyenne 1.296, max 3.629.
- area_mean : moyenne 1.285, max 3.879.
- compactness_mean : moyenne 1.198, max 2.058.
- concavity_worst : moyenne 1.178, max 2.163.
- compactness_worst : moyenne 1.074, max 2.281.
- area_se : moyenne 1.061, max 2.397.
- radius_se : moyenne 1.056, max 2.462.
- perimeter_se : moyenne 1.035, max 2.306.
- concave points_se : moyenne 0.946, max 1.549.
- compactness_se : moyenne 0.862, max 1.687.
- concavity_se : moyenne 0.846, max 1.872.
- smoothness_mean : moyenne 0.794, max 1.595.
- smoothness_worst : moyenne 0.782, max 1.369.
- symmetry_mean : moyenne 0.768, max 1.534.
- fractal_dimension_worst : moyenne 0.751, max 1.603.
- fractal_dimension_mean : moyenne 0.726, max 1.695.
- symmetry_worst : moyenne 0.694, max 1.602.
- texture_worst : moyenne 0.673, max 2.245.
- texture_mean : moyenne 0.661, max 2.201.
- fractal_dimension_se : moyenne 0.643, max 1.644.
- smoothness_se : moyenne 0.563, max 1.216.
- symmetry_se : moyenne 0.530, max 0.901.
- texture_se : moyenne 0.515, max 1.214.
- id : moyenne 0.228, max 0.372.

## Seuils propres par flux (top 3 par run)

| contrôle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| id (71.28 %) | texture_mean 80.26 % (0.534) | texture_worst 84.62 % (0.465) | diagnosis_encoded 18.72 % (0.412) |
| radius_mean (84.02 %) | area_mean 78.62 % (3.225) | perimeter_mean 78.62 % (3.216) | radius_worst 77.54 % (2.885) |
| texture_mean (52.92 %) | texture_worst 24.84 % (2.245) | diagnosis_encoded 49.89 % (1.009) | perimeter_worst 25.92 % (0.811) |
| perimeter_mean (84.21 %) | area_mean 83.21 % (3.879) | radius_mean 83.21 % (3.714) | radius_worst 83.96 % (3.359) |
| area_mean (81.21 %) | radius_mean 78.62 % (3.237) | perimeter_mean 78.62 % (3.182) | radius_worst 81.21 % (2.968) |
| smoothness_mean (19.37 %) | smoothness_worst 23.30 % (1.369) | compactness_mean 19.37 % (1.056) | concave points_mean 19.37 % (0.938) |
| compactness_mean (76.67 %) | concavity_mean 77.97 % (1.980) | compactness_worst 54.64 % (1.882) | concave points_mean 80.78 % (1.807) |
| concavity_mean (68.68 %) | concave points_mean 72.14 % (2.523) | concave points_worst 72.14 % (2.324) | concavity_worst 59.40 % (2.163) |
| concave points_mean (68.68 %) | concave points_worst 68.68 % (2.576) | diagnosis_encoded 70.63 % (2.368) | concavity_mean 81.21 % (2.364) |
| symmetry_mean (90.73 %) | symmetry_worst 5.76 % (1.602) | compactness_mean 90.48 % (1.380) | concavity_mean 84.96 % (1.133) |
| fractal_dimension_mean (88.98 %) | fractal_dimension_worst 81.64 % (1.431) | fractal_dimension_se 81.43 % (1.130) | smoothness_mean 35.64 % (1.107) |
| radius_se (86.39 %) | area_se 81.64 % (2.397) | perimeter_se 81.64 % (2.306) | radius_worst 86.39 % (1.768) |
| texture_se (15.47 %) | texture_worst 14.93 % (1.086) | texture_mean 14.93 % (0.918) | smoothness_se 86.67 % (0.681) |
| perimeter_se (80.80 %) | radius_se 84.81 % (2.291) | area_se 85.39 % (2.020) | concave points_mean 85.67 % (1.576) |
| area_se (86.39 %) | radius_se 83.59 % (2.462) | radius_worst 86.39 % (2.436) | perimeter_worst 86.39 % (2.400) |
| smoothness_se (8.02 %) | texture_se 94.74 % (1.174) | smoothness_worst 6.27 % (0.987) | symmetry_se 82.96 % (0.847) |
| compactness_se (47.73 %) | concavity_se 69.33 % (1.872) | fractal_dimension_se 83.59 % (1.644) | compactness_mean 34.77 % (1.623) |
| concavity_se (44.53 %) | compactness_se 62.40 % (1.687) | concavity_mean 44.53 % (1.619) | concavity_worst 26.13 % (1.614) |
| concave points_se (34.77 %) | concavity_se 16.38 % (1.367) | concavity_mean 16.38 % (1.337) | concave points_worst 16.95 % (1.335) |
| symmetry_se (97.73 %) | symmetry_mean 97.73 % (1.534) | symmetry_worst 97.73 % (1.215) | texture_se 93.86 % (1.214) |
| fractal_dimension_se (35.21 %) | compactness_se 70.41 % (1.591) | fractal_dimension_mean 89.63 % (1.367) | fractal_dimension_worst 9.72 % (1.349) |
| radius_worst (78.19 %) | area_worst 78.62 % (3.211) | perimeter_worst 78.62 % (3.155) | perimeter_mean 81.64 % (2.857) |
| texture_worst (44.28 %) | texture_mean 26.57 % (2.201) | diagnosis_encoded 44.28 % (1.061) | perimeter_worst 44.28 % (0.854) |
| perimeter_worst (83.21 %) | radius_worst 83.21 % (3.671) | area_worst 81.95 % (3.629) | perimeter_mean 81.45 % (3.293) |
| area_worst (85.71 %) | radius_worst 83.96 % (3.750) | perimeter_worst 81.95 % (3.591) | perimeter_mean 77.19 % (3.273) |
| smoothness_worst (16.01 %) | smoothness_mean 17.98 % (1.595) | concave points_worst 16.01 % (0.977) | fractal_dimension_worst 83.43 % (0.939) |
| compactness_worst (76.41 %) | concavity_worst 71.79 % (2.022) | compactness_mean 78.21 % (1.833) | concave points_worst 76.41 % (1.824) |
| concavity_worst (73.93 %) | concave points_worst 72.93 % (2.475) | concavity_mean 80.45 % (2.284) | compactness_worst 83.96 % (2.281) |
| concave points_worst (69.72 %) | diagnosis_encoded 70.00 % (3.062) | concave points_mean 69.72 % (2.714) | concavity_mean 66.94 % (2.270) |
| symmetry_worst (93.06 %) | compactness_worst 93.06 % (1.572) | symmetry_mean 30.00 % (1.447) | concave points_worst 91.67 % (1.406) |
| fractal_dimension_worst (80.83 %) | compactness_worst 80.83 % (1.894) | fractal_dimension_mean 84.44 % (1.695) | compactness_mean 89.72 % (1.621) |
| diagnosis_encoded (58.53 %) | concave points_worst 58.53 % (2.139) | concave points_mean 58.53 % (2.023) | perimeter_worst 58.53 % (1.997) |

Détail complet des 992 seuils propres (32 × 31) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- area_mean : Q1_Calme_vs_Chaos = 0.792, Q2_Tension_Seuil = 1.447, Q3_Agressivite = 0.792, Q4_Persistence = 0.492, Q5_Active_Reactive = 8.640, Q5_Actif_Receptif = 8.640
- area_se : Q1_Calme_vs_Chaos = 1.012, Q2_Tension_Seuil = 2.090, Q3_Agressivite = 1.012, Q4_Persistence = 0.300, Q5_Active_Reactive = 5.127, Q5_Actif_Receptif = 5.127
- area_worst : Q1_Calme_vs_Chaos = 0.618, Q2_Tension_Seuil = 2.760, Q3_Agressivite = 0.618, Q4_Persistence = 0.421, Q5_Active_Reactive = 8.596, Q5_Actif_Receptif = 8.596
- compactness_mean : Q1_Calme_vs_Chaos = 0.628, Q2_Tension_Seuil = 2.266, Q3_Agressivite = 0.628, Q4_Persistence = 0.286, Q5_Active_Reactive = 6.314, Q5_Actif_Receptif = 6.314
- compactness_se : Q1_Calme_vs_Chaos = 0.776, Q2_Tension_Seuil = 2.272, Q3_Agressivite = 0.776, Q4_Persistence = 0.244, Q5_Active_Reactive = 6.229, Q5_Actif_Receptif = 6.229
- compactness_worst : Q1_Calme_vs_Chaos = 0.607, Q2_Tension_Seuil = 2.758, Q3_Agressivite = 0.607, Q4_Persistence = 0.276, Q5_Active_Reactive = 5.948, Q5_Actif_Receptif = 5.948
- concave points_mean : Q1_Calme_vs_Chaos = 0.744, Q2_Tension_Seuil = 2.292, Q3_Agressivite = 0.744, Q4_Persistence = 0.304, Q5_Active_Reactive = 5.819, Q5_Actif_Receptif = 5.819
- concave points_se : Q1_Calme_vs_Chaos = 1.132, Q2_Tension_Seuil = 1.718, Q3_Agressivite = 1.132, Q4_Persistence = 0.295, Q5_Active_Reactive = 5.695, Q5_Actif_Receptif = 5.695
- concave points_worst : Q1_Calme_vs_Chaos = 0.456, Q2_Tension_Seuil = 1.258, Q3_Agressivite = 0.456, Q4_Persistence = 0.274, Q5_Active_Reactive = 6.167, Q5_Actif_Receptif = 6.167
- concavity_mean : Q1_Calme_vs_Chaos = 0.588, Q2_Tension_Seuil = 1.928, Q3_Agressivite = 0.588, Q4_Persistence = 0.330, Q5_Active_Reactive = 5.356, Q5_Actif_Receptif = 5.356
- concavity_se : Q1_Calme_vs_Chaos = 1.116, Q2_Tension_Seuil = 2.146, Q3_Agressivite = 1.116, Q4_Persistence = 0.304, Q5_Active_Reactive = 5.595, Q5_Actif_Receptif = 5.595
- concavity_worst : Q1_Calme_vs_Chaos = 0.536, Q2_Tension_Seuil = 1.882, Q3_Agressivite = 0.536, Q4_Persistence = 0.277, Q5_Active_Reactive = 6.328, Q5_Actif_Receptif = 6.328
- diagnosis_encoded : Q1_Calme_vs_Chaos = 0.952, Q2_Tension_Seuil = 2.475, Q3_Agressivite = 0.952, Q4_Persistence = 0.263, Q5_Active_Reactive = 8.919, Q5_Actif_Receptif = 8.919
- fractal_dimension_mean : Q1_Calme_vs_Chaos = 0.612, Q2_Tension_Seuil = 3.242, Q3_Agressivite = 0.612, Q4_Persistence = 0.209, Q5_Active_Reactive = 6.134, Q5_Actif_Receptif = 6.134
- fractal_dimension_se : Q1_Calme_vs_Chaos = 0.725, Q2_Tension_Seuil = 1.512, Q3_Agressivite = 0.725, Q4_Persistence = 0.200, Q5_Active_Reactive = 6.447, Q5_Actif_Receptif = 6.447
- fractal_dimension_worst : Q1_Calme_vs_Chaos = 0.504, Q2_Tension_Seuil = 1.522, Q3_Agressivite = 0.504, Q4_Persistence = 0.231, Q5_Active_Reactive = 8.402, Q5_Actif_Receptif = 8.402
- id : Q1_Calme_vs_Chaos = 0.840, Q2_Tension_Seuil = 2.195, Q3_Agressivite = 0.840, Q4_Persistence = 0.212, Q5_Active_Reactive = 4.185, Q5_Actif_Receptif = 4.185
- perimeter_mean : Q1_Calme_vs_Chaos = 0.486, Q2_Tension_Seuil = 3.287, Q3_Agressivite = 0.486, Q4_Persistence = 0.431, Q5_Active_Reactive = 8.786, Q5_Actif_Receptif = 8.786
- perimeter_se : Q1_Calme_vs_Chaos = 0.906, Q2_Tension_Seuil = 1.648, Q3_Agressivite = 0.906, Q4_Persistence = 0.283, Q5_Active_Reactive = 5.070, Q5_Actif_Receptif = 5.070
- perimeter_worst : Q1_Calme_vs_Chaos = 0.686, Q2_Tension_Seuil = 3.502, Q3_Agressivite = 0.686, Q4_Persistence = 0.404, Q5_Active_Reactive = 6.768, Q5_Actif_Receptif = 6.768
- radius_mean : Q1_Calme_vs_Chaos = 0.714, Q2_Tension_Seuil = 1.836, Q3_Agressivite = 0.714, Q4_Persistence = 0.499, Q5_Active_Reactive = 8.666, Q5_Actif_Receptif = 8.666
- radius_se : Q1_Calme_vs_Chaos = 0.862, Q2_Tension_Seuil = 2.082, Q3_Agressivite = 0.862, Q4_Persistence = 0.291, Q5_Active_Reactive = 5.937, Q5_Actif_Receptif = 5.937
- radius_worst : Q1_Calme_vs_Chaos = 0.845, Q2_Tension_Seuil = 1.418, Q3_Agressivite = 0.845, Q4_Persistence = 0.506, Q5_Active_Reactive = 6.670, Q5_Actif_Receptif = 6.670
- smoothness_mean : Q1_Calme_vs_Chaos = 1.100, Q2_Tension_Seuil = 4.576, Q3_Agressivite = 1.100, Q4_Persistence = 0.241, Q5_Active_Reactive = 8.052, Q5_Actif_Receptif = 8.052
- smoothness_se : Q1_Calme_vs_Chaos = 0.465, Q2_Tension_Seuil = 2.121, Q3_Agressivite = 0.465, Q4_Persistence = 0.252, Q5_Active_Reactive = 8.905, Q5_Actif_Receptif = 8.905
- smoothness_worst : Q1_Calme_vs_Chaos = 0.846, Q2_Tension_Seuil = 4.492, Q3_Agressivite = 0.846, Q4_Persistence = 0.208, Q5_Active_Reactive = 7.057, Q5_Actif_Receptif = 7.057
- symmetry_mean : Q1_Calme_vs_Chaos = 0.587, Q2_Tension_Seuil = 1.807, Q3_Agressivite = 0.587, Q4_Persistence = 0.231, Q5_Active_Reactive = 8.790, Q5_Actif_Receptif = 8.790
- symmetry_se : Q1_Calme_vs_Chaos = 0.629, Q2_Tension_Seuil = 0.000, Q3_Agressivite = 0.629, Q4_Persistence = 0.496, Q5_Active_Reactive = 10.387, Q5_Actif_Receptif = 10.387
- symmetry_worst : Q1_Calme_vs_Chaos = 0.522, Q2_Tension_Seuil = 1.836, Q3_Agressivite = 0.522, Q4_Persistence = 0.244, Q5_Active_Reactive = 7.893, Q5_Actif_Receptif = 7.893
- texture_mean : Q1_Calme_vs_Chaos = 0.680, Q2_Tension_Seuil = 2.628, Q3_Agressivite = 0.680, Q4_Persistence = 0.191, Q5_Active_Reactive = 5.926, Q5_Actif_Receptif = 5.926
- texture_se : Q1_Calme_vs_Chaos = 0.649, Q2_Tension_Seuil = 3.810, Q3_Agressivite = 0.649, Q4_Persistence = 0.155, Q5_Active_Reactive = 7.632, Q5_Actif_Receptif = 7.632
- texture_worst : Q1_Calme_vs_Chaos = 0.731, Q2_Tension_Seuil = 2.303, Q3_Agressivite = 0.731, Q4_Persistence = 0.193, Q5_Active_Reactive = 7.296, Q5_Actif_Receptif = 7.296

## Dérivées F1/F2 post-seuil, flux « Tous »

estimateur                  DFA  Higuchi   Hurst    Katz  SampleEn
controle                                                          
area_mean               -0.0338   0.0019  0.0115  0.0022    0.0620
area_se                  0.0028   0.0011  0.0103  0.0034    0.1153
area_worst              -0.0109  -0.0016  0.0081  0.0028    0.0574
compactness_mean        -0.0092   0.0003  0.0091  0.0022    0.0475
compactness_se          -0.0002   0.0003  0.0016  0.0005    0.0121
compactness_worst       -0.0056  -0.0005  0.0081  0.0023    0.0532
concave points_mean     -0.0058  -0.0021  0.0060 -0.0002    0.0261
concave points_se       -0.0011   0.0000  0.0019  0.0005    0.0111
concave points_worst    -0.0091  -0.0043  0.0061 -0.0003    0.0231
concavity_mean          -0.0023   0.0000  0.0045  0.0010    0.0290
concavity_se            -0.0004   0.0004  0.0020  0.0006    0.0109
concavity_worst         -0.0060  -0.0009  0.0047  0.0015    0.0319
diagnosis_encoded        0.0161   0.0013 -0.0101 -0.0000    0.0089
fractal_dimension_mean  -0.0062   0.0016  0.0160  0.0040    0.1171
fractal_dimension_se    -0.0036  -0.0009  0.0037  0.0004    0.0081
fractal_dimension_worst -0.0112  -0.0016  0.0073  0.0022    0.0374
id                      -0.0045   0.0005  0.0069  0.0015    0.0334
perimeter_mean          -0.0067  -0.0046  0.0110  0.0004    0.0757
perimeter_se            -0.0016  -0.0000  0.0106  0.0023    0.0696
perimeter_worst         -0.0069  -0.0003  0.0150  0.0031    0.0626
radius_mean             -0.0057   0.0024  0.0116  0.0027    0.0818
radius_se               -0.0017   0.0009  0.0051  0.0037    0.1039
radius_worst            -0.0046  -0.0035  0.0067 -0.0002    0.0424
smoothness_mean         -0.0008  -0.0000  0.0012  0.0004    0.0050
smoothness_se           -0.0002  -0.0002  0.0006  0.0001    0.0017
smoothness_worst        -0.0008   0.0001  0.0017  0.0004    0.0056
symmetry_mean           -0.0136   0.0008  0.0158  0.0084    0.1857
symmetry_se             -0.0188  -0.0044  0.0088  0.0018   -0.0238
symmetry_worst           0.0023  -0.0003  0.0064  0.0073    0.1836
texture_mean            -0.0040  -0.0009  0.0045  0.0008    0.0178
texture_se              -0.0013   0.0000  0.0015  0.0002    0.0057
texture_worst           -0.0018  -0.0000  0.0024  0.0006    0.0113

Détail complet (5120 lignes) : `tous_F1F2.csv`.

## Réserves (gelées avant les runs, rappelées ici)

- Données transversales (569 cas, pas une série temporelle) : le contrôle est un axe de rang, pas un temps.
- `id` est un identifiant, pas une mesure.
- `diagnosis_encoded` est binaire : un seuil entre les deux paliers de rang sépare les mêmes deux groupes B/M.
- Aucune conclusion médicale, aucun seuil clinique ne découle de ces mesures du pipeline.

## Fichiers livrés

- `PROTOCOLE.md` — protocole gelé avant les runs.
- `synthese_runs.csv` — une ligne par contrôle (seuils, stabilité, scan, valeur au seuil).
- `tous_seuils_par_flux.csv` — les 992 seuils propres par flux.
- `tous_F1F2.csv` — dérivées F1/F2 post-seuil, tous runs.
- `plateaux_controles.csv` — paliers de rang des contrôles.
- `results/ctrl_<colonne>/` — sorties complètes du pipeline par run.
- `breast_cancer_32_controles_resultats.zip` — archive de l’ensemble ci-dessus + données.

