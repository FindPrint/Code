# Mushroom Classification × pipeline Tlog v3.4-H3 — Rapport complet

**Protocole gelé avant tout run :** `PROTOCOLE.md` (26 oct. 2026). Données : Kaggle `uciml/mushroom-classification`, zip SHA-256 `4e688b…`, CSV `mushrooms.csv` SHA-256 `f0284c…`, fichier de travail `mushrooms_pipeline.csv` SHA-256 `fa6e5c…` (8 124 lignes × 23 colonnes, 0 doublon exact). Pipeline : `Tlog_v3_4_harmonic_v3.py` SHA-256 `81092eb6…` (v3.4-H3 : scan rapide vérifié bit-identique, repli Monte Carlo journalisé, F1/F2 avant ET après seuil). Paramètres : mode stable, w_size initial 80, test cohen_d, graine 42, HARMONIC_PROB 0,45, sans triangulation complète, contrôle exclu des 22 flux analysés, ordre des lignes préservé, 2 runs en parallèle, design résumable (un run avec `run_summary.json` est sauté, un run partiel est jeté et relancé de zéro).

## Verdict

- **23 runs, 22 seuils Monte Carlo, 1 échec mesuré pré-enregistré.** Tous les runs sauf veil-type ont `threshold_source = monte_carlo`, 0 avertissement, 0 repli de scan rapide.
- **veil-type est un échec mesuré, pas un seuil :** colonne constante (`p` sur toutes les lignes), MC NaN, défaut NaN, brut NaN, rigide NaN, score 0,0, stabilité UNKNOWN, 2 avertissements enregistrés, durée 1 098 s. Le 52,5 % du diagnostic bruit est une valeur d'urgence, explicitement PAS un seuil détecté. Ce run n'est jamais lu comme un détecteur.
- **Le seuil MC ne suit ni le défaut ni le rigide-1001 de loin :** écart médian |MC − défaut| 13,84 pts (13/22 runs > 5 pts, 10/22 > 20 pts) ; écart médian |MC − brut| 0,0 pt (seuls class 9,75 pts et habitat 16,19 pts > 5 pts) ; écart médian |MC − rigide-1001| 0,24 pt (4/22 > 5 pts, max 7,72 pts). Le traitement (flux bruts vs traités) ne déplace donc presque jamais le seuil, sauf class et habitat.
- **L'étiquette de stabilité ne mesure pas l'accord avec le MC.** Seuls 9/22 runs ont |MC − moyenne bootstrap| ≤ 1 écart-type bootstrap. 7 des 10 VERY STABLE sont hors de leur propre intervalle bootstrap : odor (écart 97,69 pts, moyenne bootstrap 1,83 % ± 0,12 contre MC 99,52 %), gill-attachment (46,06 pts, 96,18 % ± 2,09 contre 50,12 %), veil-color (41,75 pts, 95,25 % ± 1,67 contre 53,50 %), ring-number n'est pas VERY STABLE mais l'écart atteint 46,51 pts. L'étiquette mesure la dispersion du bootstrap (écart-type petit), pas la proximité du MC : un bootstrap serré ailleurs que le MC donne VERY STABLE + grand écart. Ce motif, déjà vu pour odor, est donc général dans ce lot et il est signalé tel quel, sans mécanisme inventé.
- **Scores MC** de 0,465 (cap-surface, stalk-shape) à 0,697 (veil-color). Les plus forts : veil-color 0,697, gill-attachment 0,691, cap-shape 0,679, gill-color 0,671.
- **En tant que flux**, les scores propres moyens les plus élevés : stalk-color-below-ring 1,598, stalk-color-above-ring 1,446, ring-type 1,404, class 1,354, gill-attachment 1,333 ; veil-type 0,000 partout. Le score propre maximal du lot est 11,269 (ring-number comme flux dans le run odor).
- **F1/F2 (flux Tous, 22 runs × 5 estimateurs = 110 lignes, toutes success avant et après) :** 55 changements de signe sur 110. Les plus fortes dérivées post-seuil : ring-type DFA F1 −0,1196, stalk-surface-below-ring SampleEn F1 −0,0300 et Higuchi F1 −0,0277, stalk-color-below-ring Higuchi F1 −0,0228, spore-print-color Higuchi F1 −0,0223. Détail complet par run, estimateur et flux dans `tous_F1F2.csv` et dans le PDF.
- **Q moyens** (moyenne sur les caractéristiques, par run) : médianes Q1 1,129, Q2 1,468, Q3 1,129, Q4 0,329, Q5 13,197. Valeurs extrêmes signalées telles quelles : veil-color Q2 1 035,305, stalk-root Q1/Q3 70,864, ring-type Q2 41,327. Le run class reproduit exactement le pilote v3.3 (Q1 1,511 / Q2 2,836 / Q3 1,511 / Q4 0,247 / Q5 19,859), ce qui valide la chaîne de calcul des Q.
- **Bruit :** tous les runs portent le label « Proxy de variance résiduelle colorée (CSD) — Forte signature de mémoire et de variance », sauf gill-color (« Proxy de variance modéré »).
- **Durées :** 16 287 s cumulées (4,52 h) pour 23 runs, du 26 oct. ~16h32 au 26 oct. 18h56 (temps mural ~2 h 24, 2 en parallèle) ; un redémarrage VM vers 17h10 a interrompu la paire gill-attachment + gill-spacing sans fichier de sortie, relancée de zéro, les 6 runs terminés intacts et sautés ; un redémarrage runtime vers 19h15 n'a touché que la vieille session de lancement, le lot étant déjà terminé.

