# Lecture des 29 estimateurs, loupe par loupe — v5.9.0f (étape 1) et v5.4.0

**Date :** 8 novembre 2026, ~21h00 (horloge de la VM, UTC — soit ~16h00 HNE). Rapport complet : loupes A, B, C, D + variante sans dégénérés.
**Auteur :** TagPrint (sous-agent lecture estimateurs)
**Statut :** re-lecture seulement, AUCUN nouveau run pipeline, originaux jamais modifiés.

## Verdict d'abord

- **26 signaux distincts sur 29 estimateurs.** Trois paires duplicata, les mêmes que sur v3.5.4 : {Hurst, Hurst2mH}, {CorrelationD2, GrassbergerProcaccia}, {SpectralBeta, SpectralDimension}. Aucune autre redondance. Résultat identique sur les deux bancs (synthétique et Ising), les deux versions (v5.9.0f et v5.4.0), et sous les deux règles de support testées.
- **Le contraste à la transition est porté par MultifractalDeltaAlpha, Sevcik et Katz** (Ising, médiane |d| de Cohen : 1,56 / 1,42 / 1,38 ; nuls : 0,11–0,22). En bas : LevinaBickel (0,24), Petrosian (0,35), GraphDimension (0,36).
- **Lyapunov est un artefact, pas un signal.** Sur le banc synthétique sa série n'a que 13 valeurs finies et 2 paliers ; son Spearman vaut ±1,0 avec 23 estimateurs et son d de Cohen atteint 20,55. Ces chiffres ne mesurent pas Lyapunov : ils mesurent l'alignement de son palier avec la transition. Exclu avec les trois autres estimateurs dégénérés (MFA, KolmogorovLZ, SingularityFmax), le consensus redevient les 3 paires partout.
- **Gain incrémental (loupe C) : saturation à 2 estimateurs en Ising, 4–5 en synth sans dégénérés.** AUC médiane : Ising v59 [0,5 ; 0,963 ; 1,0] ; synth sans les 4 dégénérés [0,5 ; 0,891 ; 0,955 ; 0,985 ; 0,996 ; 1,0]. La saturation à 1 estimateur mesurée d'abord sur synth était entièrement l'artefact Lyapunov (25/50 ouvertures, AUC 1,0) : elle disparaît sans lui. Aucun ouvreur dominant (Higuchi ouvre 9/21 cas Ising ; PermutationEntropy 11/50 synth sans dégénérés) ; après saturation, les sélections suivantes ont un gain médian de 0,000 — du remplissage.
- **v5.9.0f et v5.4.0 sont identiques sur la couche estimateurs.** `df_feat.csv` bit-identiques 45/45 sur les sorties appariées ; lectures natives (loupe D) : 0 différence sur 82 940 comparaisons. Seules les couches autour diffèrent (L7b, télémétrie, workers).
- **La classe native du pipeline ne mesure pas le contraste.** MultifractalDeltaAlpha est classé `null_reference` par le pipeline et pourtant premier au contraste ; Hurst est `null_reference` avec d = 1,09. Les classes sont uniformes sur les 143 sorties-flux v59 (8 saturation, 7 criticality, 7 divergence, 7 null_reference) : elles décrivent l'estimateur, pas le run.
- **Couche E (comparaison à Tc) : abandonnée.** La reconstruction des cohortes ne se vérifie pas exactement en v5.x (meilleure règle : 58/120 comptes exacts, écart max 2). Aucune garde Tc donc ; la circularité des loupes B et C est couverte par les nuls permutés.
- **L7b : FRAGILE sur 143/143 sorties v59** (t0_std médian 29,40), cohérent avec l'analyse géométrique du parent (fenêtres glissantes à axe renormalisé) — ce n'est pas une mesure de fragilité de l'instrument.

## 1. Provenance

### Fichiers lus (lecture seule, jamais modifiés)

| Source | Contenu | SHA / repère |
|---|---|---|
| `workspace/ising-v59/synth/*/df_feat.csv` + `master_results.json` (39 sorties) et `workspace/ising-v59/ising/fast/*/df_feat.csv` + `master_results.json` (6 sorties) | Étape 1 v5.9.0f, 45 sorties, 143 cas (sortie, flux) | `df_feat.csv` bit-identiques 45/45 avec v5.4.0 (voir §6) |
| `workspace/ising-v54/synth/*/df_feat.csv` + `master_results.json` (39 sorties) et `workspace/ising-v54/ising/*/*/df_feat.csv` + `master_results.json` (13 sorties : fast 6, full 6, predict 1) | Lot v5.4.0, 52 sorties, 178 cas | — |
| `workspace/ising-v354/data/ising_classic_v354.csv` | Données Ising, 960 lignes, L=32, graine 42 | SHA `9027dfd5…` |
| `workspace/ising-v354/data/ising_classic_v354_temperature.csv` | Températures (960 lignes, colonne `temperature`) | SHA `4863b1de…` |
| `workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py` | Code v5.9.0f, 13 013 lignes, **lu seulement** (lignes 5462–5501 : `compute_estimator_redundancy`) | SHA `4f80f6a7…` |
| `workspace/hp-estimator-info/PROTOCOLE.md` | Protocole gelé du 30 oct. 2026, validé par Zackary sans amendement | référence méthodologique |
| `workspace/hp-estimator-info/RAPPORT.md` | Résultat de référence v3.5.4 (3 paires → 26 signaux, AUC saturée à 3 estimateurs) | référence de comparaison |

### Scripts de cette lecture (tous sous `workspace/ising-v59/harness_estimateurs/`)

