# Food_Costs 2014 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1 — Rapport des 14 contrôles

Protocole : `PROTOCOLE.md` (gelé le 26 oct. 2026 avant les runs de 2014, répétition exacte du protocole 2013). Pipeline uploadé, tel quel : mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse les 13 autres colonnes numériques. Source : `data/Food_Costs_2014_original.csv` (WICAgencies2014ytd/Food_Costs.csv, 92 lignes, 14 colonnes, exercice WIC 2014, 2013-10 à 2014-09). Fichier de travail : copie exacte + `agency_encoded` + Cumulative Cost convertie en nombre (vérifiée égale à la somme des 12 mois, écart 0). Aucun seuil attendu pré-enregistré : lecture descriptive seulement, aucune conclusion de politique publique, budgétaire ou nutritionnelle.

## Écarts et pièges de structure

- Le dataset complet compte 68 fichiers, dont 4 fichiers nommés Food_Costs.csv (2013, 2014, 2015, 2016) : seul 2014 est traité ici.
- Texas en double (ligne vide + ligne réelle) ; chaque colonne mensuelle et Cumulative Cost ont donc 91 valeurs valides, pas 92.
- Valeurs mensuelles négatives, conservées telles quelles : Chickasaw Nation, OK, 2014-06, -24,170.
- **Mountain Plains est une ligne d'agrégat** : 248,629,292, somme des 10 États + 10 agences tribales du groupe = 248,629,292, écart 0. Le total du fichier (4,572,952,566) double-compte donc cet agrégat, et Mountain Plains figure parmi les 12 plus grandes sans être une agence distincte.
- Cumulative Cost est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels.

## Verdict en une ligne

**14/14 runs terminés, 0 échec** (durée totale des runs : 182.5 s, ~13 s par run). Stabilité (critère du pipeline) : VERY STABLE = 14. **Mais** cette note repose sur l'écart-type bootstrap (≈ 0), pas sur l'accord MC / moyenne bootstrap : écart de 28.79 à 42.42 points pour les contrôles numériques et de 40.91 points pour Agency. La note VERY STABLE ne doit donc PAS être lue comme une confirmation du seuil MC.
Les contrôles numériques donnent 87,88 % ; Agency donne 83.33 %. Le seuil MC, c'est la coupure après les 12 plus grandes agences, qui totalisent 62.6 % du total du fichier sur Cumulative Cost. Les courbes de scan montent régulièrement jusqu'au MC puis s'arrêtent : ce n'est pas un pic intérieur, c'est le bord de la zone calculable qui isole la queue des très grandes agences.

## Synthèse par contrôle

| contrôle | n | seuil MC % | défaut % | MC−défaut | moy. bootstrap % | MC−moy. | stabilité | score MC | scan max | valeur au MC (médiane) | durée s |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Agency | 92 | 83.33 | 29.63 | +53.70 | 42.42 | +40.91 | VERY STABLE | 0.540 | 0.373 | 75 | 12.8 |
| 2013-10 | 91 | 87.88 | 33.33 | +54.55 | 45.45 | +42.42 | VERY STABLE | 0.507 | 1.666 | 7,556,156 | 12.5 |
| 2013-11 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.514 | 1.778 | 10,230,655 | 13.3 |
| 2013-12 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.514 | 1.752 | 9,652,550 | 14.5 |
| 2014-01 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.514 | 1.772 | 9,514,577 | 13.2 |
| 2014-02 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.516 | 1.806 | 8,177,351 | 12.5 |
| 2014-03 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.509 | 1.711 | 8,353,113 | 14.0 |
| 2014-04 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.511 | 1.743 | 9,756,356 | 13.1 |
| 2014-05 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.510 | 1.725 | 8,652,594 | 12.3 |
| 2014-06 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.504 | 1.624 | 8,998,388 | 12.3 |
| 2014-07 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.517 | 1.775 | 10,136,511 | 12.9 |
| 2014-08 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.513 | 1.776 | 9,255,570 | 12.6 |
| 2014-09 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.505 | 1.634 | 10,053,388 | 13.0 |
| Cumulative | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.516 | 1.794 | 107,943,509 | 13.5 |

Note : pour Agency, la « valeur au MC » est un code d'agence, pas un montant.

## Groupes au-dessus du seuil MC par contrôle

