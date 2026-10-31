# RAPPORT — Loupes estimateur sur le lot réduit UNIVERSAL_LOG (30 oct. 2026)

## Verdict
- **25 signaux distincts sur 29** : 4 paires duplicata seulement
  (CorrelationD2 = GrassbergerProcaccia, Hurst = Hurst2mH,
  Katz = Petrosian, SpectralBeta = SpectralDimension). Tout le reste
  est singleton au consensus.
- **Les têtes de contraste sont la famille entropie/complexité** :
  PermutationEntropy (2,28), Petrosian (2,05), Sevcik (1,82), Katz (1,68),
  SampleEn (1,66) — très au-dessus des nuls (~0,32). La hiérarchie ne se
  transfère pas d'Ising (où MultifractalDeltaAlpha dominait à 1,36 ; ici
  1,16) : chaque domaine a ses propres loupes fortes.
- **Saturation AUC dès le pas 1** (médiane 1,000 sur 374 cas), comme au
  pilote — mais 110 cas sans aucune sélection (étiquetages dégénérés par
  seuils extrêmes) et un remplissage post-saturation massif
  (BoxCounting 362/484 à gain 0, DFA 340/484 à gain 0) : les sélections
  tardives ne sont pas de l'importance.
- **Aucun ouvreur dominant** : BoxCounting 77, DFA 38, CorrelationD2 36,
  Higuchi 32, Fisher 24, DANCo 24, Katz 22… — même motif que sur Ising
  et sur le pilote.

## Matériel et méthode
- Sorties du lot réduit (`mushroom-universal-reduced/ctrl_*/`), code
  UNIVERSAL_LOG v3.5.5-HP-v1 SHA `2f58d414…`, données réduites 2 000 lignes
  SHA `dee93263…`. Lecture seule, aucun nouveau run pipeline.
- Cas : **484 = 22 runs × 22 flux** (30 cohortes, 29 estimateurs, séries
  `_mean`). veil-type EXCLU comme contrôle (seuil NaN, cohortes non
  étiquetables) ; inclus comme flux dans les autres runs.
- Paramètres gelés (`PROTOCOLE_LOUPES_LOT.md`) : Spearman ≥ 0,90 ;
  Cohen d + Cliff au seuil propre du run ; logistique IRLS L2 = 1,0,
  CV 5 plis graine 42, gloutonne max 5, AUC ; nuls 20 permutations,
  graines 1234 (A/B) et 4321 (C). Couche Tc inapplicable (pas de vérité
  terrain).
- SHA des 46 fichiers d'entrée inscrits dans
  `resultats_estimateurs_lot.json`. Tableau complet par estimateur :
  `resultats_estimateurs_lot.csv`.

## Loupe A — redondance
- Médiane |ρ| réelle **0,4498** vs nulle **0,1426** ; paires ≥ 0,90 :
  **12,08 %** réel vs **0,39 %** nul.
- Paires consensus (médiane |ρ| ≥ 0,90 sur les 484 cas) :
  CorrelationD2–GrassbergerProcaccia, Hurst–Hurst2mH, Katz–Petrosian,
  SpectralBeta–SpectralDimension → **25 signaux distincts**.
- Comparaisons : Ising (lot v3.5.4) = 3 paires, 26 distincts ; pilote
  mushroom (1 run class) = 3 paires + 1 triple inédit
  {PermutationEntropy, Petrosian, Sevcik}, 24 distincts.
- Nouveauté du lot : le triple pilote ne survit pas comme groupe —
  Petrosian s'apparie avec Katz (0,9168), pas avec PermutationEntropy
  ni Sevcik au-dessus du seuil. Les duplicata structurels
  (CorrelationD2, Hurst, Spectral) persistent dans les trois jeux ;
  les appariements « mous » (Katz–Petrosian, triple pilote) dépendent
  du jeu et du contrôle — ce ne sont pas des identités d'estimateurs.

## Loupe B — contraste au seuil propre du run
Têtes (médiane |d| réel, nul entre parenthèses) :
PermutationEntropy **2,28** (0,32), Petrosian **2,05** (0,32),
Sevcik **1,82** (0,32), Katz **1,68** (0,32), SampleEn **1,66** (0,32),
LocalPCA **1,60** (0,33), BoxCounting **1,55** (0,28),
VisibilityGraph **1,53** (0,31), Higuchi 1,26, Hurst 1,25,
PCAIntrinsic 1,23, Fisher 1,08, MultifractalDeltaAlpha 1,16.
Bas : PersistentHomology **0,19** (0,09), SingularityFmax 0,63,
InformationD1 0,66 (nul 0,15), Lyapunov 0,69, TwoNN 0,75, MFA 0,81.
- Lecture : les 4 premiers dépassent 1,65, soit 5× leurs nuls. Fisher,
  tête du pilote (0,95), reste présente (1,08) sans dominer.
  MultifractalDeltaAlpha, tête d'Ising (1,36), tombe à 1,16 et
  InformationD1 (1,15 sur Ising, 0,15 au pilote) à 0,66 : la hiérarchie
  est propre à chaque domaine, pas une propriété des estimateurs seuls.