- `inventory.py` / `inventory.json` — inventaire, SHA, appariement v59/v54.
- `harness_lecture_v59.py` — loupes A, B, D, couche E (adaptation du harnais gelé, fonctions copiées avec attribution).
- `harness_C.py` — loupe C (sélection gloutonne, Pool(2)).
- `harness_C_sans_degeneres.py` — loupe C, variante sans les 4 dégénérés (banc synthétique).
- `generer_csv.py` — CSV une-ligne-par-estimateur (`workspace/ising-v59/resultats_estimateurs.csv`).
- `harness_A_pipeline_rule.py` — loupe A avec la règle de support du pipeline.
- `analyse_complement.py` — consensus restreint, tableaux B, comparaison D v59/v54, L7b, recoupement redondance, dégénérescence par banc.
- Sorties : `resultats_ABDE.json` (22,9 Mo), `resultats_A_pipeline_rule.json`, `resultats_complement.json`, `resultats_C.json`, `resultats_C_sans_degeneres.json`, `degeneracy.json`.

### Ce qui n'a pas été touché

- `workspace/ising-v59/ising/full/fliprate/` (run en cours au moment de la lecture) : jamais lu, jamais modifié.
- Aucun fichier d'entrée modifié. Aucun run pipeline lancé. MEMORY.md non touché. Rien envoyé à l'utilisateur.
- Incident en cours de lecture : redémarrage VM le 8 nov. ~19h39 (horloge VM) — il a tué le run full/fliprate (lancé 14h13, en phase Monte Carlo) et le harnais A/B/D/E (PID 42377, ~46 % fait). Le harnais a été relancé (PID 2418, `python3 -u`, log non bufferisé) et a terminé à 20h00 (horloge VM). La relance du run full/fliprate relève du fil principal (surveillance `ising-v59-watch`), pas de cette lecture. (Toutes les heures de ce rapport sont en horloge VM, UTC, comme les horodatages des fichiers cités ; HNE = VM − 5 h.)

## 2. Méthode adaptée et ses limites

### Déviation déclarée : les séries

Le protocole gelé (v3.5.4) lisait des séries de 30 cohortes dans `numerical_results.csv`. Ce format n'existe pas en v5.x : `master_results.json` ne stocke AUCUNE série brute (seulement des résumés : dérivées, z, four-tests, consensus). Les séries lues sont donc celles de **`df_feat.csv`** : 120 points de scan, axe Progress 0–100 (pas 100/119 ≈ 0,8403), colonnes `<flux>_<estimateur>_mean` / `_std`. C'est la sortie vérifiée du même run, même dossier, relue seulement. La structure change (120 points au lieu de 30 cohortes, fenêtres de scan au lieu de cohortes) : les comparaisons chiffrées avec v3.5.4 sont donc indicatives, pas des réplications exactes.

### Cas et consensus

- **Cas = (sortie, flux).** v59 : 143 cas (113 synth + 30 Ising) ; v54 : 178 cas (113 synth + 65 Ising).
- **Duplication massive :** les séries sont bit-identiques entre sorties de même mode (45 fichiers v59 → 24 distincts par hash ; 52 fichiers v54 → 31 distincts). Exemple : les 9 fichiers fast synth sont bit-identiques, séries et seuils compris. Le consensus primaire est donc calculé sur **cas DISTINCTS** (même X + même seuil = un seul cas) : v59 = 71 distincts (50 synth + 21 Ising), v54 = 97 distincts (50 synth + 47 Ising). Le consensus sur tous les cas est donné en sensibilité (il ne change pas les paires).
- **Étiquette pré/post (loupe B et C) = seuil propre du run** (MC `opt_threshold`, en Progress 0–100). Circularité déclarée d'avance, comme dans le protocole : le seuil est celui que le pipeline a trouvé, pas une vérité indépendante. Les nuls permutés (20 par série pour B, 20 étiquettes pour C) sont la garde.
- **Comparaison à Tc (2,2692) : seulement descriptive et post-hoc**, jamais comme verdict ni comme entrée d'un calcul. Voir §6 : la couche E est abandonnée, faute de reconstruction exacte.

### Les trois loupes (+ D)

- **A — redondance :** Spearman par paires complètes entre les 29 séries d'un cas, médiane inter-cas ; paire consensus si médiane |ρ| ≥ 0,90 ; signaux distincts par union-find. Nuls : 20 permutations par série (graine 1234). Deux règles de support : **protocole** (≥ 3 paires finies) et **pipeline** (≥ 10 paires finies ET ≥ 2 valeurs uniques par série, copie exacte de `compute_estimator_redundancy`, lignes 5462–5501).
- **B — contraste :** d de Cohen et delta de Cliff pré/post au seuil propre du run, médiane sur cas distincts ; nuls : 20 permutations par série (graine 1234).
- **C — gain incrémental :** régression logistique IRLS numpy (sklearn absent de cette VM), L2 = 1,0, CV 5 plis stratifiés graine 42, sélection gloutonne max 5 estimateurs, AUC ; 20 nuls par permutation d'étiquettes (graine 4321). Calculée une fois par cas distinct. Résultats §5, plus variante sans les 4 dégénérés (§5.3).
- **D — lectures natives (ajout v5.x, déclaré) :** classes, z, T_log, four-tests, dérivées de transition, consensus CSD, verdict L7b — extraits tels quels de `master_results.json`, comparés v59 vs v54 valeur par valeur sur les 45 sorties appariées.
- **E — couche Tc (tentée, pas exigée) :** reconstruction des cohortes comme dans le harnais d'origine (contrôle ordonné par rang, fenêtres glissantes, tolérance 3,0, w_size candidat 80 / 113). Vérification = reproduction exacte de `N_cohorts` sur les 120 points + Progress. **Non vérifiée → abandonnée** (voir §6).

### Limites connues avant lecture des résultats

1. Les séries `df_feat.csv` sont des moyennes de fenêtres glissantes, autocorrélées : les corrélations de Spearman (loupe A) ne sont pas des corrélations entre mesures indépendantes. Le protocole le savait ; la médiane inter-cas et les nuls permutés (marginales conservées) sont les gardes.
2. Quatre estimateurs sont structurellement dégénérés sur ce banc (voir §3.3) : toute corrélation ou contraste les impliquant est suspecte.
3. Le seuil propre du run sert d'étiquette (circularité déclarée) ; sans couche E vérifiée, il n'y a pas de garde externe contre cette circularité pour B et C — seulement les nuls.