- 2013-10 (12 au-dessus) : plus petite au-dessus = 7,556,156 (Washington), plus grande en dessous = 7,442,418 (Louisiana) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Illinois; North Carolina; Georgia; Michigan; New Jersey; Washington.
- 2013-11 (12 au-dessus) : plus petite au-dessus = 10,230,655 (Michigan), plus grande en dessous = 9,709,990 (Tennessee) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Ohio; Illinois; North Carolina; Georgia; Pennsylvania; Michigan.
- 2013-12 (12 au-dessus) : plus petite au-dessus = 9,652,550 (Arizona), plus grande en dessous = 9,569,385 (Indiana) — California; New York; Texas; Pennsylvania; Mountain Plains; Florida; Illinois; Puerto Rico; Georgia; Michigan; North Carolina; Arizona.
- 2014-01 (12 au-dessus) : plus petite au-dessus = 9,514,577 (Ohio), plus grande en dessous = 8,852,339 (New Jersey) — California; New York; Florida; Mountain Plains; Puerto Rico; Pennsylvania; Texas; North Carolina; Georgia; Illinois; Michigan; Ohio.
- 2014-02 (12 au-dessus) : plus petite au-dessus = 8,177,351 (Ohio), plus grande en dessous = 8,037,067 (Pennsylvania) — California; Texas; New York; Mountain Plains; Florida; Puerto Rico; Illinois; North Carolina; Michigan; Georgia; New Jersey; Ohio.
- 2014-03 (12 au-dessus) : plus petite au-dessus = 8,353,113 (New Jersey), plus grande en dessous = 7,252,630 (Washington) — California; New York; Florida; Mountain Plains; Texas; Puerto Rico; Illinois; North Carolina; Georgia; Michigan; Ohio; New Jersey.
- 2014-04 (12 au-dessus) : plus petite au-dessus = 9,756,356 (Arizona), plus grande en dessous = 9,685,324 (Louisiana) — California; Texas; New York; Florida; Mountain Plains; Illinois; Puerto Rico; North Carolina; Georgia; Pennsylvania; Michigan; Arizona.
- 2014-05 (12 au-dessus) : plus petite au-dessus = 8,652,594 (New Jersey), plus grande en dessous = 7,730,901 (Washington) — California; New York; Mountain Plains; Texas; Puerto Rico; Florida; Illinois; Michigan; Georgia; North Carolina; Ohio; New Jersey.
- 2014-06 (12 au-dessus) : plus petite au-dessus = 8,998,388 (Ohio), plus grande en dessous = 8,784,754 (New Jersey) — California; Florida; New York; Texas; Mountain Plains; Illinois; Puerto Rico; Pennsylvania; North Carolina; Arizona; Michigan; Ohio.
- 2014-07 (12 au-dessus) : plus petite au-dessus = 10,136,511 (Illinois), plus grande en dessous = 9,390,049 (Ohio) — California; Texas; New York; Mountain Plains; Georgia; Puerto Rico; North Carolina; Florida; Pennsylvania; Michigan; Tennessee; Illinois.
- 2014-08 (12 au-dessus) : plus petite au-dessus = 9,255,570 (New Jersey), plus grande en dessous = 8,954,404 (Ohio) — California; New York; Mountain Plains; Florida; Texas; Pennsylvania; Puerto Rico; North Carolina; Georgia; Illinois; Michigan; New Jersey.
- 2014-09 (12 au-dessus) : plus petite au-dessus = 10,053,388 (Ohio), plus grande en dessous = 9,448,008 (Minnesota) — California; Texas; New York; Mountain Plains; Florida; Puerto Rico; North Carolina; Illinois; Georgia; Indiana; Michigan; Ohio.
- Cumulative (12 au-dessus) : plus petite au-dessus = 107,943,509 (Ohio), plus grande en dessous = 104,297,765 (New Jersey) — California; New York; Texas; Mountain Plains; Florida; Puerto Rico; Illinois; North Carolina; Georgia; Pennsylvania; Michigan; Ohio.

## Seuils propres par flux (top 10 de tout le banc, 182 seuils)

- contrôle 2014-08 : flux 2013-12 87.88 % (score 2.136).
- contrôle Cumulative : flux 2013-12 87.88 % (score 2.128).
- contrôle Cumulative : flux 2014-08 86.36 % (score 2.114).
- contrôle 2014-01 : flux 2013-12 87.88 % (score 2.104).
- contrôle 2014-04 : flux 2013-12 87.88 % (score 2.099).
- contrôle 2014-07 : flux 2014-08 87.88 % (score 2.076).
- contrôle 2014-01 : flux 2014-08 87.88 % (score 2.067).
- contrôle 2014-07 : flux 2013-12 86.36 % (score 2.062).
- contrôle 2014-06 : flux 2013-12 87.88 % (score 2.058).
- contrôle 2013-11 : flux 2014-08 86.36 % (score 2.040).

