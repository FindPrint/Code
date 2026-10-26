# Earthquake / Tsunami (Kaggle ahmeduzaki) x pipeline v3.3-H1 — Rapport des 13 contrôles

Protocole gelé avant les runs : `PROTOCOLE.md` (25 oct. 2026 ~10h52 HAE).
Pipeline uploadé ce jour-là, tel quel : mode stable, w_size 80, cohen_d, graine 42,
HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse
les 12 autres colonnes. Source : `data/earthquake_data_tsunami.csv`, 782 lignes,
13 colonnes, toutes numériques, 0 valeur manquante. Aucun seuil attendu pré-enregistré :
lecture descriptive seulement, pas de vérité terrain.

## Verdict en une ligne

**13/13 runs terminés, 0 échec** (durée totale 4 783,5 s, ~368 s par run).
Seuls 2 runs sont VERY STABLE selon le critère du pipeline : **dmin (41,90 %) et Year (50,67 %)**.
5 runs sont UNSTABLE et ne doivent pas être lus seuls : cdi, gap, latitude, longitude, Month.
Deux faisceaux se répètent à travers les runs : (1) intensité haute ~85–92 %
(magnitude / sig / cdi / mmi, plus depth), (2) un faisceau dmin–Year–nst–tsunami autour de 42–53 %.
Le faisceau (2) est le plus fort en scores propres (jusqu’à 2,94), mais il est en partie
porté par des plateaux de zéros (dmin, nst) — voir les réserves ci-dessous.

## Synthèse par contrôle

| contrôle | seuil MC % | défaut % | MC−défaut | stabilité | ± | score MC | scan max | valeur au seuil (médiane) | durée s |
|---|---:|---:|---:|---|---:|---:|---:|---|---:|
| magnitude | 91.07 | 92.80 | -1.73 | MODERATELY STABLE | 3.87 | 0.447 | 0.262 | 7.6 | 369.8 |
| cdi | 84.40 | 92.52 | -8.12 | UNSTABLE | 7.06 | 0.456 | 0.438 | 8.0 | 507.3 |
| mmi | 11.74 | 8.03 | +3.71 | MODERATELY STABLE | 5.48 | 0.514 | 0.474 | 4.0 | 490.3 |
| sig | 84.92 | 93.91 | -8.99 | MODERATELY STABLE | 3.75 | 0.465 | 0.450 | 1050.0 | 366.3 |
| nst | 51.71 | 46.26 | +5.45 | MODERATELY STABLE | 3.99 | 0.496 | 0.645 | 176.5 | 336.9 |
| dmin | 41.90 | 47.09 | -5.19 | VERY STABLE | 2.82 | 0.561 | 0.775 | 0.0 | 327.2 |
| gap | 6.98 | 5.54 | +1.44 | UNSTABLE | 43.87 | 0.651 | 0.316 | 0.0 | 370.3 |
| depth | 89.59 | 94.18 | -4.60 | MODERATELY STABLE | 4.26 | 0.672 | 0.275 | 174.25 | 366.3 |
| latitude | 96.41 | 21.33 | +75.08 | UNSTABLE | 11.90 | 0.497 | 0.311 | 54.031 | 363.9 |
| longitude | 1.81 | 14.13 | -12.32 | UNSTABLE | 10.21 | 0.497 | 0.940 | -178.153 | 346.5 |
| Year | 50.67 | 49.86 | +0.81 | VERY STABLE | 2.58 | 0.528 | 0.670 | 2013.0 | 382.4 |
| Month | 32.72 | 78.39 | -45.68 | UNSTABLE | 30.34 | 0.601 | 0.110 | 4.0 | 334.0 |
| tsunami | 74.74 | 79.50 | -4.76 | MODERATELY STABLE | 3.14 | 0.503 | 0.475 | 1.0 | 222.3 |

## Stabilité : ce qui tient, ce qui ne tient pas

- **VERY STABLE (2)** : dmin 41,90 % (±2,82, scan max 0,775) ; Year 50,67 % (±2,58, scan max 0,670).
  Ce sont les deux seuls seuils globaux que le critère de stabilité du pipeline soutient seuls.
- **MODERATELY STABLE (6)** : magnitude, mmi, sig, nst, depth, tsunami (±3,14 à ±5,48).
- **UNSTABLE (5)** : cdi (±7,06) ; gap (±43,87, moyenne bootstrap 52,58 % contre MC 6,98 % —
  le seuil MC ne survit pas au bootstrap) ; latitude (±11,90, MC 96,41 % contre défaut 21,33 %
  et moyenne 26,39 % — désaccord total) ; longitude (±10,21, MC 1,81 % en bordure, moyenne 18,26 %) ;
  Month (±30,34, MC 32,72 % contre défaut 78,39 %, scan max 0,110 — le plus faible de tous les runs).

## Les deux faisceaux qui se répètent

### 1. Intensité haute, ~85–92 %