## 3. Loupe A — redondance : 3 paires, 26 signaux

### 3.1 Consensus (cas distincts, médiane |ρ| ≥ 0,90)

| Banc | Version | Règle | Paires consensus | Signaux distincts |
|---|---|---|---|---|
| Ising | v59 et v54 | protocole ET pipeline | {Hurst, Hurst2mH}, {CorrelationD2, GrassbergerProcaccia}, {SpectralBeta, SpectralDimension} | **26 / 29** |
| Global (synth + Ising) | v59 et v54 | protocole ET pipeline | les 3 mêmes | **26 / 29** |
| Synth | v59 et v54 | protocole | les 3 mêmes + 23 paires impliquant Lyapunov | 6 / 29 (artefact, voir §3.3) |
| Synth | v59 et v54 | pipeline | les 3 mêmes + 9 paires impliquant Lyapunov | 17 / 29 (artefact atténué) |
| Tous bancs, **sans les 4 dégénérés** | v59 et v54 | protocole ET pipeline | les 3 mêmes | **22 / 25** |

Le résultat est **identique à v3.5.4** (mêmes 3 paires, mêmes 26 signaux), sur le banc Ising comme en global, dans les deux versions, sous les deux règles de support. La médiane |ρ| réelle est ~4× celle des nuls (global v59 : 0,259 contre 0,068 ; Ising : 0,253 contre 0,066 ; synth : 0,261 contre 0,069). Fraction de paires à |ρ| ≥ 0,90 : global 0,0347 (nul 0,0014), Ising 0,0117 (nul 0,0000), synth 0,0410 (nul 0,0017).

### 3.2 Les trois paires duplicata

- **{Hurst, Hurst2mH}** — deux estimateurs de Hurst (Hurst2mH = Hurst par la méthode 2mH). Redondance attendue : c'est le même exposant mesuré deux fois.
- **{CorrelationD2, GrassbergerProcaccia}** — deux estimateurs de la dimension de corrélation (Grassberger–Procaccia = la méthode historique, CorrelationD2 = sa formulation dimensionnelle). Redondance attendue.
- **{SpectralBeta, SpectralDimension}** — les deux faces spectrales. **Signe inversé par rapport à v3.5.4** : en v3.5.4, ρ ≈ +0,90 ; en v5.x, ρ = **−1,0** sur Target (120 points finis chacun). La paire survit en |ρ| = 1,0 mais l'une des deux séries est renversée (changement de convention de signe entre les versions du code, ou entre les constructions 30 cohortes / 120 points). À signaler, pas à interpréter : en valeur absolue, ce sont des duplicata.

Aucune autre paire ne passe le seuil de consensus dans aucun découpage (banc, version, règle, cas distincts ou tous cas). Les 26 signaux distincts sont donc : les 3 paires comptées une fois chacune (3 signaux pour 6 estimateurs) + les 23 estimateurs restants, chacun son propre signal.

### 3.3 L'artefact Lyapunov (banc synthétique)

Sur le banc synthétique seulement, la loupe A rapporte un effondrement du consensus (6 signaux sous la règle protocole, 17 sous la règle pipeline). La cause est unique et identifiée : **Lyapunov**.

- Série de Lyapunov sur synth : **13 valeurs finies sur 120, 2 valeurs uniques** (ex. Target : 0,3212 ×7 puis 0,238 ×6 — une fonction en escalier à 2 paliers). Sur certains cas : 0 valeur finie.
- Son Spearman vaut **+1,0 ou −1,0** avec 23 estimateurs (règle protocole) : toute série dont les valeurs se séparent proprement de part et d'autre du palier de Lyapunov obtient |ρ| ≥ 0,90. Ce n'est pas une redondance : c'est la signature d'un estimateur à 2 niveaux dont le point de bascule coïncide avec la transition. Le nul permuté le confirme par contraste : frac ≥ 0,90 = 0,0017 en nul contre 0,0410 en réel — l'alignement des paliers n'est pas du hasard, mais il ne dit rien de Lyapunov lui-même.
- Sous la règle pipeline (≥ 10 paires finies), l'artefact s'atténue (9 paires Lyapunov restantes, 17 signaux) sans disparaître : sur synth, les paires complètes de Lyapunov sont ≥ 10 pour 9 estimateurs.
- Sur le banc Ising, l'artefact n'existe pas : Lyapunov y a 40 valeurs finies et 33 uniques (médiane), et le consensus Ising est les 3 paires sous les deux règles.
- **Conséquence méthodologique :** exclu avec les trois autres estimateurs dégénérés (MFA, KolmogorovLZ, SingularityFmax — voir §3.4), le consensus est les 3 paires partout, sous les deux règles, dans les deux versions, sur les deux bancs : **22 signaux distincts sur 25 estimateurs non dégénérés**. C'est le chiffre à retenir pour la redondance.

### 3.4 Dégénérescence des séries (médianes par banc)

La plupart des estimateurs sont sains : 120 valeurs finies, ~109–111 uniques. Quatre sont structurellement dégénérés (fonctions en escalier, peu de paliers) ; trois autres sont fragiles.

| Estimateur | Synth (fin / uniq, min uniq) | Ising (fin / uniq, min uniq) | Statut |
|---|---|---|---|
| Lyapunov | 13 / 2 (min 0) | 40 / 33 (min 23) | **dégénéré** (synth) |
| MFA | 120 / 6 (min 2) | 120 / 6 (min 4) | **dégénéré** |
| KolmogorovLZ | 120 / 20 (min 7) | 120 / 12 (min 2) | **dégénéré** |
| SingularityFmax | 107 / 15 (min 1) | 120 / 8 (min 1) | **dégénéré** |
| TwoNN | 93 / 93 (min 3) | 89 / 83 (min 63) | fragile (NaN + paliers sur synth) |
| DANCo | — | 78 / 72 (min 60) | fragile (NaN sur Ising) |
| LevinaBickel | 102 / 102 (min 2) | 108 / 102 (min 94) | fragile (paliers sur synth) |
| Petrosian | 120 / 106 (min 66) | 120 / 110 (min 19) | fragile (paliers sur Ising) |
| PermutationEntropy | 120 / 109 (min 82) | 120 / 114 (min 19) | fragile (paliers sur Ising) |
| PersistentHomology | 115 / 109 (min 8) | 111 / 105 (min 99) | fragile (paliers sur synth) |

