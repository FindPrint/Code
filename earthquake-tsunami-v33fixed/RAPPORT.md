# Earthquake / Tsunami (Kaggle ahmeduzaki) x pipeline v3.3 FIXED — Rapport des 13 controles

Protocole gele avant les runs : `PROTOCOLE.md` (25 oct. 2026 ~13h45 HAE). Meme protocole que la serie v3.3-H1 du matin, seul le pipeline change (Monte Carlo classique, sans guidage harmonique). Mode stable, w_size 80, cohen_d, graine 42. Controle EXCLU des flux (12 flux par run). Donnees : 782 lignes, 13 colonnes, 0 manquant. Lecture descriptive seulement.

## Verdict

**13/13 runs termines, 0 echec** (duree totale 5 506,4 s). VERY STABLE : **dmin 44,37 % et Year 47,41 %** — les memes deux que en harmonic, decales de +2,47 et -3,26 pts. MODERATELY STABLE : mmi, sig, depth, tsunami (4). UNSTABLE : magnitude, cdi, nst, gap, latitude, longitude, Month (7, contre 5 en harmonic : magnitude et nst ont bascule).

## Comparaison fixed vs harmonic (seuil MC %)

| controle | fixed MC % | harmonic MC % | delta | stabilite fixed | stabilite harmonic |
|---|---:|---:|---:|---|---|
| magnitude | 89.62 | 91.07 | -1.45 | UNSTABLE | MODERATELY STABLE |
| cdi | 80.31 | 84.40 | -4.09 | UNSTABLE | UNSTABLE |
| mmi | 10.30 | 11.74 | -1.44 | MODERATELY STABLE | MODERATELY STABLE |
| sig | 90.56 | 84.92 | +5.64 | MODERATELY STABLE | MODERATELY STABLE |
| nst | 49.45 | 51.71 | -2.26 | UNSTABLE | MODERATELY STABLE |
| dmin | 44.37 | 41.90 | +2.47 | VERY STABLE | VERY STABLE |
| gap | 7.45 | 6.98 | +0.47 | UNSTABLE | UNSTABLE |
| depth | 91.95 | 89.59 | +2.36 | MODERATELY STABLE | MODERATELY STABLE |
| latitude | 31.70 | 96.41 | -64.71 | UNSTABLE | UNSTABLE |
| longitude | 1.83 | 1.81 | +0.02 | UNSTABLE | UNSTABLE |
| Year | 47.41 | 50.67 | -3.26 | VERY STABLE | VERY STABLE |
| Month | 39.12 | 32.72 | +6.40 | UNSTABLE | UNSTABLE |
| tsunami | 56.34 | 74.74 | -18.40 | MODERATELY STABLE | MODERATELY STABLE |

Ecarts les plus forts : latitude -64,71 (96,41 % harmonic -> 31,70 % fixed, UNSTABLE dans les deux : ne pas trancher), tsunami -18,40 (74,74 -> 56,34), sig +5,64, Month +6,40. Ecarts les plus faibles : longitude +0,02, gap +0,47, magnitude -1,45, mmi -1,44. Les deux VERY STABLE bougent peu (+2,47 / -3,26).

## Synthese fixed

| controle | seuil MC % | defaut % | stabilite | ± | score MC | scan max | valeur au seuil |
|---|---:|---:|---|---:|---:|---:|---|
| magnitude | 89.62 | 92.80 | UNSTABLE | 8.59 | 0.461 | 0.285 | 7.6 |
| cdi | 80.31 | 92.52 | UNSTABLE | 6.44 | 0.481 | 0.449 | 7.0 |
| mmi | 10.30 | 8.03 | MODERATELY STABLE | 4.76 | 0.501 | 0.468 | 4.0 |
| sig | 90.56 | 93.91 | MODERATELY STABLE | 3.62 | 0.453 | 0.438 | 1221.0 |
| nst | 49.45 | 46.26 | UNSTABLE | 6.08 | 0.522 | 0.651 | 129.0 |
| dmin | 44.37 | 47.09 | VERY STABLE | 2.81 | 0.541 | 0.775 | 0.0 |
| gap | 7.45 | 5.54 | UNSTABLE | 43.87 | 0.649 | 0.303 | 0.0 |
| depth | 91.95 | 94.18 | MODERATELY STABLE | 4.27 | 0.669 | 0.322 | 220.0 |
| latitude | 31.70 | 21.33 | UNSTABLE | 12.06 | 0.484 | 0.329 | -10.004 |
| longitude | 1.83 | 14.13 | UNSTABLE | 10.23 | 0.529 | 0.831 | -178.126 |
| Year | 47.41 | 49.86 | VERY STABLE | 2.70 | 0.512 | 0.670 | 2013.0 |
| Month | 39.12 | 78.39 | UNSTABLE | 30.34 | 0.621 | 0.124 | 5.0 |
| tsunami | 56.34 | 79.50 | MODERATELY STABLE | 3.09 | 0.512 | 0.469 | 0.0 |

