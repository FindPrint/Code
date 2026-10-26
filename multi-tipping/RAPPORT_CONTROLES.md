# Rapport — Tous les flux en contrôle, à tour de rôle (harmonique v1, 35 runs)

Protocole gelé avant les runs : `PROTOCOLE_CONTROLES.md` (confirmé par l'utilisateur
le 25 oct. 2026, 19 h 49 HAE : pipeline harmonique v1, périmètre complet).
Pipeline `pipeline_autonome_v3_3_harmonic_v1.py` tel quel, mode stable, w80, cohen_d,
graine 42, guidage harmonique par défaut (0,45), aveugle, contrôle toujours EXCLU
des flux analysés (règle porte D). 35 runs, 11 847 s de calcul cumulé (moyenne 338,5 s),
deux redémarrages machine absorbés par le design résumable (7 puis 33 runs sauvegardés
avant chaque reprise ; 0 run perdu, 0 run refait inutilement).

## VERDICT GLOBAL

1. **Le seuil global du pipeline est un détecteur de la PREMIÈRE rupture dominante,
   pas un sélecteur de transition.** Sur AT, quel que soit le contrôle, le seuil
   global ne pointe JAMAIS vers T2 : il pointe vers T1 (ou juste sous T1) dans les
   20 runs à attente définie — y compris quand le contrôle est magnetization_prod
   ou flip_rate, pour lesquels le protocole attendait T2. Attente « prod/flip → T2 »
   réfutée : 0/8, même en comptant les compatibilités à ±1 écart-type.
2. **La lecture par flux, elle, résout les deux transitions quel que soit le
   contrôle monotone.** Les flux pointent vers leur propre transition dans 19–20/20
   cas (compatibles ±1 std) et JAMAIS vers la mauvaise transition (0 croisement
   strict) : m_s/m_tau → T1, m_prod/flip_rate → T2. local_variance (flux) pointe
   toujours tôt (T ≈ 4,0–4,3, 20/20 hors fenêtres) : précurseur, pas transition.
3. **La qualité du contrôle décide de la qualité de la lecture.** Contrôles
   monotones (|Spearman| ≥ 0,93) : lecture par flux propre. Contrôle local_variance
   (Spearman 0,73, non monotone) : seuils propres dégradés (17/20 hors fenêtres,
   moyennes par flux rabattues vers 4,0–4,6) et seuil global stable mais précoce
   (T ≈ 4,1–4,4, VERY STABLE dans les 4 jeux AT).
4. **Horloge q=6 : aucun contrôle ne sauve les positions publiées.** Globaux tous
   hors fenêtres (T ≈ 1,04–1,10), stabilité mélangée. Par flux : energy/flip_rate
   touchent T1 dans 2/5 runs chacun ; magnetization/vortex_density/local_variance
   restent groupés vers T ≈ 1,04–1,13 (le haut du jeu L=24, comme en porte C).
5. **Nul B2 : discrimination par les scores, totale ; par la stabilité, 5/6.**
   Scores par flux 0,205 en moyenne contre 3,894 en réel (~19×) ; max de courbe
   0,111–0,135 contre ~3,5 en réel ; seuils dispersés (8–88 %). Stabilité : 5/6
   UNSTABLE — mais 1/6 VERY STABLE résiduel (contrôle magnetization_s, 81,86 %,
   std 1,64), à consigner : la stabilité seule n'est pas un critère suffisant.

## 1. Seuils globaux AT (24 runs, tous VERY STABLE)