- magnitude (MC 91,07 %) : sig 91,94 % (score propre 0,939), mmi 88,27 % (0,657), cdi 88,27 % (0,483).
- sig (MC 84,92 %) : 7 flux à ±5 pts du MC, dont cdi 84,92 % (1,276) et mmi 89,41 % (1,115).
- cdi (MC 84,40 %) : sig 84,40 % (1,132), mmi 84,40 % (1,114).
- depth (MC 89,59 %) : mmi 90,31 % (1,024), 5 flux à ±5 pts — mais scan global max faible (0,275).
- Lecture : quand on ordonne par magnitude, sig, cdi ou mmi, la coupure la plus nette tombe
  dans le haut de l’échelle (magnitude médiane ~7,6 au seuil, sig ~1 050, cdi 8).
  C’est une coupure « gros séismes » descriptive, pas une magnitude critique démontrée.

### 2. Faisceau dmin–Year–nst–tsunami, ~42–53 % (scores propres les plus forts)

- dmin (MC 41,90 %, VERY STABLE) : nst 41,90 % (2,843), Year 41,90 % (2,424), tsunami 34,03 % (1,629).
- Year (MC 50,67 %, VERY STABLE) : nst 53,05 % (2,936 — le plus fort de tout le banc),
  tsunami 42,05 % (2,125), cdi 9,36 % (1,509).
- nst (MC 51,71 %) : Year 42,64 % (2,133), tsunami 52,90 % (1,762), dmin 42,05 % (1,394).
- tsunami (MC 74,74 %) : nst 78,75 % (1,773), Year 78,75 % (1,629), dmin 74,74 % (1,027).
- En tant que flux (moyenne sur les 12 runs où la colonne est flux) :
  nst 1,015 (max 2,936), Year 1,010 (max 2,424), tsunami 0,862 (max 2,125), puis dmin 0,726.
  À l’autre bout : Month 0,281 et gap 0,371 — les flux les plus faibles du banc.

## Réserves qui changent la lecture (mesurées avant / pendant, pas après coup)

- **dmin est zéro à 51,8 %** (405/782 lignes à 0 exactement). Un seuil MC à 41,90 % tombe
  *à l’intérieur* du plateau de zéros : il coupe des lignes toutes à dmin = 0 selon l’ordre
  de tri, il ne sépare pas « dmin = 0 » de « dmin > 0 » (cette frontière est à 51,8 %).
  Le VERY STABLE de dmin ne doit donc pas être lu comme un seuil physique sur dmin.
- **nst est zéro à 46,7 %** (365/782). Son seuil MC 51,71 % est juste au-dessus de la frontière
  zéro/non-zéro : il sépare à peu près « pas de station » de « stations présentes », ce qui est
  plus interprétable que le cas dmin, mais reste une coupure de disponibilité de mesure.
- **tsunami est binaire** : plateaux de rang 30,63 % (tsunami = 0, 478 lignes) et 80,63 %
  (tsunami = 1, 304 lignes). Le seuil MC 74,74 % ne sépare pas 0 de 1 — il tombe entre les deux
  plateaux, du côté du groupe tsunami = 1. Tout % entre 30,63 et 80,63 ne sépare pas les mêmes
  groupes au sens strict du rang moyen ; la lecture « seuil tsunami » est donc à manier avec
  cette réserve, comme pour fbs dans Heart Attack.
- **cdi / mmi / Month sont discrets** (plateaux détaillés dans `plateaux_controles.csv`) :
  cdi 0 = 27,1 % des lignes ; mmi 7 = 26,7 % et 6 = 26,0 % ; Month 12 valeurs quasi uniformes.
  Leurs seuils en % se lisent comme des paliers de rang, pas comme des valeurs continues.
- **latitude / longitude ne sont pas des axes de progression** : ordonner par longitude, c’est
  ordonner d’ouest en est. Le seuil longitude à 1,81 % isole ~14 événements extrêmes ouest
  (médiane −178,15) et le scan max de 0,940 ne compense pas l’instabilité (±10,21) ni la bordure.
  Même remarque pour latitude (MC 96,41 % contre défaut 21,33 %) : désaccord à ne pas trancher.
- **Year n’est pas un seuil physique** : 50,67 % correspond à l’année 2013, médiane de couverture
  2001–2022. C’est une coupure temporelle descriptive (avant/après ~2013), pas une transition
  du système sismique démontrée par ce seul banc.

## Seuils propres par flux (top 3 par run)

