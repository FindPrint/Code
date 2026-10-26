# Food_Costs 2016 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1 — Rapport des 14 contrôles

Protocole : `PROTOCOLE.md` (gelé le 26 oct. 2026 avant les runs de 2016, répétition exacte du protocole 2013). Pipeline uploadé, tel quel : mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse les 13 autres colonnes numériques. Source : `data/Food_Costs_2016_original.csv` (WICAgencies2016ytd/Food_Costs.csv, 92 lignes, 14 colonnes, exercice WIC 2016, 2015-10 à 2016-09). Fichier de travail : copie exacte + `agency_encoded` + Cumulative Cost convertie en nombre (vérifiée égale à la somme des 12 mois, écart 0). Aucun seuil attendu pré-enregistré : lecture descriptive seulement, aucune conclusion de politique publique, budgétaire ou nutritionnelle.

## Écarts et pièges de structure

- Le dataset complet compte 68 fichiers, dont 4 fichiers nommés Food_Costs.csv (2013, 2014, 2015, 2016) : seul 2016 est traité ici.
- Texas en double (ligne vide + ligne réelle) ; chaque colonne mensuelle et Cumulative Cost ont donc 91 valeurs valides, pas 92.
- Valeurs mensuelles négatives, conservées telles quelles : Maine, 2016-01, -121,621; Otoe-Missouria Tribe, OK, 2016-03, -4,446; Inter-Tribal Council, NV, 2016-03, -8,152.
- **Mountain Plains est une ligne d'agrégat** : 223,486,855, somme des 10 États + 10 agences tribales du groupe = 223,486,855, écart 0. Le total du fichier (4,172,825,280) double-compte donc cet agrégat, et Mountain Plains figure parmi les 12 plus grandes sans être une agence distincte.
- Cumulative Cost est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels.

## Verdict en une ligne

**14/14 runs terminés, 0 échec** (durée totale des runs : 171.3 s, ~12 s par run). Stabilité (critère du pipeline) : VERY STABLE = 14. **Mais** cette note repose sur l'écart-type bootstrap (≈ 0), pas sur l'accord MC / moyenne bootstrap : écart de 22.73 à 28.79 points pour les contrôles numériques et de 14.58 points pour Agency. La note VERY STABLE ne doit donc PAS être lue comme une confirmation du seuil MC.
Les contrôles numériques donnent entre 81,82 % et 87,88 % ; Agency donne 43.75 %. Le seuil MC, c'est la coupure après les 12 plus grandes agences, qui totalisent 62.3 % du total du fichier sur Cumulative Cost. Les courbes de scan montent régulièrement jusqu'au MC puis s'arrêtent : ce n'est pas un pic intérieur, c'est le bord de la zone calculable qui isole la queue des très grandes agences.

## Synthèse par contrôle

| contrôle | n | seuil MC % | défaut % | MC−défaut | moy. bootstrap % | MC−moy. | stabilité | score MC | scan max | valeur au MC (médiane) | durée s |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Agency | 92 | 43.75 | 29.63 | +14.12 | 29.17 | +14.58 | VERY STABLE | 0.389 | 0.567 | 39 | 20.9 |
| 2015-10 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.510 | 1.719 | 8,592,530 | 13.0 |
| 2015-11 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.513 | 1.754 | 8,402,906 | 10.9 |
| 2015-12 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.523 | 1.875 | 8,234,754 | 11.4 |
| 2016-01 | 91 | 81.82 | 59.26 | +22.56 | 59.09 | +22.73 | VERY STABLE | 0.507 | 1.678 | 6,058,150 | 10.6 |
| 2016-02 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.875 | 7,694,113 | 11.8 |
| 2016-03 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.515 | 1.796 | 7,492,381 | 10.8 |
| 2016-04 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.517 | 1.821 | 8,361,734 | 12.0 |
| 2016-05 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.519 | 1.842 | 9,190,082 | 12.1 |
| 2016-06 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.508 | 1.706 | 7,208,601 | 10.7 |
| 2016-07 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.514 | 1.771 | 9,130,205 | 12.6 |
| 2016-08 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.508 | 1.696 | 7,529,263 | 11.3 |
| 2016-09 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.515 | 1.805 | 9,078,139 | 12.1 |
| Cumulative | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.521 | 1.874 | 99,647,240 | 11.1 |

Note : pour Agency, la « valeur au MC » est un code d'agence, pas un montant.

## Groupes au-dessus du seuil MC par contrôle