En tant que flux (moyenne sur les 13 runs où la colonne est flux) :
- 2013-12 : moyenne 1.863.
- 2014-08 : moyenne 1.845.
- Cumulative : moyenne 1.800.
- 2014-04 : moyenne 1.756.
- 2014-03 : moyenne 1.741.
- 2014-07 : moyenne 1.731.
- 2014-09 : moyenne 1.726.
- 2014-06 : moyenne 1.718.
- 2014-01 : moyenne 1.713.
- 2014-05 : moyenne 1.670.
- 2013-11 : moyenne 1.644.
- 2014-02 : moyenne 1.599.
- 2013-10 : moyenne 1.557.
- Agency : moyenne 0.779.

## Seuils propres par flux (top 3 par run)

| contrôle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| Agency (83.33 %) | 2013-12 42.42 % (0.412) | 2014-06 83.33 % (0.394) | 2014-03 83.33 % (0.392) |
| 2013-10 (87.88 %) | 2014-03 87.88 % (1.898) | Cumulative 87.88 % (1.832) | 2014-04 87.88 % (1.810) |
| 2013-11 (87.88 %) | 2014-08 86.36 % (2.040) | 2013-12 87.88 % (2.010) | 2014-07 84.85 % (1.998) |
| 2013-12 (87.88 %) | 2014-08 87.88 % (2.021) | Cumulative 87.88 % (1.972) | 2014-04 87.88 % (1.963) |
| 2014-01 (87.88 %) | 2013-12 87.88 % (2.104) | 2014-08 87.88 % (2.067) | Cumulative 87.88 % (1.974) |
| 2014-02 (87.88 %) | 2013-12 87.88 % (2.027) | 2014-08 86.36 % (2.008) | Cumulative 87.88 % (1.970) |
| 2014-03 (87.88 %) | Cumulative 87.88 % (1.908) | 2014-08 87.88 % (1.903) | 2014-09 87.88 % (1.866) |
| 2014-04 (87.88 %) | 2013-12 87.88 % (2.099) | 2014-08 87.88 % (2.027) | Cumulative 87.88 % (1.939) |
| 2014-05 (87.88 %) | 2014-03 87.88 % (1.962) | 2014-08 84.85 % (1.908) | Cumulative 87.88 % (1.896) |
| 2014-06 (87.88 %) | 2013-12 87.88 % (2.058) | 2014-08 87.88 % (1.891) | 2014-04 87.88 % (1.858) |
| 2014-07 (87.88 %) | 2014-08 87.88 % (2.076) | 2013-12 86.36 % (2.062) | Cumulative 86.36 % (1.957) |
| 2014-08 (87.88 %) | 2013-12 87.88 % (2.136) | Cumulative 87.88 % (1.995) | 2014-03 84.85 % (1.936) |
| 2014-09 (87.88 %) | 2013-12 87.88 % (1.812) | Cumulative 87.88 % (1.790) | 2014-07 69.70 % (1.785) |
| Cumulative (87.88 %) | 2013-12 87.88 % (2.128) | 2014-08 86.36 % (2.114) | 2014-04 87.88 % (1.951) |

