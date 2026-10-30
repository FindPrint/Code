# PROTOCOLE GELÉ — Information en plus par estimateur, banc Ising

**Gel : 30 octobre 2026, validé par Zackary sans amendement (« allez s'y »).
AUCUN nouveau run pipeline : l'analyse porte sur les sorties déjà
vérifiées du lot v3.5.4, relues seulement. Le brouillon
(PROTOCOLE_DRAFT.md) est conservé tel quel pour la traçabilité.**

*DRAFT, 30 Oct. 2026 — not frozen until Zackary approves it. No run
launched under it. No new pipeline run: re-analysis of the already
verified v3.5.4 lot outputs only.*

## 1. Question

Sur le banc Ising, que vaut chaque estimateur de complexité EN PLUS
des autres — lequel est redondant, lequel porte le seuil, lequel
ajoute une information que les autres n'ont pas ? Trois loupes,
chacune contre ses nuls : redondance, contraste à la transition,
gain incrémental en classification.

*On the Ising bench, what is each complexity estimator worth ON TOP
of the others — which is redundant, which carries the threshold,
which adds information the others lack? Three loupes, each against
its nulls: redundancy, transition contrast, incremental
classification gain.*

## 2. Données (sorties vérifiées du lot v3.5.4, pas de nouveau run)

- `workspace/ising-v354/runs/<contrôle>/numerical_results.csv` —
  6 runs (un par contrôle : energy, flip, fliprate, localvar,
  magnetization, susceptibility), 30 cohortes × 292 colonnes chacun.
- Vérifié le 30 oct. 2026 : chaque run contient bien 29 estimateurs
  × 5 flux analysés (le contrôle est exclu, règle Porte D), en
  colonnes `<flux>_<estimateur>_mean` et `<flux>_<estimateur>_std`.
  Les noms des 29 estimateurs sont extraits des colonnes à
  l'exécution ; si le compte n'est pas 29 pour un flux, arrêt et
  rapport, pas de run partiel.
- `pipeline_results.json` de chaque run : `metadata.opt_threshold`
  (seuil propre du pipeline pour ce run) et `metadata.n_pts` = 960.
- Les SHA-256 des 6 fichiers d'entrée sont calculés par le harnais
  et inscrits dans les sorties (pas de SHA inventé ici).
- Nature : snapshots SIMULÉS du banc Ising (L=32, T 1,7–3,3),
  pas mesurés. Les 6 runs partagent les mêmes snapshots sous 6
  contrôles différents : ils ne sont PAS indépendants. Le
  consensus entre runs est une médiane descriptive, jamais une
  mise en commun statistique.

## 3. Séries (relues, jamais recalculées par le pipeline)

- Par run, par flux (5), par estimateur (29) : la série des 30
  moyennes de cohorte (`<flux>_<estimateur>_mean`), axe = colonne
  `Progress` (0,10–100 %). Les colonnes `_std` servent de
  contexte de dispersion, pas de série principale.
- Étiquette de régime (pour les loupes B et C seulement) : cohorte
  pré vs post au seuil `opt_threshold` DU RUN. Circularité dite
  d'avance : cette étiquette vient du pipeline lui-même, donc les
  loupes B et C mesurent l'accord avec le seuil du pipeline, pas
  avec la physique. La comparaison à Tc reste descriptive et
  post-hoc (couche E, tentée seulement si la reconstruction
  vérifie).

## 4. Loupes (gelées dans le brouillon, paramètres nommés)

- **A — Redondance (aucune étiquette requise).** Par flux et par
  run : matrice de Spearman ρ entre les 29 séries moyennes.
  Paires quasi-duplicata : |ρ| ≥ 0,90 (seuil conventionnel,
  nommé, pas découvert). Sorties : paires et groupes à |ρ| ≥ 0,90,
  estimateurs singletons (aucun |ρ| ≥ 0,90 avec un autre), médiane
  de |ρ| par estimateur à travers runs et flux.
- **B — Contraste à la transition.** Par estimateur, par flux, par
  run : d de Cohen et delta de Cliff entre cohortes pré et post
  (étiquette opt_threshold du run). Classement par médiane de |d|
  à travers runs et flux. Un estimateur plat à la transition a un
  contraste proche de zéro, même s'il est « complexe ».
- **C — Gain incrémental.** Par run : régression logistique sur
  séries standardisées, étiquette pré/post opt_threshold,
  validation croisée 5 plis (plis fixes, graine 42), métrique AUC.
  Sélection ascendante gloutonne, 5 estimateurs maximum
  (plafond anti-surajustement, 30 cohortes seulement) : à chaque
  pas, l'estimateur qui donne le plus grand gain d'AUC-CV.
  Le « plus » d'un estimateur = son gain d'AUC au pas où il est
  sélectionné, et le pas médian de sa sélection à travers runs.
- **Nuls (même doctrine que les tests cascade et bruit).**
  A et B : 20 permutations de chaque série à travers les cohortes
  (graine 1234) — marginales conservées, ordre brisé. C : 20
  permutations des étiquettes par run (graine 4321) — distributions
  nulles des gains d'AUC. Chaque résultat réel est comparé à sa
  distribution nulle, jamais lu seul.
- **E — Couche Tc descriptive (tentée, pas exigée).** Le harnais
  tente de reconstruire la T médiane de chaque cohorte à partir
  du banc et de la règle de cohortes du code v3.5.4. Si la
  reconstruction vérifie exactement (tailles de cohortes et
  Progress retrouvés), les contrastes B sont aussi rapportés
  avec un partage pré/post Tc (descriptif post-hoc, comme le lot).
  Sinon, la couche E est rapportée « reconstruction non vérifiée »
  et abandonnée, sans toucher aux loupes A–D.

## 5. Jugement (écrit avant les runs)

- (a) Redondance : quels estimateurs sont quasi-duplicata de quels
  autres (groupes |ρ| ≥ 0,90), lesquels sont singletons, réel
  contre nuls permutés.
- (b) Contraste : quels estimateurs bougent à la transition
  (médiane |d| haute, au-dessus de leurs nuls), lesquels sont
  plats.
- (c) Incrémental : ordre de sélection par run, gain d'AUC par
  pas, consensus entre runs ; un estimateur sélectionné tard ou
  jamais, ou dont le gain ne dépasse pas ses nuls, n'apporte rien
  en plus — même si son contraste seul est bon (cas typique
  d'un duplicata).
- (d) Aucune conclusion tirée d'un seul run : chaque résultat est
  donné par run et en médiane descriptive des 6 runs.
- (e) Aucun verdict « cet estimateur ne sert à rien » à partir
  d'une seule loupe : un estimateur peut être redondant ici
  (banc Ising, 30 cohortes) et informatif ailleurs. Le verdict
  porte sur ce banc seulement.

## 6. Sorties (tout gardé, rien dans /tmp)

- `harness_estimator_info.py` — harnais (lecture seule des sorties
  du lot).
- `resultats_estimateurs.json` — sorties complètes par run, flux,
  estimateur et nul.
- `resultats_estimateurs.csv` — synthèse une ligne par estimateur
  (médianes, rangs, gains, comparaisons nulles).
- `RAPPORT.md` — verdict par loupe, avec les groupes de
  redondance et l'ordre incrémental.
- Publication, si Zackary le décide après le rapport : dépôt privé
  FindPrint/Code, dossier `hp-estimator-info/`, fichiers texte
  seulement.

## 7. Ce que ce test ne fait PAS

- Il ne relance pas le pipeline (coût ×10 évité : réutilisation
  des sorties vérifiées).
- Il ne teste pas la prédiction L1–L7 ni la saliency.
- Il ne valide pas les dossiers PC de Zackary (inaccessibles
  depuis cette VM).
- Il ne fusionne pas les 6 runs : le consensus est descriptif.
