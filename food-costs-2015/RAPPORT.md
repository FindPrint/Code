# Food_Costs 2015 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1 — Rapport des 14 contrôles

Protocole : `PROTOCOLE.md` (gelé le 26 oct. 2026 avant les runs de 2015, répétition exacte du protocole 2013). Pipeline uploadé, tel quel : mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse les 13 autres colonnes numériques. Source : `data/Food_Costs_2015_original.csv` (WICAgencies2015ytd/Food_Costs.csv, 92 lignes, 14 colonnes, exercice WIC 2015, 2014-10 à 2015-09). Fichier de travail : copie exacte + `agency_encoded` + Cumulative Cost convertie en nombre (vérifiée égale à la somme des 12 mois, écart 0). Aucun seuil attendu pré-enregistré : lecture descriptive seulement, aucune conclusion de politique publique, budgétaire ou nutritionnelle.

## Écarts et pièges de structure

- Le dataset complet compte 68 fichiers, dont 4 fichiers nommés Food_Costs.csv (2013, 2014, 2015, 2016) : seul 2015 est traité ici.
- Texas en double (ligne vide + ligne réelle) ; chaque colonne mensuelle et Cumulative Cost ont donc 91 valeurs valides, pas 92.
- Valeurs mensuelles négatives, conservées telles quelles : Navajo Nation, AZ, 2014-10, -5,806.
- **Mountain Plains est une ligne d'agrégat** : 239,859,968, somme des 10 États + 10 agences tribales du groupe = 239,859,968, écart 0. Le total du fichier (4,415,699,637) double-compte donc cet agrégat, et Mountain Plains figure parmi les 12 plus grandes sans être une agence distincte.
- Cumulative Cost est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels.

## Verdict en une ligne

**14/14 runs terminés, 0 échec** (durée totale des runs : 191.7 s, ~14 s par run). Stabilité (critère du pipeline) : VERY STABLE = 14. **Mais** cette note repose sur l'écart-type bootstrap (≈ 0), pas sur l'accord MC / moyenne bootstrap : écart de 24.14 à 28.79 points pour les contrôles numériques et de 40.91 points pour Agency. La note VERY STABLE ne doit donc PAS être lue comme une confirmation du seuil MC.
Les contrôles numériques donnent entre 82,76 % et 87,88 % ; Agency donne 83.33 %. Le seuil MC, c'est la coupure après les 12 plus grandes agences, qui totalisent 62.2 % du total du fichier sur Cumulative Cost. Les courbes de scan montent régulièrement jusqu'au MC puis s'arrêtent : ce n'est pas un pic intérieur, c'est le bord de la zone calculable qui isole la queue des très grandes agences.

## Synthèse par contrôle

| contrôle | n | seuil MC % | défaut % | MC−défaut | moy. bootstrap % | MC−moy. | stabilité | score MC | scan max | valeur au MC (médiane) | durée s |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Agency | 92 | 83.33 | 29.63 | +53.70 | 42.42 | +40.91 | VERY STABLE | 0.540 | 0.374 | 75 | 15.2 |
| 2014-10 | 91 | 82.76 | 59.26 | +23.50 | 58.62 | +24.14 | VERY STABLE | 0.518 | 1.569 | 6,689,267 | 18.3 |
| 2014-11 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.519 | 1.859 | 8,670,890 | 12.5 |
| 2014-12 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.846 | 9,188,793 | 13.1 |
| 2015-01 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.517 | 1.811 | 8,989,280 | 13.2 |
| 2015-02 | 91 | 86.36 | 59.26 | +27.10 | 59.09 | +27.27 | VERY STABLE | 0.515 | 1.786 | 7,935,520 | 13.3 |
| 2015-03 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.512 | 1.750 | 9,344,641 | 12.7 |
| 2015-04 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.857 | 9,022,004 | 13.6 |
| 2015-05 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.858 | 8,384,120 | 13.2 |
| 2015-06 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.509 | 1.704 | 7,475,704 | 13.3 |
| 2015-07 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.517 | 1.811 | 9,328,988 | 13.6 |
| 2015-08 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.512 | 1.741 | 9,368,011 | 13.8 |
| 2015-09 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.510 | 1.704 | 9,616,630 | 13.3 |
| Cumulative | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.521 | 1.872 | 103,757,360 | 12.6 |

Note : pour Agency, la « valeur au MC » est un code d'agence, pas un montant.

## Groupes au-dessus du seuil MC par contrôle

