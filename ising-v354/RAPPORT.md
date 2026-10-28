# RAPPORT — Ising classique 2D × pipeline v3.5.4-H1 (Q6-A)

**Lot ising-v354 — 28 octobre 2026. Synthèse vérifiée (script
`synthese.py`, relecture indépendante des sorties). Protocole gelé
avant exécution : `PROTOCOLE.md`. Provenance complète : `PROVENANCE.md`.**

*Verified synthesis — classical 2D Ising × v3.5.4-H1 pipeline (Q6-A).
Frozen protocol before execution. Full provenance in PROVENANCE.md.*

## Verdict

**6/6 runs OK, 0 échec, 0 avertissement, 0 repli.** Sur une simulation
physique à transition connue (Tc d'Onsager = 2,2692), le pipeline
désigne la même frontière physique depuis **chaque** lentille : 5
contrôles sur 6 traduisent leur seuil Monte Carlo à **T = 2,2565**
(ΔT = −0,013, un pas de grille sous Tc), avec des scores MC de
0,736–0,762 et des stabilités bootstrap **VERY STABLE** dont les
moyennes s'écartent du seuil MC de 0,14 à 1,36 point seulement.
L'exception est le contrôle `susceptibility` (T = 2,1174, ΔT = −0,152),
biaisée par la construction même de ce flux (fenêtre expansive à
mémoire — voir §5). `flip` et `fliprate` donnent des résultats
bit-identiques, comme la proportionnalité exacte l'exigeait.

C'est, à ce jour, la validation la plus forte de l'instrument sur un
système à vérité terrain connue : le banc Ashkin-Teller était un
générateur d'agent, celui-ci est une simulation physique avec un Tc
exact. Les réserves (§6) portent sur la calibration de Q6-A, le
plateau des courbes de scan, et la taille unique L = 32 — elles ne
retirent rien à la convergence observée.

## 1. Données et protocole (rappel gelé)

- Générateur `gen_ising_classic_v354.py` (SHA
  `24069e4e…`), adapté de `gen_ising_proxy.py` (mêmes `sweep`,
  énergie, variance locale). L = 32, J = 1, limites périodiques,
  Metropolis checkerboard, graine 42, T = linspace(1,7, 3,3, 24),
  1 500 sweeps d'équilibration, 40 snapshots par T, GAP 50.
- 960 lignes × 6 flux (`fliprate, flip, energy, magnetization,
  localvar, susceptibility`), 0 NaN, 0 doublon. Température dans un
  CSV séparé (`ising_classic_v354_temperature.csv`, SHA `4863b1de…`),
  même ordre, jamais lu par le pipeline.
- Portes physiques P1–P4 passées avant les runs : chute de |m| entre
  T = 2,2565 et 2,3957 (Tc encadré), Spearman(T, énergie) = 1,0, pic de
  χ à T = 2,3261 (écart 0,057), 960 lignes / 0 NaN.
- Pipeline v3.5.4-H1 (Q6-A), SHA `b54fcf66…`, mode stable, w80,
  cohen_d, graine 42, HARMONIC_PROB 0,45, Theiler 1/φ planché (source
  fixe), triangulation complète désactivée. Contrôle exclu des flux.
  Max 2 runs en parallèle. Harnais `run_one_ising.py`.

## 2. Seuils Monte Carlo par contrôle (détail complet)

| Contrôle | Seuil MC % | Score MC | Seuil défaut % | MC brut % | Rigide 1001 % | Stabilité | Moy. boot ± std | Durée s | T au seuil MC | ΔT vs Tc |
|---|---|---|---|---|---|---|---|---|---|---|
| fliprate | 36,50 | 0,7624 | 38,05 | 36,50 | 36,50 | VERY STABLE | 35,14 ± 2,70 | 126,9 | 2,2565 | −0,013 |
| flip | 36,50 | 0,7624 | 38,05 | 36,50 | 36,50 | VERY STABLE | 35,14 ± 2,70 | 127,4 | 2,2565 | −0,013 |
| energy | 35,76 | 0,7583 | 38,29 | 35,76 | 35,70 | VERY STABLE | 36,35 ± 1,66 | 124,9 | 2,2565 | −0,013 |
| magnetization | 63,75 | 0,7602 | 63,66 | 63,75 | 63,40 | VERY STABLE | 63,61 ± 1,20 | 122,7 | 2,2565 | −0,013 |
| localvar | 35,76 | 0,7615 | 38,05 | 35,76 | 35,70 | VERY STABLE | 36,49 ± 1,71 | 128,3 | 2,2565 | −0,013 |
| susceptibility | 25,22 | 0,7363 | 22,44 | 25,22 | 25,20 | VERY STABLE | 23,92 ± 2,06 | 125,5 | 2,1174 | −0,152 |

- Configurations MC retenues : règle **uniform** dans les 6 runs
  (jamais harmonique), w_size 100 (fliprate/flip/magnetization/
  susceptibility) ou 118 (energy/localvar), n_candidates 605–790,
  min_grp 5–9. Source du seuil : `monte_carlo` partout.
- Les pourcentages diffèrent (25–64 %) parce que ce sont des rangs de
  contrôles différents (|m| est renversée en T, χ est distordue) ; la
  traduction en température les unifie. C'est exactement pour cela que
  la température a été gardée à part.
- Le `rigid_1001` et le MC brut coïncident avec le MC retenu à
  ≤ 0,35 point près dans tous les runs : le MC ne déplace presque pas
  le seuil par rapport au scan rigide ici — la coupure est dans les
  données, pas dans l'optimiseur.

## 3. Seuils propres par flux (matrices complètes)

Seuil propre de chaque flux, sous chaque contrôle (% du rang du
contrôle). Diagonale vide : le contrôle n'est jamais un flux.

| Flux \ Contrôle | fliprate | flip | energy | magnetization | localvar | susceptibility |
|---|---:|---:|---:|---:|---:|---:|
| fliprate | — | 38,28 | 36,50 | 38,53 | 36,50 | 29,78 |
| flip | 38,28 | — | 36,50 | 38,53 | 36,50 | 29,78 |
| energy | 37,91 | 37,91 | — | 36,26 | 35,60 | 26,49 |
| magnetization | 61,22 | 61,22 | 63,75 | — | 62,61 | 71,36 |
| localvar | 35,76 | 35,76 | 35,76 | 35,76 | — | 26,16 |
| susceptibility | 25,22 | 25,22 | 25,22 | 25,22 | 25,22 | — |

Températures médianes correspondantes :

| Flux \ Contrôle | fliprate | flip | energy | magnetization | localvar | susceptibility |
|---|---:|---:|---:|---:|---:|---:|
| fliprate | — | 2,3261 | 2,2565 | 2,3261 | 2,2565 | 2,1870 |
| flip | 2,3261 | — | 2,2565 | 2,3261 | 2,2565 | 2,1870 |
| energy | 2,2565 | 2,2565 | — | 2,2565 | 2,2565 | 2,1174 |
| magnetization | 2,3261 | 2,3261 | 2,2565 | — | 2,2565 | 2,1870 |
| localvar | 2,2565 | 2,2565 | 2,2565 | 2,2565 | — | 2,1174 |
| susceptibility | 2,1174 | 2,1174 | 2,1174 | 2,1174 | 2,1174 | — |

Lecture : 20 des 30 seuils propres traduisent T = 2,2565 ou 2,3261
(les deux pas de grille qui encadrent Tc) ; les 10 autres passent par
le contrôle `susceptibility` (T = 2,1174–2,1870). Le flux
`susceptibility` lui-même a un seuil propre **invariant** (25,22 %,
T = 2,1174) sous les 5 contrôles — signature de sa construction, pas
d'une physique différente.

## 4. Questions Q1–Q6 (moyennes par run)

| Contrôle | Q1 | Q2 | Q3 | Q4 | Q5 | Q6-A |
|---|---:|---:|---:|---:|---:|---:|
| fliprate | 0,852 | 2,260 | 0,852 | 1,362 | 8,713 | 158,62 |
| flip | 0,852 | 2,260 | 0,852 | 1,362 | 8,713 | 158,62 |
| energy | 1,479 | 1,421 | 1,479 | 1,260 | 6,327 | 63,01 |
| magnetization | 1,690 | 1,921 | 1,690 | 0,789 | 6,658 | 102,80 |
| localvar | 1,478 | 1,476 | 1,478 | 1,277 | 5,924 | 51,53 |
| susceptibility | 0,833 | 2,639 | 0,833 | 0,462 | 7,502 | 248,37 |

- Q1 = Q3 dans chaque run (même définition sur ces données — fait
  déjà observé au pilote v3.5, non une erreur).
- **Q6-A fonctionne mécaniquement** (non nulle, différenciée entre
  runs, invariante d'échelle vérifiée avant le lot), mais ses
  magnitudes (51–248) ne sont **pas comparables** à celles de Q5
  (6–9) : la référence moyenne, après mise à l'échelle, est très
  lisse, ce qui gonfle le d de Cohen. Q6 se lit en intra-Q6
  uniquement. Sa calibration (ce qui compte comme « grand ») n'est
  pas établie par un seul lot. Sous contrôle `susceptibility`,
  Q6 = 248 — la valeur la plus extrême du lot, portée par le flux χ
  lui-même (voir §5).

## 5. Analyse

### 5.1 Convergence : la triangulation tient

Cinq lentilles différentes (taux de retournement, énergie, |m|,
variance locale, et leurs redondances) désignent la même température
à un pas de grille près, avec des scores MC serrés (0,758–0,762) et
des bootstraps qui confirment le MC au lieu de le contredire (écarts
0,14–1,36 point — à comparer au gouffre de 97,69 points du contrôle
`odor` sur mushroom). Le paysage de scan est un **plateau haut** :
les bandes à ≥ 95 % du score maximal couvrent 6 à 13 points de %
(32,6–39,9 % pour energy, 59,8–67,9 % pour magnetization) ; le
pourcentage exact est mou (±3 points), la bande de température est
robuste (un pas de grille). La règle MC `uniform` a gagné les 6 fois :
le guidage harmonique (45 % des tirages) n'a pas dominé ici — le
signal est assez fort pour que l'exploration uniforme suffise.

### 5.2 L'exception `susceptibility` : un artefact de construction, nommé

Le flux χ a été défini par fenêtre expansive intra-bloc : à chaque
bloc de température, χ repart de 0 et croît avec la fenêtre — 24 dents
de scie superposées à la tendance en T. Sa progression en rangs est
donc distordue dès la construction, et son seuil (comme contrôle et
comme flux) tombe systématiquement 0,07–0,15 trop bas, avec le score
de scan le plus faible du lot (max 2,66, médiane 1,00, contre
3,47–3,81 et 2,06–2,28 pour les autres). Ce n'est pas une physique
différente : c'est la mémoire que la définition injecte. Leçon
opérationnelle : **un flux cumulatif/à fenêtre expansive ne doit pas
servir de contrôle sans que ce biais soit nommé** — comme flux
analysé, il reste informatif (sa dérive au bruit blanc est la plus
forte du lot, §5.4).

### 5.3 F1/F2 : la rupture traverse presque toutes les loupes

174 lignes par run (29 estimateurs × 5 flux + agrégat « Tous ») ;
changements de signe de la dérivée : 105 à 131 selon le run
(60–75 %). L'agrégat « Tous » change de signe pour 25 estimateurs
sur 29 (run fliprate). Les réfractaires sont concentrés dans la
famille des dimensions (TwoNN, LevinaBickel, DANCo, Fisher, D2/GP,
InformationD1, GraphDimension, homologie persistante) plus
SingularityFmax (saturée à 1,000 — constante connue, sans
information de rupture) et KolmogorovLZ/MFA. Sur données continues
simulées, les estimateurs de dimension ne basculent pas comme les
autres : soit insensibilité réelle à cette longueur de fenêtre, soit
saturation — non tranché par ce lot, et rapporté comme tel.

### 5.4 Bruit et dérive : des flux structurés, pas du bruit blanc

Diagnostic de bruit : « proxy de variance modéré » (5 runs),
« proxy coloré CSD » (contrôle magnetization). Scores moyens de proxy
0,727–0,813 (échelle 0–1 ; magnetization 0,813, les autres 0,727–0,750 ;
min par flux 0,634–0,796, max 0,750–0,838). Run fliprate (détail lu) :
Hurst moyens par flux 0,72–1,08, pente spectrale post-seuil −1,78. Dérives standardisées au bruit
blanc (table `estimator_drift`, 29 estimateurs, références empiriques
R = 8, graine 1234) : médianes 1,4–8,5 selon le flux, aucune
référence dégénérée. `susceptibility` dérive le plus (médiane
7,5–8,5, max 44–54 via PermutationEntropy) ; PCAIntrinsic porte le max
dans la plupart des runs (15–26). Traduction : les flux sont loin du
bruit blanc, comme attendu d'une simulation physique — et χ l'est
encore plus, par construction.

### 5.5 Estimateurs sur données continues : le dossier des liens se tait

Taux de NaN dans `df_feat` (30 lignes, run fliprate) : 0 % pour 25
estimateurs ; SpectralBeta/Dimension 6,7 %, Lyapunov 2,0 %,
TwoNN 2,7 %. À comparer à mushroom (Spectral 32 %, PH 21 %, DANCo
20 %) : sur des séries continues presque sans liens exacts, les
décisions discrètes qui rendaient 9 estimateurs métastables ne se
déclenchent presque pas. La fragilité mesurée le 27 oct. est bien une
propriété de la rencontre formules/données liées, pas de l'instrument
seul.

### 5.6 Exécution

Lot total : 6 min 38 s (10:07:47–10:14:25 EDT), 123–128 s par run,
2 en parallèle, 0 échec, 0 repli de scan (`scan_fast_fallback_log`
vide), 0 avertissement de seuil. Coût ≈ 125 s/run pour 5 flux
(cohérent avec l'échelle en nombre de flux du pilote v3.5 : 4 439 s
pour 22 flux). La veille cron posée pour la fin du lot a été retirée
après constat direct de la fin (`LOT TERMINÉ`, 6/6 résumés OK).
Harnais et reprise non sollicités (aucun redémarrage VM pendant le
lot).

## 6. Opinion (demandée)

Le pipeline fait, sur ce test, exactement ce qu'il prétend faire :
trouver une coupure critique qui influence le système, et la trouver
depuis chaque lentille indépendamment. La convergence en température
(5/6 à un pas de grille de Tc, bootstraps d'accord) est le résultat
le plus propre obtenu jusqu'ici — plus propre que le banc
Ashkin-Teller, parce que la vérité terrain est ici un théorème
(Onsager), pas un générateur d'agent. Trois choses à ne pas
sur-vendre : (1) Q6-A sort des nombres, pas encore une échelle —
il faut d'autres lots pour savoir ce que « 150 » veut dire ;
(2) le seuil en % est mou (plateau), c'est la bande de température
qui est la mesure ; (3) une seule taille, une seule graine : l'écart
−0,013 peut être un effet de taille finie, pas un biais
systématique. La suite logique, dans l'ordre : L = 64 + seconde
graine (le −0,013 tient-il ?), puis la comparaison réel-vs-nul
loupe par loupe déjà cadrée, avec χ gardée comme flux analysé et
jamais comme contrôle sans mention de son biais.

## 7. Limites (gelées, rappel)

L = 32 fini (transition arrondie, pic χ décalé de 0,057 — mesuré,
attendu) ; χ par fenêtre expansive (biais de début de bloc, §5.2) ;
`flip`/`fliprate` exactement proportionnels (redondance voulue,
vérifiée bit-identique) ; contrôles discrets/à paliers lus en rangs ;
une seule graine ; pas de champ magnétique ; pas d'étude en taille
finie. Lecture descriptive sur données simulées — aucune règle
physique générale n'est inférée au-delà de ce lot.

## 8. Fichiers et hachages

| Fichier | SHA-256 (début) / contenu |
|---|---|
| `gen_ising_classic_v354.py` | `24069e4e…` |
| `data/ising_classic_v354.csv` | `9027dfd5…` (960 × 6, 0 NaN) |
| `data/ising_classic_v354_temperature.csv` | `4863b1de…` (960 × 1) |
| `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1) | `b54fcf66…` |
| `run_one_ising.py` / `run_lot.sh` / `synthese.py` | harnais, pilote, synthèse (voir dépôt) |
| `runs/<controle>/` × 6 | `pipeline_results.json`, `numerical_results.csv`, `text_report.txt`, `threshold_scan.png`, `noise_diagnostic.png`, `scan_curve.csv`, `per_flux_thresholds.csv`, `landscape_peaks.csv`, `transition_F1F2.csv`, `run_summary.json`, `run.log` |
| `RAPPORT.md` (ce fichier), `PROTOCOLE.md`, `PROVENANCE.md`, `synthese.json` | synthèse et traçabilité |
| PDF + zip | voir §9 |

## 9. Publication

Synthèse vérifiée d'abord, puis PDF + zip des résultats complets,
puis dépôt GitHub privé FindPrint/Code (texte par snapshot, binaires
par Release, vérifiés par relecture) selon la règle permanente
« publier toujours tout ». Détails des commits et de la Release dans
`PROVENANCE.md` (addendum de publication).