(Toutes les autres valeurs : 120 finies, ~107–111 uniques. NaN par sortie : 350 à 2 251 cellules sur 10 440 en single ; D_nan 2 251, attendu ; déterministe par mode, identiques v59/v54.)

### 3.5 Recoupement : la matrice de redondance propre au pipeline

Le pipeline calcule sa propre matrice (`estimator_redundancy.json`, fonction `compute_estimator_redundancy`, lignes 5462–5501 du code v5.9.0f) : Spearman par flux, médiane inter-flux, avec la règle de support ≥ 10 paires + ≥ 2 uniques. Vérifications sur `synth/A_single_fast_off` :

- La fonction du pipeline, recopiée exactement et appliquée au `df_feat.csv` sauvé, **reproduit son propre JSON exactement** (écart max 0,000000). La matrice du pipeline est donc fidèle à ses séries.
- Ma médiane (règle protocole, ≥ 3 paires) diffère de la sienne sur 65 paires non ordonnées de plus de 0,01 (130 entrées de matrice, symétrie comprise ; écart max 0,5998, médiane des écarts 0,0000). Toutes les différences concernent les estimateurs clairsemés (LevinaBickel en tête) : elles viennent **uniquement de la règle de support** (la fonction pipeline exclut Flux1 pour LevinaBickel–Hurst2mH, dont les paires complètes sont < 10 ; la médiane porte alors sur 2 flux au lieu de 3). Exemple : LevinaBickel–Hurst2mH, valeurs par flux [Target −0,5718, Flux2 +0,0839], médiane pipeline −0,2439 ; ma règle ajoute Flux1 (+0,5000) et donne +0,3559.
- Les paires consensus (les 3 duplicata) sont identiques sous les deux règles : le désaccord ne touche que les estimateurs fragiles, jamais le verdict de redondance.

## 4. Loupe B — contraste à la transition

Contraste pré/post au seuil propre du run (MC `opt_threshold`), médiane sur cas distincts. Nuls : 20 permutations par série (graine 1234), médiane |d| du nul entre parenthèses (Ising : 0,110–0,221 ; synth : 0,093–0,297).

### 4.1 Banc Ising (v59, 21 cas distincts)

| Rang | Estimateur | médiane \|d\| | médiane \|Cliff\| | nul \|d\| | NaN médian |
|---|---|---|---|---|---|
| 1 | MultifractalDeltaAlpha | **1,563** | 0,796 | 0,116 | 0 |
| 2 | Sevcik | **1,421** | 0,738 | 0,119 | 0 |
| 3 | Katz | **1,380** | 0,787 | 0,118 | 0 |
| 4 | SampleEn | 1,263 | 0,790 | 0,131 | 0 |
| 5 | GrassbergerProcaccia | 1,210 | 0,624 | 0,127 | 0 |
| 6 | DFA | 1,094 | 0,538 | 0,126 | 0 |
| 7 | Higuchi | 1,089 | 0,699 | 0,119 | 0 |
| 8–9 | Hurst / Hurst2mH | 1,088 | 0,522 | 0,118 | 0 |
| 10 | PCAIntrinsic | 1,036 | 0,535 | 0,110 | 0 |
| 11 | CorrelationD2 | 1,020 | 0,611 | 0,129 | 0 |
| 12–13 | SpectralDimension / SpectralBeta | 0,997 | 0,549 | 0,118 | 0 |
| 14 | KolmogorovLZ | 0,994 | 0,544 | 0,142 | 0 |
| 15 | PermutationEntropy | 0,853 | 0,386 | 0,132 | 0 |
| 16 | Lyapunov | 0,734 | 0,427 | 0,221 | 80,5 |
| 17 | InformationD1 | 0,628 | 0,366 | 0,137 | 3,5 |
| 18 | BoxCounting | 0,611 | 0,633 | 0,122 | 0 |
| 19 | PersistentHomology | 0,574 | 0,310 | 0,134 | 9 |
| 20 | TwoNN | 0,546 | 0,248 | 0,153 | 31 |
| 21 | LocalPCA | 0,529 | 0,313 | 0,115 | 1 |
| 22 | Fisher | 0,510 | 0,386 | 0,146 | 0 |
| 23 | MFA | 0,441 | 0,276 | 0,111 | 0 |
| 24 | DANCo | 0,440 | 0,210 | 0,159 | 41,5 |
| 25 | VisibilityGraph | 0,420 | 0,183 | 0,123 | 0 |
| 26 | SingularityFmax | 0,375 | 0,089 | 0,129 | 0 |
| 27 | GraphDimension | 0,363 | 0,248 | 0,137 | 1 |
| 28 | Petrosian | 0,350 | 0,344 | 0,118 | 0 |
| 29 | LevinaBickel | 0,242 | 0,223 | 0,143 | 11,5 |

Tous les contrastes réels dépassent leur nul d'un facteur ~1,7 à ~13,5 (médiane |d| du nul : 0,110–0,221 ; 0,110–0,159 hors Lyapunov, dont le nul est plus élevé à 0,221 parce que sa série clairsemée se permute mal). Le trio de tête (MultifractalDeltaAlpha, Sevcik, Katz) est le même qu'en v3.5.4 pour les deux premiers (1,36 et 1,29) ; en revanche Fisher (1,15 en v3.5.4 → 0,510 ici) et InformationD1 (1,15 → 0,628) chutent — comparaison indicative seulement (séries 120 points vs 30 cohortes, seuils propres différents). Hurst et Hurst2mH ont le même contraste (1,088) : cohérent avec leur redondance. SpectralBeta et SpectralDimension aussi (0,997) : cohérent.

