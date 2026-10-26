# Food_Costs 2013 (Kaggle jpmiller/publicassistance) x pipeline v3.3-H1 — Rapport des 14 contrôles

Protocole : `PROTOCOLE.md` (réglages gelés le 26 oct. 2026 avant le lot ; pilote de faisabilité Cumulative Cost à 11h24, mêmes réglages, puis protocole rédigé ~11h25, puis 13 autres runs ; lot interrompu par un redémarrage du service à 9/14, repris par les seuls manquants, terminé à 11h27).
Pipeline uploadé, tel quel : mode stable, w_size 80, cohen_d, graine 42, HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse les 13 autres colonnes numériques. Source : `data/Food_Costs_2013_original.csv` (WICAgencies2013ytd/Food_Costs.csv, 92 lignes, 14 colonnes, exercice WIC 2013, octobre 2012 à septembre 2013). Fichier de travail : copie exacte + `agency_encoded` + Cumulative Cost convertie en nombre (vérifiée égale à la somme des 12 mois, écart 0). Aucun seuil attendu pré-enregistré : lecture descriptive seulement, aucune conclusion de politique publique, budgétaire ou nutritionnelle.

## Écarts et pièges de structure (constatés avant / vérifiés sur le fichier)

- Le dataset complet compte 68 fichiers, dont 4 fichiers nommés Food_Costs.csv (2013, 2014, 2015, 2016) : seul 2013 est traité ici, les 3 autres années feront 3 autres PDF séparés.
- Texas apparaît deux fois : une ligne entièrement vide et une ligne réelle (Cumulative 303 294 654) ; chaque colonne mensuelle et Cumulative Cost ont donc 91 valeurs valides, pas 92.
- Une seule valeur mensuelle négative, conservée telle quelle : Pennsylvania, novembre 2012, −550 874.
- **Mountain Plains est une ligne d'agrégat** : 253 793 211, exactement la somme des 10 États et des 10 agences tribales du groupe Mountain Plains qui la précèdent dans le fichier (écart 0). Le total du fichier (4 751 013 254) double-compte donc 253,8 millions, et Mountain Plains figure à tort parmi les « 12 plus grandes ».
- Cumulative Cost est la somme exacte des 12 mois : ses runs ne sont pas indépendants des runs mensuels.

## Verdict en une ligne

**14/14 runs terminés, 0 échec** (durée totale des runs : 168.6 s, ~12 s par run). Stabilité (critère du pipeline) : VERY STABLE = 14. **Mais** cette note repose sur l'écart-type bootstrap (≈ 0, 7 valeurs bootstrap identiques), pas sur l'accord MC / moyenne bootstrap : écart de 28,79 points pour les 13 contrôles numériques et de 40,91 points pour Agency. La note VERY STABLE ne doit donc PAS être lue comme une confirmation du seuil MC.
Les 13 contrôles numériques donnent exactement le même seuil MC, **87,88 %** (défaut 59,26 %, moyenne bootstrap 59,09 %). Agency donne **83,33 %** (défaut 29,63 %, moyenne bootstrap 42,42 %). 87,88 %, c'est la coupure après les 12 plus grandes agences, qui totalisent 62,6 % du total du fichier sur Cumulative Cost. Les courbes de scan montent régulièrement jusqu'à 87,88 % puis s'arrêtent (plus de score au-delà) : ce n'est pas un pic intérieur, c'est le bord de la zone calculable qui isole la queue des très grandes agences.

## Synthèse par contrôle