- 2015-10 (12 au-dessus) : plus petite au-dessus = 8,592,530 (New Jersey), plus grande en dessous = 8,042,122 (Ohio) — California; Texas; New York; Florida; Mountain Plains; Illinois; Puerto Rico; North Carolina; Georgia; Tennessee; Michigan; New Jersey.
- 2015-11 (12 au-dessus) : plus petite au-dessus = 8,402,906 (Alabama), plus grande en dessous = 8,383,559 (New Jersey) — California; New York; Mountain Plains; Florida; Texas; Puerto Rico; Illinois; Georgia; North Carolina; Pennsylvania; Michigan; Alabama.
- 2015-12 (12 au-dessus) : plus petite au-dessus = 8,234,754 (New Jersey), plus grande en dessous = 7,658,575 (Ohio) — California; Texas; New York; Florida; Pennsylvania; Mountain Plains; Puerto Rico; Illinois; North Carolina; Georgia; Michigan; New Jersey.
- 2016-01 (17 au-dessus) : plus petite au-dessus = 6,112,731 (Maryland), plus grande en dessous = 6,003,569 (Alabama) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Ohio; Illinois; Georgia; Arizona; Michigan; North Carolina; New Jersey; Washington; Virginia; Louisiana; Maryland.
- 2016-02 (12 au-dessus) : plus petite au-dessus = 7,694,113 (New Jersey), plus grande en dessous = 7,145,204 (Ohio) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Pennsylvania; Georgia; North Carolina; Illinois; Michigan; New Jersey.
- 2016-03 (12 au-dessus) : plus petite au-dessus = 7,492,381 (Ohio), plus grande en dessous = 7,051,603 (Washington) — California; Texas; New York; Mountain Plains; Florida; Puerto Rico; Illinois; North Carolina; Georgia; Michigan; New Jersey; Ohio.
- 2016-04 (12 au-dessus) : plus petite au-dessus = 8,361,734 (Maryland), plus grande en dessous = 8,123,016 (New Jersey) — California; New York; Florida; Texas; Mountain Plains; Pennsylvania; Puerto Rico; North Carolina; Illinois; Georgia; Michigan; Maryland.
- 2016-05 (12 au-dessus) : plus petite au-dessus = 9,190,082 (Tennessee), plus grande en dessous = 8,238,098 (New Jersey) — California; Texas; New York; Florida; Mountain Plains; Illinois; Puerto Rico; Pennsylvania; North Carolina; Georgia; Michigan; Tennessee.
- 2016-06 (12 au-dessus) : plus petite au-dessus = 7,208,601 (Ohio), plus grande en dessous = 7,075,694 (Washington) — California; New York; Florida; Mountain Plains; Puerto Rico; North Carolina; Georgia; Illinois; Michigan; Texas; New Jersey; Ohio.
- 2016-07 (12 au-dessus) : plus petite au-dessus = 9,130,205 (Illinois), plus grande en dessous = 9,100,370 (Tennessee) — California; Texas; New York; Florida; Mountain Plains; Pennsylvania; Puerto Rico; North Carolina; Georgia; Michigan; Arizona; Illinois.
- 2016-08 (12 au-dessus) : plus petite au-dessus = 7,529,263 (Ohio), plus grande en dessous = 6,913,298 (Kentucky) — California; New York; Florida; Mountain Plains; Texas; Puerto Rico; North Carolina; Georgia; Michigan; Illinois; New Jersey; Ohio.
- 2016-09 (12 au-dessus) : plus petite au-dessus = 9,078,139 (Michigan), plus grande en dessous = 8,423,718 (New Jersey) — California; Texas; New York; Florida; Mountain Plains; Pennsylvania; Puerto Rico; Illinois; Ohio; North Carolina; Georgia; Michigan.
- Cumulative (12 au-dessus) : plus petite au-dessus = 99,647,240 (New Jersey), plus grande en dessous = 89,214,696 (Ohio) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Illinois; Pennsylvania; North Carolina; Georgia; Michigan; New Jersey.

## Seuils propres par flux (top 10 de tout le banc, 182 seuils)

- contrôle Cumulative : flux 2016-09 87.88 % (score 2.225).
- contrôle 2016-02 : flux 2016-09 87.88 % (score 2.216).
- contrôle 2015-12 : flux 2016-09 87.88 % (score 2.184).
- contrôle 2016-02 : flux 2015-12 87.88 % (score 2.168).
- contrôle Cumulative : flux 2015-12 87.88 % (score 2.152).
- contrôle Cumulative : flux 2016-04 86.36 % (score 2.116).
- contrôle 2016-04 : flux 2015-12 87.88 % (score 2.103).
- contrôle 2016-02 : flux 2016-04 87.88 % (score 2.095).
- contrôle 2015-12 : flux 2016-04 87.88 % (score 2.092).
- contrôle 2015-12 : flux Cumulative 87.88 % (score 2.073).