Détail complet des 182 seuils propres (14 × 13) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- Agency : Q1_Calme_vs_Chaos = 0.427, Q2_Tension_Seuil = 1.424, Q3_Agressivite = 0.427, Q4_Persistence = 0.793, Q5_Active_Reactive = 0.498, Q5_Actif_Receptif = 0.498
- 2013-10 : Q1_Calme_vs_Chaos = 0.346, Q2_Tension_Seuil = 1.933, Q3_Agressivite = 0.346, Q4_Persistence = 1.077, Q5_Active_Reactive = 0.478, Q5_Actif_Receptif = 0.478
- 2013-11 : Q1_Calme_vs_Chaos = 0.406, Q2_Tension_Seuil = 2.355, Q3_Agressivite = 0.406, Q4_Persistence = 1.267, Q5_Active_Reactive = 0.493, Q5_Actif_Receptif = 0.493
- 2013-12 : Q1_Calme_vs_Chaos = 0.446, Q2_Tension_Seuil = 1.576, Q3_Agressivite = 0.446, Q4_Persistence = 1.475, Q5_Active_Reactive = 0.501, Q5_Actif_Receptif = 0.501
- 2014-01 : Q1_Calme_vs_Chaos = 0.471, Q2_Tension_Seuil = 1.442, Q3_Agressivite = 0.471, Q4_Persistence = 1.374, Q5_Active_Reactive = 0.494, Q5_Actif_Receptif = 0.494
- 2014-02 : Q1_Calme_vs_Chaos = 0.31, Q2_Tension_Seuil = 2.199, Q3_Agressivite = 0.31, Q4_Persistence = 1.523, Q5_Active_Reactive = 0.497, Q5_Actif_Receptif = 0.497
- 2014-03 : Q1_Calme_vs_Chaos = 0.41, Q2_Tension_Seuil = 1.799, Q3_Agressivite = 0.41, Q4_Persistence = 1.181, Q5_Active_Reactive = 0.457, Q5_Actif_Receptif = 0.457
- 2014-04 : Q1_Calme_vs_Chaos = 0.43, Q2_Tension_Seuil = 1.674, Q3_Agressivite = 0.43, Q4_Persistence = 1.541, Q5_Active_Reactive = 0.487, Q5_Actif_Receptif = 0.487
- 2014-05 : Q1_Calme_vs_Chaos = 0.408, Q2_Tension_Seuil = 1.78, Q3_Agressivite = 0.408, Q4_Persistence = 1.346, Q5_Active_Reactive = 0.456, Q5_Actif_Receptif = 0.456
- 2014-06 : Q1_Calme_vs_Chaos = 0.553, Q2_Tension_Seuil = 2.016, Q3_Agressivite = 0.553, Q4_Persistence = 1.217, Q5_Active_Reactive = 0.459, Q5_Actif_Receptif = 0.459
- 2014-07 : Q1_Calme_vs_Chaos = 0.481, Q2_Tension_Seuil = 1.718, Q3_Agressivite = 0.481, Q4_Persistence = 1.452, Q5_Active_Reactive = 0.49, Q5_Actif_Receptif = 0.49
- 2014-08 : Q1_Calme_vs_Chaos = 0.359, Q2_Tension_Seuil = 1.791, Q3_Agressivite = 0.359, Q4_Persistence = 1.499, Q5_Active_Reactive = 0.48, Q5_Actif_Receptif = 0.48
- 2014-09 : Q1_Calme_vs_Chaos = 0.322, Q2_Tension_Seuil = 1.691, Q3_Agressivite = 0.322, Q4_Persistence = 1.22, Q5_Active_Reactive = 0.498, Q5_Actif_Receptif = 0.498
- Cumulative : Q1_Calme_vs_Chaos = 0.421, Q2_Tension_Seuil = 1.692, Q3_Agressivite = 0.421, Q4_Persistence = 1.674, Q5_Active_Reactive = 0.486, Q5_Actif_Receptif = 0.486

## Dérivées F1/F2 post-seuil, flux « Tous »

estimateur              DFA  Higuchi   Hurst    Katz  SampleEn
controle                                                      
2013-10-01 00:00:00 -3.7282  -0.0618 -0.0559  0.0017    0.0176
2013-11-01 00:00:00 -4.3478  -0.0983 -0.0476 -0.0046    0.0413
2013-12-01 00:00:00 -3.7407  -0.0917 -0.0571  0.0007    0.0238
2014-01-01 00:00:00 -3.5164  -0.1047 -0.0226 -0.0011   -0.0010
2014-02-01 00:00:00 -4.0114  -0.0872 -0.0623 -0.0033    0.0131
2014-03-01 00:00:00 -3.1059  -0.0759 -0.0502  0.0011    0.0095
2014-04-01 00:00:00 -3.7724  -0.0875 -0.0643 -0.0036    0.0242
2014-05-01 00:00:00 -4.1799  -0.0881 -0.0432  0.0001    0.0422
2014-06-01 00:00:00 -3.1336  -0.0979 -0.0479 -0.0018    0.0200
2014-07-01 00:00:00 -4.3271  -0.1121 -0.0443 -0.0070    0.0197
2014-08-01 00:00:00 -3.7199  -0.0929 -0.0409  0.0005    0.0303
2014-09-01 00:00:00 -3.7134  -0.0941 -0.0801 -0.0050    0.0264
Cumulative Cost     -3.7763  -0.0851 -0.0630 -0.0018    0.0263
agency_encoded      -2.4198  -0.0921 -0.0092 -0.0006   -0.0107

Détail complet (980 lignes) : `tous_F1F2.csv`.

## Réserves

- Petit n : 92 lignes seulement (91 valides par contrôle numérique). Avec w_size 80, les fenêtres sont très larges par rapport à n (scan plafonné à n//2) : prudence accrue, pas de classement direct des scores avec les séries à grand n.
- Les lignes sont des agences/États, pas une série temporelle : le contrôle est un axe de rang, pas un temps.
- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier, pas un seuil géographique ou économique.
- Aucune conclusion de politique publique, budgétaire ou nutritionnelle tirée des seuils : mesures du pipeline sur ce fichier.