| Jeu | Contrôle | Global % | T mappée | Hit | Attendu | Spearman |
|---|---|---|---|---|---|---|
| at | magnetization_s | 45,09 | 4,835 | T1 | T1 | −0,946 |
| at | magnetization_tau | 44,71 | 4,830 | T1 | T1 | −0,939 |
| at | magnetization_prod | 44,71 | 4,800 | T1 | T2 | −0,961 |
| at | energy | 56,55 | 4,878 | T1 | T1 | 0,991 |
| at | flip_rate | 54,10 | 4,703 | T1 | T2 | 0,997 |
| at | local_variance | 39,63 | 4,149 | hors | — | 0,731 |
| at_s7 | magnetization_s | 48,03 | 4,643 | T1 | T1 | −0,943 |
| at_s7 | magnetization_tau | 47,60 | 4,656 | T1 | T1 | −0,940 |
| at_s7 | magnetization_prod | 47,74 | 4,578 | hors | T2 | −0,961 |
| at_s7 | energy | 51,76 | 4,592 | hors | T1 | 0,992 |
| at_s7 | flip_rate | 51,67 | 4,578 | hors | T2 | 0,997 |
| at_s7 | local_variance | 43,33 | 4,608 | T1 | — | 0,736 |
| at_s123 | magnetization_s | 48,87 | 4,570 | hors | T1 | −0,929 |
| at_s123 | magnetization_tau | 48,18 | 4,646 | T1 | T1 | −0,930 |
| at_s123 | magnetization_prod | 48,87 | 4,592 | hors | T2 | −0,963 |
| at_s123 | energy | 51,76 | 4,603 | T1 | T1 | 0,992 |
| at_s123 | flip_rate | 50,95 | 4,533 | hors | T2 | 0,997 |
| at_s123 | local_variance | 41,92 | 4,073 | hors | — | 0,728 |
| at_L36 | magnetization_s | 46,05 | 4,741 | T1 | T1 | −0,938 |
| at_L36 | magnetization_tau | 46,17 | 4,732 | T1 | T1 | −0,935 |
| at_L36 | magnetization_prod | 46,05 | 4,705 | T1 | T2 | −0,962 |
| at_L36 | energy | 53,53 | 4,689 | T1 | T1 | 0,995 |
| at_L36 | flip_rate | 53,53 | 4,678 | T1 | T2 | 0,998 |
| at_L36 | local_variance | 41,88 | 4,358 | hors | — | 0,739 |

Comptes : hits stricts sur attente 10/20 ; compatibles à ±1 écart-type 12/20.
Les 8 incompatibles sont tous des contrôles m_prod/flip_rate pointant vers la
région T1 (4,53–4,80), jamais vers T2. Les 2 « hors » parmi energy/m_s/m_tau
(at_s7/energy 4,592 ; at_s123/m_s 4,570) sont à moins d'un écart-type de la fenêtre
T1 : ce sont des cas limites, pas des ratés francs. Scores MC globaux AT :
0,740–0,763 (moyenne 0,755) — remarquablement constants quel que soit le contrôle.

## 2. Seuils propres par flux AT (chaque flux pointe-t-il vers SA transition ?)

Stricts / compatibles ±1 std (sur 20 runs par flux) :
- magnetization_s → T1 : 9 stricts, 19 compatibles ; « hors » stricts presque tous
  à 4,53–4,59 (juste sous la fenêtre), sauf 4,149 (run contrôle local_variance) et
  4,95 (limite haute).
- magnetization_tau → T1 : 9 stricts, 20 compatibles.
- magnetization_prod → T2 : 12 stricts, 19 compatibles ; « hors » : 5,12–5,19
  (juste sous T2) et 4,11–4,44 (runs contrôle local_variance).
- flip_rate → T2 : 13 stricts, 18 compatibles.
- **Croisements : 0.** Aucun flux ne pointe strictement vers la transition de
  l'autre groupe (m_s/m_tau vers T2 : 0 ; m_prod/flip vers T1 : 0).