## Flux informationnels, a part

Definition : Year, Month, latitude, longitude, tsunami. Fichiers a part : `flux_informationnels_donnees.csv` (5 colonnes brutes, 782 lignes) et `seuils_flux_informationnels.csv` (60 lignes).

Scores propres moyens en tant que flux : Year 1,013 (max 2,426), tsunami 0,821 (max 2,053), latitude 0,480 (max 1,196), longitude 0,468 (max 0,971), Month 0,282 (max 0,717). Top par run (flux info seulement) : Year porte les plus forts — dmin : Year 49,45 % (2,426) ; nst : Year 38,67 % (2,152) ; tsunami : Year 79,28 % (1,581) ; longitude : tsunami 2,14 % (1,574) ; Year (controle) : tsunami 44,58 % (2,053). Month ne depasse jamais 0,717 (controle longitude).

Reserves inchangees : dmin = 0 a 51,8 % (seuil 44,37 % a l'interieur du plateau), nst = 0 a 46,7 %, tsunami binaire (plateaux 30,63 % / 80,63 %, seuil fixed 56,34 % avec valeur mediane 0), latitude/longitude = ordre geographique, Year 47,41 % = annee 2013 (mediane de couverture).

## Seuils propres par flux (top 3 par run)

| controle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| magnitude (89.62 %) | sig 86.56 % (1.029) | mmi 92.37 % (0.712) | cdi 92.06 % (0.595) |
| cdi (80.31 %) | Year 16.34 % (1.174) | sig 80.92 % (1.162) | mmi 81.07 % (1.142) |
| mmi (10.30 %) | sig 91.60 % (1.104) | depth 8.72 % (1.033) | cdi 84.94 % (0.937) |
| sig (90.56 %) | magnitude 40.30 % (1.633) | cdi 86.51 % (1.227) | mmi 89.21 % (1.087) |
| nst (49.45 %) | Year 38.67 % (2.152) | tsunami 49.45 % (1.756) | dmin 50.87 % (1.421) |
| dmin (44.37 %) | nst 44.37 % (2.761) | Year 49.45 % (2.426) | tsunami 42.79 % (1.598) |
| gap (7.45 %) | longitude 85.42 % (0.971) | Year 7.45 % (0.896) | cdi 6.97 % (0.613) |
| depth (91.95 %) | mmi 91.95 % (1.331) | dmin 91.95 % (0.473) | Year 91.95 % (0.472) |
| latitude (31.70 %) | longitude 18.55 % (0.782) | sig 61.72 % (0.707) | dmin 32.38 % (0.581) |
| longitude (1.83 %) | tsunami 2.14 % (1.574) | nst 2.29 % (1.320) | Year 4.13 % (1.243) |
| Year (47.41 %) | nst 52.12 % (2.847) | tsunami 44.58 % (2.053) | cdi 8.95 % (1.556) |
| Month (39.12 %) | mmi 42.16 % (0.313) | depth 32.88 % (0.306) | Year 72.51 % (0.270) |
| tsunami (56.34 %) | nst 80.31 % (1.754) | Year 79.28 % (1.581) | dmin 65.24 % (0.956) |

Detail complet : `tous_seuils_par_flux.csv` (156 lignes), `tous_F1F2.csv` (845 lignes), `synthese_runs.csv`, `plateaux_controles.csv`.
Archive : `earthquake_tsunami_v33fixed_13_controles_resultats.zip`.