- Circularité nommée : le contraste est mesuré au seuil propre du run,
  choisi pour maximiser le contraste Monte Carlo — c'est un accord avec
  le seuil du pipeline, pas avec une physique. Les nuls (même seuil,
  séries permutées) bornent cet effet : l'écart réel–nul reste massif.

## Loupe C — gain incrémental AUC
- Courbe AUC médiane : **1,000 dès le pas 1** (et à tous les pas),
  sur 374 cas avec sélection. Détail pas 1 : 312 cas à 1,000, 17 à 0,500,
  45 entre les deux.
- **110 cas sans aucune sélection** : la sélection gloutonne ne trouve
  rien — étiquetages dégénérés par seuils extrêmes (ex. spore-print-color
  98,89 %, gill-color 99,37 %, population 96,46 % : 0–1 cohorte d'un côté,
  étiquette quasi constante). C n'informe rien sur ces cas.
- Ouvreurs pas 1 distribués, aucun dominant : BoxCounting 77, DFA 38,
  CorrelationD2 36, Higuchi 32, Fisher 24, DANCo 24, Katz 22,
  GraphDimension 19, PermutationEntropy 18…
- Remplissage post-saturation (avertissement déjà livré sur Ising et
  pilote) : BoxCounting sélectionné 362/484 fois à gain médian 0,00,
  DFA 340/484 à gain 0,00, CorrelationD2 300/484 à gain 0,00. Dans une
  paire duplicata, le premier tiré absorbe les sélections :
  GrassbergerProcaccia 16 (vs CorrelationD2 300), Hurst2mH 3 (vs Hurst 29),
  SpectralDimension 0 (vs SpectralBeta 6), Petrosian 1 (vs Katz 27).
- Gains pas 1 réels de 0,50 (Katz, PermutationEntropy, SampleEn,
  InformationD1, LocalPCA, MultifractalDeltaAlpha…) contre nul médian
  0,2444 / p95 0,4444 : au-dessus du p95 nul, mais modestement.
- Caveat : 30 cohortes, 29 candidats, CV 5 plis (~6 cohortes par pli
  test) — la sélection gloutonne surajuste. Un AUC médian de 1,000 ne
  doit pas se lire comme « prédiction parfaite », mais comme
  « séparation immédiate sur ces cohortes, y compris par surajustement ».

## Dégénérescence
- **219/484 cas** ont ≥ 1 série dégénérée (< 10 cohortes finies sur 30).
  Par estimateur : TwoNN 114, PersistentHomology 100,
  CorrelationD2 / GrassbergerProcaccia 77, InformationD1 64, DANCo 47,
  LevinaBickel 29, Lyapunov 27, SpectralBeta / SpectralDimension 16.
- Médiane de cohortes NaN par estimateur = 0,0 partout sauf Lyapunov
  (1,0) : la dégénérescence est concentrée dans certains cas, pas
  diffuse. TwoNN et PersistentHomology échouent sur données discrètes
  liées (distances nulles, complexes dégénérés) — cohérent avec la
  métastabilité par décisions discrètes déjà établie sur mushroom.

## Limites (dites, pas cachées)
- Les 484 cas ne sont PAS indépendants : mêmes 2 000 lignes, relues par
  22 contrôles. Les médianes décrivent le lot, pas 484 expériences.
- Contrastes mesurés aux seuils propres (circularité, voir loupe B).
- Aucune comparaison directe au pilote v3.5 (autres lignes) et aucune
  couche Tc (pas de vérité terrain).
- Données = échantillons HYPOTHÉTIQUES du guide Audubon 1981, pas des
  spécimens mesurés ; couleurs/odeurs = mots humains.

## Conclusion
Sur sorties fraîches UNIVERSAL_LOG, le lot réduit confirme les trois
motifs déjà vus — duplicata structurels stables, hiérarchie de contraste
propre au domaine (entropie en tête sur mushroom), saturation AUC
immédiate avec remplissage — et ajoute deux faits : Katz–Petrosian
comme 4e paire (le triple pilote ne se généralise pas) et 110 cas
muets par seuils extrêmes. Le prochain pas utile, si Zackary le veut :
la comparaison réel-vs-nul loupe par loupe sur un jeu à vérité terrain
(Ising), ou les flux mesurés (couleurs RVB-Lab, VOC) comme futurs flux.

## Suite
Publication GitHub du lot réduit + ce rapport, sur décision de Zackary.
Fichiers : `resultats_estimateurs_lot.json`,
`resultats_estimateurs_lot.csv`, `harness_estimator_info_lot.py`,
`PROTOCOLE_LOUPES_LOT.md`, `SYNTHESE.md`.
