# RAPPORT — Information en plus par estimateur, banc Ising v3.5.4

**Test exécuté le 30 octobre 2026, protocole gelé le même jour
(validé par Zackary sans amendement). Aucun nouveau run pipeline :
ré-analyse des sorties vérifiées du lot v3.5.4 (6 runs, 30 cohortes,
29 estimateurs × 5 flux par run).**

*Re-analysis of the verified v3.5.4 lot outputs only. No new pipeline
run. Frozen protocol: PROTOCOLE.md (draft kept as PROTOCOLE_DRAFT.md).*

## 1. Verdict d'abord

- **Redondance — seulement 3 paires duplicata sur 29 estimateurs.**
  CorrelationD2 = GrassbergerProcaccia, Hurst = Hurst2mH,
  SpectralBeta = SpectralDimension (médiane |ρ| ≥ 0,90 à travers les
  30 cas run × flux). Tout le reste est singleton au niveau
  consensus : la batterie porte **26 signaux distincts**, pas 29
  copies. Médiane |ρ| réelle 0,30 contre 0,13 pour les nuls ;
  1,7 % des paires ≥ 0,90 contre 0 % sous permutation.
- **Contraste — la plupart bougent à la transition, un seul est
  plat.** Médianes |d| réelles 0,19–1,36 contre 0,19–0,31 pour les
  nuls. Tête : MultifractalDeltaAlpha 1,36, Sevcik 1,29,
  Fisher 1,15, InformationD1 1,15, Hurst/Hurst2mH 1,08.
  **Lyapunov est plat** (0,19, sous son nul 0,22) : il n'apporte
  rien ici. Petrosian 0,34 et LevinaBickel 0,36 sont faibles.
- **Incrémental — 3 estimateurs suffisent, le reste est du
  remplissage.** AUC médiane (validation croisée) : **0,933 avec
  1 estimateur, 0,975 avec 2, 1,000 avec 3**, puis saturée.
  Au-delà de 3, le « plus » vaut 0 sur ce banc. Aucun ouvreur
  dominant : Hurst ouvre 6 fois sur 30, CorrelationD2 5,
  Higuchi 5, MultifractalDeltaAlpha 4 — l'information est
  distribuée, pas tenue par un seul estimateur. Gains du pas 1
  dépassant le p95 nul (0,345 ; médiane nulle 0,233) : Katz 0,446,
  MultifractalDeltaAlpha 0,417, InformationD1 0,408, Hurst 0,35.
- **Couche Tc descriptive — le classement survit à l'épreuve
  indépendante.** Reconstruction des cohortes vérifiée (tailles
  N_cohorts et Progress retrouvés exactement). Corrélation de
  rangs **Spearman 0,95** entre les contrastes au seuil du
  pipeline (B) et au partage Tc (E) : les estimateurs qui
  suivent le seuil du pipeline suivent aussi la vraie
  transition. Tête E : MultifractalDeltaAlpha 1,31,
  Sevcik 1,08, Hurst/Hurst2mH 1,08. Lyapunov reste plat (0,20).
- **Avertissement de lecture — ne pas confondre sélection et
  importance.** DFA est sélectionné 24 fois sur 30 mais au pas
  médian 4 avec un gain de 0,00 ; CorrelationD2 22 fois, pas
  médian 3, gain 0,00. Après saturation de l'AUC, la sélection
  remplit les 5 places, elle ne mesure plus d'information.