| contrôle | n | seuil MC % | défaut % | MC−défaut | moy. bootstrap % | MC−moy. | stabilité | score MC | scan max | valeur au MC (médiane) | durée s |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Agency | 92 | 83.33 | 29.63 | +53.70 | 42.42 | +40.91 | VERY STABLE | 0.540 | 0.372 | 75 | 12.7 |
| 2012-10 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.511 | 1.729 | 8,920,038 | 13.0 |
| 2012-11 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.517 | 1.791 | 9,018,020 | 12.0 |
| 2012-12 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.512 | 1.742 | 8,902,786 | 12.9 |
| 2013-01 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.513 | 1.753 | 8,201,217 | 12.9 |
| 2013-02 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.851 | 8,948,880 | 13.0 |
| 2013-03 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.522 | 1.873 | 8,591,296 | 12.6 |
| 2013-04 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.521 | 1.848 | 9,325,388 | 13.1 |
| 2013-05 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.521 | 1.871 | 9,130,670 | 12.5 |
| 2013-06 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.860 | 8,893,980 | 12.9 |
| 2013-07 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.516 | 1.803 | 8,841,066 | 12.6 |
| 2013-08 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.516 | 1.808 | 10,155,447 | 12.4 |
| 2013-09 | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.520 | 1.854 | 9,219,730 | 7.7 |
| Cumulative | 91 | 87.88 | 59.26 | +28.62 | 59.09 | +28.79 | VERY STABLE | 0.522 | 1.875 | 113,207,358 | 8.3 |

## Groupes au-dessus du seuil MC par contrôle

- 2012-10 (12 au-dessus) : plus petite au-dessus = 8,920,038 (North Carolina), plus grande en dessous = 8,357,868 (Washington) — California; Texas; New York; Florida; Mountain Plains; Puerto Rico; Illinois; Georgia; Louisiana; Ohio; New Jersey; North Carolina.
- 2012-11 (12 au-dessus) : plus petite au-dessus = 9,018,020 (New Jersey), plus grande en dessous = 8,402,724 (Washington) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Georgia; Illinois; North Carolina; Ohio; Michigan; New Jersey.
- 2012-12 (12 au-dessus) : plus petite au-dessus = 8,902,786 (New Jersey), plus grande en dessous = 7,733,802 (Washington) — California; New York; Mountain Plains; Florida; Puerto Rico; Ohio; North Carolina; Georgia; Illinois; Michigan; Texas; New Jersey.
- 2013-01 (12 au-dessus) : plus petite au-dessus = 8,201,217 (Washington), plus grande en dessous = 7,139,525 (Louisiana) — California; New York; Texas; Mountain Plains; Florida; Pennsylvania; Puerto Rico; Illinois; Georgia; Michigan; New Jersey; Washington.
- 2013-02 (12 au-dessus) : plus petite au-dessus = 8,948,880 (New Jersey), plus grande en dessous = 7,856,760 (Washington) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Georgia; Illinois; North Carolina; Michigan; Ohio; New Jersey.
- 2013-03 (12 au-dessus) : plus petite au-dessus = 8,591,296 (New Jersey), plus grande en dessous = 8,474,119 (Ohio) — California; New York; Texas; Mountain Plains; Florida; Puerto Rico; Illinois; Georgia; Pennsylvania; Michigan; North Carolina; New Jersey.
- 2013-04 (12 au-dessus) : plus petite au-dessus = 9,325,388 (New Jersey), plus grande en dessous = 8,624,054 (Ohio) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Illinois; Georgia; North Carolina; Pennsylvania; Michigan; New Jersey.
- 2013-05 (12 au-dessus) : plus petite au-dessus = 9,130,670 (New Jersey), plus grande en dessous = 9,096,860 (Ohio) — California; New York; Texas; Mountain Plains; Florida; Puerto Rico; Illinois; Pennsylvania; Georgia; Michigan; North Carolina; New Jersey.
- 2013-06 (12 au-dessus) : plus petite au-dessus = 8,893,980 (Ohio), plus grande en dessous = 8,832,062 (New Jersey) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Michigan; Illinois; Georgia; North Carolina; Pennsylvania; Ohio.
- 2013-07 (12 au-dessus) : plus petite au-dessus = 8,841,066 (New Jersey), plus grande en dessous = 7,638,512 (Washington) — California; New York; Texas; Mountain Plains; Florida; Puerto Rico; Pennsylvania; Georgia; North Carolina; Ohio; Illinois; New Jersey.
- 2013-08 (12 au-dessus) : plus petite au-dessus = 10,155,447 (Ohio), plus grande en dessous = 9,248,991 (New Jersey) — California; New York; Florida; Mountain Plains; Puerto Rico; Georgia; Pennsylvania; North Carolina; Illinois; Michigan; Texas; Ohio.
- 2013-09 (12 au-dessus) : plus petite au-dessus = 9,219,730 (Ohio), plus grande en dessous = 8,596,771 (New Jersey) — California; Texas; Florida; Mountain Plains; Pennsylvania; Puerto Rico; New York; North Carolina; Georgia; Illinois; Michigan; Ohio.
- Cumulative (12 au-dessus) : plus petite au-dessus = 113,207,358 (Ohio), plus grande en dessous = 107,731,536 (New Jersey) — California; New York; Texas; Florida; Mountain Plains; Puerto Rico; Illinois; Georgia; North Carolina; Pennsylvania; Michigan; Ohio.

