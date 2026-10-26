# Air Quality Dataset (Kaggle srisyra02) x pipeline v3.3-H1 — Rapport des 10 controles

Protocole gele avant les runs : `PROTOCOLE.md` (26 oct. 2026 ~08h50 HAE).
Pipeline uploade ce jour-la, tel quel : mode stable, w_size 80, cohen_d, graine 42,
HARMONIC_PROB 0,45. Controle EXCLU des flux (regle Porte D) : chaque run analyse
les 9 autres colonnes numeriques. Source : `data/air_quality_dataset.csv`, 500 lignes,
10 colonnes, 0 valeur manquante ; fichier de travail copie exacte, aucune colonne derivee.
Aucun seuil attendu pre-enregistre : lecture descriptive seulement, pas de verite terrain,
aucune conclusion sanitaire ou reglementaire.

## Ecart page Kaggle / fichier reel (constate avant les runs)

La page Kaggle decrit des mesures horaires avec Date, Time et une etiquette Source
(Traffic, Industrial, Biomass) ainsi que des capteurs PT08 et RH/AH. Le fichier
telecharge ne contient rien de tout cela : 10 colonnes numeriques seulement
(PM2.5, PM10, NOx, NO2, SO2, VOCs, CO, CO2, CH4, Temperature), sans aucune colonne
temporelle ni etiquette. Aucune lecture temporelle ni par source d'emission n'est
donc possible sur ce fichier. Valeurs negatives presentes (NOx min -0,08 ; NO2 min
-1,94 ; SO2 min -1,10), signalees, non corrigees.

## Verdict en une ligne

**10/10 runs termines, 0 echec(s)** (duree totale des runs OK : 1289.0 s, ~129 s par run). Stabilites (critere du pipeline) : MODERATELY STABLE = 6, UNSTABLE = 4.
Aucun run VERY STABLE selon le critere du pipeline.
Les runs UNSTABLE ne doivent pas etre lus seuls.
Tous les seuils MC se situent entre 66.33 % et 78.91 %, soit dans le tiers superieur de l'axe de rang, pour les 10 controles.

## Synthese par controle

| controle | seuil MC % | defaut % | MC-defaut | stabilite | +/- | score MC | scan max | valeur au seuil (mediane) | duree s |
|---|---:|---:|---:|---|---:|---:|---:|---|---:|
| PM2.5 | 69.33 | 74.09 | -4.76 | MODERATELY STABLE | 3.23 | 0.663 | 1.764 | 64.78 | 131.6 |
| PM10 | 69.08 | 70.91 | -1.83 | MODERATELY STABLE | 5.66 | 0.652 | 1.773 | 102.031 | 133.4 |
| NOx | 78.01 | 73.18 | +4.83 | UNSTABLE | 6.15 | 0.617 | 1.221 | 142.863 | 127.7 |
| NO2 | 76.30 | 72.73 | +3.57 | MODERATELY STABLE | 5.87 | 0.660 | 1.768 | 65.206 | 128.4 |
| SO2 | 67.92 | 71.82 | -3.90 | MODERATELY STABLE | 4.13 | 0.680 | 2.126 | 13.551 | 130.2 |
| VOCs | 78.91 | 77.27 | +1.64 | UNSTABLE | 6.85 | 0.623 | 1.454 | 145.114 | 127.3 |
| CO | 77.22 | 85.91 | -8.69 | UNSTABLE | 9.42 | 0.611 | 1.311 | 2.807 | 128.3 |
| CO2 | 66.33 | 65.00 | +1.33 | MODERATELY STABLE | 4.76 | 0.637 | 1.909 | 469.875 | 127.2 |
| CH4 | 72.90 | 75.45 | -2.55 | MODERATELY STABLE | 4.87 | 0.635 | 1.769 | 2.311 | 126.5 |
| Temperature | 67.59 | 56.36 | +11.23 | UNSTABLE | 8.46 | 0.592 | 1.024 | 31.951 | 128.4 |

## Stabilite : ce qui tient, ce qui ne tient pas