En tant que flux (moyenne sur les 13 runs où la colonne est flux) :
- 2016-09 : moyenne 1.890.
- 2016-04 : moyenne 1.882.
- Cumulative : moyenne 1.860.
- 2015-12 : moyenne 1.842.
- 2016-03 : moyenne 1.814.
- 2016-08 : moyenne 1.798.
- 2016-02 : moyenne 1.796.
- 2016-01 : moyenne 1.787.
- 2015-11 : moyenne 1.773.
- 2016-07 : moyenne 1.764.
- 2016-06 : moyenne 1.728.
- 2015-10 : moyenne 1.673.
- 2016-05 : moyenne 1.600.
- Agency : moyenne 0.808.

## Seuils propres par flux (top 3 par run)

| contrôle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| Agency (43.75 %) | 2016-08 43.75 % (0.643) | 2016-04 43.75 % (0.637) | 2016-06 43.75 % (0.604) |
| 2015-10 (87.88 %) | 2016-07 78.79 % (1.906) | Cumulative 87.88 % (1.879) | 2016-08 87.88 % (1.872) |
| 2015-11 (87.88 %) | 2016-04 87.88 % (2.014) | 2016-09 87.88 % (1.956) | Cumulative 87.88 % (1.946) |
| 2015-12 (87.88 %) | 2016-09 87.88 % (2.184) | 2016-04 87.88 % (2.092) | Cumulative 87.88 % (2.073) |
| 2016-01 (81.82 %) | 2016-04 77.27 % (1.956) | 2016-03 87.88 % (1.887) | 2016-09 87.88 % (1.884) |
| 2016-02 (87.88 %) | 2016-09 87.88 % (2.216) | 2015-12 87.88 % (2.168) | 2016-04 87.88 % (2.095) |
| 2016-03 (87.88 %) | 2016-01 87.88 % (2.034) | 2016-09 86.36 % (2.011) | Cumulative 87.88 % (1.977) |
| 2016-04 (87.88 %) | 2015-12 87.88 % (2.103) | 2016-09 87.88 % (2.051) | Cumulative 87.88 % (2.026) |
| 2016-05 (87.88 %) | 2015-12 87.88 % (2.072) | 2016-09 87.88 % (2.070) | 2016-04 87.88 % (2.043) |
| 2016-06 (87.88 %) | 2016-01 87.88 % (1.981) | 2016-03 87.88 % (1.912) | 2016-08 87.88 % (1.905) |
| 2016-07 (87.88 %) | 2016-09 87.88 % (2.017) | 2016-04 87.88 % (1.973) | Cumulative 87.88 % (1.967) |
| 2016-08 (87.88 %) | 2016-03 87.88 % (1.937) | 2016-04 75.76 % (1.898) | 2016-06 87.88 % (1.869) |
| 2016-09 (87.88 %) | 2015-12 87.88 % (2.033) | 2016-04 87.88 % (2.025) | Cumulative 87.88 % (2.016) |
| Cumulative (87.88 %) | 2016-09 87.88 % (2.225) | 2015-12 87.88 % (2.152) | 2016-04 86.36 % (2.116) |