- local_variance (flux) : 20/20 hors, T = 3,98–4,33 — précurseur systématique.
- energy (flux, dans les 20 runs où le contrôle n'est pas energy) : T1 11 fois,
  T2 1 fois, hors 8 fois (T de 4,07 à 5,23) — mélange des deux transitions, comme
  en vague 1 (seuil propre 61 % entre les deux).

Moyennes des T propres par contrôle (AT, 4 jeux) : contrôle energy → s/tau
4,55–4,58, prod/flip 5,34–5,39 (séparation la plus propre) ; contrôle m_s →
s/tau 4,60–4,71, prod/flip 5,30–5,35 ; contrôle m_tau → 4,60–4,76 / 5,24–5,26 ;
contrôle m_prod → s/tau 4,59, prod/flip 5,33–5,51, energy 5,03 ; contrôle
flip_rate → s/tau 4,60, prod 5,33, energy 4,89 ; contrôle local_variance →
tout rabattu : energy 4,30, flip 4,26, prod 4,46, s/tau 4,56 (17/20 hors).

## 3. Horloge q=6 (5 runs)

| Contrôle | Global % | T mappée | Hit | Stabilité | Spearman |
|---|---|---|---|---|---|
| magnetization | 15,34 | 1,100 | hors | VERY STABLE | −0,974 |
| energy | 84,92 | 1,089 | hors | MODERATELY STABLE | 0,991 |
| flip_rate | 84,92 | 1,089 | hors | MODERATELY STABLE | 0,997 |
| vortex_density | 84,16 | 1,076 | hors | UNSTABLE | 0,925 |
| local_variance | 80,10 | 1,039 | hors | VERY STABLE | 0,931 |

Par flux (T par run, 4 runs par flux — le run où il est contrôle l'exclut) :
- energy : 0,656 / 0,800 / 0,997 / 1,100 → T1 dans 2/5 runs (0,656 ; 0,800 en bord
  de fenêtre [0,62 ; 0,80]).
- flip_rate : 0,543 / 0,610 / 0,626 / 0,789 → T1 dans 2/5 runs (0,626 ; 0,789).
- magnetization : 1,037 / 1,076 / 1,091 / 1,128 → 0 hit.
- vortex_density : 1,082 / 1,089 / 1,089 / 1,100 → 0 hit.
- local_variance : 1,083 / 1,102 / 1,119 / 1,127 → 0 hit.
Conclusion horloge inchangée depuis la porte C, et généralisée : changer de
contrôle ne déplace pas les lectures vers les positions publiées ; les flux
« hauts » restent groupés vers T ≈ 1,04–1,13, c'est-à-dire vers le haut réel du
jeu L=24 (vortex tardifs), pas vers T2 = 0,88.

## 4. Nul B2 (6 runs, contrôle exclu des flux)

| Contrôle | Global % | Stabilité (std) | Score MC | Max courbe |
|---|---|---|---|---|
| magnetization_s | 81,86 | VERY STABLE (1,64) | 0,662 | 0,127 |
| magnetization_tau | 43,20 | UNSTABLE (17,44) | 0,523 | 0,115 |
| magnetization_prod | 8,01 | UNSTABLE (40,83) | 0,557 | 0,135 |
| energy | 86,44 | UNSTABLE (18,51) | 0,603 | 0,131 |
| flip_rate | 17,86 | UNSTABLE (39,75) | 0,518 | 0,130 |
| local_variance | 28,19 | UNSTABLE (35,40) | 0,557 | 0,111 |

Seuils par flux dispersés (8–89 %, aucune grappe), scores par flux max
0,212–0,326 par run, moyenne 0,205 contre 3,894 en réel (~19×). Le résidu à
consigner : le nul contrôle magnetization_s reste VERY STABLE — la stabilité
globale seule ne suffit pas à déclarer un nul ; le couple (scores effondrés +
dispersion) discrimine, lui, dans les 6/6 cas.

## 5. Harmonique vs fixed (contrôle = energy, mêmes jeux)

| Jeu | Fixed (vague 2 / porte D) | Harmonique (ce lot) | T mappée fixed | T mappée harm. |
|---|---|---|---|---|
| at | 54,16 % | 56,55 % | 4,724 | 4,878 |
| at_s7 | 52,20 % | 51,76 % | 4,592 | 4,592 |
| at_s123 | 51,51 % | 51,76 % | 4,586 | 4,603 |
| at_L36 | 56,35 % | 53,53 % | 4,838 | 4,689 |

Les % bougent, les T mappées restent dans T1 (sauf at_s7 harm. 4,592, à 0,008
sous la fenêtre — cas limite). L'harmonique ne change pas le verdict global
sur AT ; il décale le seuil en % sans déplacer la température retrouvée.

## 6. Ce que ce lot change par rapport à la vague 2

- Avant : « le seuil global choisit T1 » n'était observé que pour le contrôle
  energy. Maintenant : c'est vrai pour TOUS les contrôles monotones (et même
  pour local_variance, dont le global stable pointe tôt, pas vers une transition).
  Le seuil global est donc structurellement un détecteur de première rupture.
- Avant : la résolution par flux n'était montrée que pour le contrôle energy.
  Maintenant : elle tient pour tout contrôle monotone (19–20/20 compatibles),
  et se dégrade mesurablement pour un contrôle non monotone.
- La règle « contrôle exclu des flux » est désormais testée dans les 35 cas, pas
  seulement pour energy : sans elle (vague 2, porte B), le global du nul restait
  VERY STABLE ; avec elle, 5/6 nuls sont UNSTABLE et les scores s'effondrent
  dans 6/6 cas.
- Limites inchangées : données synthétiques ; horloge L=24 trop petit pour le
  BKT ; lecture par flux toujours post-run (fonction de scan du pipeline),
  pas une sortie native.

Fichiers : `controles/<jeu>/<contrôle>/` (run_summary.json, verdict.json,
per_flux_thresholds.csv, scan_curve.csv, threshold_scan.png, noise_diagnostic.png,
text_report.txt, pipeline_results.json) ; synthèse `controles/synthese_globaux.csv`,
`controles/synthese_par_flux.csv`, `controles/synthese.json` ; lot
`controles_batch.py`, pilotes `run_ctrl.py` / `analyse_ctrl.py`.