## Limites d'interprétation (gelées dans le protocole)

- Les codes sont des étiquettes nominales, pas des grandeurs : les seuils sont des coupes de rang sur l'ordre de première apparition (plateaux de rang, voir `plateaux_controles.csv`), jamais des règles de décision comestible/vénéneux.
- Aucune colonne temporelle : aucune lecture causale ou temporelle. Données réelles, lecture descriptive seulement, aucune vérité terrain, aucun seuil critique attendu revendiqué.
- `stalk-root` porte `?` sur 2 480 lignes (30,5 %) : en contrôle, ces lignes sont écartées (5 644 valides) ; en flux, NaN remplacé par la moyenne du flux avant z-score (comportement du pipeline d'origine).

## Tableau principal — seuils par contrôle

| contrôle | MC % | score | w | défaut % | brut MC % | rigide % | stabilité | moy boot % | ± | valides | durée s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| class | 52.75 | 0.548 | 861 | 61.71 | 62.50 | 56.10 | UNSTABLE | 52.73 | 14.78 | 8124 | 684 |
| cap-shape | 71.12 | 0.679 | 4062 | 92.44 | 71.12 | 74.80 | UNSTABLE | 88.02 | 6.39 | 8124 | 1422 |
| cap-surface | 20.00 | 0.465 | 1034 | 85.85 | 21.38 | 20.00 | UNSTABLE | 79.62 | 16.21 | 8124 | 706 |
| cap-color | 99.45 | 0.538 | 42 | 99.27 | 99.45 | 99.40 | UNSTABLE | 88.46 | 9.79 | 8124 | 301 |
| bruises | 52.88 | 0.531 | 1292 | 54.15 | 52.88 | 47.30 | UNSTABLE | 37.98 | 9.17 | 8124 | 911 |
| odor | 99.52 | 0.584 | 13 | 2.44 | 99.52 | 99.50 | VERY STABLE | 1.83 | 0.12 | 8124 | 229 |
| gill-attachment | 50.12 | 0.691 | 1034 | 92.68 | 50.12 | 49.60 | VERY STABLE | 96.18 | 2.09 | 8124 | 743 |
| gill-spacing | 51.00 | 0.551 | 4062 | 91.46 | 51.00 | 43.90 | UNSTABLE | 75.77 | 16.04 | 8124 | 1625 |
| gill-size | 20.62 | 0.497 | 1292 | 61.95 | 20.62 | 15.60 | UNSTABLE | 31.27 | 21.61 | 8124 | 842 |
| gill-color | 98.86 | 0.671 | 100 | 99.27 | 98.86 | 98.60 | UNSTABLE | 96.63 | 6.30 | 8124 | 362 |
| stalk-shape | 44.62 | 0.465 | 861 | 60.49 | 44.62 | 44.60 | UNSTABLE | 42.50 | 15.68 | 8124 | 711 |
| stalk-root | 65.69 | 0.597 | 1995 | 98.05 | 65.69 | 65.90 | UNSTABLE | 86.43 | 27.09 | 5644 | 628 |
| stalk-surface-above-ring | 84.75 | 0.558 | 1034 | 72.93 | 84.75 | 82.50 | VERY STABLE | 77.95 | 2.85 | 8124 | 724 |
| stalk-surface-below-ring | 80.75 | 0.543 | 1034 | 79.27 | 80.75 | 81.00 | VERY STABLE | 82.36 | 2.20 | 8124 | 792 |
| stalk-color-above-ring | 99.52 | 0.645 | 13 | 98.05 | 99.52 | 99.50 | VERY STABLE | 98.08 | 0.21 | 8124 | 186 |
| stalk-color-below-ring | 98.07 | 0.648 | 57 | 98.29 | 98.07 | 98.30 | VERY STABLE | 98.27 | 0.12 | 8124 | 244 |
| veil-type | — | 0.000 | 135 | — | — | — | UNKNOWN | — | — | 8124 | 1098 |
| veil-color | 53.50 | 0.697 | 861 | 93.41 | 53.00 | 53.50 | VERY STABLE | 95.25 | 1.67 | 8124 | 633 |
| ring-number | 46.38 | 0.634 | 4062 | 97.32 | 46.38 | 47.60 | UNSTABLE | 92.89 | 7.33 | 8124 | 1694 |
| ring-type | 88.62 | 0.607 | 861 | 89.02 | 88.62 | 88.60 | VERY STABLE | 86.59 | 1.77 | 8124 | 621 |
| spore-print-color | 98.84 | 0.653 | 149 | 99.02 | 98.84 | 99.00 | VERY STABLE | 98.74 | 0.40 | 8124 | 323 |
| population | 96.54 | 0.567 | 42 | 97.56 | 96.54 | 96.50 | VERY STABLE | 97.10 | 0.86 | 8124 | 254 |
| habitat | 68.12 | 0.512 | 1292 | 2.68 | 84.31 | 60.40 | UNSTABLE | 41.89 | 48.47 | 8124 | 553 |

## Seuils propres par flux — les 3 plus forts par run

| contrôle | flux | seuil propre % | score max |
|---|---|---|---|
| bruises | ring-type | 46.25 | 2.029 |
| bruises | stalk-surface-above-ring | 46.12 | 1.501 |
| bruises | spore-print-color | 70.62 | 1.398 |
| cap-color | stalk-shape | 99.59 | 1.654 |
| cap-color | spore-print-color | 99.45 | 1.326 |
| cap-color | habitat | 99.45 | 1.153 |
| cap-shape | population | 72.88 | 0.432 |
| cap-shape | habitat | 68.25 | 0.309 |
| cap-shape | gill-color | 71.12 | 0.308 |
| cap-surface | stalk-root | 20.00 | 0.925 |
| cap-surface | gill-color | 68.12 | 0.765 |
| cap-surface | spore-print-color | 68.00 | 0.699 |
| class | spore-print-color | 27.75 | 1.686 |
| class | odor | 52.75 | 1.466 |
| class | stalk-surface-above-ring | 50.25 | 1.364 |
| gill-attachment | class | 50.38 | 1.224 |
| gill-attachment | ring-type | 51.50 | 1.040 |
| gill-attachment | stalk-surface-below-ring | 50.12 | 1.005 |
| gill-color | stalk-color-below-ring | 98.86 | 5.526 |
| gill-color | stalk-color-above-ring | 98.73 | 4.725 |
| gill-color | gill-attachment | 99.24 | 3.857 |
| gill-size | gill-color | 19.88 | 1.507 |
| gill-size | class | 24.75 | 1.427 |
| gill-size | spore-print-color | 27.12 | 1.123 |
| gill-spacing | spore-print-color | 51.00 | 0.944 |
| gill-spacing | class | 55.25 | 0.925 |
| gill-spacing | gill-color | 51.00 | 0.866 |
| habitat | spore-print-color | 59.12 | 1.477 |
| habitat | population | 43.00 | 1.393 |
| habitat | gill-color | 90.88 | 1.131 |
| odor | ring-number | 99.52 | 11.269 |
| odor | stalk-color-below-ring | 99.52 | 5.975 |
| odor | ring-type | 99.52 | 5.946 |
| population | habitat | 90.18 | 1.951 |
| population | stalk-shape | 95.85 | 1.769 |
| population | stalk-color-below-ring | 95.85 | 1.638 |
| ring-number | class | 47.12 | 0.911 |
| ring-number | spore-print-color | 46.25 | 0.805 |
| ring-number | gill-size | 49.88 | 0.760 |
| ring-type | stalk-surface-below-ring | 86.75 | 2.637 |
| ring-type | stalk-surface-above-ring | 89.38 | 2.575 |
| ring-type | bruises | 45.88 | 2.172 |
| spore-print-color | gill-attachment | 98.84 | 4.208 |
| spore-print-color | stalk-color-below-ring | 98.84 | 3.109 |
| spore-print-color | veil-color | 98.84 | 2.956 |
| stalk-color-above-ring | stalk-color-below-ring | 97.62 | 6.792 |
| stalk-color-above-ring | gill-attachment | 97.78 | 4.338 |
| stalk-color-above-ring | ring-number | 99.52 | 4.075 |
| stalk-color-below-ring | gill-attachment | 98.07 | 8.038 |
| stalk-color-below-ring | stalk-color-above-ring | 98.07 | 5.138 |
| stalk-color-below-ring | veil-color | 98.07 | 3.264 |
| stalk-root | habitat | 24.31 | 1.019 |
| stalk-root | population | 23.79 | 0.987 |
| stalk-root | spore-print-color | 65.69 | 0.944 |
| stalk-shape | stalk-color-below-ring | 56.75 | 0.827 |
| stalk-shape | ring-number | 22.38 | 0.776 |
| stalk-shape | odor | 22.38 | 0.745 |
| stalk-surface-above-ring | ring-type | 75.62 | 1.824 |
| stalk-surface-above-ring | stalk-surface-below-ring | 72.00 | 1.719 |
| stalk-surface-above-ring | bruises | 62.12 | 1.706 |
| stalk-surface-below-ring | ring-type | 73.75 | 1.705 |
| stalk-surface-below-ring | stalk-surface-above-ring | 80.75 | 1.635 |
| stalk-surface-below-ring | class | 81.25 | 1.613 |
| veil-color | class | 49.00 | 1.265 |
| veil-color | ring-type | 52.00 | 1.125 |
| veil-color | stalk-surface-below-ring | 51.50 | 1.043 |

## Q moyens par run

| contrôle | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| bruises | 0.000 | 5.372 | 0.000 | 0.356 | 14.183 |
| cap-color | 2.321 | 0.000 | 2.321 | 0.333 | 4.800 |
| cap-shape | 2.683 | 3.026 | 2.683 | 0.241 | 28.523 |
| cap-surface | 9.492 | 0.000 | 9.492 | 0.209 | 10.795 |
| class | 1.511 | 2.836 | 1.511 | 0.247 | 19.859 |
| gill-attachment | 0.000 | 0.000 | 0.000 | 0.333 | 23.776 |
| gill-color | 1.129 | 0.000 | 1.129 | 0.197 | 6.019 |
| gill-size | 0.000 | 9.595 | 0.000 | 0.347 | 22.527 |
| gill-spacing | 0.000 | 1.739 | 0.000 | 0.547 | 18.076 |
| habitat | 1.191 | 1.468 | 1.191 | 0.305 | 10.327 |
| odor | 0.740 | 0.000 | 0.740 | 0.329 | 0.546 |
| population | 0.711 | 0.000 | 0.711 | 0.347 | 4.876 |
| ring-number | 0.000 | 0.000 | 0.000 | 0.620 | 28.490 |
| ring-type | 5.384 | 41.327 | 5.384 | 0.273 | 6.512 |
| spore-print-color | 1.941 | 0.000 | 1.941 | 0.195 | 5.826 |
| stalk-color-above-ring | 1.034 | 0.000 | 1.034 | 0.425 | 0.494 |
| stalk-color-below-ring | 1.563 | 0.000 | 1.563 | 0.210 | 5.377 |
| stalk-root | 70.864 | 44.733 | 70.864 | 0.428 | 14.949 |
| stalk-shape | 0.000 | 4.082 | 0.000 | 0.297 | 13.703 |
| stalk-surface-above-ring | 1.286 | 19.865 | 1.286 | 0.343 | 13.197 |
| stalk-surface-below-ring | 1.153 | 5.145 | 1.153 | 0.345 | 13.984 |
| veil-color | 0.000 | 1035.305 | 0.000 | 0.300 | 20.685 |
| veil-type | 0.000 | 0.000 | 0.000 | 0.142 | 0.000 |

## F1/F2 — flux Tous, avant et après seuil

| contrôle | estimateur | F1 post | F2 post | F1 pré | F2 pré | ΔF1 | ΔF2 | changement signe |
|---|---|---|---|---|---|---|---|---|
| bruises | Higuchi | 0.001818 | 0.000780 | -0.004284 | -0.000102 | 0.006102 | 0.000882 | True |
| bruises | DFA | -0.004080 | -0.001998 | 0.000301 | -0.000087 | -0.004381 | -0.001911 | True |
| bruises | Katz | -0.000117 | -0.000061 | 0.000014 | -0.000006 | -0.000131 | -0.000055 | True |
| bruises | Hurst | 0.006235 | 0.002408 | -0.001684 | 0.000303 | 0.007918 | 0.002105 | True |
| bruises | SampleEn | 0.003397 | 0.003403 | 0.003255 | 0.000260 | 0.000142 | 0.003144 | False |
| cap-color | Higuchi | 0.022298 | -0.008612 | -0.000261 | 0.000123 | 0.022558 | -0.008735 | True |
| cap-color | DFA | 0.004723 | -0.008288 | -0.000151 | 0.000125 | 0.004875 | -0.008412 | True |
| cap-color | Katz | 0.004790 | 0.000229 | -0.000725 | 0.000065 | 0.005514 | 0.000164 | True |
| cap-color | Hurst | 0.014921 | 0.001610 | -0.000615 | 0.000021 | 0.015536 | 0.001589 | True |
| cap-color | SampleEn | 0.010919 | -0.011391 | 0.000088 | 0.000042 | 0.010830 | -0.011434 | False |
| cap-shape | Higuchi | 0.000029 | -0.000007 | -0.000285 | 0.000039 | 0.000315 | -0.000046 | True |
| cap-shape | DFA | -0.003651 | 0.000847 | 0.000911 | -0.000305 | -0.004561 | 0.001153 | True |
| cap-shape | Katz | 0.000448 | -0.000102 | -0.000029 | 0.000004 | 0.000476 | -0.000106 | True |
| cap-shape | Hurst | 0.005562 | -0.001254 | -0.000686 | 0.000228 | 0.006248 | -0.001482 | True |
| cap-shape | SampleEn | -0.000972 | 0.000275 | -0.000022 | -0.000247 | -0.000951 | 0.000522 | False |
| cap-surface | Higuchi | -0.002449 | -0.000027 | -0.003538 | 0.000553 | 0.001089 | -0.000581 | False |
| cap-surface | DFA | -0.002684 | -0.000015 | 0.007243 | -0.000418 | -0.009927 | 0.000403 | True |
| cap-surface | Katz | -0.001450 | 0.000040 | 0.000228 | -0.000024 | -0.001679 | 0.000063 | True |
| cap-surface | Hurst | -0.000262 | 0.000078 | -0.008742 | 0.001066 | 0.008480 | -0.000988 | False |
| cap-surface | SampleEn | 0.002347 | -0.000179 | -0.012112 | 0.001991 | 0.014460 | -0.002170 | True |
| class | Higuchi | -0.000649 | 0.000053 | -0.000270 | 0.000004 | -0.000379 | 0.000049 | False |
| class | DFA | -0.000494 | -0.001194 | -0.001078 | -0.000586 | 0.000585 | -0.000608 | False |
| class | Katz | -0.000065 | -0.000005 | -0.000059 | -0.000035 | -0.000006 | 0.000030 | False |
| class | Hurst | 0.002887 | 0.001469 | -0.000737 | 0.000738 | 0.003624 | 0.000731 | True |
| class | SampleEn | -0.004585 | 0.001821 | -0.000369 | 0.000286 | -0.004216 | 0.001535 | False |
| gill-attachment | Higuchi | 0.000308 | -0.000032 | -0.000894 | 0.000858 | 0.001202 | -0.000890 | True |
| gill-attachment | DFA | 0.000510 | -0.000024 | 0.006675 | -0.008846 | -0.006165 | 0.008823 | False |
| gill-attachment | Katz | 0.000299 | -0.000033 | 0.000447 | -0.000149 | -0.000148 | 0.000116 | False |
| gill-attachment | Hurst | 0.002520 | -0.000267 | -0.011204 | 0.008672 | 0.013724 | -0.008938 | True |
| gill-attachment | SampleEn | -0.000495 | 0.000099 | -0.016901 | 0.006812 | 0.016406 | -0.006713 | False |
| gill-color | Higuchi | 0.031874 | 0.001735 | -0.004951 | -0.000070 | 0.036826 | 0.001805 | True |
| gill-color | DFA | 0.008196 | 0.008589 | -0.003665 | -0.000050 | 0.011861 | 0.008639 | True |
| gill-color | Katz | 0.007022 | -0.000193 | -0.001305 | 0.000020 | 0.008327 | -0.000212 | True |
| gill-color | Hurst | 0.005415 | -0.003580 | 0.000463 | 0.000068 | 0.004952 | -0.003648 | False |
| gill-color | SampleEn | -0.014578 | 0.016377 | -0.002744 | -0.000111 | -0.011834 | 0.016488 | False |
| gill-size | Higuchi | 0.001697 | -0.000050 | 0.010449 | 0.010733 | -0.008752 | -0.010782 | False |
| gill-size | DFA | -0.000238 | -0.000051 | -0.007970 | -0.004782 | 0.007732 | 0.004731 | False |
| gill-size | Katz | 0.000055 | -0.000004 | 0.000985 | 0.001185 | -0.000930 | -0.001189 | False |
| gill-size | Hurst | 0.000928 | 0.000138 | -0.001995 | -0.006534 | 0.002923 | 0.006672 | True |
| gill-size | SampleEn | -0.001438 | -0.000130 | -0.000816 | -0.003435 | -0.000622 | 0.003305 | False |
| gill-spacing | Higuchi | 0.000034 | -0.000005 | 0.001017 | -0.000376 | -0.000983 | 0.000371 | False |
| gill-spacing | DFA | -0.002374 | 0.000389 | 0.009063 | -0.002194 | -0.011437 | 0.002583 | True |
| gill-spacing | Katz | 0.000396 | -0.000054 | 0.000368 | -0.000074 | 0.000028 | 0.000020 | False |
| gill-spacing | Hurst | 0.004709 | -0.000650 | -0.009636 | 0.003017 | 0.014345 | -0.003667 | True |
| gill-spacing | SampleEn | -0.000920 | 0.000068 | -0.043119 | 0.013349 | 0.042199 | -0.013280 | False |
| habitat | Higuchi | 0.008450 | -0.000842 | 0.000174 | -0.000395 | 0.008277 | -0.000447 | False |
| habitat | DFA | -0.003859 | -0.000934 | 0.002866 | -0.000106 | -0.006725 | -0.000828 | True |
| habitat | Katz | 0.002618 | -0.000133 | 0.000611 | -0.000042 | 0.002007 | -0.000092 | False |
| habitat | Hurst | 0.007560 | 0.000446 | -0.001929 | 0.000095 | 0.009489 | 0.000351 | True |
| habitat | SampleEn | 0.006485 | -0.001744 | -0.001537 | -0.000363 | 0.008022 | -0.001381 | True |
| odor | Higuchi | -0.000965 | 0.021604 | -0.001624 | -0.000334 | 0.000659 | 0.021939 | False |
| odor | DFA | 0.007782 | 0.015542 | 0.018048 | 0.002996 | -0.010266 | 0.012545 | False |
| odor | Katz | 0.014594 | 0.013285 | -0.000742 | -0.000398 | 0.015336 | 0.013683 | True |
| odor | Hurst | 0.018505 | 0.009790 | 0.000428 | -0.000102 | 0.018077 | 0.009892 | False |
| odor | SampleEn | -0.014846 | -0.005799 | -0.000119 | -0.000449 | -0.014728 | -0.005350 | False |
| population | Higuchi | 0.019552 | 0.001546 | 0.003517 | -0.000177 | 0.016035 | 0.001722 | False |
| population | DFA | 0.005190 | -0.002507 | 0.002326 | 0.000031 | 0.002864 | -0.002538 | False |
| population | Katz | 0.003792 | -0.003104 | 0.001745 | -0.000122 | 0.002047 | -0.002981 | False |
| population | Hurst | 0.009383 | 0.000981 | 0.001210 | -0.000191 | 0.008172 | 0.001172 | False |
| population | SampleEn | -0.001442 | 0.000319 | 0.000776 | -0.000059 | -0.002218 | 0.000378 | True |
| ring-number | Higuchi | 0.000024 | -0.000002 | -0.000369 | -0.000353 | 0.000393 | 0.000351 | True |
| ring-number | DFA | -0.002998 | 0.000357 | 0.008792 | -0.007546 | -0.011791 | 0.007902 | True |
| ring-number | Katz | 0.000242 | -0.000031 | 0.000932 | -0.000119 | -0.000690 | 0.000087 | False |
| ring-number | Hurst | 0.002194 | -0.000255 | -0.010076 | 0.006834 | 0.012270 | -0.007089 | True |
| ring-number | SampleEn | 0.000981 | -0.000153 | 0.005017 | 0.008498 | -0.004036 | -0.008651 | False |
| ring-type | Higuchi | -0.037175 | 0.008486 | -0.008026 | -0.000446 | -0.029149 | 0.008931 | False |
| ring-type | DFA | -0.119557 | -0.012810 | -0.005280 | -0.000543 | -0.114277 | -0.012266 | False |
| ring-type | Katz | -0.009616 | 0.002000 | -0.003486 | -0.000244 | -0.006129 | 0.002244 | False |
| ring-type | Hurst | 0.009245 | 0.004264 | -0.001792 | 0.000053 | 0.011037 | 0.004210 | True |
| ring-type | SampleEn | 0.000506 | -0.000117 | -0.003735 | -0.000093 | 0.004241 | -0.000024 | True |
| spore-print-color | Higuchi | -0.022291 | -0.002436 | 0.001262 | -0.000199 | -0.023553 | -0.002237 | True |
| spore-print-color | DFA | -0.001020 | 0.002622 | 0.000077 | -0.000070 | -0.001097 | 0.002693 | True |
| spore-print-color | Katz | -0.003095 | -0.001138 | 0.001492 | -0.000035 | -0.004587 | -0.001103 | True |
| spore-print-color | Hurst | -0.001150 | -0.003349 | 0.002194 | -0.000016 | -0.003344 | -0.003333 | True |
| spore-print-color | SampleEn | -0.000561 | 0.007247 | -0.001046 | -0.000123 | 0.000485 | 0.007370 | False |
| stalk-color-above-ring | Higuchi | 0.004078 | 0.007568 | -0.001119 | 0.000619 | 0.005197 | 0.006948 | True |
| stalk-color-above-ring | DFA | 0.011721 | -0.000373 | 0.095272 | 0.002568 | -0.083551 | -0.002941 | False |
| stalk-color-above-ring | Katz | 0.028152 | -0.003572 | -0.000873 | 0.000366 | 0.029025 | -0.003938 | True |
| stalk-color-above-ring | Hurst | 0.030478 | -0.006049 | 0.002439 | 0.000176 | 0.028039 | -0.006226 | False |
| stalk-color-above-ring | SampleEn | -0.011395 | -0.001764 | -0.004131 | 0.000228 | -0.007264 | -0.001992 | False |
| stalk-color-below-ring | Higuchi | -0.022819 | -0.005661 | -0.004490 | 0.000198 | -0.018329 | -0.005859 | False |
| stalk-color-below-ring | DFA | -0.010771 | 0.002820 | -0.000480 | 0.000112 | -0.010291 | 0.002707 | False |
| stalk-color-below-ring | Katz | 0.009623 | -0.002126 | -0.001507 | 0.000110 | 0.011130 | -0.002235 | True |
| stalk-color-below-ring | Hurst | 0.018337 | -0.006586 | -0.001697 | 0.000155 | 0.020034 | -0.006741 | True |
| stalk-color-below-ring | SampleEn | -0.018314 | -0.006330 | -0.003152 | 0.000011 | -0.015162 | -0.006341 | False |
| stalk-root | Higuchi | 0.000015 | -0.000004 | 0.000598 | 0.000016 | -0.000583 | -0.000019 | False |
| stalk-root | DFA | -0.000974 | 0.000246 | 0.002956 | -0.000163 | -0.003930 | 0.000409 | True |
| stalk-root | Katz | 0.000219 | -0.000055 | -0.000177 | 0.000024 | 0.000396 | -0.000079 | True |
| stalk-root | Hurst | 0.001628 | -0.000411 | -0.002777 | 0.000310 | 0.004405 | -0.000721 | True |
| stalk-root | SampleEn | 0.000122 | -0.000031 | -0.003683 | 0.000106 | 0.003804 | -0.000137 | True |
| stalk-shape | Higuchi | -0.001278 | -0.000374 | -0.001851 | 0.000327 | 0.000573 | -0.000701 | False |
| stalk-shape | DFA | 0.000126 | -0.000625 | 0.000952 | -0.000988 | -0.000825 | 0.000363 | False |
| stalk-shape | Katz | -0.000252 | -0.000036 | -0.000008 | -0.000037 | -0.000244 | 0.000001 | False |
| stalk-shape | Hurst | 0.001997 | 0.000711 | -0.003088 | 0.001322 | 0.005085 | -0.000611 | True |
| stalk-shape | SampleEn | -0.008616 | 0.000488 | 0.000618 | 0.001688 | -0.009233 | -0.001200 | True |
| stalk-surface-above-ring | Higuchi | -0.003171 | 0.001682 | 0.000615 | 0.000021 | -0.003785 | 0.001660 | True |
| stalk-surface-above-ring | DFA | 0.016016 | -0.003890 | 0.002067 | 0.000019 | 0.013949 | -0.003909 | False |
| stalk-surface-above-ring | Katz | -0.000874 | 0.000571 | 0.001141 | 0.000053 | -0.002015 | 0.000518 | True |
| stalk-surface-above-ring | Hurst | 0.004485 | -0.001014 | 0.000049 | 0.000191 | 0.004436 | -0.001206 | False |
| stalk-surface-above-ring | SampleEn | 0.001901 | -0.000842 | 0.000878 | -0.000254 | 0.001023 | -0.000588 | False |
| stalk-surface-below-ring | Higuchi | -0.027656 | 0.019762 | -0.000027 | -0.000077 | -0.027630 | 0.019839 | False |
| stalk-surface-below-ring | DFA | 0.001855 | 0.007854 | 0.000214 | -0.000264 | 0.001642 | 0.008118 | False |
| stalk-surface-below-ring | Katz | -0.001499 | 0.001372 | 0.000023 | -0.000028 | -0.001521 | 0.001400 | True |
| stalk-surface-below-ring | Hurst | 0.000622 | -0.010859 | -0.000531 | 0.000286 | 0.001153 | -0.011144 | True |
| stalk-surface-below-ring | SampleEn | -0.030002 | 0.004859 | 0.002417 | -0.000106 | -0.032418 | 0.004964 | True |
| veil-color | Higuchi | -0.000139 | 0.000021 | -0.042342 | -0.047686 | 0.042203 | 0.047707 | False |
| veil-color | DFA | 0.000707 | 0.000010 | 0.019554 | 0.022521 | -0.018847 | -0.022511 | False |
| veil-color | Katz | 0.000176 | -0.000022 | -0.011692 | -0.013219 | 0.011868 | 0.013197 | True |
| veil-color | Hurst | 0.002581 | -0.000374 | -0.050387 | -0.057984 | 0.052968 | 0.057610 | True |
| veil-color | SampleEn | -0.000439 | 0.000067 | -0.038674 | -0.092931 | 0.038235 | 0.092998 | False |

## Corrections transparentes

- **Scan rapide v3.4 (avant le lot) :** écart max 0,0149 sur le scan brut initial, causé par les fenêtres commençant par un NaN (flux stalk-root) ; corrigé dans `scan_fast.py` et dans le pipeline, re-vérifié bit-identique (écart 0,0) sur stalk-root, odor et le scan traité du pilote. Le pilote v3.4 antérieur à la correction a été jeté, le lot est reparti de zéro.
- **synthese.py (26 oct. 19h16, outil de synthèse seulement) :** plantage sur veil-type (stabilité None, per_flux vide, transition_F1F2.csv absent) ; 3 gardes ajoutées (stabilité None, médiane/IQR vides, F1F2 absent). Pipeline et protocole intacts. Synthèse vérifiée ensuite : 23 lignes, 484 seuils par flux, 2 530 lignes F1F2, 118 plateaux.
- **Lot v3.3 arrêté le 26 oct. ~16h28** à la demande de l'utilisateur (cap-shape, cap-surface, cap-color, bruises, odor, gill-attachment tués sans fichier de sortie) ; seul le pilote v3.3 class est conservé, pour comparaison : identique au run v3.4 class sur tous les chiffres clés (MC 52,75 %, score 0,548, défaut 61,71 %, brut 62,5 %, rigide 56,1 %, UNSTABLE, bootstrap 52,73 % ± 14,78).

## Fichiers

- Synthèse : `synthese_runs.csv`, `tous_seuils_par_flux.csv`, `tous_F1F2.csv`, `plateaux_controles.csv`, `qs_par_run.csv`.
- Par run : `results/ctrl_<contrôle>/` (run_summary.json, scan_curve.csv, per_flux_thresholds.csv, landscape_peaks.csv, transition_F1F2.csv, threshold_scan.png, noise_diagnostic.png, text_report.txt, pipeline_results.json, numerical_results*.csv). veil-type n'a ni per_flux_thresholds.csv, ni transition_F1F2.csv, ni threshold_scan.png, ni text_report.txt — conséquence directe de l'absence de seuil.
- PDF complet : `Mushroom_Classification_v34_Resultats_complets.pdf` (avec figures). Zip des résultats : `mushroom_v34_23_controles_resultats.zip` (pipeline_results.json exclus, comme pour les séries précédentes, ils restent dans les dossiers par run).