- 2014-10 (16 au-dessus) : plus petite au-dessus = 7,211,240 (Arizona), plus grande en dessous = 6,689,267 (Indiana) — California; Texas; New York; Florida; Mountain Plains; Illinois; Puerto Rico; North Carolina; Georgia; Michigan; New Jersey; Ohio; Alabama; Washington; Pennsylvania; Arizona.
- 2014-11 (12 au-dessus) : plus petite au-dessus = 8,670,890 (Ohio), plus grande en dessous = 8,619,354 (New Jersey) — California; New York; Texas; Mountain Plains; Florida; Puerto Rico; Illinois; Georgia; Michigan; Pennsylvania; North Carolina; Ohio.
- 2014-12 (12 au-dessus) : plus petite au-dessus = 9,188,793 (Alabama), plus grande en dessous = 8,985,757 (Ohio) — California; Texas; New York; Florida; Mountain Plains; Pennsylvania; Illinois; Puerto Rico; North Carolina; Georgia; Michigan; Alabama.
- 2015-01 (12 au-dessus) : plus petite au-dessus = 8,989,280 (New Jersey), plus grande en dessous = 8,388,439 (Maryland) — California; New York; Mountain Plains; Texas; Florida; Puerto Rico; Illinois; Pennsylvania; Georgia; Michigan; North Carolina; New Jersey.
- 2015-02 (13 au-dessus) : plus petite au-dessus = 7,989,509 (New Jersey), plus grande en dessous = 7,881,532 (Alabama) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Ohio; Illinois; Georgia; Michigan; Pennsylvania; Maryland; New Jersey.
- 2015-03 (12 au-dessus) : plus petite au-dessus = 9,344,641 (Tennessee), plus grande en dessous = 9,265,841 (Michigan) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Illinois; Pennsylvania; North Carolina; Georgia; Arizona; Tennessee.
- 2015-04 (12 au-dessus) : plus petite au-dessus = 9,022,004 (Ohio), plus grande en dessous = 8,670,263 (New Jersey) — California; New York; Texas; Florida; Mountain Plains; Pennsylvania; Illinois; Puerto Rico; North Carolina; Georgia; Michigan; Ohio.
- 2015-05 (12 au-dessus) : plus petite au-dessus = 8,384,120 (New Jersey), plus grande en dessous = 8,355,243 (Ohio) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Illinois; Georgia; Pennsylvania; North Carolina; Michigan; New Jersey.
- 2015-06 (12 au-dessus) : plus petite au-dessus = 7,475,704 (Washington), plus grande en dessous = 6,328,350 (Alabama) — California; New York; Florida; Mountain Plains; Texas; Puerto Rico; Illinois; North Carolina; Georgia; Michigan; New Jersey; Washington.
- 2015-07 (12 au-dessus) : plus petite au-dessus = 9,328,988 (Illinois), plus grande en dessous = 9,046,162 (New Jersey) — California; Texas; New York; Mountain Plains; Florida; Puerto Rico; Ohio; Pennsylvania; North Carolina; Georgia; Michigan; Illinois.
- 2015-08 (12 au-dessus) : plus petite au-dessus = 9,368,011 (Michigan), plus grande en dessous = 8,907,030 (Alabama) — California; Texas; New York; Florida; Mountain Plains; Pennsylvania; Puerto Rico; North Carolina; Georgia; Tennessee; Illinois; Michigan.
- 2015-09 (12 au-dessus) : plus petite au-dessus = 9,616,630 (Michigan), plus grande en dessous = 8,568,137 (New Jersey) — California; New York; Mountain Plains; Florida; Texas; Puerto Rico; Pennsylvania; North Carolina; Georgia; Arizona; Illinois; Michigan.
- Cumulative (12 au-dessus) : plus petite au-dessus = 103,757,360 (New Jersey), plus grande en dessous = 101,852,969 (Ohio) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Illinois; Pennsylvania; North Carolina; Georgia; Michigan; New Jersey.

## Seuils propres par flux (top 10 de tout le banc, 182 seuils)

- contrôle Cumulative : flux 2015-04 87.88 % (score 2.184).
- contrôle 2015-05 : flux 2015-04 87.88 % (score 2.156).
- contrôle 2014-12 : flux 2015-04 87.88 % (score 2.141).
- contrôle 2014-11 : flux 2015-04 87.88 % (score 2.130).
- contrôle 2015-07 : flux 2015-04 87.88 % (score 2.104).
- contrôle 2015-04 : flux 2015-09 86.36 % (score 2.092).
- contrôle Cumulative : flux 2015-09 87.88 % (score 2.084).
- contrôle 2015-07 : flux 2015-03 83.33 % (score 2.079).
- contrôle 2015-02 : flux 2015-08 80.30 % (score 2.074).
- contrôle Cumulative : flux 2014-12 87.88 % (score 2.069).

