# PROTOCOLE GELÉ — Test de la cascade 5 seuils v3.7.0-HP-v3 sur le banc Ising

**Gel : 30 octobre 2026, avant tout run de ce test. Aucune modification
après le gel sans nouvelle version datée.**
*Frozen 30 Oct. 2026, before any run of this test.*

## 1. Question

La cascade 5 seuils de v3.7.0 (`compute_5_threshold_cascade`, dérivées F1/F2
d'une série lissée) localise-t-elle un seuil central T_0 sur le banc Ising
2D déjà validé, et que vaut ce résultat face aux nuls — loupe par loupe ?
Question d'attribution jointe : le flux décompressé E_thermal porte-t-il
une information propre, ou celle de T seul, ou celle de M seul ?

*Does the v3.7.0 5-threshold cascade locate a central threshold T_0 on the
already-validated 2D Ising bench, and what is it worth against nulls,
loupe by loupe? Joined attribution question: does the decompressed flux
E_thermal carry its own information, T's alone, or M's alone?*

## 2. Code sous test (reçu, jamais modifié)

- `Tlog_v3_5_5_HP_v1.py` — 6 012 lignes, SHA-256
  `24e6549536091bb1b1429856a3b42607a5e7328851a6061f209b4610ed87de6e`
- `Tlog_v3_6_0_HP_v2.py` — 872 lignes, SHA-256
  `7a6948483e8995370ed0c581dd97215bcb1d2ad7dfeed5b29a95cb37f40c31c1`
- `Tlog_v3_7_0_HP_v3.py` — 568 lignes, SHA-256
  `8527b92ccd2eda0ad3b0205eb63fe380cc0046741132d2e81bcc13dff14056fc`
- Chaîne d'import : v3.7.0 charge v3.6.0, qui charge v3.5.5
  (`SourceFileLoader`, fichiers voisins). Originaux dans
  `workspace/user/files/`, intacts. Copies SHA-vérifiées dans
  `sources/` du présent dossier, pour l'archive seulement.
- Fonction testée : `compute_5_threshold_cascade`, paramètres PAR DÉFAUT
  (`smooth_sigma=3.0`, `min_dist=3.0`). Aucun réglage pendant le test.
- Remarque de lecture (pas un résultat) : la clé de sortie s'appelle
  `T_0_Monte_Carlo_Central`, mais le calcul est argmax|F1| sur série
  lissée — ce n'est pas un seuil Monte Carlo. Le nom ne fait pas la mesure.

## 3. Données (banc validé, pas de nouvelles données)

- `workspace/ising-v354/data/ising_classic_v354.csv` — 960 lignes,
  6 flux (`fliprate, flip, energy, magnetization, localvar,
  susceptibility`), SHA-256
  `9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d`.
- `workspace/ising-v354/data/ising_classic_v354_temperature.csv` — 960
  lignes, colonne `temperature`, SHA-256
  `4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4`.
- Générateur : Ising 2D, L=32, J=1, Metropolis damier, graine 42,
  T = linspace(1.7, 3.3, 24), 40 snapshots par T (protocole gelé du
  28 oct. 2026, `workspace/ising-v354/PROTOCOLE.md`).
- Nature : snapshots SIMULÉS, pas mesurés. T ne sert qu'au harnais
  (construction des séries + conversion descriptive %→T après coup).
  La cascade ne voit que des rangs % et des séries y.

## 4. Séries (construites par le harnais, hors pipeline)

- Axe de progrès : p = 100 × rang(T) / n (rangs moyens, `rankdata`),
  jamais les valeurs de T.
- V1 (primaire) : y = aimantation moyenne par T (24 points),
  p = rangs % des 24 T.
- V1b (robustesse, secondaire) : y = aimantation par snapshot, triée
  par T (960 points), p = rangs % des 960 T répétés.
- V2 : y = E_thermal reconstruit par le harnais avec LA formule de la
  décompression : E = T/4 × (1−M+0,2), normalisé min-max, clip [0,1],
  sur les moyennes par T (24 points).
- V3 (attribution, T seul) : E_thermal avec M permuté entre les T
  (graine 7), T intact.
- V4 (attribution, M seul) : E_thermal avec T permuté entre les M
  (graine 8), M intact.
- V5 (nuls) : 20 permutations de y(V1), p fixe, graine 1234
  (permutations 0–19). Le nul conserve les marginales et brise
  seulement la structure testée (l'ordre en T).

## 5. Conversion %→T (harnais seulement, descriptive)

T_0(%) → T par interpolation sur les 24 T triés. Cette conversion est
un jugement descriptif post-hoc, sans règle succès/échec et sans retour
dans aucun paramètre — même séparation que le lot v3.5.4.

## 6. Repère (référence descriptive, PAS règle succès/échec)

Le lot v3.5.4 a donné T = 2,2565 pour 5 contrôles sur 6
(ΔT −0,013 vs Tc d'Onsager 2,2692). Ce repère sert à situer T_0 de la
cascade, pas à déclarer le test réussi ou raté. Le jugement se fait
sur la comparaison réel-vs-nul (section 7).

## 7. Jugement (écrit avant les runs)

- (a) T_0(V1) converti en T, comparé à la distribution des T_0 sur les
  20 nuls V5 (médiane, étendue, rang du réel parmi les 21 valeurs).
- (b) Structure 5 zones strictement ordonnées
  (T_-2 < T_-1 < T_0 < T_+1 < T_+2, statut `ok`) : présente sur V1 ?
  Fréquence de présence sur les 20 nuls ?
- (c) Attribution E_thermal : si T_0 persiste en V3 (M mélangé) et
  s'efface en V4 (T mélangé), le signal vient de T seul
  (construction) ; si l'inverse, il vient de M ; si les deux
  l'effacent, il vient du couple (T, M).
- (d) Tout statut `insufficient_data` ou repli arithmétique
  (t0 ± min_dist) est rapporté comme tel, jamais comme un seuil mesuré.
- Aucun verdict « pas de signal » à partir d'une seule série : le
  verdict porte sur chaque série séparément, réel contre nul.

## 8. Sorties (tout gardé, rien dans /tmp)

- `harness_cascade.py` — harnais (lecture seule des sources et données).
- `resultats_cascade.json` — sorties complètes de la cascade par série.
- `resultats_cascade.csv` — synthèse une ligne par run.
- `RAPPORT.md` — verdict réel-vs-nul, loupe par loupe.
- `sources/` — copies SHA-vérifiées des 3 fichiers HP.
- Publication : dépôt privé FindPrint/Code, dossier `hp-cascade-test/`,
  fichiers texte seulement (aucun binaire).

## 9. Ce que ce test ne fait PAS

- Il ne teste pas la prédiction HP (L1–L7), ni le discriminateur
  bruit-information, ni la saliency : chacun aura son protocole propre.
- Il ne valide pas les dossiers PC de Zackary (inaccessibles depuis
  cette VM) : il valide la loupe cascade sur le banc disponible ici.
- Il n'utilise pas la consolidation en un seul fichier : le test porte
  sur le code reçu (3 fichiers). La consolidation est une étape
  séparée, avec sa propre vérification d'équivalence.
