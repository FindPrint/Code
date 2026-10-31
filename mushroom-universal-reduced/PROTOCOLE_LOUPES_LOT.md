# PROTOCOLE — Loupes estimateur sur le lot réduit (gelé le 30 oct. 2026,
# avant tout run de harnais)

## Objet
Mêmes loupes que le pilote mushroom (`hp-estimator-info/PROTOCOLE_MUSHROOM.md`),
généralisées aux sorties fraîches du lot réduit : information en plus par
estimateur, sans nouveau run pipeline (lecture seule des sorties).

## Cas
- Un cas = un couple (contrôle, flux) : 22 runs × 22 flux = **484 cas**.
- Runs inclus : les 23 contrôles SAUF veil-type comme contrôle
  (opt_threshold NaN → cohortes non étiquetables, cas exclus).
  veil-type comme FLUX dans les autres runs reste inclus normalement.
- Chaque cas : 30 cohortes, 29 estimateurs, séries `_mean`.
- Noms d'estimateurs vérifiés uniformes (29 par flux, sinon arrêt).

## Loupes (paramètres gelés, identiques au pilote mushroom)
- A — redondance Spearman |ρ| ≥ 0,90 ; groupes consensus = médiane |ρ|
  ≥ 0,90 à travers les 484 cas ; 20 nuls permutation, graine 1234.
- B — contraste Cohen d + Cliff au seuil propre du run (circularité
  nommée : accord avec le seuil du pipeline, pas avec la physique) ;
  mêmes nuls, graine 1234.
- C — incrémental par (contrôle, flux) : régression logistique IRLS
  numpy L2 = 1,0, standardisation intra-pli, CV 5 plis stratifiés
  graine 42, sélection gloutonne max 5, AUC ; nuls = 20 permutations
  d'étiquettes par cas, graine 4321.
- Couche Tc : INAPPLICABLE (pas de vérité terrain sur mushroom) —
  supprimée, pas remplacée.
- NaN : Spearman paires complètes, contrastes sur cohortes finies,
  sélection sur cohortes finies pour l'ensemble évalué. Dégénérescence :
  série à < 10 cohortes finies sur 30, rapportée par (contrôle, flux).

## Sorties
`resultats_estimateurs_lot.json` + `resultats_estimateurs_lot.csv`
(dans ce dossier), SHA des 23 `numerical_results.csv` + 23
`pipeline_results.json` inscrits dans le JSON.

## Durée estimée
Version 1 run × 22 flux : ~143 s. Ici 484 cas (≈ 22×) : ~50 min
en fond, machine partagée avec rien d'autre (le lot est terminé).