En tant que flux (moyenne sur les 13 runs où la colonne est flux) :
- 2015-04 : moyenne 1.885.
- 2015-03 : moyenne 1.849.
- 2015-09 : moyenne 1.836.
- 2015-08 : moyenne 1.832.
- 2014-12 : moyenne 1.825.
- Cumulative : moyenne 1.804.
- 2015-07 : moyenne 1.774.
- 2015-02 : moyenne 1.764.
- 2014-10 : moyenne 1.751.
- 2014-11 : moyenne 1.699.
- 2015-06 : moyenne 1.663.
- 2015-01 : moyenne 1.638.
- 2015-05 : moyenne 1.623.
- Agency : moyenne 0.805.

## Seuils propres par flux (top 3 par run)

| contrôle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| Agency (83.33 %) | 2015-09 83.33 % (0.404) | 2015-01 83.33 % (0.398) | 2015-08 43.94 % (0.391) |
| 2014-10 (82.76 %) | 2015-08 74.14 % (1.812) | 2015-03 82.76 % (1.738) | 2015-02 81.03 % (1.712) |
| 2014-11 (87.88 %) | 2015-04 87.88 % (2.130) | 2015-08 84.85 % (2.025) | Cumulative 87.88 % (2.000) |
| 2014-12 (87.88 %) | 2015-04 87.88 % (2.141) | 2015-09 86.36 % (2.032) | 2015-03 84.85 % (2.021) |
| 2015-01 (87.88 %) | 2015-04 87.88 % (2.051) | 2015-09 86.36 % (2.036) | 2015-08 87.88 % (1.948) |
| 2015-02 (86.36 %) | 2015-08 80.30 % (2.074) | 2015-04 86.36 % (2.044) | 2015-03 75.76 % (1.949) |
| 2015-03 (87.88 %) | 2015-08 87.88 % (1.994) | 2014-12 87.88 % (1.967) | 2015-09 87.88 % (1.956) |
| 2015-04 (87.88 %) | 2015-09 86.36 % (2.092) | 2014-12 87.88 % (2.052) | 2015-03 87.88 % (2.050) |
| 2015-05 (87.88 %) | 2015-04 87.88 % (2.156) | 2014-12 87.88 % (2.052) | 2015-03 87.88 % (2.049) |
| 2015-06 (87.88 %) | 2015-03 87.88 % (1.912) | 2014-10 87.88 % (1.872) | 2015-04 87.88 % (1.863) |
| 2015-07 (87.88 %) | 2015-04 87.88 % (2.104) | 2015-03 83.33 % (2.079) | 2015-09 86.36 % (2.011) |
| 2015-08 (87.88 %) | 2015-02 78.79 % (1.971) | 2015-03 83.33 % (1.956) | 2014-12 87.88 % (1.933) |
| 2015-09 (87.88 %) | 2015-04 87.88 % (2.023) | 2015-03 87.88 % (2.001) | 2014-12 87.88 % (1.881) |
| Cumulative (87.88 %) | 2015-04 87.88 % (2.184) | 2015-09 87.88 % (2.084) | 2014-12 87.88 % (2.069) |