- **Fragilité.** SpectralBeta/SpectralDimension sont duplicata
  ET fragiles (médiane 3,5 cohortes NaN par cas, jusqu'à 10) ;
  TwoNN et Lyapunov ~1 cohorte NaN en médiane. Un estimateur
  qui rend NaN sur un tiers des cohortes est fragile, même si
  son contraste est bon.

## 2. Méthode (précisions déclarées, protocole gelé respecté)

- Données : `workspace/ising-v354/runs/<contrôle>/numerical_results.csv`
  (SHA-256 des 12 fichiers d'entrée dans `resultats_estimateurs.json`).
  29 estimateurs vérifiés par flux et par run avant tout calcul.
- Loupe A : Spearman entre séries moyennes (30 cohortes), paires
  complètes pour les NaN ; consensus = médiane |ρ| ≥ 0,90 sur les
  30 cas ; nuls = 20 permutations par série (graine 1234).
- Loupe B : d de Cohen et delta de Cliff, partage pré/post au
  seuil propre du run ; nuls = mêmes 20 permutations.
- Loupe C : régression logistique (IRLS numpy, pénalité L2 1,0 —
  sklearn absent de cette VM, installation système bloquée
  PEP 668), séries standardisées intra-pli, CV 5 plis stratifiés
  (graine 42), sélection gloutonne max 5, métrique AUC ;
  **faite par (run, flux)** — les colonnes d'estimateurs vivent
  par flux, et 30 cohortes ne portent pas une sélection sur 145
  prédicteurs ; paramètres gelés inchangés. Nuls = 20 permutations
  d'étiquettes par (run, flux) (graine 4321).
- Couche E : T médiane de chaque cohorte reconstruite depuis le
  banc et la règle de cohortes du code v3.5.4 (fenêtres glissantes
  w_size du run, tolérance 3,0) ; vérification exacte avant usage.
- Correctif documenté (2e passe, `fix_couche_E.py`) : le harnais
  propageait un NaN à tout l'estimateur (médiane non NaN-aware),
  et une première passe signée annulait des contrastes forts de
  signes opposés entre runs à contrôles de monotonies inverses.
  Les valeurs E finales sont des médianes de |d| par cellule en
  nanmedian. Les deux erreurs sont ici, pas effacées.

## 3. Synthèse par estimateur (médianes sur 30 cas run × flux)

Voir `resultats_estimateurs.csv` (une ligne par estimateur) et
`resultats_estimateurs.json` (sorties complètes). Extraits :

| Estimateur | \|ρ\| médian | \|d\| seuil | \|d\| Tc | Sélections /30 | Pas médian |
|---|---|---|---|---|---|
| MultifractalDeltaAlpha | 0,44 | 1,36 | 1,31 | 7 | 1 |
| Sevcik | 0,40 | 1,29 | 1,08 | 0 | — |
| InformationD1 | 0,25 | 1,15 | 0,86 | 2 | 1 |
| Fisher | 0,44 | 1,15 | 0,95 | 9 | 5 |
| Hurst | 0,36 | 1,08 | 1,08 | 8 | 1 |
| CorrelationD2 | 0,38 | 0,98 | 0,98 | 22 | 3 |
| DFA | 0,34 | 0,80 | 0,87 | 24 | 4 |
| Lyapunov | 0,23 | 0,19 | 0,20 | 1 | 3 |

Groupes duplicata consensus : {CorrelationD2, GrassbergerProcaccia},
{Hurst, Hurst2mH}, {SpectralBeta, SpectralDimension}.

Courbe AUC médiane réelle : pas 1 = 0,933 ; pas 2 = 0,975 ;
pas 3 = 1,000 ; pas 4 = 1,000 ; pas 5 = 1,000.
Nuls du pas 1 : gain médian 0,233, p95 0,345.

## 4. Limites (dites, pas cachées)

- Un seul banc (Ising simulé L=32), 30 cohortes seulement.
- Les 6 runs partagent les mêmes snapshots : le consensus entre
  runs est une médiane descriptive, jamais une mise en commun
  statistique.
- Circularité nommée de la loupe C (et B) : l'étiquette pré/post
  est le seuil du pipeline, construit sur ces mêmes colonnes.
  La couche E (partage Tc, indépendant du pipeline) est la garde
  contre cette circularité — et elle confirme le classement
  (Spearman 0,95).
- Seuls les nuls du pas 1 sont résumés dans les sorties ; les
  gains des pas 2 et 3 ne sont pas comparés à leurs nuls, donc
  pas déclarés significatifs — seule la saturation à 1,000 est
  factuelle.
- Verdict sur ce banc seulement : un estimateur redondant ou plat
  ici peut être informatif ailleurs.

## 5. Sorties

- `harness_estimator_info.py` — harnais (lecture seule du lot).
- `fix_couche_E.py` — correctif documenté de la couche Tc.
- `resultats_estimateurs.json` — sorties complètes, SHA d'entrée.
- `resultats_estimateurs.csv` — une ligne par estimateur.
- `PROTOCOLE.md` — protocole gelé ; `PROTOCOLE_DRAFT.md` —
  brouillon conservé.
- Publication, si Zackary le décide après ce rapport : dépôt
  privé FindPrint/Code, dossier `hp-estimator-info/`, fichiers
  texte seulement.