- **MODERATELY STABLE (6)** : PM2.5 69.33 % (+/-3.23), PM10 69.08 % (+/-5.66), NO2 76.30 % (+/-5.87), SO2 67.92 % (+/-4.13), CO2 66.33 % (+/-4.76), CH4 72.90 % (+/-4.87).
- **UNSTABLE (4)** : NOx 78.01 % (+/-6.15), VOCs 78.91 % (+/-6.85), CO 77.22 % (+/-9.42), Temperature 67.59 % (+/-8.46).

## Accord seuil MC / moyenne bootstrap (lecture critique de la stabilite)

La note de stabilite du pipeline repose sur l'ecart-type bootstrap, pas sur l'accord
entre le seuil MC et la moyenne bootstrap. Ici aucun run ne depasse 15 points d'ecart ;
un seul depasse 10 points : Temperature (MC 67,59 %, moyenne 54,36 %, ecart 13,2 pts,
UNSTABLE +/-8,46). Les autres ecarts sont tous inferieurs a 9 points.

## Seuils propres par flux (top 10 de tout le banc)

- controle SO2 : flux CO2 68.21 % (score 3.094).
- controle NO2 : flux NOx 33.82 % (score 2.896).
- controle PM10 : flux CO2 73.70 % (score 2.470).
- controle NO2 : flux CO2 76.30 % (score 2.437).
- controle PM2.5 : flux CO2 72.20 % (score 2.407).
- controle SO2 : flux PM10 67.92 % (score 2.402).
- controle CO2 : flux SO2 73.16 % (score 2.365).
- controle SO2 : flux NO2 68.79 % (score 2.298).
- controle CH4 : flux CO2 72.90 % (score 2.255).
- controle PM10 : flux SO2 67.05 % (score 2.223).

En tant que flux (moyenne sur les 9 runs ou la colonne est flux) :
- CO2 : moyenne 2.160, max 3.094.
- SO2 : moyenne 1.845, max 2.365.
- NO2 : moyenne 1.832, max 2.298.
- NOx : moyenne 1.823, max 2.896.
- PM10 : moyenne 1.747, max 2.402.
- PM2.5 : moyenne 1.726, max 2.193.
- CH4 : moyenne 1.549, max 2.032.
- CO : moyenne 1.498, max 1.828.
- VOCs : moyenne 1.481, max 1.904.
- Temperature : moyenne 1.257, max 1.467.

## Seuils propres par flux (top 3 par run)

| controle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| PM2.5 (69.33 %) | CO2 72.20 % (2.407) | SO2 65.81 % (2.124) | PM10 72.20 % (1.988) |
| PM10 (69.08 %) | CO2 73.70 % (2.470) | SO2 67.05 % (2.223) | PM2.5 69.36 % (1.923) |
| NOx (78.01 %) | NO2 31.33 % (2.094) | CO2 30.72 % (1.864) | CO 34.64 % (1.519) |
| NO2 (76.30 %) | NOx 33.82 % (2.896) | CO2 76.30 % (2.437) | SO2 76.30 % (2.216) |
| SO2 (67.92 %) | CO2 68.21 % (3.094) | PM10 67.92 % (2.402) | NO2 68.79 % (2.298) |
| VOCs (78.91 %) | CO2 78.91 % (1.850) | SO2 65.18 % (1.730) | PM10 68.05 % (1.664) |
| CO (77.22 %) | CO2 75.44 % (1.755) | NO2 61.52 % (1.603) | NOx 61.52 % (1.556) |
| CO2 (66.33 %) | SO2 73.16 % (2.365) | NO2 60.51 % (2.203) | NOx 25.57 % (2.156) |
| CH4 (72.90 %) | CO2 72.90 % (2.255) | PM2.5 72.90 % (2.079) | PM10 76.72 % (2.046) |
| Temperature (67.59 %) | CO2 20.00 % (1.306) | NOx 11.39 % (1.252) | NO2 23.80 % (1.218) |