Détail complet des 182 seuils propres (14 × 13) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- Agency : Q1_Calme_vs_Chaos = 0.423, Q2_Tension_Seuil = 1.469, Q3_Agressivite = 0.423, Q4_Persistence = 0.791, Q5_Active_Reactive = 0.499, Q5_Actif_Receptif = 0.499
- 2014-10 : Q1_Calme_vs_Chaos = 1.002, Q2_Tension_Seuil = 1.811, Q3_Agressivite = 1.002, Q4_Persistence = 1.3, Q5_Active_Reactive = 2.191, Q5_Actif_Receptif = 2.191
- 2014-11 : Q1_Calme_vs_Chaos = 0.389, Q2_Tension_Seuil = 2.098, Q3_Agressivite = 0.389, Q4_Persistence = 1.422, Q5_Active_Reactive = 0.474, Q5_Actif_Receptif = 0.474
- 2014-12 : Q1_Calme_vs_Chaos = 0.321, Q2_Tension_Seuil = 1.921, Q3_Agressivite = 0.321, Q4_Persistence = 1.293, Q5_Active_Reactive = 0.51, Q5_Actif_Receptif = 0.51
- 2015-01 : Q1_Calme_vs_Chaos = 0.411, Q2_Tension_Seuil = 3.004, Q3_Agressivite = 0.411, Q4_Persistence = 1.364, Q5_Active_Reactive = 0.502, Q5_Actif_Receptif = 0.502
- 2015-02 : Q1_Calme_vs_Chaos = 0.611, Q2_Tension_Seuil = 1.081, Q3_Agressivite = 0.611, Q4_Persistence = 1.093, Q5_Active_Reactive = 0.492, Q5_Actif_Receptif = 0.492
- 2015-03 : Q1_Calme_vs_Chaos = 0.386, Q2_Tension_Seuil = 2.323, Q3_Agressivite = 0.386, Q4_Persistence = 1.493, Q5_Active_Reactive = 0.481, Q5_Actif_Receptif = 0.481
- 2015-04 : Q1_Calme_vs_Chaos = 0.39, Q2_Tension_Seuil = 1.747, Q3_Agressivite = 0.39, Q4_Persistence = 1.526, Q5_Active_Reactive = 0.488, Q5_Actif_Receptif = 0.488
- 2015-05 : Q1_Calme_vs_Chaos = 0.417, Q2_Tension_Seuil = 1.971, Q3_Agressivite = 0.417, Q4_Persistence = 1.342, Q5_Active_Reactive = 0.478, Q5_Actif_Receptif = 0.478
- 2015-06 : Q1_Calme_vs_Chaos = 0.422, Q2_Tension_Seuil = 2.309, Q3_Agressivite = 0.422, Q4_Persistence = 1.317, Q5_Active_Reactive = 0.494, Q5_Actif_Receptif = 0.494
- 2015-07 : Q1_Calme_vs_Chaos = 0.406, Q2_Tension_Seuil = 2.107, Q3_Agressivite = 0.406, Q4_Persistence = 1.507, Q5_Active_Reactive = 0.487, Q5_Actif_Receptif = 0.487
- 2015-08 : Q1_Calme_vs_Chaos = 0.464, Q2_Tension_Seuil = 1.544, Q3_Agressivite = 0.464, Q4_Persistence = 1.458, Q5_Active_Reactive = 0.491, Q5_Actif_Receptif = 0.491
- 2015-09 : Q1_Calme_vs_Chaos = 0.325, Q2_Tension_Seuil = 1.787, Q3_Agressivite = 0.325, Q4_Persistence = 1.288, Q5_Active_Reactive = 0.497, Q5_Actif_Receptif = 0.497
- Cumulative : Q1_Calme_vs_Chaos = 0.39, Q2_Tension_Seuil = 2.053, Q3_Agressivite = 0.39, Q4_Persistence = 1.701, Q5_Active_Reactive = 0.489, Q5_Actif_Receptif = 0.489

## Dérivées F1/F2 post-seuil, flux « Tous »

estimateur              DFA  Higuchi   Hurst    Katz  SampleEn
controle                                                      
2014-10-01 00:00:00 -0.0106  -0.0018  0.0050 -0.0010    0.0182
2014-11-01 00:00:00 -3.3396  -0.0877 -0.0650 -0.0021    0.0246
2014-12-01 00:00:00 -4.2133  -0.0874 -0.0680 -0.0033    0.0263
2015-01-01 00:00:00 -4.0334  -0.0800 -0.0524 -0.0003    0.0195
2015-02-01 00:00:00 -4.0218  -0.0994 -0.0381 -0.0056    0.0264
2015-03-01 00:00:00 -3.6680  -0.0825 -0.0410 -0.0023    0.0275
2015-04-01 00:00:00 -3.9566  -0.0849 -0.0623 -0.0022    0.0360
2015-05-01 00:00:00 -3.2796  -0.0794 -0.0629 -0.0020    0.0238
2015-06-01 00:00:00 -3.0472  -0.0749 -0.0439 -0.0004    0.0423
2015-07-01 00:00:00 -3.3288  -0.0923 -0.0510 -0.0040    0.0254
2015-08-01 00:00:00 -3.7473  -0.1009 -0.0643 -0.0070    0.0318
2015-09-01 00:00:00 -3.7469  -0.0973 -0.0618 -0.0023    0.0238
Cumulative Cost     -3.6549  -0.0733 -0.0521 -0.0014    0.0197
agency_encoded      -3.1303  -0.0920 -0.0092 -0.0006   -0.0112

Détail complet (980 lignes) : `tous_F1F2.csv`.

## Réserves

- Petit n : 92 lignes seulement (91 valides par contrôle numérique). Avec w_size 80, les fenêtres sont très larges par rapport à n (scan plafonné à n//2) : prudence accrue, pas de classement direct des scores avec les séries à grand n.
- Les lignes sont des agences/États, pas une série temporelle : le contrôle est un axe de rang, pas un temps.
- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier, pas un seuil géographique ou économique.
- Aucune conclusion de politique publique, budgétaire ou nutritionnelle tirée des seuils : mesures du pipeline sur ce fichier.