3 mois sur 12 (juin, août, septembre) partagent exactement le même groupe au-dessus que Cumulative Cost ; les autres mois en diffèrent par un membre échangé (sauf octobre 2012 et janvier 2013 : deux membres échangés). Ce n'est donc pas 13 seuils indépendants, c'est 13 fois la même queue de grandes agences.

## Seuils propres par flux (top 10 de tout le banc, 182 seuils)

- contrôle 2013-03 : flux 2013-06 87.88 % (score 2.179).
- contrôle 2013-05 : flux 2013-06 87.88 % (score 2.179).
- contrôle Cumulative : flux 2013-06 87.88 % (score 2.165).
- contrôle 2013-02 : flux 2013-06 87.88 % (score 2.134).
- contrôle 2013-02 : flux 2012-12 87.88 % (score 2.125).
- contrôle 2013-08 : flux 2013-06 87.88 % (score 2.113).
- contrôle 2013-04 : flux 2013-06 87.88 % (score 2.081).
- contrôle 2013-04 : flux 2013-09 87.88 % (score 2.081).
- contrôle 2013-06 : flux 2012-12 86.36 % (score 2.079).
- contrôle 2013-03 : flux 2013-05 87.88 % (score 2.078).

En tant que flux (moyenne sur les 13 runs où la colonne est flux) :
- 2013-06 : moyenne 1.935, max 2.179.
- 2012-12 : moyenne 1.904, max 2.125.
- Cumulative : moyenne 1.867, max 2.056.
- 2013-05 : moyenne 1.862, max 2.078.
- 2013-09 : moyenne 1.858, max 2.081.
- 2013-03 : moyenne 1.858, max 2.062.
- 2013-04 : moyenne 1.846, max 2.037.
- 2013-08 : moyenne 1.827, max 2.025.
- 2013-02 : moyenne 1.762, max 1.937.
- 2013-01 : moyenne 1.718, max 1.961.
- 2012-10 : moyenne 1.701, max 1.878.
- 2012-11 : moyenne 1.644, max 1.960.
- 2013-07 : moyenne 1.642, max 1.806.
- Agency : moyenne 0.775, max 0.845.

## Seuils propres par flux (top 3 par run)