### 4.2 Banc synthétique (v59, 50 cas distincts)

| Rang | Estimateur | médiane \|d\| | médiane \|Cliff\| | nul \|d\| |
|---|---|---|---|---|
| 1 | Lyapunov | 20,548 | 1,000 | 0,297 |
| 2 | MultifractalDeltaAlpha | 0,831 | 0,522 | 0,153 |
| 3 | Sevcik | 0,636 | 0,281 | 0,108 |
| 4 | PermutationEntropy | 0,617 | 0,339 | 0,155 |
| 5 | PersistentHomology | 0,610 | 0,418 | 0,156 |
| 6–7 | Hurst / Hurst2mH | 0,586 | 0,260 | 0,118 |
| 8 | Higuchi | 0,521 | 0,353 | 0,146 |
| … | … | … | … | … |
| 27 | MFA | 0,257 | 0,134 | 0,136 |
| 28 | LevinaBickel | 0,247 | 0,154 | 0,172 |
| 29 | BoxCounting | 0,190 | 0,264 | 0,093 |

**Lyapunov à 20,548 est un artefact** (même mécanisme qu'en loupe A : série à 2 paliers, 107 NaN sur 120, Cliff = 1,000 — séparation parfaite des deux paliers par le seuil). Sans lui, le contraste synthétique est globalement plus faible qu'en Ising (tête à 0,83 contre 1,56) : le jeu synthétique sépare moins bien que le banc Ising, ce qui est attendu (la transition synthétique est construite, la transition Ising est physique). MultifractalDeltaAlpha reste en tête sur les deux bancs. LevinaBickel est en queue sur les deux bancs (0,242 Ising, 0,247 synth) — l'estimateur le plus faible au contraste, et fragile de surcroît.

### 4.3 Comparaison v59 / v54 (loupe B)

Sur les cas appariés (mêmes sorties, mêmes séries bit-identiques), les contrastes sont identiques. Les médianes globales diffèrent légèrement parce que v54 compte 20 sorties Ising de plus (full + predict) : tête Ising v54 = Lyapunov 1,745, Sevcik 1,394, MultifractalDeltaAlpha 1,192, DFA 1,090, Katz 1,074 (contre 1,563 / 1,421 / 1,380 pour v59 fast seul). La différence vient du mélange de cas, pas du calcul des estimateurs.

## 5. Loupe C — gain incrémental en classification

Méthode gelée : régression logistique IRLS numpy (L2 = 1,0), CV 5 plis stratifiés graine 42, sélection gloutonne max 5 estimateurs, métrique AUC ; 20 nuls par permutation d'étiquettes (graine 4321). Calculée une fois par cas distinct (168 cas : 71 v59 + 97 v54), Pool(2). Étiquette pré/post = seuil propre du run (circularité déclarée).

### 5.1 Courbes AUC médianes (pas 0 = 0,5, hasard)

| Version / banc | Cas distincts | AUC pas 1 | AUC pas 2 | AUC pas 3 | AUC pas 4 | AUC pas 5 | Nul pas 1 (méd. / p95) |
|---|---|---|---|---|---|---|---|
| v59 synth | 50 | **1,000** | 1,000 | 1,000 | 1,000 | 1,000 | 0,156 / 0,317 |
| v59 Ising | 21 | 0,963 | **1,000** | 1,000 | 1,000 | 1,000 | 0,122 / 0,200 |
| v59 global | 71 | 0,989 | **1,000** | 1,000 | 1,000 | 1,000 | 0,143 / 0,304 |
| v54 synth | 50 | **1,000** | 1,000 | 1,000 | 1,000 | 1,000 | 0,156 / 0,317 |
| v54 Ising | 47 | 0,954 | 0,984 | 0,994 | **1,000** | 1,000 | 0,122 / 0,204 |
| v54 global | 97 | 0,970 | **1,000** | 1,000 | 1,000 | 1,000 | 0,134 / 0,300 |

**Point de saturation : 1 estimateur sur le banc synthétique, 2 sur le banc Ising (v59 fast seul), 4 sur l'Ising v54 (qui inclut full + predict).** En v3.5.4, la saturation était à 3 estimateurs (AUC médiane 0,933 → 0,975 → 1,000). Ici elle arrive plus tôt : les séries de 120 points séparent pré/post plus nettement que les 30 cohortes de v3.5.4 (chaque point est une moyenne de fenêtre, la structure en marche est plus propre). Les gains réels au pas 1 (0,50 synth, 0,463 Ising v59) dépassent largement le p95 des nuls (0,317 / 0,200) : la séparation est réelle, pas du surajustement — le nul, lui, ne gagne que 0,12–0,16 au pas 1 en médiane (surajustement résiduel de la sélection gloutonne sur 120 points × 29 candidats, CV 5 plis).

**Réserve sur la saturation synthétique à 1 estimateur :** sur le banc synthétique, 25 des 50 cas distincts s'ouvrent avec Lyapunov (gain 0,5, AUC 1,0) — l'estimateur dégénéré à 2 paliers, dont le palier EST la séparation pré/post. La saturation à 1 sur synth est donc portée pour moitié par l'artefact. Variante sans les 4 dégénérés : voir §5.3.

### 5.2 Qui ouvre, qui remplit

**Banc Ising v59 (21 cas) — pas de dominant :** Higuchi ouvre 9 cas, PermutationEntropy 3, MultifractalDeltaAlpha 3, puis 6 estimateurs à 1 cas chacun (SampleEn, Hurst, Sevcik, PersistentHomology, BoxCounting, Katz). AUC pas 1 : médiane 0,963, min 0,726, max 1,000 ; 8/21 cas atteignent AUC 1,0 avec un seul estimateur. En v54 Ising (47 cas, plus divers) : Higuchi 12, PermutationEntropy 8, Sevcik 6, Katz 5, MultifractalDeltaAlpha 4 — même absence de dominant.

**Sélections par estimateur (v59 Ising, sur 21 cas) :** Higuchi 17 cas (pas médian 1, gain médian 0,343) ; DFA 14 (pas 2, gain 0,000) ; Hurst 13 (pas 4, gain 0) ; Katz 11 (pas 3, gain 0) ; SampleEn 11 (pas 5, gain 0) ; PermutationEntropy 7 (pas 2, gain 0,058) ; TwoNN 6 (pas 3,5, gain 0,028) ; Lyapunov 5 (pas 3, gain 0,011) ; Sevcik 4 (pas 3, gain 0,051) ; MultifractalDeltaAlpha 3 (pas 1, gain 0,383) ; les autres ≤ 3 cas. **Lecture :** après saturation (pas 2), les sélections suivantes ont un gain médian de 0,000 — ce sont des remplissages post-saturation, pas de l'information nouvelle. C'est exactement la structure trouvée en v3.5.4 (sélections tardives sans valeur). Seuls les pas 1–2 portent du gain ; Higuchi est l'ouvreur le plus fréquent sans être dominant (9/21 au pas 1, 17/21 sélectionné au total).

**Banc synthétique v59 (50 cas) :** Lyapunov ouvre 25 cas (pas 1, gain 0,5) ; PermutationEntropy 6 (pas 1, gain 0,233) ; MultifractalDeltaAlpha 4 ; TwoNN 3 ; Sevcik, DFA, SpectralBeta, SampleEn 2 chacun. Puis le quatuor de remplissage : Higuchi sélectionné dans 38/50 cas (pas médian 2, gain 0), DFA 36/50 (pas 3, gain 0), Katz 31/50 (pas 4, gain 0), Hurst 30/50 (pas 5, gain 0). Le contraste avec l'Ising est net : sur synth, la sélection est dominée par l'artefact Lyapunov au pas 1 puis par le remplissage Higuchi/DFA/Katz/Hurst à gain nul.

### 5.3 Variante sans les 4 estimateurs dégénérés (banc synthétique)

**Résultat décisif : sans Lyapunov, MFA, KolmogorovLZ et SingularityFmax, la saturation synthétique à 1 estimateur disparaît.** Courbe AUC médiane (50 cas distincts synth, 25 candidats) : **[0,5 ; 0,891 ; 0,955 ; 0,985 ; 0,996 ; 1,0]** — saturation à **5 estimateurs** (1,0 seulement au pas 5), contre [0,5 ; 1,0 ; …] avec les dégénérés. Nul pas 1 : médiane 0,136, p95 0,252 (gain réel pas 1 : 0,391, au-dessus du p95).

Ouvreurs sans dégénérés : PermutationEntropy 11/50, MultifractalDeltaAlpha 8, SampleEn 8, DFA 4, Sevcik 4, TwoNN 3, PersistentHomology 3, SpectralBeta 3, PCAIntrinsic 2, puis 4 estimateurs à 1 cas. Aucun dominant (max 22 %). AUC pas 1 : médiane 0,891, min 0,618 ; seulement 3/50 cas à 1,0 avec un seul estimateur.

**Lecture :** la saturation à 1 sur synth était entièrement l'artefact Lyapunov. Sans lui, le banc synthétique se comporte comme un banc honnête : il faut 4 à 5 estimateurs pour saturer (0,985 au pas 3, 0,996 au pas 4), un peu plus lentement qu'en v3.5.4 (3 estimateurs) — les séries 120 points sont plus propres, mais pas au point de rendre un seul estimateur suffisant. Sur le banc Ising, en revanche, la saturation à 2 n'est PAS un artefact : Lyapunov n'y est sélectionné que dans 5/21 cas (pas médian 3, gain 0,011) et les ouvreurs sont Higuchi, PermutationEntropy et MultifractalDeltaAlpha, tous sains. Le banc Ising sépare donc réellement mieux que le banc synthétique — cohérent avec la loupe B (contrastes plus élevés en Ising).

## 6. Couche E — comparaison à Tc : ABANDONNÉE

La reconstruction des cohortes a été tentée exactement comme dans le harnais d'origine : contrôle ordonné par rang (`100*rankdata(ctrl)/len(ctrl)`, tri stable), fenêtres glissantes de taille w_size, tolérance 3,0, points de scan = linspace(0, 100, 120). Vérification exigée : reproduction exacte de `N_cohorts` sur les 120 points + Progress.

**Résultat : non vérifiée, pour les deux versions.** Meilleure règle (w_size = 113, tolérance 3,0, rang/n) : 49/120 comptes exacts, écart max 2 ; variante (rang−1)/(n−1) : 58/120, écart max 2. Fenêtres centrées : 35/120. w_size = 80 : 41/120. La règle v3.5.4 est donc proche mais pas exacte en v5.x : la définition des fenêtres (ou de l'axe) a légèrement changé entre les versions, et le code du pipeline n'a pas été fouillé pour la retrouver — ce n'est pas l'objet de cette lecture.

**Conséquence (protocole) : la couche E est abandonnée.** Aucune comparaison à Tc (2,2692) n'entre dans un calcul de ce rapport ; Tc n'apparaît que comme repère descriptif dans cette phrase. La circularité des loupes B et C (étiquette = seuil propre du run) reste couverte par les nuls permutés uniquement.

À noter : les comptes `N_cohorts` observés ([1,1,1,1,5,13,21,29,37,45,53,57,…], max ~57–59) sont compatibles avec des fenêtres à pas de 1 et une tolérance de 3,0 — la densité est bonne, c'est la forme exacte qui diffère de ±1–2 (bords et milieu). Une piste pour une reprise : la règle exacte est dans le code du pipeline (construction de `df_feat`) ; elle exigerait une lecture ciblée du code, pas une nouvelle inférence statistique.

## 7. Comparaison v5.9.0f vs v5.4.0 — la couche estimateurs n'a pas changé

| Vérification | Résultat |
|---|---|
| `df_feat.csv` bit-identiques (SHA-256) | **45 / 45** sorties appariées |
| `master_results.json` identiques | 0 / 45 (attendu : versions, télémétrie, L7b, durées diffèrent) |
| Seuils MC (`opt_threshold`) | aucune différence |
| Seuils T_0 (cascade) | aucune différence |
| Lectures natives par estimateur (loupe D) | **0 différence sur 82 940 comparaisons** (20 champs × 29 estimateurs × 143 sorties-flux) |
| Consensus A, contrastes B (cas appariés) | identiques |
| Médianes B globales | diffèrent légèrement (mélange de cas : v54 inclut full + predict) |

**Verdict :** entre v5.4.0 et v5.9.0f, le calcul des 29 estimateurs est inchangé — bit à bit. Ce qui a changé : L7b (nouvel audit), la télémétrie, le nombre de workers (3 au lieu de 4 par défaut, BLAS 1 thread/worker) et le correctif `CONTROL_MODE = "single"`. Le ralentissement mesuré à l'étape 1 (+2 % à +74 % en synth, +19 % à +26 % en fast Ising) ne vient donc pas des estimateurs.

## 8. Loupe D — lectures natives du pipeline

### 8.1 Classes : uniformes, stables, et version-invariantes

Sur les 143 sorties-flux v59 (et les 178 v54), **chaque estimateur a la même classe partout** :

| Classe native | Estimateurs (7 ou 8 chacun) |
|---|---|
| saturation (8) | Higuchi, DFA, Katz, Petrosian, Sevcik, BoxCounting, PermutationEntropy, Hurst2mH |
| criticality (7) | CorrelationD2, GrassbergerProcaccia, InformationD1, VisibilityGraph, TwoNN, DANCo, Fisher |
| divergence (7) | LevinaBickel, PCAIntrinsic, LocalPCA, GraphDimension, PersistentHomology, MFA, KolmogorovLZ |
| null_reference (7) | Hurst, SampleEn, SpectralBeta, SpectralDimension, Lyapunov, MultifractalDeltaAlpha, SingularityFmax |

La classe est une propriété de l'estimateur sur ce banc, pas du run, du mode, du contrôle ou de la version. Les trois paires duplicata de la loupe A sont cohérentes avec les classes : {CorrelationD2, GrassbergerProcaccia} sont tous deux `criticality` ; {SpectralBeta, SpectralDimension} tous deux `null_reference` ; {Hurst, Hurst2mH} en revanche se séparent — Hurst est `null_reference`, Hurst2mH est `saturation`. La classe ne suit donc pas la redondance à la lettre.

### 8.2 La classe ne mesure pas le contraste

Tension à noter : **MultifractalDeltaAlpha est classé `null_reference` par le pipeline et pourtant premier au contraste** (loupe B : 1,563 Ising, 0,831 synth). **Hurst est `null_reference` avec d = 1,088** en Ising. Inversement, Fisher est `criticality` avec un contraste médiocre (0,510). La classe native (fondée sur le z croisé contre une référence nulle) et le contraste pré/post (loupe B) mesurent deux choses différentes. Ni l'une ni l'autre n'est « la » vérité de l'estimateur : elles se lisent ensemble, comme deux loupes.

### 8.3 Autres lectures natives (médianes sur 143 sorties-flux v59)

- **z == cross_z partout** (les deux champs sont identiques — stockage redondant dans le pipeline). Médianes par estimateur : de −0,69 (SpectralBeta) à +0,68 (PCAIntrinsic), **sauf KolmogorovLZ : +4,815** — seul estimateur dont le z croisé sort de la bande, d'un facteur ~7. À surveiller, pas à interpréter seul.
- **T_log = (d − 4)·log(n), n = 960** (formule stockée dans le JSON). C'est une transformation monotone de la médiane brute `d` : son classement = celui de `d`, elle n'ajoute aucune information. Absente pour 8 estimateurs (Hurst, SampleEn, PermutationEntropy, KolmogorovLZ, SpectralBeta, Lyapunov, MultifractalDeltaAlpha, SingularityFmax — ceux dont la médiane brute n'est pas une dimension). Seuls Fisher (+1,995), LevinaBickel (+3,180), MFA (+5,298) et PCAIntrinsic (+7,116) ont un T_log positif (d > 4).
- **Four-tests** (médianes) : step1_ratio de 0,513 (BoxCounting) à 3,187 (MultifractalDeltaAlpha) ; step3_hurst_mean de 0,778 (SingularityFmax) à 1,312 (Lyapunov) ; step4_delta_slope de −0,529 (BoxCounting) à +0,425 (MultifractalDeltaAlpha). Les dérivées de transition ta_d1/ta_d2 sont minuscules partout sauf KolmogorovLZ (ta_d1 = −0,0619, ~3,5× le suivant) et LevinaBickel / MFA (−0,017).
- **CSD : csd_class == class chaque fois qu'elle existe.** Elle est **None** (abstention, pas contradiction) pour Lyapunov 92/143 cas, LevinaBickel 20/143, PersistentHomology 2/143, TwoNN 1/143 — les séries trop clairsemées pour le consensus CSD. Total : 115 désaccords apparents sur 4 147, tous des None.
- **n_valid** (four-tests et CSD) = nombre de points finis de la série : Lyapunov 13, TwoNN 92, DANCo 114 (médianes). Cohérent avec §3.4.

### 8.4 L7b (v59 seulement)

Verdict **FRAGILE sur 143/143** sorties-flux (mode light), t0_std walk-forward médian 29,40 (seuil de PASS : ≤ 10). Déclencheur quasi unique : `stabilite_walkforward` FAIL, alors que T_0 est stable d'un mode à l'autre. Rappel de l'analyse du parent (8 nov. ~14h40) : `adaptive_walk_forward_validation` recalcule l'axe de progression sur chaque fenêtre seulement — la dérive de t0_reestimated est la signature géométrique attendue d'une transition unique vue par fenêtres glissantes à axe renormalisé. Le check échoue donc sur tout système à transition unique localisée : ce n'est pas une mesure de fragilité de l'instrument. Confirmation définitive à faire par un nul permuté (dérive attendue si c'est la géométrie).

## 9. Classement par apport (synthèse des quatre loupes)

- **Porteurs du seuil (contraste fort, non redondants, sains, ouvrent en C) :** MultifractalDeltaAlpha (tête B sur les deux bancs : 1,56 Ising / 0,83 synth ; ouvre 3 cas Ising au pas 1 avec gain 0,383 ; ouvre 8 cas synth sans dégénérés), Sevcik (2e B : 1,42 / 0,64), Katz (3e B Ising : 1,38). Ce sont les trois estimateurs qui séparent le mieux pré/post au seuil propre du run.
- **Ouvreur le plus fréquent (Ising) :** Higuchi — ouvre 9/21 cas Ising (v59), sélectionné dans 17/21 (pas médian 1, gain médian 0,343) ; contraste B 1,089. Solide et fréquent, sans être dominant.
- **Solides, contraste moyen à fort :** SampleEn (B 1,26 Ising ; sélectionné 11/21 Ising, pas médian 5, gain 0 — remplissage), GrassbergerProcaccia (B 1,21 ; 1 signal avec CorrelationD2), DFA (B 1,09 ; sélectionné 14/21 Ising, pas 2, gain 0), Hurst/Hurst2mH (B 1,09 ; une seule paire, un seul signal), PCAIntrinsic (B 1,04), CorrelationD2 (B 1,02), SpectralBeta/SpectralDimension (B 1,00 ; une seule paire).
- **Utiles mais faibles au contraste :** PermutationEntropy (B 0,85 Ising / 0,62 synth ; ouvre 3 cas Ising, 11 cas synth sans dégénérés — bon ouvreur de second rang), InformationD1 (0,63), BoxCounting (0,61 ; ouvre 1 cas Ising au pas 1 avec gain 0,401), Fisher (0,51), PersistentHomology (0,57), LocalPCA (0,53), VisibilityGraph (0,42), GraphDimension (0,36), Petrosian (0,35).
- **Faibles et fragiles :** LevinaBickel (queue du contraste sur les deux bancs : 0,24 / 0,25 ; paliers sur synth ; CSD abstention 20/143), TwoNN (B 0,55 ; 27–31 NaN), DANCo (B 0,44 ; 41,5 NaN sur Ising).
- **Dégénérés — à exclure des consensus, à lire avec méfiance :** Lyapunov (2 paliers sur synth ; artefact A et C : 25/50 ouvertures synth avec AUC 1,0 ; mais contraste Ising honnête 0,734 avec 40 valeurs finies), MFA (6 paliers ; B 0,44), KolmogorovLZ (12–20 paliers ; z croisé aberrant +4,8 ; ta_d1 −0,062), SingularityFmax (8–15 paliers ; B 0,38).
- **Redondants (un signal pour deux) :** Hurst2mH = Hurst ; GrassbergerProcaccia = CorrelationD2 ; SpectralDimension = SpectralBeta (signe inversé en v5.x). Garder un seul des deux par paire suffit pour toute tâche fondée sur la série — sauf si la différence de construction (méthode 2mH, formulation spectrale) est elle-même l'objet d'étude.
- **Leçon de la loupe C :** pour classer pré/post au seuil du run, 2 estimateurs suffisent en Ising (v59 fast), 4–5 en synth sans dégénérés, 4 en Ising v54 (full + predict). Le reste est du remplissage à gain nul. Un seul estimateur ne suffit jamais hors artefact — et la saturation à 1 mesurée d'abord sur synth était l'artefact Lyapunov.

## 10. Ce qui reste ouvert

1. **Couche E** : retrouver la règle exacte de construction des fenêtres de `df_feat` (lecture ciblée du code, pas d'inférence) pour réactiver la garde Tc, ou acter définitivement son abandon en v5.x.
2. **L7b** : confirmation par un nul permuté que la dérive walk-forward est géométrique (attendue) et non une fragilité ; recalibration éventuelle du seuil t0_std ≤ 10.
3. **Signe SpectralBeta/SpectralDimension** : vérifier dans le code pourquoi ρ passe de +0,90 (v3.5.4) à −1,0 (v5.x) — changement de convention, pas de données.
4. **KolmogorovLZ (cross_z +4,8) et ta_d1 −0,062** : vérifier si c'est un vrai signal ou un artefact de sa construction (12–20 paliers).
5. **Suite du lot v5.9.0f** (étape 2 : full/fliprate relancé après le redémarrage VM ~19h39 ; étape 3 : 30 runs) : décision du fil principal, pas de cette lecture.
6. **Reprise éventuelle des lots arrêtés** (v5.4.0 à 13/36, v4.4.2 figé à 37/67) : décisions de Zackary, en attente.

## 11. Reproductibilité

- Graines : permutations A/B graine 1234 ; permutations d'étiquettes C graine 4321 ; plis CV graine 42. Seuils : consensus |ρ| ≥ 0,90 ; support protocole ≥ 3 paires, support pipeline ≥ 10 paires + ≥ 2 uniques ; tolérance E 3,0.
- Versions logicielles : Python 3.12.3, numpy 1.26.4, pandas 2.1.4, scipy 1.11.4 ; sklearn absent (logistique IRLS numpy, L2 = 1,0).
- Tous les chiffres de ce rapport sont recalculables à partir de `resultats_ABDE.json`, `resultats_A_pipeline_rule.json`, `resultats_complement.json`, `resultats_C.json` et `resultats_C_sans_degeneres.json` sous `workspace/ising-v59/harness_estimateurs/`, et du CSV une-ligne-par-estimateur `workspace/ising-v59/resultats_estimateurs.csv` (29 lignes, 62 colonnes).