Detail complet des 90 seuils propres (10 x 9) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- CH4 : Q1_Calme_vs_Chaos = 0.644, Q2_Tension_Seuil = 0.912, Q3_Agressivite = 0.644, Q4_Persistence = 0.269, Q5_Active_Reactive = 5.416, Q5_Actif_Receptif = 5.416
- CO : Q1_Calme_vs_Chaos = 0.753, Q2_Tension_Seuil = 1.268, Q3_Agressivite = 0.753, Q4_Persistence = 0.279, Q5_Active_Reactive = 4.475, Q5_Actif_Receptif = 4.475
- CO2 : Q1_Calme_vs_Chaos = 0.647, Q2_Tension_Seuil = 0.628, Q3_Agressivite = 0.647, Q4_Persistence = 0.460, Q5_Active_Reactive = 3.060, Q5_Actif_Receptif = 3.060
- NO2 : Q1_Calme_vs_Chaos = 0.548, Q2_Tension_Seuil = 2.154, Q3_Agressivite = 0.548, Q4_Persistence = 0.295, Q5_Active_Reactive = 5.139, Q5_Actif_Receptif = 5.139
- NOx : Q1_Calme_vs_Chaos = 0.583, Q2_Tension_Seuil = 1.415, Q3_Agressivite = 0.583, Q4_Persistence = 0.343, Q5_Active_Reactive = 4.468, Q5_Actif_Receptif = 4.468
- PM10 : Q1_Calme_vs_Chaos = 0.509, Q2_Tension_Seuil = 1.660, Q3_Agressivite = 0.509, Q4_Persistence = 0.259, Q5_Active_Reactive = 5.862, Q5_Actif_Receptif = 5.862
- PM2.5 : Q1_Calme_vs_Chaos = 0.538, Q2_Tension_Seuil = 1.228, Q3_Agressivite = 0.538, Q4_Persistence = 0.250, Q5_Active_Reactive = 6.430, Q5_Actif_Receptif = 6.430
- SO2 : Q1_Calme_vs_Chaos = 0.671, Q2_Tension_Seuil = 1.630, Q3_Agressivite = 0.671, Q4_Persistence = 0.287, Q5_Active_Reactive = 5.708, Q5_Actif_Receptif = 5.708
- Temperature : Q1_Calme_vs_Chaos = 0.563, Q2_Tension_Seuil = 1.833, Q3_Agressivite = 0.563, Q4_Persistence = 0.261, Q5_Active_Reactive = 4.688, Q5_Actif_Receptif = 4.688
- VOCs : Q1_Calme_vs_Chaos = 0.533, Q2_Tension_Seuil = 1.092, Q3_Agressivite = 0.533, Q4_Persistence = 0.234, Q5_Active_Reactive = 5.600, Q5_Actif_Receptif = 5.600

## Derivees F1/F2 post-seuil, flux « Tous »

estimateur      DFA  Higuchi   Hurst    Katz  SampleEn
controle                                              
CH4         -0.0037  -0.0003  0.0025  0.0022    0.0341
CO           0.0035  -0.0001 -0.0006  0.0027    0.0972
CO2          0.0050   0.0021 -0.0020  0.0021    0.0556
NO2         -0.0039   0.0003  0.0052  0.0025    0.0418
NOx         -0.0060   0.0002  0.0052  0.0023    0.0809
PM10        -0.0007   0.0011  0.0018  0.0019    0.0281
PM2.5        0.0001  -0.0009  0.0012  0.0019    0.0167
SO2          0.0028   0.0011 -0.0008  0.0018    0.0187
Temperature -0.0053  -0.0005  0.0082  0.0014    0.0498
VOCs        -0.0015   0.0002  0.0073  0.0028    0.0432

Detail complet (500 lignes) : `tous_F1F2.csv`.

## Reserves (gelees avant les runs, rappelees ici)

- Pas de colonne temporelle dans le fichier reel : le controle est un axe de rang, pas un temps.
- Aucune etiquette Source dans le fichier : aucune lecture par source d'emission.
- Valeurs negatives de NOx/NO2/SO2 : signalees, non corrigees.
- Aucune conclusion sanitaire ou reglementaire tiree des seuils : mesures du pipeline sur ce fichier.