| contrôle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| magnitude (91.07 %) | sig 91.94 % (0.939) | mmi 88.27 % (0.657) | cdi 88.27 % (0.483) |
| cdi (84.40 %) | sig 84.40 % (1.132) | Year 17.09 % (1.128) | mmi 84.40 % (1.114) |
| mmi (11.74 %) | sig 89.90 % (1.131) | depth 8.32 % (1.041) | cdi 82.17 % (0.912) |
| sig (84.92 %) | magnitude 26.93 % (1.648) | cdi 84.92 % (1.276) | mmi 89.41 % (1.115) |
| nst (51.71 %) | Year 42.64 % (2.133) | tsunami 52.90 % (1.762) | dmin 42.05 % (1.394) |
| dmin (41.90 %) | nst 41.90 % (2.843) | Year 41.90 % (2.424) | tsunami 34.03 % (1.629) |
| gap (6.98 %) | Year 6.98 % (0.958) | longitude 85.88 % (0.941) | cdi 7.73 % (0.568) |
| depth (89.59 %) | mmi 90.31 % (1.024) | gap 78.99 % (0.486) | dmin 86.54 % (0.421) |
| latitude (96.41 %) | longitude 13.15 % (0.999) | tsunami 95.81 % (0.778) | sig 65.92 % (0.651) |
| longitude (1.81 %) | tsunami 2.14 % (1.626) | depth 1.81 % (1.477) | mmi 1.81 % (1.467) |
| Year (50.67 %) | nst 53.05 % (2.936) | tsunami 42.05 % (2.125) | cdi 9.36 % (1.509) |
| Month (32.72 %) | depth 28.33 % (0.310) | mmi 40.30 % (0.264) | Year 81.45 % (0.223) |
| tsunami (74.74 %) | nst 78.75 % (1.773) | Year 78.75 % (1.629) | dmin 74.74 % (1.027) |

Détail complet des 156 seuils propres (13 × 12) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- Month : Q1 0.952, Q2 1.810, Q3 0.952, Q4 0.151, Q5 9.915
- Year : Q1 0.989, Q2 1.549, Q3 0.989, Q4 0.242, Q5 6.623
- cdi : Q1 1.136, Q2 1.623, Q3 1.136, Q4 0.291, Q5 9.571
- depth : Q1 0.941, Q2 3.325, Q3 0.941, Q4 0.202, Q5 7.922
- dmin : Q1 1.868, Q2 1.671, Q3 1.868, Q4 0.300, Q5 5.515
- gap : Q1 0.940, Q2 0.000, Q3 0.940, Q4 0.210, Q5 7.970
- latitude : Q1 0.430, Q2 0.000, Q3 0.430, Q4 0.338, Q5 5.502
- longitude : Q1 0.503, Q2 0.000, Q3 0.503, Q4 0.563, Q5 6.939
- magnitude : Q1 0.999, Q2 2.182, Q3 0.999, Q4 0.169, Q5 9.007
- mmi : Q1 1.192, Q2 2.477, Q3 1.192, Q4 0.243, Q5 6.376
- nst : Q1 8.088, Q2 3.111, Q3 8.088, Q4 0.213, Q5 5.855
- sig : Q1 1.298, Q2 1.949, Q3 1.298, Q4 0.231, Q5 6.287
- tsunami : Q1 1.320, Q2 2.021, Q3 1.320, Q4 0.358, Q5 9.475

Note : Q5 est élevé partout (5,50–9,92), Q4 faible partout (0,15–0,56) ;
Q2 vaut 0,000 dans les runs gap, latitude et longitude. Q1 sort à 8,088 dans le run nst,
contre 0,43–1,87 ailleurs — un point à vérifier avant toute lecture du run nst seul.

## Dérivées F1/F2 post-seuil, flux « Tous »

estimateur     DFA  Higuchi   Hurst    Katz  SampleEn
controle                                             
Month      -0.0025   0.0001  0.0025  0.0003    0.0014
Year        0.0003   0.0010  0.0010  0.0007    0.0063
cdi        -0.0014   0.0012  0.0085  0.0035    0.0496
depth       0.0016  -0.0003  0.0100  0.0040    0.0726
dmin        0.0034   0.0011 -0.0010  0.0004    0.0088
gap        -0.0000   0.0009  0.0005  0.0002    0.0043
latitude   -0.0144  -0.0018  0.0184  0.0046    0.0405
longitude   0.0007   0.0004 -0.0004  0.0002   -0.0007
magnitude  -0.0283  -0.0015  0.0300  0.0057    0.0807
mmi        -0.0000   0.0018  0.0006  0.0004    0.0041
nst        -0.0017  -0.0033 -0.0012 -0.0014    0.0097
sig        -0.0069  -0.0004  0.0097  0.0035    0.0405
tsunami     0.0320   0.0160 -0.0080 -0.0036    0.0559

Détail complet (65 lignes par run, 845 au total) : `tous_F1F2.csv`.

## Fichiers livrés

- `PROTOCOLE.md` — protocole gelé avant les runs.
- `synthese_runs.csv` — un ligne par contrôle (seuils, stabilité, scan, valeur au seuil).
- `tous_seuils_par_flux.csv` — les 156 seuils propres par flux.
- `tous_F1F2.csv` — dérivées F1/F2 post-seuil, tous runs.
- `plateaux_controles.csv` — paliers de rang des contrôles discrets.
- `results/ctrl_<colonne>/` — sorties complètes du pipeline par run
  (pipeline_results.json, numerical_results*.csv, scan_curve.csv, per_flux_thresholds.csv,
  landscape_peaks.csv, transition_F1F2.csv, threshold_scan.png, noise_diagnostic.png, text_report.txt).
- `earthquake_tsunami_13_controles_resultats.zip` — archive de l’ensemble ci-dessus + données.