| contrôle (MC %) | flux 1 | flux 2 | flux 3 |
|---|---|---|---|
| Agency (83.33 %) | 2012-12 42.42 % (0.431) | 2013-08 40.91 % (0.397) | 2013-06 42.42 % (0.396) |
| 2012-10 (87.88 %) | 2012-12 87.88 % (1.957) | 2013-09 80.30 % (1.901) | Cumulative 87.88 % (1.887) |
| 2012-11 (87.88 %) | 2012-12 87.88 % (2.053) | 2013-06 87.88 % (2.038) | Cumulative 87.88 % (1.957) |
| 2012-12 (87.88 %) | 2013-06 87.88 % (1.976) | Cumulative 86.36 % (1.925) | 2013-04 86.36 % (1.914) |
| 2013-01 (87.88 %) | 2013-06 87.88 % (2.037) | 2013-03 87.88 % (1.963) | 2013-05 87.88 % (1.963) |
| 2013-02 (87.88 %) | 2013-06 87.88 % (2.134) | 2012-12 87.88 % (2.125) | Cumulative 87.88 % (2.024) |
| 2013-03 (87.88 %) | 2013-06 87.88 % (2.179) | 2013-05 87.88 % (2.078) | 2013-09 87.88 % (2.069) |
| 2013-04 (87.88 %) | 2013-06 87.88 % (2.081) | 2013-09 87.88 % (2.081) | 2012-12 86.36 % (2.037) |
| 2013-05 (87.88 %) | 2013-06 87.88 % (2.179) | 2013-09 87.88 % (2.074) | 2013-03 87.88 % (2.062) |
| 2013-06 (87.88 %) | 2012-12 86.36 % (2.079) | 2013-05 87.88 % (2.068) | Cumulative 87.88 % (2.056) |
| 2013-07 (87.88 %) | 2012-12 86.36 % (1.997) | 2013-09 87.88 % (1.983) | Cumulative 87.88 % (1.970) |
| 2013-08 (87.88 %) | 2013-06 87.88 % (2.113) | 2012-12 84.85 % (2.020) | Cumulative 87.88 % (1.999) |
| 2013-09 (87.88 %) | 2012-12 87.88 % (2.078) | 2013-06 87.88 % (2.061) | 2013-04 87.88 % (2.018) |
| Cumulative (87.88 %) | 2013-06 87.88 % (2.165) | 2013-05 87.88 % (2.076) | 2013-09 87.88 % (2.073) |

Détail complet des 182 seuils propres (14 × 13) : `tous_seuils_par_flux.csv`.

## Scores Q moyens par run

- Agency : Q1_Calme_vs_Chaos = 0.384, Q2_Tension_Seuil = 1.403, Q3_Agressivite = 0.384, Q4_Persistence = 0.792, Q5_Active_Reactive = 0.501, Q5_Actif_Receptif = 0.501
- 2012-10 : Q1_Calme_vs_Chaos = 0.356, Q2_Tension_Seuil = 2.141, Q3_Agressivite = 0.356, Q4_Persistence = 1.183, Q5_Active_Reactive = 0.499, Q5_Actif_Receptif = 0.499
- 2012-11 : Q1_Calme_vs_Chaos = 0.335, Q2_Tension_Seuil = 2.035, Q3_Agressivite = 0.335, Q4_Persistence = 1.497, Q5_Active_Reactive = 0.485, Q5_Actif_Receptif = 0.485
- 2012-12 : Q1_Calme_vs_Chaos = 0.498, Q2_Tension_Seuil = 1.012, Q3_Agressivite = 0.498, Q4_Persistence = 1.399, Q5_Active_Reactive = 0.497, Q5_Actif_Receptif = 0.497
- 2013-01 : Q1_Calme_vs_Chaos = 0.38, Q2_Tension_Seuil = 2.322, Q3_Agressivite = 0.38, Q4_Persistence = 1.342, Q5_Active_Reactive = 0.496, Q5_Actif_Receptif = 0.496
- 2013-02 : Q1_Calme_vs_Chaos = 0.369, Q2_Tension_Seuil = 1.869, Q3_Agressivite = 0.369, Q4_Persistence = 1.574, Q5_Active_Reactive = 0.436, Q5_Actif_Receptif = 0.436
- 2013-03 : Q1_Calme_vs_Chaos = 0.393, Q2_Tension_Seuil = 1.718, Q3_Agressivite = 0.393, Q4_Persistence = 1.686, Q5_Active_Reactive = 0.487, Q5_Actif_Receptif = 0.487
- 2013-04 : Q1_Calme_vs_Chaos = 0.254, Q2_Tension_Seuil = 1.825, Q3_Agressivite = 0.254, Q4_Persistence = 1.457, Q5_Active_Reactive = 0.501, Q5_Actif_Receptif = 0.501
- 2013-05 : Q1_Calme_vs_Chaos = 0.463, Q2_Tension_Seuil = 1.291, Q3_Agressivite = 0.463, Q4_Persistence = 1.562, Q5_Active_Reactive = 0.496, Q5_Actif_Receptif = 0.496
- 2013-06 : Q1_Calme_vs_Chaos = 0.402, Q2_Tension_Seuil = 1.296, Q3_Agressivite = 0.402, Q4_Persistence = 1.545, Q5_Active_Reactive = 0.504, Q5_Actif_Receptif = 0.504
- 2013-07 : Q1_Calme_vs_Chaos = 0.322, Q2_Tension_Seuil = 1.668, Q3_Agressivite = 0.322, Q4_Persistence = 1.411, Q5_Active_Reactive = 0.49, Q5_Actif_Receptif = 0.49
- 2013-08 : Q1_Calme_vs_Chaos = 0.391, Q2_Tension_Seuil = 1.152, Q3_Agressivite = 0.391, Q4_Persistence = 1.299, Q5_Active_Reactive = 0.49, Q5_Actif_Receptif = 0.49
- 2013-09 : Q1_Calme_vs_Chaos = 0.474, Q2_Tension_Seuil = 1.453, Q3_Agressivite = 0.474, Q4_Persistence = 1.209, Q5_Active_Reactive = 0.488, Q5_Actif_Receptif = 0.488
- Cumulative : Q1_Calme_vs_Chaos = 0.404, Q2_Tension_Seuil = 1.813, Q3_Agressivite = 0.404, Q4_Persistence = 1.801, Q5_Active_Reactive = 0.505, Q5_Actif_Receptif = 0.505

