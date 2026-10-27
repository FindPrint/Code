# 3 tests diagnostics — Mushroom Classification × pipeline Tlog v3.4-H3

Protocole gelé avant tout run : `PROTOCOLE_TESTS.md` (27 oct. 2026).
Pipeline commun : `Tlog_v3_4_harmonic_v3.py` v3.4-H3, SHA-256
`81092eb6…`, mode stable, w_size 80, cohen_d, graine 42,
HARMONIC_PROB 0,45, sans triangulation complète, contrôle exclu des
flux, ordre des lignes préservé, 2 runs en parallèle, design
résumable. Les tests sont des diagnostics du lot v3.4, pas une
validation de ses seuils : le découvreur ne valide jamais.

## Provenance (à nommer partout, règle permanente du 27 oct. 2026)

Source : *The Audubon Society Field Guide to North American Mushrooms*
(1981, G. H. Lincoff, Knopf, pp. 500–525), donateur Jeff Schlimmer
(27 avril 1987), UCI Machine Learning Repository dataset n° 73
(https://archive.ics.uci.edu/dataset/73/mushroom), miroir Kaggle
`uciml/mushroom-classification`. Les 8 124 lignes sont des
descriptions d'échantillons **hypothétiques** de 23 espèces
d'*Agaricus*/*Lepiota*, pas des spécimens mesurés. Couleurs et odeurs
= mots humains du guide, aucune mesure instrumentale ni chimique.
Détail complet, sources et hachages : `PROVENANCE.md` (aussi dans
`../mushroom-v34/PROVENANCE.md`).

## Verdicts — d'abord, les chiffres

| Contrôle | Test 1 encodage | Test 2 nul |
|---|---|---|
| class | SENSIBLE (seuil Δ −1,75 pt, score Δ −0,070) | INDISTINGUABLE (nul 0,630 > réel 0,548) |
| odor | SENSIBLE (seuil Δ −8,02 pts, score Δ −0,052) | INDISTINGUABLE (nul 0,680 > réel 0,584) |
| cap-surface | SENSIBLE (seuil Δ +46,12 pts, score Δ +0,006) | INDISTINGUABLE (nul 0,629 > réel 0,465) |

**Test 3 — corrélations :** les flux dominants se suivent très
fortement (Spearman max 0,934 ; V de Cramér max 0,978) : leurs
témoignages ne sont pas indépendants. Accord exact des deux couleurs
de pied : 62,38 % des lignes.

**Bilan :** encodage 3/3 sensibles, nul 3/3 indistinguables (et
dépassés), corrélations très fortes entre flux dominants. Le lot
v3.4 reste techniquement propre, mais comme détection de régime sur
ce dataset il ne tient pas : les seuils sont des coupes de rang sur
des étiquettes, sensibles à leur numérotation, reproductibles sans
aucune association, et portés par des flux qui se suivent.

## Test 1 — Encodage (alphabétique vs ordre d'apparition)

Données : `encodage/data/mushrooms_alpha.csv`, SHA-256
`4552be72…`, 8 124 × 23, 2 480 NaN (stalk-root, comme le lot),
mapping `encodage/data/mapping_alpha.json`. L'ordre alphabétique
diffère de l'ordre d'apparition pour les 3 contrôles (vérifié avant
les runs). Règle gelée : écart de seuil MC > 5 pts OU écart de score
MC > 0,05 → sensible à l'encodage. Runs : class + odor en parallèle,
puis cap-surface. Durées : class 648 s, odor 536 s, cap-surface
1 042 s. Tous `threshold_source = monte_carlo`, 0 avertissement.

| Contrôle | Origine MC % / score | Alpha MC % / score | Δ seuil (pts) | Δ score | Verdict |
|---|---|---|---|---|---|
| class | 52,75 / 0,548 | 51,00 / 0,479 | −1,75 | −0,070 | SENSIBLE (score) |
| odor | 99,52 / 0,584 | 91,50 / 0,531 | −8,02 | −0,052 | SENSIBLE (seuil + score) |
| cap-surface | 20,00 / 0,465 | 66,13 / 0,471 | +46,12 | +0,006 | SENSIBLE (seuil) |

Moyennes bootstrap : class 52,73 % (±14,78) → 60,21 % (±10,21) ;
odor 1,83 % (±0,12) → 87,98 % (±0,80) ; cap-surface 79,62 %
(±16,21) → 22,62 % (±7,08). La renumérotation déplace aussi le
bootstrap d'un bout à l'autre. Seuils par défaut, bruts et rigides :
voir `synthese/comparaison_controles.csv`. Incident : aucun run
partiel compté ; le batch a été relancé de zéro après le lot
(aucun résultat du lot repris).

## Test 2 — Nul propre (permutation du contrôle, graine 1234)

Données : encodage d'origine, colonne de contrôle permutée avec
`np.random.default_rng(1234).permutation` (permutation enregistrée :
`nul/data/permutation_indices.npy`, SHA-256 de la permutation
`6df1051b1…`, identique pour les 3 contrôles), flux intacts,
fréquences marginales conservées (vérifié), 3 CSV
`nul/data/mushrooms_null_<controle>.csv` (SHA-256 : class
`18c1291a…`, odor `8cc07f99…`, cap-surface `bbb54c80…`).
Vérification avant les runs : corrélation de Spearman contrôle-flux
tombée à ~0 (class vs odor : −0,771 → −0,001 ; odor vs cap-color :
0,139 → 0,008 ; cap-surface vs odor : −0,093 → −0,004).
Règle gelée : score nul ≥ score réel − 0,05 → indistinguable du nul.
Durées : class 854 s, odor 798 s, cap-surface 446 s. Tous
`threshold_source = monte_carlo`, 0 avertissement, UNSTABLE.

| Contrôle | Réel MC % / score | Nul MC % / score | Δ score (nul − réel) | Seuil de distinguabilité | Verdict |
|---|---|---|---|---|---|
| class | 52,75 / 0,548 | 25,25 / 0,630 | +0,082 | 0,498 | INDISTINGUABLE |
| odor | 99,52 / 0,584 | 33,88 / 0,680 | +0,096 | 0,534 | INDISTINGUABLE |
| cap-surface | 20,00 / 0,465 | 16,88 / 0,629 | +0,164 | 0,415 | INDISTINGUABLE |

Les trois scores nuls dépassent les scores réels. Avec zéro
association, le pipeline trouve des seuils du même calibre, voire
meilleurs. « Score 0,6 » ne veut donc rien dire seul sur ce dataset.
Incident de lancement (transparence) : le premier lancement du batch
a échoué en < 1 s sur une erreur de mon script d'adaptation
(variable utilisée avant sa définition) ; corrigé, relancé, aucun
run partiel compté, `results/` était vide.

## Test 3 — Corrélations entre flux dominants (aucun run pipeline)

Mesures gelées : Spearman sur valeurs encodées (origine) + V de
Cramér sur codes bruts, matrices 23 × 23 complètes
(`correlations/results/spearman_matrix.csv`,
`cramer_matrix.csv`), top 15 (`top15_spearman.csv`,
`top15_cramer.csv`), focus trio + accord exact
(`trio_focus.json`). Exécution : 3,4 s, après le test 2.

Top 5 Spearman : gill-attachment / veil-color 0,934 ; class / odor
−0,771 ; bruises / ring-type 0,740 ; stalk-surface-above-ring /
ring-type 0,680 ; stalk-surface-below-ring / ring-type 0,663.
Top 5 V de Cramér : gill-attachment / stalk-color-above-ring 0,978 ;
gill-attachment / stalk-color-below-ring 0,978 ; class / odor 0,971 ;
gill-attachment / veil-color 0,955 ; gill-attachment /
spore-print-color 0,827. Top 15 complets dans les CSV.

Focus trio (pré-enregistré) : Spearman stalk-color-above /
stalk-color-below 0,622, above / ring-type 0,430, below / ring-type
0,359 ; V de Cramér 0,635 / 0,673 / 0,665 ; accord exact entre les
deux colonnes stalk-color : 62,38 % des 8 124 lignes.

Interprétation gelée : une forte corrélation ne prouve pas la
circularité, elle retire seulement l'indépendance des témoignages.
Les scores propres élevés des mêmes flux (couleurs du pied,
ring-type, gill-attachment, class, odor) ne sont donc pas des
témoignages indépendants qui se confirment.

## Hypothèses de l'utilisateur sur les Q — état après les 3 tests

Hypothèses (non établies, protocole) : Q5 énorme partout = données
en partie sans flux réceptif ; Q4 plat partout = persistance de
l'information ; Q2 centré sur veil-color = tension là où le signal
est placé sans flux physique/biologique. Constats mesurés ici :
Q5 est énorme aussi sous le nul (class 29,047 ; odor 15,338 ;
cap-surface 14,243) et sous encodage alphabétique (18,145 / 4,055 /
15,374) — Q5 ne sépare donc pas le signal du nul sur ces runs.
Q2 vaut 0,0 dans 3 des 6 runs tests (class nul, odor alpha,
cap-surface nul) et 5,387 dans odor nul : pas de concentration
stable. Q4 reste faible partout (0,164–0,389 sur les 6 runs tests).
Ces hypothèses restent non établies ; les tests 1 et 2 montrent que
les Q, calculés par le pipeline sur les mêmes données, portent
aussi sa signature. Valeurs complètes : `synthese/qs_tests.csv`
(Q1–Q5, 6 runs tests ; Q du lot d'origine dans le rapport v3.4).

## Limites (identiques au lot)

Codes nominaux, seuils = coupes de rang (plateaux), lecture
descriptive, aucune vérité terrain, jamais une règle
comestible/vénéneux, aucune lecture causale/temporelle. Aucun flux
physique, biologique, chimique, temporel ou spatial n'existe dans ce
dataset ; le manque est structurel. La suite (après analyse) : un
dataset complet avec flux mesurés (espèce, mesures, chimie,
microscopie, ADN, date/lieu/saison, flux physiques et biologiques),
et comparaison pipeline sur dataset d'origine vs enrichi.

## Fichiers

- Protocole gelé : `PROTOCOLE_TESTS.md` ; provenance : `PROVENANCE.md`
- Synthèses vérifiées : `synthese/comparaison_controles.csv` (3 lignes),
  `synthese/tous_seuils_par_flux_tests.csv` (132 lignes = 6 runs × 22 flux),
  `synthese/tous_F1F2_tests.csv` (690 lignes),
  `synthese/qs_tests.csv` (6 lignes)
- Figures : `figures/fig_scores_comparaison.png`,
  `figures/fig_seuils_comparaison.png`,
  `figures/heatmap_spearman.png`, `figures/heatmap_cramer.png`
- Par run (encodage + nul) : `run_summary.json`,
  `per_flux_thresholds.csv`, `transition_F1F2.csv`, `scan_curve.csv`,
  `threshold_scan.png`, `noise_diagnostic.png`, `text_report.txt`,
  `numerical_results*.csv`, `pipeline_results.json` (exclu du zip,
  comme pour les lots précédents)
- Scripts : `encodage/scripts/run_one_alpha.py`,
  `nul/scripts/run_one_null.py`, `nul/scripts/build_null_data.py`,
  `correlations/scripts/analyse_correlations.py`,
  `scripts/synthese_tests.py`

## English summary

Three pre-registered diagnostic tests on the mushroom lot (v3.4-H3).
(1) Encoding: alphabetical recoding moves every threshold/score
beyond the frozen rule — 3/3 encoding-sensitive. (2) Null: permuting
the control (seed 1234) yields scores that beat the real ones for all
three controls (0.630 vs 0.548, 0.680 vs 0.584, 0.629 vs 0.465) — real
scores are indistinguishable from null. (3) Correlations: dominant
fluxes are strongly correlated (Spearman up to 0.934, Cramér's V up to
0.978) and are not independent witnesses. Provenance: hypothetical
samples from the 1981 Audubon Field Guide (23 Agaricus/Lepiota
species), UCI dataset 73, Kaggle mirror — words, not measurements.