Détail complet des 182 seuils propres (14 × 13) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- Agency : Q1_Calme_vs_Chaos = 1.674, Q2_Tension_Seuil = 3.806, Q3_Agressivite = 1.674, Q4_Persistence = 0.469, Q5_Active_Reactive = 1.738, Q5_Actif_Receptif = 1.738
- 2015-10 : Q1_Calme_vs_Chaos = 0.417, Q2_Tension_Seuil = 1.894, Q3_Agressivite = 0.417, Q4_Persistence = 1.253, Q5_Active_Reactive = 0.481, Q5_Actif_Receptif = 0.481
- 2015-11 : Q1_Calme_vs_Chaos = 0.424, Q2_Tension_Seuil = 1.791, Q3_Agressivite = 0.424, Q4_Persistence = 1.298, Q5_Active_Reactive = 0.479, Q5_Actif_Receptif = 0.479
- 2015-12 : Q1_Calme_vs_Chaos = 0.373, Q2_Tension_Seuil = 1.884, Q3_Agressivite = 0.373, Q4_Persistence = 1.202, Q5_Active_Reactive = 0.504, Q5_Actif_Receptif = 0.504
- 2016-01 : Q1_Calme_vs_Chaos = 0.45, Q2_Tension_Seuil = 0.747, Q3_Agressivite = 0.45, Q4_Persistence = 1.234, Q5_Active_Reactive = 0.487, Q5_Actif_Receptif = 0.487
- 2016-02 : Q1_Calme_vs_Chaos = 0.326, Q2_Tension_Seuil = 1.952, Q3_Agressivite = 0.326, Q4_Persistence = 1.329, Q5_Active_Reactive = 0.5, Q5_Actif_Receptif = 0.5
- 2016-03 : Q1_Calme_vs_Chaos = 0.366, Q2_Tension_Seuil = 2.425, Q3_Agressivite = 0.366, Q4_Persistence = 1.183, Q5_Active_Reactive = 0.48, Q5_Actif_Receptif = 0.48
- 2016-04 : Q1_Calme_vs_Chaos = 0.46, Q2_Tension_Seuil = 1.573, Q3_Agressivite = 0.46, Q4_Persistence = 1.394, Q5_Active_Reactive = 0.458, Q5_Actif_Receptif = 0.458
- 2016-05 : Q1_Calme_vs_Chaos = 0.391, Q2_Tension_Seuil = 2.209, Q3_Agressivite = 0.391, Q4_Persistence = 1.325, Q5_Active_Reactive = 0.497, Q5_Actif_Receptif = 0.497
- 2016-06 : Q1_Calme_vs_Chaos = 0.455, Q2_Tension_Seuil = 1.539, Q3_Agressivite = 0.455, Q4_Persistence = 1.051, Q5_Active_Reactive = 0.463, Q5_Actif_Receptif = 0.463
- 2016-07 : Q1_Calme_vs_Chaos = 0.348, Q2_Tension_Seuil = 1.696, Q3_Agressivite = 0.348, Q4_Persistence = 1.282, Q5_Active_Reactive = 0.495, Q5_Actif_Receptif = 0.495
- 2016-08 : Q1_Calme_vs_Chaos = 0.365, Q2_Tension_Seuil = 1.922, Q3_Agressivite = 0.365, Q4_Persistence = 1.267, Q5_Active_Reactive = 0.501, Q5_Actif_Receptif = 0.501
- 2016-09 : Q1_Calme_vs_Chaos = 0.328, Q2_Tension_Seuil = 1.843, Q3_Agressivite = 0.328, Q4_Persistence = 1.223, Q5_Active_Reactive = 0.498, Q5_Actif_Receptif = 0.498
- Cumulative : Q1_Calme_vs_Chaos = 0.408, Q2_Tension_Seuil = 2.218, Q3_Agressivite = 0.408, Q4_Persistence = 1.606, Q5_Active_Reactive = 0.503, Q5_Actif_Receptif = 0.503

## Dérivées F1/F2 post-seuil, flux « Tous »

estimateur              DFA  Higuchi   Hurst    Katz  SampleEn
controle                                                      
2015-10-01 00:00:00 -2.4981  -0.0859 -0.0684 -0.0039    0.0254
2015-11-01 00:00:00 -4.0277  -0.0934 -0.0714 -0.0006    0.0173
2015-12-01 00:00:00 -3.9145  -0.0803 -0.0449 -0.0006    0.0176
2016-01-01 00:00:00 -2.2193  -0.0601 -0.0111 -0.0042    0.0150
2016-02-01 00:00:00 -3.9862  -0.0826 -0.0482 -0.0022    0.0211
2016-03-01 00:00:00 -4.0023  -0.0698 -0.0498 -0.0008    0.0312
2016-04-01 00:00:00 -4.0994  -0.0912 -0.0487 -0.0014    0.0220
2016-05-01 00:00:00 -4.1087  -0.0860 -0.0633 -0.0029    0.0150
2016-06-01 00:00:00 -3.1254  -0.1002 -0.0157 -0.0035    0.0264
2016-07-01 00:00:00 -4.0851  -0.0979 -0.0558 -0.0065    0.0210
2016-08-01 00:00:00 -4.0070  -0.0886 -0.0589  0.0001    0.0282
2016-09-01 00:00:00 -3.3422  -0.0959 -0.0603 -0.0038    0.0243
Cumulative Cost     -4.1221  -0.0787 -0.0556 -0.0020    0.0169
agency_encoded       0.0833   0.0022 -0.0007  0.0008    0.0083

Détail complet (980 lignes) : `tous_F1F2.csv`.

## Réserves

- Petit n : 92 lignes seulement (91 valides par contrôle numérique). Avec w_size 80, les fenêtres sont très larges par rapport à n (scan plafonné à n//2) : prudence accrue, pas de classement direct des scores avec les séries à grand n.
- Les lignes sont des agences/États, pas une série temporelle : le contrôle est un axe de rang, pas un temps.
- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier, pas un seuil géographique ou économique.
- Aucune conclusion de politique publique, budgétaire ou nutritionnelle tirée des seuils : mesures du pipeline sur ce fichier.