## Dérivées F1/F2 post-seuil, flux « Tous »

estimateur              DFA  Higuchi   Hurst    Katz  SampleEn
controle                                                      
2012-10-01 00:00:00 -3.6825  -0.0876 -0.0707 -0.0041    0.0121
2012-11-01 00:00:00 -3.9882  -0.0726 -0.0678 -0.0009    0.0350
2012-12-01 00:00:00 -3.3320  -0.1011 -0.0315 -0.0093    0.0503
2013-01-01 00:00:00 -3.6798  -0.0772 -0.0603 -0.0023    0.0165
2013-02-01 00:00:00 -2.7710  -0.0769 -0.0609 -0.0027    0.0400
2013-03-01 00:00:00 -3.0752  -0.0794 -0.0619 -0.0017    0.0219
2013-04-01 00:00:00 -4.3106  -0.0802 -0.0653 -0.0020    0.0148
2013-05-01 00:00:00 -3.7125  -0.0828 -0.0504 -0.0022    0.0273
2013-06-01 00:00:00 -4.3080  -0.0837 -0.0463 -0.0030    0.0293
2013-07-01 00:00:00 -4.0990  -0.0853 -0.0539 -0.0032    0.0300
2013-08-01 00:00:00 -3.0783  -0.1017 -0.0159 -0.0092    0.0296
2013-09-01 00:00:00 -3.3762  -0.0996 -0.0246  0.0002    0.0087
Cumulative Cost     -4.3178  -0.0741 -0.0583 -0.0013    0.0033
agency_encoded      -2.8581  -0.0920 -0.0090 -0.0008   -0.0142

Détail complet (980 lignes) : `tous_F1F2.csv`.

## Réserves (gelées avant les runs, rappelées ici)

- Petit n : 92 lignes seulement (91 valides par contrôle numérique), contre 500–569 dans les séries précédentes. Avec w_size 80, les fenêtres sont très larges par rapport à n (la fonction de scan plafonne w_size à n//2) : prudence accrue, pas de classement direct des scores avec les séries à grand n.
- Les lignes sont des agences/États, pas une série temporelle : le contrôle est un axe de rang, pas un temps, même pour les colonnes mensuelles (les mois sont des colonnes, pas des lignes).
- `agency_encoded` est nominal : son seuil est une coupure dans l'ordre d'apparition des agences dans le fichier (bloc Western en fin de fichier au-dessus de 83,33 %), pas un seuil géographique ou économique.
- Aucune conclusion de politique publique, budgétaire ou nutritionnelle tirée des seuils : mesures du pipeline sur ce fichier.