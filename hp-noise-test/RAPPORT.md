# RAPPORT — Test du discriminateur bruit-information HP sur le banc Ising

**Test exécuté le 30 octobre 2026, protocole gelé le même jour
(validé par Zackary sans amendement). Fonction
`analyze_noise_information_content` importée du fichier unique
consolidé (SHA `45dadb94…`, équivalence vérifiée pour cette fonction).
Données : banc Ising v3.5.4 validé, 960 snapshots, résidus
d'aimantation (snapshot moins moyenne de son bloc).**

## Verdict d'abord

- Le booléen `is_informative` ne prouve rien seul, comme le
  protocole l'avait prévu : réel vrai, 20/20 nuls permutés vrais,
  0/20 nuls gaussiens vrais. Il sépare le bruit blanc pur, pas les
  nuls permutés.
- Mais le discriminateur n'est pas vide : deux composantes séparent
  le réel des DEUX familles de nuls sur ce banc — entropie
  spectrale (réel 0,9613 contre ≥ 0,9754 permutés et ≥ 0,9757
  gaussiens) et longueur fractale (réel 1,4683 contre ≥ 1,5021
  permutés et ≥ 1,5781 gaussiens). Hurst, lui, ne sépare pas
  (réel 0,4828 dans les deux gammes de nuls).
- Conclusion, composante par composante : lire le discriminateur
  par ses composantes, jamais par son booléen. Sur ce banc, le
  « bruit » résiduel réel porte une structure spectrale que les
  nuls n'ont pas — c'est une information, pas une preuve à elle
  seule, et elle ne vaut que pour ce banc et ce flux.

## Résultats complets

| Série | Informatif | Hurst | Kurtosis | Skewness | p Jarque-Bera | Long. fractale | Entropie spectrale |
|---|---|---|---|---|---|---|---|
| R_all (960) | vrai | 0,4828 | 5,258 | −0,2432 | 6,44e−243 | 1,4683 | 0,9613 |
| R_pre (320) | vrai | 0,4120 | 7,2432 | −1,6151 | 7,77e−183 | 1,5066 | 0,9165 |
| R_post (600) | vrai | 0,4751 | 1,7886 | 0,2170 | 4,07e−19 | 1,5141 | 0,9613 |
| Nuls permutés ×20 | 20/20 vrais | 0,4761–0,5705 (méd. 0,5153) | = réel | = réel | ≈ réel | 1,5021–1,5618 (méd. 1,5421) | 0,9754–0,9844 (méd. 0,9820) |
| Nuls gaussiens ×20 | 0/20 vrais | 0,4794–0,5694 (méd. 0,5081) | — | — | 0,0253–0,8646 (méd. 0,3642) | 1,5781–1,6450 (méd. 1,6059) | 0,9757–0,9866 (méd. 0,9819) |

## Lecture, composante par composante

- **Jarque-Bera / kurtosis / skewness** : identiques entre R_all et
  ses nuls permutés, en substance — kurtosis et skewness à une
  seule valeur unique sur les 20 nuls ; p de Jarque-Bera à
  6,443517e−243 partout, avec 3 valeurs distinctes seulement
  au-delà de la 7e décimale (ordre de sommation flottante, pas
  une différence de fond). Ces trois composantes ne séparent
  donc pas le réel du nul permuté, par construction. C'est le
  point de méthode du protocole, confirmé, pas découvert après.
- **Hurst (R/S)** : réel 0,4828, dans la gamme des permutés
  (0,4761–0,5705) et des gaussiens (0,4794–0,5694). Ne sépare pas
  sur ce banc. La persistance R/S ne voit rien ici que les nuls
  ne voient aussi.
- **Entropie spectrale (Welch, fs=1000 arbitraire, même
  segmentation pour réel et nuls, donc comparaison équitable)** :
  réel 0,9613, sous le minimum des deux familles de nuls
  (0,9754 / 0,9757). Le spectre réel est moins plat, plus
  structuré. C'est la séparation la plus nette du test.
- **Longueur fractale** : réel 1,4683, sous le minimum des deux
  familles (1,5021 / 1,5781). Réserve dite : une série ordonnée
  est plus lisse qu'une série mélangée par construction, donc
  cette composante favorise mécaniquement l'ordre — elle sépare
  ici, mais elle ne prouve pas à elle seule une structure
  physique.
- **Pré vs post** : différences marquées — kurtosis 7,2432 vs
  1,7886, skewness −1,6151 vs 0,2170, entropie 0,9165 vs 0,9613.
  Descriptif seulement : aucun nul dédié pré/post n'était gelé
  dans le protocole, donc cet écart n'est pas jugé contre des
  nuls. À ne pas conclure sans nuls pré/post propres.

## Précisions et limites (dites, pas cachées)

- Repère 2,2565 : c'est la valeur ARRONDIS du point de grille
  2,2565217… (9e bloc). Le partage pré (8 blocs, 320 points) /
  repère (1 bloc, 40) / post (15 blocs, 600) est celui du
  protocole ; seule la tolérance de l'assertion du harnais a été
  corrigée (1e-9 → 1e-3), pas le protocole.
- Fonction testée via le fichier unique consolidé, pas la chaîne
  3 fichiers — équivalence vérifiée pour cette fonction le
  30 oct. 2026, pas sur un lot complet.
- Un seul banc, un seul flux (résidus d'aimantation). Aucune
  généralisation au-delà.
- La prédiction L1–L7, la saliency et le diagnostic de bruit
  v3.5.4 en 4 étapes ne sont pas testés ici. Les dossiers PC de
  Zackary n'ont pas été testés (inaccessibles depuis cette VM).

## Fichiers

- `PROTOCOLE.md` (gelé 30 oct. 2026, validé sans amendement),
  `PROTOCOLE_DRAFT.md` (conservé tel quel),
  `harness_noise.py`, `resultats_noise.json`,
  `resultats_noise.csv`.
- Publication GitHub : NON faite — le protocole la réserve à la
  décision de Zackary après ce rapport.
